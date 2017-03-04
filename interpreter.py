import re
import sys

from paser import parser
from scanner import scanner,pattern_match

def interpreter( parserTree ):
    print(convert(parserTree))


def convert(tree):
    model_patterns = {
     'SYMBOL':'([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*',
     'INTEGER':'(\+|\-)?([0-9])+', 
     'REAL':'(\+|\-)?([0-9])*\.([0-9])+',
     'PUNCTUATION':'\(|\)|\'',
     'BOOLEAN':'(\#t|\#f)' 
    }

    for i in range(len(tree)):
        if type(tree[i]) is list:
            convert(tree[i])
        else:
            tree[i] = pattern_match(tree[i], model_patterns)
    return tree
   

if __name__ == '__main__':
    parserTree = ['isnull', "'", []]
    interpreter(parserTree)
