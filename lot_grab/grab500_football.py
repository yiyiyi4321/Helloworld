import re
import urllib.request, zlib
import time
import sys
import string
from selenium import webdriver

def get_html(url):
    browser = webdriver.Firefox()
    content = ""
    fail_count = 0
    while(len(content) < 10000 and fail_count < 5):
        browser.get(url)
        content = browser.page_source
        if len(content) < 10000:
            fail_count += 1
    print(url, fail_count)
    browser.quit()
    return content

def get_data_set(shuju_html):
    reg = []
    reg.append('<div class="M_title">\n\
      <h4>赛前联赛积分排名</h4>\n\
    </div>\n\
    <div class="M_sub_title">\n\
    <div class="team_name">(.*)<span>\[(.*)\]</span></div>\n\
    <div class="team_name">(.*)<span>\[(.*)\]</span></div>')
    reg.append('<p class="game_time">比赛时间(.*)</p>\n\
            <p class="odds_hd_bf"><strong>(\d*):(\d*)</strong></p>')
    reg.append('<td class="td_one">总成绩</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([-|0-9]\d*)</td><td><span class="ying">([0-9]\d*)</span></td><td>([0-9]\d*)</td><td>([0-9]\d*)%</td>')
    reg.append('<td class="td_one">主场</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([-|0-9]\d*)</td><td><span class="ying">([0-9]\d*)</span></td><td>([0-9]\d*)</td><td>([0-9]\d*)%</td>')
    reg.append('<td class="td_one">客场</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([0-9]\d*)</td><td>([-|0-9]\d*)</td><td><span class="ying">([0-9]\d*)</span></td><td>([0-9]\d*)</td><td>([0-9]\d*)%</td>')

    line = ""
    page = re.compile(reg[0])
    rs = re.findall(page,html)
    line += rs[0][0] + "," + rs[0][2]
    page = re.compile(reg[1])
    rs = re.findall(page,html)
    line += "," + rs[0][0] + "," + rs[0][1] + "," + rs[0][2]
    for i in range(2, 5):
        page = re.compile(reg[i])
        rs = re.findall(page,html)
        for r in rs:
            for j in range(1, len(r)-2):
                line += "," + str(int(r[j])/int(r[0]))
            line += "," + str(math.log(int(r[-2])))
            line += "," + str(int(r[-1])/100)
    with open(datapath+'/lot_500_football.csv', 'a') as f:
        f.write(line+'\n')
    return line

def  bfs_grab():
    html = get_html('http://liansai.500.com/zuqiu-4826/')
    reg = '//odds.500.com/fenxi/shuju-([0-9]\d*).shtml'
    page = re.compile(reg)
    rs = re.findall(page,html)
    liansai_name = '英超'
    id_set = set(rs)
    id_list = []
    id_list.extend(rs)
    print(id_list)
    indx = 0
    while(indx < len(id_list)):
        url = 'http://odds.500.com/fenxi/shuju-'+id_list[indx]+'.shtml'
        shuju_html = get_html(url)
        get_data_set(shuju_html)
        reg = liansai_name + '</a></td><td>\d*-\d*-\d*</td><td class="dz"><a href="./shuju-([0-9]\d*).shtml'
        page = re.compile(reg)
        rs = re.findall(page,html)
        for shuju_id in rs:
        if shuju_id not in id_set:
            id_set.add(shuju_id)
            id_list.append(shuju_id)
            #print('append ', shuju_id)
        indx += 1

bfs_grab()