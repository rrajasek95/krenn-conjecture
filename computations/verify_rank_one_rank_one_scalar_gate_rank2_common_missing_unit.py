#!/usr/bin/env python3
"""Exact unit for the common-missing-coordinate rank-two scalar gate.

After relabelling the common missing coordinate as 2, the four contractions
of the double-annihilator plane have the literal form

    L*M*E = a X0 + b X1,
    L*V*E = 0,
    N*M*E = 0,
    N*V*E = c X2,

with a,b,c nonzero if all three dark target functionals survive.  The last
row forces one local component of E onto the e2 axis.  Normalize that site
as site 2, retaining arbitrary E components on sites 0 and 1.  This checker
expands the resulting 108 top coefficients, adds z*a*b*c-1, and verifies
that their exact standard basis is [1].

QQ is checked in dp and lp orders; F_2 and F_32003 in dp are independent
regression audits.  Standard library plus the external exact Singular
executable used throughout this repository.
"""

from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
from shutil import which
from subprocess import run


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SINGULAR = which("Singular") or "/usr/local/bin/Singular"
HERE = Path(__file__).resolve().parent
DEPENDENCY = HERE / "verify_rank_one_rank_one_scalar_gate_three_target_cofactor_unit.py"
DEPENDENCY_SHA256 = "fa762d646596638d8fba8ff9fe2e4bd9f4592e27ed81cdf3f4fac8e42f1225e9"
EXPECTED_GENERATOR_DIGEST = "6008f39b01f5ffd317c6066025ec933f520a19155b8b9a939ada318467023255"
EXPECTED_LEDGER_DIGEST = "88b9d678651d7d33080c8bd5db77088d5419797235294fb1d6344f984f29ff51"


def dependency_guard():
    actual = sha256(DEPENDENCY.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            ("the rank-three scalar-gate dependency changed", actual))


def value(form, site, colour):
    if form == "e" and site == 2:
        return "1" if colour == 2 else "0"
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


def build_packet():
    forms = ("l", "m", "n", "v")
    variables = [f"{form}{site}{colour}"
                 for form in forms
                 for site in range(3) for colour in range(3)]
    variables += [f"e{site}{colour}"
                  for site in (0, 1) for colour in range(3)]
    variables += ["a", "b", "c", "z"]
    pairs = (("l", "m"), ("l", "v"),
             ("n", "m"), ("n", "v"))
    labels = []
    generators = []
    for row, (left, right) in enumerate(pairs):
        for word in product(range(3), repeat=3):
            polynomial = top_coefficient(left, right, word)
            if row == 0 and word == (0, 0, 0):
                polynomial += "-a"
            if row == 0 and word == (1, 1, 1):
                polynomial += "-b"
            if row == 3 and word == (2, 2, 2):
                polynomial += "-c"
            labels.append(f"F{row}_{''.join(map(str, word))}")
            generators.append(polynomial)
    labels.append("localization")
    generators.append("z*a*b*c-1")
    require(len(generators) == 109, "bad rank-two generator count")
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
                    capture_output=True, timeout=60, check=False)
    require(completed.returncode == 0,
            ("Singular failed", characteristic, order,
             completed.stdout, completed.stderr))
    require(completed.stdout.strip() == "UNIT",
            ("rank-two common-missing ideal stopped being a unit",
             characteristic, order, completed.stdout, completed.stderr))
    return completed.stdout.strip()


def audit():
    dependency_guard()
    variables, labels, generators = build_packet()
    generator_digest = sha256(
        repr((variables, labels, generators)).encode()).hexdigest()
    if EXPECTED_GENERATOR_DIGEST is not None:
        require(generator_digest == EXPECTED_GENERATOR_DIGEST,
                ("rank-two generator ledger changed", generator_digest))
    runs = []
    for characteristic, order in ((0, "dp"), (0, "lp"),
                                  (2, "dp"), (32003, "dp")):
        runs.append((characteristic, order,
                     singular_unit(characteristic, order,
                                   variables, generators)))
    digest = sha256(repr((generator_digest, tuple(runs))).encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST is not None:
        require(digest == EXPECTED_LEDGER_DIGEST,
                ("rank-two audit ledger changed", digest))
    return len(generators), len(runs), generator_digest, digest


def main():
    generator_count, run_count, generator_digest, digest = audit()
    print("rank-(1,1) scalar-gate common-missing unit: passed")
    print(f"  exact generators         : {generator_count}")
    print(f"  exact Singular runs      : {run_count}")
    print(f"  generator digest         : {generator_digest}")
    print(f"  aggregate ledger digest  : {digest}")
    print("  conclusion               : rank-two scalar gate also loses a label")


if __name__ == "__main__":
    main()
