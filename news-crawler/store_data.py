from datetime import datetime

from model import *

def check_article_exists(url):
    return exists(a.article_id for a in Article if a.url_news == url)

def insert_images(new_article, imgs):
    if (imgs is not None) and (imgs):
        for img in imgs:
            img_exists = exists(i.image_id for i in Image if i.image_id == img)
            if (not img_exists):
                new_article_id = new_article.article_id
                new_img = Image(image_url=img, article_id=new_article_id) 
                commit()


def insert_movies(new_article, movies):
    if (movies is not None) and (movies):
        for movie in movies:
            movie_exists = exists(m.movie_id for m in Movie if m.movie_id == movie)
            if (not movie_exists):
                new_article_id = new_article.article_id
                new_movie = Movie(movie_url=movie, article_id=new_article_id) 
                commit()


def insert_keywords(db, new_article, keywords):
    if (keywords is not None) and (keywords):
        for keyword in keywords:
            keyword_exists = exists(k.keyword_id for k in Keyword if k.keyword == keyword)
            if (keyword_exists):
                keyword_id = db.get("select keyword_id from Keyword where keyword = $keyword") 
                new_article_id = new_article.article_id
                db.execute("insert into article_keyword (article, keyword) values ($new_article_id, $keyword_id)")
            else:
                new_keyword = Keyword(keyword=keyword, article=new_article) 
                commit()
    


def insert_authors(db, new_article, authors):
    if (authors is not None) and (authors):
        for author in authors:
            author_exists = exists(au.author_id for au in Author if au.author_name == author)
            if (author_exists):
                author_id = db.get("select author_id from Author where author_name = $author") 
                new_article_id = new_article.article_id
                db.execute("insert into article_author (article, author) values ($new_article_id, $author_id)")
            else:
                new_author = Author(author_name=author, article=new_article) 
                commit()

def insert_article(current_source, url, article):
    publish_date = article.publish_date
    if publish_date is not None:
        time = datetime.datetime.time(publish_date)
        date = datetime.datetime.date(publish_date)
    else:
        time = None
        date = None
        
    new_article = Article(title=article.title, publish_datetime=publish_date, 
        publish_date=date, 
        publish_time=time, 
        meta_description=article.meta_description, 
        summary=article.summary, 
        text=article.text, 
        url_news=url, 
        url_source_news=current_source, 
        url_top_image=article.top_image)
    commit()

    if new_article is None:
        raise Exception("error while creating article")
    
    return new_article