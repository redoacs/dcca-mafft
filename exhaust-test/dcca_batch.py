#!/usr/bin/python3
'''

@author: Edgar D. Arenas-Díaz
'''

from optparse import OptionParser
import subprocess
import os

DCCA = "../src/dcca.py"

def main():
    parser = OptionParser()
    parser.add_option("-s", "--source-path", dest="srcpath", metavar="SRCPATH",
                      help="Source path for input files")
    parser.add_option("-d", "--destination-path", dest="destpath", metavar="DESTPATH",
                      help="Destination path for the output files")
    parser.add_option("-m", "--minimum-length-align", dest="mlp", metavar="MLP",
                      help="Minimum number of columns of a partition to be aligned again")
    (options,args) = parser.parse_args()
    
    if (options.srcpath == None or options.destpath == None):
        print("Both paths (source and destination) are needed")
        print()
        parser.print_help()
        exit()
        
    if (os.path.exists(options.destpath) == False):
        print("Creating destination path" + options.destpath)
        os.makedirs(options.destpath)
    
    mlp = 0
    
    if not (options.mlp == None):
        mlp = options.mlp
    
    muslcedr(options.srcpath, options.destpath, mlp)
    
def muslcedr(srcPath, destPath, mlp):
    
    contentlist = os.listdir(srcPath)
    dirslist = []
    
    for element in contentlist:
        srcElemFPath = srcPath+"/"+element
        destElemFPath = destPath+"/"+element
        if os.path.isdir(srcElemFPath):
            dirslist.append((srcElemFPath, destElemFPath))
            if not os.path.exists(destElemFPath):
                os.makedirs(destElemFPath)
        elif srcElemFPath.endswith("fst"):
            size = len(destElemFPath)
            destElemFPath = destElemFPath[0:size-3]
            commandStr = DCCA +  " -m " + str(mlp) + " < " + srcElemFPath + " > " + destElemFPath+"fst"
            print(commandStr)
            print(subprocess.getoutput(commandStr))
    
    if(len(dirslist) > 0):
        for dirspath in dirslist:
            muslcedr(dirspath[0], dirspath[1])
    

if __name__ == '__main__':
    main()