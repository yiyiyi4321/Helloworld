# -*- coding:utf-8 -*-
import re
import urllib.request, zlib
import time
import sys
import string
from selenium import webdriver
#from lxml import tree

datapath = sys.path[0]
datasuffix = 'txt'
if (len(sys.argv)>1):
    datapath = sys.argv[1]
    datasuffix = sys.argv[2]

def getHtml(url):
    browser = webdriver.Firefox()
    content = ""
    fail_count = 0
    while(len(content) < 10000 and fail_count < 5):
        browser.get(url)
        content = browser.page_source
        if len(content) < 10000:
            fail_count += 1
    print(fail_count)
    browser.quit()
    return content


def getCode(year, turn, url):
    print(url)
    html = getHtml(url)
    #print(html)
    reg =  []
    #<li class="ball_red">16</li>
    reg.append('一等奖</td>\n\t*<td>\n\t*([0-9]\d*)</td>')
    reg.append('<li class="ball_red">([0-9]\d*)</li>')
    reg.append('<li class="ball_blue">([0-9]\d*)</li>')
    outstr = ""
    for i in range(len(reg)):
        page = re.compile(reg[i])
        rs = re.findall(page,html)
        if i == 0:
            print(len(html), rs)
        if i == 0 and (len(rs) != 1 or int(rs[0]) < 20):
            return len(html)
        for j in range(len(rs)):
            outstr+= rs[j] + ","

    print(str(year)+","+str(turn)+","+outstr[:-1])
    if(len(outstr) > 15):
        with open(datapath+'/lot_500_ssq.'+datasuffix, 'a') as f:
            f.write(str(year)+","+str(turn)+","+outstr[:-1]+'\n')
    return len(html)


for year in range(11, 20):
    for turn in range(1, 200):
        str_turn = "{0:02d}{1:03d}".format(year, turn)
        url = "http://kaijiang.500.com/shtml/ssq/"+str_turn+".shtml"
        if getCode(year, turn, url) < 10000:
            break

