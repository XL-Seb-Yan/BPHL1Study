#!/usr/bin/env python
import os, re, sys, commands, math, time, calendar

print '\nSTART\n'
ts = calendar.timegm(time.gmtime())

fileName = "L1Ntuple"
jobName = "KeeMC_Yuta"
jobCfg = "run-MC.py"
jobScript = "cmsRun.sh"
rel = "CMSSW_10_2_1"
eosDir = "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/" + os.environ["USER"] + "/condor/" + jobName + "_" + str(ts) + "/"
rootDir = os.environ["CMSSW_BASE"] + "/src/BPHL1Study/L1NtupleProducer/"
jobDir = rootDir + jobName + "_" + str(ts) + "/"
ret = 0
files_batch = 100

fileList = rootDir + "KeeMC_Yuta.list" 

while ret == 0:
   ret = os.system("mkdir -p " + jobDir)
   ret = os.system("mkdir -p " + eosDir)
   ret = os.system("mkdir -p " + jobDir + "out/")
   ret = os.system("mkdir -p " + jobDir + "err/")
   ret = os.system("mkdir -p " + jobDir + "log/")
   ret = os.system("rm " + jobDir + "filelist.tgz")
   ret = os.chdir(os.environ["CMSSW_BASE"]+"/../")
   print('Tarballing ' + rel + "/ into " + jobName + ".tgz...")
   ret = os.system("tar --exclude='L1Ntuple.root' --exclude='ignore' --exclude='.git' " + "-zcf " + jobName + ".tgz " + rel)
   print 'Done!'
   ret = os.system("mv " + jobName + ".tgz " + eosDir) 
   ret = os.chdir(rootDir)
   ret = os.system("cp /tmp/x509up_u93529 /afs/cern.ch/user/x/xuyan/private/x509up/x509up_u93529")
   proxy_path = "/afs/cern.ch/user/x/xuyan/private/x509up/x509up_u93529"
   
   file1 = open(fileList, 'r')
   file_content = file1.readlines()
   chunks = len(file_content) / files_batch + 1
   
   ret = os.system("rm filelist_tmp_*.list")
   for ichunk in range(chunks):
      filelist_name = "filelist_tmp_%i.list" %(ichunk)
      filelist_tmp = open(filelist_name, 'w')
      for file in file_content[ichunk*files_batch:(ichunk+1)*files_batch]:
         filelist_tmp.write(file)
      filelist_tmp.close()
   ret = os.system("tar -cvf filelist.tgz filelist_tmp_*")
   
   with open(jobDir + jobName + '.jdl', 'w') as jdl:
      jdl.write("universe = vanilla\n")
      jdl.write("Executable = " + jobScript + "\n")
      jdl.write("Should_Transfer_Files = YES\n")
      jdl.write("WhenToTransferOutput = ON_EXIT\n")
      jdl.write("Transfer_Input_Files = " + jobScript + ", " + jobCfg + ", filelist.tgz" + ", JSON_dataNtuples.txt" + "\n")
      jdl.write("Output = "    + jobDir + "out/$(ProcId).out\n")
      jdl.write("Error = "     + jobDir + "err/$(ProcId).err\n")
      jdl.write("Log = "       + jobDir + "log/$(ProcId).log\n")
      jdl.write("Arguments = " + eosDir + " " + jobName + " " + rel + " $(ProcId) " + jobCfg + " " + filelist_name + " " + fileName + " " + proxy_path + "\n")
      # jdl.write("+MaxRuntime = 28800\n")
      # jdl.write("on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)\n")
      # jdl.write("max_retries = 3\n")
      # jdl.write("requirements = Machine =!= LastRemoteHost\n")
      jdl.write("Queue " + str(chunks) + "\n")      

   os.system("condor_submit " + jobDir + jobName + ".jdl")
   print str(chunks) + " jobs submitted."
   os.system("condor_q")
   sys.exit(0)

print("Submission failed.")
sys.exit(1)