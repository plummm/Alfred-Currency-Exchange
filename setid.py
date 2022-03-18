import sys
import urllib2, ssl
from workflow import Workflow, web

reload(sys)
sys.setdefaultencoding('utf-8')

subtitle = 'Set API id'

api_url = 'https://openexchangerates.org/api/latest.json?app_id={0}&show_alternative=1'

def test_id(myid):
    test_url = api_url.format(myid)
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        req = urllib2.urlopen(test_url)
    except:
        return False
    #print(req, req.getcode())
    return req.getcode() == 200

def main(wf):
    args = wf.args
    length = len(args)
    f = open('id', 'w')

    #print("args", args)
    if length == 1:
        myid = args[0]
        #print("myid", myid)
        if test_id(myid):
            f.write(myid)
            f.close
            wf.add_item("Setting ID succeed", " ")
        else:
            wf.add_item("Invalid id", " ")
    else:
        wf.add_item("Invalid id", " ")
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))