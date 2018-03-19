#!/usr/bin/env python3
# coding: utf-8

import hashlib
import feedparser
import models
import nltk
import time
from models import News
from newspaper import Article
from newspaper.article import ArticleDownloadState
from sqlalchemy.orm.exc import NoResultFound

nltk.download('punkt')

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


def getContents(url):
    '''
    입력받은 url 에 접속하여 본문을 가져온다

    :param url:
    :return: text, keywords, summary
    '''

    article = Article(url, language='ko')

    try:
        article.download()

        loopCnt = 0
        while True:
            loopCnt += 1
            if article.download_state != ArticleDownloadState.NOT_STARTED: break
            if loopCnt > 10: break
            time.sleep(1)


        if article.download_state == ArticleDownloadState.SUCCESS:
            article.parse()
            article.nlp()
        else:
            print(article.download_exception_msg)

    except Exception as ex:
        print('Handling exception:', ex)
        return '','',''

    return article.text, article.keywords, article.summary


def run():

    # TODO RSS URL 목록을 DB 에서 가져오는 코드 작성 필요 함.
    # 일단, 기능 개발을 위해 구글뉴스의 RSS 를 가져와서 진행함.
    urls = ["https://news.google.com/news/rss/?ned=kr&gl=KR&hl=ko"]

    for url in urls:
        feeds = crawl_rss(url)

        db_session = models.db_session

        for feed in feeds:

            time.sleep(0.5)

            link_url_sha1 = hashlib.sha1(feed[1].encode()).hexdigest()

            article = getContents(feed[1])

            news = News(title         = feed[0],
                        link_url      = feed[1],
                        link_url_sha1 = link_url_sha1,
                        published     = feed[2],
                        contents      = article[0],
                        summarize     = article[2],
                        keywords      = ','.join(article[1]),
                        status_cd     = 'I')

            try:
                temp_news = db_session.query(News).filter(News.link_url_sha1==link_url_sha1).one()
                if temp_news.contents == news.contents: continue
                temp_news.title = news.title
                temp_news.contents = news.contents
                temp_news.summarize = news.summarize
                temp_news.keywords = news.keywords
                temp_news.published = news.published
                temp_news.status_cd = 'C'
                db_session.commit()
                continue
            except NoResultFound as e:
                print('')

            try:
                print(news)
                db_session.add(news)
                if news.summarize != '':
                    news.status_cd = 'C'
                db_session.commit()
            except Exception as ex:
                print('Handling exception:', ex)
                db_session.rollback()
                continue

if __name__ == '__main__':
    run()