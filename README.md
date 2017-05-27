# douban
爬取豆瓣多部电影的短评和评分

movie_list.py:
爬取电影的名称和相应的链接

douban_spider.py:
根据movie_list.py爬取的链接爬取每部电影短评前10页每个用户的评分和评论，存入数据库

douban_spider.sql:
数据库表头文件
