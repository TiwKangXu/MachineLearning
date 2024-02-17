from minesweeper import *


# sentence1 = Sentence({1, 2, 3, 4, 5, 6, 7, 8}, 3)
# sentence2 = Sentence({9, 10, 11, 12, 13, 14}, 2)
# knowledge = [sentence1, sentence2]

# mines = [2, 3, 6, 9]
# for x in mines:
#     sentence1.mark_mine(x)
# print(sentence1)

# sentence2 = sentence2.mark_mine(y for y in mines)
# print(sentence2)





setA = Sentence({1, 2}, 0)
setB = Sentence({3}, 1)
setC = Sentence({4, 5, 6, 7, 8}, 3)
setD = Sentence({9, }, 1)
setE = Sentence({10, 11, 12}, 3)
setF = Sentence({13}, 1)

list2 = [setA, setB, setC, setD, setE, setF]
record = []

for a in list2:
    print(a)

for s in list2:
    for t in list2:
        if s == t:
            continue
        record = record + [s, ]
print("-----------------------------------------")

for a in list2:
    print(a)

print("-----------------------------------------")

for rec in record:
    print(rec)

for rec in record:
    list2.remove(rec)
    print("removed", rec)
