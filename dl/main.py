import sys

import webview

from dl.Downloader import Downloader
from dl.db_manager import DBManager

window = None  # new_window = None


# class NewDownloadApi:
#     def __init__(self):
#         self.cancel_heavy_stuff_flag = False
#
#     def select_save_in(self, filename: str):
#         result = new_window.create_file_dialog(webview.SAVE_DIALOG, directory='/', save_filename=filename)
#         return result

class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def init(self):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        return response

    def new_download(self, url, name):
        # new_api = NewDownloadApi()
        # new_window = webview.create_window('New download', "new.html", js_api=new_api, min_size=(500, 350))
        # new_window.resize(500, 350)
        # webview.start(new_window)
        self.dl = Downloader(url, name)
        return {
            'name': name,
            'size': self.dl.get_size()
        }
    def start_download(self):
        self.dl.download()

    def getStatus(self):
        return {
            'percent': self.dl.percent(),
            'speed': self.dl.speed
        }
    # def save_file_dialog(self, filename: str):
    #     time.sleep(5)
    #     result = window.create_file_dialog(webview.SAVE_DIALOG, directory='/', save_filename=filename)
    #     print(result)


if __name__ == '__main__':
    api = Api()
    window = webview.create_window('Downloader', "index.html", js_api=api, min_size=(800, 600))
    webview.start(window)
    # db = DBManager("downloader.sqlite")
    # print(db.delete('test', {"id": [1, 2, 3, 4], "name": "ali"}))
