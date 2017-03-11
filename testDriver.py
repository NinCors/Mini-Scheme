#!/usr/bin/env python3
import re
import sys

from paser import parser
from scanner import scanner
from interpreter import interpreter


def testDriver_s():
    for line in sys.stdin:
        outPut = ''
        if line == '\n':
            print('The input line is empty, exit program')
            sys.exit()
        info = scanner(line,'t')
        print(info)
        print('\n')
        #outPut = "\nInput string : " + line + info  + '\n'
        sys.stdout.write(outPut)

def testDriver_p():
    for line in sys.stdin:
        outPut = ''
        if line == '\n':
            print('The input line is empty, exit program')
            sys.exit()
        parserInfo, status = parser(scanner(line,'t'),'t')
        print("This is final result")
        print(parserInfo)
        #outPut = "\nInput string : " + line + parserInfo  + '\n'
        sys.stdout.write(outPut)

def testDriver_i():
    for line in sys.stdin:
        outPut = ''
        if line == '\n':
            print('The input line is empty, exit program')
            sys.exit()
        info, status = parser(scanner(line,'s'),'t')
        if status == True:
            info = interpreter(info)
        outPut = "\nInput string : " + line + str(info) + '\n'
        sys.stdout.write(outPut)

'''
    Test todo:
        plus: with 1 argument or none argumennt
        parserError: (isnnull '(1 2 3) '()) why this one miss parenthese
        car: return with type format name before it {'SYMBOL': 'plus'}, need get rid of format
        

'''



if __name__ == '__main__':
    testDriver_p()
