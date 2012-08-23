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
                      help="Path to the source files")
    parser.add_option("-d", "--destination-path", dest="destpath", metavar="DESTPATH",
                      help="Destination path for output files")
    (options,args) = parser.parse_args()
    
    if (options.srcpath == None or options.destpath == None):
        print("Both paths (source and destination) are needed")
        print()
        parser.print_help()
        exit()
        
    if (os.path.exists(options.destpath) == False):
        print("Creating destination path" + options.destpath)
        os.makedirs(options.destpath)
    
    rate(options.srcpath, options.destpath)
    
def rate(srcPath, destPath):
    
    contentlist = os.listdir(srcPath)
    dirslist = []
    
    for element in contentlist:
        tbElemFPath = srcPath+"/"+element
        destElemFPath = destPath+"/"+element
        if os.path.isdir(tbElemFPath):
            dirslist.append((tbElemFPath, destElemFPath))
            if not os.path.exists(destElemFPath):
                os.makedirs(destElemFPath)
        elif tbElemFPath.endswith("fst"):
            size = len(destElemFPath)
            destElemFPath = destElemFPath[0:size-3]
            cmd = "java -jar glocsaeval/glocsaeval.jar " + tbElemFPath + " " + destElemFPath + "rating" 
            print(cmd)
            print(subprocess.getoutput(cmd))
    
    if(len(dirslist) > 0):
        for dirspath in dirslist:
            rate(dirspath[0], dirspath[1])
    
    
if __name__ == '__main__':
    main()