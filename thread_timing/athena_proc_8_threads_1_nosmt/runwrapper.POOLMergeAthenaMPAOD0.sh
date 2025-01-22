#!/bin/sh
# AthenaMT explicitly disabled for this executor
# AthenaMP explicitly disabled for this executor
athena.py --preloadlib=$ATLASMKLLIBDIR_PRELOAD/libimf.so:$ATLASMKLLIBDIR_PRELOAD/libintlc.so.5 runargs.POOLMergeAthenaMPAOD0.py
