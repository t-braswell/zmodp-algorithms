##################################
# Various algorithms, utilities,
# and other stuff from Abstract Algebra.
#
# DEPENDENCIES: NUMPY as numpy
##################################
import numpy

def gcd(a,b):
    """
    Euclidean algorithm over signed integers, handled recursively
    INPUT: integers a, b
    OUTPUT: positive integer gcd(a,b) representing the greatest common divisor
    """
    if a==0:
        return abs(b)
    if b==0:
        return abs(a)
    if max( abs(a), abs(b)) % min(abs(a),abs(b)) == 0:
        return min (abs(a) , abs(b))
    return gcd( min(abs(a),abs(b)) , max( abs(a), abs(b)) % min(abs(a),abs(b)))


def gcd_pos(a,b):
    """
    Euclidean algorithm over strictly positive integers, handled recursively
    INPUT: positive integers a, b
    OUTPUT: positive integer gcd(a,b) representing the greatest common divisor
    """
    if max(a,b) % min(a,b) == 0:
        return min(a,b)
    return gcd(min(a,b) , max(a,b) % min(a,b))



def bezout(a,b):
    """
    Calculates the bezout coefficients for 2 numbers using linear algebra. 
    the mechanics of finding bezout coefficients can be thought of as Q1*Q2*...Q{N-1}*[1 -q_n]'
    wherere Qk=[[0,1] [1 -q_n]]. This way, we can quickly keep track of Q1*...*Q{N-1} instead of working backwards
    DEPENDANCIES: numpy
    INPUTS: a, b positive integers. a is assumed larger, switched if not
             NOTE: will sometimes work for negative integers,but seems to be occaisonally sum to -gcd.
    OUTPUTS: u, v integers. a*u+b*v=gcd(a,b).
    """
    if b>a:
        b,a = a,b
    q_mat = numpy.array([[1, 0], [0,1]])
    if (a<0) and (b<0):
        q_mat*=-1
    uv=numpy.array([[0],[1]]) 
    while a%b!=0:
        q = a//b
        r = a % b
        q_mat=numpy.dot(q_mat, numpy.array([[0,1],[1,-q]]))
        a = b
        b = r
    uv=numpy.dot(q_mat,uv)
    return uv



######################################
"""The following is a much more naive implementation of the bezout algorithm stuff.
given the recursive nature of the GCD function, and the dynamic nature of the algorithm, it will be slower. However, the linear algebra trick used in the above isnt obvious, and this will take note of every value generated.
"""
def gcd_bezout(a,b,abqr_list=list()):
    """
    Euclidean algorithm over strictly positive integers, handled recursively.
    In addition, a list of arguments will be passed and appended to keep of a=bq+r quadruplets.
    This is a dynamic algorithm, so we need to keep track
    INPUTS: positive integers a, b, as well as a list of previous quadruplets (default: empty list).
            for the sake of readability, we will assume that a>b, and swap variables if untrue
    OUTPUT: abqr_list, generated recursively. the GCD will be the last number in the last sublist.
    """
    if a==0: return  abqr_list
    if b==0: return  abqr_list
    if b>a:
        b,a=a,b    
    if a%b == 0:
        return abqr_list
    return gcd_bezout(b, a%b, abqr_list+[[a,b, a//b, a%b ]])

def bezout_calc(a,b):
    """
    takes an abqr_list as generated by gcd_bezout(a,b) and backtraces to find the Bezout coefficients
    INPUTS: a, b positive integers. a is assumed larger- if they are not, it is switched internally
    OUTPUTS: 2 numbers, u, v. u is the bezout coefficient for the larger number, v for the smaller
    """
    abqr_list=gcd_bezout(a,b)
    u=1
    v=-1*abqr_list[len(abqr_list)-1][2] ###Q is in position 2 of each sublist
    for i in range(len(abqr_list)-2, -1, -1): 
        u, v = v, u-v*abqr_list[i][2] 
    return u, v
######################################



def polysolve_zmodn(polyvec,n):
    """
    Brute force calculator for solutions to polynomial p_x=0 mod n.
    INPUTS: polyvec, a vector of polynomial coefficients for polynomial p_x
            eg, [2,3,1] -> p_x = 2*x**2 + 3*x + 1
           n: defines the modulo of the ring, ie, smallest positive integer n such that n = 0 mod n
    OUTPUT: solvec, a vector of solutions to p_x=0 mod n
    """
    solvec = []
    for i in range(0,n):
        p_x = 0
        for j in range(0,len(polyvec)):
            p_x += (polyvec[j] * i**(len(polyvec)-(j+1))) % n
            p_x %= n
        if p_x ==0 :
            solvec.append(i)
    return(solvec)

def linsolve_zmodn(a,b,n):
    """
    solves for x such that a*x = b mod n. uses algorithm as discussed in class
    DEPENDENCIES: numpy, bezout & gcd (from /320/algorithms.py)
    INPUTS: a,b integers 
            n: defines modulo of ring, ie, smallest positive integer n such thatn = 0 mod n
    OUTPUT: x_list: a list of values such that a*x_list[i] = b mod n for all i . If no solutions exist, returns empty string. principal values will always be in x_list[0]
    """
    x_list=[]
    if a>=n:
        a %= n
    if b>=n:
        b %= n
    d=gcd(n,a) 
    if b%d!=0:
        return x_list
    else: numsol = d
    x_list.append( int(bezout(n,a)[1])* b//d % n ) # int(bezout(n,a)[1]) returns the coefficient v in un+va=d. can be substituted if you have a different bezout function.
    i = 1
    while len(x_list) < numsol:
        x_list.append((x_list[0]+i*(n//d)) % n )
        i+=1
    return x_list

