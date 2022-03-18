# -*- coding:utf-8 -*-
import json,sys
import urllib2
import ssl
from workflow import Workflow, web

reload(sys)
sys.setdefaultencoding('utf-8')

currencies_url = 'https://openexchangerates.org/api/currencies.json?app_id={0}&show_alternative=1'
default_id = '498c33dac59d4b5b91651036c1033484'


def main(wf):
    ssl._create_default_https_context = ssl._create_unverified_context
    url = currencies_url.format(default_id)
    req = urllib2.urlopen(url)
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
