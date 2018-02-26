#!/usr/bin/env python3
# coding: utf-8

import feedparser
import models
from models import News


def crawl_rss(url):
    '''
    입력받은 url 에 접속하여 RSS 정보를 가져온후 title, link, pubDate 를 배열로 반환한다

    :param url: RSS URL
    :return: [[title, link, pubDate]]
    '''
    d = feedparser.parse(url)

    feeds = []
    for e in d.entries:
        title = e.title
        link = e.link
        pubDate = str(e.published)

        feeds.append([title, link, pubDate])

    return feeds


def run():

    # TODO RSS URL 목록을 DB 에서 가져오는 코드 작성 필요 함. (서버 셋팅 필요)
    # 일단, 기능 개발을 위해 구글뉴스의 RSS 를 가져와서 진행함.
    urls = ["https://news.google.com/news/rss/?ned=kr&gl=KR&hl=ko"]

    for url in urls:
        feeds = crawl_rss(url)

        db_session = models.db_session

        for feed in feeds:
            news = News(title=feed[0], link_url=feed[1], published=feed[2], status_cd='I')

            try:
                print(news)
            except Exception as ex:
                print(ex)
                continue

if __name__ == '__main__':
    run()