# -*- coding:utf-8 -*-
import json,sys
import urllib2
from workflow import Workflow, web

reload(sys)
sys.setdefaultencoding('utf-8')


subtitle = 'Add new currency to panel'

"""
push item into item class
"""
def push_item(item_title,item_subtitle,flag,value):
    wf.add_item(title=item_title,
                subtitle=item_subtitle,
                icon='flags/{0}.png'.format(flag),
                valid='yes',
                arg=str(value)+" add")


def main(wf):
    args = wf.args
    args = [x.upper() for x in args]
    length = len(args)
    f = open('currencies.json', 'r')
    j_currencies = json.load(f,'utf-8')
    if length == 0:
        for e in j_currencies:
            push_item(e, subtitle, e, e)

    if length == 1:
        for key in j_currencies:
            if key.startswith(args[0]):
                push_item(key, subtitle, key, key)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
    #main([])