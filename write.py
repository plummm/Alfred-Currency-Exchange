# -*- coding:utf-8 -*-
import json,sys
import requests
from workflow import Workflow, web

reload(sys)
sys.setdefaultencoding('utf-8')

def main(wf):
    args = wf.args
    data = args[0]
    op = args[1]
    if op == 'add':
        f = open('config.json', 'r')
        j_config = json.load(f, 'utf-8')
        f.close()
        f = open('config.json', 'w+')
        j_config['units'].append(data)
        json.dump(j_config,f)
        f.close()
        wf.item_class.arg = data

    if op == 'del':
        f = open('config.json', 'r')
        j_config = json.load(f, 'utf-8')
        f.close()
        f = open('config.json', 'w+')
        j_config['units'].remove(data)
        json.dump(j_config, f)
        f.close()

    if op == 'base':
        f = open('config.json', 'r+')
        j_config = json.load(f, 'utf-8')
        j_config['base'] = data
        f.seek(0)
        json.dump(j_config, f)
        f.close()

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))