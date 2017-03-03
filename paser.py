#!/usr/bin/env python3
import re
import sys

def error_messages( error_token ):
    error_model_patterns = {
    's_i':'((\+|\-)?([0-9])+)?(([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*)((\+|\-)([0-9]))?',
    #'i_s':'(\+|\-)?([0-9])+(([a-z]|[A-Z])([a-z]|[A-Z]|[0-9]))',
    's_r':'((\+|\-)?([0-9])*\.([0-9])+)?(([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*)((\+|\-)?([0-9])*\.[0-9])?', 
    #'r_s':'(\+|\-)?([0-9])*\.([0-9])+(([a-z]|[A-Z])([a-z]|[A-Z]|[0-9]))',
    'r_i':'[0-9](\+|\-)'
    }
    errorMessage = ''
    if re.search(error_model_patterns['s_i'], error_token) != None:
        if re.search('\.',error_token) == None:
            errorMessage = 'Need white space between symbol and integer'
        else:
            errorMessage = 'Need white space between symbol and real'
    #elif re.search(error_model_patterns['i_s'], error_token) != None:
     #   errorMessage = 'Do not put integer before symbol, need white space'
      #  if re.search(error_model_patterns['r_s'], error_token) != None:
       #     errorMessage = 'Do not put real number before symbol, need white space'
    if re.search('\#', error_token) != None:
        if re.search('\#t|\#f',error_token) != None:
            if re.search('\.', error_token) != None:
                errorMessage = 'Need white spcae between boolean and real number'
            elif re.search('((\#t|\#f)([a-z]|[A-z]))|(([a-z]|[A-z])(\#t|\#f))', error_token) != None:
                errorMessage = 'Need white space between boolean and symbol'
            elif re.search('[0-9]',error_token ) != None:
                errorMessage = 'Need white space between boolean and integer'
        elif re.search('\#[0-9]|[a-z]|[A-Z]', error_token) != None:
            errorMessage = 'input the unknown symbol after #'
        else:
            errorMessage = 'Wrong boolean pattern'
    if re.search(error_model_patterns['r_i'],error_token ) != None:
        if re.search('([0-9](\+|\-)([0-9])(\.)?)', error_token) != None:
            errorMessage = 'Need white space bwtween two numbers'
        else:
            errorMessage = 'wrong usage of + or - symbol'
    if errorMessage == '':
        errorMessage = 'Unknow error'
        
    return errorMessage

def pattern_match( token, model_patterns ):
    token_info = []
    match = 0
    for types in model_patterns:
        if re.fullmatch( model_patterns[types], token) != None:
            match = match + 1
            token_info.append(types)
            token_info.append(token)
            return token_info
    if match == 0:
        token_info.append('error')
        token_info.append(token)
        token_info.append( error_messages( token ) )
        return token_info
        

def getToken( pattern ):
    #If punctuation in the pattern, divide the pattern into different tokens
    punctuations = []
    #Save all the puncuations
    for match in re.finditer('\(|\)|\'', pattern):
        s = match.start()
        e = match.end()
        punctuations.append( pattern[s:e] )
    punctuations = punctuations[::-1]
    #print("The punctuations are ")
    #print(punctuations)

    #get the tokens without puncuations and combine it with the saved puncuations
    tokens = re.split('\(|\)|\'', pattern)
    #print("The tokens are")
    #print(tokens)

    #get last token that is not puncuation
    lastPosition = 0
    allPunc = True
    for i in range(len(tokens)):
        if tokens[i] != '':
            allPunc = False
            lastPosition = i
    #print("The lastpostion is " + str(lastPosition))
    change = []
    for i in range(lastPosition):
        if tokens[i] != '':
            find = False
            for w in range( i+1,lastPosition+1):
                if tokens[w] != '' and find == False:
                    change.append(w)
                    find = True
    #print("The change is ")
    #print(change)
    for i in range(len(change)):
        tokens.insert(change[i], '')
    #print("New tokens is")
    if allPunc == True:
        tokens.pop()

    for i in range(len(tokens)):
        if tokens[i] == '':
            tokens[i] = punctuations.pop()     
    #print("Final tokens is")
    #print(tokens)
    
    return tokens
 


def scanner( inputStrings='', mode='s' ):
    '''
	mode: 't' - token mode, scanner will return the scanned tokens.
		  'm' - message mode, scanner will return the full information of scanned tokens


    '''
    model_patterns = {
    'SYMBOL':'([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*',
    'INTEGER':'(\+|\-)?([0-9])+', 
    'REAL':'(\+|\-)?([0-9])*\.([0-9])+',
    'PUNCTUATION':'\(|\)|\'',
    'BOOLEAN':'(\#t|\#f)' 
   }
    inputString = inputStrings.split()
    scanner_result = []
    for pattern in inputString:
        tokens = getToken( pattern )
        for token in tokens:
            result = pattern_match( token, model_patterns ) 
            scanner_result.append(result)
    tokens = []
    output = inputStrings + '\n'
    error = False
    for token in scanner_result:
        tokens.append(token)
        tmp = token[0]+ ' : '+ token[1]
        if len(token) == 3:
            tmp = tmp + '  Error message: '+ token[2]
            error = True
            errorMessage = 'Error token: '+ token[1] + " -> " + token[2]
        output = output + tmp + '\n'
    if mode=='m':
        return output
    if (error == True):
        return errorMessage
    return tokens



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

def testDriver():
    for line in sys.stdin:
        outPut = ''
        if line == '\n':
            print('The input line is empty, exit program')
            sys.exit()
        outPut = "\nInput string : " + line + parser(scanner(line,'s')) + '\n'
        sys.stdout.write(outPut)

if __name__ == '__main__':
    testDriver()
