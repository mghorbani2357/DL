# import argparse
# from Downloader import Downloader
#
# # idm_url = "https://dl2.soft98.ir/soft/i/Internet.Download.Manager.6.38.Build.11.exe"
#
#
# parser = argparse.ArgumentParser(description='Downloader.')
#
# parser.add_argument('strings', metavar='L', type=str, nargs='+',
#                     help='an string for the download')
# parser.add_argument('--o', dest='output', help='output file path for download (default: file name from url)')
#
# if __name__ == '__main__':
#     args = parser.parse_args()
#     downloader = Downloader()
#     for url in args.strings:
#         downloader.download(url, args.output if args.output else url.split('/')[-1])


from multiprocessing import Lock
from multiprocessing.pool import ThreadPool

i = 0


def func(var):
    global i
    while True:
        lock.acquire()
        if i >= 100:
            break
        i += 1
        lock.release()
    lock.release()


lock = Lock()
pool = ThreadPool(8)

pool.map(func, range(8))

print(i)
