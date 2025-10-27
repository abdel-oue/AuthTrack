from datetime import datetime
import requests
import re
from mysql import connector

filename = './data/auth.log.1'

"""
The failed authentifications are represented in the log files by these keywords :
 - Invalid user
 - Failed password
 - Connection closed
The successful authentifications :
 - Accepted password
 - Accepted publickey
"""

def get_connection():
    con = connector.connect(
        user='root',
        password='',
        database='PythonLogs',
        host='127.0.0.1',
        port=3306
    )
    return con

def open_file(file:str) -> list:
    # Opens file then puts lines into a List 
    with open(file) as f:
        data = f.readlines()
    return data

def ip_valid(line :str) -> str: 
    # Returns an ip if there is an ip in the string given
    ip = re.search(r"(\d){1,3}\.(\d){1,3}\.(\d){1,3}\.(\d){1,3}",line)
    if ip:
        return ip.group(0)
    return ""

def extract_data(data) -> list:
    # Returns list of tuples (date, attempt, session, user, ip,)
    datalist = []
    
    for line in data:
        datatuple = ()
        # IP Extraction
        ip = ip_valid(line)

        # USER Extraction
        line_stripped = line.split()
        pos = 0
        if 'user' in line_stripped:
            pos = line_stripped.index('user')  # gives the position of 'user'
        if pos+1 > len(line_stripped): 
            user = line_stripped[pos + 1]
        else:
            user = ""
        # DATE Extraction

        month = line_stripped[0]
        day = line_stripped[1]
        time = line_stripped[2]
        time_stripped = time.split(':')
        month_number = datetime.strptime(month, '%b').month
        date =  datetime(2025, month_number, int(day), int(time_stripped[0]),int(time_stripped[1]),int(time_stripped[2]))

        # SESSION Extraction
        pid = None
        for part in line_stripped:
            if part.startswith('sshd['):
                pid = part[5:-2]  # extract PID
                break

        # ATTEMPT Extraction
        attempt = "None"
        if ("Invalid" or "Failed" or "closed") in line:
            attempt = "Invalid"
        elif ("Accepted") in line:
            attempt = "valid"
        datatuple = (date,attempt,pid,user,ip)
        datalist.append(datatuple)
    return datalist

def creating_table(con):
    query = 'CREATE TABLE IF NOT EXISTS ssh_logs (log_date DATETIME NOT NULL,attempt VARCHAR(50) NOT NULL,session_id VARCHAR(50) NOT NULL,username VARCHAR(50) NOT NULL,ip_address VARCHAR(15) NOT NULL);'
    try:
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
    except connector.Error as e:
        print("Error:", e)
        return False
    
def data_is_clean(data):
    # We don't want the lines where the the ip is null the username is null 
    # (date, attempt, session, user, ip,)
    if (data[1] == None and data[3] == "") or data[4] == "":
        return False
    return True

def insert_to_table(con, datalist):
    query = "INSERT INTO ssh_logs (log_date, attempt, session_id, username, ip_address)VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor = con.cursor()
        for data in datalist:
            if data_is_clean(data):
                cursor.execute(query, data)
        con.commit()
    except connector.Error as e:
        print("Error:", e)
        return False


def get_country_city(ip: str)->list:
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url, timeout=4)
        if response.status_code == 200:
            data = response.json()
            country_city = [data.get("country"),data.get("city")]
            return country_city
        return []
    except Exception as e:
        return []


if __name__ == "__main__":
    data = open_file(filename)
    datalist = extract_data(data)

    con = get_connection()
    creating_table(con)
    insert_to_table(con,datalist)