## Como criar a base de dados

1. Pré-requisitos
- MySQL com um banco de dados vazio
- Última versão do Python, com pip

2. Criação do banco de dados

- No terminal, execute o seguinte comando:
`mysql -u<username> -p -h<host> -P<port> <database> < <path_of_project>\schema.sql`

3. Rodar o script do crawler para popular o banco (crawler.py)

- Primeiramente, instale os pacotes necessários para rodar os scripts Python desse projeto:
`pip install -r requirements.txt`

- Altere os valores referentes à conexão do seu banco de dados dentro do seguinte bloco de código dentro do script
```
cnx = mysql.connector.connect(
        user='root',
        password='root',
        host='localhost',
        port='3306',
        db='news')
```
- Execute o crawler
`python crawler.py`

Para pará-lo, pressione `Ctrl + v`

4. Rodar o script de exportação das colunas do banco para Excel (database2excel.py)

- Altere os valores referentes à conexão do seu banco de dados dentro do seguinte bloco de código dentro do script
```
cnx = mysql.connector.connect(
        user='root',
        password='root',
        host='localhost',
        port='3306',
        db='news')
```

- Caso tenha necessidade, altere os valores que deseja exportar fazendo a consulta referente à esses valores no seguinte bloco de código dentro do script
```
query = ("select article_id, title, meta_description," + 
        "summary, text, url_news, url_source_news from article;")
```
- Execute o script de exportação
`python database2excel.py`

Um arquivo chamado news.xlsx será criado dentro da mesma pasta que contém o script database2excel.py