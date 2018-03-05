# -*- coding:utf-8 -*-

import sys
version = sys.version
from flask import Flask, request, render_template,jsonify
import time
if "2.7" in  version:
    import ConfigParser
else:
    import configparser as ConfigParser
from PIL import Image
import requests
import os
import json
import base64

app = Flask(__name__)
global_pet = {}
headers = {}
degree_map = {
    0:"common",
    1:"rare",
    2:"excellence",
    3:"epic",
    4:"mythical",
}
degree_conf = {}


@app.route("/")
def index():
    return render_template("index.html", time=time.time())


@app.route("/getMarket")
def get_market():
    #pets = pet_chain.get_market(model="html")
    #data = {
    #    "pets":pets
    #}
    degree_map = {
            0:u"普通",
            1:u"稀有",
            2:u"卓越",
            3:u"史诗",
            4:u"神话",
    }
    data = {}
    html = ""
    try:
        pets = market()
        for pet in pets:
            amount = float(pet.get(u"amount"))
            if amount > degree_conf.get(pet.get(u"rareDegree")):
                continue
            degree = degree_map.get(pet.get(u"rareDegree"), u"普通")
            validCode = pet.get(u"validCode")
            did = pet.get(u"petId")
            petUrl = pet.get(u"petUrl")

            global_pet[did] = {
                u"amount":amount,
                u"validCode":validCode,
            }

            html += u'''<div class="dog-detail"> 
                        <input type="hidden" name="amount" value="{}">             
                        <input type="hidden" name="degree" value="{}">            
                        <input type="hidden" name="validCode" value="{}">
                        <input type="hidden" name="id" value="{}">
                        <div class="dog">
                            <div class="dog-img-container">
                                <img src="{}" class="dog-img">
                            </div>
                            <div class="dog-info-container">
                                <div class="dog-proper127.0.0.1 - - [07/Feb/2018 18:42:07] "GET /getMarket HTTP/1.1" 200 -
                                    <span class="dog-amount">价格：{}</span>
                                    <span class="dog-degree">等级：{}</span>
                                </div>
                                <div class="captcha">
                                    <div class="captcha-img">
                                    </div>
                                    <input type="input" class="captcha-input" name="captcha-input" focus="autofocus">
                                    <input type="submit" name="captcha-submit">
                                </div>
                            </div>
                        </div>

                     </div>'''.format(
                         amount,
                         degree,
                         validCode,
                         did,
                         petUrl,
                         amount,
                         degree,
                     )
        html = "没有满足条件的狗" if not html else html
    except Exception as e:
        html = str(e)
        print(e)
    return jsonify({"html":html})

@app.route("/purchase")
def purchase():
    r = {"code":400}
    try:
        did = request.args.get(u"did")
        seed = request.args.get(u"seed")
        captcha = request.args.get(u"captcha")
        if did in global_pet:
            pet = global_pet.get(did)
            pet_amount = pet.get(u"amount")
            pet_validCode = pet.get(u"validCode")

            data = {
                    "appId":1,
                    "petId":did.encode("utf-8"),
                    "captcha": captcha.encode("utf-8"),
                    "seed": seed.encode("utf-8"),
                    "requestId": 1518007015081,
                    "tpl":"",
                    "amount":"{}".format(pet_amount),
                    "validCode": pet_validCode.encode("utf-8")
            }
            print data
            headers['Referer'] = u"https://pet-chain.baidu.com/chain/detail?channel=market&petId={}&appId=1&validCode={}".format(did, pet_validCode)
            print headers
            page = requests.post("https://pet-chain.baidu.com/data/txn/create", headers=headers, data=json.dumps(data), timeout=2)
            resp = page.json()
            r['msg'] = resp.get(u"errorMsg")
            if r['msg'] != u"验证码错误":
                os.rename("data/captcha.jpg", "data/captcha_dataset/{}.jpg".format(captcha))
    except Exception as e:
        r['msg'] = str(e)
    return jsonify(r)

@app.route("/getCaptcha")
def get_captcha():
    r = {"code":400}
    try:
        data = {
            "requestId":1518007015081,
            "appId":1,
            "tpl":""
        }
        page = requests.post("https://pet-chain.baidu.com/data/captcha/gen", data=json.dumps(data), headers=headers)
        resp = page.json()
        if resp.get(u"errorMsg") == u"success":
            seed = resp.get(u"data").get(u"seed")
            img = resp.get(u"data").get(u"img")
            with open('data/captcha.jpg', 'wb') as fp:
                    fp.write(base64.b64decode(img))
                    fp.close()
            r = {
                "code":200,
                "img":img,
                "seed":seed
            }
    except Exception as e:
        pass
    return jsonify(r)


def get_headers():
    header = {}
    with open("data/headers.txt") as f:
        lines = f.readlines()
        headers = dict()
        for line in lines:
            splited = line.strip().split(":")
            key = splited[0].strip()
            value = ":".join(splited[1:]).strip()
            headers[key] = value
    return headers

def get_config():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    for i in range(5):
        try:
            amount = config.getfloat("Pet-Chain", degree_map.get(i))
        except Exception as e:
            amount = 100
        degree_conf[i] = amount

def market():
    pets = []
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
        page = requests.post("https://pet-chain.baidu.com/data/market/queryPetsOnSale", headers=headers, data=json.dumps(data))
        if page.json().get(u"errorMsg") == u"success":
            print("[->] purchase")
            pets = page.json().get(u"data").get("petsOnSale")
    except Exception as e:
        pass
    return pets

headers = get_headers()
get_config()
app.run(debug=True)

