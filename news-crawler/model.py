import datetime

from pony.orm import *

with db_session:
    db = Database()

class Article(db.Entity):
    article_id = PrimaryKey(int, auto=True)
    title = Required(LongStr)
    publish_datetime = Optional(datetime.datetime, nullable=True)
    publish_date = Optional(datetime.date, nullable=True)
    publish_time = Optional(datetime.time, nullable=True)
    meta_description = Optional(LongStr)
    summary = Optional(LongStr)
    text = Required(LongStr)
    url_news = Required((str))
    url_source_news = Required(str)
    url_top_image = Optional(LongStr)
    author = Set('Author')
    keyword = Set('Keyword')
    image = Set('Image')
    movie = Set('Movie')
    
class Author(db.Entity):
    author_id = PrimaryKey(int, auto=True)
    author_name = Required(str)
    article = Set(Article)
    
class Keyword(db.Entity):
    keyword_id = PrimaryKey(int, auto=True)
    keyword = Required(str)
    article = Set(Article)
    
class Image(db.Entity):
    image_id = PrimaryKey(int, auto=True)
    image_url = Required(LongStr)
    article_id = Required(Article)
    
class Movie(db.Entity):
    movie_id = PrimaryKey(int, auto=True)
    movie_url = Required(str)
    article_id = Required(Article)