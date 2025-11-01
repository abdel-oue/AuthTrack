from country_names import country_names 
from matplotlib import pyplot as plt

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

def draw_users(data):
    """
    data: [(day, user, attempts), ...] from get_accepted_user_data
    """
    labels = []
    counts = []

    for day, user, attempts in data:
        labels.append(f"{day} - {user}")
        counts.append(attempts)

    plt.figure(figsize=(12,6))
    plt.bar(labels, counts, color='skyblue')
    plt.xticks(rotation=45, ha='right')  # easy to read
    plt.title("Connexions acceptées par utilisateur et par jour")
    plt.ylabel("Nombre d'accès")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
