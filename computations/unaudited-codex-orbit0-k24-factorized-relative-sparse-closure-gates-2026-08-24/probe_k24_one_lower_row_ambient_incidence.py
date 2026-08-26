#!/usr/bin/env python3
"""Exact one-row ambient B20 incidence prefix; a cap, never a closure verdict."""
import argparse
import hashlib
import importlib.util
import json
import os
import resource
from pathlib import Path
from time import perf_counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROVIDER = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-relative-production-gate-2026-08-24/k24_factorized_B20_provider.py"
PROVIDER_SHA = "689499ecf501eb37879b41f05e3f3caecfad454eaf57f5586b28edd7c616a018"
WITNESSES = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/prefix1_fast/literal_witnesses.tsv"
WITNESS_SHA = "477b9ae9249b72d2e1c9ba4c71fd5b63605866ce533c6c79eb199b8103dd001c"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_provider():
    need(sha(PROVIDER) == PROVIDER_SHA, "provider hash")
    spec = importlib.util.spec_from_file_location("k24_one_row_incidence_provider", PROVIDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_frozen_source_word(word):
    return tuple(word) == (word[0], word[0], word[2], word[2], word[4], word[4], word[6], word[6])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    need(not output.exists(), "refuse overwrite")
    need(sha(WITNESSES) == WITNESS_SHA, "witness hash")
    fields = WITNESSES.read_text().splitlines()[1].split("\t")
    need(len(fields) == 24 and fields[2] == "0", "first witness")
    provider = load_provider()
    column = provider.P.parse_column_key(fields[14])
    canonical, orbit_size, *_ = provider.fast_natural_canonical_and_orbit_size(column)
    need(canonical == column and orbit_size == int(fields[15]), "seed natural canonical")
    lower = provider.block_counter(column, 20)
    need(len(lower) == 1 and list(lower.values()) == [1], "one K20 output")
    row = next(iter(lower))
    begun = perf_counter()
    literal_incident = provider.P.D24.incident_degree24_columns(row)
    natural = {}
    for incident in literal_incident:
        representative, size, *_ = provider.fast_natural_canonical_and_orbit_size(incident)
        old = natural.setdefault(representative, size)
        need(old == size, "orbit-size consistency")
    elapsed = perf_counter() - begun
    frozen = sum(is_frozen_source_word(item[0]) for item in natural)
    ambient = len(natural) - frozen
    need(canonical in natural, "seed absent from inverse incidence")
    need(ambient > 0, "hostile restricted 78-word domain unexpectedly complete")
    payload = {
        "status": "PASS_BOUNDED_ONE_K20_ROW_AMBIENT_INCIDENCE_CAP",
        "degree": 24,
        "seed_column": fields[14],
        "seed_column_orbit_size": orbit_size,
        "row_degree": 20,
        "row_hex": row.hex(),
        "literal_incident_columns": len(literal_incident),
        "natural_incident_column_orbits_N": len(natural),
        "incident_orbits_in_frozen_78_source_word_dictionary": frozen,
        "incident_orbits_outside_frozen_78_source_word_dictionary": ambient,
        "seed_self_edge_lower_bound_E": 1,
        "processed_row_orbits": 1,
        "queued_column_orbits": len(natural),
        "closure_status": "ROW_CAP_1_NOT_COMPLETE",
        "lower_transfer_below_K20_complete": False,
        "elapsed_seconds": elapsed,
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "provider_sha256": PROVIDER_SHA,
        "witness_sha256": WITNESS_SHA,
        "hostile_restricted_word_domain_rejected": True,
        "global_verdict": "INCONCLUSIVE_INCOMPLETE_AMBIENT_CLOSURE",
        "scope": "one K20 row-orbit inverse-incidence prefix only; no complete closure or membership claim",
    }
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
