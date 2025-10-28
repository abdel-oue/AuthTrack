from datetime import datetime
import requests
import re
from mysql import connector
from matplotlib import pyplot as plt
import logging


filename = './data/small-auth.log'

"""
The failed authentifications are represented in the log files by these keywords :
 - Invalid user
 - Failed password
 - Connection closed
The successful authentifications :
 - Accepted password
 - Accepted publickey
"""
#---------------------------- DATABASE MANAGEMENT ----------------------------
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
    query = 'CREATE TABLE IF NOT EXISTS ssh_logs (log_date DATETIME NOT NULL,attempt VARCHAR(50) NOT NULL,session_id VARCHAR(50) NOT NULL,username VARCHAR(50) NOT NULL,ip_address VARCHAR(15) NOT NULL);'
    try:
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
    except connector.Error as e:
        print("Error:", e)
        return False   
def data_is_clean(data):
    if (data[1] == None and data[3] == "") or data[2] == "None" or data[4] == "":
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
#---------------------------- DATA EXTRACTION ----------------------------
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
        if data_is_clean(datatuple): # !!
            datalist.append(datatuple)
    return datalist
#---------------------------- DATA VISUALISATION ----------------------------
def get_country(ip: str)->str:
    country = "NAN"
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            country = data.get("country")
            return country
        return country
    except Exception :
        return country

def draw_plot_and_write_log(datalist: list):
    # Data received is in this form (date, attempt, session, user, ip)
    try:
        countriesdata = {}
        logdata = []
        userdata = []
        for data in datalist:
            if data[1] == "Invalid":
                country = get_country(data[4])
                if country != "NAN":
                    countriesdata[country] = countriesdata.get(country, 0) + 1
                elif country == "NAN":
                    logdata.append(data)
            elif data[1] == "valid":
                userdata.append((data[0],data[3]))
        
        draw_user_data(userdata)
        #draw_countries_data(countriesdata)

    except Exception:
        return 

def draw_user_data(datalist : list):
    try:
        counts = {}
        for _, user in datalist:
            if user in counts:
                counts[user] += 1
            else:
                counts[user] = 1

        newlist = []
        for date, user in datalist:
            if user not in newlist:
                newlist.append((date, user, counts[user]))

        user_colors = {}
        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
        for i, user in enumerate(set(u for _, u, _ in newlist)):
            user_colors[user] = colors[i % len(colors)]

        for user in user_colors:
            x = [date for date, u, c in newlist if u == user]
            y = [c for date, u, c in newlist if u == user]
            plt.plot(x, y, 'o-', color=user_colors[user], label=user)
        plt.title("Nombre d'accès par utilisateur")
        plt.xlabel("Date")
        plt.ylabel("Nombre d'occurrences")
        plt.grid(True)
        plt.legend()
        plt.show()


    except Exception as e:
        print(e)

def draw_countries_data(datalist : dict):
    try:
        x_years=[]
        y_score=[]
        for matricule,year,moyenne in data:
            x_years.append(year)
            y_score.append(moyenne)
        plt.plot(x_years, y_score, 'o-g')
        plt.title(f'{matricule}')
        plt.xlabel('Year')
        plt.ylabel('Moyenne')
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(e)

def write_log_file(datalist : list):
    pass
if __name__ == "__main__":
    # Data extraction
    data = open_file(filename)
    datalist = extract_data(data)

    # Database management
    con = get_connection()
    creating_table(con)
    insert_to_table(con,datalist)

    # Visualization
    draw_plot_and_write_log(datalist)
