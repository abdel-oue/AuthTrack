from datetime import datetime
import re

#line ='Sep 29 00:11:20 ns sshd[2988132]: Accepted password for invalid user test from 85.209.11.27 port 35198 ssh2'
def convert_log_date(date : str) -> datetime:
    # This funtion returns datetime object based on the date on the log file "Sep 19 00:01:00"
    date_stripped = date.strip().split()
    month = date_stripped[0]
    day = date_stripped[1]
    time = date_stripped[2]
    time_stripped = time.split(':')
    month_number = datetime.strptime(month, '%b').month
    return datetime(2025, month_number, int(day), int(time_stripped[0]),int(time_stripped[1]),int(time_stripped[2]))

def extract_line(line : str)-> tuple: 
    invalid_pattern = r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+.+Invalid user\s+(\w+)\s+from\s+(\d{1,3}(?:\.\d{1,3}){3}) port (\d{1,5})(?:\s+(\w+))?'
    failed_pattern = r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+.+Failed password for (?:invalid user )?(\w+)\s+from\s+(\d{1,3}(?:\.\d{1,3}){3}) port (\d{1,5}) (\w+)'
    accepted_pattern = r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+.+Accepted password for (\w+)\s+from\s+(\d{1,3}(?:\.\d{1,3}){3}) port (\d{1,5}) (\w+)'
    status = "Failed"
    match = re.search(failed_pattern, line)
    if not match:
        match = re.search(accepted_pattern, line)
        status = "Accepted"
    if not match:
        match = re.search(invalid_pattern, line)
        status = "Invalid"
    if match : 
        date = match.group(1)
        clean_date = convert_log_date(date)
        user = match.group(2)
        ip = match.group(3)
        service = match.group(5) or "Unknown"
        return (clean_date,user,ip,status,service)
    return ()

def extract_data(url :str) -> list[tuple[str,...]]:
    datalist = []
    with open(url) as f:
        data = f.readlines()
        for line in data:
            linedata = extract_line(line)
            if linedata:
                datalist.append(linedata)
    return datalist
