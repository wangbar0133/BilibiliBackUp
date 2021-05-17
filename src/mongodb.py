import json

import pymongo
from bson import json_util


class Db(object):

    def __init__(self):
        try:
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            dblist = myclient.list_database_names()
            mydb = myclient["patchy_backup"]
            self.mycol = mydb["video"]
        except Exception as e:
            print("数据库创建失败：" + str(e))

    def get_all_video(self):
        video = self.mycol.find({}, {"_id": False})
        return json.loads(json_util.dumps(video))

    def get_all_bv(self):
        bv_list = self.mycol.find({}, {"_id": False, "bv": 1})
        return json.loads(json_util.dumps(bv_list))

    def get_all_url(self):
        url_list = self.mycol.find({}, {"_id": False, "url": 1})
        return json.loads(json_util.dumps(url_list))

    def insert(self, video):
        self.mycol.insert_one(video.video_dict)

    def search_video(self, video):
        return json.loads(json_util.dumps(self.mycol.find({"bv": video.bv}, {"_id": False})))[0]

    def delete(self, video):
        self.mycol.delete_one({"bv": video.bv})

    def clean(self):
        """清空数据库"""
        try:
            self.mycol.delete_many({})
        except Exception as e:
            pass


if __name__ == "__main__":
    Db().clean()