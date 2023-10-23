import numpy as np
from copy import deepcopy
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
class Number :
    def __init__(self,value,mult=1):
        self.value = value #value of the vurrent number
        self.multiplier = mult #multiplier of the number

        self.filterNegative()

    def filterNegative(self):
        if self.value<1:
            self.value = self.value*-1
            self.multiplier = self.multiplier*-1

def dissolve(e):
    """Extract a nested listwithin the main list of elements

    Args:
        e (list): original list of elements to dissolve

    Returns:
        list: list of elements with no nested lists
    """
    result = []
    for i in e:
        if isinstance(i, list):
            for j in i:
                result.append(i)
        else:
            result.append(i)
    
    return result

def proveR(r,e):
    res=0
    for i in e:
        res += i.value * i.multiplier
    if r==res:
        return True
    return False

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

def joinMultiplier(first,second,show=False):
    if first.value==second.value:
        #add multipliers
        first.multiplier = first.multiplier + second.multiplier
        if show:
            print("Equation= "+str(first.multiplier)+" + "+str(second.multiplier))
            print(first.multiplier+second.multiplier)
    return first


def step1(kn,I, b, r_counter):
    """Obtain all the equations from the matrix

    Args:
        kn (list): list of the matrix's values
        I (list): matrix with only ones and zeros where the inverse will be
        b (int): maximum number of values to use in encryption
        r_counter (int): row counter to skip to the rwo where this process takes place

    Returns:
        list: list of equation values
    """
    #b = p x q + r
    #Make each operation e.g: 89=33(2)+23 -> 33=23(1) + 10
    #obtains p,q,r
    
    iterations = [getFirstEquation(kn,I,b,r_counter)]
    counter = 0

    while iterations[-1][0]!=1:
        iterations.append(getEquation(iterations[-1]))
        counter += 1

    #returns p,q,r,b
    return iterations


#[p=33, q=2, r=23, b=89]
def step2(iterations):
    #part one
    #obtain the first equation
    p,q,r,b = iterations[0]
    #dictionary to store the equivalence of a value 
    b = Number(b)
    p = Number(p*-1,q)
    #r=b+(p(q))*-1
    equivalence = {r:[b,p]}

    equations = iterations [1:-1]
    #-----------------------------------
    #Part two
    for iteration in equations:
        p,q,r,b = iteration
        #look for equivalente equations
        if b in equivalence:
            b = deepcopy(equivalence[b])
        else:
            b = Number(b)

        if p in equivalence:
            p = deepcopy(equivalence[p])
            for element in p:
                element.multiplier = (element.multiplier * q)*-1
        
        else:
            p = Number(p*-1,q)

        #make new equation of R=B+(P*Q)*-1
        #make sure b is not a list inside e
        if isinstance(b, list):
            e = dissolve(b)
        else:
            e = [b]

        #Add elements of p to the e list
        for i in p:
            e.append(i)
        
        #join similar numbers with thier multipliers
        #eg: 33+ 83(1)+33(2) => 33(3) + 83(1)
        length = len(e)-1

        for i in range(length-1):
            #look for elements in reverse order to avoid out of bounds error
            if i == len(e)-1:
                break
            elif e[i] == e[-2]:
                #avoid the cycle if its the last two elements
                a = e[-1]
                if e[i].value==a.value:
                    e[i] =joinMultiplier(e[i],a)                    
                    e.pop(-1)
                break

            for j in range(len(e)-1):
                a = e[length-j]

                if e[i].value==a.value:
                    e[i] = joinMultiplier(e[i],a)
                    e.pop(length-j)
                    
        
        #prove the equation is correct
        if not proveR(r,e):
            txt =""
            for i in e:
                txt += f"({i.value}*{i.multiplier}) + "
            print(f"Error with ecuation:\n{r}!={txt}")

            return False
        #Store new equation to the dictionary
        equivalence[r] = dissolve(e)

    #----------------------------------
    #part three last equation (just replicate part twoo but without adding to the dictionary and look for X based on the pivot)
    
def step3(K,I,X,B,r_counter):
    #Use the x[r_counter] as reference for multiplications but tot eh process first on x[r_counter]
    #R1 = r1 * X  % B
    #R2 = R1*-R2[r_counter]+R2
    #R3 = R1*-R3[r_counter]+R3
    
    #FIRST
    #Change X
    main_row = X[r_counter]
    for i in range(main_row):
        col = main_row[i]
        main_row[i] = (col * X)% B
        
    X[r_counter] = main_row
    #go for each row
    length = len(X)
    for i in range(length):
        if i != r_counter:
            for j in range(length):
                #R2 = R1*-R2[r_counter]+R2
                r = X[i][r_counter]
                X[i][j] = main_row[j]*(r*-1) + X[i][j]
    
    #Change I
    
#create the matrix
k = [[33,17,60],[50,28,72],[26,86,41]]
I = [[1,0,0],[0,1,0],[0,0,1]]
b = 89
row_counter = 0

it = step1(k,I, b, row_counter)
X = step2(it)