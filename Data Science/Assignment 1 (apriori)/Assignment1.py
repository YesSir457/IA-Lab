# Assignement 1 Apriori program
# Yassir JALAL

import sys

input_min_support = int(sys.argv[1])
input_name = sys.argv[2]
output_name = sys.argv[3]
min_support = float(input_min_support)

f = open(input_name, 'r')
DataBase = []

while True:
  line = f.readline()
  if not line:
    break
  transaction = []
  num = ""
  for carac in line:
    if carac.isdigit():
      num += carac
    elif num != "":
      transaction.append(int(num))
      num = ""
  if num != "":
    transaction.append(int(num))
  DataBase.append(transaction)
f.close()

cdc = []
L = []

def generate_combinaisons(cdc, r):
  if r == 0:
    return [[]]
  if len(cdc) == 0:
    return []
  combinaisons = []
  for i in range(len(cdc)):
    element = cdc[i]
    rest = cdc[i + 1:]
    for comb in generate_combinaisons(rest, r - 1):
      combinaisons.append([element] + comb)
  return combinaisons

def FrequentSubset(L, cdc):
  for i in range(len(cdc)):
    if i == 0:
      continue
    subsets = generate_combinaisons(cdc, i)
    for subset in subsets:
      s = list(subset)
      flag = False
      for l in L[len(s) - 1]:
        if set(s).issubset(set(l)):
          flag = True
      if flag is False:
        return False
  return True

C = []
k = 0

def combinaison(C, L, k):
  jsp = []
  count = 0
  for un in range(len(C) - 1):
    count = count + 1
    deux = un + 1
    while True:
      if deux >= len(C):
        break
      uni = set(C[un]) | set(C[deux])
      if len(uni) == k + 1 and FrequentSubset(L, list(uni)):
        jsp.append(list(uni))
      deux = deux + 1
  return jsp

count = []
solo_count = {}
solo = set()
for bat in DataBase:
  for num in bat:
    solo.add(num)
    if num in solo_count:
      solo_count[num] = solo_count[num] + 1
    else:
      solo_count[num] = 1

listsolo = []
deh = list(solo)
index = 0
for t in deh:
  if (solo_count[index] * 100 / len(DataBase)) >= min_support:
    new_list = []
    new_list.append(t)
    listsolo.append(new_list)
  index = index + 1

C.append(listsolo)
L.append(listsolo)

sololistcount = []
for num in listsolo:
  sololistcount.append(solo_count[num[0]])
count.append(sololistcount)

while True:
  if len(C[k]) == 0 or len(L[k]) == 0:
    break
  com = combinaison(C[k], L, k + 1)
  C.append(com)
  deh_count = [0 for i in range(len(com))]
  index = 0
  for itemset in com:
    for tr in DataBase:
      if set(itemset).issubset(set(tr)):
        deh_count[index] = deh_count[index] + 1
    index = index + 1
  count.append(deh_count)
  deh = []
  index = 0
  for support in deh_count:
    if (support * 100 / len(DataBase)) >= min_support:
      deh.append(com[index])
    index = index + 1
  L.append(deh)
  k = k + 1

f = open(output_name, 'w')
for i in range(len(L)):
  jsp = {}
  deh = []
  for j in range(len(L[i])):
    if j in jsp:
      continue
    L[i][j].sort()
    deh.append(L[i][j])
    for k in range(j + 1, len(L[i])):
      if set(L[i][j]) == set(L[i][k]):
        jsp[k] = True
  cdc.append(deh)

#weird but works
for r in range(len(cdc)):
  for c in range(len(cdc[r])):
    for r2 in range(len(cdc)):
      for c2 in range(len(cdc[r2])):
        if set(cdc[r][c]).issubset(set(cdc[r2][c2])) or set(
            cdc[r2][c2]).issubset(set(cdc[r][c])):
          continue
        support_count = 0
        confidence_count = 0
        confidence2 = 0
        unionset = set(cdc[r][c]).union(set(cdc[r2][c2]))
        for tr in DataBase:
          tr_set = set(tr)
          if unionset.issubset(tr_set):
            support_count = support_count + 1
            confidence_count = confidence_count + 1
          if set(cdc[r][c]).issubset(tr_set):
            confidence2 = confidence2 + 1
        if confidence_count == 0 or confidence2 == 0:
          continue
        item_set = '{'
        associative_item_set = '{'
        index = 0
        for item in cdc[r][c]:
          if index < len(cdc[r][c]) - 1:
            item_set += str(item) + ','
          else:
            item_set += str(item)
          index = index + 1
        item_set += '}'
        index = 0
        for item in cdc[r2][c2]:
          if index < len(cdc[r2][c2]) - 1:
            associative_item_set += str(item) + ','
          else:
            associative_item_set += str(item)
          index = index + 1
        associative_item_set += '}'
        support = support_count / len(DataBase) * 100
        confidence = confidence_count / confidence2 * 100
        if support < min_support:
          continue
        f.write(item_set + '\t' + associative_item_set + '\t' + str(f"{support:.2f}") + '\t' + str(f"{confidence:.2f}") + '\n')

f.close()
