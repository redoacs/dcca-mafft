#!/usr/bin/python3
'''

@author: Edgar D. Arenas-Díaz
'''

import sys

class Basal(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
        
    def __str__(self):
        string = str(self.binfo) + "\n"
        for n,s in zip(self.names, self.seqs):
            string += '>' + n + ': ' + str(s) + '\n'
        return string

def cReadFASTA(filename):
    file = open(filename)
    basal = readFASTA(file)
    file.close()
    return basal

def readFASTA(file=sys.stdout):
    
    line = file.readline()
    
    names = []
    namesSet = set()
    seqs = []
    maxlen = 0
    
    readingSeq = False 
    seqtemp = []
    
    while line != '':
        line = line[:-1]

        if line[0] != ';': #it is not a comment
            if line[0] == '>': # it is a sequence name
                name = line[1:]
                if name not in namesSet:
                    names.append(name)
                    namesSet.add(name)
                else:
                    raise ValueError('Repeated sequence names in alignment')
                if readingSeq:
                    seqlen = len(seqtemp)
                    if seqlen > maxlen: maxlen = seqlen 
                    seqs.append(seqtemp)
                    seqtemp = []
                readingSeq = True
            elif readingSeq:
                seqtemp += line
                
        line = file.readline()
    
    if readingSeq:
        seqlen = len(seqtemp)
        if seqlen > maxlen: maxlen = seqlen 
        seqs.append(seqtemp)
    
    binfo = {'nseqs':len(names), 'maxlen': maxlen}
    return Basal(names=names, seqs=seqs, binfo=binfo)

def cWriteFASTA(basal, filename):
    file = open(filename, 'w')
    printFASTA(basal, file)
        

def printFASTA(basal, file=sys.stdout):
    for name,seq in zip(basal.names,basal.seqs):
        print('>', name , sep='', file=file)
        for sym in seq:
            print(sym, end='', file=file)
        print(file=file)
        

if __name__ == '__main__':
    filename = '../testfiles/mini-fasta-test.fst'
    wFilename = '../testfiles/mini-fasta-test.write.fst'
    alignment = cReadFASTA(filename)
    print(alignment)
    printFASTA(alignment)
    
    cWriteFASTA(alignment, wFilename)