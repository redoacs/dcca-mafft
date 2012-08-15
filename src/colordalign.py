#!/usr/bin/python3
'''

@author: Edgar D. Arenas-Díaz
'''
from basicalign import cReadFASTA, Basal

class Colordal(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
        
    def __str__(self):
        string = str(self.binfo) + "\n"
        string += str(self.names) + '\n'
        for c in self.columns:
            string += str(c) + '\n'
        return string

def columnifyBasal(basal):
    
    maxlen = basal.binfo['maxlen']
    nseqs = basal.binfo['nseqs']
    seqlen = []
    
    for seq in basal.seqs: seqlen.append(len(seq))
    
    columns = []
    
    for j in range(maxlen):
        column = []
        for i in range(nseqs):
            if j < seqlen[i]:
                column.append(basal.seqs[i][j])
            else:
                column.append('-')
        columns.append(column)
        
    return Colordal(names=basal.names, columns=columns, binfo=basal.binfo)
    
def isAllGaps(column):
    val = True
    for sym in column:
        if sym != '-': 
            val = False
            break
    return val

#Eliminate columns which contents are only '-' 
def purgeColordal(colordal):
    colskeep = []
    for col in colordal.columns:
        if not isAllGaps(col):
            colskeep.append(col)
    
    binfo = {'maxlen': len(colskeep), 'nseqs': colordal.binfo['nseqs']}
    
    return Colordal(names=colordal.names, columns=colskeep, binfo=binfo)

def basalifyColordal(colordal):
    seqs = [ [] for i in range(colordal.binfo['nseqs']) ]
    for col in colordal.columns:
        for seq,sym in zip(seqs,col):
            seq.append(sym)
    return Basal(names=colordal.names, seqs=seqs, binfo=colordal.binfo)

if __name__ == '__main__':
    filename = '../testfiles/mini-fasta-test.fst'
    balign = cReadFASTA(filename)
    print(balign)
    calign = columnifyBasal(balign)
    print(calign)
    pcalign = purgeColordal(calign)
    print(pcalign)
    pbalign = basalifyColordal(pcalign)
    print(pbalign)