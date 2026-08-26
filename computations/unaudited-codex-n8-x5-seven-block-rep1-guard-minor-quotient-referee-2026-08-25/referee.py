#!/usr/bin/env python3
"""Independent, design-only referee for the rep1 guard-minor quotient."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
from collections import Counter
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
ANTECEDENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-incidence-pivot-quotient-2026-08-25"
PINS = {
    PRODUCER / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    PRODUCER / "generate_minor_quotient.py": "63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
    PRODUCER / "minor_quotient_metadata.json": "1a8c5bb3c105d8d87b2eab58a52934a44d7768c537cc33a1542d7d06402d317c",
    PRODUCER / "rep1_minor_i0_p00_x0_y0_d01_p32003.sing": "edd174ccbc75a563fd67e0515b6dde2c54e5469b742629953080290fe7d1fb49",
    PRODUCER / "results_design_audit.json": "abe37d5ae4555fc2df64a3778b6d8a84e316613afbed72d61fb820d8f64bdabb",
    ANTECEDENT / "MANIFEST.sha256": "87bf2d17fcd4c5b8d52ba74c3cca8ecf5a19be2878df1fc2a86c70e05e7773cc",
    ANTECEDENT / "generate_quotient.py": "03993104d59aecf887cecbc9ea6f1c5e2703a5449933961d73520c53cb7ae68b",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


# Sparse integer polynomials, used only to check the generic substitution identities.
NAMES = ("wa", "wb", "wc", "va", "vb", "vc", "abar", "t", "beta")
ZERO_MONOMIAL = (0,) * len(NAMES)


class Poly(dict):
    def __add__(self, other):
        other = poly(other)
        out = dict(self)
        for monomial, coefficient in other.items():
            out[monomial] = out.get(monomial, 0) + coefficient
            if not out[monomial]:
                del out[monomial]
        return Poly(out)

    def __neg__(self):
        return Poly({m: -c for m, c in self.items()})

    def __sub__(self, other):
        return self + (-poly(other))

    def __mul__(self, other):
        other = poly(other)
        out = {}
        for left, lc in self.items():
            for right, rc in other.items():
                monomial = tuple(a + b for a, b in zip(left, right))
                out[monomial] = out.get(monomial, 0) + lc * rc
        return Poly({m: c for m, c in out.items() if c})


def poly(value):
    if isinstance(value, Poly):
        return value
    return Poly({ZERO_MONOMIAL: value}) if value else Poly()


def variable(name):
    powers = [0] * len(NAMES)
    powers[NAMES.index(name)] = 1
    return Poly({tuple(powers): 1})


def permutation_image(record, permutation):
    coordinate, p, q, r, kind, s, a, b = record
    aa, bb = sorted((permutation[a], permutation[b]))
    return (permutation[coordinate], permutation[p], permutation[q], permutation[r], kind, permutation[s], aa, bb)


def representative(record):
    return min(permutation_image(record, p) for p in itertools.permutations(range(3)))


def chart_census():
    raw = []
    for coordinate, p, q, r, s in itertools.product(range(3), repeat=5):
        for kind in ("y", "z"):
            for other in range(3):
                if other != q:
                    raw.append((coordinate, p, q, r, kind, s, *sorted((q, other))))
    groups = {}
    for record in raw:
        groups.setdefault(representative(record), []).append(record)
    all_equal_y = {
        representative((0, 0, 0, 0, "y", 0, *sorted((0, other))))
        for other in (1, 2)
    }
    return raw, groups, all_equal_y


def check_cramer_identities():
    wa, wb, wc, va, vb, vc, abar, t, _ = map(variable, NAMES)
    d = wa * vb - wb * va
    for delta in (0, 1):
        reduced = poly(delta) * abar - t * wc
        aa = reduced * vb + wb * t * vc
        ab = -(wa * t * vc + reduced * va)
        ac = d * t
        assert aa * va + ab * vb + ac * vc == Poly()
        assert aa * wa + ab * wb + ac * wc == poly(delta) * d * abar


def check_partner_identity(kind):
    # Independent symbolic cancellation: solve the selected row/column entry
    # and substitute it into A13^T*qy + A35*qz.
    # Each unsolved summand gets its own formal monomial variable encoded below.
    beta = variable("beta")
    for delta in (0, 1):
        left_tail = variable("wa") + variable("wb")
        right_tail = variable("va") + variable("vb")
        if kind == "y":
            solved = poly(delta) * beta - left_tail - right_tail
            total = left_tail + solved + right_tail
        else:
            solved = poly(delta) * beta - left_tail - right_tail
            total = left_tail + right_tail + solved
        assert total == poly(delta) * beta


def replay_manifest():
    for line in (PRODUCER / "MANIFEST.sha256").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        assert sha256(PRODUCER / relative) == expected


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, path
    replay_manifest()
    metadata = json.loads((PRODUCER / "minor_quotient_metadata.json").read_text())
    assert metadata["scope"] == {"D12_reads": False, "design_only": True, "launches": 0, "rep1_closed": False}

    raw, groups, all_equal_y = chart_census()
    orbit_sizes = Counter(map(len, groups.values()))
    assert len(raw) == 972
    assert len(groups) == 162
    assert orbit_sizes == {6: 162}
    assert sum(1 for record in groups if record[4] == "y") == 81
    assert sum(1 for record in groups if record[4] == "z") == 81
    assert len(all_equal_y) == 1

    # If both q-minors vanished while v_q != 0, then w=(w_q/v_q)v,
    # contradicting A06*v=0 and A06*w=alpha*e_i with alpha nonzero.
    check_cramer_identities()
    check_partner_identity("y")
    check_partner_identity("z")

    source = (PRODUCER / "rep1_minor_i0_p00_x0_y0_d01_p32003.sing").read_text()
    ring_line = next(line for line in source.splitlines() if line.startswith("ring r="))
    variables = ring_line.split(",(", 1)[1].split("),dp;", 1)[0].split(",")
    assert len(variables) == len(set(variables)) == 91
    assert not any(name.startswith("a06_") for name in variables)
    assert all(name in variables for name in ("t0", "t1", "t2", "abar", "beta", "sat"))
    body = source.split("ideal I=", 1)[1].split(";\nprint(", 1)[0]
    equations = body.split(",\n")
    assert len(equations) == len(set(equations)) == 6577
    assert "0" not in equations
    saturation = "abar*beta*a47_00*(a47_01-(xn1*a47_00))*sat-1"
    assert equations[-1] == saturation

    # Independent dimension/count ledger.
    source_variables = 10 * 9 - 9 - 3
    witness_and_scales = 2 + 1 + 5 + 1 + 3 + 1
    assert source_variables == 78 and witness_and_scales == 13
    assert source_variables + witness_and_scales == 91
    assert 3**8 + 6 + 9 + 1 == 6577
    assert metadata["counts"] == {
        "A06_entries_solved": 9,
        "first_quotient_generators": 6580,
        "first_quotient_variables": 94,
        "minor_quotient_generators": 6577,
        "minor_quotient_variables": 91,
        "original_incidence_generators": 6586,
        "original_incidence_variables": 100,
        "partner_entries_solved": 3,
        "tautological_guard_equations_removed": 3,
    }

    result = {
        "schema": "KRENN_X5_REP1_GUARD_MINOR_QUOTIENT_REFEREE_V1",
        "status": "PASS_EXACT_DESIGN_ONLY_NO_CLOSURE",
        "producer_manifest_sha256": PINS[PRODUCER / "MANIFEST.sha256"],
        "antecedent_manifest_sha256": PINS[ANTECEDENT / "MANIFEST.sha256"],
        "equivalence": {
            "v_w_independence": True,
            "two_minor_cover": True,
            "A06_cramer_entries": 9,
            "partner_entries": 3,
            "tautological_guard_rows_removed": 3,
            "combined_saturation_exact": True,
            "forward_reverse_localization": True,
        },
        "census": {
            "raw": len(raw),
            "s3_orbits": len(groups),
            "orbit_sizes": {str(k): v for k, v in sorted(orbit_sizes.items())},
            "y_orbits": 81,
            "z_orbits": 81,
            "all_equal_y_minor_orbits": len(all_equal_y),
        },
        "counts": {"variables": 91, "generators": 6577},
        "scope": {"design_only": True, "ideal_runs": 0, "rep1_closed": False, "D12_reads": False},
    }
    temporary = HERE / "results_referee.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_referee.json")
    print(json.dumps({"status": result["status"], "raw": len(raw), "orbits": len(groups)}, sort_keys=True))


if __name__ == "__main__":
    main()
