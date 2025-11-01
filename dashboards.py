from country_names import country_names 
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import os




def draw_countries(countrylist):
    # countrylist: [(country_code, attempts), ...]
    x_countries = []
    y_attacks = []

    for code, attacks in countrylist:
        full_name = country_names.get(code, code)
        x_countries.append(full_name)
        y_attacks.append(attacks)

    plt.figure(figsize=(12,6))
    plt.bar(x_countries, y_attacks, color='skyblue')
    plt.xticks(rotation=45, ha='right')  # rotate so full names fit
    plt.title("Nombre d'attaques par pays")
    plt.ylabel("Nombre d'attaques")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def draw_userdata(userlist :list):
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