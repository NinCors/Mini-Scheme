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
        print("In this round, start is %d and end is %d"%( start,end))
        print("Tokens are")
        print(tokens)
        if start != -1 and end != -1:
            # pop start and end, recursively call this function
            tokens.pop(start)
            tokens.pop(end-1)
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
    #print("\nThis is the token")
    #print(tokens)
    #print("This round start! The start is %d and end is %d"%(start,end))
    # Now, I alreay passed the checkParentheses test.If start or end still equal -1,
    # then it means there is not any parenthese in the tokens
    if start != -1 and end != -1:
        # before
        #print("before_append")
        for i in range(start):
            #print(tokenns[i])
            parserT.append(tokens[i])
        # Between start and after
        parserT.append([])
        tmp_tokens = tokens[start+1:end]
        #print("Between_append")
        #print(tmp_tokens)
        parserTree(tmp_tokens, parserT[start])
        # After 
        #print("After_append")
        for w in range(end+1, len(tokens)):
            #print(tokens[w])
            parserT.append(tokens[w])
    else:
        #print("else_append")
        for i in range(len(tokens)):
            #print(tokens[i])
            parserT.append(tokens[i])
        return parserT 



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

