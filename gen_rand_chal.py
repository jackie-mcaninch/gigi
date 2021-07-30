import random

f = open("random_challenge.txt","w")
string = ""
for i in range(256):
    string += str(random.randint(0,1))
f.write(string)
f.close()