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

def insert(table, attributes, values):
	return f"INSERT INTO {table} {attributes} VALUES {values};"

def update(table, attributes, values, cond1, cond2):
	return f"UPDATE {table} SET {attributes} = {values} WHERE {cond1} = '{cond2}';"

def update2(table, attributes, values, cond1, cond2, cond3, cond4):
	return f"UPDATE {table} SET {attributes} = {values} WHERE {cond1} = {cond2} and {cond3} = '{cond4}';"

jogosid_id = []
jogosid_nome = []
jogosid_release = []
jogosid_develop = []
jogosid_age = []

jogos_names = ["Last", "First", "Night", "Dawn", "Sun", "Earth", "Guardian", "Soldier", "Fight", "War", "I", "II", "Ultimate", "Plus", "Ultra", "Pro", "Extreme"]
jogos_devs = ["Pokemon", "Sony", "Nintendo", "Valve", "Naughty Dog", "Intel"]

ages_dict = {}
deve_dict = {}

for jogosid in range(20):

    jogosid_id.append(jogosid)

    temp_name = random.choice(jogos_names) + " " + random.choice(jogos_names)
    jogosid_nome.append(temp_name )

    jogosid_release.append(random_date())

    temp_dev = jogosid % len(jogos_devs)
    jogosid_develop.append( temp_dev )

    temp_age = random.choice([2, 8, 12, 16, 18])
    jogosid_age.append(temp_age)

    if temp_age not in ages_dict:
        ages_dict[temp_age] = [jogosid]
    else:
        ages_dict[temp_age].append( jogosid )

    if temp_dev not in deve_dict:
        deve_dict[temp_dev] = [jogosid]
    else:
        deve_dict[temp_dev].append(jogosid)

for i in range(20):
    print(insert("jogosId", ("id", "name", "released", "developer", "pg"), (jogosid_id[i], jogosid_nome[i], jogosid_release[i], jogosid_develop[i], jogosid_age[i])))
    print(insert("jogosName", ("id", "name", "released", "developer", "pg"), (jogosid_id[i], jogosid_nome[i], jogosid_release[i], jogosid_develop[i], jogosid_age[i])))


locations = ["Aveiro", "Viseu", "Coimbra", "Faro", "Porto", "Sagres", "Super", "Bock", "Martin", "Lisboa", "Angola", "America"]

for key in deve_dict:
    print(insert("developerId", ("id", "name", "foundation", "gamesowned", "locations"), ( key, jogos_devs[key], random_date(), deve_dict[key], [locations[random.randint(0, len(locations) - 1)] for i in range(random.randint(1,3)) ]  ) ))

nomes = ["João", "José", "Maria", "Luís", "Miguel", "Rafael", "Rafaela", "Pedro", "Rita", "Inês", "Marta",
              "Margarida", "Francisca", "Leonor", "Ana", "Lara", "Alice", "Mafalda", "Helena", "Teresa", "Carla", "Filipa",
                  "Soraia", "Rosa", "Vera", "Santiago", "Rodrigo"]

users_userName = []
users_name = []
users_email = []
users_games = []

for i in range(15):
    t_name = nomes.pop(random.randint(0, len(nomes) - 1))
    t_Rname = t_name + str(random.randint(0,99))

    users_userName.append(t_Rname)
    users_name.append(t_name)
    users_email.append(t_Rname.lower() + "@" + str(random.choice(["hotmail.com", "ua.pt", "outlook.pt"])))

for i in range(15):
    temp_jogos = [random.randint(0, jogosid - 1) for i in range(random.randint(1,4))]
    print(insert("users", ("username", "name", "games", "email", "gameinfo"), (users_userName[i], users_name[i], temp_jogos,users_email[i], { "most_played": random.choice(temp_jogos), "least_played" : random.choice(temp_jogos), "favorite" : random.choice(temp_jogos) }  )))

for key in ages_dict:
    print(insert("pgTable", ("pg", "games"), (key, ages_dict[key])))