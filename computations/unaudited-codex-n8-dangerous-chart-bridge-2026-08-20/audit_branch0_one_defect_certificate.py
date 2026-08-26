#!/usr/bin/env python3
"""Independent literal replay of the branch-0 one-defect certificate."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
CERT_PATH = HERE / "certificate_branch0_one_defect.json"
OUT = HERE / "results_branch0_one_defect_certificate_audit.json"
N = 13
ZERO_EXP = (0,) * N


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SCREEN = load("n8_b0_one_defect_audit_screen",
              SOURCE / "screen_lowq_joint_branch_orbits.py")


def tidy(poly):
    return {key: value for key, value in poly.items() if value}


def plus(*polys):
    result = Counter()
    for poly in polys:
        result.update(poly)
    return tidy(result)


def times(*polys):
    result = {ZERO_EXP: Fraction(1)}
    for poly in polys:
        next_result = Counter()
        for left, lc in result.items():
            for right, rc in poly.items():
                next_result[tuple(x + y for x, y in zip(left, right))] += lc * rc
        result = tidy(next_result)
    return result


def atom(index, power=1, coefficient=1):
    exponent = [0] * N
    exponent[index] = power
    return {tuple(exponent): Fraction(coefficient)}


def substitution():
    answer = []
    for edge in range(6):
        if edge == 0:
            c = plus(atom(6, -1, -1),
                     times(atom(0), atom(12), atom(6, -1, -1)))
            answer += [atom(0), atom(6), c, atom(12)]
        else:
            answer += [atom(edge), atom(6 + edge),
                       atom(6 + edge, -1, -1), {}]
    return tuple(answer)


SUB = substitution()


def specialize(raw):
    result = {}
    for monomial, coefficient in raw.items():
        term = {ZERO_EXP: Fraction(coefficient)}
        for index in monomial:
            term = times(term, SUB[index])
        result = plus(result, term)
    return result


def clear(poly):
    if not poly:
        return {}, ZERO_EXP
    shift = tuple(max(0, -min(exponent[index] for exponent in poly))
                  for index in range(N))
    return tidy({tuple(exponent[index] + shift[index] for index in range(N)): c
                 for exponent, c in poly.items()}), shift


def encode(poly):
    names = tuple([f"a{i}" for i in range(6)]
                  + [f"b{i}" for i in range(6)] + ["d"])
    pieces = []
    for exponent, coefficient in sorted(poly.items()):
        factors = [names[index] + (f"^{power}" if power != 1 else "")
                   for index, power in enumerate(exponent) if power]
        body = "*".join(factors) or "1"
        magnitude = abs(coefficient)
        if magnitude != 1:
            body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces) if pieces else "0"


def labels():
    result = ["e_" + "".join(map(str, edge))
              for edge in SCREEN.PROBE.CORE.SUPER_EDGES]
    result += ["t_" + "".join(map(str, triple))
               for triple in combinations(range(4), 3)]
    result += [f"cofactor_{edge}_{position}"
               for edge in range(6) for position in (0, 3)]
    return tuple(result)


def literal_rows():
    equations, raw_h = SCREEN.PROBE.equations((0,) * 6)
    records = {}
    order = []
    for label, raw in zip(labels(), equations):
        poly, shift = clear(specialize(raw))
        if not poly:
            continue
        key = encode(poly)
        if key in records:
            records[key]["source_labels"].append(label)
        else:
            row = {"source_labels": [label],
                   "clearing_shift_a0_a5_b0_b5_d": list(shift),
                   "polynomial": key}
            records[key] = row
            order.append(row)
    h, h_shift = clear(specialize(raw_h))
    return order, encode(h), list(h_shift)


def singular_replay(rows, mutate=False):
    variables = [f"a{i}" for i in range(6)] + [f"b{i}" for i in range(6)]
    variables += ["d", "u", "z"]
    summands = []
    changed = False
    for row in rows:
        coefficient = row["coefficient"]
        if mutate and not changed and coefficient != "0":
            coefficient = f"-({coefficient})"
            changed = True
        summands.append(f"({coefficient})*({row['polynomial']})")
    command = (
        f"ring R=0,({','.join(variables)}),dp; "
        f"poly residue=({'+'.join(summands)})-d; "
        'if(residue==0){print("ZERO");}else{print("NONZERO");};quit;'
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=30, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular replay failed: " + completed.stderr[-1000:])
    return completed.stdout.strip()


def main():
    cert = json.loads(CERT_PATH.read_text())
    logical_cert = dict(cert)
    claimed_cert_sha = logical_cert.pop("result_sha256")
    actual_cert_sha = sha256(json.dumps(logical_cert, sort_keys=True,
                                        separators=(",", ":")).encode("ascii")).hexdigest()
    require(actual_cert_sha == claimed_cert_sha,
            "certificate logical digest mismatch")

    actual, h_poly, h_shift = literal_rows()
    require(len(actual) == 15, "independent distinct-row count changed")
    frozen = cert["rows"]
    require(frozen[:15] == [row | {"coefficient": frozen[index]["coefficient"]}
                            for index, row in enumerate(actual)],
            "frozen literal rows differ from independent raw substitution")
    require(frozen[15]["source_labels"] == ["localize_H"]
            and frozen[15]["clearing_shift_a0_a5_b0_b5_d"] == h_shift
            and frozen[15]["polynomial"] == f"u*({h_poly})-1",
            "H-localization row changed")
    require(frozen[16]["source_labels"] == ["localize_b_product"]
            and frozen[16]["polynomial"] == "z*b0*b1*b2*b3*b4*b5-1",
            "b-localization row changed")
    require(singular_replay(frozen) == "ZERO", "frozen identity failed")
    require(singular_replay(frozen, mutate=True) == "NONZERO",
            "coefficient-sign mutation was not detected")

    nonzero = [row for row in frozen if row["coefficient"] != "0"]
    require([row["source_labels"] for row in nonzero]
            == [["cofactor_1_0"], ["cofactor_2_0"],
                ["localize_b_product"]],
            "compact three-row support changed")
    result = {
        "status": "UNAUDITED independent branch-0 one-defect audit PASS",
        "certificate_logical_sha256": actual_cert_sha,
        "independent_literal_nonzero_distinct_rows": len(actual),
        "exact_identity_replay": True,
        "coefficient_sign_mutation_detected": True,
        "compact_nonzero_rows": [row["source_labels"][0] for row in nonzero],
        "human_identity": (
            "cofactor_1_0=d*(-b4+b3*b5), "
            "cofactor_2_0=d*(b4+b3*b5), hence their sum is "
            "2*d*b3*b5; the live b-product forces d=0"
        ),
        "stronger_scope": "The pure-H localization has coefficient zero.",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 one-defect independent audit: PASS")
    print("literal rows / nonzero lift rows:", len(actual), len(nonzero))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
