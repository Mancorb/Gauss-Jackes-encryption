import numpy as np
"""
Steps:
Create a 3x3 matrix for initial tests
K matrix = ([33,17,60],[50,28,72],[26,86,41])
Total number of characters available for the encryption(e,g fi ussing ascii m = 256, if the numebr of charqacters is a list of 89 elements (like in this example) then m = 89)
M = 89
Pivot, aka numebr to analize in the matrix (in this case it's the first numebr of the matrix K = 33)
P = 33

FORMULAS:

b = M
p = P
r = b-q
q = result (int) of b/p
b = p * q + r

"""

def getP(kn,I,r_counter):
    for  i in range(len(kn)):
        if I[r_counter][i] == 1:
            p = kn[r_counter][i]
            break
    return p

def getQ(b,p):
    q = int(b/p)
    return q

def getR(b,q,p):
    r = b - (p*q)
    return r

def getFirstEquation (kn,I,b,r_counter):
    #Find the corresponding pivot based on I matrix
    p = getP(kn,I,r_counter)
    q = getQ(b,p)
    r = getR(b,q,p)

    return p,q,r,b

def getEquation(data):
    #input = (p,q,r)
    #p= r x (new r) + (new q)
    #b = p
    b = data[0]
    p = data[-2]
    q = getQ(b,p)
    r = getR(b,q,p)
    return p,q,r,b

def step1(kn,I, b, r_counter):
    #b = p x q + r
    #Make each operation e.g: 89=33(2)+23 -> 33=23(1) + 10
    #obtains p,q,r
    iterations = [getFirstEquation(kn,I,b,r_counter)]
    counter = 0

    while iterations[-1][0]!=1:
        iterations.append(getEquation(iterations[-1]))
        counter += 1

    return iterations
    
""" def step2(iterations):
    for it in iterations:
        if it[] """


#create the matrix
k = [[33,17,60],[50,28,72],[26,86,41]]
I = [[1,0,0],[0,1,0],[0,0,1]]
b = 89
row_counter = 0


step1(k,I, b, row_counter)