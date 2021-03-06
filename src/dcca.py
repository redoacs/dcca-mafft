#!/usr/bin/python3.2
'''

@author: Edgar D. Arenas-Díaz
'''

import basicalign
import colordalign
import partitionalign
import columneval
import sys
import subprocess
import io
from optparse import OptionParser

#MUSCLE = '/home/redoacs/tmp/bioinformatics/projects/dcca-exhaust-test/muscle3.8.31_i86linux64'
#MUSCLE = '/home/redoacs/workspaces/eclipse-bioinformatics/dcca/sw/muscle3.8.31_i86linux32'
FFTNS = ['fftns', '--preservecase' , '/tmp/alintmp.fst']
EINSI = ['einsi', '--preservecase' , '/tmp/alintmp.fst']

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option("-m", "--minimum-length-align", dest="mlp", metavar="MLP",
                      help="Minimum number of columns of a partition to be aligned again")
    (options,args) = parser.parse_args()
    
    mlp = 0
    
    if not (options.mlp == None):
        mlp = int(options.mlp)
    
    basalPreIM = basicalign.readFASTA(sys.stdin)
    #print(basalPreIM)
    
    
    #columnHomogeneity = columneval.computeColumnHomogeneity(colordalign.columnifyBasal(basalPreIM).columns)
    #print('Initial CH:', sum(columnHomogeneity)/len(columnHomogeneity))
    
    sio = io.StringIO()
    #basicalign.printFASTA(basalPreIM, sio)

    tmpFile = open('/tmp/alintmp.fst','w')
    basicalign.printFASTA(basalPreIM,tmpFile)
    tmpFile.close()
    
    process = subprocess.Popen(FFTNS, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    out, err = process.communicate( bytes(sio.getvalue(), 'utf-8') )
    
    basalPostIM =  basicalign.readFASTA( io.StringIO(out.decode()) )
            
    colordal = colordalign.columnifyBasal(basalPostIM)
    
    partitions = partitionalign.partitionAlignment(colordal, columneval.computeColumnHomogeneity, 0.85, 10)
    partitionsPost = []
    offset = 0
    size = 0;
    mutable_counter = 0;
    for part,ann in partitions:
        offset = offset + size
        size = len(part)
        #if ann:
        if ann and size >= mlp:
            mutable_counter = mutable_counter + 1
            print("Mutable", offset, '-', offset+size-1, '('+str(size)+')', file=sys.stderr)
            #print('Mutable partition:')
            basalpartPre = partitionalign.basalifyPartition(part, colordal.names)
            #print('basalpartPre:',basalpartPre)
            sio = io.StringIO()
            #basicalign.printFASTA(basalpartPre,sio)
            
            tmpFile = open('/tmp/alintmp.fst','w')
            basicalign.printFASTA(basalpartPre,tmpFile)
            tmpFile.close()

            process = subprocess.Popen(EINSI, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
            out, err = process.communicate( bytes(sio.getvalue(), 'utf-8') )
            
            basalpartPost = basicalign.readFASTA( io.StringIO(out.decode()) )
            #print('basalpartPost:', basalpartPost)
            basalpartCert = partitionalign.certifyBasal(basalpartPre, basalpartPost)
            #print('basalpartCert',  basalpartCert )
            partitionalign.verifyExactBasal(basalpartPre, basalpartCert)
            partitionsPost.append(colordalign.columnifyBasal(basalpartCert).columns)
        else:
            #print("Fixed", offset, '-', offset+size-1, '('+str(size)+')', file=sys.stderr)
            #print('Fixed partition:')
            #basalpartPre = partitionalign.basalifyPartition(part, colordal.names)
            #print(basalpartPre)
            partitionsPost.append(part)
    print("# of mutable partitions:", mutable_counter, file=sys.stderr)
    basalPost = partitionalign.basalifyPartitionList(partitionsPost, basalPostIM.names)
    basicalign.printFASTA(basalPost)
    #columnHomogeneity = columneval.computeColumnHomogeneity(colordalign.columnifyBasal(basalPost).columns)
    #print('Final CH:', sum(columnHomogeneity)/len(columnHomogeneity))
    
