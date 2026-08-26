#!/usr/bin/env python3
"""Export deterministic affine slices of the frozen 0:31:30 core8 gate.

The last polynomial in every modular input is the 16-term base-live product,
intended for msolve F4SAT's ``-S`` interface.  The transported c/H factors are
deliberately not saturated here: they are restrictions to replay on any
component or finite residual that lands.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
COMP = HERE.parent
REPO = COMP.parent
SOURCE_INPUT = HERE / "face03130_aopen_core8_split_live_char0.msolve"
SOURCE_LABELS = HERE / "face03130_aopen_core8_split_live_labels.json"
SOURCE_EXPORT = HERE / "results_face03130_aopen_export.json"
TOOLKIT = COMP / "toolkit/groebner/msolve_io.py"
RESULT = HERE / "results_face03130_core8_slice_export.json"
PRIME = 1073741827
ACTIVE_NAMES = ("a0", "a1", "a2", "a3", "a5", "b3", "b4", "b5",
                "d2", "d3", "d4")
SEED = "k5-face-0:31:30-Aopen-core8-affine-slices-v1"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def centered_hash_integer(depth, name):
    digest = sha256(f"{SEED}|{depth}|{name}".encode()).digest()
    value = int.from_bytes(digest[:8], "big") % (PRIME - 1) + 1
    return value if value <= PRIME // 2 else value - PRIME


def encode(poly, variables):
    pieces = []
    for position, (exponent, coefficient) in enumerate(poly.terms()):
        require(coefficient.q == 1 and coefficient != 0,
                "slice encoder requires nonzero integer coefficients")
        coefficient = int(coefficient)
        symbolic = [name + (f"^{power}" if power != 1 else "")
                    for name, power in zip(ACTIVE_NAMES, exponent, strict=True)
                    if power]
        magnitude = abs(coefficient)
        factors = [] if magnitude == 1 and symbolic else [str(magnitude)]
        factors.extend(symbolic)
        body = "*".join(factors)
        pieces.append((("-" if coefficient < 0 else "+") if position else
                       ("-" if coefficient < 0 else "")) + body)
    require(pieces, "empty encoded polynomial")
    return "".join(pieces)


def modular_rank(matrix):
    value = [[entry % PRIME for entry in row] for row in matrix]
    rank = 0
    for column in range(len(value[0])):
        pivot = next((row for row in range(rank, len(value))
                      if value[row][column]), None)
        if pivot is None:
            continue
        value[rank], value[pivot] = value[pivot], value[rank]
        inverse = pow(value[rank][column], PRIME - 2, PRIME)
        value[rank] = [entry * inverse % PRIME for entry in value[rank]]
        for row in range(len(value)):
            if row == rank or not value[row][column]:
                continue
            scale = value[row][column]
            value[row] = [(left - scale * right) % PRIME
                          for left, right in zip(value[row], value[rank],
                                                 strict=True)]
        rank += 1
        if rank == len(value):
            break
    return rank


def main():
    try:
        import sympy as sp
    except ImportError:
        sites = sorted((REPO / ".venv/lib").glob("python*/site-packages"))
        require(bool(sites), "sympy unavailable")
        sys.path.append(str(sites[-1]))
        import sympy as sp

    MSOLVE_IO = load("face03130_slice_msolve_io", TOOLKIT)
    source = MSOLVE_IO.read_msolve_input(
        SOURCE_INPUT, strict=True, allow_characteristic_zero=True)
    labels = json.loads(SOURCE_LABELS.read_text())
    export = json.loads(SOURCE_EXPORT.read_text())
    require(source.characteristic == 0 and len(source.polynomials) == 11 and
            labels["source_raw_indices"] == [6, 8, 12, 14, 16, 18, 19, 20]
            and export["result_sha256"] ==
            "38882f87ad3c77f8031cdf8bdb446e7c05e32ff92a198e9be7e3ad60d1bc819d",
            "frozen core8 source interface changed")

    source_names = source.variables
    source_symbols = sp.symbols(" ".join(source_names))
    source_by_name = dict(zip(source_names, source_symbols, strict=True))
    variables = tuple(source_by_name[name] for name in ACTIVE_NAMES)
    locals_map = source_by_name
    expressions = tuple(sp.expand(sp.sympify(
        value.replace("^", "**"), locals=locals_map))
        for value in source.polynomials)
    source_rows = tuple(sp.Poly(value, *variables, domain=sp.QQ)
                        for value in expressions[:8])
    zbase = source_by_name["zbase"]
    base = sp.Poly(sp.Poly(expressions[8] + 1, zbase).nth(1),
                   *variables, domain=sp.QQ)
    require(len(base.terms()) == 16 and base.total_degree() == 17,
            "base-live saturator changed")

    slices = []
    coefficient_matrix = []
    for depth in range(1, 4):
        coefficients = [centered_hash_integer(depth, name)
                        for name in ACTIVE_NAMES]
        constant = centered_hash_integer(depth, "constant")
        polynomial = sp.Poly(
            sum(coefficient * variable for coefficient, variable in
                zip(coefficients, variables, strict=True)) + constant,
            *variables, domain=sp.QQ)
        coefficient_matrix.append(coefficients)
        slices.append({
            "depth": depth,
            "coefficients": dict(zip(ACTIVE_NAMES, coefficients, strict=True)),
            "constant": constant,
            "polynomial": polynomial,
            "encoded": encode(polynomial, variables),
        })
    require(modular_rank(coefficient_matrix) == 3,
            "deterministic slice normals lost rank")

    source_encoded = [encode(poly, variables) for poly in source_rows]
    saturator_encoded = encode(base, variables)
    artifacts = []
    for depth in range(1, 4):
        path = HERE / f"face03130_core8_slice{depth}_p{PRIME}.msolve"
        label_path = HERE / f"face03130_core8_slice{depth}_labels.json"
        polys = source_encoded + [row["encoded"] for row in slices[:depth]] + [
            saturator_encoded]
        row_labels = labels["labels"][:8] + [
            f"AFFINE_SLICE_{index}" for index in range(1, depth + 1)] + [
            "SATURATOR_Aopen_base_live"]
        path.write_text(",".join(ACTIVE_NAMES) + f"\n{PRIME}\n" +
                        ",\n".join(polys) + "\n")
        label_path.write_text(json.dumps({
            "labels": row_labels,
            "source_raw_indices": labels["source_raw_indices"],
            "slice_depth": depth,
            "saturator_label": row_labels[-1],
            "saturator_scope": (
                "A*B*a1*a2*a3*a5*b3*b4*d2*d3*d4; c/H are omitted "
                "component restrictions, not saturators in this screen"),
        }, indent=2, sort_keys=True) + "\n")
        parsed = MSOLVE_IO.read_msolve_input(path, strict=True)
        require(parsed.variables == ACTIVE_NAMES and
                len(parsed.polynomials) == 8 + depth + 1 and
                parsed.polynomial_sha256[:8] == source.polynomial_sha256[:8],
                f"slice{depth} strict source interface changed")
        artifacts.append({
            "depth": depth, "input": path.name,
            "input_sha256": parsed.file_sha256,
            "input_logical_sha256": parsed.logical_sha256,
            "labels": label_path.name,
            "labels_sha256": file_sha(label_path),
            "polynomial_count_including_saturator": len(parsed.polynomials),
        })

    result = {
        "status": "UNAUDITED deterministic modular slice export PASS",
        "prime": PRIME, "seed": SEED,
        "active_variables": list(ACTIVE_NAMES),
        "source_raw_indices": labels["source_raw_indices"],
        "source_input_sha256": source.file_sha256,
        "source_export_sha256": file_sha(SOURCE_EXPORT),
        "base_saturator_terms_degree": [16, 17],
        "base_saturator_sha256": MSOLVE_IO.polynomial_sha256(saturator_encoded),
        "slice_normal_rank_mod_prime": 3,
        "slices": [
            {key: value for key, value in row.items()
             if key not in ("polynomial", "encoded")}
            for row in slices],
        "artifacts": artifacts,
        "scope": (
            "Discovery over one prime only. A unit generic slice does not "
            "prove the unsliced branch empty. Any finite residual must replay "
            "the seven omitted source rows and transported c/H numerators; "
            "leading/infinity exceptions remain separate."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("face03130 core8 slice export: PASS")
    print("slice rank", result["slice_normal_rank_mod_prime"])
    for row in artifacts:
        print(row["depth"], row["input_sha256"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
