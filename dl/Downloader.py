from urllib.request import urlopen, Request
from multiprocessing.pool import ThreadPool
from multiprocessing import Queue
from multiprocessing import Lock


class Downloader:
    block_size = 8192
    threads = 8
    url = None
    download_path = None
    downloaded_size = 0
    file_size = 0
    file_name = None
    download_file = None
    lock = Lock()

    def __init__(self, threads=8, block_size=8196):
        self.thread_pool = ThreadPool(self.threads)
        self.threads = threads
        self.block_size = block_size

    def download(self, url, download_path):
        u = urlopen(url)
        meta = u.info()

        self.url = url
        self.download_path = download_path
        self.file_name = url.split('/')[-1]
        self.file_size = int(meta.get("Content-Length"))

        self.download_file = open(self.download_path, 'wb')
        self.download_file.seek(self.file_size - 1)
        self.download_file.write(b'\0')

        queue = Queue()

        for i in range(int(self.file_size / self.block_size)):
            queue.put(i * self.block_size)

        self.thread_pool.map(self.download_thread, (queue,))

        self.download_file.close()

    def download_thread(self, queue):
        while not queue.empty():
            pointer = queue.get()
            request = Request(self.url)
            request.add_header("Range", f"bytes={pointer}-{pointer + self.block_size}")
            download_url = urlopen(request)
            buffer = download_url.read(self.block_size)
            self.write_file(buffer, pointer)
        print('done')

    def write_file(self, buffer, pointer):
        self.lock.acquire()
        self.download_file.seek(pointer)
        self.download_file.write(buffer)
        self.downloaded_size += len(buffer)
        print('\r', self.downloaded_size, end='')
        self.lock.release()
