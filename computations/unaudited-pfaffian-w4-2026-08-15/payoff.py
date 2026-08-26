#!/usr/bin/env python3
"""UNAUDITED PROBE (W4 / Route F.1) -- the payoff test: does the Pfaffian frame
make the blocking structure classical?

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Three things are tested.

(C1) The two named blocking mechanisms and their exact reach.
     M1  rank mu_pq = 36 (the multiplication map Xi_a (x) .. (x) Xi_d ->
         Sym^2 V_p (x) Sym^2 V_q is onto)               => every kappa_c^2 blocks.
     M2* Xi_x meets the coordinate 2-plane D_c = <e_c (+) 0, 0 (+) e_c> for
         every x in U, with generators (a_x e_c, b_x e_c), and the binary-quartic
         middle coefficient  e2(a,b) = [t^2] prod_x (a_x t + b_x)  is nonzero
                                                        => kappa_c^2 blocks,
         because then E(eta) = 2 e2(a,b) kappa_c^2 exactly.
     Contrapositive tested: kappa_c^2 free => rank mu <= 35 AND some x has
     Xi_x n D_c = 0 or e2 = 0.

(C2) THE DEGREE-3 LAW (new; the frame's own prediction).  Cauchy:
       Sym^d(V_p (x) V_q) = (+)_{lambda |- d, l(lambda)<=3} S_lambda V_p (x) S_lambda V_q.
     I_2 = span of the error components sits in S_(2) (x) S_(2) = W, missing
     S_(11) (x) S_(11) (the 2x2 minors).  Hence
       I_3 = (V_p (x) V_q) . I_2  sits in  (S_3 (x) S_3) (+) (S_21 (x) S_21),
     missing  Lambda^3 V_p (x) Lambda^3 V_q = <det K>.  So a degree-3
     L-monomial can block only if its "mixed determinant" vanishes:
       D(X,Y,Z) = sum_{sigma,tau in S_3} sgn(sigma)sgn(tau)
                  X_{sigma1 tau1} Y_{sigma2 tau2} Z_{sigma3 tau3}.
     Consequences (all verified exhaustively below):
       s^3            blocks =>  det A_pq = 0
       s^2 kappa_c    blocks =>  the (c,c) cofactor of A_pq vanishes
       s kappa_c kappa_c'  blocks =>  (A_pq)_{c'' c''} = 0 (c'' the third colour)
       kappa_0 kappa_1 kappa_2  NEVER blocks
       every monomial with a repeated kappa is unconditional.
     In degree 4 and above no such obstruction exists (Pieri: every lambda |- d
     with at most three rows is reachable), which is why P2 saw minimal
     blocking degrees 2,3,4,5 but pattern laws only at low degree.

(C3) Witness correlation: every witness-carrying pair must have rank mu <= 35.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(
    HERE, "..", "unaudited-witness-splitting-p2-2026-08-15")))

from wsplit_core import (KAPPA_VARS, PAIRS, Source, decide_pair, in_row_space,
                         lin_mul, lin_zero, matrix_rank, quad_add, quad_vector,
                         random_matrix, random_source, row_space, require)
from translate import (PfaffFrame, RANGE3, anchored_coordinate_source, delta,
                       lambda_projection, psi, rank_of, solve_in_span, survey)

SIGN3 = {p: (1 if sum(1 for i in range(3) for j in range(i + 1, 3)
                      if p[i] > p[j]) % 2 == 0 else -1)
         for p in permutations(range(3))}


# --------------------------------------------------- D_c incidence (M2*)

def dc_basis(colour):
    """The coordinate 2-plane D_c = <e_c (+) 0, 0 (+) e_c> in C^6."""
    first = [Fraction(0)] * 6
    second = [Fraction(0)] * 6
    first[colour] = Fraction(1)
    second[3 + colour] = Fraction(1)
    return [first, second]


def intersect_with_dc(xis, colour):
    """Xi n D_c as a list of (a, b) with the intersection vector (a e_c, b e_c).

    Xi = span of the three xi's.  Solve for the vectors of Xi whose only
    nonzero coordinates are the two D_c ones.  Exact, by elimination.
    """
    rows = []
    for coefficient in range(3):
        rows.append(list(xis[coefficient]))
    # find all combinations lambda with (sum lambda_i xi_i) killed outside D_c
    # -> linear system in 3 unknowns with 4 equations
    equations = []
    for index in range(6):
        if index == colour or index == 3 + colour:
            continue
        equations.append([rows[k][index] for k in range(3)])
    kernel = nullspace(equations, 3)
    out = []
    for vector in kernel:
        a = sum(vector[k] * rows[k][colour] for k in range(3))
        b = sum(vector[k] * rows[k][3 + colour] for k in range(3))
        out.append((a, b))
    return out


def nullspace(equations, nvars):
    """Exact kernel basis of a list of linear equations in nvars unknowns."""
    rows = [list(map(Fraction, eq)) for eq in equations]
    pivots = []
    r = 0
    for column in range(nvars):
        pivot = None
        for index in range(r, len(rows)):
            if rows[index][column] != 0:
                pivot = index
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        head = rows[r]
        for index in range(len(rows)):
            if index != r and rows[index][column] != 0:
                factor = rows[index][column] / head[column]
                rows[index] = [a - factor * b for a, b in zip(rows[index], head)]
        pivots.append(column)
        r += 1
    free = [c for c in range(nvars) if c not in pivots]
    basis = []
    for f in free:
        vector = [Fraction(0)] * nvars
        vector[f] = Fraction(1)
        for index, column in enumerate(pivots):
            vector[column] = -rows[index][f] / rows[index][column]
        basis.append(vector)
    return basis


def e2_mixed(pairs):
    """[t^2] prod_x (a_x t + b_x) for four (a,b)."""
    total = Fraction(0)
    for T in combinations(range(4), 2):
        rest = [k for k in range(4) if k not in T]
        total += (pairs[T[0]][0] * pairs[T[1]][0]
                  * pairs[rest[0]][1] * pairs[rest[1]][1])
    return total


def m2star(frame: PfaffFrame, colour):
    """(reachable, forced_zero): can M2* be fired at this colour?"""
    generators = {}
    for x in frame.U:
        inter = intersect_with_dc(frame.xis[x], colour)
        if not inter:
            return False, False
        generators[x] = inter
    # if some site has a 2-dimensional intersection we may choose freely;
    # otherwise the four (a,b) are fixed up to scale and e2 is determined.
    if all(len(v) == 1 for v in generators.values()):
        value = e2_mixed([generators[x][0] for x in frame.U])
        return value != 0, value == 0
    # 2-dimensional somewhere: search a nonzero choice over a small grid
    options = []
    for x in frame.U:
        vectors = generators[x]
        if len(vectors) == 1:
            options.append([vectors[0]])
        else:
            options.append([
                (sum(c * v[0] for c, v in zip(coeffs, vectors)),
                 sum(c * v[1] for c, v in zip(coeffs, vectors)))
                for coeffs in ((1, 0), (0, 1), (1, 1), (1, -1), (2, 1))])
    for choice in product(*options):
        if e2_mixed(list(choice)) != 0:
            return True, False
    return False, True


# ---------------------------------------------------- the degree-3 law

def mixed_determinant(X, Y, Z):
    total = Fraction(0)
    for sigma in permutations(range(3)):
        for tau in permutations(range(3)):
            total += (SIGN3[sigma] * SIGN3[tau]
                      * X[sigma[0]][tau[0]] * Y[sigma[1]][tau[1]]
                      * Z[sigma[2]][tau[2]])
    return total


def epsilon(triple):
    a, b, c = triple
    if len({a, b, c}) < 3:
        return 0
    sign = 1
    seq = [a, b, c]
    for i in range(3):
        for j in range(i + 1, 3):
            if seq[i] > seq[j]:
                sign = -sign
    return sign


def det_projection(cubic):
    """The Lambda^3 V_p (x) Lambda^3 V_q coefficient of a cubic in the K_ij.

    The projection Sym^3(V_p (x) V_q) -> Lambda^3 (x) Lambda^3 sends the basis
    monomial (e_i1 (x) e_j1)(e_i2 (x) e_j2)(e_i3 (x) e_j3) to
    eps(i1i2i3) eps(j1j2j3); it is well defined because both epsilons change
    sign together under a transposition of the three factors.
    """
    total = Fraction(0)
    for key, value in cubic.items():
        rows = tuple(k // 3 for k in key)
        columns = tuple(k % 3 for k in key)
        total += value * epsilon(rows) * epsilon(columns)
    return total


def cubic_of_monomial(forms):
    """Product of three linear forms as a dict on sorted variable triples."""
    out = {}
    for i in range(9):
        if forms[0][i] == 0:
            continue
        for j in range(9):
            if forms[1][j] == 0:
                continue
            for k in range(9):
                if forms[2][k] == 0:
                    continue
                key = tuple(sorted((i, j, k)))
                out[key] = out.get(key, Fraction(0)) + \
                    forms[0][i] * forms[1][j] * forms[2][k]
    return {key: value for key, value in out.items() if value != 0}


def matrix_of_form(form):
    return [[form[3 * i + j] for j in RANGE3] for i in RANGE3]


CUBIC_KEYS = tuple(sorted(set(tuple(sorted(t))
                              for t in product(range(9), repeat=3))))
CUBIC_INDEX = {key: n for n, key in enumerate(CUBIC_KEYS)}
PRIME = (1 << 61) - 1


def cubic_vector(cubic):
    vector = [Fraction(0)] * len(CUBIC_KEYS)
    for key, value in cubic.items():
        vector[CUBIC_INDEX[key]] = value
    return vector


def quad_to_cubic(quad, variable):
    out = {}
    for (u, v), value in quad.items():
        key = tuple(sorted((u, v, variable)))
        out[key] = out.get(key, Fraction(0)) + value
    return out


def to_modp(vector, prime=PRIME):
    out = []
    for value in vector:
        value = Fraction(value)
        out.append(value.numerator % prime
                   * pow(value.denominator % prime, prime - 2, prime) % prime)
    return out


def row_space_modp(rows, prime=PRIME):
    basis, pivots = [], []
    for vector in rows:
        row = list(vector)
        for pivot, brow in zip(pivots, basis):
            if row[pivot]:
                factor = row[pivot] * pow(brow[pivot], prime - 2, prime) % prime
                row = [(a - factor * b) % prime for a, b in zip(row, brow)]
        pivot = next((n for n, value in enumerate(row) if value), None)
        if pivot is None:
            continue
        basis.append(row)
        pivots.append(pivot)
    return list(zip(pivots, basis))


def in_row_space_modp(basis, vector, prime=PRIME):
    row = list(vector)
    for pivot, brow in basis:
        if row[pivot]:
            factor = row[pivot] * pow(brow[pivot], prime - 2, prime) % prime
            row = [(a - factor * b) % prime for a, b in zip(row, brow)]
    return not any(row)


def degree3_ideal_basis(frame: PfaffFrame, exact=False):
    """I_3 = (V_p (x) V_q) . I_2.  Uses the reduced basis of I_2 (<=36 rows)."""
    quads = []
    seen = row_space([quad_vector(q) for q in frame.components.values() if q])
    for _pivot, row in seen:
        quad = {}
        from wsplit_core import QUAD_KEYS
        for n, value in enumerate(row):
            if value:
                quad[QUAD_KEYS[n]] = value
        quads.append(quad)
    rows = []
    for quad in quads:
        for variable in range(9):
            rows.append(cubic_vector(quad_to_cubic(quad, variable)))
    if exact:
        return ("Q", row_space(rows))
    return ("modp", row_space_modp([to_modp(row) for row in rows]))


def cubic_in_ideal(basis, cubic):
    kind, data = basis
    if kind == "Q":
        return in_row_space(data, cubic_vector(cubic))
    return in_row_space_modp(data, to_modp(cubic_vector(cubic)))


def check_degree3_law(trials=6, seed=31, exact=False):
    """det K is never in I_3, and the degree-3 L-monomial laws."""
    rng = random.Random(seed)
    modes = ("generic", "sparse", "lowrank", "diagonal", "binary")
    det_cubic = {}
    for sigma in permutations(range(3)):
        key = tuple(sorted(3 * i + sigma[i] for i in range(3)))
        det_cubic[key] = det_cubic.get(key, Fraction(0)) + SIGN3[sigma]
    stats = {"pairs": 0, "det_in_I3": 0, "law_violations": 0,
             "k012_blocks": 0, "s3_blocks": 0, "s3_blocks_det_nonzero": 0,
             "s2k_blocks": 0, "s2k_blocks_cofactor_nonzero": 0,
             "skk_blocks": 0, "skk_blocks_entry_nonzero": 0,
             "arithmetic": "Q" if exact else "mod 2^61-1"}
    for index in range(trials):
        source = random_source(rng, modes[index % len(modes)])
        for p, q in PAIRS:
            frame = PfaffFrame(source, p, q)
            basis = degree3_ideal_basis(frame, exact=exact)
            stats["pairs"] += 1
            if cubic_in_ideal(basis, det_cubic):
                stats["det_in_I3"] += 1
            A = matrix_of_form(frame.pd.s)
            kforms = []
            for colour in RANGE3:
                form = lin_zero()
                form[KAPPA_VARS[colour]] = Fraction(1)
                kforms.append(form)
            Ks = [matrix_of_form(f) for f in kforms]
            monomials = {
                "sss": ([frame.pd.s] * 3, [A, A, A]),
                "k012": (kforms, Ks),
            }
            for colour in RANGE3:
                monomials["ssk%d" % colour] = (
                    [frame.pd.s, frame.pd.s, kforms[colour]],
                    [A, A, Ks[colour]])
            for c, cc in combinations(RANGE3, 2):
                monomials["sk%dk%d" % (c, cc)] = (
                    [frame.pd.s, kforms[c], kforms[cc]], [A, Ks[c], Ks[cc]])
            for colour in RANGE3:
                monomials["skk%d" % colour] = (
                    [frame.pd.s, kforms[colour], kforms[colour]],
                    [A, Ks[colour], Ks[colour]])
            for name, (forms, matrices) in monomials.items():
                cubic = cubic_of_monomial(forms)
                if not cubic:
                    continue
                blocks = cubic_in_ideal(basis, cubic)
                mixed = mixed_determinant(*matrices)
                projected = det_projection(cubic)
                require(projected == mixed,
                        "det projection != mixed determinant for " + name)
                if blocks and mixed != 0:
                    stats["law_violations"] += 1
                if name == "k012" and blocks:
                    stats["k012_blocks"] += 1
                if name == "sss" and blocks:
                    stats["s3_blocks"] += 1
                    if mixed != 0:
                        stats["s3_blocks_det_nonzero"] += 1
                if name.startswith("ssk") and blocks:
                    stats["s2k_blocks"] += 1
                    if mixed != 0:
                        stats["s2k_blocks_cofactor_nonzero"] += 1
                if name.startswith("sk") and len(name) == 5 and blocks:
                    stats["skk_blocks"] += 1
                    if mixed != 0:
                        stats["skk_blocks_entry_nonzero"] += 1
    return stats


def check_mixed_determinant_meanings():
    """The three named readings of D(X,Y,Z), exhaustively over 0/1 supports."""
    checked = 0
    for support in product((0, 1), repeat=9):
        A = [[Fraction(support[3 * i + j]) for j in RANGE3] for i in RANGE3]
        Ks = []
        for colour in RANGE3:
            matrix = [[Fraction(0)] * 3 for _ in range(3)]
            matrix[colour][colour] = Fraction(1)
            Ks.append(matrix)
        det = sum(SIGN3[s] * A[0][s[0]] * A[1][s[1]] * A[2][s[2]]
                  for s in permutations(range(3)))
        require(mixed_determinant(A, A, A) == 6 * det, "D(A,A,A) != 6 det A")
        for colour in RANGE3:
            others = [k for k in RANGE3 if k != colour]
            cofactor = (A[others[0]][others[0]] * A[others[1]][others[1]]
                        - A[others[0]][others[1]] * A[others[1]][others[0]])
            require(mixed_determinant(A, A, Ks[colour]) == 2 * cofactor,
                    "D(A,A,E_cc) != 2 * cofactor")
            require(mixed_determinant(A, Ks[colour], Ks[colour]) == 0,
                    "D(A,E_cc,E_cc) != 0")
        for c, cc in combinations(RANGE3, 2):
            third = [k for k in RANGE3 if k not in (c, cc)][0]
            require(mixed_determinant(A, Ks[c], Ks[cc]) == A[third][third],
                    "D(A,E_cc,E_c'c') != A_{c''c''}")
        require(mixed_determinant(Ks[0], Ks[1], Ks[2]) == 1,
                "D(E00,E11,E22) != 1")
        checked += 1
    return checked


# --------------------------------------------------------- C1 statistics

def payoff_survey(label, trials, seed, modes):
    rng = random.Random(seed)
    records = []
    for index in range(trials):
        mode = modes[index % len(modes)]
        source = (random_source(rng, mode) if isinstance(mode, str)
                  else mode(rng))
        for p, q in PAIRS:
            frame = PfaffFrame(source, p, q)
            record = {"label": label, "source": index, "pair": [p, q],
                      "live": frame.pd.is_live(), "span": frame.span,
                      "kappa2": [], "M1": frame.span == 36, "M2star": [],
                      "M2star_zero_e2": [], "dc_all": []}
            for colour in RANGE3:
                record["kappa2"].append(frame.in_span(frame.kappa_square(colour)))
                reachable, forced = m2star(frame, colour)
                record["M2star"].append(reachable)
                record["M2star_zero_e2"].append(forced)
                record["dc_all"].append(
                    all(bool(intersect_with_dc(frame.xis[x], colour))
                        for x in frame.U))
            records.append(record)
    return records


def summarise_payoff(records, name):
    out = {"name": name, "pairs": len(records)}
    out["M1_wrong"] = sum(1 for r in records if r["M1"] and not all(r["kappa2"]))
    out["M2star_wrong"] = sum(1 for r in records for c in RANGE3
                              if r["M2star"][c] and not r["kappa2"][c])
    out["blocked"] = sum(1 for r in records for c in RANGE3 if r["kappa2"][c])
    out["free"] = sum(1 for r in records for c in RANGE3 if not r["kappa2"][c])
    out["free_with_span36"] = sum(1 for r in records for c in RANGE3
                                  if not r["kappa2"][c] and r["M1"])
    out["free_with_dc_all"] = sum(1 for r in records for c in RANGE3
                                  if not r["kappa2"][c] and r["dc_all"][c])
    out["free_with_dc_all_and_e2_nonzero"] = sum(
        1 for r in records for c in RANGE3
        if not r["kappa2"][c] and r["M2star"][c])
    out["blocked_outside_M1_M2star"] = sum(
        1 for r in records for c in RANGE3
        if r["kappa2"][c] and not r["M1"] and not r["M2star"][c])
    return out


def main():
    print("UNAUDITED PROBE (W4, Route F.1) -- payoff test")
    print("pinned HEAD 26ba69f7e643694c6a58464af6e9e1de9ec92f01")
    print()
    print("C2. degree-3 law: the mixed-determinant readings, 512 supports:",
          check_mixed_determinant_meanings())
    stats = check_degree3_law(trials=int(os.environ.get("W4_D3_TRIALS", 6)))
    print("    degree-3 ideal test:", json.dumps(stats))
    exact = check_degree3_law(trials=1, seed=97, exact=True)
    print("    same test over Q (one source, 15 pairs):", json.dumps(exact))
    print()
    print("C1. reach of the two named mechanisms")
    batches = [("generic", ("generic",), 8, 41),
               ("mixed", ("sparse", "lowrank", "binary"), 12, 42),
               ("diagonal", ("diagonal",), 8, 43),
               ("anchored", (anchored_coordinate_source,), 10, 44)]
    allrecords = []
    for name, modes, trials, seed in batches:
        records = payoff_survey(name, trials, seed, modes)
        allrecords.extend(records)
        print("  ", json.dumps(summarise_payoff(records, name)))
    with open("results_payoff.json", "w") as handle:
        json.dump({"degree3": stats, "records": allrecords}, handle, indent=1,
                  default=str)
    print("   wrote results_payoff.json (%d records)" % len(allrecords))


if __name__ == "__main__":
    main()
