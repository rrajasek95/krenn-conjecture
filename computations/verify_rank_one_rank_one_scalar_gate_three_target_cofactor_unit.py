#!/usr/bin/env python3
"""Exact three-target cofactor units on the rank-(1,1) scalar gate.

After the joint-diagonal theorem, the rank-three scalar gate has three
rank-one cap contractions.  Contract a maximal dark shore coefficient and
suppose all three fixed target labels survive.  The common one-hole cofactor
can then be normalized to

    e = e0@0 + e1@1 + e2@2.

The three rank-one responses have exactly three line-incidence normal forms:

  A: l0*m0, l1*m1, (l0+l1)*(m0+m1);
  B: l*m0,  l*m1,  n*(m0+m1);
  D: l*m,   l*v,    n*m.

Signs are immaterial and are retained as minus signs in A/B.  For each
normal form this checker expands all 81 coefficients of response_i*e,
adjoins nonzero target scalars b0,b1,b2 by z*b0*b1*b2=1, and asks exact
Singular standard-basis computations to verify the unit ideal.  It checks
QQ in dp and lp orders, and F_2/F_32003 in dp order.  The theorem is over C;
the finite-field runs are independent regression audits.
"""

from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
from shutil import which
from subprocess import run


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SINGULAR = which("Singular") or "/usr/local/bin/Singular"
HERE = Path(__file__).resolve().parent
DEPENDENCY = HERE / "verify_rank_one_rank_one_scalar_gate_diagonal_cycle.py"
DEPENDENCY_SHA256 = "a7efd73c93ad435b4026237d83f68b095a3e88cf3f75f3c397e5c8c486ea42f7"


NORMAL_FORMS = {
    "A": {
        "forms": ("l0", "l1", "m0", "m1"),
        "pairs": (("l0", "m0"), ("l1", "m1"), ("l2", "m2")),
    },
    "B": {
        "forms": ("l", "n", "m0", "m1"),
        "pairs": (("l", "m0"), ("l", "m1"), ("n", "m2")),
    },
    "D": {
        "forms": ("l", "n", "m", "v"),
        "pairs": (("l", "m"), ("l", "v"), ("n", "m")),
    },
}

EXPECTED_GENERATOR_DIGEST = (
    "84ba8110d7ce2ad51547c2626d2582de86b7a4b9ece33afceba83a120a2e7b35"
)
EXPECTED_LEDGER_DIGEST = (
    "2781a6e50b81018b80f35da23da8eafb2f46eae7a0f099c7a5bb0a7ead3d3715"
)


def dependency_guard():
    actual = sha256(DEPENDENCY.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            ("the diagonal-cycle dependency changed", actual))


def value(form, site, colour):
    if form == "l2":
        return f"(-l0{site}{colour}-l1{site}{colour})"
    if form == "m2":
        return f"(-m0{site}{colour}-m1{site}{colour})"
    if form == "e":
        return "1" if site == colour else "0"
    return f"{form}{site}{colour}"


def top_coefficient(left, right, word):
    factors = (left, right, "e")
    terms = []
    for assignment in permutations(range(3)):
        entries = [value(factors[index], assignment[index],
                         word[assignment[index]])
                   for index in range(3)]
        if "0" in entries:
            continue
        terms.append("*".join(entry for entry in entries if entry != "1")
                     or "1")
    return "(" + ("+".join(terms) if terms else "0") + ")"


def build_packet(name):
    data = NORMAL_FORMS[name]
    variables = [f"{form}{site}{colour}"
                 for form in data["forms"]
                 for site in range(3) for colour in range(3)]
    variables += ["b0", "b1", "b2", "z"]
    labels = []
    generators = []
    for target, (left, right) in enumerate(data["pairs"]):
        for word in product(range(3), repeat=3):
            polynomial = top_coefficient(left, right, word)
            if word == (target, target, target):
                polynomial += f"-b{target}"
            labels.append(f"F{target}_{''.join(map(str, word))}")
            generators.append(polynomial)
    labels.append("localization")
    generators.append("z*b0*b1*b2-1")
    require(len(generators) == 82, ("bad generator count", name))
    return tuple(variables), tuple(labels), tuple(generators)


def singular_unit(characteristic, order, variables, generators):
    source = (
        f"ring r={characteristic},({','.join(variables)}),{order};\n"
        f"ideal I={','.join(generators)};\n"
        "ideal G=slimgb(I);\n"
        'if(size(G)==1 && G[1]==1){print("UNIT");}'
        'else{print("NONUNIT");print(size(G));}\n'
        "quit;\n"
    )
    completed = run([SINGULAR, "-q"], input=source, text=True,
                    capture_output=True, timeout=30, check=False)
    require(completed.returncode == 0,
            ("Singular failed", characteristic, order,
             completed.stdout, completed.stderr))
    require(completed.stdout.strip() == "UNIT",
            ("cofactor ideal stopped being a unit", characteristic, order,
             completed.stdout, completed.stderr))
    return completed.stdout.strip()


def support_pattern_census():
    supports = tuple(combination for size in (2, 3)
                     for combination in combinations(range(3), size))
    counts = {"A": 0, "B": 0, "D": 0, "rank2": 0}
    records = []
    for left in supports:
        for right in supports:
            common_missing = (set(range(3)) - set(left)) & (
                set(range(3)) - set(right))
            if common_missing:
                kind = "rank2"
            elif len(left) == len(right) == 3:
                kind = "A"
            elif len(left) == 2 and len(right) == 2:
                kind = "D"
            else:
                kind = "B"
            counts[kind] += 1
            records.append((left, right, kind))
    require(counts == {"A": 1, "B": 6, "D": 6, "rank2": 3},
            ("support normal-form census changed", counts))
    return tuple(records), counts


def audit():
    dependency_guard()
    support_records, counts = support_pattern_census()
    packets = {}
    generator_ledger = []
    run_ledger = []
    for name in NORMAL_FORMS:
        variables, labels, generators = build_packet(name)
        packets[name] = (variables, labels, generators)
        generator_ledger.append((name, variables, labels, generators))
        for characteristic, order in ((0, "dp"), (0, "lp"),
                                      (2, "dp"), (32003, "dp")):
            result = singular_unit(characteristic, order,
                                   variables, generators)
            run_ledger.append((name, characteristic, order, result))
    generator_digest = sha256(
        repr(tuple(generator_ledger)).encode()).hexdigest()
    require(generator_digest == EXPECTED_GENERATOR_DIGEST,
            ("three-target generator ledger changed", generator_digest))
    ledger = (support_records, tuple(run_ledger), generator_digest)
    digest = sha256(repr(ledger).encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST is not None:
        require(digest == EXPECTED_LEDGER_DIGEST,
                ("three-target audit ledger changed", digest))
    return counts, len(run_ledger), generator_digest, digest


def main():
    counts, run_count, generator_digest, digest = audit()
    print("rank-(1,1) scalar-gate three-target cofactor unit: passed")
    print(f"  support normal forms     : {dict(sorted(counts.items()))}")
    print(f"  exact Singular runs      : {run_count}")
    print(f"  generator digest         : {generator_digest}")
    print(f"  aggregate ledger digest  : {digest}")
    print("  conclusion               : rank-three scalar gate loses a fixed label")


if __name__ == "__main__":
    main()
