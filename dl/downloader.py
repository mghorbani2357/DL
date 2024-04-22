import copy
import json
import math
import uuid
from urllib.request import urlopen, Request
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock
import time
from threading import Thread

store_key = ['_Downloader__url', '_Downloader__download_path', 'download_id', '_Downloader__threads',
             '_Downloader__block_size'
    , 'limited_speed', '_Downloader__download_block_count', '_Downloader__pause_able', '_Downloader__file_size']


class Downloader:
    __check_list = list()
    __to_be_downloaded = list()
    # __block_size = 8192
    # __threads = 8
    # __url = None
    # __download_path = None
    __content_type = None
    __downloaded_size = 0
    __file_size = 0
    # __file_name = None
    __download_file = None
    __pause_able = False
    __connection = None
    __speed = 0
    __percent = 0
    __remaining_time = 0
    # __update_meter = 0.5
    __headers = None
    __lock = Lock()
    __downloading = False
    __partitions = list()
    __thread_pool = None

    def __init__(self, url, download_path, download_state_path=None, download_id=str(uuid.uuid4()), threads=8,
                 block_size=2048, limited_speed=float('inf'), download_block_count=64, update_meter=0.5):
        """

            Args:
                url(str): Download file URL
                download_id(str): Download identifier
                download_path(str): Download path of file
                download_state_path(str|None): Download file state
                threads(int): Threads count
                block_size(int) : Download size in each block
                limited_speed(int|float) : Speed limiter for download speed
        """
        self.__url = url
        self.download_id = download_id
        self.__download_path = download_path
        self.__threads = threads
        self.__block_size = block_size
        self.__download_block_count = download_block_count
        self.limited_speed = limited_speed

        u = urlopen(self.__url)
        meta = u.info()
        self.__file_name = self.__url.split('/')[-1]
        self.__file_size = int(meta.get("Content-Length"))
        self.__content_type = meta.get("Content-Type")
        self.__connection = meta.get("Connection")
        self.__headers = meta
        if meta.get('Accept-Ranges') == 'bytes':
            self.__pause_able = True

        # self.get_details()

    @staticmethod
    def load_from_str():
        pass
        # return Downloader()

    # @staticmethod
    def export_to_str(self):
        # 'download_state_path',
        export = '::'.join([str(self.__dict__[item]) for item in store_key])
        print(export)
        # x = self.__dict__
        # print(json.dumps(x))
        # buffer = ''
        # for key, value in self.__dict__.items():
        #     buffer +=

    def resume(self, remaining_partitions):
        self.__partitions = remaining_partitions
        self.download()

    def __speed_meter(self):
        previous_downloaded_size = self.__downloaded_size
        while self.__downloading:
            self.__speed = (self.__downloaded_size - previous_downloaded_size) / self.update_meter
            self.__percent = float(self.__downloaded_size * 100 / self.__file_size)
            self.__remaining_time = ((self.__file_size - self.__downloaded_size) / self.__speed) \
                if self.__speed != 0 else float('inf')
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
        self.__thread_pool = ThreadPool(self.__threads)
        self.__downloading = True
        self.__download_file = open(self.__download_path, 'w+b')
        # Reserve file size
        self.__download_file.seek(self.__file_size - 1)
        self.__download_file.write(b'\0')
        self.__download_file.seek(0)
        Thread(target=self.__speed_meter).start()
        if self.__pause_able:
            if not self.__partitions:
                self.__partitions = [
                    (i, i * (self.__block_size * self.__download_block_count),
                     min((i + 1) * (self.__block_size * self.__download_block_count) - 1, self.__file_size))
                    for i in range(math.ceil(self.__file_size / (self.__block_size * self.__download_block_count)))
                ]
                self.__check_list = [False for _ in range(len(self.__partitions))]
                self.__to_be_downloaded = copy.deepcopy(self.__partitions)
            else:
                self.__to_be_downloaded = list()
                for i in range(len(self.__partitions)):
                    if not self.__check_list[i]:
                        self.__to_be_downloaded.append(self.__partitions[i])

            self.__thread_pool.map(self.threaded_download, self.__to_be_downloaded)
        else:
            self.single_thread_download()

        self.__download_file.close()
        self.__downloading = False

    def threaded_download(self, partition):
        index, beginning_pointer, ending_pointer = partition
        if self.__downloading:

            self.__lock.acquire()
            while self.__speed > self.limited_speed:
                time.sleep(0.1)
            self.__lock.release()

            request = Request(self.__url)
            request.add_header("Range", f"bytes={beginning_pointer}-{ending_pointer}")
            buffer = b''
            with urlopen(request) as response:
                for _ in range(self.__download_block_count):
                    block_buffer = response.read(self.__block_size)
                    buffer += block_buffer
                    self.__lock.acquire()
                    self.__downloaded_size += len(block_buffer)
                    self.__lock.release()
            self.write_file(buffer, beginning_pointer)
            self.__check_list[index] = True

    def single_thread_download(self):
        request = Request(self.__url)
        response = urlopen(request)

        while buffer := response.read(self.__block_size):
            while self.__speed > self.limited_speed:
                time.sleep(0.1)
            self.__download_file.write(buffer)
            self.__downloaded_size += len(buffer)

    def write_file(self, buffer, pointer):
        self.__lock.acquire()
        self.__download_file.seek(pointer)
        self.__download_file.write(buffer)
        self.__lock.release()

    # region Attributes

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
        return self.__partitions

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
