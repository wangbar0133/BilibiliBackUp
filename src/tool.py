import time

import requests

from mongodb import Db

data_list = Db().get_all_bv()

bv_list = list()
for data in data_list:
    bv_list.append(data['bv'])




miss_list = list()
for bv in bv_list:
    url = "http://api.bilibili.com/x/web-interface/view?bvid={}".format(bv)
    resp = requests.get(url).json()
    if resp["message"] == "稿件不可见":
        miss_list.append(bv)
        print(bv)
    elif resp["code"] == -412:
        time.sleep(60)

print("************************************************")

