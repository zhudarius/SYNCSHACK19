# Library is from SAGEMATH, but has been modified to be compatible with Python 3.
# This library was non-functional in its original state (did not compile with Python 2.7,
#  nor 3)
from logicparser import *

tree, vars_order = parse('INFO1113|INFO1105|INFO1905|INFO1103')
print(tree)