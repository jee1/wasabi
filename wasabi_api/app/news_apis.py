from app import app, db
from app.models import News, AlchemyEncoder
from flask import make_response
import json


@app.route('/news', methods=['GET'])
def news():
    _news_list = News.query.order_by(db.desc('published')).limit(100).all()

    response = make_response(json.dumps(_news_list, ensure_ascii=False, cls=AlchemyEncoder))
    response.headers['Content-Type'] = 'application/json;charset=UTF-8'
    return response