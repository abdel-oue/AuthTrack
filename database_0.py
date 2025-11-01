
from mysql import connector

def get_connection():
    con = connector.connect(
        user='root',
        password='',
        database='PythonLogs',
        host='127.0.0.1',
        port=3306
    )
    return con

def creating_table(con):
    query = 'CREATE TABLE IF NOT EXISTS ssh_logs (log_date DATETIME NOT NULL,user VARCHAR(50) NOT NULL,ip VARCHAR(50) NOT NULL,status VARCHAR(50) NOT NULL,service VARCHAR(50) NOT NULL, country VARCHAR(50));'
    try:
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
    except connector.Error as e:
        print("Error:", e)
        return False   
    
def insert_to_table(con, datalist):
    query = "INSERT INTO ssh_logs (log_date, user, ip, status, service)VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor = con.cursor()
        cursor.executemany(query, datalist)  # <--- this one
        con.commit()
        cursor.close()
        return True
    except connector.Error as e:
        print("Error:", e)
        return False

def insert_country_to_line(con, country: str, ip: str):
    query = "UPDATE ssh_logs SET country = %s WHERE ip = %s"
    try:
        cursor = con.cursor()
        cursor.execute(query, (country, ip))
        con.commit()
        cursor.close()
        return True
    except connector.Error as e:
        print("Error:", e)
        return False
