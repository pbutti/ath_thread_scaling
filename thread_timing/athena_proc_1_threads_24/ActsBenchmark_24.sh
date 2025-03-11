#!/usr/bin/bash


ignore_pattern="Acts.+FindingAlg.+ERROR.+Propagation.+reached.+the.+step.+count.+limit,Acts.+FindingAlg.+ERROR.+Propagation.+failed:.+PropagatorError:3.+Propagation.+reached.+the.+configured.+maximum.+number.+of.+steps.+with.+the.+initial.+parameters,Acts.+FindingAlg.Acts.+ERROR.+CombinatorialKalmanFilter.+failed:.+CombinatorialKalmanFilterError:5.+Propagation.+reaches.+max.+steps.+before.+track.+finding.+is.+finished.+with.+the.+initial.+parameters,Acts.+FindingAlg.Acts.+ERROR.+SurfaceError:1,Acts.+FindingAlg.Acts.+ERROR.+failed.+to.+extrapolate.+track"

DATADIR="/mnt/ssd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700" 

export TRF_ECHO=1 
export ATHENA_CORE_NUMBER=24 
echo "ATHENA_CORE_NUMBER=" ${ATHENA_CORE_NUMBER} 


cd ./thread_timing/athena_proc_1_threads_24

Reco_tf.py \
--maxEvents  2400 \
--autoConfiguration 'everything' \
--conditionsTag 'all:OFLCOND-MC21-SDR-RUN4-02' \
--geometryVersion 'all:ATLAS-P2-RUN4-03-00-00' \
--postInclude 'all:PyJobTransforms.UseFrontier' \
--preInclude 'InDetConfig.ConfigurationHelpers.OnlyTrackingPreInclude,ActsConfig.ActsCIFlags.actsFastWorkflowFlags' \
--steering 'doRAWtoALL' \
--postExec 'all:cfg.getService("AlgResourcePool").CountAlgorithmInstanceMisses = True;' \
--inputRDOFile ${DATADIR}"/*" \
--outputAODFile 'myAOD.pool.root' \
--jobNumber '1' \
--ignorePatterns "${ignore_pattern}" \
--multithreaded 


cd -