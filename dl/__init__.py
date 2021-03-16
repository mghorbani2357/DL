"""Advance downloader"""
import json
from urllib.request import urlopen, Request
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock
import time
from threading import Thread

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions


class Downloader:
    __block_size = 8192
    __threads = 8
    __url = None
    __download_path = None
    __content_type = None
    __downloaded_size = 0
    __file_size = 0
    __file_name = None
    __download_file = None
    __pause_able = False
    __connection = None
    __speed = 0
    __percent = 0
    __remaining_time = 0
    update_meter = 0.5
    __headers = None
    __lock = Lock()
    __downloading = False
    __remaining_partitions = list()

    # region attributes
    @property
    def pause_able(self):
        return self.__pause_able

    @property
    def speed(self):
        return self.__speed

    @property
    def percent(self):
        return self.__percent

    @property
    def remaining_time(self):
        return self.__remaining_time

    @property
    def remaining_partitions(self):
        return self.__remaining_partitions

    @property
    def content_type(self):
        return self.__content_type

    @property
    def downloaded_size(self):
        return self.__downloaded_size

    @property
    def file_size(self):
        return self.__file_size

    @property
    def file_name(self):
        return self.__file_name

    @property
    def download_file(self):
        return self.__download_file

    @property
    def block_size(self):
        return self.__block_size

    @property
    def threads(self):
        return self.__threads

    @property
    def url(self):
        return self.__url

    @property
    def download_path(self):
        return self.__download_path

    @property
    def downloading(self):
        return self.__downloading

    # endregion

    def __init__(self, url, download_path, threads=8, block_size=8196, limited_speed=float('inf')):
        """

            Args:
                url(str): Download file URL
                download_path(str): Download path of file
                threads(int): Threads count
                block_size(int) : Download size in each block
                limited_speed(int|float) : Speed limiter for download speed
        """
        self.__url = url
        self.__download_path = download_path
        self.thread_pool = ThreadPool(self.__threads)
        self.__threads = threads
        self.__block_size = block_size
        self.limited_speed = limited_speed
        self.get_details()

    def __speed_meter(self):
        previous_downloaded_size = self.__downloaded_size
        while self.__downloading:
            self.__speed = (self.__downloaded_size - previous_downloaded_size) / self.update_meter
            self.__percent = float(self.__downloaded_size * 100 / self.__file_size)
            self.__remaining_time = (self.__file_size - self.__downloaded_size) / self.__speed if self.__speed != 0 else float('inf')
            previous_downloaded_size = self.__downloaded_size
            time.sleep(self.update_meter)

    def get_details(self):
        u = urlopen(self.__url)
        meta = u.info()
        self.__file_name = self.__url.split('/')[-1]
        self.__file_size = int(meta.get("Content-Length"))
        self.__content_type = meta.get("Content-Type")
        self.__connection = meta.get("Connection")
        self.__headers = meta
        if meta.get('Accept-Ranges') == 'bytes':
            self.__pause_able = True

    def pause(self):
        self.__downloading = False

    def download(self):
        self.__downloading = True
        self.__download_file = open(self.__download_path, 'w+b')
        self.__download_file.seek(self.__file_size - 1)
        self.__download_file.write(b'\0')
        self.__download_file.seek(0)
        Thread(target=self.__speed_meter).start()
        if self.__pause_able:

            if not self.__remaining_partitions:

                i = 0
                partitions = list()
                while True:
                    if self.__block_size * (i + 1) > self.__file_size:
                        if self.__file_size % self.__block_size != 0:
                            partitions.append([i * self.__block_size, self.__file_size])

                        break

                    partitions.append([i * self.__block_size, (i + 1) * self.__block_size])
                    i += 1
            else:
                partitions = self.__remaining_partitions
            self.thread_pool.map(self.threaded_download, partitions)
        else:
            self.single_thread_download()

        self.__download_file.close()
        self.__downloading = False

    def threaded_download(self, download_partition):
        beginning_pointer, ending_pointer = download_partition
        if self.__downloading:

            self.__lock.acquire()
            while self.__speed > self.limited_speed:
                time.sleep(0.1)
            self.__lock.release()

            request = Request(self.__url)
            request.add_header("Range", f"bytes={beginning_pointer}-{ending_pointer}")
            with urlopen(request) as response:
                buffer = response.read(self.__block_size)
                self.write_file(buffer, beginning_pointer)
        else:
            self.__lock.acquire()
            self.__remaining_partitions.append(download_partition)
            self.__lock.release()

    def single_thread_download(self):
        request = Request(self.__url)
        response = urlopen(request)

        while buffer := response.read(self.__block_size):
            while self.__speed > self.limited_speed:
                time.sleep(0.1)
            self.__download_file.write(buffer)
            self.__downloaded_size += len(buffer)

    def write_file(self, buffer, pointer):
        self.__download_file.seek(pointer)
        self.__download_file.write(buffer)
        self.__lock.acquire()
        self.__downloaded_size += len(buffer)
        self.__lock.release()


class DownloadManager:
    downloads = dict()
    parallel_downloads = 3
    download_threads = 8
    block_size = 8196
    limit_speed = float('inf')
    counter = 0

    def __init__(self, json_db_path):
        self.json_db_path = json_db_path
        with open(self.json_db_path, 'r') as json_file:
            self.json_db = json.load(json_file)

    def save_state(self):
        with open(self.json_db_path, 'w') as json_file:
            json.dump(self.json_db, json_file)

    def add_download(self, url, download_path, threads=8, block_size=8196, limited_speed=float('inf')):
        self.counter += 1
        self.downloads[self.counter] = (Downloader(url, download_path, threads, block_size, limited_speed))

    def start_download(self, download_id):
        self.downloads[download_id].download()

    def pause_download(self, download_id):
        self.downloads[download_id].pause()
