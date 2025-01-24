
import os,sys
import argparse
import subprocess
import itertools


def prepareJobScript(outfolder,nthreads,args):

    nevents=args.maxevents * ntrheads
    legacy=args.legacy
    outf=outfolder+"/ActsBenchmark_"+str(nthreads)+".sh"
    
    with open(outf, "w") as f:

        f.write("#!/usr/bin/bash\n\n\n")
        f.write('ignore_pattern="Acts.+FindingAlg.+ERROR.+Propagation.+reached.+the.+step.+count.+limit,Acts.+FindingAlg.+ERROR.+Propagation.+failed:.+PropagatorError:3.+Propagation.+reached.+the.+configured.+maximum.+number.+of.+steps.+with.+the.+initial.+parameters,Acts.+FindingAlg.Acts.+ERROR.+CombinatorialKalmanFilter.+failed:.+CombinatorialKalmanFilterError:5.+Propagation.+reaches.+max.+steps.+before.+track.+finding.+is.+finished.+with.+the.+initial.+parameters,Acts.+FindingAlg.Acts.+ERROR.+SurfaceError:1,Acts.+FindingAlg.Acts.+ERROR.+failed.+to.+extrapolate.+track"\n\n')
        #f.write("DATADIR=\"/cvmfs/atlas-nightlies.cern.ch/repo/data/data-art/PhaseIIUpgrade/RDO\" \n\n")  #Single File

        #Full PU Truth, larger file, higher IO, slower processing time, PU200
        #f.write("DATADIR=\"/home/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14701\" \n\n")

        #HS PU Only, smaller file, lower IO, faster processing time, PU200
        f.write("DATADIR=\"/home/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700\" \n\n")
        
        f.write("export TRF_ECHO=1 \n")
        f.write("export ATHENA_CORE_NUMBER="+str(nthreads)+" \n")
        
        f.write('echo "ATHENA_CORE_NUMBER=" ${ATHENA_CORE_NUMBER} \n\n\n')

        f.write("cd "+outfolder+"\n\n")


        
        preInclude = "--preInclude 'InDetConfig.ConfigurationHelpers.OnlyTrackingPreInclude' \\\n"
        preExec    = "--preExec 'all:ConfigFlags.Tracking.doITkFastTracking=True' \\\n"
        multiproc  = ""

        if args.nproc > 1:
            multiproc="--athenaopts=\"--nprocs="+str(args.nproc)+"\" \\\n"

        #For ACTS
        if not legacy:
            preInclude = "--preInclude 'InDetConfig.ConfigurationHelpers.OnlyTrackingPreInclude,ActsConfig.ActsCIFlags.actsAloneFastWorkflowFlags' \\\n"
            preExec=""
        
        f.write("Reco_tf.py \\\n"
                + "--maxEvents  "+str(nevents)+" \\\n"
                + "--autoConfiguration 'everything' \\\n"
                + "--conditionsTag 'all:OFLCOND-MC21-SDR-RUN4-02' \\\n"
                + "--geometryVersion 'all:ATLAS-P2-RUN4-03-00-00' \\\n"
                + "--postInclude 'all:PyJobTransforms.UseFrontier' \\\n"
                + preInclude
                + "--steering 'doRAWtoALL' \\\n"
                + preExec
                + "--postExec 'all:cfg.getService(\"AlgResourcePool\").CountAlgorithmInstanceMisses = True;' \\\n"
                + "--inputRDOFile ${DATADIR}\"/*\" \\\n"
                +"--outputAODFile 'myAOD.pool.root' \\\n"
                +"--jobNumber '1' \\\n"
                +"--ignorePatterns \"${ignore_pattern}\" \\\n"
                + multiproc
                +"--multithreaded \n\n\n")
        
        f.write("cd -")


def geo_progression(start, ratio=2, limit=48):
    progression = []
    term = start
    while term <= limit:
        progression.append(term)
        term *= ratio
    if not limit in progression:
        progression.append(limit)
        
    return progression


# /software/modules/sw/core/likwid/5.2/bin/likwid-topology
# p is the process number, n is the thread number
def make_thread_list(p, n, smt=True):

    thread_lists = []

    #if number of processes is set as <=0 by mistake, put it to 1 
    if p<=0:
        p=1

    # total threads are split in between processes and 
    total_threads = p * n

    if (n > 24):
        print("Running with processes=",p,"and threads=",n," is not supported because is more than 24 threads in parallel")
        sys.exit(1)
    
    if smt:
        thread_lists = list(itertools.chain.from_iterable([(6 * j + i) % 48, (6 * j + i + 24) % 48] for i in range(6) for j in range(4)))
    
    else:
        thread_lists = [(6 * j + i) % 48 for i in range(6) for j in range(4)]
                           
    threads_str  = ",".join(str(x) for x in thread_lists[:total_threads])
    
    
    return(threads_str)
    

def runJob(jobfile,threads, args):

    nosmt=args.nosmt
    subprocess.run(['chmod','u+x',jobfile])
    threads_str = make_thread_list(args.nproc, threads, not nosmt)
    
    
    command=['taskset','-c',threads_str,jobfile]
    print(command)
    
    if not args.dry:
        subprocess.run(command)


def main():

    # Create the parser
    parser = argparse.ArgumentParser(description="Run thread scaling for Athena.")

    # Add arguments

    parser.add_argument('-n', '--minthreads', type=int, required=False, default=1, help="The minimum number of threads")
    parser.add_argument('-m', '--maxthreads', type=int, required=True, help="The maximum number of threads")

    parser.add_argument("-s", '--nosmt', required=False, action="store_true", help="Switch off SMT / HT")
    
    parser.add_argument("-d", '--dry', required=False, action="store_true", help="Dry run. Do not execute the commands")

    parser.add_argument("-v", '--verbose', required=False, help="Toggle verbosity",action="store_true")

    parser.add_argument("-e", '--maxevents', type=int, required=False, default=100, help="Max number of events per thread")

    parser.add_argument("-o", '--outputpath', type=str, required=False, default="./thread_timing/", help="output path")

    parser.add_argument("-r", "--runs",type=int, required=False, default=1,help="Number of runs for each data point")

    parser.add_argument("-l", "--legacy", required=False, default=False, action="store_true", help="Run legacy tracking instead")

    parser.add_argument("-p", "--nproc", required=False, default=1, type=int, help="How many processes to run with")
    
    # Parse the arguments
    args = parser.parse_args()

    # Create the thread list
    threads = geo_progression(args.minthreads, 2, args.maxthreads)

    path = args.outputpath

    if (args.verbose):
        print("Setting up jobs with following thread list: ",threads)

    #For each thread configuration make a folder, setup the RecoTf script and run

        
    for tc in threads:
        
        outfolder = path+"athena_proc_"+str(args.nproc)+"_threads_"+str(tc)

        if (args.legacy):
            outfolder = outfolder+"_legacy"
            
        if (args.nosmt):
            outfolder = outfolder+"_nosmt"

        if not os.path.exists(outfolder):
            os.makedirs(outfolder)

        outfile = outfolder+"/ActsBenchmark_"+str(tc)+".sh"
        prepareJobScript(outfolder, tc, args)
        
        #Run the measurement for each
            
        for run in range(args.runs):
            print("#########")
            print("Running run "+str(run)+"/"+str(args.runs)+" for thread "+str(tc) + " with SMT=", not args.nosmt)
            print("#########")
                  
            runJob(outfile,tc,args)


            if (os.path.isfile(outfolder+"/log.RAWtoALL")):
                os.rename(outfolder+"/log.RAWtoALL", outfolder+"/log.RAWtoALL_run_"+str(run))
            else:
                print("Log file", outfolder+"/log.RAWtoALL", "not found")
            
            

if __name__=="__main__":
    main()
