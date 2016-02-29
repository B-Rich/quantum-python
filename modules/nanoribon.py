
# coding: utf-8

# In[5]:

from sympy import symbols, pi, I,mpmath,cos, sin
from sympy.matrices import Matrix
from sympy.interactive.printing import init_printing
from sympy.physics.matrices import msigma
from sympy.functions import conjugate
from customOperators import*
import numpy as np
from numpy import linalg as LA
import math as math
from scipy.linalg import eig
#import scipy.sparse as sparse
from scipy.linalg import eigvals


np.set_printoptions(suppress=True)


init_printing()

pi=pi.evalf(40)
A,B,C,D =symbols('A:D')
R_0 =symbols('R_0')
a = symbols('a')
M=symbols('M')
k=symbols('k')
tA= A/(a*2)
tB=B/(a**2)
tD=D/(a**2)


I_2 =  Matrix(2, 2, lambda i,j: int(i==j))


def ctranspose(matrix):
    return matrix.transpose().applyfunc(lambda i:conjugate(i))

class Hamiltonian(object):
    
    def __init__(self,nY):
        self.H_0 = (C-float(4)*tD)*(I_2|kron|I_2) +(M-float(4)*tB)*(I_2|kron|msigma(3)) 
        #I*A/a*((msigma(3)|kron|msigma(1))-(I_2|kron|msigma(2)))
        #I*R_0/a*(TensorProduct(msigma(2),(msigma(3)+I_2)/2)-TensorProduct(msigma(1),(msigma(3)+I_2)/2))
        
        self.V_0=  +(tD)*(I_2|kron|I_2)+(tB)*(I_2|kron|msigma(3))-        I*tA*(I_2|kron|msigma(2))
        #I*R_0/a*TensorProduct(msigma(1),(msigma(3)+I_2)/2)
        
        self.W_0d =  +(tD)*(I_2|kron|I_2)+(tB)*(I_2|kron|msigma(3))
        self.W_0off = -I*tA*(msigma(3)|kron|msigma(1))
        #I*A/(2*a)*(msigma(3)|kron|msigma(1))
        #I*R_0/a*TensorProduct(msigma(2),(msigma(3)+I_2)/2) 
        
        self.IdDown = Matrix(nY,nY , lambda i,j :int(i-j==1))
        self.IdUp = Matrix(nY,nY , lambda i,j :int(i-j==-1))
        self.Id= Matrix(nY,nY , lambda i,j :int(i==j))
    

    def hamiltonianNumeric(self, valA,valB,valC,valD,valR_0,vala,valM,valk):
        matrix= self.expandHilbertSpace().evalf(subs={A:valA,B:valB,C:valC,D:valD,R_0:valR_0,a:vala,M:valM,k:valk})
        return  np.array(matrix.tolist()).astype(np.float64)
    
    def V(self, valA,valB,valC,valD,valR_0,vala,valM):
        matrix =  (self.Id|kron|self.H_0) +               (self.IdUp|kron|self.V_0)+(self.IdDown|kron|ctranspose(self.V_0))
        numeric = matrix.evalf(subs={A:valA,B:valB,C:valC,D:valD,R_0:valR_0,a:vala,M:valM})
        return {
            'numeric':np.array(numeric.tolist(),dtype=float),
            'object':matrix
        }
    
    def Wcos(self, valA,valB,valC,valD,valR_0,vala,valM):
        matrix=  2*((self.Id|kron|self.W_0d))
        numeric = matrix.evalf(subs={A:valA,B:valB,C:valC,D:valD,R_0:valR_0,a:vala,M:valM})
        return {
            'numeric':np.array(numeric.tolist(),dtype=float),
            'object':matrix
        }    
    
    def Wsin(self, valA,valB,valC,valD,valR_0,vala,valM):
        matrix=  2*I*(self.Id|kron|self.W_0off)
        numeric = matrix.evalf(subs={A:valA,B:valB,C:valC,D:valD,R_0:valR_0,a:vala,M:valM})
        return {
            'numeric':np.array(numeric.tolist(),dtype=float),
            'object':matrix
        }
    
    def eigenvals(self,k,matrixV,matrixWcos,matrixWsin):

        k=k*pi
        seno= math.sin(k)
        cosseno= math.cos(k)
        w= eigvals(np.array(matrixV+matrixWcos*cosseno+matrixWsin*seno))
        w=np.asarray(w,np.float64)
        idx = w.argsort()[::-1]   
        w = w[idx]
        return w






# In[ ]:



