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
    '''
        check if all the parentheses are bound

    '''
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
        start,end = findStartEnd(tokens)
        #print("tokens is")
        #print(tokens)
        #print("start is " + str(start))
        #print("end is "+ str(end))
        if start != -1 and end != -1:
            # pop start and end, recursively call this function
            tokens.pop(start)
            tokens.pop(end-1)
            #print("New tokens is")
            #print(tokens)
            return (checkParentheses(tokens))
        else:
            return False,"ERROR: MISSING parentheses!"


def findStartEnd(tokens):
    start = -1
    end = -1        
    findFirst = False
    for i in range(len(tokens)):
        if tokens[i] == '(' and findFirst == False:
            start = i
            findFirst = True
            for w in range(i+1, len(tokens)):
                if tokens[w] == ')':
                    end = w
    return start, end

def parserTree(tokens, parserT):
    '''
        Build the tree structure

    '''
    start,end = findStartEnd(tokens)
    # Now, I alreay passed the checkParentheses test.If start or end still equal -1,
    # then it means there is not any parenthese in the tokens
    if start != -1 and end != -1:
        # before
        for i in range(start):
            parserT.append(tokens[i])
        # Between start and after
        parserT.append([])
        tmp_tokens = tokens[start+1:end]
        parserTree(tmp_tokens, parserT[start])
        # After 
        for w in range(end, len(tokens)-1):
            parserT.append(tokens[w])


    else:
        for i in range(len(tokens)):
            parserT.append(tokens[i])
        return parserT 

def parser( tokens ):
    '''
        parser body
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
        return m1
       
    elif cP == False:
        return m2

    elif cQ == False:
        return m3
        
    elif cT and cP and cQ:
        parserT = []
        parserTree(tmp_tokens1,parserT)
        return treeToStr(parserT)
    else:
        return "Parser ERROR"


def treeToStr(parserT):
    returnStr = ''
    for i in parserT:
        if type(i) is list:
            returnStr = returnStr + "() -> \n"
            returnStr = returnStr + "( " + treeToStr(i) + " ) "
        else:
            returnStr = returnStr + i + " " 

    return returnStr

