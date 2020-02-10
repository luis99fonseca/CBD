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

no_users = 11
no_videos = 0

users_userName = []
users_name = []
users_email = []
users_horaRegisto = []

nomes = ["João", "José", "Maria", "Luís", "Miguel", "Rafael", "Rafaela", "Pedro", "Rita", "Inês", "Marta",
                  "Margarida", "Francisca", "Leonor", "Ana", "Lara", "Alice", "Mafalda", "Helena", "Teresa", "Carla", "Filipa",
                  "Soraia", "Rosa", "Vera", "Santiago", "Rodrigo"]

for i in range(no_users):
    t_name = nomes.pop(random.randint(0, len(nomes) - 1))
    t_Rname = t_name + str(random.randint(0,99))
    users_userName.append(t_Rname)
    users_name.append(t_name)
    users_email.append(t_Rname.lower() + "@" + str(random.choice(["hotmail.com", "ua.pt", "outlook.pt"])))
    users_horaRegisto.append(random_date())

# print(users_userName)
# print(users_name)
# print(users_email)
# print(users_horaRegisto)

for i in range(no_users):
    print(insert("users", ("usernamer", "nome", "email", "hora_registo"), (users_userName[i], users_name[i], users_email[i], users_horaRegisto[i]) ))

print("------------1--------")
vid_c = 0
vid_id = []
vid_nome = []
vid_descric = []
vid_tags = []
vid_timeUp = []
vid_author = []

dict_tags = {}

for i in range(no_users):
    tags = ["comedy", "aveiro", "lifestyle", "reaction", "cooking", "top10", "gameplay", "gamer", "music"]
    description = "Lorem Ipsum is simply dummy text of the printing and typesetting industry."
    for vid in range(random.randint(1, 3)):
        vid_id.append(vid_c)
        vid_nome.append(random.choice(description.split()) + str(vid_c))
        vid_descric.append(description)
        temp_tags = [random.choice(tags) for l in range(random.randint(1,4))]
        vid_tags.append( temp_tags )

        for t in temp_tags:
            if t not in dict_tags:
                dict_tags[t] = [vid_c]
            else:
                dict_tags[t].append(vid_c)

        user = random.randint(0, no_users - 1)
        vid_timeUp.append(users_horaRegisto[user])
        vid_author.append(users_userName[user])
        vid_c += 1

# print(vid_id)
# print(vid_nome)
# # print(vid_descric)
# print(vid_tags)
# print(vid_timeUp)
# print(vid_author)
#
for i in range(vid_c):
    print(insert("videoId", ("id", "nome", "descricao", "tags", "time_upload", "autor"), (vid_id[i], vid_nome[i], vid_descric[i], vid_tags[i], vid_timeUp[i], vid_author[i]) ))

print("------------2--------")

comment_c = 0
comments = ["muito", "odeio", "adoro", "nice", "fixe", "bom", "mau", "like", "dislike", "fa"]
vid1_id = []
vid1_name = []
vid1_timeCom = []
vid1_autorCom = []
vid1_content = []

comment_autor = {}

needed_vidId = vid_id[:]
needed_vidTime = vid_timeUp[:]

for i in range(vid_c):
    index_vid1 = random.randint(0, len(vid_id) - 1)
    t_vid1_id = vid_id.pop(index_vid1)
    t_vid1_nome = vid_nome.pop(index_vid1)
    t_vid1_time = vid_timeUp.pop(index_vid1)
    for l in range(random.randint(1,4)):
        vid1_id.append(t_vid1_id)
        vid1_name.append(t_vid1_nome)
        vid1_timeCom.append(random_date(t_vid1_time))

        temp_author = random.choice(vid_author)

        vid1_autorCom.append(temp_author)

        t_vid1_comment = random.choice(comments) + " " + random.choice(comments)

        vid1_content.append(t_vid1_comment)
        if temp_author not in comment_autor:
            comment_autor[temp_author] = [t_vid1_comment]
        else:
            comment_autor[temp_author].append(t_vid1_comment)

        comment_c += 1

for i in range(comment_c):
    print(insert("video_vid_time", ("video_id", "video_name", "timeComment", "authorComment", "content"), (vid1_id[i], vid1_name[i], vid1_timeCom[i], vid1_autorCom[i], vid1_content[i]) ))
    print(insert("video_author_time", ("video_id", "video_name", "timeComment", "authorComment", "content"), (vid1_id[i], vid1_name[i], vid1_timeCom[i], vid1_autorCom[i], vid1_content[i]) ))


for i in range(no_users):
    print(update("users", "coments", comment_autor[vid1_autorCom[i]], "usernamer", vid1_autorCom[i]))
print("------------3--------")

### 4)
vidF = {}
userV = {}


for i in range(vid_c):
    t_vid2 = random.choice(vid1_id)
    for l in range(random.randint(1, 3)):
        t_user2 = random.choice(vid_author)
        if t_vid2 not in vidF:
            vidF[t_vid2] = [t_user2]
        elif t_user2 not in vidF[t_vid2]:
            vidF[t_vid2].append(t_user2)
        if t_user2 not in userV:
            userV[t_user2] = [t_vid2]
        elif t_vid2 not in userV[t_user2]:
            userV[t_user2].append(t_vid2)

# print(vidF)
# print("----------")
# print(userV)

for key in vidF:
        print(update2("videoid", "followers", vidF[key], "id", key, "time_upload", needed_vidTime[needed_vidId.index(key)] ))

for key in userV:
    print(update("users", "videosfollowing", userV[key], "usernamer", key))

print("------------4--------")

event_user = []
event_vid = []
event_time = []
event_action = []

for i in range(no_users):
    event_user.append(random.choice(vid_author))

    vid3 = random.choice(needed_vidId)
    event_vid.append(vid3)

    vid3_time = random_date( needed_vidTime[needed_vidId.index(vid3)]  )
    event_time.append(vid3_time)


    increment = 0
    action = {}
    sub_actions = {}
    act = ["play", "pause", "stop"]
    for l in range(random.randint(1,3)):
        timeS = random.choice([100, 110, 120]) + increment
        # if vid3_time not in action:
        #     action[vid3_time] = [(random.choice(["play", "pause", "stop"]), timeS)]
        # else:
        #     action[vid3_time].append((random.choice(["play", "pause", "stop"]), timeS))
        sub_actions[act.pop(random.randint(0, len(act) - 1))] = timeS
        increment += 15
    action[vid3_time] = sub_actions
    event_action.append(action)

# print(event_user, len(event_user))
# print(event_vid, len(event_vid))
# print(event_time, len(event_time))
# print(event_action, len(event_action))
for i in range(no_users):
    print(insert("eventsvideouser", ("usernamer", "videoid", "event"), (event_user[i], event_vid[i], event_action[i]) ) )
print("------------5--------")

## 6)

r_vid = []
r_time = []
r_no = []
r_total = []

for i in range(vid_c):
    r_vid.append( needed_vidId[i] )
    r_time.append( needed_vidTime[i] )
    t_r_total = random.choice([10,20,30,40,50])
    t_r_no = int(random.choice([10, t_r_total, 10]))

    r_no.append(t_r_no)
    r_total.append(t_r_total)

for i in range(vid_c):
    print(update2("videoid", "nofratings", r_no[i], "id", r_vid[i], "time_upload", r_time[i]))
    print(update2("videoid", "totalrating", r_total[i], "id", r_vid[i], "time_upload", r_time[i]))

print("------------6--------")

dict = {}
for a in range(len(vid_author)):
    if vid_author[a] not in dict:
        dict[vid_author[a]] = [needed_vidId[a]]
    else:
        dict[vid_author[a]].append(needed_vidId[a])

for key in dict:
    print(update("users", "videoowned", dict[key], "usernamer", key))

print("------------7--------")

for key in dict_tags:
    print(insert("tagsvideo", ("tag", "videoid"), (key, dict_tags[key])))

print("-----------10--------")


