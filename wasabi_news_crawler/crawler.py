#!/usr/bin/env python3
# coding: utf-8

import hashlib
import feedparser
import models
import nlp
import time
import ssl
import chardet
import networkx
import locale
import nltk
from models import News
from newspaper import Article
from sqlalchemy.orm.exc import NoResultFound
from urllib.request import urlopen, Request
from datetime import datetime
from dateutil import tz

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
        title   = e.title
        link    = e.link
        locale.setlocale(locale.LC_TIME, "en_US")
        gmt     = datetime.strptime(e.published, '%a, %d %b %Y %H:%M:%S %Z')
        pubDate = gmt.astimezone(tz.gettz('Asia/Seoul'))

        feeds.append([title, link, pubDate])

    return feeds


def downloadContent(url):
    '''
        입력받은 url 에 접속하여 본문을 가져온다

        :param url:
        :return: doc
    '''
    context = ssl._create_unverified_context()
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=headers)
    try:
        page = urlopen(req, context=context)
        document = page.read()
    except:
        pass
    finally:
        page.close()

    doc = ''
    for txt in document.splitlines():
        charset = chardet.detect(txt)['encoding']
        try:
            doc = doc + txt.decode(charset)
        except TypeError:
            pass
        except UnicodeDecodeError:
            pass

    return doc

def getContents(url):
    '''
    뉴스 정보를 반환한다

    :param url:
    :return: text, keywords, summary
    '''
    article = Article(url='', language='ko')
    # article.extractor.stopwords
    article.download(input_html=downloadContent(url))
    article.parse()
    article.nlp()

    sentences = nlp.get_sentences(article.text)
    graph = nlp.build_graph(sentences)
    pagerank = networkx.pagerank(graph, weight='weight')
    reordered = sorted(pagerank, key=pagerank.get, reverse=True)

    i = 0
    summrize = []
    for txt in reordered:
        summrize.append([txt.index, txt.text])
        i = i + 1
        if (i > 2): break

    summrize.sort()

    summary = ''
    for txt in summrize:
        summary += '* ' + txt[1] + '\n'

    return article.text, article.keywords, summary


def run():

    # TODO RSS URL 목록을 DB 에서 가져오는 코드 작성 필요 함.
    # 일단, 기능 개발을 위해 구글뉴스의 RSS 를 가져와서 진행함.
    urls = ["https://news.google.com/news/rss/?ned=kr&gl=KR&hl=ko"]

    db_session = models.db_session

    for url in urls:
        feeds = crawl_rss(url)

        for feed in feeds:

            time.sleep(0.5)

            writeNewsToDb(db_session, feed)


def writeNewsToDb(db_session, feed):
    link_url_sha1 = hashlib.sha1(feed[1].encode()).hexdigest()
    article = getContents(feed[1])
    news = News(title=feed[0],
                link_url=feed[1],
                link_url_sha1=link_url_sha1,
                published=feed[2],
                contents=article[0],
                summarize=article[2],
                keywords=','.join(article[1]),
                scraping_dt=datetime.now(),
                status_cd='I')
    try:
        # 기존에 등록된 뉴스인지 확인한다
        temp_news = db_session.query(News).filter(News.link_url_sha1 == link_url_sha1).one()
        if temp_news.contents == news.contents: return

        updateNews(db_session, news, temp_news)
    except NoResultFound as e:
        # 기존에 등록된 뉴스가 없으면 새로 등록한다
        addNews(db_session, news)


def addNews(db_session, news):
    try:
        if news.summarize != '': news.status_cd = 'C'

        print(news)

        db_session.add(news)
        db_session.commit()

    except Exception as ex:
        print('Handling exception:', ex)
        db_session.rollback()


def updateNews(db_session, news, temp_news):
    temp_news.title = news.title
    temp_news.contents = news.contents
    temp_news.summarize = news.summarize
    temp_news.keywords = news.keywords
    temp_news.published = news.published
    temp_news.status_cd = 'C'
    db_session.commit()


if __name__ == '__main__':
    run()