import argparse
import os.path
from threading import Thread
from dl import Downloader
from utils import *
from . import consts

parser = argparse.ArgumentParser(description='Downloader.')

parser.add_argument('strings', metavar='L', type=str, nargs='+',
                    help='an string for the download')
parser.add_argument('--o', dest='output', help="output path to download (default: file name at the end of url)")


if __name__ == '__main__':
    # Initialize
    if not os.path.exists(consts.LOCAL_DIR_DIRECTORY):
        os.mkdir(consts.LOCAL_DIR_DIRECTORY)

    args = parser.parse_args()
    for url in args.strings:
        download = Downloader(url, args.output if args.output else extract_file_name(url))
        Thread(target=download.download).start()
        thread = Thread(target=print_download_state, args=(download,))
        thread.start()
        thread.join()
