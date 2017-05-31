#!/usr/bin/env python
#encoding=utf-8

import re
import time
import random
import pymysql
import urllib2
import numpy as np
from bs4 import BeautifulSoup

def get_url():
    fp = open("movie_set.txt")
    urls = []
    for line in fp:
        for start in range(0,181,20):
            url = line.strip().split(" ")[0]
            url = url + "comments?start=" + str(start) + "&limit=20&sort=new_score&status=P"
            urls.append(url)
    return urls

def get_element(url,db):
    cur = db.cursor()
    user_flag = re.compile(r'a title="(.+?)"')
    date_flag = re.compile(r'\d{4}-\d+-\d+')
    score_flag = re.compile(r'allstar(.+?) ')
    comment_flag = re.compile('<p class="">(.+?)<')

    htmls = urllib2.urlopen(url,timeout=30).read()
    
    title_flag = re.compile(r'<title>(.+?)</title>')
    title = title_flag.findall(htmls)[0].split(" ")[0]
    
    module = []
    while True:
        begin = htmls.find('<div class="avatar">')
        end = begin + 10 + htmls[begin+10:].find('<div class="avatar">')
        if end == 8:
            break
        module.append(htmls[begin:end])
        htmls = htmls[end:]
    module = module[:-1]
    for ele in module:
        ele = " ".join(ele.split("\n"))
        username = user_flag.findall(ele)

        if len(username) != 0:
            username = username[0].strip()
        else:
            continue
        dates = date_flag.findall(ele)
        if len(dates) != 0:
            dates = dates[0].strip()
        else:
            continue
        score = score_flag.findall(ele)
        if len(score) != 0:
            score = int(score[0].strip())/10
        else:
            continue
        comment = comment_flag.findall(ele)
        if len(comment) != 0:
            comment = comment[0].strip()
        else:
            continue
#        print username + "\t" + title + "\t" + dates + "\t" + str(score) + "\t" + comment
        
        sql = "INSERT INTO comments_new \
                (username,title,date,score,comment) \
                VALUES ('%s','%s','%s','%d','%s');" % \
                (username,title,dates,score,comment)
        try:
            cur.execute(sql)
            db.commit()
        except:
            print "出错"
            db.rollback()
    cur.close()
#    print ""

#去除重复影评
def get_newdb(db):
    cur_r = db.cursor()
    cur_w = db.cursor()
    sql = "SELECT distinct * FROM comments_new order by title;"
    cur_r.execute(sql)
    x = 0
    for ele in cur_r:
        x += 1
        print x
        line = list(ele)
        username = line[0]
        title = line[1]
        dates = line[2]
        score = int(line[3])
        comment = line[4]
        sql = "INSERT INTO movies_new \
                (username,title,date,score,comment) \
                VALUES ('%s','%s','%s','%d','%s');" % \
                (username,title,dates,score,comment)
        try:
            cur_w.execute(sql)
            db.commit()
        except:
            print "出错"
            db.rollback()
    cur_r.close()
    cur_w.close()

if __name__ == "__main__":
    db = pymysql.connect("222.28.136.74","root","litangxi101","douban",charset='utf8')
    
    #爬取影评和评分
    urls = get_url()
    print len(urls)
    exit()
    urls = urls[40000:80000]
    x = 0
    for url in urls:
        x += 1
        print url + " " + str(x) + "/" + str(len(urls))
        try:
            get_element(url,db)
            time.sleep(2)
        except:
            print "ERROR"
            continue
    
#    get_newdb(db)

    db.close()
