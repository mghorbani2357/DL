from threading import Thread
from dl import Downloader
from utils.query import download_state, print_download_state

if __name__ == '__main__':
    while True:
        pass
        # download = Downloader(url, args.output if args.output else url.split('/')[-1])
        # Thread(target=download.download).start()
        # thread = Thread(target=print_download_state, args=(download,))
        # thread.start()
        # thread.join()
