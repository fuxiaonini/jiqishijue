import sqlite3

# 检查人员学号是否存在
def check_person_is_new(number):
    conn = sqlite3.connect("db/data.db")
    with conn:
        cur = conn.cursor()
        cur.execute("select number, name from person WHERE number = ?", (number,))
        return cur.fetchall()

def record_person(data):
    conn = sqlite3.connect("db/data.db")
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO person (number, name) VALUES (?,?)", data)
        return cur.fetchall()

def get_all_person_list():
    conn = sqlite3.connect("db/data.db")
    with conn:
        cur = conn.cursor()
        cur.execute("select number, name from person")
        return cur.fetchall()

def num2name(number):
    conn = sqlite3.connect("db/data.db")
    with conn:
        cur = conn.cursor()
        cur.execute("select name from person WHERE number = ?", (number,))
        return cur.fetchall()[0][0]

def sign2db(id, name, time):
    conn = sqlite3.connect("db/data.db")
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO sign (id, name, time) VALUES (?,?,?)", (id, name, time))

def getall_sign_records():
    conn = sqlite3.connect("db/data.db")
    with conn:
        cur = conn.cursor()
        cur.execute("select * from sign")
        return cur.fetchall()

def db_reset(table_name):
    conn = sqlite3.connect("db/data.db")
    with conn:
        cur = conn.cursor()
        cur.execute(f"delete from {table_name }")

def show_tables():
    conn = sqlite3.connect("db/data.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM sqlite_master where type='table'")
        print(cur.fetchall())

def show_table_data(table_name):
    conn = sqlite3.connect("db/data.db")
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        print(cur.fetchall())

if __name__=="__main__":
    db_reset("person")
    db_reset("sign")
    show_table_data("person")
    show_table_data("sign")

