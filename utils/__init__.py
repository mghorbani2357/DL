import time
import humanize
import re

url_pattern = re.compile(r"^(\w*){1}\:\/{2}(\w[\w\-\.{1}]*\w)(\/[[\w\/\.\-\&]*)?\/(\w[\w\.\-]*){1}(\?[\w\=\&]*)?$")


def extract_file_name(url: str) -> str:
    return url_pattern.search(url).group(4)


def validate_url(url):
    x = url_pattern.fullmatch('/' + url)
    # x = re.match(url_regex_pattern, url)
    print(type(x.group()))
    print(x.group())


def download_state(downloader):
    state = f'{downloader.downloaded_size * 100 / downloader.file_size:3.2f}% {downloader.file_name:>30} '
    state += f' [{humanize.naturalsize(downloader.downloaded_size)}/{humanize.naturalsize(downloader.file_size)}] '
    state += f' {humanize.naturalsize(downloader.speed)}/s '
    if downloader.remaining_time != float('inf'):
        state += f' {humanize.naturaldelta(downloader.remaining_time)} '

    return state


def print_download_state(downloader):
    while downloader.downloading:
        print('\r', download_state(downloader), end='')
        time.sleep(0.5)
    print('\r', download_state(downloader), end='')
