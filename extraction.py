import re

#ligne par ligne .search 
line ='Sep 29 00:11:20 ns sshd[2988132]: Failed password for invalid user test from 85.209.11.27 port 35198 ssh2'
def extraction_data(url : str)-> list[tuple[str,...]]: 
    data = []
    pattern = r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+.+(Failed password for)? invalid user\s+(\w+)+\s+from\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'

    match = re.search(pattern,line)
    if match : 
        date = match.group(1)
        status = match.group(2)
        user = match.group(3)
        ip = match.group(4)
        data.append((date,status,user,ip))
    return data
