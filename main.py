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
class Number :
    def __init__(self,value,mult=0,equal=None):
        self.value = value #value of the vurrent number
        self.multiplier = mult #multiplier of the number
        self.equivalence = equal #equation it represents
    
    def tranasformEquivalence(self, symbol, multiplier=1):
        """Transform the equivalence equation according to the external symbol and multiplier
        """
        #first replace the value in the list for its real equation
        tempEqui = self.equivalence

        for val in tempEqui:
            #[a,b]
            #b = [c,e]
            #e = [g,f]
            #g = 2(1)
            #f = 1(3)
            #b = [c,[2(1),1(3)]]
            #[a,[c,e]]
            if val.
        pass
    
    def extraction(self):
        #if there is no equivalence equation just return the object
        if not self.equivalence:
            return self
        
        elif self.equivalence:
            for val in self.equivalence:
                val = val.extraction()


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
""" def step2(iterations):
    #extract first values in a simple list for better accesibility 
    values = iterations[0]
    iterations[0] =  """
        


#create the matrix
k = [[33,17,60],[50,28,72],[26,86,41]]
I = [[1,0,0],[0,1,0],[0,0,1]]
b = 89
row_counter = 0


step1(k,I, b, row_counter)