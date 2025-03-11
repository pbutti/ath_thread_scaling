import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


from common import io
import numpy as np
import argparse
import glob,sys


from collections import OrderedDict


def getProcScatterPoints(results,index):

    npproc    = []
    npthreads = []
    npy       = []

    for nproc,_ in results.items():
        npproc.append(float(nproc))

        for nt,r in _.items():
            npthreads.append(nt)
            npy.append(r[index])

    return np.array(npproc),np.array(npthreads),np.array(npy)


#This returns a tuple of x/y for the scatter plot
#index is used to select which
def getScatterPoints(results,index):

    npx = []
    npy = []
    for k,v in results.items():
        npx.append(float(k))
        npy.append(v[index])
    
    npx = np.array(npx)
    npy = np.array(npy)
    
    return npx,npy

def getLogInfo(logfile):

    with open(logfile) as f:
        lines = f.readlines()

        #nevents, CPU usage / event [ms], Events / s, CPU eff [%]
        result = []
        
        for line in lines:
            if "Number of events processed:" in line:
                #print(line.split()[-1])
                result.append(float(line.split()[-1]))
            if "CPU usage per event [ms]:" in line:
                #print(line.split()[-1])
                result.append(float(line.split()[-1]))
            if "Events per second:" in line:
                #print(line.split()[-1])
                result.append(float(line.split()[-1]))
            if "CPU utilization efficiency [%]:" in line:
                #print(line.split()[-1])
                result.append(float(line.split()[-1]))
            
    return result


def collectProcData(folderList,args):
    logdata = {}
    results = {}

    #print("collectProcData",folderList)
    
    nproc=1
    nthreads=1

    logdata[nproc] = {}
    
    for fld in folderList:
        fldsplit = fld.split("_")

        if "smt" not in fldsplit:
            nthreads = int(fldsplit[-1])
            nproc    = int(fldsplit[-3])
        else:
            nthreads = int(fldsplit[-2])
            nproc    = int(fldsplit[-4])

        if not args.doThreads:
            logdata[nproc] = {}
            logdata[nproc][nthreads]=glob.glob(fld+"/athenaMP-workers-RAWtoALL-r2a/worker*/AthenaMP.log")
        else:

            logdata[nproc][nthreads]=glob.glob(fld+"/log.RAWtoALL_run_0")
        

    # Step 1: Sort the outer dictionary by nproc
    sorted_data = OrderedDict(sorted(logdata.items()))

    # Step 2: Sort each inner dictionary by nthread
    for nproc, threads in sorted_data.items():
        sorted_data[nproc] = OrderedDict(sorted(threads.items()))

    logdata = sorted_data
        
    
    for nproc, threads in logdata.items():

        results[nproc]={}
        
        for nt, logs in threads.items():

            #print(nproc,nt)

            aggdata = np.array([0.,0.,0.,0])
            
            
            for log in logs:
                reslog = np.array(getLogInfo(log))  
                aggdata += reslog
                #print(reslog)

            #aggdata[1]/=len(logs)
            #aggdata[2]/=len(logs)
            #aggdata[3]/=len(logs)
            
            #print(aggdata)
            results[nproc][nt]=aggdata

    return results

# deprecated
def collectData(folderList,args):

    results={}

    for fld in folderList:
        fldsplit=fld.split("_")
        nthreads = fldsplit[-1]

        if "legacy" in fldsplit:
            nthreads = fldsplit[-2]
            if ("nosmt" in fldsplit):
                print(fldsplit)
                nthreads = fldsplit[-3]
        else:
            if "nosmt" in fldsplit:
                nthreads=fldsplit[-2]
        
        logfiles = glob.glob(fld+"/log.RAWtoALL_run_*")
        print(logfiles,nthreads)

        logInfo=[]
        
        if len(logfiles)>1:

            if not args.avg:
                logInfo = getLogInfo(logfiles[0])
                
            else:
                print("Option not supported")
                sys.exit(1)
                #logInfo=getAvgLogInfo(logfiles,nthreads)
        
        else: # only one logfile
            logInfo = getLogInfo(logfiles[0])
            
        results[float(nthreads)]=logInfo


    #order by key
    results = dict(sorted(results.items()))
        
    return results


def analyseAthenaMT(folders,args):

    
    #Split the collected folders into SMT ON / OFF
    dir_smt = []
    dir_nosmt = []
    dir_smt_legacy = []
    dir_nosmt_legacy = []

    for folder in folders:

        if "legacy" in folder:
            if "nosmt" in folder:
                dir_nosmt_legacy.append(folder)
            else:
                dir_smt_legacy.append(folder)
                
        else:
            if "nosmt" in folder:
                dir_nosmt.append(folder)
            else:
                dir_smt.append(folder)

    
    #print(dir_smt)
    smtResults = collectData(dir_smt,args)
    
    threads, evt_per_s = getScatterPoints(smtResults,1)
    _, throughput      = getScatterPoints(smtResults,2)
    _, cpu_usage       = getScatterPoints(smtResults,3)


    
    nosmtResults = collectData(dir_nosmt,args)
        
    _,evt_per_s_nosmt        = getScatterPoints(nosmtResults,1)
    _, throughput_nosmt      = getScatterPoints(nosmtResults,2)


    smtLegacyResults = collectData(dir_smt_legacy,args)
    _,evt_per_s_smt_legacy        = getScatterPoints(smtLegacyResults,1)
    _, throughput_smt_legacy      = getScatterPoints(smtLegacyResults,2)

    nosmtLegacyResults = collectData(dir_nosmt_legacy,args)
    _,evt_per_s_nosmt_legacy        = getScatterPoints(nosmtLegacyResults,1)
    _, throughput_nosmt_legacy      = getScatterPoints(nosmtLegacyResults,2)

    
    #print(threads)
    #print(evt_per_s)
    #print(throughput)
    #print(cpu_usage)    

    #fig = plt.figure()
    #ax1 = fig.add_subplot(1,1,1)
    #ax1.plot(threads, throughput, label="throughput")
    #ax1.set_xlabel("n threads")
    #ax1.set_ylabel("Throughput (Evt/s)")
    #ax1.set_ylim(0, 15)

    #Add a straight line with slope = troughput for 1 thread (0.313s)
    ideal = 0.31*threads

    
    #ax2 = ax1.twinx()
    #ax2.plot(threads, cpu_usage / 100., color='r',label="cpu_usage")
    #ax2.set_xlabel("n threads")
    #ax2.set_ylabel("CPU usage")
    #ax2.set_ylim(0, 2)
    
    #ax1.legend(loc='upper right')
    #ax2.legend(loc='lower right')


    plt_cfg = {}
    

    allplotlines=[ideal,throughput,throughput_nosmt,throughput_smt_legacy,throughput_nosmt_legacy]

    return threads,ideal,throughput,throughput_nosmt,throughput_smt_legacy,throughput_nosmt_legacy



def analyseAthenaMP(folders,args):

    #Split the collected folders into SMT ON / OFF
    dir_smt = []
    dir_nosmt = []
    dir_smt_legacy = []
    dir_nosmt_legacy = []
    

    for folder in folders:

        if "legacy" in folder:
            if "nosmt" in folder:
                dir_nosmt_legacy.append(folder)
            else:
                dir_smt_legacy.append(folder)
                
        else:
            if "nosmt" in folder:
                dir_nosmt.append(folder)
            else:
                dir_smt.append(folder)

    print("collecting proc data from")
    
    print("NO SMT")
    print(dir_nosmt)
    print("SMT")
    print(dir_smt)
    
    
    #nosmtResults = collectProcData(dir_nosmt,args)
    
    smtResults = collectProcData(dir_smt,args)

    print("SMT RESULTS")
    print(smtResults)
    
    procs, threads, throughputMP = getProcScatterPoints(smtResults,2)
    print(procs,threads,throughputMP)
    
    return procs,threads,throughputMP
    
def main():

    print("Run thread scaling analysis")
    
    parser = argparse.ArgumentParser(description="Run thread scaling analysis")

    parser.add_argument("-i","--inputdir",type=str, required=False, default="./thread_timing",help="Input directory with the logs")

    parser.add_argument("-a","--avg",required=False,default=False,action="store_true",help="If there are multiple logs for the same point, do the average")

    parser.add_argument("-t","--doThreads",required=False,default=False,action="store_true",help="Process thread logs or process logs")
    
    parser.add_argument("-d","--dry",required=False,default=False,action="store_true",help="Dry run")

    
    args = parser.parse_args()
    
    folders = glob.glob(args.inputdir+"/*proc*threads*")

    print("Procesing folders...")
    print(folders)

    procs, threads, throughput  = analyseAthenaMP(folders,args)

    #folders = glob.glob(args.inputdir+"/*threads*")
    #sel_folders = []
    
    #for fld in folders:
    #    if "proc" not in fld:
    #        sel_folders.append(fld)
            
    #threads, ideal,throughput,throughput_nosmt,throughput_smt_legacy,throughput_nosmt_legacy = analyseAthenaMT(sel_folders,args)
    
    threads = np.array([ 1  2  4  8 16 24])
    MP = np.array([0.307 ,0.621 ,1.241 ,2.462, 4.648, 6.457])
    MT = np.array([0.302 ,0.597 ,1.099 ,2.002, 3.4  , 4.218])
    ideal = 0.307*threads
    #Combined plot    

    io.mtlibPlot(threads,[ideal,MT,MP],
                 titleX="n threads / n proc [ AMD EPYC 7413 24-Core / 48-threads ] ",titleY="Throughput Evt/s",
                 xlim=[0,24],
                 legends=["Linear Scaling","Acts Tracking MT", "Acts Tracking MP"],
                 styles=["--","-","-","-","-","-"],colors=['blue','orange','green','red','indigo','black']
                 )

    plt.savefig("thread_nproc_amd_scaling.pdf", format="pdf")




    #ARM
    
    #MP=np.array([0.124, 3.956,  7.822, 14.997, 20.714])
    #threads =np.array([ 1., 32.,  64., 128., 192.])
    #ideal = 0.124*threads


    #io.mtlibPlot(threads,[ideal,MP],
    #             titleX="n threads [ ARM UnicornMachine 192-Core] ",titleY="Throughput Evt/s",
    #             xlim=[0,200],
    #             legends=["Linear Scaling","Athena with Acts FT MP"],
    #             styles=["--","-","-","-","-","-"],colors=['blue','orange','green','red','indigo','black'] )
        
    #plt.savefig("arm_scaling.pdf", format="pdf")

    if not args.dry:
    
        threads = np.array([  1,   2,   4,   8,  16,  32,  64, 128])
        ARM_MT      = np.array([0.131, 0.222, 0.365, 0.52,  0.562, 0.553, 0.533, 0.517])
        ideal_t = 0.131*threads

        procs  = np.array([  1. ,   32.,  64. , 128.  , 192.])
        ARM_MP = np.array([0.131,   3.956, 7.822, 14.997, 20.714])

        ideal   = 0.131*procs
        
        #io.mtlibPlot([procs,threads,procs],[ideal,ARM_MT,ARM_MP],
        #             titleX="n threads [ ARM UnicornMachine 192-Core] ",titleY="Throughput Evt/s",
        #             xlim=[0,200],
        #             legends=["Linear Scaling","Athena with Acts FT MT"],
        #             styles=["--","-","-","-","-","-"],colors=['blue','orange','green','red','indigo','black'] )


        fig = plt.figure()
        gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])
        ax1 = fig.add_subplot(gs[0, 0])

        ax1.grid(True)
        ax1.xaxis.set_major_locator(MaxNLocator(nbins=12))
        ax1.plot(threads,ARM_MT,linestyle="-",label="Athena with Acts FT MT",color="blue")
        ax1.plot(procs,ARM_MP,  linestyle="-",label="Athena with Acts FT MP",color="green")
        ax1.plot(procs,ideal, linestyle="--",label="Linear Scaling",color="black")
        
        ax1.legend()
        ax1.set_ylabel("Throughput Evt/s")
        ax1.set_xlabel("Processes / Threads")
        
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.xaxis.set_major_locator(MaxNLocator(nbins=12))
        ax2.set_yticks(np.arange(0, 1.25, 0.25))
        ax2.grid(True)

        # Adjust layout to prevent overlap
        fig.subplots_adjust(hspace=0.3)  # Increase space between subplots
        
        
    
        ratio_t = ARM_MT / ideal_t
        ratio_p = ARM_MP / ideal
                
        ax2.plot(threads,ratio_t,color="blue")
        ax2.plot(procs,ratio_p,color="green")


        plt.savefig("arm_scaling.pdf", format="pdf")
        
if __name__=="__main__":
    main()













