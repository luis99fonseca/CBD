# pip3 install cassandra-driver

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# https://docs.datastax.com/en/developer/python-driver/3.20/getting_started/

cluster = Cluster()
session = cluster.connect()
session.execute("USE cbde2  ")

# Pesquisa
usernames = session.execute("SELECT * from users")

for n in usernames:
    print(n.usernamer, ", is following ->", n[-1])
    # diferentes maneiras de aceder

                                                                                # Note: you must always use a sequence for the second argument, even if you are only passing in a single variable;
nameParametized = session.execute("SELECT nome from users WHERE usernamer = %s", ("Carla39",))
print("Nome is: ", nameParametized[0])

# Inserção
# insertion = SimpleStatement("INSERT into users (usernamer, nome, email) VALUES (%s, %s, %s)")
# session.execute(insertion, ("Maria69", "Maria", "mary@ua.pt"))

nameParametized = session.execute("SELECT nome from users WHERE usernamer = %s", ("Maria69",))
print("Nome is: ", nameParametized[0])

# Update
# updateQuery = session.execute("UPDATE users SET email = 'carla039@gmail.com' WHERE usernamer = 'Carla39';")

nameParametized = session.execute("SELECT nome, email from users WHERE usernamer = %s", ("Carla39",))
print("Nome is: ", nameParametized[:])

"""
b)
"""
print()
print("select * from tagsvideo WHERE tag = 'aveiro';")
for row in session.execute("select * from tagsvideo WHERE tag = 'aveiro';"):
    print(row[:])
print("-----------------------------------------------")
print("select * from videoid LIMIT 6;")
for row in session.execute("select * from videoid LIMIT 6;"):
    print(row[:])
print("-----------------------------------------------")
print("select nome, followers from videoid where id = 23;")
for row in session.execute("select nome, followers from videoid where id = 23;"):
    print(row[:])
print("-----------------------------------------------")
print("select tag, count(videoid) from tagsvideo ;")
for row in session.execute("select tag, count(videoid) from tagsvideo ;"):
    print(row[:])
print("-----------------------------------------------")
print("select * from videoid ;")
for row in session.execute("select * from videoid ;"):
    print(row[:])
print("-----------------------------------------------")