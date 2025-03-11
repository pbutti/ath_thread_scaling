#!/usr/bin/env athena.py
# Run arguments file auto-generated on Wed Jan 22 13:08:10 2025 by:
# JobTransform: POOLMergeAthenaMPAOD0
# Version: $Id: trfExe.py 792052 2017-01-13 13:36:51Z mavogel $
# Import runArgs class
from PyJobTransforms.trfJobOptions import RunArguments
runArgs = RunArguments()
runArgs.trfSubstepName = 'POOLMergeAthenaMPAOD0' 

runArgs.perfmon = 'fastmonmt'
runArgs.autoConfiguration = ['everything']
runArgs.conditionsTag = 'OFLCOND-MC21-SDR-RUN4-02'
runArgs.geometryVersion = 'ATLAS-P2-RUN4-03-00-00'
runArgs.postInclude = ['PyJobTransforms.UseFrontier']
runArgs.preInclude = ['InDetConfig.ConfigurationHelpers.OnlyTrackingPreInclude', 'ActsConfig.ActsCIFlags.actsAloneFastWorkflowFlags']
runArgs.postExec = ['cfg.getService("AlgResourcePool").CountAlgorithmInstanceMisses = True;']
runArgs.jobNumber = 1
runArgs.multithreaded = True

# Explicitly added to process all events in this step
runArgs.maxEvents = -1

 # Input data
runArgs.inputPOOL_MRG_INPUTFile = ['myAOD.pool.root_001', 'myAOD.pool.root_002', 'myAOD.pool.root_003', 'myAOD.pool.root_004', 'myAOD.pool.root_005', 'myAOD.pool.root_006', 'myAOD.pool.root_007', 'myAOD.pool.root_008', 'myAOD.pool.root_009', 'myAOD.pool.root_010', 'myAOD.pool.root_011', 'myAOD.pool.root_012', 'myAOD.pool.root_013', 'myAOD.pool.root_014', 'myAOD.pool.root_015', 'myAOD.pool.root_016']
runArgs.inputPOOL_MRG_INPUTFileType = 'AOD'
runArgs.inputPOOL_MRG_INPUTFileNentries = 2400
runArgs.POOL_MRG_INPUTFileIO = 'input'

 # Output data
runArgs.outputPOOL_MRG_OUTPUTFile = 'myAOD.pool.root'
runArgs.outputPOOL_MRG_OUTPUTFileType = 'AOD'

 # Extra runargs

 # Extra runtime runargs

 # Literal runargs snippets

 # Executor flags
runArgs.totalExecutorSteps = 0

 # Threading flags
runArgs.nprocs = 0
runArgs.threads = 0
runArgs.concurrentEvents = 0

 # Import skeleton and execute it
from RecJobTransforms.MergePool_Skeleton import fromRunArgs
fromRunArgs(runArgs)
