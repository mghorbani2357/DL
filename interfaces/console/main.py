import argparse
from threading import Thread
from dl import Downloader
from utils.query import download_state, print_download_state

parser = argparse.ArgumentParser(description='Downloader.')

parser.add_argument('strings', metavar='L', type=str, nargs='+',
                    help='an string for the download')
parser.add_argument('--o', dest='output', help='output file path for download (default: file name from url)')

if __name__ == '__main__':
    args = parser.parse_args()
    for url in args.strings:
        download = Downloader(url, args.output if args.output else url.split('/')[-1])
        Thread(target=download.download).start()
        thread = Thread(target=print_download_state, args=(download,))
        thread.start()
        thread.join()
