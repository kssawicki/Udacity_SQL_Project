#!/usr/bin/env python3
import psycopg2
from variables import database, user, password

conn = psycopg2.connect(f"dbname={database} "
                        f"user={user} password={password}")
DBNAME = 'news'
# conn = psycopg2.connect(dbname=DBNAME)
cur = conn.cursor()

questionOne = "What are the most popular three articles of all time?"

queryOne = '''CREATE OR REPLACE VIEW popular_articles AS
            SELECT title, count(*) AS views
            FROM articles, log
            WHERE articles.slug=substring(log.path FROM 10)
            GROUP BY articles.title
            ORDER BY views DESC'''

cur.execute(queryOne)

select_three_most_popular_articles = '''
    SELECT title, views FROM popular_articles LIMIT 3
'''


# Printing out Query 1

cur.execute(select_three_most_popular_articles)

print("The most popular articles are:")
print("-" * 20)
for article in cur:
    print("\"{}\" -- {}".format(article[0], article[1]))


queryTwo = '''SELECT authors.name, count(*) as num
            FROM articles, authors, log
            WHERE log.status='200 OK'
            AND authors.id = articles.author
            AND articles.slug = substr(log.path, 10)
            GROUP BY authors.name
            ORDER BY num desc;'''

cur.execute(queryTwo)

# Printing out Query 2

print("The most popular authors are:")
print("-" * 20)
for authors in cur:
    print("\"{}\" -- {}".format(authors[0], authors[1]))


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
              SELECT ROUND(
                ( total::float / everything::float * 100)::DECIMAL,
                2
                )::DECIMAL
              AS answer, time
              FROM TogethaForeva)
              SELECT TogethaForeva.time, answer.answer
              FROM TogethaForeva
              JOIN answer
              ON answer.time = TogethaForeva.time
              WHERE answer.answer > 1.0;
              '''


cur.execute(error_logs)

# Printing out Query 3

print("The day with most errors:")
print("-" * 20)
for error in cur:
    print("\"{}\" -- {}%".format(error[0], error[1]))
