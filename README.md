# ath_thread_scaling

## Example

Setup athena first and source setup script from build folder, then run


```
python run_thread_scaling.py -v -m 48 -n 1
```

## Run from the test.py
```
setupATLAS
asetup Athena,25.0.45
athena test.py -o test_thread_timing_nov_25 -p 1 -t 8 -n 100
```
