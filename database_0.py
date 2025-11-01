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

def get_country_failed_attempts(con):
    """
    Returns list of tuples: [(country, attempts), ...]
    attempts = count of rows where status is Invalid or Failed
    """
    query = """
    SELECT country, COUNT(*) AS attempts
    FROM ssh_logs
    WHERE status IN ('Invalid', 'Failed')
    GROUP BY country
    """
    try:
        cursor = con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()  # [(country1, attempts1), (country2, attempts2), ...]
        cursor.close()
        return results
    except connector.Error as e:
        print("Error:", e)
        return []
    
def get_accepted_user_data(con):
    """
    Returns list of tuples: [(date, user, attempts), ...]
    attempts = count of rows where status is Invalid or Failed
    """
    query = """
    SELECT DATE(log_date) as day, user, COUNT(*) as attempts
    FROM ssh_logs
    WHERE status = 'Accepted'
    GROUP BY day, user
    HAVING COUNT(*) > 0
    ORDER BY day, user
    """
    try:
        cursor = con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()  # [(2025-10-04, 'user1', 3), ...]
        cursor.close()
        return results
    except connector.Error as e:
        print("Error:", e)
        return []

def get_logging_data(con):
    """
    Returns [(log_date, service, user, ip, status), ...]
    for rows where country IS NULL and status is Failed or Accepted.
    """
    query = """
    SELECT log_date,
           service,
           user,
           ip,
           status
    FROM ssh_logs
    WHERE country IS NULL
      AND status IN ('Failed', 'Accepted', 'Invalid')
    ORDER BY log_date;
    """
    try:
        cursor = con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except connector.Error as e:
        print("Error:", e)
        return []