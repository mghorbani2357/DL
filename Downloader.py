from urllib.request import urlopen, Request
from hurry.filesize import size
from threading import Thread


class Downloader:
    block_size = 8192
    threads = 8
    url = None
    download_path = None
    downloaded_size = 0
    file_size = 0
    file_name = None
    download_file = None

    def __init__(self, threads=8, block_size=8196):
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

        thread_download_size = int(self.file_size / self.threads)

        threads = list()
        for i in range(self.threads - 1):
            threads.append(
                Thread(target=self.download_thread, args=(i * thread_download_size, (i + 1) * thread_download_size)))

        i += 1
        threads.append(Thread(target=self.download_thread, args=(i * thread_download_size, self.file_size)))

        for thread in threads:
            # thread.setDaemon(True)
            thread.start()

        for thread in threads:

            thread.join()

        self.download_file.close()

    def download_thread(self, start, end):
        print("I'm working")
        request = Request(self.url)
        request.add_header("Range", f"bytes={start}-{end}")
        download_url = urlopen(request)

        current_download_point = start
        while current_download_point < end:

            buffer = download_url.read(self.block_size)
            self.write_file(buffer, current_download_point)
            current_download_point += len(buffer)

            if not buffer:
                break

    def write_file(self, buffer, seek_address):
        self.download_file.seek(seek_address)
        self.download_file.write(buffer)
        self.downloaded_size += len(buffer)

        print(f"\r\033[kDownloading state: {size(self.downloaded_size)}  [%3.2f%%]" % (
                self.downloaded_size * 100. / self.file_size), end='')
