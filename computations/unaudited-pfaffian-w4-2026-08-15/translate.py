#!/usr/bin/env python3
"""UNAUDITED PROBE (W4 / Route F.1) -- the witness data in Pfaffian coordinates.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01
Reuses the constructors of the P2 probe
(computations/unaudited-witness-splitting-p2-2026-08-15/wsplit_core.py).

Nothing here is a proved claim of the project.  Every printed line is an exact
rational identity, an exhaustive finite check, or a labelled statistic.

THE DICTIONARY (each line is verified below).

Fix a pair (p,q) of the six sites and U = {a,b,c,d} = B \\ {p,q}.
Put  E = V_p (+) V_q = C^6  and, for a site x in U and a colour alpha,

    xi_x^alpha  =  A_{p|x}(.,alpha)  (+)  A_{q|x}(.,alpha)   in E.     (D1)

The cap covector K in (V_p (x) V_q)^* is the same thing as the "hyperbolic"
symmetric bilinear form on E

    B_K( m(+)n , m'(+)n' ) = <K, m (x) n'> + <K, m' (x) n>,             (D2)

i.e. the forms vanishing on V_p and on V_q separately.  Then

    R_xy(alpha,beta) = B_K( xi_x^alpha , xi_y^beta )                    (D3)

so the effective-edge blocks R are the GRAM MATRICES of the marked vectors,
and with delta_c = e_c (+) e_c and A_pq = u (x) v when rank A_pq = 1,

    kappa_c = (1/2) B_K(delta_c, delta_c),   s = (1/2) B_K(u(+)v, u(+)v). (D4)

The 81 error components are the Gram hafnians / K_4 Pfaffians

    E_w = haf_4( B_K(xi_x^{w_x}, xi_y^{w_y}) ) = Pf( eps .* Gram ),      (D5)

so  E_w = 0  <=>  the 6-vector (R_xy) is DECOMPOSABLE in Lambda^2 C^4, i.e.
lies on the Klein quadric Gr(2,4); the whole cap condition E_pq(K)=0 says the
4-parameter family of 2-forms R(lambda) consists of rank-<=2 forms only.

Equivalently, in Sym^*(V_p) (x) Sym^*(V_q),

    E_w = pi_{2,2}( xi_a^{w_a} xi_b^{w_b} xi_c^{w_c} xi_d^{w_d} )
        = sum_{T subset U, |T|=2} psi( m_T ; n_{T^c} ),                 (D6)

the bidegree-(2,2) part of a SPLIT QUARTIC on E, where
psi(m,m';n,n') = <K,m(x)n><K,m'(x)n'> + <K,m(x)n'><K,m'(x)n> (a 2x2 permanent).

Consequences proved by (D6):
  FACT 1 (P2, checked there on 60 sources) becomes a one-line identity: each
  summand of (D6) is symmetric in its two V_p arguments and in its two V_q
  arguments, so it lies in W = Sym^2 V_p (x) Sym^2 V_q; the Lambda^2 (x)
  Lambda^2 component cancels in six pairs.
  FACT 2 (P2's pattern laws) becomes the single computation
  pi_Lambda(X (.) Y) = sum X_ij Y_kl (e_i ^ e_k) (x) (e_j ^ e_l):
      s*s        : pi_Lambda = the 2x2 minors of A_pq   => rank A_pq <= 1
      s*kappa_c  : pi_Lambda = (A_pq)_{ij}, i!=c!=j     => row c u column c
      kappa_c*kappa_c' : pi_Lambda = (e_c^e_c')(x)(e_c^e_c') != 0 => NEVER
      kappa_c^2  : pi_Lambda = 0 identically            => UNCONDITIONAL.

  SPAN: with Xi_x = span{xi_x^0, xi_x^1, xi_x^2} (a <=3-plane in C^6),
  multilinearity of (D6) gives
      span{E_w : 81 words} = image of the multiplication map
      mu_pq : Xi_a (x) Xi_b (x) Xi_c (x) Xi_d -> Sym^2 V_p (x) Sym^2 V_q.  (D7)
  So degree-2 blocking is exactly APOLARITY of the four 3-planes:
      kappa_c^2 blocks  <=>  delta_c^{(x)4} in image(mu_pq).             (D8)
  Two named sufficient conditions, both verified below:
      (M1) mu_pq surjective (dim image = 36)  => every kappa_c^2 blocks;
      (M2) delta_c in Xi_x for every x in U   => kappa_c^2 blocks.
  and (M2) has the coordinate form: if A_{p|x}(.,c) and A_{q|x}(.,c) are both
  multiples of e_c at every x in U, then the monochromatic-word component
  E_{cccc} is itself a multiple of kappa_c^2.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
import json
import os
import random
import sys

P2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                  "unaudited-witness-splitting-p2-2026-08-15")
sys.path.insert(0, os.path.abspath(P2))

from wsplit_core import (KAPPA_VARS, NVAR, PAIRS, PairData, SITES, Source,
                         decide_pair, in_row_space, in_sym_square, lin_mul,
                         lin_zero, matrix_rank, quad_add, quad_vector,
                         random_matrix, random_source, row_space, require)

RANGE3 = range(3)


# ------------------------------------------------------- linear algebra

def dot(vector, other):
    return sum(a * b for a, b in zip(vector, other))


def rank_of(rows):
    return len(row_space([list(row) for row in rows]))


def solve_in_span(columns, target):
    """Is `target` in the span of `columns` (lists of Fractions)?  Exact."""
    basis = row_space([list(column) for column in columns])
    return in_row_space(basis, list(target))


# ------------------------------------------------------- the xi picture

def xi_vectors(source: Source, p: int, q: int, x: int):
    """The three marked vectors xi_x^alpha in C^6 = V_p (+) V_q."""
    Apx, Aqx = source.oriented(p, x), source.oriented(q, x)
    return [[Apx[i][alpha] for i in RANGE3] + [Aqx[j][alpha] for j in RANGE3]
            for alpha in RANGE3]


def delta(colour):
    vector = [Fraction(0)] * 6
    vector[colour] = Fraction(1)
    vector[3 + colour] = Fraction(1)
    return vector


def bform(xi, eta):
    """B_K(xi, eta) as a linear form in the nine cap coordinates K_ij."""
    form = lin_zero()
    for i in RANGE3:
        for j in RANGE3:
            form[3 * i + j] += xi[i] * eta[3 + j] + eta[i] * xi[3 + j]
    return form


def psi(m, mm, n, nn):
    """psi(m,m';n,n') = <K,m(x)n><K,m'(x)n'> + <K,m(x)n'><K,m'(x)n>."""
    def lin(u, v):
        form = lin_zero()
        for i in RANGE3:
            for j in RANGE3:
                form[3 * i + j] += u[i] * v[j]
        return form
    quad = {}
    quad_add(quad, lin_mul(lin(m, n), lin(mm, nn)))
    quad_add(quad, lin_mul(lin(m, nn), lin(mm, n)))
    return quad


def error_from_xis(xis):
    """(D6): the bidegree-(2,2) part of the split quartic xi_a xi_b xi_c xi_d."""
    quad = {}
    sites = (0, 1, 2, 3)
    for T in combinations(sites, 2):
        rest = tuple(s for s in sites if s not in T)
        m = [xis[T[0]][:3], xis[T[1]][:3]]
        n = [xis[rest[0]][3:], xis[rest[1]][3:]]
        quad_add(quad, psi(m[0], m[1], n[0], n[1]))
    return quad


K4_SIGNS = {(0, 1): 1, (0, 2): -1, (0, 3): 1, (1, 2): 1, (1, 3): 1, (2, 3): 1}


def error_from_gram(xis):
    """(D5): haf_4 of the Gram matrix = Pf of the K_4 Kasteleyn matrix."""
    gram = {}
    for x, y in combinations(range(4), 2):
        gram[(x, y)] = bform(xis[x], xis[y])
    quad = {}
    for pairing in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        quad_add(quad, lin_mul(gram[pairing[0]], gram[pairing[1]]))
    pf = {}
    for pairing, sign in ((((0, 1), (2, 3)), 1), (((0, 2), (1, 3)), -1),
                          (((0, 3), (1, 2)), 1)):
        term = lin_mul([sign * K4_SIGNS[pairing[0]] * v
                        for v in gram[pairing[0]]],
                       [K4_SIGNS[pairing[1]] * v for v in gram[pairing[1]]])
        quad_add(pf, term)
    return quad, pf


# --------------------------------------------------- Lambda^2 projection

def lambda_projection(quad):
    """pi_Lambda: Sym^2(V_p (x) V_q) -> Lambda^2 V_p (x) Lambda^2 V_q (dim 9)."""
    out = {}
    for (u, v), value in quad.items():
        i, j = divmod(u, 3)
        k, l = divmod(v, 3)
        if i == k or j == l:
            continue
        sign = (1 if i < k else -1) * (1 if j < l else -1)
        key = (min(i, k), max(i, k), min(j, l), max(j, l))
        out[key] = out.get(key, Fraction(0)) + sign * value
    return {key: value for key, value in out.items() if value != 0}


# ------------------------------------------------------------ pair frame

class PfaffFrame:
    """The Pfaffian/Gram picture of one pair, alongside P2's PairData."""

    def __init__(self, source: Source, p: int, q: int):
        self.source, self.p, self.q = source, p, q
        self.pd = PairData(source, p, q)
        self.U = self.pd.U
        self.xis = {x: xi_vectors(source, p, q, x) for x in self.U}
        self.Xi_rank = {x: rank_of(self.xis[x]) for x in self.U}
        self.words = tuple(product(RANGE3, repeat=4))
        self.components = {}
        for word in self.words:
            xis = [self.xis[x][word[n]] for n, x in enumerate(self.U)]
            self.components[word] = error_from_xis(xis)
        self.basis = row_space([quad_vector(q_) for q_ in self.components.values()
                                if q_])
        self.span = len(self.basis)

    # -- the L-monomials as quadrics -----------------------------------
    def kappa_square(self, colour):
        form = lin_zero()
        form[KAPPA_VARS[colour]] = Fraction(1)
        return lin_mul(form, form)

    def s_square(self):
        return lin_mul(self.pd.s, self.pd.s)

    def s_kappa(self, colour):
        form = lin_zero()
        form[KAPPA_VARS[colour]] = Fraction(1)
        return lin_mul(self.pd.s, form)

    def kappa_cross(self, c, cc):
        f1, f2 = lin_zero(), lin_zero()
        f1[KAPPA_VARS[c]] = Fraction(1)
        f2[KAPPA_VARS[cc]] = Fraction(1)
        return lin_mul(f1, f2)

    def in_span(self, quad):
        return in_row_space(self.basis, quad_vector(quad))

    # -- the geometric predicates --------------------------------------
    def delta_in_Xi(self, colour):
        """For each x in U: is delta_c in Xi_x?"""
        return {x: solve_in_span(self.xis[x], delta(colour)) for x in self.U}

    def colour_coordinate(self, colour):
        """A_{p|x}(.,c) and A_{q|x}(.,c) both multiples of e_c, every x in U."""
        for x in self.U:
            xi = self.xis[x][colour]
            if any(xi[i] != 0 for i in RANGE3 if i != colour):
                return False
            if any(xi[3 + j] != 0 for j in RANGE3 if j != colour):
                return False
        return True

    def mono_component_multiple_of_kappa2(self, colour):
        """Is E_{cccc} a nonzero multiple of kappa_c^2?"""
        quad = self.components[(colour,) * 4]
        if not quad:
            return False, Fraction(0)
        key = (KAPPA_VARS[colour], KAPPA_VARS[colour])
        if set(quad) != {key}:
            return False, Fraction(0)
        return True, quad[key]


# ------------------------------------------------------------- checks

def check_dictionary(trials=40, seed=11):
    """(D3),(D5),(D6): the three formulae reproduce P2's 81 quadrics exactly."""
    rng = random.Random(seed)
    modes = ("generic", "sparse", "lowrank", "diagonal", "binary")
    counts = {"R": 0, "gram": 0, "pf": 0, "split": 0, "lambda": 0}
    for index in range(trials):
        source = random_source(rng, modes[index % len(modes)])
        for p, q in PAIRS:
            frame = PfaffFrame(source, p, q)
            pd = frame.pd
            # (D3) R blocks are Gram matrices of the xi's
            for x, y in combinations(frame.U, 2):
                for alpha in RANGE3:
                    for beta in RANGE3:
                        got = bform(frame.xis[x][alpha], frame.xis[y][beta])
                        require(got == pd.R[(x, y)][alpha][beta],
                                "(D3) Gram identity failed")
                        counts["R"] += 1
            # (D5)/(D6): the components agree with P2's quadrics
            p2quads = {}
            a, b, c, d = frame.U
            position = {a: 0, b: 1, c: 2, d: 3}
            for word in frame.words:
                quad = {}
                for (e1, e2) in pd.matchings:
                    l1 = pd.R[e1][word[position[e1[0]]]][word[position[e1[1]]]]
                    l2 = pd.R[e2][word[position[e2[0]]]][word[position[e2[1]]]]
                    quad_add(quad, lin_mul(l1, l2))
                p2quads[word] = {k: v for k, v in quad.items() if v}
            for word in frame.words:
                xis = [frame.xis[x][word[n]] for n, x in enumerate(frame.U)]
                gram, pf = error_from_gram(xis)
                require(gram == p2quads[word], "(D5) haf-Gram identity failed")
                require(pf == p2quads[word], "(D5) K_4 Pfaffian identity failed")
                require(frame.components[word] == p2quads[word],
                        "(D6) split-quartic identity failed")
                counts["gram"] += 1
                counts["pf"] += 1
                counts["split"] += 1
                # FACT 1 by the Lambda^2 cancellation
                require(not lambda_projection(p2quads[word]),
                        "FACT 1 (Lambda^2 part) failed")
                require(in_sym_square(p2quads[word]) ==
                        (not lambda_projection(p2quads[word])),
                        "pi_Lambda disagrees with P2's in_sym_square")
                counts["lambda"] += 1
    return counts


def check_fact2_laws():
    """FACT 2 as exact statements about pi_Lambda.  Exhaustive on supports."""
    checked = 0
    for support in product((0, 1), repeat=9):
        matrix = [[Fraction(support[3 * i + j]) for j in RANGE3]
                  for i in RANGE3]
        s = [matrix[i][j] for i in RANGE3 for j in RANGE3]
        rank = matrix_rank(matrix)
        # s*s  <->  the 2x2 minors of A_pq
        minors = lambda_projection(lin_mul(s, s))
        expected = {}
        for i, k in combinations(RANGE3, 2):
            for j, l in combinations(RANGE3, 2):
                value = matrix[i][j] * matrix[k][l] - matrix[i][l] * matrix[k][j]
                if value:
                    expected[(i, k, j, l)] = 2 * value
        require(minors == expected, "s*s pi_Lambda != 2 * 2x2 minors")
        require((not minors) == (rank <= 1), "s*s law failed")
        for colour in RANGE3:
            form = lin_zero()
            form[KAPPA_VARS[colour]] = Fraction(1)
            cross = lambda_projection(lin_mul(s, form))
            support_ok = all(matrix[i][j] == 0 for i in RANGE3 for j in RANGE3
                             if i != colour and j != colour)
            require((not cross) == support_ok, "s*kappa law failed")
            for other in RANGE3:
                f2 = lin_zero()
                f2[KAPPA_VARS[other]] = Fraction(1)
                kk = lambda_projection(lin_mul(form, f2))
                require((not kk) == (colour == other), "kappa*kappa law failed")
        checked += 1
    return checked


# ------------------------------------------------------- the payoff test

def survey(trials, modes, seed, witness=False, timeout=60, label=""):
    """Per-pair: span dimension, degree-2 patterns, and the geometric tests."""
    rng = random.Random(seed)
    rows = []
    for index in range(trials):
        mode = modes[index % len(modes)]
        source = (random_source(rng, mode) if isinstance(mode, str)
                  else mode(rng))
        for p, q in PAIRS:
            frame = PfaffFrame(source, p, q)
            live = frame.pd.is_live()
            row = {
                "label": label, "mode": mode if isinstance(mode, str) else "custom",
                "source": index, "pair": [p, q], "live": live,
                "span": frame.span,
                "Xi_ranks": [frame.Xi_rank[x] for x in frame.U],
                "rank_Apq": matrix_rank(source.blocks[(min(p, q), max(p, q))]),
                "kappa2": [frame.in_span(frame.kappa_square(c)) for c in RANGE3],
                "s2": frame.in_span(frame.s_square()) if live else None,
                "skappa": [frame.in_span(frame.s_kappa(c)) for c in RANGE3]
                          if live else None,
                "kcross": [frame.in_span(frame.kappa_cross(c, cc))
                           for c, cc in combinations(RANGE3, 2)],
                "delta_all": [all(frame.delta_in_Xi(c).values()) for c in RANGE3],
                "delta_some": [any(frame.delta_in_Xi(c).values())
                               for c in RANGE3],
                "coord": [frame.colour_coordinate(c) for c in RANGE3],
                "mono_mult": [frame.mono_component_multiple_of_kappa2(c)[0]
                              for c in RANGE3],
            }
            if witness and live:
                entry = decide_pair(frame.pd, max_degree=3, timeout=timeout)
                row["witness"] = entry["witness"]
                row["arithmetic"] = entry.get("arithmetic")
            rows.append(row)
    return rows


def anchored_coordinate_source(rng):
    """Coordinate-anchored family: most blocks diagonal, a few generic."""
    blocks = {}
    dirty = set(rng.sample(list(PAIRS), rng.choice([1, 2, 3])))
    for pair in PAIRS:
        if pair in dirty:
            blocks[pair] = random_matrix(rng)
        else:
            matrix = [[Fraction(0)] * 3 for _ in range(3)]
            for c in RANGE3:
                matrix[c][c] = Fraction(rng.choice([1, 1, 1, 2, -1, 3]))
            blocks[pair] = matrix
    return Source(blocks)


def summarise(rows, name):
    live = [r for r in rows if r["live"]]
    out = {"name": name, "pairs": len(rows), "live": len(live)}
    out["span_hist"] = {}
    for r in rows:
        out["span_hist"][r["span"]] = out["span_hist"].get(r["span"], 0) + 1
    # M1: span = 36  =>  every kappa_c^2 blocks
    out["M1_violations"] = sum(1 for r in rows
                               if r["span"] == 36 and not all(r["kappa2"]))
    # M2: delta_c in every Xi_x  =>  kappa_c^2 blocks
    out["M2_violations"] = sum(1 for r in rows for c in RANGE3
                               if r["delta_all"][c] and not r["kappa2"][c])
    # coordinate colour => monochromatic component is a multiple of kappa_c^2
    out["coord_instances"] = sum(1 for r in rows for c in RANGE3 if r["coord"][c])
    out["coord_mono_violations"] = sum(
        1 for r in rows for c in RANGE3
        if r["coord"][c] and not r["mono_mult"][c])
    out["coord_block_violations"] = sum(
        1 for r in rows for c in RANGE3
        if r["coord"][c] and not r["kappa2"][c])
    # the converse questions
    out["kappa2_blocks"] = sum(1 for r in rows for c in RANGE3 if r["kappa2"][c])
    out["kappa2_blocks_no_M1_no_M2"] = sum(
        1 for r in rows for c in RANGE3
        if r["kappa2"][c] and r["span"] != 36 and not r["delta_all"][c])
    out["kappa2_free"] = sum(1 for r in rows for c in RANGE3
                             if not r["kappa2"][c])
    out["kcross_ever_blocks"] = sum(1 for r in rows if any(r["kcross"]))
    out["s2_blocks_rank_gt1"] = sum(
        1 for r in live if r["s2"] and r["rank_Apq"] > 1)
    if any("witness" in r for r in rows):
        wit = [r for r in live if r.get("witness")]
        out["witness_pairs"] = len(wit)
        out["witness_with_span36"] = sum(1 for r in wit if r["span"] == 36)
        out["witness_span_hist"] = {}
        for r in wit:
            out["witness_span_hist"][r["span"]] = \
                out["witness_span_hist"].get(r["span"], 0) + 1
        out["blocked_span_hist"] = {}
        for r in live:
            if r.get("witness") is False:
                out["blocked_span_hist"][r["span"]] = \
                    out["blocked_span_hist"].get(r["span"], 0) + 1
        out["undecided"] = sum(1 for r in live if r.get("witness") is None)
    return out


def main():
    print("UNAUDITED PROBE (W4, Route F.1) -- witness data in Pfaffian coordinates")
    print("pinned HEAD 26ba69f7e643694c6a58464af6e9e1de9ec92f01")
    print()
    print("A. the dictionary (D3),(D5),(D6) against P2's constructors")
    counts = check_dictionary(trials=int(os.environ.get("W4_DICT_TRIALS", 20)))
    for key, value in sorted(counts.items()):
        print("   identities verified [%s]: %d" % (key, value))
    print()
    print("B. FACT 2 as pi_Lambda statements, exhaustive over the 512 supports")
    print("   supports checked:", check_fact2_laws())
    print()
    print("C. payoff survey")
    results = {}
    batches = [
        ("generic", ("generic",), 12, 21),
        ("mixed", ("sparse", "lowrank", "binary"), 18, 22),
        ("diagonal", ("diagonal",), 10, 23),
        ("anchored", (anchored_coordinate_source,), 16, 24),
    ]
    allrows = []
    for name, modes, trials, seed in batches:
        rows = survey(trials, modes, seed, label=name)
        allrows.extend(rows)
        summary = summarise(rows, name)
        results[name] = summary
        print("  ", json.dumps(summary))
    with open("results_translate.json", "w") as handle:
        json.dump({"summaries": results, "rows": allrows}, handle, indent=1,
                  default=str)
    print("   wrote results_translate.json (%d pair records)" % len(allrows))


if __name__ == "__main__":
    main()
