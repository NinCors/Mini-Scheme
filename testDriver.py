#!/usr/bin/env python3
import re
import sys

from paser import parser,findRight
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

def testFunc():
    tokens = ['car', '(', '1', '2', ')', '(', '2', '3', ')']
    print(findRight(5,tokens))

'''
    Test todo:
        checkformat, function
        add more functions
        add more testcase
'''

if __name__ == '__main__':
    #testFunc()
    testDriver_i()
