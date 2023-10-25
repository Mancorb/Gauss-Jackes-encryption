from methods import *
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
def step2(iterations,k,I,r_counter):
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
        e,r = EquationIteration(iteration,equivalence)
        
        #Store new equation to the dictionary
        equivalence[r] = dissolve(e)

    #----------------------------------
    #part three last equation (just replicate part twoo but without adding to the dictionary and look for X based on the pivot)
    e,r = EquationIteration(equations[-1],equivalence)

    #find row pivot and return the multiplier
    for i in e:
        if i.value == k[r_counter][r_counter]:
            if I[r_counter][r_counter]:
                return i.multiplier     


def step3(K,I,X,B,r_counter):
    #Use the x[r_counter] as reference for multiplications but tot eh process first on x[r_counter]
    #R1 = r1 * X  % B
    #R2 = R1*-R2[r_counter]+R2
    #R3 = R1*-R3[r_counter]+R3

    #FIRST
    #Change I
    I_main_row =I[r_counter] = P3_first_process(I,r_counter,B,X)
    
    #Change K
    K_main_row = K[r_counter] = P3_first_process(K,r_counter,B,X)

    #go for each row
    temp = deepcopy(K)

    K = P3_second_process(K,r_counter,K_main_row,B)    
    #Change I
    I = P3_second_process(I,r_counter,I_main_row,B,temp)

    return K,I

#create the matrix
K = [[33,17,60],[50,28,72],[26,86,41]]
I = [[1,0,0],[0,1,0],[0,0,1]]
b = 89

for row_counter in range(len(K)):
    #row_counter = 0
    it = step1(K,I, b, row_counter)
    X = step2(it,K,I,row_counter)
    K,I = step3(K,I,X,b,row_counter)

showResults((K,I))