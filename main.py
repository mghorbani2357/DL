# # import argparse
# # from Downloader import Downloader
# #
# # # idm_url = "https://dl2.soft98.ir/soft/i/Internet.Download.Manager.6.38.Build.11.exe"
# #
# #
# # parser = argparse.ArgumentParser(description='Downloader.')
# #
# # parser.add_argument('strings', metavar='L', type=str, nargs='+',
# #                     help='an string for the download')
# # parser.add_argument('--o', dest='output', help='output file path for download (default: file name from url)')
# #
# # if __name__ == '__main__':
# #     args = parser.parse_args()
# #     downloader = Downloader()
# #     for url in args.strings:
# #         downloader.download(url, args.output if args.output else url.split('/')[-1])
#
#
# # from multiprocessing import Lock
# # from multiprocessing.pool import ThreadPool
# # from multiprocessing.queues import Queue
# # import multiprocessing as mp
# #
# # i = 0
# #
# #
# # def func(q):
# #     global i
# #
# #     while q.qsize() > 0:
# #         q.get()
# #         i += 1
# #
# #
# # lock = Lock()
# # ctx = mp.get_context('spawn')
# # q = ctx.Queue()
# # pool = ThreadPool(8)
# #
# # for i in range(30):
# #     q.put(i)
# #
# # print(q.qsize())
# #
# # pool.map(func, (q,))
# #
# # print(q.qsize())
# # print(i)
#
# #
# # from multiprocessing import Queue
# #
# # colors = ['red', 'green', 'blue', 'black']
# # cnt = 1
# # # instantiating a queue object
# # queue = Queue()
# # print('pushing items to queue:')
# # for color in colors:
# #     print('item no: ', cnt, ' ', color)
# #     queue.put(color)
# #     cnt += 1
# #
# #
# # def func(q):
# #     cnt = 0
# #     while not queue.empty():
# #         print('item no: ', cnt, ' ', queue.get())
# #         cnt += 1
# #
# # pool.map(func, (queue,))
# #
# # print(cnt)
#
# from multiprocessing.pool import ThreadPool
# from multiprocessing import Queue
# import time
#
# work = (["A", 5], ["B", 2], ["C", 1], ["D", 3])
#
#
# def work_log(work_data):
#     print(" Process %s waiting %s seconds" % (work_data[0], work_data[1]))
#     time.sleep(int(work_data[1]))
#     print(" Process %s Finished." % work_data[0])
#
#
# def pool_handler():
#     p = ThreadPool(4)
#     p.map(work_log, work)
#
#
# if __name__ == '__main__':
#     pool_handler()


from dl.Downloader import Downloader

downloader = Downloader()

downloader.download('file:///home/bluesp/Downloads/Soul.2020.720p.WEBRip.800MB.x264-GalaxyRG[TGx]/Soul.2020.720p.WEBRip.800MB.x264-GalaxyRG.mkv',
                    'Soul.2020.720p.WEBRip.800MB.x264-GalaxyRG.mkv')
