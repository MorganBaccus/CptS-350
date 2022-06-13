# Morgan Baccus
# CptS 350

from pyeda.inter import *

even_numbers = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
prime_numbers = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
#R is the set of all edges in G


def singleBooleanFormula(number):
    bin_number = '{0:05b}'.format(number)
    symbolic_number = ""
    index = 0
    for i in bin_number:
        if int(i) == 0:
            symbolic_number += f"~x[{index}] & "
        elif int(i) == 1:
            symbolic_number += f"x[{index}] & "
        index +=1
    symbolic_number = symbolic_number[:-3]

    return symbolic_number

# Converts the numbers to binary so we get ~x[0]...x[4]
def edgeToBooleanFormula(i, j):

    index = 0
    xFormula = ""
    yFormula = ""
    xBin = '{0:05b}'.format(i)
    yBin = '{0:05b}'.format(j)

   
    # Produces "x[i] & ".. 
    for digit in xBin:
        
        if int(digit) == 0:
            xFormula += f"~x[{index}] & "
        elif int(digit) == 1:
            xFormula += f"x[{index}] & "
        
        index += 1    

    
    index = 0

    # Iterate over the bits to create the yFormula
    for digit in yBin:
        
        if int(digit) == 0:
            yFormula += f"~y[{index}] & "
        elif int(digit) == 1:
            yFormula += f"y[{index}] & "
        
        index += 1  
    
    # Pop last 3 chars from the expressions
    xFormula = xFormula[:-3]
    yFormula = yFormula[:-3]

    # Create a new Formula with x and y expressions
    formula = f"({xFormula}) & ({yFormula})"

    return formula

def joinEdgeFormulaList(edgeFormulaList):

    jointFormula = ""

    # Add OR between each formula
    for edgeFormula in edgeFormulaList:
        
        jointFormula += f"({edgeFormula}) | "

    # Convert the formula string to an expression
    jointFormula = expr(jointFormula[:-3])

    return jointFormula

# Creates and compose R
def composeR(R):
    x0, x1, x2, x3, x4 = bddvars('x', 5)
    y0, y1, y2, y3, y4 = bddvars('y', 5)
    z0, z1, z2, z3, z4 = bddvars('z', 5)
    
    R1 = R

    r1 = R1.compose({y0:z0, y1:z1, y2:z2, y3:z3, y4:z4 })
    
    r2 = R.compose({x0:z0, x1:z1, x2:z2, x3:z3, x4:z4 }) 
        
    bdd = r1 & r2
    bdd = bdd.smoothing((z0, z1, z2, z3, z4))

    return bdd

def transitive_closure(R):
    
    x0, x1, x2, x3, x4 = bddvars('x', 5)
    y0, y1, y2, y3, y4 = bddvars('y', 5)
    z0, z1, z2, z3, z4 = bddvars('z', 5)
    
    # Transitive closure algorithm
    H = R
    HPrime = None

    while True:

        HPrime = H
        
        # H
        r1 = H.compose({y0:z0, y1:z1, y2:z2, y3:z3, y4:z4 })

        # R
        r2 = R.compose({x0:z0, x1:z1, x2:z2, x3:z3, x4:z4 }) 

        # H x R
        r = r1 & r2

        # H = H v (H x R)
        H = HPrime | r

        # apply smoothing over all z BDD Vars to rid them from the graph
        H = H.smoothing((z0, z1, z2, z3, z4))

        if H.equivalent(HPrime):
            break

    return H
# main program 
if __name__ == '__main__':

    
    edgeFormulaList = []
    prime = []
    even = []
    
    x0, x1, x2, x3, x4 = bddvars('x', 5)
    y0, y1, y2, y3, y4 = bddvars('y', 5)

    print("Building graph G...")
    for i in range(0, 32):

        for j in range(0,32):
            
            if (((i+3) % 32) == (j % 32)) | (((i+7) % 32) == (j % 32)):
                

                # Getting PRIME, EVEN and RR BDDs
                if i in prime_numbers:
                    p = singleBooleanFormula(i)
                    prime.append(p)

                elif i in even_numbers:
                    e = singleBooleanFormula(i)
                    even.append(e)

                if j in prime_numbers:
                    p = singleBooleanFormula(j)
                    prime.append(p)

                elif j in even_numbers:
                    e = singleBooleanFormula(j)
                    even.append(e)

                # Send the edge to formula creation function
                newFormula = edgeToBooleanFormula(i, j)

                # Add the new formula to the list
                edgeFormulaList.append(newFormula)

                
    
    
    # Create a big boolean expression, F, for the entire graph G
    print("Building the boolean expression F...")
    R = joinEdgeFormulaList(edgeFormulaList)

    print("Building the boolean expression E...")
    E = joinEdgeFormulaList(even)

    print("Building the boolean expression P...")
    P = joinEdgeFormulaList(prime)
    
    # Obtain BDDs RR, EVEN, PRIME
    print("Converting R to a BDD called RR...")
    RR = expr2bdd(R)

    print("Converting E to a BDD called EVEN...")
    EVEN = expr2bdd(E)

    print("Converting P to a BDD called PRIME...")
    PRIME = expr2bdd(P)

    # Compute BDD RR2 for the set R * R, from BDD RR
    print("Computing BDD RR2... ")
    RR2 = composeR(RR)

    # Compute the transitive closure RR2star of RR2
    print("Computing transitive closure RR2star... ")
    RR2star = transitive_closure(RR2)

    #Compute the BDD PE, from BDDs P RIME, EV EN, and RR2star
    print("Computing BDD PE... ")
    PE = RR2star.smoothing((x0, x1, x2, x3, x4, y0, y1, y2, y3, y4))&EVEN.smoothing((y0, y1, y2, y3, y4))&PRIME.smoothing((x0, x1, x2, x3, x4))

    result = ~PE

    if(result):
        print("Statement A is true")


    
