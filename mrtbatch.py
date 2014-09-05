#!usr/bin/python
#MRT Batch Process
#bahadir

import os 
import sys 
import re 
import subprocess



def readHdf(hdfdir,prmdir):
    hdflist = []
    for f in os.listdir(hdfdir):
        if f.endswith('.hdf'):
            hdfname =os.path.splitext(f)[0] 
            hdflist.append(hdfdir + hdfname)
        else:
            pass
    if not hdflist:
        sys.exit('No HDF file(s) in Directory!')
    return hdflist

def writeprm(hdflist):
    for hdf in (hdflist):
        with open(hdf + '.prm' , 'w') as prmout:
            with open(prmdir, 'r') as prmin:
                for line in prmin:
                    line = re.sub(r'INPUT_FILENAME\s=\s(.+)', hdf + '.hdf' , line) 
                    line = re.sub(r'OUTPUT_FILENAME\s=\s(.+)', hdf + '.tif', line)
                    prmout.write(line)

def createbatch():
    with open('batch.bat', 'w') as batch: 
        for prm in os.listdir(hdfdir):
            if prm.endswith('.prm'):
                batch.writelines('swtif.exe -p ' + hdfdir + prm + '\n')
                    
if __name__ == '__main__':
    hdfdir = sys.argv[1]
    prmdir = sys.argv[2]
    hdflist = readHdf(hdfdir,prmdir)
    writeprm(hdflist)
    createbatch()
    subprocess.call('batch.bat')