#!/usr/bin/env python3
import re
import sys

from paser import parser
from scanner import scanner,pattern_match

model_patterns = {
     'SYMBOL':'([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*',
     'INTEGER':'(\+|\-)?([0-9])+', 
     'REAL':'(\+|\-)?([0-9])*\.([0-9])+',
     'PUNCTUATION':'\(|\)|\'',
     'BOOLEAN':'(\#t|\#f)' 
    }

preDefFunc = ['plus','lessthan','isnull','car','cdr','define', 'if']

def interpreter( parserTree ):
    print(convert(parserTree))
    print(checkFormat(parserTree))

def plus(tree):
    if len(tree) == 3:
        value = 0
        print(tree)
        for i in range(1,3):
            print(tree[i])
            if type(tree[i]) is list:
                print(1)
                value = value + checkFormat(tree[i])

            elif list(tree[i])[0] == 'INTEGER':
                print(2)
                value = value + int(tree[i][list(tree[i])[0]])

            else:
                return "plus:unknow error"

        return value

    else:
        return "Error: need provide valid number of arguments"

def convert(tree):
    for i in range(len(tree)):
        if type(tree[i]) is list:
            convert(tree[i])
        else:
            tmp_tree = pattern_match(tree[i], model_patterns)
            tree[i] = {}
            tree[i][tmp_tree[0]] = tmp_tree[1]
    return tree
   
def checkFormat(parserTree):
    if type(parserTree[0]) is not list and list(parserTree[0])[0] == 'SYMBOL':
        predefined = False
        for func in preDefFunc:
            if parserTree[0][list(parserTree[0])[0]] == func:
                predefined = True
                funcString = func + '(parserTree)'
                result = eval(funcString)
                return result
        if predefined == False:
            return "The function: %s is not defined"%(parserTree[0][list(parserTree[0])[0]])
    elif type(parserTree[0]) is list:
        checkFormat(parserTree[0])
    else:
        return "Invalid application " + parserTree[0][list(parserTree[0])[0]]

if __name__ == '__main__':
    parserTree = ['plus', '3', ['plus', '4', '3']]
    interpreter(parserTree)
