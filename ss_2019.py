import numpy as np
import random

#Arrays and Constants
n = 5
N = 1
players = ['Cormac', 'Conor', 'James', 'Mary', 'Michael']
opponents = ['Cormac', 'Conor', 'James', 'Mary', 'Michael']
n = len(players)

def fun():
    while True:
        #Shuffling
        matchups = []
        random.shuffle(opponents)                                               #Shuffles our opponents
        for i in range(n):
            if opponents[i] == players[i]:
                opponents[i], opponents[i-1] = opponents[i-1], opponents[i]     #If anybodyplays themselves, the 

        #List Formating
        for i in range(n):
            a = players[i]
            b = opponents[i]
            c = opponents.index(b)
            if c == a:
                break
            matchups.append([a,b])
        if len(matchups) == n:
            return matchups


matchups = fun()

for i in range(len(players)):
    f = open(players[i] + '.txt', 'w')
    f.write(('You buy for ' + opponents[i]))
    f.close()
