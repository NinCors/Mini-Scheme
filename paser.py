#!/usr/bin/env python3
import re
import sys

'''
    This is the Parser part

'''
def checkQuotation(tokens):
    for i in range(len(tokens)):
        if tokens[i] == '\'':
            #check after
            if tokens[i+1] == ')':
                return False,"ERROR: Need atom between ) and \'"
            #check before
            if i >= 1:
                if tokens[i-1] == ')':
                    return False,"ERROR: Don't put ) before \'"
    return True,"cQ test Passed!"

def checkToken(tokens):
    ''' 
        check if there is any unexpected tokens

    '''
    tokenList = {'SYMBOL','REAL','BOOLEAN','INTEGER','PUNCTUATION'}
    for token in tokens:
        if token[0] not in tokenList:
            em = "ERROR: Unexpected token: %s " %(token[1])
            return False, em
    return True, 'cT test passed!'


def checkParentheses(tokens):
    #check if all the parentheses are bound
    #check if there is any parentheses
    pt = {'(',')'}
    clear = True
    for i in tokens:
        if i in pt:
            clear = False
    # if not or the lenth of tokens is 0, return true
    if clear == True or len(tokens) == 0:
        return True, 'cP test passed!'
    else:
        # else, start check pair
        start,end,b,a = findStartEnd(tokens)
        if start != -1 and end != -1:
            # pop start and end, recursively call this function
            tokens.pop(start)
            tokens.pop(end-1)
            return (checkParentheses(tokens))
        else:
            return False,"ERROR: MISSING parentheses!"

def findStartEnd(tokens):
    pre_s = 0
    after_e = len(tokens)
    start = -1
    end = -1        

    findEnd = False
    for w in range(len(tokens)):
        if tokens[w] == ')' and findEnd == False:
            end = w
            findEnd = True
            findAfter = False
            for e in range(w+1,len(tokens)):
                if tokens[e] == ')' and findAfter == False:
                    after_e = e
                    findAfter = True

    for i in range(end):
        if tokens[i] == '(':
            start = i
            for w in range(start):
                if tokens[w] == '(':
                    pre_s = w 

    return start, end, pre_s, after_e


def findRight(left_index,tokens):
    tmp_tokens = []
    for token in tokens:
        tmp_tokens.append(token)
    right = findRight_sub(left_index,tmp_tokens,0)
    return right

def findRight_sub(left_index, tokens,pop):
    start,end,b,a = findStartEnd(tokens)
    #print("start is %d and end is %d"%(start,end))
    if start != -1 and end != -1:
        if start == left_index:
            return end                    
        #pop start and end, recursively call this function
        tokens[start] = ''
        tokens[end] = ''
        return (findRight_sub(left_index,tokens,pop+2))

def parserTree(tokens, parserT):
    inrange = -1
    #print("\nIn this round, tokens is ")
    #print(tokens)
    #print("In this round, parserT is ")
    #print(parserT)
    for i in range(len(tokens)):
        #print("I is %s, value is %s and inrange is %d" %(i,tokens[i],inrange))
        if tokens[i] == '(' and i >= inrange:
            
            right = findRight(i,tokens)
            #print("Try to find right in tokens")
            #print(tokens)
            
            if(type(right) is int):
                tmp_tokens = []
                tmp_tokens = tokens[i+1:right]
                inrange = right
                #print("Left is %d annd right is %d"%(i,right))
                #print("Find (), the values within is ")
                #print(tmp_tokens)
                parserT.append([])
                parserTree(tmp_tokens,parserT[len(parserT)-1])
            else:
                print("Can't find right!")
            
        elif i > inrange and tokens[i] != ')':
            #print("Append token %s with index %s "%(tokens[i],i))
            parserT.append(tokens[i])

def parser( tokens, mode = 't' ):
    '''
        parser body
        
        model:
               s: return string format 
               t: return array format
    '''
    if(type(tokens) is str):
        return tokens
   
    tmp_tokens = []
    for token in tokens:
        tmp_tokens.append(token[1])
        
    tmp_tokens1 = []
    for token in tokens:
        tmp_tokens1.append(token[1])

    cT,m1 = checkToken(tokens)
    cQ,m3 = checkQuotation(tmp_tokens)
    cP,m2 = checkParentheses(tmp_tokens)

    if cT == False:
        return m1, False
       
    elif cP == False:
        return m2, False

    elif cQ == False:
        return m3, False
        
    elif cT and cP and cQ:
        parserT = []
        parserTree(tmp_tokens1,parserT)
        if mode == "s":
            treeStr = treeToStr(parserT)
            return treeStr,True
        return parserT[0],True
    else:
        return "Parser ERROR",False


def treeToStr(parserT):
    returnStr = ''
    for i in parserT:
        if type(i) is list:
            returnStr = returnStr + "() -> \n"
            returnStr = returnStr + "( " + treeToStr(i) + ") "
        else:
            returnStr = returnStr + i + " " 
    return returnStr

