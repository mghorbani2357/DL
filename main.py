from urllib.request import urlopen, Request
from hurry.filesize import size
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor


class Downloader:
    status = dict()
    block_size = 8192
    block_count = 0
    download_block = 0
    file_size = 0
    url = ''
    file_path = ''
    file_name = ''

    def __init__(self, threads=8):
        self.threads = threads

    def write_file(self, buffer, seek_address):
        with open(self.file_path, 'wb') as file:
            file.seek(seek_address * self.block_size)
            file.write(buffer)
        self.download_block += 1

        # print("\rDownloading: %s Bytes: %s" % (self.file_name, size(self.download_block * self.block_size)), end='')

        print(f"\rDownloading state: {size(self.download_block * self.block_size)}  [%3.2f%%]" % (
                self.download_block * self.block_size * 100. / self.file_size),end='')

    def download(self, url, file_path):
        u = urlopen(url)
        meta = u.info()
        self.file_name = url.split('/')[-1]
        self.file_size = int(meta.get("Content-Length"))
        self.block_count = int(self.file_size / self.block_size)
        self.file_path = file_path
        each_thread_blocks = int(self.block_count / self.threads)

        # pool = ThreadPool(self.threads)
        download_states = ((url, i * each_thread_blocks * self.block_size, each_thread_blocks) for i in
                           range(self.threads))

        # for i in range(self.threads):
        #     download_states.append((url, i * each_thread_blocks * self.block_size, each_thread_blocks))

        # pool.map(self.download, download_states)

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for i in range(self.threads):
                executor.submit(self.download_thread, url, i * each_thread_blocks * self.block_size, each_thread_blocks)

    def download_thread(self, url, start_point, download_length):
        request = Request(url)
        request.add_header("Range", "bytes=%s-" % start_point)
        file_url = urlopen(request)

        for download_point in range(download_length):
            buffer = file_url.read(self.block_size)
            self.write_file(buffer, start_point + download_point)

            if not buffer:
                break


idm_url = "https://dl2.soft98.ir/soft/i/Internet.Download.Manager.6.38.Build.11.exe"

downloader = Downloader()

downloader.download(idm_url, 'IDM.exe')

# class DownloadManager:
#     def __init__(self):
#         pass

# status = f"\rDownloading state: {size(downloaded_size)}  [%3.2f%%]" % (
#         downloaded_size * 100. / self.file_size)
