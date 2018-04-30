# -*- coding:utf-8 -*-
import json,sys
import math,re
import urllib2
import time,os
from workflow import Workflow, web

reload(sys)
sys.setdefaultencoding('utf-8')


number = '0123456789.'
api_url = 'https://openexchangerates.org/api/latest.json?app_id={0}&show_alternative=1'


class Default():
    def __init__(self):
        self.id = '48c5e363909e4a2bba48937790c365e7'
        self.precise = 2
        self.base = ''
        self.currencies = {}
        self.units = []
        self.json = {}



def push_item(item_title,item_subtitle,flag,value):
    wf.add_item(title=item_title,
                subtitle=item_subtitle,
                icon='flags/{0}.png'.format(flag),
                valid='yes',
                arg=str(value))

def push_value(value):
    for e in value:
        unit_value = value[e]
        if unit_value == 0:
            continue
        now = time.localtime()
        title = '{0} {1}'.format(unit_value, e)
        subtitle = 'Last update : {0}/{1}/{2} {3}:{4}   Base : {5}' \
            .format(now.tm_year,
                    now.tm_mon,
                    now.tm_mday,
                    now.tm_hour,
                    now.tm_min,
                    default.base)
        push_item(title, subtitle, e, unit_value)


"""
pass 3 arguments to convert
eg. 5.2 ETH CNY
"""
def convert(base_num, cy_from, cy_to):
    #log.debug(value,cy_from,cy_to)
    result = {}
    for e in cy_to:
            unit_value = round(
                float(base_num) * (default.json["rates"][e] / default.json["rates"][cy_from])
                ,default.precise)
            #if (e != default.base):
            result[e] = unit_value

    return result

"""
parse different query
"""
def parse_query(args):
    length = len(args)
    if length == 0:
        return convert('1',default.base,default.units)

    if length == 1:
        #eg. 600
        try:
            float(args[0])
            return convert(args[0], default.base, default.units)
        except:
            pass

        #eg. BTC
        if args[0] in default.currencies:
            return convert('1',args[0],default.units)

        #eg. 5ETH
        len0 = len(args[0])
        for i in range(0,len0):
            if args[0][i] not in number:
                value = args[0][:i]
                name = args[0][i:]
                try:
                    float(value)
                    if name in default.currencies:
                        return convert(value, name, default.units)
                except:
                    pass
                break

    if length == 2:
        #eg. 500 USD
        try:
            float(args[0])
            if args[1] in default.currencies:
                return convert(args[0], default.base, [args[1]])
        except:
            pass

        #eg. BTC CNY
        if args[0] in default.currencies and args[1] in default.currencies:
            return convert('1', args[0], [args[1]])

    if length == 3:
        #eg. 500 ETH USD
        try:
            float(args[0])
            if args[1] in default.currencies and args[2] in default.currencies:
                return convert(args[0], args[1], [args[2]])
        except:
            pass

    wf.add_item('> \'cy-help\' for more information')


"""
return currencies name
"""
def get_currencies_names():
    f = open('currencies.json','r')
    j = json.load(f,'utf-8')
    return j


"""
return currencies json
"""
def get_currencies_json():
    mtime = 0
    if os.path.exists('data.json'):
        mtime = os.path.getmtime('data.json')
    if time.time() - mtime < 300:
        f = open('data.json', 'r')
        j = json.load(f,'utf-8')
        f.close()
    else:
        f = open('data.json', 'w+')
        convert_url = api_url.format(default.id)
        req = urllib2.urlopen(convert_url)
        j = json.load(req)
        #j = requests.request("GET", convert_url).json()
        json.dump(j,f)
        f.close()
    return j

"""
load json from config.json
"""
def load_data(value, path):
    f = open(path, "r")
    data = json.load(f, encoding="utf-8")
    default.base = data['base']
    for e in data['units']:
        default.units.append(e)
        value[e] = 0


def split_query(op, query):
    for e in query:
        if e in '+-*/':
            op.append(e)

    ele = re.split("\+|-|\*|/", query)
    return ele


def calculate(total_value, value, op):
    length = len(total_value)
    for e in value:
        express = '{0}{1}{2}'.format(total_value[e],op[0],value[e])
        total_value[e] = eval(express)
    del op[0]


def main(wf):
    query = ''
    total_value = {}
    op = ['+']
    args = wf.args
    args = [x.upper() for x in args]
    global elem
    for e in args:
        query += e + ' '
    global default
    default = Default()
    try:
        load_data(total_value, "config.json")
        default.currencies = get_currencies_names()
        default.json = get_currencies_json()
        elem = split_query(op, query)
        for e in elem:
            parse_e = e.split(' ')
            try:
                while 1:
                 parse_e.remove('')
            except ValueError:
                pass

            calculate(total_value, parse_query(parse_e), op)
        push_value(total_value)
    except:
        wf.add_item(title='> \'cy-help\' for more information',
                    subtitle="Format error")
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
    #main(['500', 'eth', '+', '0.2btc'])