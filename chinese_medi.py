import urllib2
import lxml
import cookielib
import requests
import re
import json
import sys
import os

import bs4
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

cookiefile = './cookie_tmp.txt'
savefile = './data.json'

#medi_info_dict = {'36245':27,'56605':22,'10073':20,'58169':20,'21303':22,'52904':49}
medi_info_dict = {'36245':2}
url_pre = 'http://cowork.cintcm.com/engine/'

def cookie_load(url_login):
    global cookfile
    cookie1 = cookielib.MozillaCookieJar(cookiefile)
    handler = urllib2.HTTPCookieProcessor(cookie1)
    opener = urllib2.build_opener(handler)
    response = opener.open(url_login)
    cookie1.save(ignore_discard=True, ignore_expires=True)

if __name__ == '__main__':
    page = 1
    id = 10073
    url = 'http://cowork.cintcm.com/engine/login_do.jsp?u=guest&p=guest321&cnid=' + str(id)
    cookie_load(url)
    cookie2 = cookielib.MozillaCookieJar()
    cookie2.load(cookiefile, ignore_discard=True, ignore_expires=True)

    id_list = medi_info_dict.keys()
    count_list = medi_info_dict.values()

    #os.system("rm -fr ./data.json")
    f = open(savefile,'w')


    for num in range(len(id_list)):
        id = id_list[num]
        count = count_list[num]


        for i in range(1,count+1):

            url_sub = 'http://cowork.cintcm.com/engine/outline?page=' + str(i) + '&channelid=' + id + '&ispage=yes'

            r = requests.get(url_sub, cookies=cookie2)
            html = r.content.decode('GBK')
            soup = BeautifulSoup(html, "lxml")
            page_list = soup.select('a[target="_blank"]')

            odd = 0
            for title in page_list:

                odd = odd + 1
                if odd % 2 == 0:
                    continue

                url_sub2 = url_pre + title['href']

                print "name:\t" + title.get_text() + "\t link:\t" +  url_sub2

                r2 = requests.get(url_sub2, cookies=cookie2)
                html2 = r2.content.decode('GBK','ignore')

                soup2 = BeautifulSoup(html2, "lxml")

                page_list1 = soup2.select('td[class="td1c"]')
                page_list2 = soup2.select('td > div')

                json_data={}
                f.write("{\n    " + title.get_text() + "\n")
                for i in range(len(page_list1)):
                    name1 = page_list1[i].get_text()
                    value1 = page_list2[i].get_text()
                    json_data[name1]= value1
                    #print "name is: " + name1 + "\t value is:" + value1
                    f.write(name1 + ":" + value1)
                f.write("}\n")
                # with open(savefile, 'a') as json_file:
                #     #json_file.write(json.dumps(json_data, sort_keys=True, indent=4, ensure_ascii=False))

    f.close()