<<<<<<< HEAD
#!/usr/bin/env python2
import psycopg2

news = 'news'
user = 'vagrant'
password = ''
conn = psycopg2.connect(f"dbname={news} "
                        f"user={user} password={password}")
DBNAME = 'news'
conn = psycopg2.connect(dbname=DBNAME)
cur = conn.cursor()


questionOne = "What are the most popular three articles of all time?"

queryOne = '''CREATE OR REPLACE VIEW popular_articles AS
            SELECT title, count(*) AS views
            FROM articles, log
            WHERE articles.slug=substring(log.path FROM 10)
            GROUP BY articles.title
            ORDER BY views DESC'''

cur.execute(queryOne)

queryTwo = '''SELECT authors.name, count(*) as num
            FROM articles, authors, log
            WHERE log.status='200 OK'
            AND authors.id = articles.author
            AND articles.slug = substr(log.path, 10)
            GROUP BY authors.name
            ORDER BY num desc;'''

cur.execute(queryTwo)


queryThree = '''CREATE OR REPLACE VIEW status_error AS
              SELECT to_char(time, 'FMMonth DD, YYYY')
              AS time, status
              FROM log;

              CREATE OR REPLACE VIEW error_404 AS
              SELECT time, count (*) AS total
              FROM status_error
              WHERE status='404 NOT FOUND'
              GROUP BY time
              ORDER BY time;

              CREATE OR REPLACE VIEW total_status AS
              SELECT time, count (*) AS everything
              FROM status_error
              GROUP BY time
              ORDER BY time;

              CREATE OR REPLACE VIEW TogethaForeva AS
              SELECT total_status.time,
              error_404.total, total_status.everything
              FROM total_status
              LEFT JOIN error_404
              ON total_status.time=error_404.time
              ORDER BY total_status.time;'''

cur.execute(queryThree)

error_logs = '''
WITH answer AS (
              SELECT ( total::float / everything::float * 100)::float
              AS answer, time
              FROM TogethaForeva)
              SELECT TogethaForeva.time, answer.answer
              FROM TogethaForeva
              JOIN answer
              ON answer.time = TogethaForeva.time
              WHERE answer.answer > 1.0;
              '''

 # Printing out Query 1

print("The most popular articles are:")
print("-" * 20)
for article in cur:
 print("\"{}\" -- {}".format(article[0], article[1]))

 # Printing out Query 2

print("The most popular authors are:")
print("-" * 20)
for authors.name in cur:
 print("\"{}\" -- {}".format(authors.name[0], authors.name[1]))

 # Printing out Query 3

 print("The day with most errors:")
 print("-" * 20)
for error in cur:
 print("\"{}\" -- {}%".format(error[0], error[1]))
||||||| merged common ancestors
#! /usr/bin/env python3
import psycopg2

conn = psycopg2.connect("dbname=postgres user=postgres password=PICKYSonnet#60")
cur = conn.cursor()


questionOne = "What are the most popular three articles of all time?"

queryOne = ('''CREATE OR REPLACE VIEW popular_articles AS
            SELECT title, count(*) AS views
            FROM articles, log
            WHERE articles.slug=substring(log.path FROM 10)
            GROUP BY articles.title
            ORDER BY views DESC
            limit 3;''')

cur.execute(queryOne)

queryTwo = ('''CREATE OR REPLACE VIEW authors_articles AS
            SELECT authors.name, articles.title
            FROM authors, articles
            WHERE articles.author=authors.id;
            
            CREATE OR REPLACE VIEW popular_authors AS
            SELECT authors_articles.name,
            SUM(popular_articles.views) AS sum
            FROM authors_articles, popular_articles
            WHERE popular_articles.title=authors_articles.title
            GROUP BY authors_articles.name
            ORDER BY sum DESC;''')

cur.execute(queryTwo)


queryThree = ('''CREATE OR REPLACE VIEW status_error AS
              SELECT to_char(time, 'Month DD YYYY')
              AS time, status
              FROM log;
              
              CREATE OR REPLACE VIEW error_404 AS
              SELECT time, count (*) AS total
              FROM status_error
              WHERE status='404 NOT FOUND'
              GROUP BY time
              ORDER BY time;
              
              CREATE OR REPLACE VIEW total_status AS
              SELECT time, count (*) AS everything
              FROM status_error
              GROUP BY time
              ORDER BY time;
              
              CREATE OR REPLACE VIEW TogethaForeva AS
              SELECT total_status.time,
              error_404.total, total_status.everything
              FROM total_status
              LEFT JOIN error_404
              ON total_status.time=error_404.time
              ORDER BY total_status.time;
              
              ''')

cur.execute(queryThree)

error_logs = '''
WITH answer AS (
              SELECT ( total::float / everything::float * 100)::float
              AS answer, time
              FROM TogethaForeva)
              SELECT TogethaForeva.time, answer.answer
              FROM TogethaForeva
              JOIN answer
              ON answer.time = TogethaForeva.time
              WHERE answer.answer > 1.0;
'''


#Printing out Query 1
print("The most popular articles are:")
cur.execute("SELECT * FROM popular_articles")
for article in cur:
    print(article)

print("-------")
print("The most popular authors are:")
#Printing out Query 2
cur.execute("SELECT * FROM popular_authors")

for name in cur:
    print(name)
print("-------")
#Printing out Query 3
print("The day with most errors:")
cur.execute(error_logs)

for error in cur:
    print(error)
=======
#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect("f*dbname={news} user={user} password={password}")
cur = conn.cursor()


questionOne = "What are the most popular three articles of all time?"

queryOne = ('''CREATE OR REPLACE VIEW popular_articles AS
            SELECT title, count(*) AS views
            FROM articles, log
            WHERE articles.slug=substring(log.path FROM 10)
            GROUP BY articles.title
            ORDER BY views DESC
            limit 3;''')

cur.execute(queryOne)

queryTwo = ('''CREATE OR REPLACE VIEW authors_articles AS
            SELECT authors.name, articles.title
            FROM authors, articles
            WHERE articles.author=authors.id;

            CREATE OR REPLACE VIEW popular_authors AS
            SELECT authors_articles.name,
            SUM(popular_articles.views) AS sum
            FROM authors_articles, popular_articles
            WHERE popular_articles.title=authors_articles.title
            GROUP BY authors_articles.name
            ORDER BY sum DESC;''')

cur.execute(queryTwo)


queryThree = ('''CREATE OR REPLACE VIEW status_error AS
              SELECT to_char(time, 'Month DD YYYY')
              AS time, status
              FROM log;

              CREATE OR REPLACE VIEW error_404 AS
              SELECT time, count (*) AS total
              FROM status_error
              WHERE status='404 NOT FOUND'
              GROUP BY time
              ORDER BY time;

              CREATE OR REPLACE VIEW total_status AS
              SELECT time, count (*) AS everything
              FROM status_error
              GROUP BY time
              ORDER BY time;

              CREATE OR REPLACE VIEW TogethaForeva AS
              SELECT total_status.time,
              error_404.total, total_status.everything
              FROM total_status
              LEFT JOIN error_404
              ON total_status.time=error_404.time
              ORDER BY total_status.time;''')

cur.execute(queryThree)

error_logs = '''
WITH answer AS (
              SELECT ( total::float / everything::float * 100)::float
              AS answer, time
              FROM TogethaForeva)
              SELECT TogethaForeva.time, answer.answer
              FROM TogethaForeva
              JOIN answer
              ON answer.time = TogethaForeva.time
              WHERE answer.answer > 1.0;''')

# Printing out Query 1

print("The most popular articles are:")
cur.execute("SELECT * FROM popular_articles")
for article in cur:
    print(article)

print("-------")
print("The most popular authors are:")

#Printing out Query 2

cur.execute("SELECT * FROM popular_authors")

for name in cur:
print(name)
print("-------")

#Printing out Query 3

print("The day with most errors:")
cur.execute(error_logs)

for error in cur:
print(error)
>>>>>>> 1487218a92f9e7eba53e9229d0b2b64e717cfe6f
