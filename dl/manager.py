import json
from .downloader import *


class DownloadManager:
    downloads = dict()
    parallel_downloads = 3
    download_threads = 8
    block_size = 8196
    limit_speed = float('inf')
    counter = 0

    def __init__(self, json_db_path):
        # self.json_db_path = json_db_path
        # with open(self.json_db_path, 'r') as json_file:
        #     self.json_db = json.load(json_file)
        pass

    # def save_state(self):
    #     with open(self.json_db_path, 'w') as json_file:
    #         json.dump(self.json_db, json_file)

    def add(self, url, download_path, threads=8, block_size=8196, limited_speed=float('inf')):
        self.counter += 1
        self.downloads[self.counter] = Downloader(url, download_path, threads, block_size, limited_speed)

    def start(self, download_id):
        self.downloads[download_id].download()

    def pause(self, download_id):
        self.downloads[download_id].pause()

    def resume(self, download_id):
        self.downloads[download_id].resume()

    def delete(self, download_id):
        self.downloads.pop(download_id)
