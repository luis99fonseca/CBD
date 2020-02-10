import time
import random
import string

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def random_date(start="2015-1-1 1:00", end="2019-1-1 23:00"):
    return str_time_prop(start, end, '%Y-%m-%d %H:%M', random.random())

jogosid_nome = []
jogosid_release = []
jogosid_develop = []
jogosid_age = []

jogos_names = ["Final", "Digital","Insane", "Infamous", "Car", "Motor", "Last", "First", "Night", "Dawn", "Sun", "Earth", "Guardian", "Soldier", "Fight", "War", "I", "II", "Ultimate", "Plus", "Ultra", "Pro", "Extreme"]
jogos_devs = ["Pokemon", "Sony", "Nintendo", "Valve", "Naughty Dog", "Intel"]

# games_dict = {}
all_names = []

for jogosid in range(40):

    temp_name = random.choice(jogos_names) + " " + random.choice(jogos_names)
    while temp_name in all_names:
        temp_name = random.choice(jogos_names) + " " + random.choice(jogos_names)

    all_names.append(temp_name)
    jogosid_nome.append(temp_name )

    jogosid_release.append(random_date())

    temp_dev = jogosid % len(jogos_devs)
    jogosid_develop.append( jogos_devs[temp_dev] )

    temp_age = random.choice([2, 8, 12, 16, 18])
    jogosid_age.append(temp_age)

locations = ["Aveiro", "Viseu", "Coimbra", "Faro", "Porto", "Sagres", "Super", "Bock", "Martin", "Lisboa", "Angola", "America"]

devs_dict = {}

for k in jogos_devs:
    devs_dict[k] = random.choice(locations)

nomes = ["João", "José", "Maria", "Luís", "Miguel", "Rafael", "Rafaela", "Pedro", "Rita", "Inês", "Marta",
              "Margarida", "Francisca", "Leonor", "Ana", "Lara", "Alice", "Mafalda", "Helena", "Teresa", "Carla", "Filipa",
                  "Soraia", "Rosa", "Vera", "Santiago", "Rodrigo"]

users_userName = []
users_name = []
users_email = []

for i in range(500):
    t_name = nomes[(random.randint(0, len(nomes) - 1))]
    t_Rname = t_name + str(random.randint(0,99))

    users_userName.append(t_Rname)
    users_name.append(t_name)
    users_email.append(t_Rname.lower() + "@" + str(random.choice(["hotmail.com", "ua.pt", "outlook.pt"])))

if True:
    print("username", "user", "mail", "jogoname", "jogoage", "jogorelease", "devname", "devloc", sep=",")
    for u in range(350):
        all_usergame = []
        for j in range(random.randint(1, 6)):
            t_game = random.randint(0, len(jogosid_nome) - 1)
            while t_game in all_usergame:
                t_game = random.randint(0, len(jogosid_nome) - 1)
            all_usergame.append(t_game)
            print(users_userName[u], users_name[u], users_email[u], jogosid_nome[t_game], jogosid_age[t_game], jogosid_release[t_game], jogosid_develop[t_game],  devs_dict[jogosid_develop[t_game]] ,sep=",")