#!/usr/bin/python3
'''

@author: Edgar D. Arenas-Díaz
'''

from optparse import OptionParser
import subprocess
import os

COMMAND = "einsi"

def main():
    parser = OptionParser()
    parser.add_option("-s", "--source-path", dest="srcpath", metavar="SRCPATH",
                      help="Path to source files")
    parser.add_option("-d", "--destination-path", dest="destpath", metavar="DESTPATH",
                      help="Destination path for the output files")
    (options,args) = parser.parse_args()
    
    if (options.srcpath == None or options.destpath == None):
        print("Both paths (source and destination) are needed")
        print()
        parser.print_help()
        exit()
        
    if (os.path.exists(options.destpath) == False):
        print("Creating destination path" + options.destpath)
        os.makedirs(options.destpath)
    
    commanddr(options.srcpath, options.destpath)
    
def commanddr(srcPath, destPath):
    
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
            cmd_str = COMMAND + " " + srcElemFPath + " > " + destElemFPath+"fst"
            print(cmd_str)
            print(subprocess.getoutput(cmd_str))
    
    if(len(dirslist) > 0):
        for dirspath in dirslist:
            commanddr(dirspath[0], dirspath[1])
    

if __name__ == '__main__':
    main()
