#!/usr/bin/env athena.py
# Run arguments file auto-generated on Fri Jan 17 11:07:06 2025 by:
# JobTransform: RAWtoALL
# Version: $Id: trfExe.py 792052 2017-01-13 13:36:51Z mavogel $
# Import runArgs class
from PyJobTransforms.trfJobOptions import RunArguments
runArgs = RunArguments()
runArgs.trfSubstepName = 'RAWtoALL' 

runArgs.perfmon = 'fastmonmt'
runArgs.maxEvents = 100
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
runArgs.inputRDOFile = ['/cvmfs/atlas-nightlies.cern.ch/repo/data/data-art/PhaseIIUpgrade/RDO/ATLAS-P2-RUN4-03-00-00/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700/RDO.33629020._000047.pool.root.1']
runArgs.inputRDOFileType = 'RDO'
runArgs.inputRDOFileNentries = 200
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
runArgs.threads = 4
runArgs.concurrentEvents = 4

 # Import skeleton and execute it
from RecJobTransforms.RAWtoALL_Skeleton import fromRunArgs
fromRunArgs(runArgs)
