## another news web crawler

1. Prerequisites
- MySQL with an empty database
- Latest Python version with pip

2. Explaining each project folder
- news-crawler: contains all scripts required to crawl news sites, that also (optionally) creates the database schema automatically
- news-schema: contains the schema structure, useful by creating the tables not using the crawler script (but creates the **same** structure)
- news-utils: contains scripts that reads the news database to output data in other formats

3. How to run scripts inside each project folder
    1. **news-crawler:**
    - First, install the necessary files to run the Python scripts for this project:
`pip install -r requirements.txt`
    - Add in the script `crawler.py` the sources that you want to crawl, in the sources array, and define the language of your scripts:
        ```
        language = 'pt'
        sources = [
        'https://noticias.uol.com.br/', # add here more sources 
        ]
        ```
    - Available languages are:
         ```
          code            language
        
          ar              Arabic
          ru              Russian
          nl              Dutch
          de              German
          en              English
          es              Spanish
          fr              French
          he              Hebrew
          it              Italian
          ko              Korean
          no              Norwegian
          fa              Persian
          pl              Polish
          pt              Portuguese
          sv              Swedish
          hu              Hungarian
          fi              Finnish
          da              Danish
          zh              Chinese
          id              Indonesian
          vi              Vietnamese
          sw              Swahili
          tr              Turkish
          el              Greek
          uk              Ukrainian
        ```
    - Then, run the `crawler.py` script respecting the flags:
        ```
        python crawler.py [--host HOST] [--port PORT] [--usr USR] [--pwd PWD] [--db DB] [--debug DEBUG] [--tables TABLES]
        ```
    
    - Flags:
    `host` is the name or ip of the host that contains the mysql database
    `port` is the port of the host that contains the mysql database
    `usr` is the user that have the permission to access the mysql database
    `pwd` is the password of the user that have the permission to access the mysql database
    `db` is the name of the database already created and that have or not the structure to store the news crawled data
    `debug` is a flag (True/False) that you pass to see or not the commands that the `script` is sending to the database
    `tables` is a flag (True/False) that defines if you want the script to create or not the structure in the database related to the news crawled data (the created schema is described in news-schema section)
    - To stop it, press Ctrl + v

    2. **news-schema:**

    - The tables that are created are described in the following image:
    
        ![db-schema](./news-schema/schema.PNG)
    
    - To create the database on the terminal, run the following command:
`mysql -u <username> -p -h <host> -P <port> <database> << <project_path>\news-schema\mysql.sql`
    - Type the password and wait until the process finishes successfully

    3. **news-utils:** 
    
    - `database2excel.py`: script to export columns of the database to excel 
    - Change the values referring to the database connection within the following block of code inside the script:
        ```
        cnx = mysql.connector.connect(
                user='root',
                password='root',
                host='localhost',
                port='3306',
                db='news')
        ```

    - If necessary, change the values that you want to export by making a query with reference to those values in the following code block inside the script
        ```
        query = ("select article_id, title, meta_description," + 
                "summary, text, url_news, url_source_news from article;")
        ```
    - Run the export script: `python database2excel.py`
    - A file named news.xlsx will be created inside the same folder that contains the `database2excel.py` script