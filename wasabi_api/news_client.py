import grpc
import news_pb2
import news_pb2_grpc

def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = news_pb2_grpc.NewsStub(channel)

  for news in stub.getList(news_pb2.RequestNews(keyword='keyword')):
    print("News client received: " + news.linkUrlSha1)


if __name__ == '__main__':
    run()