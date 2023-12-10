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
    p =kn[r_counter][r_counter]
    return p

def getQ(b,p):
    try:
        q = int(b/p)
    except ZeroDivisionError:
        print("[-] Processs can't be completed attempted to divide by 0")
        exit()
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
            #avoid the cycle if it's the last two elements
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

def P3_second_process(array,counter,main_row,B,original= None):
    length = len(array)
    for i in range(length):
        if i != counter:
            #Distinguish between K array and I array for r
            #Since for I r is the same as K but for K r is dynamic
            if original:
                r = (original[i][counter])*-1
            else:
                r = (array[i][counter])*-1

            for j in range(length):
                #R2 = R1*-R2[r_counter]+R2
                array[i][j] = ((main_row[j] * r) + array[i][j]) % B
    return array

def showResults(arrays):
    print("K:\t\tI:")
    for i in range(len(arrays[0][0])):
        print(f"{arrays[0][i]}\t\t{arrays[1][i]}")
    print("\n--------------------------------\n")

def initial_Scan(K,I, check=False):
    """This method is supposed to scan the matrix and see if the pivot 
    is 0, if it is 0 then,
    if there is a row below, then it will switch the values of the current row 
    with the row below it

    If there is no row below, return an error saying that the process can't be completed due to the nature 
    of the matrix it self.

    Inputs: 

    K (List): original K matrix
    I (List): Image matrix of K
    check(boolean) just return if it is possible to switchor not

    Process:
    1.-Verify if the pivot is at the last row, if so activate a flag
    2.-Look for the corresponding pivot values based on a counter 
    (eg. if the counter == 3 then look in row three for the value in the third column)
    3-a.-if the value is 0 and != flag then switch values with next row (for both K and I matrices)
    3-b.- if the value is 0 and flag = True then return False
    """
    counter = 0
    length = len(K)
    for i in range(len(K)):
        if i == length-1: #check if it is last row
            flag = True
        else:
            flag = False
        
        for j in range(len(K)):#check if pivot is not equal to 0 in each row
            value = K[i][j]
            if value == 0 and counter == j:# if so return False
                if flag:
                    return False
                
                if not check:
                    K,I = switch(K,I,counter)# else switch
                    print(f"[+]Switched: {value} with counter: {counter}")
        counter+=1
    
    if check:
        return True
    
    return (K,I)
    
def switch(K,I,counter):
    """Switch the values of two rows for two different arrays"""
    #Save the rows into variable for easier access
    arrays = [[K [counter], K [counter+1]],[I [counter], I [counter+1]]]
    
    for group in arrays:
        #a = [K[counter], k[counter+1]]

        for i in range(len(group[0])): # switch process
            temp = group[0][i]
            group[0][i] = group[1][i]
            group[1][i] = temp
    
    #save values back into the original arrays
    K[counter], K[counter + 1] = arrays[0]
    I[counter], I[counter + 1] = arrays[1]

    return K,I
