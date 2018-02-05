# -*- coding:utf-8 -*-
import requests
import time
import thread
import threadpool
import json
import ConfigParser


class PetChain():
    def __init__(self):


        self.degree_map = {
            0:"common",
            1:"rare",
            2:"excellence",
            3:"epic",
            4:"mythical",
        }
        self.degree_conf = {}
        self.interval = 1
        self.headers = {}
        self.get_headers()
        self.get_config()

    def get_config(self):
        config = ConfigParser.ConfigParser()
        config.read("config.ini")

        for i in range(5):
            try:
                amount = config.getfloat("Pet-Chain", self.degree_map.get(i))
            except Exception,e:
                amount = 100
            self.degree_conf[i] = amount

        self.interval = config.getfloat("Pet-Chain", "interval")


    def get_headers(self):
        with open("data/headers.txt") as f:
            lines = f.readlines()
            headers = dict()
            for line in lines:
                splited = line.strip().split(":")
                key = splited[0].strip()
                value = ":".join(splited[1:]).strip()
                self.headers[key] = value

    def get_market(self):
        try:
            data = {
                "appId":1,
                "lastAmount":1,
                "lastRareDegree":0,
                "pageNo":1,
                "pageSize":20,
                "petIds":[],
                "querySortType":"AMOUNT_ASC",
                "requestId":1517730660382,
                "tpl":"",
            }
            page = requests.post("https://pet-chain.baidu.com/data/market/queryPetsOnSale", headers=self.headers, data=json.dumps(data))
            if page.json().get(u"errorMsg") == u"success":
                print "[->] purchase"
                pets = page.json().get(u"data").get("petsOnSale")

                pool = threadpool.ThreadPool(10)
                req = threadpool.makeRequests(self.purchase, pets)
                for queue in req:
                    pool.putRequest(queue)
                pool.wait()
        except Exception,e:
            pass

    def purchase(self, pet):
        try:
            pet_id = pet.get(u"petId")
            data = {
                "appId":1,
                "petId":pet_id,
                "requestId":1517730660382,
                "tpl":""
            }
            pet_amount = pet.get(u"amount")
            pet_degree = pet.get(u"rareDegree")
            if float(pet_amount) <= self.degree_conf.get(pet_degree):
                page = requests.post("https://pet-chain.baidu.com/data/txn/create", headers=self.headers, data=json.dumps(data), timeout=2)
                print page.json()
        except Exception,e:
            pass

    def run(self):
        while True:
            pc.get_market()
            time.sleep(self.interval)

if __name__ == "__main__":
    pc = PetChain()
    pc.run()