#!/usr/bin/env python3
"""Verify a small-denominator Q lift of the profile-71 terminal dual.

The Rust closure works over F_32003.  Balanced representatives are not a
rational reconstruction: in particular 16001 == -1/2 (mod 32003).  This
checker reconstructs every stored coefficient with a bounded denominator,
clears the common denominator, and replays all abstract translations over Z.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import product
import argparse
import json
from math import gcd, isqrt, lcm
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_closure22_joint_cegar import projected_word
from audit_colour_holonomy_quotients import PM8, key_add, matching_term, semigroup_key
from audit_physical_graph_quotient import holonomy


P = 32003


def rational_reconstruct(value, max_denominator=32):
    """Return the unique smallest-height a/b congruent to value mod P."""
    value %= P
    candidates = []
    bound = isqrt(P // 2)
    for denominator in range(1, max_denominator + 1):
        if gcd(denominator, P) != 1:
            continue
        residue = value * denominator % P
        numerator = residue if residue <= P // 2 else residue - P
        if abs(numerator) <= bound and gcd(numerator, denominator) == 1:
            candidates.append(Fraction(numerator, denominator))
    if not candidates:
        raise ValueError(f"no bounded rational reconstruction for {value}")
    return min(candidates, key=lambda q: (max(abs(q.numerator), q.denominator), q.denominator))


def sub_key(left, right):
    out = tuple(a - b for a, b in zip(left, right))
    return out if min(out) >= 0 else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        default="results_closure22_plus_profile71_joint_cegar_rust.json",
    )
    parser.add_argument(
        "--result",
        default="results_closure22_plus_profile71_rational_dual.json",
    )
    args = parser.parse_args()
    source = HERE / args.source
    result_path = HERE / args.result
    stored = json.loads(source.read_text())
    dual_q = {}
    for item in stored["terminal_integer_dual"]:
        column = tuple(item["column"])
        residue = item["coefficient"] % P
        dual_q[column] = rational_reconstruct(residue)

    denominator = 1
    for coefficient in dual_q.values():
        denominator = lcm(denominator, coefficient.denominator)
    dual_z = {
        column: coefficient.numerator * (denominator // coefficient.denominator)
        for column, coefficient in dual_q.items()
    }

    crossings = 0
    crossing_words = {}
    for label in stored["source_words"]:
        generator = projected_word(tuple(map(int, label)))
        pairings = defaultdict(int)
        for column, coefficient in dual_z.items():
            for term in generator:
                quotient = sub_key(column, term)
                if quotient is not None:
                    pairings[quotient] += coefficient
        live = {quotient: value for quotient, value in pairings.items() if value}
        if live:
            crossing_words[label] = len(live)
            crossings += len(live)

    cone = semigroup_key(matching_term((0,) * 8, PM8[0]))
    target = defaultdict(int)
    for term, coefficient in holonomy().items():
        target[key_add(cone, semigroup_key(term))] += coefficient
    target_pairing = sum(
        coefficient * dual_z.get(column, 0)
        for column, coefficient in target.items()
    )

    assert denominator == 2
    assert crossings == 0, crossing_words
    assert target_pairing != 0
    result = {
        "status": "PASS exact characteristic-zero separator",
        "source": source.name,
        "prime_used_only_for_reconstruction": P,
        "dual_support": len(dual_z),
        "common_denominator": denominator,
        "integer_coefficient_min": min(dual_z.values()),
        "integer_coefficient_max": max(dual_z.values()),
        "translation_crossings": crossings,
        "crossing_words": crossing_words,
        "target_pairing": target_pairing,
        "scope": (
            "Exact Z dual after clearing denominator 2; annihilates every "
            f"abstract joint-semigroup translation of the {len(stored['source_words'])} "
            "stored words."
        ),
        "dual": [
            {"column": list(column), "coefficient": coefficient}
            for column, coefficient in sorted(dual_z.items())
        ],
    }
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "dual"}, sort_keys=True))


if __name__ == "__main__":
    main()
