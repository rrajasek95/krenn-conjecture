#!/usr/bin/env python3
"""Exact small linear interface for the generic Delta=0 cycle branch.

On ``Delta=b1*d3+b3*d1*d4=0`` put ``x=b3/b1``.  The four upper
cofactor equations have rank two.  Away from ``b1+d1=0`` they solve p3,p4;
their other two rows are precisely two small consistency equations U,V.
Away from ``x=1``, Cof(5,0) then solves a0.  Every remaining literal row is
linear in the three unknowns p1,p2,a5, giving a normalized 6 by 4 augmented
matrix over Q[b0,b1,x,d1,d4].

The branch ``x=1`` is closed directly by a short Laurent unit in U,V.  This
is otherwise a source-faithful reduction theorem, not an emptiness theorem:
the rank conditions of the two exported matrices remain to be decided.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_branch0_cycle_delta_zero_linear_interface.json"
GENERIC = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
           "discover_branch0_k4_cycle_cramer_generic.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("n8_cycle_delta_linear_source", GENERIC)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def polynomial_digest(poly):
    return sha256(str(sp.expand(poly)).encode("ascii")).hexdigest()


def raw_digest(poly):
    payload = [
        [list(monomial), coefficient.numerator, coefficient.denominator]
        for monomial, coefficient in sorted(poly.items())
    ]
    logical = json.dumps(payload, separators=(",", ":"))
    return sha256(logical.encode("ascii")).hexdigest()


def normalize_row(entries, variables):
    denominators = [sp.cancel(entry).as_numer_denom()[1]
                    for entry in entries]
    common = sp.Integer(1)
    for denominator in denominators:
        common = sp.lcm(common, denominator)
    polynomials = [sp.Poly(sp.cancel(entry*common), *variables,
                           domain=sp.QQ)
                   for entry in entries]
    require(any(not polynomial.is_zero for polynomial in polynomials),
            "a normalized interface row became zero")
    # Do not divide a polynomial row gcd here: it need not be a chart unit.
    # Only rational integer content is removed below.  This guard is
    # load-bearing on the Bplus=0 t023 row, whose sole entry has a non-live
    # factor d1^2*x-d1*x+d1+1.
    denominator_lcm = sp.ilcm(*[
        coefficient.q
        for polynomial in polynomials
        for coefficient in polynomial.coeffs()
    ])
    integer = [sp.Poly(polynomial.as_expr()*denominator_lcm,
                       *variables, domain=sp.ZZ)
               for polynomial in polynomials]
    content = 0
    for polynomial in integer:
        for coefficient in polynomial.coeffs():
            content = sp.igcd(content, abs(int(coefficient)))
    require(content, "a normalized row lost integer content")
    integer = [sp.Poly(polynomial.as_expr()/content,
                       *variables, domain=sp.ZZ)
               for polynomial in integer]
    first = next(polynomial.LC() for polynomial in integer
                 if not polynomial.is_zero)
    if first < 0:
        integer = [-polynomial for polynomial in integer]
    return [polynomial.as_expr() for polynomial in integer]


def derive(rows):
    b0, b1, b3, d1, d3, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    variables = (b0, b1, x, d1, d4)
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    ratio = {b3: x*b1, d3: -x*d1*d4}
    upper_ratio = [sp.factor(row.subs(ratio)) for row in upper]
    p3_p4 = sp.solve([upper_ratio[2], upper_ratio[3]],
                     [SOURCE.P[3], SOURCE.P[2]], dict=True,
                     simplify=False)[0]

    u = (b0**2*d1*x - b0**2*x - b0*d1*d4*x - b0*d1*x
         - b0*d4*x + b0 - d1*d4*x - d4)
    v = (b0**2*d1*x + b0**2*x - b0*d1*d4*x**2 - b0*d1*x
         + b0*d4*x**2 - b0 - d1*d4*x**2 + d4*x)

    # The exceptional Cof(5,0) denominator x=1 is actually empty already
    # from U,V.  Put A=(U+V)/(2d1), B=(V-U)/2 and K=b0+d4-2.
    # Then A-B=-2*d4*(b0+1) and B=(b0+1)*K+2, giving the identity below.
    u_one = sp.expand(u.subs(x, 1))
    v_one = sp.expand(v.subs(x, 1))
    k_one = b0 + d4 - 2
    x_one_identity = sp.expand(
        2*d1*d4*(v_one - u_one)
        + ((u_one + v_one) - d1*(v_one - u_one))*k_one)
    require(x_one_identity == 8*d1*d4,
            "the x=1 Laurent unit identity changed")
    require(sp.factor(sp.cancel(upper_ratio[0].subs(p3_p4))
                      + d4*u) == 0,
            "the first Delta consistency row changed")
    require(sp.factor(sp.cancel(upper_ratio[1].subs(p3_p4))
                      - b1**2*d1*d4*x*v) == 0,
            "the second Delta consistency row changed")

    # The displayed 2x2 minor is live when b1+d1 is live.  All 3x3 minors
    # vanish because the upper matrix is a direct sum of two rank-one blocks.
    matrix, _ = sp.linear_eq_to_matrix(upper_ratio, SOURCE.P)
    witness_minor = sp.factor(matrix.extract([2, 3], [2, 3]).det())
    require(witness_minor == -b1*d1*(b1 + d1)**2,
            "the exact-rank-two witness minor changed")
    for row_indices in ((0, 1, 2), (0, 1, 3),
                        (0, 2, 3), (1, 2, 3)):
        for col_indices in ((0, 1, 2), (0, 1, 3),
                            (0, 2, 3), (1, 2, 3)):
            require(sp.factor(matrix.extract(row_indices,
                                             col_indices).det()) == 0,
                    "the Delta upper rank exceeded two")

    labels = ("t_012", "t_013", "cofactor_5_0", "t_023", "t_123",
              "cofactor_0_0", "cofactor_0_3")
    reduced = {label: sp.cancel(rows[label].subs(ratio).subs(p3_p4))
               for label in labels}
    a0_row = reduced["cofactor_5_0"]
    a0_coefficient = sp.factor(sp.diff(a0_row, SOURCE.A0))
    require(a0_coefficient == -b0*d1*d4*(x - 1),
            "the Cof(5,0) solve coefficient changed")
    a0_value = sp.cancel(-a0_row.subs(SOURCE.A0, 0)/a0_coefficient)

    linear_labels = ("t_012", "t_013", "t_023", "t_123",
                     "cofactor_0_0", "cofactor_0_3")
    unknowns = (SOURCE.P[0], SOURCE.P[1], SOURCE.A5)
    normalized = []
    for label in linear_labels:
        value = sp.cancel(reduced[label].subs(SOURCE.A0, a0_value))
        entries = [sp.cancel(sp.diff(value, variable))
                   for variable in unknowns]
        entries.append(sp.cancel(value.subs({variable: 0
                                             for variable in unknowns})))
        # Exact linearity is part of the interface contract.
        reconstruction = sum(entry*variable for entry, variable
                             in zip(entries[:3], unknowns)) + entries[3]
        require(sp.cancel(value - reconstruction) == 0,
                f"{label} ceased to be linear")
        normalized.append(normalize_row(entries, variables))
    # Complementary Bplus=0 branch.  The other diagonal entries of the two
    # parity blocks are now the live pivots, solving p1,p2 and leaving p3,p4.
    minus = {b1: -d1}
    upper_minus = [sp.factor(row.subs(minus)) for row in upper_ratio]
    p1_p2 = sp.solve([upper_minus[2], upper_minus[3]],
                     [SOURCE.P[1], SOURCE.P[0]], dict=True,
                     simplify=False)[0]
    require(sp.factor(sp.cancel(upper_minus[0].subs(p1_p2))
                      + d4*u) == 0,
            "the first Bplus=0 consistency row changed")
    require(sp.factor(sp.cancel(upper_minus[1].subs(p1_p2))
                      - d1**3*d4*x*v) == 0,
            "the second Bplus=0 consistency row changed")
    minus_matrix, _ = sp.linear_eq_to_matrix(upper_minus, SOURCE.P)
    minus_witness = sp.factor(
        minus_matrix.extract([2, 3], [0, 1]).det())
    require(minus_witness == 4*d1**4*d4**2*x**2,
            "the Bplus=0 exact-rank-two witness changed")

    minus_reduced = {
        label: sp.cancel(rows[label].subs(ratio).subs(minus).subs(p1_p2))
        for label in labels
    }
    minus_a0_row = minus_reduced["cofactor_5_0"]
    minus_a0_coefficient = sp.factor(
        sp.diff(minus_a0_row, SOURCE.A0))
    require(minus_a0_coefficient == -b0*d1*d4*(x - 1),
            "the Bplus=0 Cof(5,0) solve coefficient changed")
    minus_a0 = sp.cancel(
        -minus_a0_row.subs(SOURCE.A0, 0)/minus_a0_coefficient)
    minus_variables = (b0, x, d1, d4)
    minus_unknowns = (SOURCE.P[2], SOURCE.P[3], SOURCE.A5)
    minus_normalized = []
    for label in linear_labels:
        value = sp.cancel(minus_reduced[label].subs(SOURCE.A0, minus_a0))
        entries = [sp.cancel(sp.diff(value, variable))
                   for variable in minus_unknowns]
        entries.append(sp.cancel(value.subs({variable: 0
                                             for variable in minus_unknowns})))
        reconstruction = sum(entry*variable for entry, variable
                             in zip(entries[:3], minus_unknowns)) + entries[3]
        require(sp.cancel(value - reconstruction) == 0,
                f"Bplus=0 {label} ceased to be linear")
        minus_normalized.append(normalize_row(entries, minus_variables))

    # The Bplus=0 t023 row is independent of the three remaining unknowns
    # but has a non-live four-term factor W; this is exactly why row-gcd
    # normalization is forbidden above.  W solves x, and U,V then give a
    # two-factor resultant after removing chart units.
    w_minus = d1**2*x - d1*x + d1 + 1
    literal_t023 = sp.factor(
        minus_reduced["t_023"].subs(SOURCE.A0, minus_a0))
    require(sp.cancel(literal_t023/(b0*d1*w_minus/(d4*x))) == 1,
            "the Bplus=0 t023 factor changed")
    x_minus = -(d1 + 1)/(d1*(d1 - 1))
    u_minus = sp.cancel(u.subs(x, x_minus)).as_numer_denom()[0]
    v_minus = sp.cancel(v.subs(x, x_minus)).as_numer_denom()[0]
    qplus = d1**2 + 2*d1 - 1
    p_residual = (
        d1**6*d4**2 + 4*d1**6*d4 + 4*d1**6
        + 4*d1**5*d4**2 + 16*d1**5*d4
        + 7*d1**4*d4**2 + 16*d1**4*d4 + 4*d1**4
        + 8*d1**3*d4**2 + 7*d1**2*d4**2 - 4*d1**2*d4
        + 4*d1*d4**2 + d4**2)
    uv_resultant = sp.factor(sp.resultant(u_minus, v_minus, b0))
    require(uv_resultant == (2*d1*d4*(d1 - 1)*(d1 + 1)
                             * qplus*p_residual),
            "the Bplus=0 W-resultant split changed")

    # The qplus branch has b0=-(d1+2)d4.  The already-solved p2 then equals
    # -1 modulo qplus, contradicting its selected offdiagonal localizer.
    b0_qplus = -(d1 + 2)*d4
    require(sp.rem(sp.Poly(u_minus.subs(b0, b0_qplus), d1),
                   sp.Poly(qplus, d1)).is_zero
            and sp.rem(sp.Poly(v_minus.subs(b0, b0_qplus), d1),
                       sp.Poly(qplus, d1)).is_zero,
            "the qplus U,V solution changed")
    p2_qplus = sp.cancel(p1_p2[SOURCE.P[1]].subs(
        {x: x_minus, b0: b0_qplus}) + 1)
    p2_top, p2_bottom = p2_qplus.as_numer_denom()
    require(sp.rem(sp.Poly(p2_top, d1), sp.Poly(qplus, d1)).is_zero
            and not sp.rem(sp.Poly(p2_bottom, d1),
                           sp.Poly(qplus, d1)).is_zero,
            "the qplus p2=-1 contradiction changed")

    return (variables, u, v, p3_p4, a0_value, linear_labels, normalized,
            x_one_identity, minus_variables, p1_p2, minus_a0,
            minus_normalized, w_minus, p_residual)


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    (variables, u, v, p3_p4, a0_value, labels, normalized,
     x_one_identity, minus_variables, p1_p2, minus_a0,
     minus_normalized, w_minus, p_residual) = derive(rows)
    term_counts = [[len(sp.Poly(entry, *variables).terms())
                    if entry else 0 for entry in row]
                   for row in normalized]

    # Hostile source mutation: flip one literal Cof(0,3) coefficient.  It
    # must change the last normalized row while leaving the setup intact.
    mutated_raw = dict(raw["cofactor_0_3"])
    key = sorted(mutated_raw)[0]
    mutated_raw[key] = -mutated_raw[key]
    mutated_rows = dict(rows)
    mutated_rows["cofactor_0_3"] = SOURCE.expression(mutated_raw)
    mutated_derived = derive(mutated_rows)
    mutated = mutated_derived[6]
    mutated_minus = mutated_derived[11]
    require(normalized[:-1] == mutated[:-1]
            and normalized[-1] != mutated[-1]
            and minus_normalized[:-1] == mutated_minus[:-1]
            and minus_normalized[-1] != mutated_minus[-1],
            "the literal Cof(0,3) mutation did not fire locally")

    source_labels = tuple(f"cofactor_{edge}_0" for edge in range(1, 5)) \
        + ("cofactor_5_0", *labels)
    interface = {
        "status": "UNAUDITED exact Delta=0 linear interface",
        "assumptions": [
            "b0*b1*b3*d1*d3*d4 != 0", "Delta=0",
            "b1+d1 != 0", "x=b3/b1 != 1",
            "all selected-term factors remain live"],
        "variables": [str(variable) for variable in variables],
        "unknowns": ["p1", "p2", "a5"],
        "upper_rank": 2,
        "rank_witness": "-b1*d1*(b1+d1)^2",
        "U": str(u),
        "V": str(v),
        "p3_p4": {str(variable): str(sp.cancel(value))
                    for variable, value in p3_p4.items()},
        "a0": str(a0_value),
        "x_one_unit": str(x_one_identity),
        "row_labels": list(labels),
        "normalized_augmented_matrix": [
            [str(entry) for entry in row] for row in normalized],
        "term_counts": term_counts,
        "row_sha256": [sha256("|".join(map(str, row)).encode("ascii"))
                        .hexdigest() for row in normalized],
        "bplus_zero": {
            "variables": [str(variable) for variable in minus_variables],
            "unknowns": ["p3", "p4", "a5"],
            "rank_witness": "4*d1^4*d4^2*x^2",
            "p1_p2": {str(variable): str(sp.cancel(value))
                       for variable, value in p1_p2.items()},
            "a0": str(minus_a0),
            "forced_W": str(w_minus),
            "W_resultant_remaining_factor": str(p_residual),
            "qplus_conclusion": "1+p2=0",
            "normalized_augmented_matrix": [
                [str(entry) for entry in row]
                for row in minus_normalized],
            "term_counts": [[len(sp.Poly(entry, *minus_variables).terms())
                             if entry else 0 for entry in row]
                            for row in minus_normalized],
            "row_sha256": [sha256("|".join(map(str, row)).encode("ascii"))
                            .hexdigest() for row in minus_normalized],
        },
        "raw_source_sha256": {label: raw_digest(raw[label])
                               for label in source_labels},
        "scope": (
            "The source packet on this localized Delta=0 chart is exactly "
            "U=V=0 plus rank([M|c])=rank(M) for the displayed 6x4 "
            "augmented matrix. This does not decide that condition. The "
            "x=1 branch is empty by the displayed 8*d1*d4 identity. The "
            "b1+d1=0 branch is covered by the second displayed matrix; "
            "there W=0 and the qplus resultant factor is empty by p2=-1, "
            "leaving only the displayed P(d1,d4) factor."
        ),
    }
    logical = json.dumps(interface, sort_keys=True, separators=(",", ":"))
    interface["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(interface, indent=2, sort_keys=True) + "\n")
    print("branch-0 cycle Delta=0 linear interface: PASS")
    print("term counts:", term_counts)
    print("result sha256:", interface["result_sha256"])


if __name__ == "__main__":
    main()
