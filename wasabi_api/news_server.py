from concurrent import futures
import time

import grpc
import news_pb2
import news_pb2_grpc

if __package__ is None:
    import sys
    from os import path

    # print(path.dirname(path.dirname(path.abspath(__file__))))
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from wasabi_news_crawler import models
else:
    from ..wasabi_news_crawler import models

_ONE_DAY_IN_SECONDS = 60 * 60 * 2



class NewsService(news_pb2_grpc.NewsServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.db_session = models.db_session

    def getList(self, request, context):
        print("News server received: " + request.keyword)

        try:
            news_list = self.db_session.query(models.News)\
                            .filter(models.News.contents.ilike('%' + request.keyword + '%'))\
                            .order_by(models.News.published.desc())\
                            .paginate(page = request.pageNumber, per_page = request.resultPerPage)\
                            .all()

            for news in news_list:
                response = news_pb2.ResponseNews(linkUrlSha1 = news.link_url_sha1,
                                                 linkUrl     = news.link_url,
                                                 title       = news.title,
                                                 published   = news.published,
                                                 contents    = news.contents,
                                                 regDt       = news.reg_dt,
                                                 scrapingDt  = news.scraping_dt)
                yield response
        except:
            yield None

def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    news_pb2_grpc.add_NewsServicer_to_server(NewsService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()