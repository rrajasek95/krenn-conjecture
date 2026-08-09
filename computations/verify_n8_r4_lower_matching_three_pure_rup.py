#!/usr/bin/env python3
"""Exact pure-support/RUP closure of the lower N=8 all-flat r=4 strata.

The structural reduction leaves good graphs 2K2+4K1 and 3K2+2K1.
This checker encodes the exact essential-count profiles, but relaxes the
source coefficients to endpoint support data.  Six frozen deletion-free RUP
proofs and two positive-hint LRAT proofs (two pure-matching union orbits times
four essential profiles) are replayed by independent in-repository checkers.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from itertools import combinations, permutations
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from time import monotonic

import verify_n8_r4_4k2_three_pure_support_rup as B


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "computations/verify_n8_r4_4k2_three_pure_support_rup.py"
BASE_SHA256 = "b93c9dea6e851a78271c0abd894e4fb272ae965abe87047f9594287221bccff7"

# (number of good matching edges, cubic sites, two-essential sites)
PROFILES = {
    "g2_t2_q6": (2, 2, 6),
    "g3_t1_q7": (3, 1, 7),
    "g3_t2_q5": (3, 2, 5),
    "g3_t2_q6": (3, 2, 6),
}

SURPLUS_REPRESENTATIVES = {
    "C8": (1, 3, 5, 7),
    "C4C4": (1, 3, 4),
}

CERTIFICATE_CASES = tuple(
    (orbit, profile, None)
    for orbit in B.PURE_REPS
    for profile in PROFILES
)

CERTIFICATE_PATHS = {
    (orbit, profile, surplus_site): ROOT / "computations/certificates" / (
        f"n8_r4_lower_{orbit.lower()}_{profile}"
        f"{'.lrat.gz' if profile == 'g3_t2_q6' else '.drup.gz'}"
    )
    for orbit, profile, surplus_site in CERTIFICATE_CASES
}

# Filled from independently replayed generation; normal verification pins all
# three quantities.  ``--write-proofs`` deliberately does not trust this map.
EXPECTED = {
    "C8:g2_t2_q6": {
        "clauses": 4572,
        "deletions": 0,
        "format": "drup",
        "gzip_sha256": "a952e8842fb7341ab6eed734175ab534e8b07441efc1077883da97d3d372fa51",
        "proof_clauses": 11889,
        "checks": 1671761,
        "raw_sha256": "2ad6c246ca8f151bdafcd22d164a775a7148d64266b77ea7409aac3475021253",
        "variables": 420,
    },
    "C8:g3_t1_q7": {
        "clauses": 4454,
        "deletions": 0,
        "format": "drup",
        "gzip_sha256": "a12aee0e4e5326709704b62748277d2b1d52953896256fdc873556bd93dc8e4e",
        "proof_clauses": 15663,
        "checks": 2409367,
        "raw_sha256": "1e09b663fb76f4be1776e4c0a8059a7ae3213274cad7c53181dda321036a1d00",
        "variables": 420,
    },
    "C8:g3_t2_q5": {
        "clauses": 4560,
        "deletions": 0,
        "format": "drup",
        "gzip_sha256": "0a00437fbe42e5da7e21763f558ecc294783b928c2c6e8bbbd509e7f63de91d4",
        "proof_clauses": 16354,
        "checks": 2697088,
        "raw_sha256": "cb954d7d72e54a19e4604ef529c18bdd05648b8fe89ba2095c44788cc7d21a59",
        "variables": 420,
    },
    "C8:g3_t2_q6": {
        "checks": 1334067,
        "clauses": 4487,
        "deletions": 28810,
        "format": "lrat",
        "gzip_sha256": "1b6c8bad8fcd30221710e5e3deb536b41e1cceb3f86b28df618a322e7ef2bd2e",
        "proof_clauses": 36034,
        "raw_sha256": "3f3f18f41a7ff0e4131e74125ffafdecaf73444d2f3cb7f08ba9bd4a149a5f1e",
        "variables": 424,
    },
    "C4C4:g2_t2_q6": {
        "clauses": 4572,
        "deletions": 0,
        "format": "drup",
        "gzip_sha256": "f9818825035dc34135e0d575a29b1fbfc6b45a062c7616bf993b152d33b5d871",
        "proof_clauses": 11696,
        "checks": 1774820,
        "raw_sha256": "7cbbe28d6ef1bc6333e3108645128980fa58bffd640cd71124f20284c73291ba",
        "variables": 420,
    },
    "C4C4:g3_t1_q7": {
        "clauses": 4454,
        "deletions": 0,
        "format": "drup",
        "gzip_sha256": "628d4aac97aecf974d6f2073702bc473cc75977bd42a311b29f3e213eec91138",
        "proof_clauses": 20429,
        "checks": 2651093,
        "raw_sha256": "13705a064479d1af2bfa12cfcfc02c8af8b7b645aef0a0c0d001f5881179310d",
        "variables": 420,
    },
    "C4C4:g3_t2_q5": {
        "clauses": 4560,
        "deletions": 0,
        "format": "drup",
        "gzip_sha256": "6da8506ec765f1e922e106b9de74d29e5dabf17577638267ff0b0b12cf2be677",
        "proof_clauses": 18993,
        "checks": 3106168,
        "raw_sha256": "8fc84f58df4aaab139484da16099653f5186ad7a36766c456ad5f038c00c61b7",
        "variables": 420,
    },
    "C4C4:g3_t2_q6": {
        "checks": 1114292,
        "clauses": 4481,
        "deletions": 26198,
        "format": "lrat",
        "gzip_sha256": "cd9d0b7668f7c3eba77bd6bc45d334e7ef6011cb41069bd5d1570609cf781d11",
        "proof_clauses": 31951,
        "raw_sha256": "ec4fcb804f2696f9e7b1058ae2b2e8bcdfb0c2e3f8580a4efbb417c72ca5f022",
        "variables": 423,
    },
}
EXPECTED_LEDGER_SHA256 = (
    "6412bd689612cdc3682d33de70cd6163c68e7cf4787f8e93bf7fca858ce32ffd"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def build_cnf(pure_pair, profile, surplus_site=None):
    good_edges, cubic_count, q2_count = PROFILES[profile]
    cnf = B.CNF()

    def m(u, v): return cnf.var("M", *B.edge(u, v))
    def g(u, v): return cnf.var("G", *B.edge(u, v))
    def h(u): return cnf.var("H", u)
    def a(u, v): return cnf.var("A", u, v)
    def essential(u, v): return cnf.var("E", u, v)
    def label(u, v, colour): return cnf.var("L", u, v, colour)
    def z(u): return cnf.var("Z", u)
    def q2(u): return cnf.var("Q2", u)
    def common(u, colour): return cnf.var("C", u, colour)
    def generic(u): return cnf.var("CG", u)
    def third(u, v): return cnf.var("P2", *B.edge(u, v))
    def surplus(v): return cnf.var("SX", v)

    cnf.exactly([h(u) for u in B.V], 2 * good_edges)
    cnf.exactly([z(u) for u in B.V], cubic_count)
    cnf.exactly([q2(u) for u in B.V], q2_count)
    # In the q5 profile there is a unique one-essential site.  The setwise
    # stabilizer of either frozen pure pair is vertex-transitive (audited
    # below), so global colour swap 0<->1 lets us put it at site zero.
    if profile == "g3_t2_q5":
        cnf.add(-z(0))
        cnf.add(-q2(0))
    if profile == "g3_t2_q6":
        # There is exactly one essential incidence beyond the mandatory one
        # per selected bad pair.  Vertex transitivity lets us place its site
        # at zero.  It is either on an unselected pair, or is one endpoint of
        # the unique double-essential selected pair.
        union_type = B.matching_union_cycle_type(*pure_pair)
        representatives = {
            (8,): (1, 3, 5, 7),
            (4, 4): (1, 3, 4),
        }[union_type]
        cnf.exactly([surplus(v) for v in representatives], 1)
        if surplus_site is not None:
            require(surplus_site in representatives,
                    "invalid surplus-neighbour representative")
            cnf.add(surplus(surplus_site))
    else:
        require(surplus_site is None,
                "a surplus site was supplied outside the q6 profile")

    for u in B.V:
        cnf.exactly([m(u, v) for v in B.V if v != u], 1)
        incident_good = [g(u, v) for v in B.V if v != u]
        for left, right in combinations(incident_good, 2):
            cnf.add(-left, -right)
        cnf.add(-h(u), *incident_good)
        for value in incident_good:
            cnf.add(-value, h(u))

        cnf.exactly([a(u, v) for v in B.V if v != u], 3)
        incident_essential = [essential(u, v) for v in B.V if v != u]
        # At most three essential neighbours.
        for chosen in combinations(incident_essential, 4):
            cnf.add(*(-value for value in chosen))
        # Z iff the essential count is three.
        for chosen in combinations(incident_essential, 3):
            cnf.add(*(-value for value in chosen), z(u))
        for chosen in combinations(incident_essential, 5):
            cnf.add(-z(u), *chosen)
        # Q2 iff the essential count is two.
        for chosen in combinations(incident_essential, 6):
            cnf.add(-q2(u), *chosen)
        for chosen in combinations(incident_essential, 3):
            cnf.add(-q2(u), *(-value for value in chosen))
        for left, right in combinations(incident_essential, 2):
            cnf.add(-left, -right, z(u), q2(u))
        cnf.add(-z(u), -q2(u))

        # A good edge endpoint cannot be cubic.  The line state at every
        # two-essential site is either one target axis or no target axis.
        for chosen in combinations(incident_essential, 3):
            cnf.add(-h(u), *(-value for value in chosen))
        cnf.exactly(
            [generic(u)] + [common(u, colour) for colour in range(3)], 1
        )

        cnf.exactly([third(u, v) for v in B.V if v != u], 1)
        for colour in range(3):
            cnf.exactly(
                [label(u, v, colour) for v in B.V if v != u], 1
            )

    for u, v in B.EDGES:
        # Four reciprocal pairs are exactly the doubly selected pairs.
        cnf.add(-m(u, v), -g(u, v))
        cnf.add(-m(u, v), a(u, v))
        cnf.add(-m(u, v), a(v, u))
        cnf.add(-a(u, v), -a(v, u), m(u, v))

        # G is exactly the selected pairs nonessential at both endpoints.
        cnf.add(-g(u, v), a(u, v), a(v, u))
        cnf.add(-g(u, v), -essential(u, v))
        cnf.add(-g(u, v), -essential(v, u))
        # In the three equality profiles every essential incidence is
        # consumed by a selected bad pair, so E implies selected.  The q6
        # slack profile has one extra incidence, which may instead belong to
        # an unselected physical pair and must be retained.
        if profile != "g3_t2_q6":
            cnf.add(-essential(u, v), a(u, v), a(v, u))
            cnf.add(-essential(v, u), a(u, v), a(v, u))
        cnf.add(-a(u, v), g(u, v), essential(u, v), essential(v, u))
        cnf.add(-a(v, u), g(u, v), essential(u, v), essential(v, u))

        for tail, head in ((u, v), (v, u)):
            labels = [label(tail, head, colour) for colour in range(3)]
            for value in labels:
                cnf.add(-value, a(tail, head))
            cnf.add(-a(tail, head), *labels)
            for left, right in combinations(labels, 2):
                cnf.add(-left, -right)

            # A cubic site has no other selected/nonzero physical neighbour.
            cnf.add(-z(tail), -a(tail, head), essential(tail, head))
            cnf.add(-z(head), -a(tail, head), essential(head, tail))

            # At a two-essential endpoint, every nonessential incoming head
            # lies on its unique common line.
            for colour in range(3):
                cnf.add(
                    -q2(head), -label(tail, head, colour),
                    essential(head, tail), common(head, colour)
                )

    if profile == "g3_t2_q6":
        for v in representatives:
            marker = surplus(v)
            cnf.add(-marker, essential(0, v))
            cnf.add(-marker, -a(0, v), essential(v, 0))
            cnf.add(-marker, -a(v, 0), essential(v, 0))

    def force_pure_edge(u, v, colour, condition=None):
        prefix = [] if condition is None else [-condition]
        for tail, head in ((u, v), (v, u)):
            # If the chosen pure edge is a selected incoming witness, its
            # literal head label has to be this colour.
            cnf.add(*prefix, -a(tail, head), label(tail, head, colour))
            # If it is not such a witness, a cubic endpoint requires the
            # edge to be selected/essential there.
            cnf.add(
                *prefix, a(tail, head), essential(head, tail), -z(head)
            )
            # At a two-essential endpoint, an unselected/nonessential pure
            # factor is possible only when the common line is that axis.
            cnf.add(
                *prefix, a(tail, head), essential(head, tail),
                -q2(head), common(head, colour)
            )

    for colour, matching in enumerate(pure_pair):
        for u, v in matching:
            force_pure_edge(u, v, colour)
    for u, v in B.EDGES:
        force_pure_edge(u, v, 2, third(u, v))

    metadata = {
        "variables": len(cnf.names) - 1,
        "clauses": len(cnf.clauses),
        "clause_lengths": dict(sorted(Counter(map(len, cnf.clauses)).items())),
    }
    return cnf, metadata


def audit_profiles():
    rows = {}
    for name, (good, cubic, q2) in PROFILES.items():
        selected_bad = 20 - good
        q1 = B.N - cubic - q2
        essential_min = 3 * cubic + 2 * q2
        essential_max = essential_min + q1
        require(essential_max >= selected_bad
                and essential_min <= selected_bad + 1,
                f"{name} ceased to be an exact/slack profile")
        require(q1 in (0, 1), f"{name} acquired two low-essential sites")
        # Covering every selected bad pair forces the q1 site (if present)
        # to have its one available essential incidence.
        essential_total = max(essential_min, selected_bad)
        rows[name] = {
            "good": good,
            "cubic": cubic,
            "q2": q2,
            "q1": q1,
            "selected_bad": selected_bad,
            "essential_total": essential_total,
        }
    require(set(rows) == set(PROFILES), "profile coverage changed")
    return rows


def audit_q1_symmetry():
    orbit_sizes = {}
    for name, (first, second) in B.PURE_REPS.items():
        first, second = frozenset(first), frozenset(second)
        stabilizer = tuple(
            permutation for permutation in permutations(B.V)
            if {
                B.image_matching(first, permutation),
                B.image_matching(second, permutation),
            } == {first, second}
        )
        vertex_orbit = {permutation[0] for permutation in stabilizer}
        require(vertex_orbit == set(B.V),
                f"the {name} pure-pair stabilizer lost vertex transitivity")
        orbit_sizes[name] = len(stabilizer)
    require(orbit_sizes == {"C8": 16, "C4C4": 64},
            "the setwise pure-pair stabilizers changed")
    return orbit_sizes


def audit_surplus_symmetry():
    expected = {
        "C8": ((1, 2), (3, 4), (5, 6), (7,)),
        "C4C4": ((1, 2), (3,), (4, 5, 6, 7)),
    }
    rows = {}
    for name, (first, second) in B.PURE_REPS.items():
        first, second = frozenset(first), frozenset(second)
        stabilizer = tuple(
            permutation for permutation in permutations(B.V)
            if permutation[0] == 0 and {
                B.image_matching(first, permutation),
                B.image_matching(second, permutation),
            } == {first, second}
        )
        unseen, orbits = set(B.V) - {0}, []
        while unseen:
            site = min(unseen)
            orbit = tuple(sorted({p[site] for p in stabilizer}))
            unseen.difference_update(orbit)
            orbits.append(orbit)
        rows[name] = tuple(orbits)
    require(rows == expected, "the surplus-neighbour orbit census changed")
    return rows


def parse_drup(raw):
    proof = []
    for line_number, line in enumerate(raw.decode("ascii").splitlines(), 1):
        fields = tuple(map(int, line.split()))
        require(fields and fields[-1] == 0 and 0 not in fields[:-1],
                f"malformed DRUP line {line_number}")
        proof.append(fields[:-1])
    return tuple(proof)


def independently_check_lrat(cnf, raw):
    """Check a positive-hint LRAT proof without invoking a SAT solver."""

    clauses = {index: tuple(clause)
               for index, clause in enumerate(cnf.clauses, 1)}
    last_id = len(clauses)
    additions = deletions = hints_checked = 0
    final_clause = None
    variable_count = len(cnf.names) - 1
    for line_number, raw_line in enumerate(
            raw.decode("ascii").splitlines(), 1):
        fields = raw_line.split()
        require(fields, f"empty LRAT line {line_number}")
        line_id = int(fields[0])
        if len(fields) > 1 and fields[1] == "d":
            require(line_id == last_id and fields[-1] == "0",
                    f"malformed LRAT deletion line {line_number}")
            for clause_id in map(int, fields[2:-1]):
                require(clause_id in clauses,
                        f"LRAT deletes absent clause {clause_id}")
                del clauses[clause_id]
                deletions += 1
            continue

        require(line_id > last_id,
                f"nonincreasing LRAT id at line {line_number}")
        last_id = line_id
        try:
            first_zero = fields.index("0", 1)
        except ValueError as error:
            raise RuntimeError(
                f"missing LRAT clause terminator at line {line_number}"
            ) from error
        require(fields[-1] == "0",
                f"missing LRAT hint terminator at line {line_number}")
        clause = tuple(map(int, fields[1:first_zero]))
        hint_ids = tuple(map(int, fields[first_zero + 1:-1]))
        require(hint_ids and all(value > 0 for value in hint_ids),
                f"a non-RUP LRAT chain occurs at line {line_number}")

        assignment = [0] * (variable_count + 1)
        for literal in clause:
            require(0 < abs(literal) <= variable_count,
                    f"out-of-range LRAT literal at line {line_number}")
            variable = abs(literal)
            value = -1 if literal > 0 else 1
            require(assignment[variable] in (0, value),
                    f"tautological LRAT clause at line {line_number}")
            assignment[variable] = value

        conflict = False
        for hint_index, clause_id in enumerate(hint_ids):
            require(clause_id in clauses,
                    f"LRAT references absent clause {clause_id}")
            unit = 0
            satisfied = False
            for literal in clauses[clause_id]:
                value = assignment[abs(literal)]
                if value and (value > 0) == (literal > 0):
                    satisfied = True
                    break
                if not value:
                    require(not unit,
                            f"LRAT hint is not unit at line {line_number}")
                    unit = literal
            require(not satisfied,
                    f"LRAT hint is satisfied at line {line_number}")
            if not unit:
                conflict = True
                require(hint_index == len(hint_ids) - 1,
                        f"LRAT chain continues after conflict at line {line_number}")
            else:
                assignment[abs(unit)] = 1 if unit > 0 else -1
        require(conflict, f"LRAT chain has no conflict at line {line_number}")
        clauses[line_id] = clause
        additions += 1
        hints_checked += len(hint_ids)
        final_clause = clause

    require(final_clause == (), "LRAT proof does not end in the empty clause")
    return additions, deletions, hints_checked


def certificate_key(orbit, profile, surplus_site=None):
    suffix = "" if surplus_site is None else f":s{surplus_site}"
    return f"{orbit}:{profile}{suffix}"


def write_proofs(cadical, only=None):
    checker_class = B.load_independent_rup_checker()
    results = {}
    for orbit, profile, surplus_site in CERTIFICATE_CASES:
        key = certificate_key(orbit, profile, surplus_site)
        if only is not None and key != only:
            continue
        cnf, metadata = build_cnf(
            B.PURE_REPS[orbit], profile, surplus_site
        )
        with tempfile.TemporaryDirectory(prefix="krenn-r4-lower-") as tmp:
            tmp = Path(tmp)
            cnf_path = tmp / "input.cnf"
            lrat = profile == "g3_t2_q6"
            proof_path = tmp / ("proof.lrat" if lrat else "proof.drat")
            cnf_path.write_bytes(B.dimacs_bytes(cnf))
            proof_options = ["--lrat=true"] if lrat else []
            process = subprocess.run(
                [cadical, "--plain", *proof_options,
                 "--binary=false", "--quiet",
                 str(cnf_path), str(proof_path)],
                check=False, capture_output=True, text=True
            )
            require(process.returncode == 20,
                    f"CaDiCaL did not prove {orbit}/{profile} UNSAT")
            if lrat:
                raw = proof_path.read_bytes()
                proof_clauses, deletions, checks = independently_check_lrat(
                    cnf, raw
                )
            else:
                additions = []
                for line in proof_path.read_text(encoding="ascii").splitlines():
                    if not line or line.startswith("d "):
                        continue
                    fields = tuple(map(int, line.split()))
                    require(fields[-1] == 0, "malformed generated DRAT line")
                    additions.append(fields[:-1])
                proof = tuple(additions)
                checks = B.independently_replay(cnf, proof, checker_class)
                raw = B.proof_bytes(proof)
                proof_clauses, deletions = len(proof), 0
        compressed = gzip.compress(raw, compresslevel=9, mtime=0)
        path = CERTIFICATE_PATHS[(orbit, profile, surplus_site)]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(compressed)
        results[key] = {
            "format": "lrat" if lrat else "drup",
            "proof_clauses": proof_clauses,
            "deletions": deletions,
            "raw_sha256": sha256(raw).hexdigest(),
            "gzip_sha256": sha256(compressed).hexdigest(),
            "checks": checks,
            "variables": metadata["variables"],
            "clauses": metadata["clauses"],
        }
        print(key, json.dumps(results[key], sort_keys=True), flush=True)
    print("EXPECTED =", json.dumps(results, indent=4, sort_keys=True))


def audit_certificate(task):
    orbit, profile, surplus_site = task
    key = certificate_key(orbit, profile, surplus_site)
    expected = EXPECTED[key]
    cnf, metadata = build_cnf(B.PURE_REPS[orbit], profile, surplus_site)
    path = CERTIFICATE_PATHS[(orbit, profile, surplus_site)]
    compressed = path.read_bytes()
    require(sha256(compressed).hexdigest() == expected["gzip_sha256"],
            f"compressed certificate changed for {key}")
    raw = gzip.decompress(compressed)
    require(sha256(raw).hexdigest() == expected["raw_sha256"],
            f"raw certificate changed for {key}")
    if expected["format"] == "lrat":
        proof_clauses, deletions, checks = independently_check_lrat(cnf, raw)
    else:
        require(expected["format"] == "drup", f"unknown proof format for {key}")
        proof = parse_drup(raw)
        require(len(proof) == expected["proof_clauses"] and proof[-1] == (),
                f"proof shape changed for {key}")
        checker_class = B.load_independent_rup_checker()
        checks = B.independently_replay(cnf, proof, checker_class)
        proof_clauses, deletions = len(proof), 0
    require(proof_clauses == expected["proof_clauses"]
            and deletions == expected["deletions"]
            and checks == expected["checks"],
            f"proof ledger changed for {key}")
    require(metadata["variables"] == expected["variables"]
            and metadata["clauses"] == expected["clauses"],
            f"CNF dimensions changed for {key}")
    return key, proof_clauses, checks


def audit(jobs=4):
    started = monotonic()
    require(sha256(BASE_PATH.read_bytes()).hexdigest() == BASE_SHA256,
            "the pinned CNF/orbit dependency changed")
    require(EXPECTED and EXPECTED_LEDGER_SHA256,
            "proof metadata has not yet been frozen")
    require(B.pure_pair_union_orbits() == ((1260, 5040), ((4, 4), (8,))),
            "the two disjoint pure-matching orbits changed")
    profile_rows = audit_profiles()
    q1_stabilizers = audit_q1_symmetry()
    surplus_orbits = audit_surplus_symmetry()
    ledger = {
        "profiles": profile_rows,
        "q1_stabilizers": q1_stabilizers,
        "surplus_neighbor_orbits": surplus_orbits,
        "certificates": {},
    }
    total_proof, total_checks = 0, 0
    tasks = CERTIFICATE_CASES
    if jobs == 1:
        results = map(audit_certificate, tasks)
    else:
        results = []
        for offset in range(0, len(tasks), jobs):
            batch = tasks[offset:offset + jobs]
            processes = []
            for orbit, profile, surplus_site in batch:
                key = certificate_key(orbit, profile, surplus_site)
                process = subprocess.Popen(
                    [sys.executable, str(Path(__file__).resolve()),
                     "--verify-only", key],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                processes.append((key, process))
            for key, process in processes:
                stdout, stderr = process.communicate()
                require(process.returncode == 0,
                        f"subprocess replay failed for {key}: {stderr}")
                result = json.loads(stdout)
                results.append(tuple(result))
    for key, proof_clauses, checks in results:
        ledger["certificates"][key] = EXPECTED[key]
        total_proof += proof_clauses
        total_checks += checks
    digest = sha256(json.dumps(ledger, sort_keys=True).encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            f"combined ledger changed: {digest}")
    return total_proof, total_checks, digest, monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-proofs", action="store_true")
    parser.add_argument("--cadical", default=shutil.which("cadical"))
    parser.add_argument("--only", choices=[
        certificate_key(*case) for case in CERTIFICATE_CASES
    ])
    parser.add_argument("--verify-only", choices=[
        certificate_key(*case) for case in CERTIFICATE_CASES
    ], help=argparse.SUPPRESS)
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args()
    if args.verify_only:
        require(sha256(BASE_PATH.read_bytes()).hexdigest() == BASE_SHA256,
                "the pinned CNF/orbit dependency changed")
        case = next(
            case for case in CERTIFICATE_CASES
            if certificate_key(*case) == args.verify_only
        )
        print(json.dumps(audit_certificate(case)))
        return
    if args.write_proofs:
        require(args.cadical, "pass --cadical PATH to generate proofs")
        write_proofs(args.cadical, args.only)
        return
    require(args.jobs >= 1, "--jobs must be positive")
    clauses, checks, digest, seconds = audit(args.jobs)
    print("N=8 lower r=4 matching pure-support obstruction: PASS")
    print("profiles:", ", ".join(PROFILES))
    print("proof additions:", clauses)
    print("checked proof steps:", checks)
    print("ledger sha256:", digest)
    print(f"seconds: {seconds:.3f}")


if __name__ == "__main__":
    main()
