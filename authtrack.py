from datetime import datetime
import requests
import re

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


def draw_plot_and_write_log(datalist: list):
    # Data received is in this form (date, attempt, session, user, ip)
    try:
        countriesdata = {}
        logdata = []
        userdata = []
        for i,data in enumerate(datalist):
            print("DATA NUMBER :",i)
            if data[1] == "Invalid":
                country = get_country(data[4])
                if country != "NAN":
                    countriesdata[country] = countriesdata.get(country, 0) + 1
                elif country == "NAN":
                    logdata.append(data)
            elif data[1] == "valid":
                userdata.append((data[0],data[3]))
        
        draw_user_data(userdata)
        draw_countries_data(countriesdata)

    except Exception:
        return 

def draw_user_data(datalist: list):
    try:
        # 1. count how many times each user appears
        counts = {}
        for _, user in datalist:
            if user in counts:
                counts[user] += 1
            else:
                counts[user] = 1

        # 2. remove duplicates and format date
        newlist = []
        seen = []
        for date, user in datalist:
            if (date, user) not in seen:
                date_str = date.strftime("%m/%d")  # format date
                newlist.append((date_str, user, counts[user]))
                seen.append((date, user))

        # 3. assign a color per user
        colors = ['r','g','b','c','m','y','k']
        user_colors = {}
        for i, item in enumerate(newlist):
            _, user,_ = item
            user_colors[user] = colors[i % len(colors)]

        # 4. plot each user
        for user in user_colors:
            x = [date for date, u, c in newlist if u == user]
            y = [c for date, u, c in newlist if u == user]
            plt.plot(x, y, 'o-', color=user_colors[user], label=user)

        # 5. titles, labels, legend
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
        x_countries = list(datalist.keys())   # keys → x-axis
        y_attacks   = list(datalist.values()) # values → y-axis
        print(datalist)
        plt.bar(x_countries, y_attacks, color='skyblue')  # bar chart looks better
        plt.title("Nombre d'attaques par pays")
        plt.xlabel("Pays")
        plt.ylabel("Nombre d'attaques")
        plt.grid(axis='y')  # only horizontal grid
        plt.show()

    except Exception as e:
        print(e)

def write_log_file(datalist : list):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # file handler
    file_handler = logging.FileHandler("auth.log")
    formatter = logging.Formatter(fmt="%(asctime)s level=%(levelname)s service=auth user=%(user)s ip=%(ip)s", datefmt="%Y-%m-%dT%H:%M:%S%z")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    for date, attempt, session, user, ip in datalist:
        extra = {"user": user, "ip": ip}
        logger.info("", extra=extra)

if __name__ == "__main__":
    pass