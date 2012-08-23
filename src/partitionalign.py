#!/usr/bin/python3
'''

@author: Edgar D. Arenas-Díaz
'''
from basicalign import cReadFASTA, Basal
from colordalign import purgeColordal, columnifyBasal, Colordal, basalifyColordal
from columneval import computeColumnHomogeneity

def partitionAlignment(colordal, eval, threshold, minFixedPart):
    colscore = eval(colordal.columns)
    
    partitions = []
    mutablePartCandidate = []
    fixedPartCandidate = []
    for score,column in zip(colscore, colordal.columns):
        if score >= threshold:
            mutablePartCandidate.append(column)
            fixedPartCandidate.append(column)
        else:
            if len(fixedPartCandidate) >= minFixedPart :
                if len(mutablePartCandidate) > len(fixedPartCandidate):
                    partitions.append( (mutablePartCandidate[:-len(fixedPartCandidate)], True) )
                partitions.append( (fixedPartCandidate, False) )
                mutablePartCandidate = []
                fixedPartCandidate = []
            fixedPartCandidate = []
            mutablePartCandidate.append(column)
        
    if len(fixedPartCandidate) >= minFixedPart :
        partitions.append( (mutablePartCandidate[:-len(fixedPartCandidate)], True) )
        partitions.append( (fixedPartCandidate, False) )
    else:
        partitions.append( (mutablePartCandidate, True) )
    
    return partitions

def colordalifyPartition(partition, names):
    binfo = {'nseqs' : len(names), 'maxlen' : len(partition)}
    return Colordal(names=names, columns=partition, binfo=binfo)

def colordalifyPartitionList(partitions, names):
    columns = [ col for part in partitions for col in part ]
    return colordalifyPartition(columns, names)

def basalifyPartition(partition, names):
    colordal = colordalifyPartition(partition, names)
    return basalifyColordal(colordal)

def basalifyPartitionList(partitions, names):
    colordal = colordalifyPartitionList(partitions,names)
    return basalifyColordal(colordal)

def certifyBasal(refBasal, targetBasal):
    targetDict = {}
    maxlen = 0
    for name,seq in zip(targetBasal.names, targetBasal.seqs):
        targetDict[name] = seq
        if len(seq) > maxlen: maxlen = len(seq)
    verifiedSeqs = []
    for name in refBasal.names:
        if name in targetDict:
            verifiedSeqs.append(targetDict[name])
        else:
            verifiedSeqs.append(['-'])
    binfo = {'nseqs':len(refBasal.names), 'maxlen': maxlen}
    return Basal(names=refBasal.names, seqs=verifiedSeqs, binfo=binfo)

def verifyExactBasal(refBasal, tarBasal):
    
    if not (len(refBasal.names) == len(tarBasal.names) == len(refBasal.seqs) == len(tarBasal.seqs) ):
        raise RuntimeError( 'Different lengths: refBasal.names', len(refBasal.names), 'tarBasal.names', len(tarBasal.names), 'refBasal.seqs', len(refBasal.seqs), 'tarBasal.seqs', len(tarBasal.seqs) )
    
    for rname, tname, rseq, tseq, i in zip(refBasal.names, tarBasal.names, refBasal.seqs, tarBasal.seqs, range(len(refBasal.names))):
        if rname != tname: raise RuntimeError('Different names: ', rname, tname, 'at seq', i)
        prseq = [sym for sym in rseq if sym != '-']
        ptseq = [sym for sym in tseq if sym != '-']
        if len(prseq) != len(ptseq): raise RuntimeError('Different number of symbols:', len(prseq), len(ptseq), 'at seq', i)
        for rsym, tsym, j in zip( prseq, ptseq, range(len(prseq)) ):
            if rsym != tsym: raise RuntimeError('Different symbols:', rsym, tsym, 'at seq', i , 'position', j)

if __name__ == '__main__':
    filename = '../testfiles/mini-fasta-test.fst'
    balign = cReadFASTA(filename)
    print(balign)
    calign = purgeColordal(columnifyBasal(balign))
    print(calign)
    columnHomogeneity = computeColumnHomogeneity(calign.columns)
    print(columnHomogeneity, "mean:", sum(columnHomogeneity)/len(columnHomogeneity))
    annPartitions = partitionAlignment(calign, computeColumnHomogeneity, threshold=0.60, minFixedPart=3)
    for annPart in annPartitions: print(annPart, end='\n')
    partitions = [p for p,a in annPartitions]
    
    rcalign = colordalifyPartitionList(partitions, calign.names)
    print(rcalign)
    
    balignlist = []
    for part in partitions:
        balignlist.append(basalifyPartition(part, calign.names))
        
    for ba in balignlist:print(ba)
    