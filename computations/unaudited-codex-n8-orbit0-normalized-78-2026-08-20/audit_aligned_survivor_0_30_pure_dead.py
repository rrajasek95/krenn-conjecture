#!/usr/bin/env python3
"""Exact pure-death certificate for aligned survivor (branch 0, term 30).

The 15 nonzero specialized source rows are rederived from the raw four-site
permanent, triangle, and cofactor polynomials.  After localizing only the six
selected permanent-term coordinates, their saturated ideal contains the
literal pure Hafnian.  Thus this aligned chart has no pure-live point; this is
strictly a statement about the displayed aligned zero-cell boundary chart.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "audit_aligned_survivor_1_38_normal_form.py"
OUT = HERE / "results_aligned_survivor_0_30_pure_dead.json"
BRANCH = 0
TERM_MASK = 30
EXPECTED_LABELS = (
    "t_012", "t_013", "t_023", "t_123",
    "cofactor_0_0", "cofactor_0_3", "cofactor_1_0", "cofactor_1_3",
    "cofactor_2_0", "cofactor_2_3", "cofactor_3_0", "cofactor_3_3",
    "cofactor_4_0", "cofactor_4_3", "cofactor_5_3",
)
EXPECTED_Q_NORMAL_FORMS = (
    "-3*a0*a5", "a3*b2+a1*b4", "a4*b1+a2*b3", "-a0",
    "2*a0", "-b2", "-b1", "0", "2*a0", "-b4", "-b3", "0",
    "a2*b1*b4^2+a0*b1*b4", "0", "0", "1",
)
EXPECTED_BASIS_SHA256 = (
    "87c1e61620ca203c1a3f631db43bc6f14420f04000d93ed28664c5c17611317f"
)


def load_core():
    spec = importlib.util.spec_from_file_location("n8_0_30_core", CORE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_core()
SCREEN = CORE.SCREEN


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def entries():
    answer = []
    for edge in range(6):
        a_value, b_value = CORE.variable(edge), CORE.variable(6 + edge)
        if TERM_MASK & (1 << edge):
            answer.extend((a_value, b_value,
                           CORE.variable(6 + edge, -1, -1), {}))
        else:
            answer.extend((a_value, b_value, {},
                           CORE.variable(edge, -1, -1)))
    return tuple(answer)


ENTRIES = entries()


def substitute(raw_poly):
    answer = {}
    for monomial, coefficient in raw_poly.items():
        term = CORE.scale(CORE.ONE, coefficient)
        for raw_variable in monomial:
            term = CORE.multiply(term, ENTRIES[raw_variable])
        answer = CORE.add(answer, term)
    return answer


def raw_labels():
    labels = ["e_01", "e_02", "e_03", "e_12", "e_13", "e_23"]
    labels += ["t_012", "t_013", "t_023", "t_123"]
    for edge in range(6):
        labels += [f"cofactor_{edge}_0", f"cofactor_{edge}_3"]
    return tuple(labels)


def derive_rows_and_targets():
    equations, hafnian_raw = SCREEN.PROBE.equations(
        SCREEN.branch_bits(BRANCH))
    labelled = []
    seen = set()
    for label, raw in zip(raw_labels(), equations):
        specialized = substitute(raw)
        if specialized:
            cleared = CORE.clear_denominators(specialized)
            encoded = CORE.singular(cleared)
            if encoded in seen:
                continue
            seen.add(encoded)
            labelled.append((label, cleared))
    require(tuple(label for label, _ in labelled) == EXPECTED_LABELS,
            "nonzero raw source-row labels changed")
    hafnian = CORE.clear_denominators(substitute(hafnian_raw))
    q_polys = tuple(CORE.clear_denominators(
        substitute(SCREEN.q_poly(index))) for index in range(16))
    return labelled, hafnian, q_polys


def live_product():
    return "*".join(("b" if TERM_MASK & (1 << edge) else "a")
                    + str(edge) for edge in range(6))


def singular_run(characteristic, rows, hafnian, q_polys):
    variables = ",".join([f"a{index}" for index in range(6)]
                         + [f"b{index}" for index in range(6)] + ["z"])
    command = (
        f"ring R={characteristic},({variables}),dp;"
        f"ideal I={','.join(CORE.singular(row) for _, row in rows)},"
        f"z*{live_product()}-1;ideal G=slimgb(I);"
        'print("BEGIN_BASIS");G;print("END_BASIS");print(dim(G));'
        f"poly H={CORE.singular(hafnian)};"
        'print("BEGIN_H");reduce(H,G);print("END_H");'
        + "".join(f"poly q{index}={CORE.singular(poly)};"
                  f'print("BEGIN_Q{index}");reduce(q{index},G);'
                  f'print("END_Q{index}");'
                  for index, poly in enumerate(q_polys))
        + 'print("BEGIN_MUTATION");reduce(H+1,G);print("END_MUTATION");quit;'
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=30, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"Singular characteristic {characteristic} failed")
    lines = completed.stdout.splitlines()

    def between(left, right):
        return tuple(lines[lines.index(left) + 1:lines.index(right)])

    basis_rows = between("BEGIN_BASIS", "END_BASIS")
    basis = tuple(line.split("=", 1)[1] for line in basis_rows)
    dimension = int(lines[lines.index("END_BASIS") + 1])
    h_remainder = between("BEGIN_H", "END_H")
    q_remainders = tuple("\n".join(between(f"BEGIN_Q{index}",
                                             f"END_Q{index}"))
                         for index in range(16))
    mutation = between("BEGIN_MUTATION", "END_MUTATION")
    require(h_remainder == ("0",), "pure Hafnian did not reduce to zero")
    require(mutation == ("1",), "H+1 must-fire mutation did not survive")
    return basis, dimension, q_remainders


def main():
    rows, hafnian, q_polys = derive_rows_and_targets()
    exact_basis, dimension, exact_q = singular_run(0, rows, hafnian, q_polys)
    require(len(exact_basis) == 37 and dimension == 5,
            "exact saturated ideal size/dimension changed")
    basis_sha = sha256("\n".join(exact_basis).encode("ascii")).hexdigest()
    require(basis_sha == EXPECTED_BASIS_SHA256,
            "exact saturated Groebner basis changed")
    require(exact_q == EXPECTED_Q_NORMAL_FORMS,
            "exact Q normal forms changed")
    modular = {}
    for prime in (1009, 1013):
        basis, mod_dimension, _ = singular_run(prime, rows, hafnian, q_polys)
        require(mod_dimension == 5, "modular saturated dimension changed")
        modular[str(prime)] = {"basis_size": len(basis),
                               "dimension": mod_dimension,
                               "H_remainder": "0"}
    result = {
        "status": "UNAUDITED exact aligned-chart pure-death certificate",
        "joint_chart": [BRANCH, TERM_MASK],
        "scope": ("only the aligned zero-cell boundary chart; localization "
                  "uses the six selected permanent-term coordinates"),
        "derived_source_row_labels": list(EXPECTED_LABELS),
        "derived_source_row_count": len(rows),
        "exact_saturated_basis_size": len(exact_basis),
        "exact_saturated_dimension": dimension,
        "exact_basis_sha256": basis_sha,
        "exact_H_remainder": "0",
        "exact_Q_normal_forms": list(exact_q),
        "must_fire_H_plus_one_remainder": "1",
        "modular_controls": modular,
        "consequence": ("the literal pure Hafnian vanishes throughout this "
                        "aligned chart, so it supplies no pure-live left point"),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("aligned survivor (0,30) pure-death certificate: PASS")
    print("source rows / exact basis / dimension:", len(rows),
          len(exact_basis), dimension)
    print("exact/modular H remainders:", 0, 0, 0)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
