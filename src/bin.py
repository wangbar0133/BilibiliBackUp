import os
import json
import platform
import ctypes

from config import Config


class Video(object):
    """视频对象"""
    def __init__(self, url=None, av=None, bv=None, aid=None):
        if url:
            self.url = url
            self.bv = url.split("/")[-1]
            self.av = Bv2av().dec(self.bv)
        if av:
            self.url = "https://www.bilibili.com/video/" + Bv2av().enc(av)
            self.bv = Bv2av().enc(av)
            self.av = av
        if bv:
            self.url = "https://www.bilibili.com/video/" + bv
            self.bv = bv
            self.av = Bv2av().dec(bv)
        if aid:
            self.av = "av" + aid
            self.bv = Bv2av().enc(av)
            self.url = "https://www.bilibili.com/video/" + bv

        self.video = {
            "bv": self.bv,
            "av": self.av,
            "url": self.url,
            "name": self.name,
            "path": self.path
        }
        self.video_dict = json.loads(self.video.__str__().replace("'", '"').replace('""', "None"))

    def add_detial(self, name=None, path=None):
        self.name = name
        self.path = path


def get_free_space_mb(folder):
    """通过文件夹获取文件夹剩余空间"""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024/1024.


def download_video(url, path_storge, path_cookie):
    """下载单个视频,提供url,存储单个文件夹,cookies的位置"""
    path_storge_single = make_file(url, path_storge)
    cmd = 'you-get -o  ' + path_storge_single + ' -c ' + path_cookie + ' --playlist ' + url
    os.system(cmd)
    print(url[31:] + "下载完成")


def make_file(url, path_storge):
    """创建视频文件夹"""
    path_storge_single = path_storge + url[31:]
    if os.path.exists(path_storge_single):
        print(path_storge_single + "paths is exist>>>>")
    else:
        os.makedirs(path_storge_single)
    return path_storge_single


class Bv2av(object):
    """avbv相互转化"""

    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    def __init__(self):
        for i in range(58):
            self.tr[self.table[i]]=i

    def dec(self, x):
        """bv转av"""
        r = 0
        for i in range(6):
            r += self.tr[x[self.s[i]]] * 58 ** i
        return (r - self.add) ^ self.xor

    def enc(self, x):
        """av转bv"""
        x = (x ^ self.xor) + self.add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[self.s[i]] = self.table[x // 58 ** i % 58]
        return ''.join(r)


class Storge(object):

    def __init__(self):
        self.disk_list = Config.storge_list

    def if_video_exist(self, path):
        for file in os.listdir(path):
            if ".mp4" or "flv" in file:
                return True
            else:
                return False

    def get_video_folder_list(self):
        video_folder_list = []
        for path in self.disk_list:
            for folder in os.listdir(path):
                if self.if_video_exist(folder):
                    video_folder_list.append(folder)
        return video_folder_list

    def get_video_from_folder(self, folder_list):
        video_list = list()
        for folder in folder_list:
            videostring = folder.split("/")[-1]
            if videostring.isdigit():
                video_list.append(Video(aid=videostring))
            elif videostring[0, 1] == "av":
                video_list.append(Video(av=videostring))
            elif videostring[0, 1] == "BV":
                video_list.append(Video(bv=videostring))
        return video_list

    def scan(self):
        video_folder_list = self.get_video_folder_list()
        video_list = self.get_video_from_folder(video_folder_list)


if __name__ == "__main__":
    # print(Bv2av().dec("BV1c64y1y7nt"))
    print("123456".isdigit())
