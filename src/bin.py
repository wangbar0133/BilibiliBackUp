import os
import json
import platform
import ctypes
from os.path import join, getsize

from config import Config
from mongodb import Db


class Video(object):
    """视频对象"""
    def __init__(self, url=None, av=None, bv=None, aid=None, name=None, path=None):
        if url:
            self.url = url
            self.bv = url.split("/")[-1]
            self.av = Bv2av().dec(self.bv)
        if av:
            self.av = av
            self.url = "https://www.bilibili.com/video/" + Bv2av().enc(int(av[2:]))
            self.bv = Bv2av().enc(int(av[2:]))
        if bv:
            self.url = "https://www.bilibili.com/video/" + bv
            self.bv = bv
            self.av = av + str(Bv2av().dec(bv[2:]))
        if aid:
            self.av = "av" + aid
            self.bv = Bv2av().enc(int(av[2:]))
            self.url = "https://www.bilibili.com/video/" + bv

        self.name = name.replace('"', '’').replace("'", '’')

        if path:
            self.path = path
            size = 0
            for root, dirs, files in os.walk(path):
                size += sum([getsize(join(root, name)) for name in files])
            self.size = size/1024/1024

        self.video = {
            "bv": self.bv,
            "av": self.av,
            "url": self.url,
            "name": self.name,
            "path": self.path,
            "size": self.size
        }
        print(self.video.__str__().replace("'", '"').replace('None', '""'))
        self.video_dict = json.loads(self.video.__str__().replace("'", '"').replace('None', '""'))



def get_free_space_mb(folder):
    """通过文件夹获取文件夹剩余空间"""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024/1024.


def size_format(size):
    if size < 1000:
        return '%i' % size + 'size'
    elif 1000 <= size < 1000000:
        return '%.1f' % float(size/1000) + 'KB'
    elif 1000000 <= size < 1000000000:
        return '%.1f' % float(size/1000000) + 'MB'
    elif 1000000000 <= size < 1000000000000:
        return '%.1f' % float(size/1000000000) + 'GB'
    elif 1000000000000 <= size:
        return '%.1f' % float(size/1000000000000) + 'TB'


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
        if path == '$RECYCLE.BIN':
            return False
        try:
            for file in os.listdir(path):
                if ".mp4" or "flv" in file:
                    return True
                else:
                    return False
        except:
            return False

    def get_video_name(self, path):
        name = ""
        for file in os.listdir(path):
            if ".mp4" or "flv" in file:
                name = name + file
        return name

    def scan(self):
        for disk_path in self.disk_list:
            for folder in os.listdir(disk_path):
                try:
                    if self.if_video_exist(disk_path + folder):
                        videostring = folder.split("\\")[-1]
                        path = disk_path + folder + "\\"
                        name = self.get_video_name(path)
                        if videostring.isdigit():
                            video = Video(aid=videostring, name=name, path=path)
                            Db().insert(video)
                        elif videostring[0: 2] == "av":
                            video = Video(av=videostring, name=name, path=path)
                            Db().insert(video)
                        elif videostring[0: 2] == "BV":
                            video = Video(bv=videostring, name=name, path=path)
                            Db().insert(video)
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    Storge().scan()

