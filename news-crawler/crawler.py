# coding=utf8

import newspaper
import argparse
import nltk
import sys
import os

from store_data import *
from pony.orm import *

from newspaper import Article as NewsArticle

def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host')
    parser.add_argument('--port')
    parser.add_argument('--usr')
    parser.add_argument('--pwd')
    parser.add_argument('--db')
    parser.add_argument('--debug')
    parser.add_argument('--tables')
    args = parser.parse_args()
    
    if (len(sys.argv) != 15):
        print("usage: python {0} [-h] [--host HOST] [--port PORT] [--usr USR] [--pwd PWD] \n\t\t [--db DB] [--debug DEBUG] [--tables TABLES]".format(os.path.basename(sys.argv[0]))) 
        print(os.path.basename(sys.argv[0]) + ": error: invalid number of arguments" + str(len(sys.argv)))
        exit()
        
    connect_database(create_tables=args.tables, debug=args.debug, hst=args.host,
                     usr=args.usr, pwd=args.pwd, dtbs=args.db)
        
def check_punkt():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
def connect_database(hst, usr, pwd, dtbs, create_tables=False, debug=False):
    set_sql_debug(debug == 'True')
    db.bind(provider='mysql', host=hst, user=usr, passwd=pwd, db=dtbs)
    db.generate_mapping(create_tables=(create_tables == 'True')) 
    
    return db

@db_session
def crawl(sources, lan):    
    for current_source in sources:
        
        source = newspaper.build(current_source, language=lan)
        source_categories = source.category_urls();
        
        print("actual source: {0}".format(current_source))
        
        print("quantity of categories: {0} \t start hour: {2} \t list: {1}\n".format(len(source_categories), source_categories, datetime.datetime.now()))
        
        for category in source_categories:
            category_articles = newspaper.build(category, language=lan)  
            
            print("actual category: {0} \nquantity of articles: {1} \t hour: {2} "
                  .format(category, len(category_articles.articles), datetime.datetime.now()))
            
            for article_list in category_articles.articles:
                url = article_list.url
                url = url.strip()
                
                try:
                    article = NewsArticle(url)
                    article.download()
                    article.parse()
                    article.nlp()
                    
                    article_exists = check_article_exists(url)
                    
                    if (article_exists):   
                        continue
                    elif (article is not None and 
                          (article.title is not None and article.title) and 
                          (article.text is not None and article.text)):
                        new_article = insert_article(current_source, url, article)
                        
                        authors = article.authors
                        insert_authors(db, new_article, authors)
                        
                        keywords = article.keywords
                        insert_keywords(db, new_article, keywords)
                                
                        movies = article.movies  
                        insert_movies(new_article, movies)
                                
                        imgs = article.images
                        insert_images(new_article, imgs)
                    
                except Exception as err:
                    print("exception on url: {0} \t detail: {1}".format(str(url), str(err)))
                    
        print("\nend of category: {0} \t end hour: {1}\n".format(category, datetime.datetime.now()))    
        
    
if __name__ == '__main__':
    language = 'pt'
    sources = [
    'https://noticias.uol.com.br/', #...
    ]
    
    check_args()
    check_punkt()
    crawl(sources, language)
    
