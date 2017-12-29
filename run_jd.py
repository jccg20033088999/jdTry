import sys,time
reload(sys)
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup
import urllib2, urllib
from json import *

cookie = "your cookie"

def foo(actid): 
    f = urllib2.Request(
        url     = 'http://try.jd.com/migrate/apply?activityId='+actid+'&source=0',
        )
    f.add_header('Cookie', cookie);
    response = urllib2.urlopen(f)
    g = response.read()
    print g.decode('UTF-8','ignore')
    return 0

def foo2(actList): 
    f = urllib2.Request(
        url     = 'http://try.jd.com/user/getApplyStateByActivityIds?activityIds=' + ','.join(actList),
        )
    f.add_header('Cookie', cookie);
    f.add_header('Referer','http://try.jd.com/activity/getActivityList?page=1&activityState=0')
    response = urllib2.urlopen(f)
    g = response.read()
    d=JSONDecoder().decode(g)
    actlist2 = []
    for i in d:
        actlist2.append(str(i['activityId']))
    return set(actList) - set(actlist2)
    
def foo3(page): 
    f = urllib2.Request(
        url     = 'http://try.jd.com/activity/getActivityList?page='+str(page)+'&activityState=0',
        )
    response = urllib2.urlopen(f)
    d = response.read()
    soup = BeautifulSoup(d)

    actList = []
    for lind in soup.find_all('li'):
        actid = lind.get('activity_id')
        if actid:
            actList.append(str(actid))

    return actList
    
def foo4(): 
    f = urllib2.Request(
        url     = 'http://try.jd.com/activity/getActivityList?activityState=0',
        )
    response = urllib2.urlopen(f)
    d = response.read()
    soup = BeautifulSoup(d)

    count = 0
    start =  str(soup.head.script).find('{')
    end = str(soup.head.script).rfind('}') + 1
    jsonStr = str(soup.head.script)[start:end]
    jsonStr = jsonStr.replace('\'', "\"")

    d=JSONDecoder().decode(jsonStr)
    return d["pagination"]["pages"]

total = foo4()

for i in xrange(total+1):
    print i
    actList = foo3(i)
    actList = foo2(actList)
    for actid in actList:
        foo(actid)
        time.sleep(5)
print 'end'
while True:
    pass