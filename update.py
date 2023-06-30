# -*- coding:utf-8 -*-
import json,sys
import urllib, os
import ssl

from workflow.workflow3 import Workflow

currencies_url = 'https://openexchangerates.org/api/currencies.json?app_id={0}&show_alternative=1'
default_id = ''


def main(wf):
    if os.path.exists('id'):
        f = open('id', 'r')
        default_id = f.readline()
        f.close()
    else:
        wf.add_item(title="Set API id first: cy-setid xxxxx",
                subtitle='For more info, run cy-help')
        wf.send_feedback()
        return
    ssl._create_default_https_context = ssl._create_unverified_context
    url = currencies_url.format(default_id)
    req = urllib.request.urlopen(url)
    j = json.load(req)
    #j = requests.request('GET', url).json()
    f = open('currencies.json','w+')
    json.dump(j,f)
    f.close()
    wf.add_item("Update Finish!")
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
