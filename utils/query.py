import time
import humanize
from dl import Downloader


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
