#!/usr/bin/env python3
"""UNAUDITED PROBE (W1) -- turn the result JSONs into the report tables.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01
Usage: python3 analyse_w1.py [--push results_push.json] ...
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import os

from run_w1_push import verdict


def load(path):
    """The summary JSON if the run finished, else the incremental JSONL."""
    if os.path.exists(path):
        with open(path) as handle:
            return json.load(handle)
    if os.path.exists(path + ".jsonl"):
        rows = [json.loads(line) for line in open(path + ".jsonl")
                if line.strip()]
        return {"summary": {"partial": True, "rows": len(rows)},
                "results": rows,
                "table": [verdict(row) for row in rows
                          if "base" in row and "prefix" in row]}
    return None


def percent(value):
    return "-" if value is None else f"{100 * value:.1f}%"


def verdict_table(push):
    lines = ["| shadow | stratum | base sat | base sing | witness onset (k, sat) "
             "| stall sat (wit/live) | stall sing | stall noncoord "
             "| blocked frontier sat (live) | no-death frontier sat "
             "| decoord blocked |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for row in push["table"]:
        onset = ("-" if row["witness_onset_k"] is None
                 else f"k={row['witness_onset_k']} "
                      f"({percent(row['witness_onset_fraction'])})")
        lines.append(
            f"| {row['id']} | {row['stratum']} "
            f"| {percent(row['base_fraction'])} | {row['base_singletons']} "
            f"| {onset} "
            f"| {percent(row['cycle_fraction'])} "
            f"({row['cycle_witness']}/{row['cycle_live']}) "
            f"| {row['cycle_singletons']} | {row['cycle_noncoordinate']} "
            f"| {percent(row.get('frontier_fraction'))} "
            f"({row.get('frontier_live')}) "
            f"| {percent(row.get('nodeath_fraction'))} "
            f"| {row['decoord_all_blocked']}/{row['decoord_trials']} |")
    return "\n".join(lines)


def push_summary(push):
    table = push["table"]
    out = {
        "shadows": len(table),
        "class_counts": dict(Counter(row["class"] for row in table)),
        "base_all_coordinate": sum(1 for row in table
                                   if row["base_noncoordinate"] == 0),
        "base_fraction_range": [min(row["base_fraction"] for row in table),
                                max(row["base_fraction"] for row in table)],
        "base_singleton_range": [min(row["base_singletons"] for row in table),
                                 max(row["base_singletons"] for row in table)],
        "witness_onset_k": dict(Counter(row["witness_onset_k"] for row in table)),
        "witness_onset_fraction_range": [
            min(row["witness_onset_fraction"] for row in table
                if row["witness_onset_fraction"] is not None),
            max(row["witness_onset_fraction"] for row in table
                if row["witness_onset_fraction"] is not None)],
        "witness_onset_share_of_violated": [
            min(row["witness_onset_of_violated"] for row in table
                if row["witness_onset_of_violated"] is not None),
            max(row["witness_onset_of_violated"] for row in table
                if row["witness_onset_of_violated"] is not None)],
        "stall_fraction_range": [min(row["cycle_fraction"] for row in table),
                                 max(row["cycle_fraction"] for row in table)],
        "stall_witness_range": [min(row["cycle_witness"] for row in table),
                                max(row["cycle_witness"] for row in table)],
        "stall_all_blocked": sum(1 for row in table if row["cycle_witness"] == 0),
        "stall_live_range": [min(row["cycle_live"] for row in table),
                             max(row["cycle_live"] for row in table)],
        "frontier_fraction_range": [
            min(row["frontier_fraction"] for row in table
                if "frontier_fraction" in row),
            max(row["frontier_fraction"] for row in table
                if "frontier_fraction" in row)],
        "nodeath_fraction_range": [
            min(row["nodeath_fraction"] for row in table
                if "nodeath_fraction" in row),
            max(row["nodeath_fraction"] for row in table
                if "nodeath_fraction" in row)],
        "nodeath_singletons_range": [
            min(row["nodeath_singletons"] for row in table
                if "nodeath_singletons" in row),
            max(row["nodeath_singletons"] for row in table
                if "nodeath_singletons" in row)],
        "nodeath_noncoordinate": dict(Counter(
            row["nodeath_noncoordinate"] for row in table
            if "nodeath_noncoordinate" in row)),
        "decoordination_survival": [
            sum(row["decoord_all_blocked"] for row in table),
            sum(row["decoord_trials"] for row in table)],
        "noncoordinate_frontier_fractions": sorted(
            value for row in table
            for value in row.get("nc_frontier_fractions", [])),
    }
    arithmetic = Counter()
    undecided = 0
    for record in push["results"]:
        for key in ("base", "cycle", "frontier", "frontier_nodeath"):
            entry = record.get(key)
            if not entry:
                continue
            block = entry.get("blocking") or entry.get("final", {}).get("blocking")
            if not block:
                continue
            arithmetic.update(block["arithmetic"])
            undecided += len(block["undecided_pairs"])
    out["arithmetic"] = dict(arithmetic)
    out["undecided_pairs_total"] = undecided
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--push", default="results_push.json")
    parser.add_argument("--nearexact", default="results_nearexact.json")
    parser.add_argument("--slice", dest="slice_path", default="results_slice.json")
    parser.add_argument("--falsifier", default="results_falsifier.json")
    parser.add_argument("--monomial", default="results_monomial.json")
    args = parser.parse_args()

    push = load(args.push)
    if push:
        print("## Per-shadow verdict table\n")
        print(verdict_table(push))
        print("\n## Push summary\n")
        print(json.dumps(push_summary(push), indent=1))
    for name, path in (("near-exact census", args.nearexact),
                       ("colour slices", args.slice_path),
                       ("falsifier hunt", args.falsifier),
                       ("monomial regime", args.monomial)):
        data = load(path)
        if data:
            print(f"\n## {name}\n")
            print(json.dumps(data["summary"], indent=1))


if __name__ == "__main__":
    main()
