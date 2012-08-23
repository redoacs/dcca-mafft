#!/usr/bin/python3
'''

@author: Edgar D. Arenas-Díaz
'''

from optparse import OptionParser
import subprocess
import os

def main():
    parser = OptionParser()
    parser.add_option("-s", "--source-path", dest="srcpath", metavar="SRCPATH",
                      help="Path to source files")
    parser.add_option("-f", "--results-filename", dest="resultpath", metavar="RESULTPATH",
                      help="Name of the output results file")
    (options,args) = parser.parse_args()
    
    if (options.srcpath == None or options.resultpath == None):
        print("Both paths (source and results filename) are needed")
        print()
        parser.print_help()
        exit()   
    
    outFile = open(options.resultpath, 'w')
    print('alignment-file-rated, GLOCSA, meanColumnValue, gapConcentration, columnIncrementRatio, meanGapBlockSize, totalGapPositions, numberGapBlocks, columnsNotAligned, columnsAligned, estimatedEvents, substitutionEvents, inDelEvents', file=outFile)
    print('alignment-file-rated, GLOCSA, meanColumnValue, gapConcentration, columnIncrementRatio, meanGapBlockSize, totalGapPositions, numberGapBlocks, columnsNotAligned, columnsAligned, estimatedEvents, substitutionEvents, inDelEvents')
    
    action(options.srcpath, outFile)
    outFile.close()
    
def action(srcPath, outFile):
    
    contentlist = os.listdir(srcPath)
    dirslist = []
    
    for element in contentlist:
        srcElemFPath = srcPath+"/"+element
        if os.path.isdir(srcElemFPath):
            dirslist.append(srcElemFPath)
        elif srcElemFPath.endswith("rating"):
            ratingFile = open(srcElemFPath, 'r')
            
            line = ratingFile.readline()
            
            while line != '':
                line = line[:-1]
                name,sep,value = line.partition(':')
                if sep == ':':
                    value = value.strip()
                    print(value, end=', ', file=outFile)
                    print(value, end=', ',)
                line = ratingFile.readline()
                
            print('', file=outFile)
            print('')
            ratingFile.close()
    
    if(len(dirslist) > 0):
        for dirspath in dirslist:
            action(dirspath, outFile)
    

if __name__ == '__main__':
    main()