from methods import *
from copy import deepcopy
from time import perf_counter
import numpy as np

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
    """Retuns the multiplier to affect he original matrix

    Args:
        iterations (list): list of all the inicial equations before processing
        k (list): original matrix
        I (list): matrix with only 1s and 0s
        r_counter (int): counter to see in which row the process is tacking place

    Returns:
        int: multiplier to use in step 3
    """
    #part one
    #obtain the first equation
    p,q,r,b = iterations[0]
    #dictionary to store the equivalence of a value 
    b = Number(b)
    p = Number(p*-1,q)
    #r=b+(p(q))*-1
    equivalence = {r:[b,p]}#dictionary of equations to store

    if len(iterations) <3:
        e,r = EquationIteration(iterations[-1],equivalence)

    elif len(iterations) > 1:
    
        equations = deepcopy(iterations [1:-1])
        #-----------------------------------
        #Part two
        for iteration in equations:
            e,r = EquationIteration(iteration,equivalence)
            
            #Store new equation to the dictionary
            equivalence[r] = dissolve(e)
    
        #----------------------------------
        #part three last equation (just replicate part two but without adding to the dictionary and look for X based on the pivot)
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


def start(K=None,I=None,b=None,show=False):
    #create the matrix
    if not K:
        K = [[39, 76, 91, 99, 11, 77, 13, 73]                
            ,[46, 90, 0, 73, 13, 86, 89, 59]         
            ,[77, 45, 98, 98, 89, 64, 27, 75]                
            ,[47, 39, 66, 79, 23, 40, 49, 55]                
            ,[23, 93, 49, 98, 42, 99, 37, 98]                
            ,[86, 79, 59, 93, 12, 0, 52, 61]         
            ,[92, 11, 88, 79, 31, 31, 55, 17]                
            ,[30, 83, 40, 79, 39, 14, 35, 77]]
    if not I:
        I = [[1, 0, 0, 0, 0, 0, 0, 0]
            ,[0, 1, 0, 0, 0, 0, 0, 0]
            ,[0, 0, 1, 0, 0, 0, 0, 0]
            ,[0, 0, 0, 1, 0, 0, 0, 0]
            ,[0, 0, 0, 0, 1, 0, 0, 0]
            ,[0, 0, 0, 0, 0, 1, 0, 0]
            ,[0, 0, 0, 0, 0, 0, 1, 0]
            ,[0, 0, 0, 0, 0, 0, 0, 1]]
    if not b:
        b = 89

    if show:
        showResults((K,I))

    for row_counter in range(len(K)):
        #check pivot value
        if not initial_Scan(K,I,check=True):
            print("[-]Error the this process can't be completed due to the nature of the matrix")
            break
        
        K,I =initial_Scan(K,I)

        it = step1(K,I, b, row_counter) #Iterations
        X = step2(it,K,I,row_counter) # X factor to convert in step 3
        K,I = step3(K,I,X,b,row_counter) # Replace old matrix with new values

    if show:
        showResults((K,I))

def make_I(length):
    I = []
    counter = 0
    for i in range(length):
        temp = []
        for j in range(length):
            if j == counter:
                temp.append(1)
            else:
                temp.append(0)
        I.append(temp)
        counter +=1
    return I

if __name__ == "__main__":
    """ n = 4 #maximum funccionality with only 7 so far
    K = np.random.randint(low=0, high=100, size=(n, n)).tolist()
    I = make_I(n) """

    Original_Matrix = [[33,17,60],
                        [50,28,72],
                        [26,86,41]]
    
    #(only two equations at row 4)
    Tester_Matrix= [[74, 81, 63, 37, 4, 21, 0, 95]    
                    ,[89, 92, 0, 39, 68, 44, 26, 74]   
                    ,[56, 62, 30, 62, 56, 1, 37, 85]   
                    ,[71, 57, 37, 93, 38, 62, 23, 11]          
                    ,[82, 41, 21, 58, 22, 29, 23, 47]          
                    ,[35, 89, 11, 6, 33, 68, 48, 8]    
                    ,[62, 26, 83, 84, 61, 18, 57, 44]          
                    ,[7, 76, 71, 23, 9, 84, 48, 68]]

    K = Original_Matrix
    I = make_I(len(K))
    start(K,I,b=89,show=True)


""" 
Original_Matrix = [33,17,60],
                    [50,28,72],
                    [26,86,41]

[1,0,0],[0,1,0],[0,0,1]

Tester Matrix: (only two equations at one point)
[39, 76, 91, 99, 11, 77, 13, 73]                
[46, 90, 0, 73, 13, 86, 89, 59]         
[77, 45, 98, 98, 89, 64, 27, 75]                
[47, 39, 66, 79, 23, 40, 49, 55]                
[23, 93, 49, 98, 42, 99, 37, 98]                
[86, 79, 59, 93, 12, 0, 52, 61]         
[92, 11, 88, 79, 31, 31, 55, 17]                
[30, 83, 40, 79, 39, 14, 35, 77]   

[1, 0, 0, 0, 0, 0, 0, 0]
[0, 1, 0, 0, 0, 0, 0, 0]
[0, 0, 1, 0, 0, 0, 0, 0]
[0, 0, 0, 1, 0, 0, 0, 0]
[0, 0, 0, 0, 1, 0, 0, 0]
[0, 0, 0, 0, 0, 1, 0, 0]
[0, 0, 0, 0, 0, 0, 1, 0]
[0, 0, 0, 0, 0, 0, 0, 1]

Tester Matrix: (at some point it divides 0 to obtain q)
[74, 81, 63, 37, 4, 21, 0, 95]    
[89, 92, 0, 39, 68, 44, 26, 74]   
[56, 62, 30, 62, 56, 1, 37, 85]   
[71, 57, 37, 93, 38, 62, 23, 11]          
[82, 41, 21, 58, 22, 29, 23, 47]          
[35, 89, 11, 6, 33, 68, 48, 8]    
[62, 26, 83, 84, 61, 18, 57, 44]          
[7, 76, 71, 23, 9, 84, 48, 68]
"""