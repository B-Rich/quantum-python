
# coding: utf-8

# In[1]:

from functools import partial
from sympy.physics.quantum import TensorProduct

class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)
    
@Infix
def kron(x,y):
    return TensorProduct(x,y)


# In[ ]:



