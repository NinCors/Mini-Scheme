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

defined = {}

defined_key = []

def interpreter( parserTree ):
    '''
        The main function
    '''
    print("\nThis is parserTree")
    print(parserTree)
    #print("This is convert parserTree")
    if type(parserTree) is not list:
        return checkVariable(parserTree)
    convert(parserTree)
    #print("This is defined ")
    #print(defined)
    #print("This is checkformat")
    result = checkFormat(parserTree)
    #print(result)
    #print("\n")
    return result
    

def convert(tree):
    '''
        Convert the input tree to the format that with type infront of value

    '''
    for i in range(len(tree)):
        if type(tree[i]) is list:
            convert(tree[i])
        else:
            tmp_tree = pattern_match(tree[i], model_patterns)
            tree[i] = {}
            tree[i][tmp_tree[0]] = tmp_tree[1]
    return tree

def convertBack( tree ):
    '''
        Convert back the tree with type format to their original version

    '''
    for i in range(len(tree)):
        if type(tree[i]) is list:
            convertBack(tree[i])
        else:
            tmp = tree[i][list(tree[i])[0]]
            tree[i] = tmp
    return '( '+ toStr( tree ) +')'

def toStr(parserT):
    '''
        Convert the tree structure to string

    '''
    returnStr = ''
    for i in parserT:
        if type(i) is list:
            returnStr = returnStr + "( " + toStr(i) + ") "
        elif type(i) is dict:
            returnStr = returnStr + i[list(i)[0]] + " "
        else:
            returnStr = returnStr + i + " " 
    return returnStr

def checkVariable(parserTree):
    if type(parserTree) is dict:
        var_name = parserTree[list(parserTree)[0]]
    else:
        var_name = parserTree
    if var_name in defined_key:
        return defined[var_name]
    else:
        return var_name

def checkFormat(parserTree):
    '''
        The function to check input tree and decide which predefined function
        should be called

    '''
    if type(parserTree) is not list:
        return checkVariable(parserTree)

    if type(parserTree[0]) is not list and list(parserTree[0])[0] == 'SYMBOL':
        func_name = parserTree[0][list(parserTree[0])[0]]
        if func_name in preDefFunc:
            if func_name == 'if':
                func_name = 'if_f'
            funcString = func_name + '(parserTree)'
            result = eval(funcString)
            return result
        else:
            return "The function: %s is not defined"%(parserTree[0][list(parserTree[0])[0]])
    #################################
    elif type(parserTree[0]) is list:
        checkFormat(parserTree[0])
    else:
        return "Invalid application " + parserTree[0][list(parserTree[0])[0]]


'''
    predefined functions

'''
def plus(tree):

    '''
        The plus function

    '''
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

    '''
        The less than function
    '''
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
                return convertBack(tree[2][0])
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

def define(tree):
    if [list(tree[1])[0]][0] == 'SYMBOL':
        variable = tree[1][list(tree[1])[0]]
        if variable in preDefFunc:
            return "DEFINE_ERROR: Can't define a variable that has same name with predefined function"
        else:
            if len(tree) == 4 and tree[2][list(tree[2])[0]] == '\'' and type(tree[3]) is list:
                value = '\'(' + toStr(tree[3])+')'
            elif len(tree) == 3:
                value = tree[2][list(tree[2])[0]]
            else:
                return "DEFINE_ERROR: Need provide exactly one expression"
            key = tree[1][list(tree[1])[0]]  
            defined_key.append(key)  
            defined[key] = value
            return "%s is defined"%(key)
    else:
        return "DEFINE_ERROR: Wrong variablename: %s ! Need provide a symbol as variable name."%(tree[1][list(tree[1])[0]])

def if_f(tree):
    if len(tree) == 4:
        if type(tree[1]) is list:
            if_statement = checkFormat(tree[1])
            if if_statement == '#t':
                return checkFormat(tree[2])
            elif if_statement == '#f':
                return checkFormat(tree[3])
            else:
                return "IF_ERROR: %s is not a valid if statement"%(if_statement)
        else:
            return "IF_ERROR: Need provide a valid if statement"

    else:
        return "IF_ERROR: Wrong numbers of expression!"


if __name__ == '__main__':
    #parserTree = ['plus', 'asd', ['plus', '4', '3'],'4','5']
    #parserTree = ['cdr','\'',['1',['plus','4','3'],'3']]
    parserTree = ['define','x','\'',['plus','2','3']]
    interpreter(parserTree)
    parserTree = ['x']
    interpreter(parserTree)
