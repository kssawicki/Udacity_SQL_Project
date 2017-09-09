# Udacity Project 3: Logs Analysis Project

## Introduction

Project 3 is an in-depth look into database querying and writing in SQL, to then translate into Python. This project provides a data-heavy database to query for several prompts. The following will help navigate and understand how to answer the three database questions posed by the third project's guidelines. This will discuss the necessary software needed and outline the process taken for each query.

## Software Needed

* A terminal/command prompt window 
* VirtualBox
* Vagrant
* Psycopg2 (Required Python module)
* From Udacity, download this file: [newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

** Setup

1. For Mac or Linux, the regular terminal program will work for this project. For Windows, visit [Git Bash](https://git-scm.com/downloads) to download a terminal.
2. Install VirtualBox (to allow for access to the same software regardless of what type of computer is being used)
3. Within the terminal window, cd to the "vagrant" directory (provided from the FSND-Virtual-Box zip)
4. Within the vagrant subdirectory, run the command `vagrant up`
5. Then log onto it with `vagrant ssh`
6. After successfully logging into Vagrant, cd into `/vagrant`
<<<<<<< HEAD
7. Download [psycopg2](https://pypi.python.org/pypi/psycopg2) in order for the file to connect to the database, "news."
```
#! /usr/bin/env python2

import psycopg2

conn = psycopg2.connect("f*dbname={news} user={user} password={password}")
cur = conn.cursor()
```


## Technical

1. In order to load the data, use the command `psql -d news -f newsdata.sql` This will open the PostgreSQL command line program, connect the database, and run the SQL statements within newsdata.sql
2. The datbase contains 3 tables that will be needed to answer Udacity's questions: _authors, articles, and log._
3. There are three questions to be answered in regard to these tables. (See The SQL section)
4. In order to run my program, you will need to type your username and password in order to use postgres to access the database, "news."

## Bugs
_None to be reported so far; however, keep in mind that once VIEWs are created, there is no need to query for them to be created again. It may cause an error if queried to be created again._(Hence: CREATE OR REPLACE)

# The code and queries:

Top of document:

```
#! /usr/bin/env python3

import psycopg2

conn = psycopg2.connect("f*dbname={dbname} user={user} password={password}")
cur = conn.cursor()
```

1. What are the most popular three articles of all time?

```
CREATE VIEW popular_articles AS
SELECT title, count(*) AS views
FROM articles, log
WHERE articles.slug=substring(log.path FROM 10)
GROUP BY articles.title
ORDER BY views DESC
limit 3;
```
_The view, popular articles, will be helpful to use in the next question because it has picked out the most popular articles views from the articles and log tables._

2. Who are the most popular article authors of all time?

```
SELECT authors.name, count(*) as num
FROM articles, authors, log
WHERE log.status='200 OK'
AND authors.id = articles.author
AND articles.slug = substr(log.path, 10)
GROUP BY authors.name
ORDER BY num desc;
```

3. On which days did more than 1% of requests lead to errors?

This is going to get elaborate. First, create a view that will organize and extract the _log_ table's information: the days and statuses. 

```
CREATE VIEW status_error AS
SELECT to_char(time, 'Month DD YYYY') AS time, status
FROM log;
```
Next, create a view that will extract from the status_error view, but only look for when the status is "404 NOT FOUND"

```
CREATE VIEW error_404 AS
SELECT time, count (*) AS total
FROM status_error
WHERE status='404 NOT FOUND'
GROUP BY time
ORDER BY time;
```
Then, create a view that has extracted from status_error to obtain all statuses (404 or 200) for every day. 

```
CREATE VIEW total_status AS
SELECT time, count (*) AS everything
FROM status_error
GROUP BY time
ORDER BY time;
```

Then create a view that will select from the previous views made to organize a table that will display, the total of 404 statuses per day, and the grand total amount of statuses per day. 

```
CREATE VIEW TogethaForeva AS
SELECT total_status.time, error_404.total, total_status.everything
FROM total_status
LEFT JOIN error_404
ON total_status.time=error_404.time
ORDER BY total_status.time;
```

Lastly, the "answer" keyword can then be queried to be displayed by the date and the total amount of 404 statuses greater than 1% on a given day. In order for SQL to relay the information we need, the cast "float" allows the information that will be interpreted to be displayed in the format the answer to the question needs. 

```
WITH answer AS (
  SELECT ( total::float / everything::float * 100)::float AS answer, time
  FROM TogethaForeva
)
SELECT TogethaForeva.time, answer.answer
FROM TogethaForeva
JOIN answer
ON answer.time = TogethaForeva.time
WHERE answer.answer > 1.0;
```

## License

MIT License

Copyright (c) [2017] [Udacity / Katherine Sawicki]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
