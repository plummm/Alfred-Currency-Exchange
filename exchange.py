# -*- coding:utf-8 -*-
import json,sys
import requests
import math
from datetime import datetime
from workflow import Workflow, web

api_url = 'https://openexchangerates.org/api/latest.json?app_id={0}&show_alternative=1'

#convert_raw_url = 'https://openexchangerates.org/api/convert/{0}/{1}/{2}?app_id={3}'

class Default():
    def __init__(self):
        self.id = '48c5e363909e4a2bba48937790c365e7'
        self.precise = 2
        self.base = ''
        self.currencies = []


"""
pass 3 arguments to convert
eg. 5.2 ETH CNY
"""
def convert3(value, cy_from, cy_to):
    convert_url = api_url.format(default.id)
    req = requests.request("GET",convert_url)
    cy_json = req.json()
    result = round(
        float(value) * (cy_json["rates"][cy_to] / cy_json["rates"][cy_from])
        ,default.precise)
    print (result)
    pass

"""
pass 2 arguments to convert
eg. 600 USD
"""
def convert2():
    pass

"""
pass 1 arguments to convert
eg. 600 (base)
(base currency must be set)
"""
def convert1(value):
    convert_url = api_url.format(default.id)
    req = requests.request("GET", convert_url)
    cy_json = req.json()
    for e in default.currencies:
        if (e != default.base):
            unit_value = round(
                float(value) * (cy_json["rates"][e] / cy_json["rates"][default.base])
                ,default.precise)
            print e,unit_value


    pass

"""
pass 1 arguments to rate
eg. USD
"""
def rate1():
    pass

"""
pass 0 arguments to rate
show all rates of base currency
"""
def rate0():
    pass

def parse_query():
    pass

def load_data(path):
    f = open(path, "r")
    data = json.load(f, encoding="utf-8")
    default.base = data['base']
    for e in data['units']:
        default.currencies.append(e)

def main(args):
    payload = ''
    #args = wf.args
    length = len(args)
    global default
    default = Default()
    load_data("data.json")
    #convert3(args[0],args[1],args[2])
    convert1(args[0])

if __name__ == '__main__':
    #wf = Workflow()
    #log = wf.logger
    #sys.exit(wf.run(main))
    main(['1','USD','CNY'])