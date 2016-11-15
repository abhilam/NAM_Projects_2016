#!/bin/env python
import os
import glob
import PrintCSMFiles
import sobol_lib

def RunModel(runnum):
    #runnum (int) - for calculating Sobol starting seed.
    
    #Get run path and output paths
    runpath = os.path.abspath(os.path.dirname(__file__))
    dirs = os.path.split(runpath)
    outpath = ''
    for idir in dirs[:-1]:
        outpath+=idir
    outpath=os.path.join(outpath,'Output')
    outpath=os.path.join(outpath,dirs[-1])
    
    #Read runlist
    f = open(os.path.join(runpath, 'RUNLIST.CSV'), 'r')
    lines = f.readlines()
    f.close()
    
    filex = lines[0].rstrip().split(':')[1]
    rngp1 = [float(i) for i in lines[2].rstrip().split(':')[1].split(',')]
    rngpr = [float(i) for i in lines[3].rstrip().split(':')[1].split(',')]
    rngph = [float(i) for i in lines[4].rstrip().split(':')[1].split(',')]
    rngtb = [float(i) for i in lines[5].rstrip().split(':')[1].split(',')]
    rngpo = [float(i) for i in lines[6].rstrip().split(':')[1].split(',')]    
        
    #Print cultivar and ecotype files based on Sobol sequence
    dim_num = 5
    seed = runnum*998
    qs = sobol_lib.prime_ge(dim_num)
    mycul = PrintCSMFiles.PrintSGCUL(runpath)
    myeco = PrintCSMFiles.PrintSGECO(runpath)
    results = []
    for i in range(998):
        results.append([])
    for i in range(998):
        [r,seed_out] = sobol_lib.i4_sobol(dim_num,seed)
        seed = seed_out
        p1 = rngp1[0] + r[0] * (rngp1[1] - rngp1[0])
        pr = rngpr[0] + r[1] * (rngpr[1] - rngpr[0])
        ph = rngph[0] + r[2] * (rngph[1] - rngph[0])
        tb = rngtb[0] + r[3] * (rngtb[1] - rngtb[0])
        po = rngpo[0] + r[4] * (rngpo[1] - rngpo[0])
        p2 = 1.2*p1
        panth = 3.667*p1
        mycul.WriteLine(i+1,p1,p2,po,pr,panth,50.0,150.0,700.0,ph,15.0,5.0)
        myeco.WriteLine(i+1,tb,34.0,34.0,6.0,4.2,0.85,0.6,0.250,0.1)
        results[i] = '%6.2f,%6.2f,%6.3f,%6.2f,%6.2f,%6.3f,%5.3f,'%(p1,p2,po,pr,panth,ph,tb)
    mycul.CloseFile()
    myeco.CloseFile()
          
    #Run model
    command = 'DSCSM045.EXE A ' + filex
    os.system(command)  
    
    #Manage Summary.OUT
    f = open(os.path.join(runpath, 'Summary.OUT'), 'r')
    sumout = f.readlines()
    f.close()
    for i in range(998):
        ADAT = str(int(sumout[i+4][117:124]))            
        MDAT = str(int(sumout[i+4][125:132]))
        HWAM = '%5d' % (int(sumout[i+4][157:162]))
        results[i]+=ADAT+','+MDAT+','+HWAM+'\n'
    f = open(os.path.join(runpath, 'Summary.OUT'), 'w')
    f.write('P1,P2,P2O,P2R,PANTH,PHINT,TBASE,ADAT,MDAT,HWAM\n')
    for i in range(998):
        f.write(results[i])
    
    #Manage other model output files
    outfiles = glob.glob(os.path.join(runpath, '*.OUT'))
    for ofile in outfiles:
        fname = os.path.basename(ofile)
        outfname = os.path.join(outpath,fname)
        f = open(outfname, 'a')  
        f.write('\nOutput for ' + filex + ', Job#:' + str(runnum) + '\n\n')
        f.write(open(ofile, 'r').read())
        f.close()
  
if __name__ == '__main__':
    RunModel(9177)
