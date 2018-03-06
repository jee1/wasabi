from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

engine     = create_engine('mysql+pymysql://wasabi:Wasabi!0@192.168.0.250:3307/wasabi?charset=utf8', convert_unicode=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base       = declarative_base()
Base.query = db_session.query_property()

class News(Base):

    __tablename__ = 'news'

    title         = Column(String(1000))
    link_url      = Column(String(1000))
    link_url_sha1 = Column(String(40), primary_key=True)
    published     = Column(TIMESTAMP)
    contents      = Column(String)
    reg_dt        = Column(TIMESTAMP)
    scraping_dt   = Column(TIMESTAMP)
    status_cd     = Column(String)

    def __repr__(self):
        return "<News('%s', '%s', '%s', '%s'>" % (self.title, self.link_url, self.published, self.status_cd)
