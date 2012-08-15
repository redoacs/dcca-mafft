#!/usr/bin/python3
'''

@author: Edgar D. Arenas-Díaz
'''
from basicalign import cReadFASTA
from colordalign import columnifyBasal, purgeColordal         
from math import pow

def computeColumnHomogeneity(alignmentColumns):
    allSymbolCounts = []
    columnHomogeneity = []
    
    for column in alignmentColumns:
        symbolCount = {} 
        
        for symbol in column:
            if symbol in symbolCount:
                symbolCount[symbol] = symbolCount[symbol] + 1
            else:
                symbolCount[symbol] = 1
         
        if ( ('-' in symbolCount) and symbolCount['-'] == len(column) ):
            columnHomogeneity.append(0)
        else:
            upperTerm = 0
            lowerTerm = 0                
            for symbol in symbolCount:
                if symbol!='-':
                    upperTerm += pow(symbolCount[symbol],2)
                lowerTerm += symbolCount[symbol]
            columnHomogeneity.append(upperTerm/pow(lowerTerm,2))
        
        allSymbolCounts.append(symbolCount)
    
    #for sc,ch in zip(allSymbolCounts,columnHomogeneity):
    #    print(sc, ch)
    
    return columnHomogeneity
    

if __name__ == '__main__':
    filename = '../testfiles/mini-fasta-test.fst'
    balign = cReadFASTA(filename)
    calign = purgeColordal(columnifyBasal(balign))
    print(calign)
    columnHomogeneity = computeColumnHomogeneity(calign.columns)
    print(columnHomogeneity)
    print(sum(columnHomogeneity)/len(columnHomogeneity))
