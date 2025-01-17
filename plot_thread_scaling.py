import matplotlib.pyplot as plt
from common import io
import numpy as np
import argparse
import glob,sys



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

def getLogInfo(logfile,nthreads):

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


def collectData(folderList,args):

    results={}

    for fld in folderList:
        fldsplit=fld.split("_")
        nthreads = fldsplit[-1]
        
        if "nosmt" in fldsplit:
            nthreads=fldsplit[-2]
        
        logfiles = glob.glob(fld+"/log.RAWtoALL_run_*")
        #print(logfiles,nthreads)

        logInfo=[]
        
        if len(logfiles)>1:

            if not args.avg:
                logInfo = getLogInfo(logfiles[0],nthreads)
                
            else:
                print("Option not supported")
                sys.exit(1)
                #logInfo=getAvgLogInfo(logfiles,nthreads)
        
        else: # only one logfile
            logInfo = getLogInfo(logfiles[0],nthreads)
            
        results[float(nthreads)]=logInfo


    #order by key
    results = dict(sorted(results.items()))
        
    return results
    

def main():

    print("Run thread scaling analysis")
    
    parser = argparse.ArgumentParser(description="Run thread scaling analysis")

    parser.add_argument("-i","--inputdir",type=str, required=False, default="./thread_timing",help="Input directory with the logs")

    parser.add_argument("-a","--avg",required=False,default=False,action="store_true",help="If there are multiple logs for the same point, do the average")
    

    args = parser.parse_args()
    
    print("Looking for folders in " + args.inputdir)
    folders = glob.glob(args.inputdir+"/*threads*")
    
    #Split the collected folders into SMT ON / OFF
    dir_smt = []
    dir_nosmt = []

    for folder in folders:
        if "nosmt" in folder:
            dir_nosmt.append(folder)
        else:
            dir_smt.append(folder)

    
    #print(dir_smt)
    smtResults = collectData(dir_smt,args)

    threads, evt_per_s = getScatterPoints(smtResults,1)
    _, throughput      = getScatterPoints(smtResults,2)
    _, cpu_usage       = getScatterPoints(smtResults,3)
    
    
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
    ideal = 0.313*threads

    
    #ax2 = ax1.twinx()
    #ax2.plot(threads, cpu_usage / 100., color='r',label="cpu_usage")
    #ax2.set_xlabel("n threads")
    #ax2.set_ylabel("CPU usage")
    #ax2.set_ylim(0, 2)
    
    #ax1.legend(loc='upper right')
    #ax2.legend(loc='lower right')


    plt_cfg = {}
    
    

    io.mtlibPlot(threads,[ideal,throughput],
                 titleX="n threads [ AMD EPYC 7413 24-Core / 48-threads ] ",titleY="Throughput Evt/s",
                 xlim=[0,48],
                 legends=["Linear Scaling","SMT ON","SMT OFF"],
                 styles=["--","-","-"]
                 )

    
        
    plt.savefig("my_plot.pdf", format="pdf")
    
    print ("######")
    
    print(dir_nosmt)
    nosmtResults = collectData(dir_nosmt,args)
    

if __name__=="__main__":
    main()













