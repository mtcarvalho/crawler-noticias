#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import mysql.connector
from openpyxl import Workbook

#TODO pass values in variables
cnx = mysql.connector.connect(
        user='root',
        password='root',
        host='localhost',
        port='3306',
        db='news')
        
cursor = cnx.cursor()

#TODO use pony
query = ("select article_id, title, meta_description," + 
        "summary, text, url_news, url_source_news from article;")

cursor.execute(query,)

results = cursor.fetchall()
wb = Workbook()
ws = wb.create_sheet(0)
ws.title = "news"
ws.append(cursor.column_names)

for row in results:
    try:
        ws.append(row)
    except Exception:
        print("error when inserting value in file")
        continue

workbook_name = "news"
wb.save(workbook_name + ".xlsx")



cursor.close()
cnx.close()