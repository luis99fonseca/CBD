from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345"))

def runQuery(query):
    with driver.session() as session:
        return session.run(query)

if False:
    with driver.session() as session:
        print("Populating DB...")
        session.run("load csv with Headers from 'file:///jogosbd.csv' as row \
                    MERGE (n:User {name:row.username, real_name: row.user, mail: row.mail}) \
                    merge (m:Game {name : row.jogoname, age : row.jogoage, release: row.jogorelease }) \
                    merge (n) -[:OWNS ]-> (m) \
                    Merge (l:Developer {name: row.devname, location: row.devloc}) \
                    merge (m) -[:DEV_BY ]-> (l)")

if True:

    with open("CBD_L44c_output.txt", "w") as temp_file:
        temp_file.write("-------------1\n")
        temp_file.write("Get all the games in the database\n")
        for resul in runQuery("match (n:Game) \
                                return n"):
            temp_file.write(str(resul.items()[0][1]) + "\n")
            # print(resul.items()[0][1].get("name"))
        temp_file.write("-------------2\n")
        temp_file.write("Get all the Developers with locations in Faro\n")
        for resul in runQuery("match (n:Developer {location : \"Faro\"}) \
                                return n"):
            temp_file.write(str(resul.items()[0][1]) + "\n")
        temp_file.write("-------------3\n")
        temp_file.write("Get all the Developers and their number of Games\n")
        for resul in runQuery("match (d:Developer)<-[:DEV_BY]-(g) \
                                return d, count(g) as Jogos"):
            temp_file.write(str(resul.items()[0][1]) + " -> " + str(resul.items()[1][1]) + "\n")
        temp_file.write("-------------4\n")
        temp_file.write("Top 3 users with the most games owned\n")
        for resul in runQuery("match (u:User)-[:OWNS]->(g) \
                                return u.name, count(g) as noJogos \
                                order by noJogos DESC \
                                limit 3"):
            temp_file.write(str(resul.items()[0][1]) + " -> " + str(resul.items()[1][1]) + "\n")
        temp_file.write("-------------5\n")
        temp_file.write("Number of users in the database\n")
        for resul in runQuery("match (u:User) \
                                return count(u)"):
            temp_file.write(str(resul.items()[0][1]) + "\n")
        temp_file.write("-------------6\n")
        temp_file.write("Games for adults (18+)\n")
        for resul in runQuery("match (g:Game {age : \"18\"}) \
                                return g"):
            temp_file.write(str(resul.items()[0][1]) + "\n")
        temp_file.write("-------------7\n")
        temp_file.write("Games for age (12+)\n")
        for resul in runQuery("match (g:Game) \
                                with toInteger(g.age) as idade, g \
                                where idade >= 12 \
                                return g"):
            temp_file.write(str(resul.items()[0][1]) + "\n")
        temp_file.write("-------------8\n")
        temp_file.write("Games of the 'Dawn' series\n")
        for resul in runQuery("match (g:Game) \
                                where g.name =~ \"Dawn .*\" \
                                return g"):
            temp_file.write(str(resul.items()[0][1]) + "\n")
        temp_file.write("-------------9\n")
        temp_file.write("Number of users withing the 'UA' domain\n")
        for resul in runQuery("match (u:User) \
                                where u.mail =~ \".*@ua.pt\" \
                                return count(u)"):
            temp_file.write(str(resul.items()[0][1]) + "\n")
        temp_file.write("-------------10\n")
        temp_file.write("Most popular Game\n")
        for resul in runQuery("match (g:Game)<-[:OWNS]-(u:User) \
                                return g.name, count(u) as noUser \
                                order by noUser desc \
                                limit 1"):
            temp_file.write(str(resul.items()[0][1]) + "\n")


driver.close()