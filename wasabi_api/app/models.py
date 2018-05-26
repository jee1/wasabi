from app import db
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
import datetime

from sqlalchemy.ext.declarative import DeclarativeMeta
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class News(db.Model):
    __tablename__ = "news"

    title         = db.Column(db.String(1000))
    link_url      = db.Column(db.String(1000))
    link_url_sha1 = db.Column(db.String(40), primary_key=True)
    published     = db.Column(db.TIMESTAMP)
    summarize     = db.Column(db.String)
    contents      = db.Column(db.String)
    keywords      = db.Column(db.String(1000))
    image_url     = db.Column(db.String(1024))

    def __init__(self):
        pass

    def __repr__(self):
        return "<News(title='%s', link_url='%s', published='%s')>" % (self.title, self.link_url, self.published)
