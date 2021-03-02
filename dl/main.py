import sys

import webview


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def init(self):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        return response


if __name__ == '__main__':
    api = Api()
    window = webview.create_window('Downloader', "index.html", js_api=api, min_size=(800, 600))
    webview.start()
