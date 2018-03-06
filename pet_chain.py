# -*- coding:utf-8 -*-
import requests
import time
import thread
import json
import sys
import ConfigParser
from PIL import Image,ImageFile
import base64
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True

class PetChain():
    def __init__(self):
        self.degree_map = {
            0:"common",
            1:"rare",
            2:"excellence", 
            3:"epic",
            4:"mythical",
            5:"legend"
        }
        self.degree_conf = {}
        self.interval = 1

        self.cookies = ''
        self.headers = {}
        self.get_headers()
        self.get_config()

    def get_config(self):
        f = open("config.json")
        config = json.load(f)
        f.close()

        self.interval = config.get("interval")
        for i in range(6):
            try:
                price = config.get(self.degree_map.get(i))
            except Exception,e:
                price = 100
            self.degree_conf[i] = price

        # 稀有数量
        self.num_of_rare_attr = config.get("num_of_rare_attr")

        # 最大页数
        self.max_num_of_pages = config.get("max_num_of_pages")
        # 排序
        sort_map = {
            "rare":"RAREDEGREE_DESC",
            "price":"AMOUNT_ASC",
            "date":"CREATETIME_DESC"
        }
        sort_by = config.get("sort_by")
        self.sort_type = sort_map.get(sort_by, "RAREDEGREE_DESC")

        # 稀有类型
        self.attrs = {
            u"体型":"body",
            u"眼睛":"eyes",
            u"嘴巴":"mouth",
            u"花纹":"pattern",
            u"身体色":"color_of_body",
            u"眼睛色":"color_of_eyes",
            u"花纹色":"color_of_pattern",
            u"肚皮色":"color_of_belly"
        }
        self.attr_map = {}
        for attr in self.attrs.values():
            if config.get(attr):
                self.attr_map[attr] = config.get(attr)

    def get_headers(self):
        with open("data/headers.txt") as f:
            lines = f.readlines()
            headers = dict()
            for line in lines:
                splited = line.strip().split(":")
                key = splited[0].strip()
                value = ":".join(splited[1:]).strip()
                self.headers[key] = value

    def get_market(self, pageno, model="ter"):
        pets = []
        try:
            data = {
                "pageNo":pageno,
                "pageSize":10,
                "querySortType":self.sort_type,
                "petIds":[],
                "lastAmount":0,
                "lastRareDegree":"null",
                "requestId":1520289278968,
                "appId":1,
                "tpl":"",
            }
            page = requests.post("https://pet-chain.baidu.com/data/market/queryPetsOnSale", headers=self.headers, data=json.dumps(data), timeout=2)
            print json.dumps(page.json(), ensure_ascii=False)
            if page.json().get(u"errorMsg") == u"success":
                pets = page.json().get(u"data").get("petsOnSale")
                if model == "ter":
                    for pet in pets:
                        self.purchase(pet)
        except Exception,e:
            print e
            pets = []
        return pets

    def purchase(self, pet):
        try:
            pet_id = pet.get(u"petId")
            pet_amount = pet.get(u"amount")
            pet_degree = pet.get(u"rareDegree")
            pet_validCode = pet.get(u"validCode")

            data = {
                "appId":1,
                "petId":pet_id,
                "captcha": "",
                "seed": 0,
                "requestId": int(time.time() * 1000),
                "tpl":"",
                "amount":"{}".format(pet_amount),
                "validCode": pet_validCode
            }
            pet_attrs = self.get_attrs(pet_id)
            assert self.is_qualified(pet_attrs, pet_amount, pet_degree), ValueError("pet:%s 不符合条件" % pet_id.encode("utf-8"))
            #print "Match pet degree:{} amount:{}".format(pet_degree, pet_amount)
            captcha, seed = self.get_captcha()
            assert captcha and seed, ValueError("验证码为空")
            data['captcha'] = captcha
            data['seed'] = seed
            page = requests.post("https://pet-chain.baidu.com/data/txn/create", headers=self.headers, data=json.dumps(data), timeout=2)
            resp = page.json()
            print json.dumps(resp, ensure_ascii=False)
        except Exception,e:
            print e
            pass

    def is_qualified(self, pet_attrs, pet_amount, pet_degree):
        nums_rare = 0
        is_qualified = False

        detail = u" 特殊属性 "
        for attr in pet_attrs:
            name = attr.get(u"name")
            attr_name = self.attrs.get(name)
            rare_degree = attr.get(u"rareDegree")
            if rare_degree == u"稀有":
                nums_rare += 1
            if attr_name in self.attr_map:
                attr_value = attr.get(u"value")
                if attr_value not in self.attr_map.get(attr_name):
                    return False
                else:
                    detail += u"%s:%s " % (name, attr_value)
        if nums_rare < self.num_of_rare_attr:
            return False

        if float(pet_amount) > self.degree_conf.get(pet_degree):
            return False
        print u"稀有属性:%s  稀有等级:%s  价格:%s " % (nums_rare, pet_degree, pet_amount) + detail
        return True


    def get_attrs(self, pet_id):
        try:
            data = {
                "petId":pet_id,
                "requestId":1520286948055,
                "appId":1,
                "tpl":"",
                "timeStamp":"null",
                "nounce":"null",
                "token":"null"
            }
            page = requests.post("https://pet-chain.baidu.com/data/pet/queryPetById", data=json.dumps(data), headers=self.headers, timeout=1)
            attrs = page.json().get("data").get("attributes")
        except Exception,e:
            attrs = []
        return attrs

    def get_captcha(self):
        seed = -1
        captcha = -1
        try:
            data = {
                "requestId":1518007015081,
                "appId":1,
                "tpl":""
            }
            page = requests.post("https://pet-chain.baidu.com/data/captcha/gen", data=json.dumps(data), headers=self.headers)
            resp = page.json()
            if resp.get(u"errorMsg") == u"success":
                seed = resp.get(u"data").get(u"seed")
                img = resp.get(u"data").get(u"img")
                with open('data/captcha.jpg', 'wb') as fp:
                    fp.write(base64.b64decode(img))
                    fp.close()
                im = Image.open("data/captcha.jpg")
                im.show()
                captcha = raw_input("enter captcha:")
                im.close()
        except Exception,e:
            print e
        return captcha, seed


    def run(self):
        while True:
            for pageno in range(1, self.max_num_of_pages):
                pc.get_market(pageno)
                time.sleep(self.interval)

if __name__ == "__main__":
    pc = PetChain()
    pc.run()