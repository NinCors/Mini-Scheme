#!/usr/bin/env python3
import re
import sys

from paser import parser
from scanner import scanner

def testDriver():
    for line in sys.stdin:
        outPut = ''
        if line == '\n':
            print('The input line is empty, exit program')
            sys.exit()
        parserInfo, status = parser(scanner(line,'s'),'s')
        outPut = "\nInput string : " + line + parserInfo  + '\n'
        sys.stdout.write(outPut)

if __name__ == '__main__':
    testDriver()
