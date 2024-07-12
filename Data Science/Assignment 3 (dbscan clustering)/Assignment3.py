import sys

sys.setrecursionlimit(30000)


class ouais:
    id = 0
    x = 0.1
    y = 0.1
    fait = False
    voisin = []

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.voisin = []

    def noyau(self):
        return len(self.voisin) >= MinPts - 1


def paloin(p, q):
    if ((p.x - q.x) * (p.x - q.x) + (p.y - q.y) * (p.y - q.y)) <= Eps * Eps:
        return True
    return False


def densitegrp(centre, grp):
    for acote in centre.voisin:
        if acote.fait == False:
            acote.fait = True
            grp.append(acote)

            if acote.noyau():
                densitegrp(acote, grp)


input_name = sys.argv[1]
n = int(sys.argv[2])
Eps = float(sys.argv[3])
MinPts = int(sys.argv[4])

tout = []

f = open(input_name, 'r')

while True:

    ligne = f.readline()
    if not ligne:
        break

    id, x, y = ligne.split()
    id = int(id)
    x = float(x)
    y = float(y)

    tout.append(ouais(id, x, y))

f.close()

for p in tout:
    for q in tout:
        if p == q:
            continue

        if paloin(p, q):
            p.voisin.append(q)

groupes = []

for p in tout:
    if p.fait == False and p.noyau():
        nvgrp = []
        p.fait = True

        densitegrp(p, nvgrp)
        groupes.append(nvgrp)

if len(groupes) > n:
    groupes.sort(key=lambda c: len(c), reverse=True)

    while len(groupes) > n:
        groupes.pop()

for i in range(n):
    output_name = 'input' + input_name[5] + '_cluster_' + str(i) + '.txt'

    f = open(output_name, 'w')

    for o in groupes[i]:
        f.write(str(o.id) + '\n')

    f.close()
