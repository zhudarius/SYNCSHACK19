# Library is from SAGEMATH, but has been modified to be compatible with Python 3.
# This library was non-functional in its original state (did not compile with Python 2.7,
#  nor 3)
from logicparser import *
def generateParseTree(expression):
    
    tree, vars_order = parse(expression)
    print(tree)
    return tree

generateParseTree('(COMP2123|COMP2823)&COMP2017&(COMP2022|COMP2922)')