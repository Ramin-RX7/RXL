

# Functools
'''
from functools import reduce, partial, singledispatch

# Make function for different argument type inputs
@singledispatch
def fun(s): 
    print(str(s))
@fun.register(str)
def fun_str(s): 
    print('its str:  '  +  s * 2) 
fun('Hello') 
fun(10) 
fun(False)

# Change argumnets of a function and return the new one
def power(a, b):
    return a**b
pow2 = partial(power, b = 2)
pow4 = partial(power, b = 4)
power_of_5 = partial(power, 5)

'''


# My Type (OLD)
'''
text = '<al<i>>'
a,b = [],[]
splt= text.split('>')
splt= splt[:-1]
print(splt)
for i in splt:
    if i !='':
        if i[0] != '<': #to list b then a
            b.append(i[:i.index('<')])
            a.append(i[i.index('<')+1:])
        else: #to list a
            a.append(i[1:])

print(a)
print(b)
'''
r'''import re
mytring = '<he<llo>>xa'
wordsInside = re.findall(r"<(\w+)", mytring)
wordsOutside = re.findall(r">(\w+)", mytring)
print(wordsInside)
print(wordsOutside)'''


'''
myobj = type('MyType', (object,), dict(a=1, b=2, c=3))()
print(myobj)
print(type(myobj))
print(myobj.a)
print('\n')

class Collection:
    def __init__(self,*args):
        self.args = args
        
    def __str__(self):
        return f'Collection{self.args}'

x = Collection(10,30,40)
print(x)
print(type(x))
'''
