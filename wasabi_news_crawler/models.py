from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mysql+pymysql://wasabi:Wasabi!0@192.168.0.250:3307/wasabi?charset=utf8', convert_unicode=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class News(Base):
    __tablename__ = 'news'

    title = Column(String(1000))
    link_url = Column(String(1000))
    link_url_sha1 = Column(String(40), primary_key=True)
    published = Column(TIMESTAMP)
    contents = Column(String)
    summarize = Column(String)
    keywords = Column(String(1000))
    reg_dt = Column(TIMESTAMP)
    scraping_dt = Column(TIMESTAMP)
    status_cd = Column(String(1))
    kor_contents = Column(String)
    kor_summarize = Column(String)
    kor_title = Column(String(1000))

    def __repr__(self):
        return "<News(title='%s', link_url='%s', published='%s', status_cd='%s')>" % (
            self.title if self.kor_title == '' else self.kor_title, self.link_url, self.published, self.status_cd)


class RssSites(Base):
    __tablename__ = 'rss_sites'

    url = Column(String(1024), primary_key=True)
    description = Column(String(1000))

    def __repr__(self):
        return "<RssSites(url='%s', description='%s')>" % (self.url, self.description)
