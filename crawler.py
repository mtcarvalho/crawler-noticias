# coding=utf8

import newspaper
from newspaper import Article
import nltk
import mysql.connector
from datetime import datetime

def add_new_image(cursor, article_no, actual_img):
    print("inserting image, article no: " + str(article_no) + " url of image: " + str(actual_img))
    add_image = "INSERT INTO image (article_id, image_url) VALUES (%s, %s)"
    data_image = article_no, actual_img
    cursor.execute(add_image, data_image)

def add_new_movie(cursor, article_no, actual_movie):
    print("inserting movie, article no: " + str(article_no) + " url of movie: " + str(actual_movie))
    add_movie = "INSERT INTO movie (article_id, movie_url) VALUES (%s, %s)"
    data_movie = article_no, actual_movie
    cursor.execute(add_movie, data_movie)

def add_new_article_keyword(cursor, article_no, keyword_id):
    print("inserting keyword of an article, article no: " + str(article_no) + " keyword id: " + str(keyword_id))
    add_keyword_art = "INSERT INTO article_keyword (keyword_id, article_id) "\
    "VALUES (%s, %s)"
    data_keyword_art = keyword_id, article_no
    cursor.execute(add_keyword_art, data_keyword_art)

def add_new_keyword(cursor, actual_keyword):
    print("inserting new keyword, keyword: " + str(actual_keyword))
    add_keyword = "INSERT INTO keyword (keyword) VALUES (%s)"
    data_keyword = actual_keyword, 
    cursor.execute(add_keyword, data_keyword)
    keyword_id = cursor.lastrowid
    
    return keyword_id

def insert_new_article_author(cursor, article_no, author_id):
    print("inserting author of an article, article no: " + str(article_no) + " author id: " + str(author_id))
    add_author_art = "INSERT INTO article_author (author_id, article_id) "\
    "VALUES (%s, %s)"
    data_author_art = author_id, article_no
    cursor.execute(add_author_art, data_author_art)

def insert_new_author(cursor, author_name):
    print("inserting new author, author name: " + str(author_name))
    add_author = "INSERT INTO author (author_name) VALUES (%s)"
    data_author = author_name, 
    cursor.execute(add_author, data_author)
    author_id = cursor.lastrowid
    
    return author_id

def insert_new_article(actual_src, cursor, url, article):
    print("inserting new article, source url: " + str(actual_src) + " url of news " + str(url) + " article " + str(article))
    
    title = None
    publish_date = None
    date = None
    time = None
    meta = None
    summ = None
    text = None
    top_img = None
    title = article.title
    publish_date = article.publish_date
    
    if publish_date is not None:
        time = datetime.time(publish_date)
        date = datetime.date(publish_date)
        
    meta = article.meta_description # not obrigatory
    summ = article.summary
    text = article.text
    top_img = article.top_image
    
    add_article = "INSERT INTO article "\
    "(title, publish_datetime, publish_date, publish_time,"\
    "meta_description, summary, text, url_news, url_source_news,"\
    "url_top_image) "\
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data_article = title, publish_date, date, time, meta, summ, text, url, actual_src, top_img
    
    cursor.execute(add_article, data_article)
    article_no = cursor.lastrowid
    
    print("new article id: " + str(article_no))
    
    return article_no

sources = [
'https://noticias.uol.com.br/', 'https://oglobo.globo.com/', 'https://veja.abril.com.br/',
'https://www.r7.com/', 'http://www.estadao.com.br/', 'https://www.msn.com/pt-br',
'https://www.ig.com.br/', 'https://br.noticias.yahoo.com/', 'http://www.clicrbs.com.br/rs/',
'https://odia.ig.com.br/', 'https://www.terra.com.br/noticias/', 'https://www.folha.uol.com.br/',
'https://www.globo.com/', 'http://g1.globo.com/', 'http://www.jb.com.br/',
'https://www.metropoles.com/', 'https://www.bol.uol.com.br/', 'http://news.google.com.br/',
'https://exame.abril.com.br/', 'http://www.gazetadopovo.com.br/', 'http://portaldoholanda.com.br/',
'http://www.lance.com.br/', 'http://globoesporte.globo.com/', 'http://www.band.uol.com.br/',
'https://epoca.globo.com/', 'https://imasters.com.br/', 'https://www.correio24horas.com.br/capa/',
'https://www.uai.com.br/'
]

while (True):
    try:
        cnx = mysql.connector.connect(
        user='root',
        password='root',
        host='localhost',
        port='3306',
        db='news')
        
        for actual_src in sources:
            print("actual source: " + actual_src)
            
            src = newspaper.build(actual_src, language='pt')
            categories_url_src = src.category_urls();
            
            print(categories_url_src)
            print()
            
            for category in categories_url_src:
                category_articles = newspaper.build(category, language='pt')
                
                print("url of category: " + category)
                
                for arrArticle in category_articles.articles:
                    cursor = cnx.cursor()
                    url = arrArticle.url
                    url = url.strip()
                    print("actual article: " + url)
                    
                    try:
                        article = Article(url, language='pt')
                        article.download()
                        article.parse()
                        article.nlp()
                        
                        query = ("SELECT url_news FROM article "
                                 "WHERE url_news = %s")
                        
                        cursor.execute(query, (url,))
                        news_exist = cursor.fetchall()
                        
                        if (news_exist):
                            print("news already exist on database")        
                            continue
                        else:
                            article_no = int(insert_new_article(actual_src, cursor, url, article))
                           
                            query = ("SELECT author_id, author_name FROM author "
                                     "WHERE author_name = %s")
                            
                            authors = article.authors
                            print(authors)
                            if (authors is not None) and (authors): 
                                for author_name in authors:
                                    cursor.execute(query, (author_name,))
                                    author = cursor.fetchall()
                                    author_id = 0
                                    
                                    if (author):
                                        author_id = author[0][0]
                                    else:
                                        author_id = insert_new_author(cursor, author_name)
                                        
                                    insert_new_article_author(cursor, article_no, author_id)
                            
                            query = ("SELECT keyword_id, keyword FROM keyword "
                                     "WHERE keyword = %s")
                            
                            keywords = article.keywords 
                            print(keywords)
                            if (keywords is not None) and (keywords):
                                for actual_keyword in keywords:
                                    cursor.execute(query, (actual_keyword,))
                                    keyword = cursor.fetchall()
                                    keyword_id = 0
                                    
                                    if (keyword):
                                        keyword_id = keyword[0][0]
                                    else:
                                        keyword_id = add_new_keyword(cursor, actual_keyword)
                                

                            add_new_article_keyword(cursor, article_no, keyword_id)
                            
                            query = ("SELECT movie_id, movie FROM movie "
                                     "WHERE movie = %s")
                            
                            movies = article.movies  
                            print(movies)
                            if (movies is not None) and (movies):
                                for actual_movie in movies:
                                    cursor.execute(query, (actual_movie,))
                                    movie = cursor.fetchall()
                                    
                                    if not (movie):
                                        add_new_movie(cursor, article_no, actual_movie)
                                        
                            query = ("SELECT image_id, image_url FROM image "
                                     "WHERE image_url = %s")            
                                    
                                
                            imgs = article.images  
                            print(imgs)
                            if (imgs is not None) and (imgs):
                                for actual_img in imgs:
                                    cursor.execute(query, (actual_img,))
                                    img = cursor.fetchall()
                                    
                                    if not (img):
                                        add_new_image(cursor, article_no, actual_img)
                                        
                    except Exception as err:
                        print("exception: " + str(url))
                        print(str(err))
    
                    cnx.commit()
                print("end of category: " + category)    
                
        cursor.close()
        cnx.close()
    except Exception as err:
        print("exception: " + str(err))
