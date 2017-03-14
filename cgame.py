#coding:utf-8
import os
import sys
import requests
import urllib2
import cStringIO
import cookielib
import pickle
import time
from PIL import Image

import bs4
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

header={}
# header['Pragma']="Pragma"
# header['Referer']="http://icp.alexa.cn/index.php?q=163.com&code=CUXWDV&icp_host=sccainfo"
header['User-Agent']="Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"

cookiefile = './bbincookie.txt'
datafile = '/public/data/whwen/data.txt'
Times = 14400

if __name__ == '__main__':
    driver = webdriver.Chrome()
    #driver = webdriver.Firefox
    driver.get("http://www.benz7711.com/")
    WebDriverWait(driver,15)

    for frame in driver.find_elements_by_tag_name('iframe'):
        print frame.get_attribute('name')

    driver.switch_to.frame('mem_index')

    adv = driver.find_element_by_class_name('ui-button-text')
    adv.click()

    #assert ""

    elem_passwd = driver.find_element_by_id('passwd')
    elem_passwd.send_keys('xxxxx')

    elem_code = driver.find_element_by_id('rmNum')
    elem_code.send_keys('1')

    elem_user = driver.find_element_by_id('username')
    elem_user.send_keys('xxxxx')
    #
    time.sleep(3)
    elem_code_img = driver.find_element_by_id('vPic')
    #print elem_code_img.get_attribute('id')

    url_img = elem_code_img.get_attribute('src')

    print url_img
    print "code image url is:\t" + url_img

    checkcode_url = url_img
    time.sleep(3)
    print "checkcode_url:\t" + checkcode_url
    request = urllib2.Request(checkcode_url,headers=header)
    res = urllib2.urlopen(request).read()
    f=open("./code1.png","wb")
    f.write(res)
    f.close()

    #image = Image.open(cStringIO.StringIO(res))

    #image.show

    code = raw_input("输入验证码：")
    time.sleep(15)
    #print  code

    #elem_code.send_keys(code)
    elem_join = driver.find_element_by_id("loginBTN")
    elem_join.click()
    code = raw_input("同意按钮：")
    time.sleep(10)
    #driver.find_element_by_xpath()

    #assert "Python" in driver.title
    #dragon_door_url = 'http://lt.benz7711.com/charon/#/game/bblm?playway=general'
    #dragon_door_url = 'http://lt.benz7711.com/charon/#/game/bblm'
    dragon_door_url = 'http://lt.benz7711.com/vender.php?lang=zh-cn&referer_url=/pt/../charon/%23/game/bblm'
    cookie1 = driver.get_cookies()

    pickle.dump(driver.get_cookies(), open(cookiefile, "wb"))

    # print html
    # driver.quit()
    #driver.switch_to.frame('mem_index')
    cookies = pickle.load(open(cookiefile, "rb"))
    driver.get(dragon_door_url)
    time.sleep(5)

    f = open("/public/data/whwen/data.txt", 'wb')

    for i in range(Times):
        dragon_door_html = driver.page_source
        soup = BeautifulSoup(dragon_door_html, "lxml")
        page_list = soup.select('td[class="BBLM-historyTable-num"]')

        for item in page_list:
            print item
            f.write(str(item) + "\n")
        f.write("turn: " + str(i) + "\n")
        if i == (Times - 1):
            break
        time.sleep(3000)
    f.close()

    #print driver.page_source
