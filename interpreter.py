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
    convert(parserTree)
    print(checkFormat(parserTree))

def convert(tree):
    for i in range(len(tree)):
        if type(tree[i]) is list:
            convert(tree[i])
        else:
            tmp_tree = pattern_match(tree[i], model_patterns)
            tree[i] = {}
            tree[i][tmp_tree[0]] = tmp_tree[1]
    return tree

def convertBack( tree ):
    for i in range(len(tree)):
        if type(tree[i]) is list:
            convertBack(tree[i])
        else:
            tmp = tree[i][list(tree[i])[0]]
            tree[i] = tmp
    return '( '+ toStr( tree ) +')'

def toStr(parserT):
    returnStr = ''
    for i in parserT:
        if type(i) is list:
            returnStr = returnStr + "( " + toStr(i) + ") "
        else:
            returnStr = returnStr + i + " " 
    return returnStr

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

'''
    predefined functions

'''
def plus(tree):
    value = 0
    for i in range(1,len(tree)):
        if type(tree[i]) is list:
            value = value + checkFormat(tree[i])
        elif list(tree[i])[0] == 'INTEGER':
            value = value + int(tree[i][list(tree[i])[0]])
        elif list(tree[i])[0] == 'REAL':
            value = value + float(tree[i][list(tree[i])[0]])
        else:
            return "ERROR_PLUS: Only integer or real type argument is accept"
    return value

def lessthan(tree):
    if len(tree) == 3:
            if type(tree[1]) is list:
                num1 = checkFormat(tree[1])
            elif list(tree[1])[0] == 'INTEGER' or list(tree[1])[0] == 'REAL':
                num1 = float(tree[1][list(tree[1])[0]])
            else:
                return "ERROR_LESSTHAN: Wrong argument %s, only accpet integer or real"%(tree[1][list(tree[1])[0]])

            if type(tree[2]) is list:
                num2 = checkFormat(tree[2])
            elif list(tree[2])[0] == 'INTEGER' or list(tree[2])[0] == 'REAL':
                num2 = float(tree[2][list(tree[2])[0]])
            else:
                return "ERROR_LESSTHAN: Wrong argument %s, only accpet integer or real"%(tree[2][list(tree[2])[0]])

            if (type(num1) is float or type(num1) is int) and (type(num2) is float or type(num2) is int):
                if num1 < num2:
                    return '#t'
                else:
                    return '#f'
            else:
                return "ERROR_LESSTHAN: only accept integer or real"
            
    else:
        return "ERROR: there must be exactly two arguments!"

def isnull(tree):
    if len(tree) == 3 and tree[1][list(tree[1])[0]] == '\'' and type(tree[2]) is list:
        if len(tree[2]) == 0:
            return '#t'
        else:
            return '#f'
    else:
        return "ERROR_ISNULL: Need be exactly one list argument"

def car(tree):
    if len(tree) == 3 and tree[1][list(tree[1])[0]] == '\'' and type(tree[2]) is list:
        if len(tree[2]) > 0:
            if type(tree[2][0]) is list:
                return tree[2][0]
            else:
                return tree[2][0][list(tree[2][0])[0]]
        else:
            return "ERROR_CAR: Don't accept empty list argument"
    else:
        return "ERROR_CAR: Need be exactly one list argument"    

def cdr(tree):
    if len(tree) == 3 and tree[1][list(tree[1])[0]] == '\'' and type(tree[2]) is list:
        if len(tree[2]) > 0:
            tree[2].pop(0)
            return convertBack(tree[2])
        else:
            return "ERROR_CDR: Don't accept empty list argument"
    else:
        return "ERROR_CDR: Need be exactly one list argument"    

if __name__ == '__main__':
    #parserTree = ['plus', 'asd', ['plus', '4', '3'],'4','5']
    parserTree = ['cdr','\'',['1',['plus','4','3'],'3']]
    interpreter(parserTree)
