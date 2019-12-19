import sqlite3

db = sqlite3.connect('opros.db')
cur = db.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS 
    answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    q1 INTEGER,
    q2 INTEGER,
    q3 INTEGER
    )""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS 
    questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT
    )""")

cur.execute(
    """CREATE TABLE IF NOT EXISTS
    user ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    age INTEGER,
    town TEXT,
    gender TEXT )""")


cur.execute(
    """INSERT OR REPLACE INTO questions VALUES ('1',' Займи мне 100 рублей денег.'), 
    ('2','Собака Трезор громко лаял.'), 
    ('3','Согласно приказа все сотрудники должны являться во время.')""")
db.commit()