import threading

from bin import download_video
from config import Config


class Download(object):

    def __init__(self, url_list):
        self.path_cookie = Config.path_cookie
        self.storge_list = Config.storge_list
        self.url_list = url_list

    def go(self):
        threads = []
        for url in self.url_list:
            threads.append(threading.Thread(target=download_video, args=[url, self.path_cookie, self.storge_list, ]))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print("下载完成!")
