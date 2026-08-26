#!/bin/zsh
set -euo pipefail

repo=/Users/rishi/workplace/krenn-conjecture
exporter="$repo/computations/unaudited-codex-orbit0-k18-three-stream-exporters-2026-08-23/export_k18_parent_profiles"
out="$repo/computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23"
key_cap=250000
max_jobs=8

mkdir -p "$out"

typeset -a pids
typeset -a labels
for start in {0..480..32}; do
  end=$((start + 32))
  if (( end > 485 )); then end=485; fi
  prefix="$out/k14_${start}_${end}"
  "$exporter" k14 "$start" "$end" 0 "$key_cap" "$prefix" \
    > "$prefix.stdout.json" 2> "$prefix.stderr.log" &
  pids+=("$!")
  labels+=("$start:$end")
  if (( ${#pids} == max_jobs )); then
    for i in {1..${#pids}}; do
      wait "${pids[$i]}" || { print -u2 "FAILED ${labels[$i]}"; exit 1; }
    done
    pids=()
    labels=()
  fi
done
if (( ${#pids} > 0 )); then
  for i in {1..${#pids}}; do
    wait "${pids[$i]}" || { print -u2 "FAILED ${labels[$i]}"; exit 1; }
  done
fi
print "PASS_ALL_16_EXPORT_SHARDS"
