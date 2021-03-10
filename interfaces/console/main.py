import argparse
import time
from threading import Thread
import humanize
from dl import Downloader

parser = argparse.ArgumentParser(description='Downloader.')

parser.add_argument('strings', metavar='L', type=str, nargs='+',
                    help='an string for the download')
parser.add_argument('--o', dest='output', help='output file path for download (default: file name from url)')


def download_state(downloader: Downloader):
    state = f'{downloader.downloaded_size * 100 / downloader.file_size:3.2f}% {downloader.file_name:>30} '
    state += f' {humanize.naturalsize(downloader.speed)} '
    state += f'[{humanize.naturalsize(downloader.downloaded_size)}/{humanize.naturalsize(downloader.file_size)}] '
    if downloader.remaining_time != float('inf'):
        state += f' {humanize.naturaldelta(downloader.remaining_time)} '

    return state


def print_download_state(downloader: Downloader):
    while downloader.downloading:
        print('\r', download_state(downloader), end='')
        time.sleep(0.5)
    print('\r', download_state(downloader), end='')


if __name__ == '__main__':
    args = parser.parse_args()
    for url in args.strings:
        download = Downloader(url, args.output if args.output else url.split('/')[-1])
        Thread(target=download.download).start()
        thread = Thread(target=print_download_state, args=(download,))
        thread.start()
        thread.join()
