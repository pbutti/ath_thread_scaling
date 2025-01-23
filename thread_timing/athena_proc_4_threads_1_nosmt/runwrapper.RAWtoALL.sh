#!/bin/sh
athena.py --nprocs=4 --preloadlib=$ATLASMKLLIBDIR_PRELOAD/libintlc.so.5:$ATLASMKLLIBDIR_PRELOAD/libimf.so runargs.RAWtoALL.py
