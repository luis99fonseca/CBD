f01 = open("female-names.txt", "r")
dict = {}

for line in f01:
    if line[0] not in dict:
        dict[line[0]] = 1
    else:
        dict[line[0]] += 1

print(dict)

f02 = open("initials4redis.txt", "w")
for key in dict:
    f02.write(" set " + str(key) + " " + str(dict[key]) + "\n" )

f02.close()