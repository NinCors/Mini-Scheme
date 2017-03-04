#!/usr/bin/env python3
import re
import sys

def error_messages( error_token ):
    error_model_patterns = {
    's_i':'((\+|\-)?([0-9])+)?(([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*)((\+|\-)([0-9]))?',
    's_r':'((\+|\-)?([0-9])*\.([0-9])+)?(([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*)((\+|\-)?([0-9])*\.[0-9])?', 
    'r_i':'[0-9](\+|\-)'
    }
    errorMessage = ''
    if re.search(error_model_patterns['s_i'], error_token) != None:
        if re.search('\.',error_token) == None:
            errorMessage = 'Need white space between symbol and integer'
        else:
            errorMessage = 'Need white space between symbol and real'
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
    print(tokens)
    return tokens

