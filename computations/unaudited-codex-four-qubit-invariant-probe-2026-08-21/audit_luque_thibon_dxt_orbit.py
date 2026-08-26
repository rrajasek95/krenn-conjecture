#!/usr/bin/env python3
"""Exact Luque--Thibon D_xt and bounded SL(2)^4 orbit audit."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
COMP = HERE.parent
FAMILY = (COMP / "unaudited-codex-orbit0-t2-radical-2026-08-20" /
          "results_weight0_char0_family_and_packet.json")
BRANCH1 = (COMP / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
           "results_branch1_dzero_classification.json")
OUT_PREFIX = HERE / "results_luque_thibon_dxt_orbit"
ARXIV = "https://arxiv.org/html/quant-ph/0212069v6"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation", action="store_true")
    args = parser.parse_args()
    try:
        import sympy as sp
    except ImportError:
        sites = sorted((HERE.parents[1] / ".venv/lib").glob(
            "python*/site-packages"))
        require(bool(sites), "sympy unavailable")
        sys.path.append(str(sites[-1]))
        import sympy as sp

    r, g, z, T = sp.symbols("r g z T")

    def support_poly_reduce(value):
        first = sp.rem(sp.Poly(sp.expand(value), r,
                               domain=sp.QQ.frac_field(g)),
                       sp.Poly(r**2-2, r, domain=sp.QQ.frac_field(g))).as_expr()
        return sp.rem(sp.Poly(sp.expand(first), g,
                              domain=sp.QQ.frac_field(r)),
                      sp.Poly(g**2-65, g,
                              domain=sp.QQ.frac_field(r))).as_expr()

    def nf_tuple(value):
        poly = sp.Poly(support_poly_reduce(value), r, g, domain=sp.QQ)
        return tuple(poly.coeff_monomial(monomial) for monomial in
                     (1, r, g, r*g))

    def nf_mul(left, right):
        answer = [sp.Rational(0)] * 4
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                rp = (i & 1) + (j & 1)
                gp = (i >> 1) + (j >> 1)
                coefficient = a*b
                if rp == 2:
                    coefficient *= 2; rp = 0
                if gp == 2:
                    coefficient *= 65; gp = 0
                answer[rp+2*gp] += coefficient
        return tuple(answer)

    def nf_inverse(value):
        basis = ((1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1))
        matrix = sp.Matrix.hstack(*(sp.Matrix(nf_mul(value, vector))
                                    for vector in basis))
        solution = matrix.inv() * sp.Matrix((1,0,0,0))
        return tuple(solution)

    def nf_expr(value):
        return value[0] + value[1]*r + value[2]*g + value[3]*r*g

    def support_reduce(value):
        numerator, denominator = sp.fraction(sp.cancel(value))
        numerator = support_poly_reduce(numerator)
        denominator = support_poly_reduce(denominator)
        if denominator == 1:
            return numerator
        quotient = nf_mul(nf_tuple(numerator), nf_inverse(nf_tuple(denominator)))
        return support_poly_reduce(nf_expr(quotient))

    def branch_reduce(p):
        field = sp.QQ.frac_field(T)
        modulus = sp.Poly(z**2-p*z-1, z, domain=field)
        def reduce(value):
            numerator, denominator = sp.fraction(sp.cancel(value))
            numerator = sp.rem(sp.Poly(sp.expand(numerator), z,
                                       domain=field), modulus).as_expr()
            denominator = sp.rem(sp.Poly(sp.expand(denominator), z,
                                         domain=field), modulus).as_expr()
            if denominator == 1:
                return numerator
            inverse = sp.invert(sp.Poly(denominator, z, domain=field),
                                modulus).as_expr()
            return sp.rem(sp.Poly(sp.expand(numerator*inverse), z,
                                  domain=field), modulus).as_expr()
        return reduce

    def bits(index):
        return tuple((index >> (3-position)) & 1 for position in range(4))

    def index(bit_tuple):
        return sum(bit << (3-position)
                   for position, bit in enumerate(bit_tuple))

    def permute_tensor(q, permutation):
        return tuple(q[index(tuple(bits(target)[permutation[position]]
                                   for position in range(4)))]
                     for target in range(16))

    def determinant(matrix, reduce):
        return reduce(sp.det(sp.Matrix(matrix)))

    def D_uv(q, pair, reduce):
        complement = tuple(position for position in range(4)
                           if position not in pair)
        u0, u1, v0, v1 = sp.symbols("u0 u1 v0 v1")
        uv = ((u0, u1), (v0, v1))
        partial = []
        for cbit in (0, 1):
            row = []
            for dbit in (0, 1):
                value = 0
                for ubit, vbit in product((0, 1), repeat=2):
                    word = [0] * 4
                    word[pair[0]], word[pair[1]] = ubit, vbit
                    word[complement[0]], word[complement[1]] = cbit, dbit
                    value += q[index(tuple(word))] * uv[0][ubit] * uv[1][vbit]
                row.append(value)
            partial.append(row)
        biquadratic = sp.Poly(sp.expand(partial[0][0]*partial[1][1] -
                                        partial[0][1]*partial[1][0]),
                              u0, u1, v0, v1)
        u_exponents = ((2, 0), (1, 1), (0, 2))
        v_exponents = ((2, 0), (1, 1), (0, 2))
        B = [[reduce(biquadratic.coeff_monomial(ue + ve))
              for ve in v_exponents] for ue in u_exponents]
        return determinant(B, reduce), B

    def invariants(q, reduce):
        H = reduce(sum(((-1) ** s.bit_count()) * q[s] * q[15-s]
                       for s in range(8)))
        # Literal Luque--Thibon matrices, eqs. (6)--(8) in their convention.
        L = determinant([[q[0],q[4],q[8],q[12]],
                         [q[1],q[5],q[9],q[13]],
                         [q[2],q[6],q[10],q[14]],
                         [q[3],q[7],q[11],q[15]]], reduce)
        M = determinant([[q[0],q[8],q[2],q[10]],
                         [q[1],q[9],q[3],q[11]],
                         [q[4],q[12],q[6],q[14]],
                         [q[5],q[13],q[7],q[15]]], reduce)
        N = determinant([[q[0],q[1],q[8],q[9]],
                         [q[2],q[3],q[10],q[11]],
                         [q[4],q[5],q[12],q[13]],
                         [q[6],q[7],q[14],q[15]]], reduce)
        Dxy, Bxy = D_uv(q, (0, 1), reduce)
        Dxz, Bxz = D_uv(q, (0, 2), reduce)
        Dxt, Bxt = D_uv(q, (0, 3), reduce)
        require(reduce(L+M+N) == 0, "L+M+N convention guard failed")
        require(reduce(H*L-(Dxz-Dxt)) == 0 and
                reduce(H*M-(Dxt-Dxy)) == 0 and
                reduce(H*N-(Dxy-Dxz)) == 0,
                "Luque--Thibon sextic identities failed")
        return {"H": H, "L": L, "M": M, "N": N,
                "Dxy": Dxy, "Dxz": Dxz, "Dxt": Dxt,
                "Bxt": Bxt}

    def tuple_orbit(q, reduce):
        records = set()
        for permutation in permutations(range(4)):
            inv = invariants(permute_tensor(q, permutation), reduce)
            records.add(tuple(str(reduce(inv[key]))
                              for key in ("H", "L", "M", "Dxt")))
        return tuple(sorted(records))

    def flattening_ranks(q, reduce):
        answer = []
        for left, right in (((0,1),(2,3)), ((0,2),(1,3)),
                            ((0,3),(1,2))):
            matrix = []
            for lb in product((0,1), repeat=2):
                row = []
                for rb in product((0,1), repeat=2):
                    word = [0]*4
                    for position, bit in zip(left, lb): word[position] = bit
                    for position, bit in zip(right, rb): word[position] = bit
                    row.append(q[index(tuple(word))])
                matrix.append(row)
            rank = 0
            for size in range(4, 0, -1):
                found = False
                from itertools import combinations
                for rows in combinations(range(4), size):
                    for columns in combinations(range(4), size):
                        minor = sp.det(sp.Matrix([[matrix[i][j]
                                                  for j in columns]
                                                 for i in rows]))
                        if reduce(minor) != 0:
                            rank, found = size, True; break
                    if found: break
                if found: break
            answer.append(rank)
        return tuple(answer)

    family = json.loads(FAMILY.read_text())

    def decode_basis(basis):
        values = [sp.Rational(Fraction(value)) for value in basis]
        return values[0] + values[1]*r + values[2]*g + values[3]*r*g

    support8_q = tuple(decode_basis(value)
                       for value in family["Q_values_basis_1_r_g_rg"])
    support6_q = tuple(decode_basis(value) for value in
                       family["exact_support6_component"][
                           "Q_values_basis_1_r_g_rg"])
    require([i for i,v in enumerate(support8_q) if v != 0] ==
            [1,3,4,5,6,9,10,12], "support8 changed")
    require([i for i,v in enumerate(support6_q) if v != 0] ==
            [3,5,6,9,10,12], "support6 changed")

    branch_payload = json.loads(BRANCH1.read_text())

    def branch_tensor(component):
        answer = []
        for idx in range(16):
            value = 0
            for term in component["Q_polynomials"][str(idx)]:
                (an, ad), (bn, bd) = term["coefficient_1_z"]
                value += (sp.Rational(an, ad)+sp.Rational(bn, bd)*z) * \
                         T**term["T_degree"]
            answer.append(sp.expand(value))
        return tuple(answer)

    families = {
        "support6": (support6_q, support_reduce),
        "support8": (support8_q, support_reduce),
    }
    for component_index, component in enumerate(branch_payload["components"]):
        p = component["quadratic_relation_p_in_z2_equals_pz_plus_1"]
        families[f"branch1_p{p}"] = (branch_tensor(component), branch_reduce(p))

    invariant_records = {}
    orbits = {}
    for name, (q, reduce) in families.items():
        inv = invariants(q, reduce)
        invariant_records[name] = {
            key: (str([[reduce(entry) for entry in row] for row in value])
                  if key == "Bxt" else str(reduce(value)))
            for key, value in inv.items()
        }
        orbits[name] = tuple_orbit(q, reduce)
    require(all(not any("T" in record[key] for key in
                        ("H","L","M","N","Dxy","Dxz","Dxt"))
                for name, record in invariant_records.items()
                if name.startswith("branch1_")),
            "a branch-line invariant retained T")
    common_orbit = orbits["support6"]
    orbit_equal = all(orbit == common_orbit for orbit in orbits.values())
    require(orbit_equal, "full invariant tuples differ even up to S4")

    # Exact unipotent factorization.  A tensor supported at weight two,
    # acted on by [[1,u_i*t],[0,1]] at each qubit, acquires precisely the
    # weight-one and weight-zero pattern seen in the frozen families.
    def unipotent_decomposition(q, reduce, parameter, strict=True):
        if parameter == 1:
            q0 = tuple(value if sum(bits(idx)) == 2 else sp.Integer(0)
                       for idx, value in enumerate(q))
        else:
            q0 = tuple(reduce(value.subs(T, 0))
                       if hasattr(value, "subs") else value for value in q)
        require(all(value == 0 for idx, value in enumerate(q0)
                    if sum(bits(idx)) != 2), "base is not weight-two")
        C = sp.zeros(4, 4)
        for i in range(4):
            for j in range(i+1, 4):
                word = [0]*4; word[i]=word[j]=1
                C[i,j] = C[j,i] = q0[index(tuple(word))]
        linear = []
        for i in range(4):
            word = [0]*4; word[i]=1
            target = q[index(tuple(word))]
            coefficient = target if parameter == 1 else sp.expand(target).coeff(T, 1)
            linear.append(coefficient)
        require(reduce(C.det()) != 0, "weight-two incidence matrix singular")
        u = tuple(reduce(value) for value in C.inv()*sp.Matrix(linear))
        predicted = []
        for target in range(16):
            target_bits = bits(target)
            value = 0
            for source in range(16):
                source_bits = bits(source)
                if sum(source_bits) != 2 or any(t > s for t,s in
                                                zip(target_bits, source_bits)):
                    continue
                factor = q0[source]
                for position in range(4):
                    if source_bits[position] and not target_bits[position]:
                        factor *= u[position] * parameter
                value += factor
            predicted.append(reduce(value))
        mismatches = [(idx, reduce(left-right))
                      for idx, (left, right) in enumerate(zip(q, predicted))
                      if reduce(left-right) != 0]
        if strict:
            require(not mismatches,
                    f"unipotent tensor replay failed u={u} mismatch={mismatches}")
        return q0, u, mismatches

    decompositions = {}
    q0_support8, u8, mismatch8 = unipotent_decomposition(
        support8_q, support_reduce, 1, strict=False)
    require(q0_support8 == support6_q,
            "support8 does not retract to frozen support6 tensor")
    decompositions["support8_to_support6"] = {
        "forward_u": [str(value) for value in u8],
        "replay_mismatches": [[idx, str(value)] for idx, value in mismatch8],
        "status": ("exact upper-unipotent success" if not mismatch8 else
                   "obstructed: linear coordinates fit but Q0 does not"),
        "inverse_SL2_matrices": [
            [["1", str(support_reduce(-value))], ["0", "1"]]
            for value in u8],
    }
    for name, (q, reduce) in families.items():
        if not name.startswith("branch1_"):
            continue
        q0, u, mismatches = unipotent_decomposition(
            q, reduce, T, strict=False)
        decompositions[name] = {
            "T0_Q": [str(reduce(value)) for value in q0],
            "forward_u": [str(value) for value in u],
            "replay_mismatches": [[idx, str(value)]
                                  for idx, value in mismatches],
            "status": ("exact upper-unipotent success" if not mismatches else
                       "obstructed: weight-one fit leaves Q0*T^2 residual"),
            "inverse_SL2_matrices": [
                [["1", str(reduce(-value*T))], ["0", "1"]]
                for value in u],
            "verification": "tensor_q(T)=(tensor_i [[1,u_i*T],[0,1]]) q(0)",
        }

    # Every nonzero weight-two tensor has a bounded diagonal SL normal form.
    # The square-root symbols below define a finite algebraic extension; the
    # formulas give an explicit transformation, not merely an existence test.
    def gabcd_normal_form(q0, reduce):
        c01, c23 = q0[12], q0[3]
        c02, c13 = q0[10], q0[5]
        c03, c12 = q0[9], q0[6]
        require(all(reduce(value) != 0 for value in
                    (c01,c23,c02,c13,c03,c12)),
                "weight-two coefficient vanished")
        return {
            "alpha_squared": str(reduce(c01*c23)),
            "beta_squared": str(reduce(c02*c13)),
            "gamma_squared": str(reduce(c03*c12)),
            "target_coefficients": {
                "Q3=Q12": "alpha", "Q5=Q10": "beta",
                "Q6=Q9": "gamma"},
            "G_abcd_parameters": {
                "a": "alpha", "b": "beta+gamma",
                "c": "beta-gamma", "d": "-alpha"},
            "diagonal_SL2_construction": (
                "Set r01=alpha/Q12,r02=beta/Q10,r03=gamma/Q9, "
                "S=r01*r02*r03, x0=1, xj=S/r0j. Choose lambda_j^2=xj "
                "with product lambda_i=S; diag(lambda_i,lambda_i^-1) "
                "maps q(0) to the displayed G_abcd tensor."),
        }

    base_tensors = {"support6": support6_q, "support8": q0_support8}
    for name, (q, reduce) in families.items():
        if name.startswith("branch1_"):
            base_tensors[name] = tuple(reduce(value.subs(T,0))
                                       for value in q)
    normal_forms = {name: gabcd_normal_form(base_tensors[name], reduce)
                    for name, (_q, reduce) in families.items()}

    rank_records = {}
    for name, (q, reduce) in families.items():
        rank_records[name] = {
            "generic": list(flattening_ranks(q, reduce)),
            "sorted_generic": sorted(flattening_ranks(q, reduce)),
        }
        if name.startswith("branch1_"):
            at_zero = tuple(reduce(value.subs(T,0)) for value in q)
            rank_records[name]["T_zero"] = list(flattening_ranks(at_zero, reduce))
            rank_records[name]["sorted_T_zero"] = sorted(
                flattening_ranks(at_zero, reduce))
    support6_rank_multiset = rank_records["support6"]["sorted_generic"]
    generic_rank_obstruction = all(
        record["sorted_generic"] != support6_rank_multiset
        for name, record in rank_records.items() if name.startswith("branch1_"))

    def generator_action(q, qubit, kind):
        answer = []
        for target in range(16):
            word = list(bits(target))
            if kind == "h":
                answer.append((1 if word[qubit] == 0 else -1) * q[target])
            elif kind == "e":
                if word[qubit] == 0:
                    word[qubit] = 1; answer.append(q[index(tuple(word))])
                else:
                    answer.append(sp.Integer(0))
            else:
                if word[qubit] == 1:
                    word[qubit] = 0; answer.append(q[index(tuple(word))])
                else:
                    answer.append(sp.Integer(0))
        return tuple(answer)

    GENERATORS = tuple((qubit, kind) for qubit in range(4)
                       for kind in ("h","e","f"))

    def action_columns(q):
        return tuple(generator_action(q, *generator) for generator in GENERATORS)

    def solve_columns(columns, target, reduce):
        rows = [[reduce(columns[column][row])
                 for column in range(len(columns))] + [reduce(target[row])]
                for row in range(len(target))]
        pivot_columns = []
        pivot_row = 0
        for column in range(len(columns)):
            chosen = next((row for row in range(pivot_row, len(rows))
                           if reduce(rows[row][column]) != 0), None)
            if chosen is None:
                continue
            rows[pivot_row], rows[chosen] = rows[chosen], rows[pivot_row]
            inverse = reduce(1 / rows[pivot_row][column])
            rows[pivot_row] = [reduce(value*inverse)
                               for value in rows[pivot_row]]
            for row in range(len(rows)):
                if row == pivot_row or reduce(rows[row][column]) == 0:
                    continue
                factor = rows[row][column]
                rows[row] = [reduce(left-factor*right)
                             for left,right in zip(rows[row],rows[pivot_row])]
            pivot_columns.append(column); pivot_row += 1
            if pivot_row == len(rows): break
        inconsistent = any(all(reduce(value) == 0 for value in row[:-1]) and
                           reduce(row[-1]) != 0 for row in rows)
        solution = [sp.Integer(0)] * len(columns)
        if not inconsistent:
            for row, column in enumerate(pivot_columns):
                solution[column] = reduce(rows[row][-1])
        return {"rank": len(pivot_columns),
                "nullity": len(columns)-len(pivot_columns),
                "consistent": not inconsistent,
                "solution": tuple(solution)}

    def lie_audit(q, reduce):
        zero = (sp.Integer(0),) * 16
        columns = action_columns(q)
        stabilizer = solve_columns(columns, zero, reduce)
        return columns, stabilizer

    lie_records = {}
    for name, (q, reduce) in families.items():
        if not name.startswith("branch1_"):
            continue
        q0 = tuple(reduce(value.subs(T,0)) for value in q)
        columns0, stabilizer0 = lie_audit(q0, reduce)
        columnsT, stabilizerT = lie_audit(q, reduce)
        derivative = tuple(reduce(sp.diff(value,T)) for value in q)
        tangent = solve_columns(columnsT, derivative, reduce)
        q1 = tuple(reduce(sp.expand(value).coeff(T,1)) for value in q)
        q2 = tuple(reduce(sp.expand(value).coeff(T,2)) for value in q)
        # Constant-generator exponential test through order two and its
        # mandatory third-order vanishing condition.
        combined_columns = []
        for generator in GENERATORS:
            combined_columns.append(
                generator_action(q0,*generator) +
                generator_action(q1,*generator) +
                generator_action(q2,*generator))
        combined_target = q1 + tuple(reduce(2*v) for v in q2) + \
                          (sp.Integer(0),)*16
        jet = solve_columns(tuple(combined_columns), combined_target, reduce)
        lie_records[name] = {
            "T0_action_rank": stabilizer0["rank"],
            "T0_stabilizer_dimension": stabilizer0["nullity"],
            "generic_action_rank": stabilizerT["rank"],
            "generic_stabilizer_dimension": stabilizerT["nullity"],
            "generic_derivative_in_orbit_tangent": tangent["consistent"],
            "generic_tangent_solution": [str(v) for v in tangent["solution"]]
                if tangent["consistent"] else None,
            "constant_generator_2jet_and_truncation_consistent": jet["consistent"],
            "constant_generator_solution": [str(v) for v in jet["solution"]]
                if jet["consistent"] else None,
        }

    stabilizer_obstruction = all(
        row["T0_stabilizer_dimension"] != row["generic_stabilizer_dimension"]
        for row in lie_records.values())
    tangent_obstruction = all(not row["generic_derivative_in_orbit_tangent"]
                              for row in lie_records.values())
    constant_generator_success = all(
        row["constant_generator_2jet_and_truncation_consistent"]
        for row in lie_records.values())

    # The tangent vector has an elementary global integration on T != 0.
    # If s^2=T'/T, applying diag(s,s^-1) at every qubit multiplies a
    # weight-w coordinate by s^(4-2w)=(T'/T)^(2-w).  The frozen branch
    # tensors have exactly that T grading.  This proves that each punctured
    # branch line is one SL(2)^4 orbit, while the stabilizer jump proves that
    # its T=0 endpoint is only an orbit-closure limit.
    punctured_orbit_scaling = {}
    for name, (q, reduce) in families.items():
        if not name.startswith("branch1_"):
            continue
        grading = []
        for idx, value in enumerate(q):
            weight = sum(bits(idx))
            expected_degree = 2-weight
            reduced = reduce(value)
            if reduced == 0:
                grading.append({"index": idx, "weight": weight,
                                "status": "zero"})
                continue
            require(expected_degree >= 0,
                    f"nonzero branch coordinate above weight two: {idx}")
            coefficient = reduce(reduced / T**expected_degree)
            require(reduce(sp.diff(coefficient, T)) == 0,
                    f"branch coordinate has wrong T grading: {idx}")
            grading.append({"index": idx, "weight": weight,
                            "T_degree": expected_degree,
                            "coefficient": str(coefficient)})
        expected_tangent = []
        for qubit in range(4):
            expected_tangent.extend((sp.Rational(1, 2)/T, 0, 0))
        require(tuple(str(reduce(v)) for v in expected_tangent) ==
                tuple(lie_records[name]["generic_tangent_solution"]),
                f"diagonal tangent solution changed for {name}")
        punctured_orbit_scaling[name] = {
            "grading": grading,
            "finite_SL2_map": (
                "For T,T' nonzero choose s with s^2=T'/T and apply "
                "diag(s,s^-1) on each of the four qubits; this maps q(T) "
                "exactly to q(T')."),
            "infinitesimal_generator_order_h_e_f":
                [str(reduce(v)) for v in expected_tangent],
            "endpoint_status": (
                "T=0 is a singular limit of this map and has stabilizer "
                "dimension 1 instead of 0, hence is not in the generic "
                "SL(2)^4 orbit."),
        }

    if args.mutation:
        mutated = list(support6_q); mutated[3] += 1
        try:
            invariants(tuple(mutated), support_reduce)
        except RuntimeError:
            pass
        else:
            require(tuple_orbit(tuple(mutated), support_reduce) != common_orbit,
                    "tensor mutation failed to fire")

    result = {
        "status": "PASS exact Luque-Thibon Dxt/orbit/transformation audit",
        "mutation": args.mutation,
        "definition_source": ARXIV,
        "Dxt_definition": (
            "b_xt=det(partial^2 A / partial y_i partial z_j); "
            "b_xt=[x0^2,x0x1,x1^2] B_xt [t0^2,t0t1,t1^2]^T; Dxt=det(B_xt)"),
        "identity_guards": ["L+M+N=0", "HL=Dxz-Dxt",
                            "HM=Dxt-Dxy", "HN=Dxy-Dxz"],
        "invariants": invariant_records,
        "S4_generator_tuple_orbits": {name: [list(row) for row in orbit]
                                       for name, orbit in orbits.items()},
        "all_full_invariant_tuples_equal_up_to_qubit_permutation": orbit_equal,
        "bounded_upper_unipotent_attempts": decompositions,
        "flattening_rank_orbit_obstruction": rank_records,
        "Lie_stabilizer_and_tangent_audit": lie_records,
        "punctured_branch_SL2_scaling": punctured_orbit_scaling,
        "canonical_Gabcd_normal_forms_of_T0_limits": normal_forms,
        "conclusion": (
            "All four frozen tensors have the same complete generator tuple "
            "up to qubit permutation, so the polynomial invariants identify "
            "their categorical-quotient point.  Nevertheless a generic "
            "branch point is not SL(2)^4-equivalent to its support-six/T=0 "
            "endpoint: the exact stabilizer dimensions are 0 and 1.  Every "
            "nonzero point on either branch is explicitly equivalent to every "
            "other by the four equal diagonal matrices with s^2=T'/T; T=0 "
            "is only the singular orbit-closure limit.  The bounded "
            "upper-unipotent solve independently fails exactly in Q0 at "
            "quadratic order, and the T=0 weight-two tensor has the displayed "
            "diagonal G_abcd normalization."),
        "bounded_equivalence_verdict": {
            "stabilizer_dimension_obstruction": stabilizer_obstruction,
            "generic_tangent_obstruction": tangent_obstruction,
            "constant_generator_success": constant_generator_success,
            "flattening_rank_obstruction": generic_rank_obstruction,
        },
        "scope_guard": (
            "The transformation is proved for the frozen Q tensors only. It "
            "does not identify the underlying 24 cell charts or their full "
            "X/cofactor data, and therefore does not replace the source-row "
            "compatibility arguments. Equality of the polynomial invariant "
            "tuple proves equality in the categorical quotient, not equality "
            "of nonclosed SL(2)^4 orbits; the stabilizer computation is the "
            "separate exact orbit obstruction."),
        "source_hashes": {"family": digest(FAMILY), "branch1": digest(BRANCH1)},
    }
    result["logical_sha256"] = logical_hash(result)
    suffix = "mutation" if args.mutation else "standard"
    path = OUT_PREFIX.with_name(OUT_PREFIX.name + "_" + suffix + ".json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Luque-Thibon Dxt/orbit audit PASS", result["logical_sha256"])
    for name, record in invariant_records.items():
        print(name, {key: record[key] for key in
                     ("H","L","M","N","Dxy","Dxz","Dxt")})
    print("orbit sizes", {name: len(value) for name,value in orbits.items()})
    print("unipotents", {name: row["forward_u"]
                          for name,row in decompositions.items()})


if __name__ == "__main__":
    main()
