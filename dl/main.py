import sys

import webview

from dl.Downloader import Downloader
from dl.db_manager import DBManager
from dl.utils import sizeof_fmt

window = new_window = None


class NewDownloadApi:
    def cancel(self):
        new_window.destroy()

    def select_save_in(self, filename: str):
        result = new_window.create_file_dialog(webview.SAVE_DIALOG, directory='/', save_filename=filename)
        return result


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def init(self):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        return response

    def new_download(self, url, name):
        self.dl = Downloader(url, name)
        new_api = NewDownloadApi()
        new_window = webview.create_window('New download', "new.html", js_api=new_api, min_size=(600, 210))
        new_window.resize(650, 250)
        webview.start(new_window, debug=True)
        # new_window.evaluate_js('$("#info-url").val("%s");$("#info-size").val("%s");' % (url, sizeof_fmt(self.dl.file_size)))
        # new_window.evaluate_js(
        #     'document.getElementById("info-url").innerText = "%s";document.getElementById("info-size").innerText = "%s";' % (
        #     url, sizeof_fmt(self.dl.file_size)))
        return {
            'name': name,
            'size': sizeof_fmt(self.dl.file_size)
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
