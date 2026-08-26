#!/usr/bin/env python3
"""Characteristic-zero nine-row certificate in the colour-pair marginal.

All physical edge variables are identified, but the ordered endpoint colour
pair is retained.  The script asks Singular for a source lift and verifies it
inside Singular before accepting the certificate.
"""

from collections import defaultdict
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_physical_graph_quotient import P, PM8, holonomy


RESULTS = HERE / "results_colour_only_hamming_certificate.json"
VARIABLES = tuple(f"y{i}{j}" for i in range(3) for j in range(3))
OMITTED_WORD = (2, 1, 2, 1, 1, 1, 1, 1)
EXPECTED_ACTIVE = {
    "10000000", "11111110", "12111111", "12121111", "20000000",
    "21111110", "21111111", "21112111", "22111111",
}
TARGET_FACTORIZATION = (
    "-675*y00^6*y11^2*(2*y12^2+y11*y22)*"
    "(y00*y11*y22-y00*y12*y21-y01*y10*y22+y01*y12*y20+"
    "y02*y10*y21-y02*y11*y20)"
)


def matching_term(word, matching):
    return tuple((word[u], word[v]) for u, v in matching)


def histogram(term):
    counts = [0] * 9
    for a, b in term:
        counts[3 * a + b] += 1
    return tuple(counts)


def projected_word(word):
    out = defaultdict(int)
    for matching in PM8:
        out[histogram(matching_term(word, matching))] += 1
    return dict(out)


def signed(value):
    return value - P if value > P // 2 else value


def monomial(key):
    factors = []
    for variable, exponent in zip(VARIABLES, key):
        if exponent == 1:
            factors.append(variable)
        elif exponent:
            factors.append(f"{variable}^{exponent}")
    return "*".join(factors) or "1"


def polynomial(poly, signed_coefficients=False):
    pieces = []
    for key, coefficient in sorted(poly.items()):
        coefficient = signed(coefficient) if signed_coefficients else coefficient
        if not coefficient:
            continue
        term = monomial(key)
        if coefficient == 1:
            pieces.append(term)
        elif coefficient == -1:
            pieces.append("-" + term)
        else:
            pieces.append(f"{coefficient}*{term}")
    text = "+".join(pieces) or "0"
    return text.replace("+-", "-")


def colour_target():
    projected = defaultdict(int)
    for term, coefficient in holonomy().items():
        key = [0] * 9
        for _, _, a, b in term:
            key[3 * a + b] += 1
        key[0] += 4  # the fixed pure-0 cone matching
        projected[tuple(key)] = (projected[tuple(key)] + coefficient) % P
    return {key: value for key, value in projected.items() if value}


def build_generators():
    seen = {}
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        poly = projected_word(word)
        frozen = tuple(sorted(poly.items()))
        seen.setdefault(frozen, (word, poly))
    omitted_frozen = tuple(sorted(projected_word(OMITTED_WORD).items()))
    generators = [value for frozen, value in seen.items() if frozen != omitted_frozen]
    assert len(seen) == 5211 and len(generators) == 5210
    return generators


def run_certificate():
    generators = build_generators()
    target = colour_target()
    source = [f"ring r=0,({','.join(VARIABLES)}),dp;", "option(redSB);"]
    source.append("ideal I=" + ",".join(polynomial(poly) for _, poly in generators) + ";")
    source.append("poly T=" + polynomial(target, signed_coefficients=True) + ";")
    source.append("poly TF=" + TARGET_FACTORIZATION + ";")
    source.append('if(T-TF!=0){print("FACTORIZATION_FAILED");exit(1);}')
    source.extend([
        "ideal G=std(I);",
        "poly R=reduce(T,G);",
        'print("GBSIZE="+string(size(G)));',
        'print("REMAINDER="+string(R));',
        "matrix L=lift(I,ideal(T));",
        'if(matrix(I)*L-matrix(ideal(T))!=0){print("LIFT_FAILED");exit(1);}',
        "int i;int nz=0;int md=0;int d;",
        'print("BEGIN_ACTIVE");',
        'for(i=1;i<=nrows(L);i++){if(L[i,1]!=0){nz++;d=deg(L[i,1]);'
        'if(d>md){md=d;}print(string(i));}}',
        'print("END_ACTIVE");',
        'print("BEGIN_MULTIPLIERS");',
        'for(i=1;i<=nrows(L);i++){if(L[i,1]!=0){'
        'print("INDEX="+string(i));print(string(L[i,1]));print("END_MULTIPLIER");}}',
        'print("END_MULTIPLIERS");',
        'print("NONZERO="+string(nz));',
        'print("MAXDEG="+string(md));',
        'print("BEGIN_LIFT");L;print("END_LIFT");',
        "quit;",
    ])
    with tempfile.TemporaryDirectory(prefix="krenn-colour-cert-") as directory:
        script = Path(directory) / "certificate.sing"
        script.write_text("\n".join(source))
        completed = subprocess.run(
            ["Singular", "-q", str(script)], text=True, capture_output=True,
            timeout=120, check=False,
        )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr + completed.stdout[-2000:])
    stdout = completed.stdout
    if ("LIFT_FAILED" in stdout or "FACTORIZATION_FAILED" in stdout
            or "REMAINDER=0" not in stdout):
        raise RuntimeError(stdout[-4000:])
    active_text = stdout.split("BEGIN_ACTIVE\n", 1)[1].split("\nEND_ACTIVE", 1)[0]
    active_indices = [int(line) for line in active_text.splitlines() if line.strip()]
    active_words = {"".join(map(str, generators[index - 1][0])) for index in active_indices}
    if active_words != EXPECTED_ACTIVE:
        raise RuntimeError(f"unexpected active words: {active_words}")
    lift = stdout.split("BEGIN_LIFT\n", 1)[1].split("\nEND_LIFT", 1)[0]
    multiplier_text = stdout.split("BEGIN_MULTIPLIERS\n", 1)[1].split(
        "\nEND_MULTIPLIERS", 1
    )[0]
    multipliers = {}
    for block in multiplier_text.split("END_MULTIPLIER"):
        if not block.strip():
            continue
        lines = block.strip().splitlines()
        index = int(lines[0].split("=", 1)[1])
        word = "".join(map(str, generators[index - 1][0]))
        multipliers[word] = "".join(lines[1:])
    return {
        "status": "PASS exact characteristic-zero colour-only certificate",
        "projected_mixed_generators": len(generators),
        "omitted_incompatible_word": "".join(map(str, OMITTED_WORD)),
        "groebner_basis_size": int(stdout.split("GBSIZE=", 1)[1].splitlines()[0]),
        "target_terms": len(target),
        "target_factorization": TARGET_FACTORIZATION,
        "remainder": "0",
        "nonzero_source_multipliers": int(stdout.split("NONZERO=", 1)[1].splitlines()[0]),
        "maximum_multiplier_degree": int(stdout.split("MAXDEG=", 1)[1].splitlines()[0]),
        "active_words": sorted(active_words),
        "active_multipliers": dict(sorted(multipliers.items())),
        "lift_sha256": hashlib.sha256(lift.encode()).hexdigest(),
        "scope": (
            "The quotient identifies all physical edge variables with the same "
            "ordered colour-pair variable. It proves a marginal ideal membership, "
            "not a lift to the full decorated source ring."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_certificate()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored certificate result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
