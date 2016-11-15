#!/bin/bash
#
# Simple SGE script for submitting multiple serial
# jobs (e.g. parametric studies) using a script wrapper
# to launch the jobs.
#
# To use, build the launcher executable and your
# serial application(s) and place them in your WORKDIR
# directory.  Then, edit the CONTROL_FILE to specify 
# each executable per process.
#-------------------------------------------------------
#-------------------------------------------------------
# 
#         <------ Setup Parameters ------>
#
#SBATCH -J DSSATCSM            # Job name
#SBATCH -n 112                 # Total number of tasks
#SBATCH -p normal              # Queue name
#SBATCH -o DSSATCSM.o%j        # Name of stdout output file (%j expands to jobid)
#SBATCH -t 48:00:00            # Run time (hh:mm:ss)
#      <------------ Account String ------------>
# <--- (Use this ONLY if you have MULTIPLE accounts) --->
#SBATCH -A TG-MCB110022 		#2013020408HPC TG-DEB130024 TG-MCB110022
#------------------------------------------------------

module load launcher
module load python
export EXECUTABLE=$TACC_LAUNCHER_DIR/init_launcher 
export WORKDIR=.
export CONTROL_FILE=joblist.dat
# 
# Variable description:
#
#  EXECUTABLE     = full path to the job launcher executable
#  CONTROL_FILE   = text input file which specifies
#                   executable for each process
#                   (should be located in WORKDIR)
#  WORKDIR        = location of working directory
#
#      <------ End Setup Parameters ------>
#--------------------------------------------------------
#--------------------------------------------------------

#----------------
# Error Checking
#----------------

if [ ! -e $WORKDIR ]
then
    echo " "
	echo "Error: unable to change to working directory."
	echo "       $WORKDIR"
	echo " "
	echo "Job not submitted."
	exit
fi

if [ ! -f $EXECUTABLE ] 
then
	echo " "
	echo "Error: unable to find launcher executable $EXECUTABLE."
	echo " "
	echo "Job not submitted."
	exit
fi

#----------------
# Job Submission
#----------------

cd $WORKDIR/
echo " WORKING DIR:   $WORKDIR/"

echo "Job Started:"
date

python -c "import RunSetup4; RunSetup4.RunSetup('modelinputs.tgz')"

echo "Job Finished:"
date

echo " "
echo " DSSATCSM Job Complete"
echo " "
