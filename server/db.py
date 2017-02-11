import json
import psycopg2

def connect():
    conf = json.load(open("db.json"))
    conn = psycopg2.connect(database=conf['database'], user=conf['username'], password=conf['password'], host=conf['host'])
    cursor = conn.cursor()
    return conn, cursor
