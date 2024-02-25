from collections import deque


class Node():
    def __init__(self, name):
        self.name = name

a = Node("a")
b = Node("b")
c = Node("c")
d = Node("d")

D = {
    a: 1,
    b: 2,
    c: 1,
    d: 2, 
}

E = {
    "a": 1,
    "b": 2,
    "c": 1,
    "d": 2, 

}

dic = {
    "abbbbbb", "bbbbb", "xxbxxxxx"
}

l = [1, 2, 3, 4, 5, 6]

lis = list([1, 2, 3, ])

# E = filter(lambda item: item[1] != 2, E.items())

# E = dict(sorted(E.items(), key=lambda k: k[1]))
# print(E)

D = list(D.items())
print(D)