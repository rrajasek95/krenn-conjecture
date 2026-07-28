#!/usr/bin/env python3
"""One-time cofactor certificates for unit Singular ideals.

For a characteristic-zero ideal I = (g_1, ..., g_m) whose reduced Groebner
basis is [1], Singular's lift returns cofactors T with sum T_i g_i = 1.
That single identity is a self-contained unit certificate: re-verifying it
needs only polynomial arithmetic, no Groebner basis.  This module

* generates certificates: runs slimgb once, checks [1], lifts, and stores
  the cofactors (as Singular polynomial strings) plus SHA-256 stamps of
  the generator list in a JSON artifact;
* verifies certificates: rebuilds the ring, evaluates sum T_i g_i - 1,
  and asserts literal zero, in seconds.

The generator list is hashed in order; a verifier that recomputes the
generators from source must reproduce the identical strings, so the
certificate cannot drift silently away from the audited programs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import time


def run_singular(program, timeout=28800):
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    completed = subprocess.run(
        [singular, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    return completed.stdout


def parse_ring_and_generators(program):
    """Extract the ring line and generator strings from a packet program."""
    lines = program.splitlines()
    ring_line = next(line for line in lines if line.startswith("ring "))
    ideal_line = next(line for line in lines if line.startswith("ideal I="))
    generators = ideal_line[len("ideal I="):].rstrip(";").split(",")
    return ring_line, generators


def generators_sha(generators):
    return hashlib.sha256("\n".join(generators).encode()).hexdigest()


def generate_certificate(name, program, timeout=28800):
    """Run slimgb + lift once and return the certificate record."""
    ring_line, generators = parse_ring_and_generators(program)
    started = time.monotonic()
    script = ring_line + "\n"
    script += "option(redSB);\n"
    script += "ideal I=" + ",".join(generators) + ";\n"
    script += "ideal G=slimgb(I);\n"
    script += 'print("UNIT"); if(G[1]==1){1;}else{0;}\n'
    script += "matrix T=lift(I,ideal(1));\n"
    script += 'print("NROWS"); nrows(T);\n'
    script += 'print("COFACTORS");\n'
    script += "for(int i=1;i<=nrows(T);i++){print(string(T[i,1]));}\n"
    script += 'print("ENDCOFACTORS");\n'
    output = run_singular(script, timeout)
    lines = [line.rstrip() for line in output.splitlines()]
    unit = int(lines[lines.index("UNIT") + 1])
    assert unit == 1, (name, "not unit")
    nrows = int(lines[lines.index("NROWS") + 1])
    start = lines.index("COFACTORS") + 1
    end = lines.index("ENDCOFACTORS")
    cofactors = [line for line in lines[start:end]]
    assert len(cofactors) == nrows == len(generators), (
        name, len(cofactors), nrows, len(generators),
    )
    return {
        "name": name,
        "ring": ring_line,
        "generators_sha256": generators_sha(generators),
        "generator_count": len(generators),
        "cofactors": cofactors,
        "generate_seconds": round(time.monotonic() - started, 3),
    }


def verify_certificate(record, program, timeout=3600):
    """Check sum T_i g_i == 1 by polynomial arithmetic only."""
    ring_line, generators = parse_ring_and_generators(program)
    assert ring_line == record["ring"], record["name"]
    assert generators_sha(generators) == record["generators_sha256"], (
        record["name"], "generator drift",
    )
    cofactors = record["cofactors"]
    assert len(cofactors) == len(generators)
    started = time.monotonic()
    script = ring_line + "\n"
    script += "poly acc=0;\n"
    for generator, cofactor in zip(generators, cofactors):
        script += f"acc=acc+({generator})*({cofactor});\n"
    script += 'print("RESIDUAL"); if(acc-1==0){0;}else{1;}\n'
    output = run_singular(script, timeout)
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    residual = int(lines[lines.index("RESIDUAL") + 1])
    assert residual == 0, (record["name"], "cofactor identity failed")
    return time.monotonic() - started


def save(records, path):
    payload = {
        "records": records,
        "sha256": hashlib.sha256(
            "\n".join(record["generators_sha256"] for record in records)
            .encode()
        ).hexdigest(),
    }
    pathlib.Path(path).write_text(json.dumps(payload, indent=1))
    return payload["sha256"]


def load(path):
    payload = json.loads(pathlib.Path(path).read_text())
    return payload["records"], payload["sha256"]


def main():
    parser = argparse.ArgumentParser(
        description="Generate or verify cofactor certificates for the "
        "rank-one star packets and radical certificates."
    )
    parser.add_argument("mode", choices=("generate", "verify"))
    parser.add_argument(
        "--artifact",
        default="computations/rank_one_cofactor_certificates.json",
    )
    parser.add_argument("--timeout", type=int, default=28800)
    arguments = parser.parse_args()

    import derive_three_cut_internal_23_adjacent_25_rank_one_w_structure as wstruct
    import test_three_cut_internal_23_adjacent_25_rank_one_star_ideals as ideals

    jobs = []
    for key in ("10", "20"):
        for generator, program in wstruct.radical_programs(key):
            jobs.append((f"radical_{key}_{generator}", program))
    for job in ideals.all_jobs(split=True):
        jobs.append((job["name"], job["program"]))

    if arguments.mode == "generate":
        records = []
        for name, program in jobs:
            record = generate_certificate(name, program, arguments.timeout)
            records.append(record)
            print(
                "GENERATED", name,
                f'seconds={record["generate_seconds"]}', flush=True,
            )
        digest = save(records, arguments.artifact)
        print("ARTIFACT_SHA256", digest, flush=True)
    else:
        records, digest = load(arguments.artifact)
        by_name = {record["name"]: record for record in records}
        total = 0.0
        for name, program in jobs:
            seconds = verify_certificate(by_name[name], program)
            total += seconds
            print("VERIFIED", name, f"seconds={seconds:.3f}", flush=True)
        print("ARTIFACT_SHA256", digest, flush=True)
        print(f"total verify seconds: {total:.3f}", flush=True)


if __name__ == "__main__":
    main()
