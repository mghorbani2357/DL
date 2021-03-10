""

import json
from urllib.request import urlopen, Request
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock
import time
from threading import Thread


class Downloader:
    block_size = 8192
    threads = 8
    url = None
    download_path = None
    content_type = None
    downloaded_size = 0
    file_size = 0
    file_name = None
    download_file = None
    pause_able = False
    connection = None
    speed = 0
    percent = 0
    remaining_time = 0
    headers = None
    __lock = Lock()
    __downloading = False
    remaining_partitions = list()

    def __init__(self, url, download_path, threads=8, block_size=8196, limited_speed=float('inf')):
        """
            Args:
                url(str): Download file URL
                download_path(str): Download path of file
                threads(int): Threads count
                block_size(int) : Download size in each block
                limited_speed(int|float) : Speed limiter for download speed
        """
        self.url = url
        self.download_path = download_path
        self.thread_pool = ThreadPool(self.threads)
        self.threads = threads
        self.block_size = block_size
        self.limited_speed = limited_speed
        self.get_details()

    @property
    def downloading(self):
        return self.__downloading

    def __speed_meter(self):
        previous_downloaded_size = self.downloaded_size
        while self.__downloading:
            self.speed = (self.downloaded_size - previous_downloaded_size) * 10
            self.percent = float(self.downloaded_size * 100 / self.file_size)
            self.remaining_time = (self.file_size - self.downloaded_size) / self.speed if self.speed != 0 else float(
                'inf')
            previous_downloaded_size = self.downloaded_size
            time.sleep(0.5)

    def get_details(self):
        u = urlopen(self.url)
        meta = u.info()
        self.file_name = self.url.split('/')[-1]
        self.file_size = int(meta.get("Content-Length"))
        self.content_type = meta.get("Content-Type")
        self.connection = meta.get("Connection")
        self.headers = meta
        if meta.get('Accept-Ranges') == 'bytes':
            self.pause_able = True

    def pause(self):
        self.__downloading = False

    def download(self):
        self.__downloading = True
        self.download_file = open(self.download_path, 'w+b')
        self.download_file.seek(self.file_size - 1)
        self.download_file.write(b'\0')
        self.download_file.seek(0)
        Thread(target=self.__speed_meter).start()
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

        self.download_file.close()
        self.__downloading = False

    def threaded_download(self, download_partition):
        beginning_pointer, ending_pointer = download_partition
        if self.__downloading:

            self.__lock.acquire()
            while self.speed > self.limited_speed:
                time.sleep(0.1)
            self.__lock.release()

            request = Request(self.url)
            request.add_header("Range", f"bytes={beginning_pointer}-{ending_pointer}")
            with urlopen(request) as response:
                buffer = response.read(self.block_size)
                self.write_file(buffer, beginning_pointer)
        else:
            self.__lock.acquire()
            self.remaining_partitions.append(download_partition)
            self.__lock.release()

    def single_thread_download(self):
        request = Request(self.url)
        response = urlopen(request)

        while buffer := response.read(self.block_size):
            while self.speed > self.limited_speed:
                time.sleep(0.1)
            self.download_file.write(buffer)
            self.downloaded_size += len(buffer)

    def write_file(self, buffer, pointer):
        self.download_file.seek(pointer)
        self.download_file.write(buffer)
        self.__lock.acquire()
        self.downloaded_size += len(buffer)
        self.__lock.release()


class DownloadManager:
    downloads = list()
    parallel_downloads = 3
    download_threads = 8
    block_size = 8196
    limit_speed = float('inf')

    def __init__(self, json_db_path):
        self.json_db_path = json_db_path
        with open(self.json_db_path, 'r') as json_file:
            self.json_db = json.load(json_file)

    def save_state(self):
        with open(self.json_db_path, 'w') as json_file:
            json.dump(self.json_db, json_file)

    def add_download(self, url, download_path, threads=8, block_size=8196, limited_speed=float('inf')):
        self.downloads.append(Downloader(url, download_path, threads, block_size, limited_speed))
