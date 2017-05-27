#!/usr/bin/env python
#encoding=utf-8

import re
import time
import urllib2

TIMEOUT = 30

#获取电影标签
def get_movie_label():
    tags = []
    tag_flag = re.compile(r'href="(.+?)"')
    htmls = urllib2.urlopen("https://movie.douban.com/tag/?view=cloud",timeout=TIMEOUT).read()
    for line in htmls.split("\n"):
        if line.strip().find('href="/tag/') != -1:
            tag = "https://movie.douban.com" + tag_flag.findall(line.strip())[0]
            print tag
            tags.append(tag)
            for i in range(20,141,20):
                tags.append(tag + "?start=" + str(i) + "&type=T")
    return tags

#获取电影链接和名称
def get_movie(tag):
    movies = []
    movie_flag = re.compile(r'nbg" href="(.+?)" ')
    name_flag = re.compile(r'title="(.+?)"')
    htmls = urllib2.urlopen(tag,timeout=TIMEOUT)
    for line in htmls:
        if line.strip().find("nbg") != -1:
            movie_url = movie_flag.findall(line.strip())[0]
            movie_name = name_flag.findall(line.strip())[0]
            print movie_url,movie_name
            movies.append([movie_url,movie_name])
    return movies

#去掉重复的电影，写入新的文件
def list2set():
    fp = open("movie_list.txt")
    fout = open("movie_set.txt","w")
    movie_dict = {}
    for line in fp:
        movie_id = line.strip().split(" ")[0].split("/")[-2]
        if not movie_dict.has_key(movie_id):
            movie_dict[movie_id] = 1
            fout.write(line)
    fout.close()
    fp.close()

if __name__ == "__main__":
#    get_movie("https://movie.douban.com/tag/%E5%90%89%E5%8D%9C%E5%8A%9B?start=20&type=T")

    tags = get_movie_label()
    fp = open("movie_list.txt","w")
    x = 0
    for tag in tags:
        x += 1
        print tag + " " + str(x) + "/" + str(len(tags))
        try:
            movies = get_movie(tag)
            for movie in movies:
                fp.write(" ".join(movie) + "\n")
            time.sleep(2)
        except:
            continue
    fp.close()

    #去掉重复的电影
    time.sleep(5)    
    list2set()
