#!/usr/bin/env python3
"""Exact sparse factor and port-cycle audit of the 23-row K16 dual.

The checker removes the literal monomial gcd, asks Singular for exact
factorizations over Q, F_1009, and F_1013, and records the balanced 2-regular
port-graph cycle partition of every original monomial.  It performs no source
incidence expansion.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import argparse
import importlib.util
import json
from math import gcd
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NEXT_DIR = (ROOT / "computations"
            / "unaudited-codex-orbit0-k16-smallest-dual-next-page-2026-08-23")
NEXT_SCRIPT = NEXT_DIR / "audit_k16_smallest_dual_next_page.py"
NEXT_RESULT = NEXT_DIR / "results_k16_smallest_dual_next_page.json"
CLASS_DIR = (ROOT / "computations"
             / "unaudited-codex-orbit0-k16-dual-class-identification-2026-08-23")
CLASS_RESULT = CLASS_DIR / "results_k16_dual_class_identification.json"
RESULT = HERE / "results_k16_dual_sparse_factor.json"
SINGULAR = "/usr/local/bin/Singular"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


NEXT = load("k16_dual_sparse_factor_next", NEXT_SCRIPT)


def multiset_gcd(rows):
    common = Counter(rows[0])
    for row in rows[1:]:
        current = Counter(row)
        for cell in tuple(common):
            common[cell] = min(common[cell], current[cell])
            if not common[cell]:
                del common[cell]
    return common


def monomial_string(monomial):
    factors = []
    for cell, exponent in sorted(monomial.items()):
        if exponent == 1:
            factors.append(f"x{cell:02x}")
        elif exponent > 1:
            factors.append(f"x{cell:02x}^{exponent}")
    return "*".join(factors) or "1"


def sparse_polynomial(records):
    rows = tuple(bytes.fromhex(record["row"]) for record in records)
    common = multiset_gcd(rows)
    terms = []
    coefficients = []
    all_cells = set()
    seen = set()
    for record, row in zip(records, rows, strict=True):
        coefficient = record["coefficient"][0]
        require(record["coefficient"][1] == 1 and coefficient in (-1, 1),
                "nonintegral/nonunit dual coefficient")
        quotient = Counter(row)
        quotient.subtract(common)
        quotient = +quotient
        key = tuple(sorted(quotient.items()))
        require(key not in seen, "duplicate quotient monomial")
        seen.add(key)
        terms.append((coefficient, quotient))
        coefficients.append(coefficient)
        all_cells.update(quotient)
    terms.sort(key=lambda item: tuple(sorted(item[1].items())))
    expression = "".join(
        ("+" if coefficient > 0 else "-") + monomial_string(monomial)
        for coefficient, monomial in terms
    ).lstrip("+")
    degrees = {sum(monomial.values()) for _, monomial in terms}
    require(len(degrees) == 1, "quotient polynomial is not homogeneous")
    content = 0
    for coefficient in coefficients:
        content = gcd(content, abs(coefficient))
    require(content == 1, "quotient polynomial is not primitive")
    return {
        "rows": rows,
        "gcd": common,
        "terms": terms,
        "cells": tuple(sorted(all_cells)),
        "expression": expression,
        "degree": degrees.pop(),
        "content": content,
    }


def singular_factor(characteristic, cells, expression):
    variables = ",".join(f"x{cell:02x}" for cell in cells)
    source = (
        f"ring r={characteristic},({variables}),dp;\n"
        f"poly P={expression};\n"
        "list L=factorize(P);\n"
        'print("BEGIN");\n'
        "print(size(L[1]));\n"
        "int i;\n"
        "for(i=1;i<=size(L[1]);i++)"
        "{print(L[2][i]);print(deg(L[1][i]));print(size(L[1][i]));};\n"
        'print("END");\n'
        "quit;\n"
    )
    completed = subprocess.run(
        [SINGULAR, "-q"], input=source, text=True, capture_output=True,
        timeout=120, check=False)
    require(completed.returncode == 0 and not completed.stderr,
            (characteristic, completed.returncode, completed.stderr))
    lines = [line.strip() for line in completed.stdout.splitlines()]
    begin = lines.index("BEGIN")
    end = lines.index("END")
    payload = lines[begin + 1:end]
    factor_count = int(payload[0])
    require(len(payload[1:]) == 3 * factor_count,
            "unparseable Singular factor transcript")
    factors = []
    for index in range(factor_count):
        exponent, degree, terms = map(int, payload[1 + 3 * index:
                                                  4 + 3 * index])
        factors.append({
            "exponent": exponent,
            "total_degree": degree,
            "term_count": terms,
        })
    return {
        "characteristic": characteristic,
        "factor_count_including_unit": factor_count,
        "factors": factors,
        "source_sha256": sha256(source.encode("ascii")).hexdigest(),
    }


def factor_audit(polynomial):
    audits = [singular_factor(characteristic, polynomial["cells"],
                              polynomial["expression"])
              for characteristic in (0, 1009, 1013)]
    expected = [
        {"exponent": 1, "total_degree": 0, "term_count": 1},
        {"exponent": 1, "total_degree": polynomial["degree"],
         "term_count": len(polynomial["terms"])},
    ]
    require(all(audit["factors"] == expected for audit in audits),
            "nontrivial factor detected")

    # Hostile positive control for the transcript parser: multiplication by a
    # literal linear binomial must expose two nonconstant factors over Q.
    control_expression = f"({polynomial['expression']})*(x00+x01)"
    control = singular_factor(0, polynomial["cells"], control_expression)
    nonconstant = sorted(factor["total_degree"]
                         for factor in control["factors"]
                         if factor["total_degree"] > 0)
    require(nonconstant == [1, polynomial["degree"]],
            "factor-positive control failed")
    return audits, control


def cycle_partition(row):
    adjacency = defaultdict(list)
    degrees = Counter()
    for cell_id in row:
        left_site, right_site, left_colour, right_colour = NEXT.F.BASE.CELLS[cell_id]
        left = (left_site, left_colour)
        right = (right_site, right_colour)
        adjacency[left].append(right)
        adjacency[right].append(left)
        degrees[left] += 1
        degrees[right] += 1
    require(len(row) == 24 and len(degrees) == 24
            and set(degrees.values()) == {2},
            "row is not a balanced 2-regular port graph")
    seen = set()
    components = []
    for start in sorted(adjacency):
        if start in seen:
            continue
        seen.add(start)
        stack = [start]
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        components.append(size)
    require(sum(components) == 24, "port cycle partition lost vertices")
    return tuple(sorted(components, reverse=True))


def build(mutate=False):
    pinned = {
        NEXT_SCRIPT: "409be1569ea132ce7c564076be08f81bd9fd211d457207bbfb439e7d36fb1906",
        NEXT_RESULT: "6926b86320967b0af1e8017accede210aa4e7fb4bc412cf1f704c6539f9c46fb",
        CLASS_RESULT: "3d905e05e97b4062313ccbb0902168b3d106eecfaadbc68ee4d418283efd5443",
    }
    for path, expected in pinned.items():
        require(file_sha256(path) == expected, f"frozen input drift: {path}")
    next_result = json.loads(NEXT_RESULT.read_text())
    class_result = json.loads(CLASS_RESULT.read_text())
    require(next_result["logical_sha256"]
            == "c2dcada21b5904500e2d979bb4759cefbf6bdf449f81bef87ffb71b9827e7199"
            and class_result["logical_sha256"]
            == "720d7ff3507221b4074e198bc838f58b804444302c934d29d45997ea3f113a81",
            "logical input theorem drift")

    full_records = [dict(record) for record in next_result["next_dual"]["support"]]
    residual_records = [dict(record)
                        for record in class_result["new_23_cochain"]["residual"]]
    if mutate:
        row = bytes.fromhex(full_records[0]["row"])
        full_records[0]["row"] = row[:-1].hex()

    full = sparse_polynomial(full_records)
    residual = sparse_polynomial(residual_records)
    require((len(full["terms"]), sum(full["gcd"].values()), full["degree"],
             len(full["cells"])) == (23, 7, 17, 41),
            "full sparse polynomial interface changed")
    require((len(residual["terms"]), sum(residual["gcd"].values()),
             residual["degree"], len(residual["cells"])) == (15, 11, 13, 33),
            "residual sparse polynomial interface changed")

    full_audits, full_control = factor_audit(full)
    residual_audits, residual_control = factor_audit(residual)

    residual_rows = {record["row"] for record in residual_records}
    cycle_rows = []
    histogram = Counter()
    for record in full_records:
        row = bytes.fromhex(record["row"])
        partition = cycle_partition(row)
        histogram[partition] += 1
        cycle_rows.append({
            "row": row.hex(),
            "coefficient": record["coefficient"],
            "K_degree": record["K_degree"],
            "part": "new_residual" if row.hex() in residual_rows else "old_shadow",
            "cycle_partition": list(partition),
        })

    version = subprocess.run([SINGULAR, "--version"], text=True,
                             capture_output=True, timeout=10, check=False)
    require(version.returncode == 0, "cannot read Singular version")
    result = {
        "format": "n8-orbit0-k16-dual-sparse-factor-v1",
        "status": "UNAUDITED exact sparse factor/cycle theorem",
        "pinned": {str(path.relative_to(ROOT)): digest
                   for path, digest in pinned.items()},
        "CAS": {
            "executable": SINGULAR,
            "version": version.stdout.splitlines()[0].strip(),
            "rings": ["Q", "F_1009", "F_1013"],
        },
        "full_23_polynomial": {
            "monomial_gcd": bytes(sorted(full["gcd"].elements())).hex(),
            "monomial_gcd_degree": sum(full["gcd"].values()),
            "primitive_quotient_degree": full["degree"],
            "primitive_quotient_terms": len(full["terms"]),
            "primitive_quotient_variables": len(full["cells"]),
            "primitive_quotient_expression": full["expression"],
            "primitive_quotient_sha256": sha256(
                full["expression"].encode("ascii")).hexdigest(),
            "factor_audits": full_audits,
            "positive_factor_control": full_control,
            "verdict": "IRREDUCIBLE_OVER_Q_AFTER_MONOMIAL_GCD",
        },
        "new_15_residual_polynomial": {
            "monomial_gcd": bytes(sorted(residual["gcd"].elements())).hex(),
            "monomial_gcd_degree": sum(residual["gcd"].values()),
            "primitive_quotient_degree": residual["degree"],
            "primitive_quotient_terms": len(residual["terms"]),
            "primitive_quotient_variables": len(residual["cells"]),
            "primitive_quotient_expression": residual["expression"],
            "primitive_quotient_sha256": sha256(
                residual["expression"].encode("ascii")).hexdigest(),
            "factor_audits": residual_audits,
            "positive_factor_control": residual_control,
            "verdict": "IRREDUCIBLE_OVER_Q_AFTER_MONOMIAL_GCD",
        },
        "irreducibility_proof": (
            "Both primitive +/-1 polynomials retain total degree modulo 1009 "
            "and modulo 1013, and Singular returns one nonconstant factor of "
            "exponent one in each finite-field ring. By Gauss's lemma, already "
            "either finite-field irreducibility certificate rules out a "
            "nontrivial factorization over Q. Independent Q factorization "
            "returns the same one-factor profile."),
        "port_graphs": {
            "rows": cycle_rows,
            "cycle_partition_histogram": {
                "+".join(map(str, partition)): count
                for partition, count in sorted(histogram.items())
            },
            "balanced_degree": 2,
            "port_vertices_per_row": 24,
        },
        "conclusion": (
            "There is no non-monomial binomial, Pluecker, Pfaffian, or other "
            "low-degree polynomial factor in either the full 23-term cochain "
            "or its 15-term genuinely-new residual. Their structure is a "
            "signed sum across several port-cycle types, not a hidden sparse "
            "factor."),
        "scope_guard": (
            "Exact factorization of the two frozen sparse polynomials and "
            "literal 2-regular port-cycle census only; no next-page source "
            "incidence or claim about ideal primality."),
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(payload.encode("ascii")).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = build(mutate=args.mutate)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("K16 dual sparse factor/cycle audit: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
