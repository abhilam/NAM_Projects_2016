#!/bin/env python
import os
import shutil
import glob

def RunSetup(inptgz):
    #inptgz (str) - name of a tar file containing model input files, template files, and RUNLIST.CSV
    
    numcores = int(os.environ.get('SLURM_NTASKS'))
    thispath = os.path.abspath(os.path.dirname(__file__)) #$WORK/DSSATCSM/
    modelpath = os.path.join(thispath, 'DSSAT45') #$WORK/DSSATCSM/DSSAT45/
    scratchpath = thispath.replace('work','scratch') 
    
    #Create directory structure
    runsdir = os.path.join(thispath,'RunsDir') #$WORK/DSSATCSM/RunsDir/
    if os.path.isdir(runsdir):
        shutil.rmtree(runsdir)
    os.makedirs(runsdir)
    commonpath = os.path.join(runsdir, 'Common') #$WORK/DSSATCSM/RunsDir/Common
    os.makedirs(commonpath)
    outputpath = os.path.join(runsdir,'Output') #$WORK/DSSATCSM/RunsDir/Output
    os.makedirs(outputpath)
    for i in range(numcores):
        newpath = os.path.join(runsdir,str(i)) #$WORK/DSSATCSM/RunsDir/0/
        os.makedirs(newpath)
        newpath = os.path.join(outputpath,str(i)) #$WORK/DSSATCSM/RunsDir/Output/0/
        os.makedirs(newpath)
    os.system('ln -s ' + modelpath + ' ' + os.path.join(runsdir,'DSSAT45')) #$WORK/DSSATCSM/RunsDir/DSSAT45/
    
    #Copy and link files
    shutil.copy(os.path.join(thispath,inptgz),os.path.join(commonpath,inptgz))
    os.chdir(commonpath)
    os.system('tar xzf ' + inptgz + " --transform='s/.*\///'")
    os.chdir(thispath)
    infiles = glob.glob(os.path.join(commonpath, '*.*'))
    for ifile in infiles:
        fname = os.path.basename(ifile)
        for i in range(numcores):
            simdir = os.path.join(runsdir,str(i))
            os.system('ln -s ' + ifile + ' ' + os.path.join(simdir,fname))
    for i in range(numcores):
        simdir = os.path.join(runsdir,str(i))
        os.system('ln -s ' + os.path.join(modelpath,'DSCSM045.EXE') + ' ' + os.path.join(simdir,'DSCSM045.EXE'))
        os.system('ln -s ' + os.path.join(thispath,'RunModel4.py') + ' ' + os.path.join(simdir, 'RunModel4.py'))
        os.system('ln -s ' + os.path.join(thispath,'sobol_lib.py') + ' ' + os.path.join(simdir, 'sobol_lib.py'))
        os.system('ln -s ' + os.path.join(thispath,'PrintCSMFiles.py') + ' ' + os.path.join(simdir, 'PrintCSMFiles.py'))
        
    #Print job file     
    f = open(os.path.join(commonpath,'RUNLIST.CSV'), 'r')
    runlist=f.readlines()
    f.close()
    jobrange = runlist[1].rstrip().split(':')
    f = open(os.path.join(thispath,'joblist.dat'), 'w')
    j=0
    if os.path.exists(os.path.join(thispath,os.path.join('Post','ErroredJobs.txt'))):
        ferr = open(os.path.join(thispath,os.path.join('Post','ErroredJobs.txt')))
        errjobs = ferr.readlines()
        ferr.close()
        for err in errjobs:
            f.write('cd ' + runsdir + '/' + str(j) + '/; ')
            f.write('python -c "import RunModel4; RunModel4.RunModel(' + str(int(err)) + ')"\n')
            j+=1
            if j == numcores:
                j=0
    else: 
        for i in range(int(jobrange[1]),int(jobrange[2])):     
            f.write('cd ' + runsdir + '/' + str(j) + '/; ')
            f.write('python -c "import RunModel4; RunModel4.RunModel(' + str(i) + ')"\n')
            j+=1
            if j == numcores:
                j=0
    f.close()q
        
    #Launch
    os.system('$TACC_LAUNCHER_DIR/paramrun $EXECUTABLE ' + os.path.join(thispath,'joblist.dat'))
    #os.system('$TACC_LAUNCHER_DIR/paramrun SLURM $EXECUTABLE $WORKDIR ' + os.path.join(thispath,'joblist.dat') + ' `hostname` $PHI_WORKDIR $PHI_CONTROL_FILE')
    
    #Assemble output and clean up
    outfiles = glob.glob(os.path.join(outputpath,os.path.join('*','*.OUT')))
    outfiles = [os.path.basename(ofile) for ofile in outfiles]
    outfiles = list(set(outfiles))
    for ofile in outfiles:
        outfname = os.path.join(outputpath,ofile)
        f = open(outfname, 'w')
        for i in range(numcores):
            simoutfile = os.path.join(outputpath,os.path.join(str(i),ofile))
            if os.path.exists(simoutfile):
                f.write(open(simoutfile, 'r').read())
        f.close()
    for i in range(numcores):
        shutil.rmtree(os.path.join(outputpath, str(i)))
    os.chdir(runsdir)
    os.system('tar czf modeloutputs.tgz Output')
    os.chdir(thispath)
    shutil.copy(os.path.join(runsdir,'modeloutputs.tgz'),os.path.join(thispath,'modeloutputs.tgz'))
    shutil.rmtree(runsdir)
    os.system('rm joblist.dat')   
    
if __name__ == '__main__':
    RunSetup('modelinputs.tgz')
