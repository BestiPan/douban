#!/usr/bin/env python
#encoding=utf-8

import re
import time
import random
import pymysql
import urllib2
import numpy as np

#从文件中获取链接
def get_url():
    fp = open("movie_set.txt")
    urls = []
    for line in fp:
        for start in range(0,181,20): #每个电影爬取10页评论
            url = line.strip().split(" ")[0]
            url = url + "comments?start=" + str(start) + "&limit=20&sort=new_score&status=P"
            urls.append(url)
    return urls

#获取每个链接的评论和评分并存入数据库
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
        print username + "\t" + title + "\t" + dates + "\t" + str(score) + "\t" + comment
        
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
    print ""

if __name__ == "__main__":
    db = pymysql.connect("localhost","root","123456","douban",charset='utf8')
    urls = get_url()
    urls = urls[:40000] #截取一部分链接
    x = 0
    for url in urls:
        x += 1
        print url + " " + str(x) + "/" + str(len(urls))
        try:
            get_element(url,db)
            time.sleep(2)
        except:
            print "ERROR"
            time.sleep(2)
            continue
    db.close()
