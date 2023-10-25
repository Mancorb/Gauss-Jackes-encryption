import numpy as np
from copy import deepcopy

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

def EquationIteration(iteration,equivalence):
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
    for i in range(len(p)):
        e.append(p[i])
    
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
    #prove the equation is correct
    if not proveR(r,e):
        txt =""
        for i in e:
            txt += f"({i.value}*{i.multiplier}) + "
        print(f"Error with ecuation:\n{r}!={txt}")

        return False

    return e,r

def P3_first_process(array,counter,b,x):
    main_row = array[counter]
    for i in range(len(main_row)):
        col = main_row[i]
        main_row[i] = (col * x)% b

    return main_row 
