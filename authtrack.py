from datetime import datetime
import requests
import re


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
# Opens file then puts lines into a List 
def open_file(file:str) -> list:
    with open(file) as f:
        data = f.readlines()
    return data

def ip_valid(line :str) -> str: 
    # Returns an ip if there is an ip in the string given
    ip = re.search(r"(\d){1,3}.(\d){1,3}.(\d){1,3}.(\d){1,3}",line)
    if ip:
        return ip.group(0)
    return ""


def failed_attempts(data: list) -> list[str]: 
    # Returns a list of all the failed login attempts ips found in the auth.log
    ips = []
    for line in data:
        if ("Invalid" or "Failed" or "Closed") in line:
            ip = ip_valid(line)
            if ip != "":
                ips.append(ip)
    return ips




# Gets the ips
def get_ip(line:str)->str:
    line_stripped = line.split(' ')
    for case in line_stripped:
        if "from=" in case:
            return case.replace("from=","")
    return "NAN"


# Gets the users
def get_user(line:str)->str:
    line_stripped = line.split(' ')
    for case in line_stripped:
        if "user=" in case:
            return case.replace("user=","")
    return "NAN"


# Gets the ports
def get_port(line:str)->str:
    line_stripped = line.split(' ')
    for case in line_stripped:
        if "port=" in case:
            return case.replace("port=","")
    return "NAN"


# Gets the date and time of the connection
def get_date(line:str)->str:
    parts = line.split(' ')
    fulldatetime = parts[0] + " " + parts[1]
    dt = datetime.strptime(fulldatetime, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("[%m-%d %H:%M]")




# Prints formatted informations
# Prints formatted informations
def prints_attempts(data):
    for line in data:
        ip = get_ip(line)
        port = get_port(line)      # CALL the function
        user = get_user(line)
        country_city = get_country_city(ip)
        date = get_date(line)      # CALL the function

        if "Failed" in line:
            print(f"\033[91m{date} [FAILED CONNECTION] FROM {country_city[0]},{country_city[1]} USER : {user} , WITH IP {ip}:{port}\033[0m")
        elif "Accepted" in line:
            print(f"\033[92m{date} [ACCEPTED CONNECTION] FROM {country_city[0]},{country_city[1]} USER : {user} , WITH IP {ip}:{port}\033[0m")



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
    prints_attempts(data)