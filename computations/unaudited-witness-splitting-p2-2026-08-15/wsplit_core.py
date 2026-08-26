#!/usr/bin/env python3
"""UNAUDITED PROBE -- six-site calibration of the witness/splitting dichotomy.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a
Plan: notes/2026-08-15-witness-splitting-dichotomy-plan.md (step P2)
Target note: notes/clean-pair-cap-exact-descent-target.md

Nothing here is a proved claim.  This is an exact (rational, Groebner-backed)
experiment on six-site aggregate sources.

Setting.  B = six named sites, V_u = C^3.  Endpoint-ordered blocks
A_{uv} in V_u (x) V_v.  For a pair (p,q), U = B \ {p,q} has |U| = 4, so the
descent half-order is h = 2 and equation (4) of the descent note collapses to
the single term

    E_{p,q}(K) = [ r(K)^2 / 2 ]_U
               = sum over the 3 perfect matchings {ab|cd} of U of
                 R_ab (x) R_cd,

a TENSOR in V_a (x) V_b (x) V_c (x) V_d whose 81 components are quadratic
forms in the nine cap coordinates K_ij.  With

    s(K)      = <K, A_pq>                              (linear in K)
    R_ab(K)   = K |_ (A_{p|a} A_{q|b} + A_{p|b} A_{q|a})  (linear in K)
    kappa_c   = K_cc                                   (coordinate functional)

the witness condition (W) at the pair is

    exists K:  s(K) kappa_0 kappa_1 kappa_2 != 0  and  E_{p,q}(K) = 0.

Decision procedure (exact, over C = Qbar): let I = <81 quadrics> in
Q[K_00..K_22].  A witness exists iff V(I) is NOT contained in the union of
the four hyperplanes {s=0}, {kappa_c=0}, which by the Nullstellensatz is
iff 1 is not in <I, t*s*kappa_0*kappa_1*kappa_2 - 1>.  Decided by Singular.

Splitting test (the plan's side of the dichotomy): the degree-2 graded piece
of I is exactly the Q-span of the 81 quadrics.  The pair is "degree-2
split-blocked" iff some nonzero element of that span equals a product
l_1 l_2 with l_i in L = {s, kappa_0, kappa_1, kappa_2}: at most 10 patterns.
Generalisation used here: the pair is "L-monomial blocked in degree d" iff
some degree-d monomial in L lies in I_d.  By the Nullstellensatz, no witness
iff L-monomial blocked in SOME degree; the plan's dichotomy is the claim that
degree d = h = 2 always suffices.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, combinations_with_replacement
import os
import random
import subprocess
import tempfile

SITES = tuple(range(6))
PAIRS = tuple(combinations(SITES, 2))
NVAR = 9  # cap coordinates K_ij, index 3*i + j
KAPPA_VARS = (0, 4, 8)
QUAD_KEYS = tuple(combinations_with_replacement(range(NVAR), 2))  # 45
QUAD_INDEX = {key: n for n, key in enumerate(QUAD_KEYS)}


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


# ---------------------------------------------------------------- sources


class Source:
    """Endpoint-ordered aggregate blocks on six sites, exact rationals."""

    def __init__(self, blocks):
        # blocks[(u, v)] with u < v is a 3x3 table, row index = colour at u.
        self.blocks = {}
        for (u, v), matrix in blocks.items():
            require(u < v, "blocks are keyed by u<v")
            self.blocks[(u, v)] = [[Fraction(entry) for entry in row]
                                   for row in matrix]
        for pair in PAIRS:
            self.blocks.setdefault(pair, [[Fraction(0)] * 3 for _ in range(3)])

    def oriented(self, u, v):
        """Block with row index = colour at u, column index = colour at v."""
        if u < v:
            return self.blocks[(u, v)]
        matrix = self.blocks[(v, u)]
        return [[matrix[j][i] for j in range(3)] for i in range(3)]

    def rank(self, u, v):
        return matrix_rank(self.blocks[(min(u, v), max(u, v))])

    def coefficient(self, word):
        """Coefficient of e_{word[0]} (x) ... (x) e_{word[5]} in H_6(A)."""
        total = Fraction(0)
        for matching in perfect_matchings(SITES):
            term = Fraction(1)
            for u, v in matching:
                term *= self.oriented(u, v)[word[u]][word[v]]
                if term == 0:
                    break
            total += term
        return total

    def pure_defects(self):
        return [self.coefficient((c,) * 6) - 1 for c in range(3)]


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, vertices[index]),) + tail)
    return tuple(out)


def matrix_rank(matrix):
    rows = [[Fraction(entry) for entry in row] for row in matrix]
    rank = 0
    columns = len(rows[0])
    for column in range(columns):
        pivot = None
        for index in range(rank, len(rows)):
            if rows[index][column] != 0:
                pivot = index
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        head = rows[rank]
        for index in range(len(rows)):
            if index != rank and rows[index][column] != 0:
                factor = rows[index][column] / head[column]
                rows[index] = [a - factor * b
                               for a, b in zip(rows[index], head)]
        rank += 1
    return rank


# ------------------------------------------------------- linear/quadratic


def lin_zero():
    return [Fraction(0)] * NVAR


def lin_add(a, b):
    return [x + y for x, y in zip(a, b)]


def lin_is_zero(a):
    return all(x == 0 for x in a)


def lin_mul(a, b):
    """Product of two linear forms as a dict on QUAD_KEYS."""
    out = {}
    for i in range(NVAR):
        if a[i] == 0:
            continue
        for j in range(NVAR):
            if b[j] == 0:
                continue
            key = (i, j) if i <= j else (j, i)
            out[key] = out.get(key, Fraction(0)) + a[i] * b[j]
    return {key: value for key, value in out.items() if value != 0}


DIM_W = 36  # dim Sym^2(V_p^*) (x) Sym^2(V_q^*) inside the 45 quadrics


def in_sym_square(quad):
    """Is the quadratic form in W = Sym^2(V_p^*) (x) Sym^2(V_q^*)?

    Quadratic forms on the 3x3 cap matrix K split as
        Sym^2(M_3^*) = (Sym^2 row (x) Sym^2 col) + (Lambda^2 row (x) Lambda^2 col)
    of dimensions 36 + 9.  The second summand is spanned by the nine 2x2
    minors of K.  Membership in the 36-dimensional summand W is exactly
    invariance of the coefficient array under exchanging the two column
    (q-slot) indices, i.e. coeff[(i,j),(k,l)] = coeff[(i,l),(k,j)].
    """
    for (u, v), value in quad.items():
        i, j = divmod(u, 3)
        k, l = divmod(v, 3)
        u2, v2 = 3 * i + l, 3 * k + j
        key = (u2, v2) if u2 <= v2 else (v2, u2)
        if key == (u, v):
            continue
        if quad.get(key, Fraction(0)) != value:
            return False
    return True


def quad_add(target, other):
    for key, value in other.items():
        new = target.get(key, Fraction(0)) + value
        if new == 0:
            target.pop(key, None)
        else:
            target[key] = new


def quad_vector(quad):
    vector = [Fraction(0)] * len(QUAD_KEYS)
    for key, value in quad.items():
        vector[QUAD_INDEX[key]] = value
    return vector


# ------------------------------------------------------------ pair data


class PairData:
    """All witness data of one pair (p,q) of one source."""

    def __init__(self, source: Source, p: int, q: int):
        self.source = source
        self.p, self.q = p, q
        self.U = tuple(site for site in SITES if site not in (p, q))
        block = source.oriented(p, q)
        self.s = [block[i][j] for i in range(3) for j in range(3)]
        self.R = {}
        for a, b in combinations(self.U, 2):
            Apa, Aqb = source.oriented(p, a), source.oriented(q, b)
            Apb, Aqa = source.oriented(p, b), source.oriented(q, a)
            table = [[lin_zero() for _ in range(3)] for _ in range(3)]
            for alpha in range(3):
                for beta in range(3):
                    form = lin_zero()
                    for i in range(3):
                        for j in range(3):
                            value = (Apa[i][alpha] * Aqb[j][beta]
                                     + Apb[i][beta] * Aqa[j][alpha])
                            if value:
                                form[3 * i + j] += value
                    table[alpha][beta] = form
            self.R[(a, b)] = table
        a, b, c, d = self.U
        self.matchings = (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))
        self.quadrics = self._error_components()

    def _error_components(self):
        a, b, c, d = self.U
        position = {a: 0, b: 1, c: 2, d: 3}
        out = []
        for w0 in range(3):
            for w1 in range(3):
                for w2 in range(3):
                    for w3 in range(3):
                        word = (w0, w1, w2, w3)
                        quad = {}
                        for (e1, e2) in self.matchings:
                            lin1 = self.R[e1][word[position[e1[0]]]][
                                word[position[e1[1]]]]
                            lin2 = self.R[e2][word[position[e2[0]]]][
                                word[position[e2[1]]]]
                            if lin_is_zero(lin1) or lin_is_zero(lin2):
                                continue
                            quad_add(quad, lin_mul(lin1, lin2))
                        if quad:
                            out.append(quad)
        return out

    # -- elementary classification ------------------------------------
    def is_live(self):
        return not lin_is_zero(self.s)

    def error_identically_zero(self):
        return not self.quadrics

    def linear_forms(self):
        """L = (s, kappa_0, kappa_1, kappa_2) as linear forms."""
        forms = [list(self.s)]
        for var in KAPPA_VARS:
            form = lin_zero()
            form[var] = Fraction(1)
            forms.append(form)
        return forms

    # -- degree-2 splitting -------------------------------------------
    def split_patterns(self):
        """Patterns l_i l_j (i<=j) whose quadric lies in span(E-components)."""
        forms = self.linear_forms()
        names = ("s", "kappa_0", "kappa_1", "kappa_2")
        basis = row_space([quad_vector(quad) for quad in self.quadrics])
        found = []
        for i, j in combinations_with_replacement(range(4), 2):
            product = lin_mul(forms[i], forms[j])
            if not product:
                continue  # s identically zero: degenerate pattern
            if in_row_space(basis, quad_vector(product)):
                found.append((names[i], names[j]))
        return found, len(basis)


def row_space(vectors):
    """Reduced row echelon basis of the span (exact)."""
    basis = []
    pivots = []
    for vector in vectors:
        row = list(vector)
        for pivot, brow in zip(pivots, basis):
            if row[pivot] != 0:
                factor = row[pivot] / brow[pivot]
                row = [a - factor * b for a, b in zip(row, brow)]
        pivot = next((n for n, value in enumerate(row) if value != 0), None)
        if pivot is None:
            continue
        basis.append(row)
        pivots.append(pivot)
    return list(zip(pivots, basis))


def in_row_space(basis, vector):
    row = list(vector)
    for pivot, brow in basis:
        if row[pivot] != 0:
            factor = row[pivot] / brow[pivot]
            row = [a - factor * b for a, b in zip(row, brow)]
    return all(value == 0 for value in row)


# ------------------------------------------------------------- Singular

VARS = [f"k{n}" for n in range(NVAR)]


def poly_string_lin(form):
    parts = []
    for index, value in enumerate(form):
        if value:
            parts.append(f"({value.numerator}/{value.denominator})*{VARS[index]}")
    return "+".join(parts) if parts else "0"


def poly_string_quad(quad):
    parts = []
    for (i, j), value in sorted(quad.items()):
        parts.append(
            f"({value.numerator}/{value.denominator})*{VARS[i]}*{VARS[j]}")
    return "+".join(parts) if parts else "0"


def monomial_string(indices, forms_strings):
    return "*".join(f"({forms_strings[index]})" for index in indices)


def singular_queries(pairdata: PairData, max_degree: int = 4,
                     characteristic: int = 0):
    """Cone dimension and L-monomial ideal membership (no saturation).

    Every "MEM ... 1" line is an EXACT blocking certificate: an L-monomial
    lying in the error ideal forces every solution of E_pq = 0 onto one of
    the four hyperplanes, so no witness exists.
    """
    field = str(characteristic)
    gens = ",".join(poly_string_quad(quad) for quad in pairdata.quadrics)
    forms = [poly_string_lin(pairdata.s)] + [f"{VARS[v]}" for v in KAPPA_VARS]
    lines = [f'ring R={field},({",".join(VARS)}),dp;',
             f"ideal I=" + (gens if gens else "0") + ";",
             "ideal G=std(I);",
             # Affine cone dimension: 0 means V(I) is projectively empty,
             # -1 means the unit ideal (cannot happen for homogeneous I).
             f'"DIM {pairdata.p} {pairdata.q} "+string(dim(G));']
    for degree in range(2, max_degree + 1):
        for combo in combinations_with_replacement(range(4), degree):
            mono = monomial_string(combo, forms)
            name = "".join("s" if c == 0 else str(c - 1) for c in combo)
            lines.append(
                f'"MEM {pairdata.p} {pairdata.q} {degree} {name} "'
                f"+string(reduce({mono},G)==0);")
    return "\n".join(lines)


def singular_witness_query(pairdata: PairData, characteristic: int = 0):
    """Rabinowitsch decision: 1 in <I, t*s*kappa_0*kappa_1*kappa_2 - 1>?"""
    field = str(characteristic)
    gens = ",".join(poly_string_quad(quad) for quad in pairdata.quadrics)
    forms = [poly_string_lin(pairdata.s)] + [f"{VARS[v]}" for v in KAPPA_VARS]
    fprod = "*".join(f"({form})" for form in forms)
    return "\n".join([
        f'ring RT={field},({",".join(VARS)},t),dp;',
        f"ideal I=" + (gens if gens else "0") + ";",
        f"ideal J=I,t*{fprod}-1;",
        f'"WIT {pairdata.p} {pairdata.q} "+string(dim(std(J)));',
    ])


def run_singular(script: str, timeout: int = 900):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as handle:
        handle.write(script + "\nquit;\n")
        path = handle.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    if proc.returncode != 0:
        raise RuntimeError(f"Singular failed: {proc.stderr[:2000]}")
    return proc.stdout


def parse_singular(output: str):
    """-> {(p,q): {'dim':int,'witness':bool,'mem':{(deg,name):bool}}}"""
    table = {}
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        fields = line.split()
        if fields[0] == "DIM":
            key = (int(fields[1]), int(fields[2]))
            table.setdefault(key, {"mem": {}})["dim"] = int(fields[3])
        elif fields[0] == "WIT":
            key = (int(fields[1]), int(fields[2]))
            # dim(std(J)) == -1  <=>  1 in J  <=>  NO witness.
            table.setdefault(key, {"mem": {}})["witness"] = int(fields[3]) != -1
        elif fields[0] == "MEM":
            key = (int(fields[1]), int(fields[2]))
            entry = table.setdefault(key, {"mem": {}})
            entry["mem"][(int(fields[3]), fields[4])] = fields[5] == "1"
    return table


# ------------------------------------------------------- classification


FALLBACK_PRIMES = (1000003, 32003)


def decide_pair(pd: PairData, max_degree: int = 4, timeout: int = 120):
    """Decide witness existence for one pair.

    Stage 1 (always exact over Q): Groebner basis of the error ideal, cone
    dimension, and L-monomial membership up to `max_degree`.  A positive
    membership is a complete blocking certificate -- no witness.

    Stage 2 (only if no certificate was found): the Rabinowitsch saturation
    decision over Q, with a fallback to two large prime fields if the
    rational Groebner basis does not finish in time.  The arithmetic actually
    used is recorded in the "arithmetic" field.
    """
    key = (pd.p, pd.q)
    entry = None
    try:
        entry = parse_singular(
            run_singular(singular_queries(pd, max_degree),
                         timeout=timeout))[key]
        entry["arithmetic"] = "Q"
    except (subprocess.TimeoutExpired, KeyError):
        entry = None
    if entry is not None and any(entry["mem"].values()):
        entry["witness"] = False
        entry["arithmetic"] = "Q-certificate"
        return entry
    if entry is None:
        for prime in FALLBACK_PRIMES:
            try:
                entry = parse_singular(
                    run_singular(singular_queries(pd, max_degree, prime),
                                 timeout=timeout))[key]
                entry["arithmetic"] = "modular"
                break
            except (subprocess.TimeoutExpired, KeyError):
                continue
        if entry is None:
            return {"dim": None, "witness": None, "mem": {},
                    "arithmetic": "unknown"}
    try:
        answer = parse_singular(
            run_singular(singular_witness_query(pd), timeout=timeout))[key]
        entry["witness"] = answer["witness"]
        entry["arithmetic"] = (entry["arithmetic"]
                               if entry["arithmetic"] == "modular" else "Q")
        return entry
    except (subprocess.TimeoutExpired, KeyError):
        pass
    answers = []
    for prime in FALLBACK_PRIMES:
        try:
            answers.append(parse_singular(
                run_singular(singular_witness_query(pd, prime),
                             timeout=timeout))[key]["witness"])
        except (subprocess.TimeoutExpired, KeyError):
            continue
    if not answers:
        entry["witness"] = None
        entry["arithmetic"] = "unknown"
        return entry
    entry["witness"] = answers[0]
    entry["arithmetic"] = "modular"
    entry["modular_agreement"] = all(value == answers[0] for value in answers)
    return entry


def classify_source(source: Source, max_degree: int = 4, pairs=None,
                    timeout: int = 120):
    """Full exact map of every pair of one source."""
    pairs = tuple(pairs) if pairs is not None else PAIRS
    data = {pair: PairData(source, *pair) for pair in pairs}
    report = {}
    for pair in pairs:
        pd = data[pair]
        patterns, span = pd.split_patterns()
        entry = decide_pair(pd, max_degree, timeout)
        record = {
            "live": pd.is_live(),
            "error_zero": pd.error_identically_zero(),
            "span": span,
            "patterns": patterns,
            "cone_dim": entry["dim"],
            "witness": entry["witness"],
            "mem": entry["mem"],
            "arithmetic": entry.get("arithmetic", "Q"),
        }
        record["variety_empty"] = (entry["dim"] is not None
                                   and entry["dim"] <= 0)
        record["span_is_W"] = span == DIM_W
        record["all_components_in_W"] = all(in_sym_square(quad)
                                            for quad in pd.quadrics)
        record["min_block_degree"] = min(
            (degree for (degree, _name), value in entry["mem"].items() if value),
            default=None)
        record["status"] = pair_status(record)
        report[pair] = record
    return report


def pair_status(record):
    if not record["live"]:
        return "dead"
    if record["witness"] is None:
        return "undecided"
    if record["witness"]:
        return "witness"
    if record["patterns"]:
        return "split-blocked"
    if record["variety_empty"]:
        return "blocked-empty"
    return "blocked-other"


# ------------------------------------------------------ source builders


def random_matrix(rng, lo=-4, hi=4, density=1.0, rank=None):
    if rank is not None:
        return random_rank_matrix(rng, rank, lo, hi)
    return [[Fraction(rng.randint(lo, hi)) if rng.random() < density
             else Fraction(0) for _ in range(3)] for _ in range(3)]


def random_rank_matrix(rng, rank, lo=-4, hi=4):
    while True:
        left = [[Fraction(rng.randint(lo, hi)) for _ in range(rank)]
                for _ in range(3)]
        right = [[Fraction(rng.randint(lo, hi)) for _ in range(3)]
                 for _ in range(rank)]
        matrix = [[sum(left[i][t] * right[t][j] for t in range(rank))
                   for j in range(3)] for i in range(3)]
        if rank == 0 or matrix_rank(matrix) == rank:
            return matrix


def random_source(rng, mode="generic"):
    blocks = {}
    for pair in PAIRS:
        if mode == "generic":
            blocks[pair] = random_matrix(rng)
        elif mode == "sparse":
            blocks[pair] = random_matrix(rng, density=0.35)
        elif mode == "lowrank":
            blocks[pair] = random_matrix(rng, rank=rng.choice([0, 1, 1, 2]))
        elif mode == "diagonal":
            matrix = [[Fraction(0)] * 3 for _ in range(3)]
            for c in range(3):
                matrix[c][c] = Fraction(rng.randint(-4, 4))
            blocks[pair] = matrix
        elif mode == "binary":
            blocks[pair] = [[Fraction(rng.randint(0, 1)) for _ in range(3)]
                            for _ in range(3)]
        else:
            raise ValueError(mode)
    return Source(blocks)
