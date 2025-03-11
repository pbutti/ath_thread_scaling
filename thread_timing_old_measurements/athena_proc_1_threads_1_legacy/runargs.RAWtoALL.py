#!/usr/bin/env athena.py
# Run arguments file auto-generated on Thu Feb 13 12:36:11 2025 by:
# JobTransform: RAWtoALL
# Version: $Id: trfExe.py 792052 2017-01-13 13:36:51Z mavogel $
# Import runArgs class
from PyJobTransforms.trfJobOptions import RunArguments
runArgs = RunArguments()
runArgs.trfSubstepName = 'RAWtoALL' 

runArgs.perfmon = 'fastmonmt'
runArgs.maxEvents = 1000
runArgs.autoConfiguration = ['everything']
runArgs.conditionsTag = 'OFLCOND-MC21-SDR-RUN4-02'
runArgs.geometryVersion = 'ATLAS-P2-RUN4-03-00-00'
runArgs.postInclude = ['PyJobTransforms.UseFrontier']
runArgs.preInclude = ['InDetConfig.ConfigurationHelpers.OnlyTrackingPreInclude']
runArgs.preExec = ['ConfigFlags.Tracking.doITkFastTracking=True']
runArgs.postExec = ['cfg.getService("AlgResourcePool").CountAlgorithmInstanceMisses = True;']
runArgs.jobNumber = 1
runArgs.multithreaded = True

 # Input data
runArgs.inputRDOFile = ['/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000002.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000007.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000008.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000014.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000016.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000017.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000018.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000027.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000031.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000036.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000037.pool.root.1', '/mnt/hdd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000038.pool.root.1']
runArgs.inputRDOFileType = 'RDO'
runArgs.inputRDOFileNentries = 2400
runArgs.RDOFileIO = 'input'

 # Output data
runArgs.outputAODFile = 'myAOD.pool.root'
runArgs.outputAODFileType = 'AOD'

 # Extra runargs

 # Extra runtime runargs

 # Literal runargs snippets

 # Executor flags
runArgs.totalExecutorSteps = 0

 # Threading flags
runArgs.nprocs = 0
runArgs.threads = 1
runArgs.concurrentEvents = 1

 # Import skeleton and execute it
from RecJobTransforms.RAWtoALL_Skeleton import fromRunArgs
fromRunArgs(runArgs)
