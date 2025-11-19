#!/usr/bin/env python3
import argparse
import subprocess
import os
from datetime import datetime, timedelta
from pathlib import Path
import re
import json
import shlex
import time

p = argparse.ArgumentParser()
p.add_argument("--threads", "-t", type=int, default=1)
p.add_argument("--procs", "-p", type=int, default=1)
p.add_argument("--athena-mp", action=argparse.BooleanOptionalAction, default=True)
p.add_argument("--events", "-n", type=int, default=10)
p.add_argument("--output", "-o", type=Path, default=None)
p.add_argument("--dry-run", "-s", action="store_true")
p.add_argument("--clustering", choices=["digital", "analog"], default="digital")

args = p.parse_args()

if args.output is None:
    args.output = Path.cwd() / "outputs"

if not args.output.exists():
    args.output.mkdir(parents=True)

max_run = 1
for p in args.output.iterdir():
    if not p.is_dir(): continue

    m = re.match(r"r(\d+)", p.name)
    if m is None: continue

    num, = m.groups()
    max_run = max(max_run, int(num)+1)

run_dir = args.output / f"r{max_run:>03d}"
run_dir = run_dir.resolve()
print(run_dir)

assert not run_dir.exists(), "Output dir exists already"

if not args.dry_run:
    run_dir.mkdir()

#DATADIR=Path(os.environ["DATADIR"])
DATADIR=Path("/mnt/ssd1/pibutti/data/ttbar_PU200/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8481_s4149_r14700")
# Path("/scratch/large/pagessin/power/mc21_14TeV.601229.PhPy8EG_A14_ttbar_hdamp258p75_SingleLep.recon.RDO.e8514_s4345_r15583/")

all_files = list(sorted([p for p in DATADIR.iterdir() if p.is_file()]))

events_per_file = 100 # ?
required_files = max(1, int(args.events / events_per_file))
print("required files:", required_files)


files = all_files[:]


# Ignore specific error messages from Acts CKF
ignore_pattern="Acts.+FindingAlg.+ERROR.+Propagation.+reached.+the.+step.+count.+limit,Acts.+FindingAlg.+ERROR.+Propagation.+failed:.+PropagatorError:..+Propagation.+reached.+the.+configured.+maximum.+number.+of.+steps.+with.+the.+initial.+parameters,Acts.+FindingAlg.Acts.+ERROR.+CombinatorialKalmanFilter.+failed:.+CombinatorialKalmanFilterError:5.+Propagation.+reaches.+max.+steps.+before.+track.+finding.+is.+finished.+with.+the.+initial.+parameters,Acts.+FindingAlg.Acts.+ERROR.+SurfaceError:1,Acts.+FindingAlg.Acts.+ERROR.+failed.+to.+extrapolate.+track"

from AthenaConfiguration.TestDefaults import defaultConditionsTags; 
conditions = defaultConditionsTags.RUN4_MC

env = os.environ.copy()
env.update(
{
               "ATHENA_CORE_NUMBER": str(args.threads),
               "TRF_ECHO": "1",
    })

def make_cmd(events: int, skip: int | None) -> list[str]:
    cmd = [
        "Reco_tf.py",
        "--maxEvents",  str(events), 
    ]

    if skip is not None:
        cmd += ["--skipEvents", str(skip)]

    preExecs = [
        "flags.Tracking.doTruth=False", 
        "flags.Reco.PostProcessing.GeantTruthThinning=False",
        "flags.Output.doGEN_AOD2xAOD=False",
        "flags.Tracking.doVertexFinding=False"
    ]

    if args.clustering == "digital":
        preExecs.append("flags.Tracking.doPixelDigitalClustering=True")

    cmd += [
        "--multithreaded", 'True',
        "--autoConfiguration", 'everything',
        "--conditionsTag", f"all:{conditions}",
        "--geometryVersion", 'all:ATLAS-P2-RUN4-03-00-00',
        "--postInclude",'all:PyJobTransforms.UseFrontier',
        "--preInclude", "InDetConfig.ConfigurationHelpers.OnlyTrackingPreInclude,ActsConfig.ActsCIFlags.actsWorkflowFlags",
        "--preExec", ";".join(preExecs),
        "--steering", 'doRAWtoALL',
        "--inputRDOFile", *(map(str, files)),
        "--outputAODFile", 'myAOD.pool.root',
        "--jobNumber", '1',
        "--ignorePatterns", ignore_pattern,
        "--sharedWriter", "False",
    ]

    return cmd

commands = []

if args.athena_mp:
    print("Running Athena with internal multi-processing")

    cmd = make_cmd(events=args.events, skip=None)

    if args.procs > 1:
        cmd += [
            f'--athenaopts=--nprocs={args.procs:d}'
        ]

    commands.append(cmd)
else:
    print("Running separate athena processes")

    event_start = 0
    events_per_process = args.events // args.procs
    print(events_per_process)


    for i in range(args.procs):
        skip = i*events_per_process
        nevents = events_per_process
        if i == args.procs-1:
            nevents = args.events - skip

        assert nevents > 0

        print(f"{i=} {skip=} {nevents=}", nevents + skip)
        commands.append(make_cmd(events=nevents, skip=skip))

infodict = {
    "run_dir": str(run_dir),
    "commands": commands,
    **{k: str(v) for k, v in vars(args).items()}
}

print(json.dumps(infodict, indent=2))

if not args.dry_run:
    with (run_dir / "info.json").open("wt") as fh:
        json.dump(infodict, fh, indent=2)

start = datetime.now()
print("START", start)

ok = True
print(f"Running {len(commands)} commands")
procs = []

if not args.dry_run:

    for idx, cmd in enumerate(commands):
        cwd = run_dir / f"proc_{idx:>03d}"
        cwd.mkdir()
        print(cwd)

        fh = (cwd/ "out.log").open("w")
        p = subprocess.Popen(cmd, cwd=cwd, env=env, stderr=subprocess.STDOUT, stdout=fh)
        procs.append((p, fh))

    last_print = None
    while any([p.returncode is None for p, _ in procs]):
        for proc, _ in procs:
            proc.poll()

        if last_print is None or (datetime.now() - last_print) > timedelta(seconds=30):
            ndone = len([p  for p, _ in procs if p.returncode is not None])
            print(f"Polling: {ndone} / {len(procs)} done, elapsed time: {datetime.now() - start}")
            last_print = datetime.now()

        time.sleep(0.1)
        

end = datetime.now()
print("END", end)

for proc, fh in procs:
    fh.close()
    if proc.returncode != 0:
        ok = False

print("OK:", ok)

duration = end - start


infodict = {
    "start_wall": f"{start.isoformat()}",
    "end_wall": f"{end.isoformat()}",
    "wall_s": f"{duration.total_seconds()}",
    "ok": ok,
    **infodict,
}

if not args.dry_run:
    with (run_dir / "info.json").open("wt") as fh:
        json.dump(infodict, fh, indent=2)

