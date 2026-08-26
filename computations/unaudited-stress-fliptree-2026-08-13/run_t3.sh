#!/bin/sh
# T3/T3b need the committed constructors.  Build a snapshot of the pinned HEAD:
#   mkdir run && cd run
#   git -C <repo> archive $(cat ../PINNED_HEAD.txt) | tar -x
#   cp <repo>/computations/unaudited-repair1-k-chain-map-2026-08-13/common.py .
#   cp ../fliptree_lib.py ../t3_k8.py ../t3b_exit.py .
#   cp ../PINNED_HEAD.txt .
#   python3 t3_k8.py && python3 t3b_exit.py
