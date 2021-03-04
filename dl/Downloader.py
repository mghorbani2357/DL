from urllib.request import urlopen, Request
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock
from multiprocessing.queues import Queue
import time


class Downloader:
    block_size = 8192
    threads = 8
    url = None
    download_path = None
    downloaded_size = 0
    file_size = 0
    file_name = None
    download_file = None
    pause_able = False
    speed = 0
    percent = 0
    remaining_time = 0
    __lock = Lock()
    __downloading = False
    remaining_partitions = list()

    def __init__(self, url, download_path, threads=8, block_size=8196):
        self.url = url
        self.download_path = download_path
        self.thread_pool = ThreadPool(self.threads)
        self.threads = threads
        self.block_size = block_size
        self.get_details()

    def __speed_meter(self):
        previous_downloaded_size = self.downloaded_size
        current_downloaded_size = self.downloaded_size
        while self.__downloading:
            self.speed = (current_downloaded_size - previous_downloaded_size) * 10
            self.percent = self.downloaded_size * 100 / self.file_size
            self.remaining_time = (self.file_size - self.downloaded_size) / self.speed
            time.sleep(0.1)
            previous_downloaded_size = current_downloaded_size
            current_downloaded_size = self.downloaded_size

    def get_details(self):
        u = urlopen(self.url)
        meta = u.info()

        self.file_name = self.url.split('/')[-1]
        self.file_size = int(meta.get("Content-Length"))

        if meta.get('Accept-Ranges') == 'bytes':
            self.pause_able = True

    def pause(self):
        self.__downloading = False

    def download(self):

        self.download_file = open(self.download_path, 'w+b')
        self.download_file.seek(self.file_size - 1)
        self.download_file.write(b'\0')
        self.download_file.seek(0)
        self.__downloading = True

        if self.pause_able:

            if not self.remaining_partitions:

                i = 0
                partitions = list()
                while True:
                    if self.block_size * (i + 1) > self.file_size:
                        if self.file_size % self.block_size != 0:
                            partitions.append([i * self.block_size, self.file_size])

                        break

                    partitions.append([i * self.block_size, (i + 1) * self.block_size])
                    i += 1
            else:
                partitions = self.remaining_partitions

            self.thread_pool.map(self.threaded_download, partitions)
        else:
            self.single_thread_download()

        self.__downloading = False
        self.download_file.close()

    def threaded_download(self, download_partition):
        beginning_pointer, ending_pointer = download_partition
        if self.__downloading:
            request = Request(self.url)
            request.add_header("Range", f"bytes={beginning_pointer}-{ending_pointer}")
            response = urlopen(request)
            buffer = response.read(self.block_size)
            self.write_file(buffer, beginning_pointer)
            self.__lock.acquire()
            self.downloaded_size += len(buffer)
            self.__lock.release()
        else:
            self.__lock.acquire()
            self.remaining_partitions.append(download_partition)
            self.__lock.release()

    def single_thread_download(self):
        request = Request(self.url)
        response = urlopen(request)

        while buffer := response.read(self.block_size):
            self.download_file.write(buffer)
            self.downloaded_size += len(buffer)

    def write_file(self, buffer, pointer):
        self.download_file.seek(pointer)
        self.download_file.write(buffer)
