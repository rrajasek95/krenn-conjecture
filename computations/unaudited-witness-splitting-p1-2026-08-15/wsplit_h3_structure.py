#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1' at h = 3: equivariant home, blocking forcings,
and the machine-usable ideal-membership test.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a
(dependencies re-verified unchanged at a9dbf954)

Answers the three revised P1 asks, in the ideal-theoretic framing fixed by
the P2 calibration (blocking at a live pair = some monomial in
L = {s, kappa_0, kappa_1, kappa_2} of ANY degree lies in the error ideal).

(b) THE EQUIVARIANT HOME AT h = 3.

    Sym^3(V_p* (x) V_q*)  =  S_3 (x) S_3   (+)  S_21 (x) S_21  (+)  L^3 (x) L^3
    dim                   =  100           +    64             +    1   = 165

    The last summand is the determinant line.  Multiplicity-free, so the
    projection to it is canonical; the pairing that computes it is

        <det(d), G> = sum_sigma sgn(sigma) * coeff_G( K_{0,s0} K_{1,s1} K_{2,s2} ).

    FACT 1 (h=3).  EVERY component E_w is annihilated by det(d): the 729
    cubics lie in the codimension-ONE invariant subspace
    S_3(x)S_3 (+) S_21(x)S_21 (dim 164).  (Sym^3 (x) Sym^3 alone, dim 100,
    does NOT contain them -- the generic span has dim 136 > 100.)

    Proof.  det(d) applied to a product of three linear forms is the mixed
    (polarized) determinant D of their coefficient matrices, and
    D(u1 v1^T, u2 v2^T, u3 v3^T) = det[u1 u2 u3] * det[v1 v2 v3].
    Every full-support term of 6E = 3 s r^2 x + r^3 is indexed by a way of
    splitting the six boundary sites into pairs and ORIENTING each pair
    (which site takes the p-slot, which the q-slot); the p-vectors are the
    columns p_a = A_pa[.][w_a], the q-vectors q_a = A_qa[.][w_a].
      * r^3 terms: group the 15*8 = 120 configurations by the SET X of the
        three p-sites.  Within a group the p-determinant det[p_X] is fixed
        and the six bijections X -> Y contribute
        det[p_X] * det[q_Y] * sum_sigma sgn(sigma) = 0.
      * 3 s r^2 x terms: one factor is A_pq, the other two are rank-one
        oriented pairs; D(A, u v^T, u' v'^T) is antisymmetric under
        swapping (v, v'), so the two bijections of a 2-element p-site set
        cancel.
    Hence every term group cancels.  []

    CONSEQUENCE (what can ever block at degree 3).  An L-monomial m of
    degree 3 can lie in the degree-3 error span only if D(m) = 0:

        kappa_a kappa_b kappa_c, {a,b,c} = {0,1,2} :  D = 1   NEVER BLOCKS
        s^3                                        :  D = 6 det A_pq
        s^2 kappa_c                                :  D = 2 cof_cc(A_pq)
        s kappa_c kappa_c' (c != c')               :  D = A_pq[a][a],
                                                      a the third colour
        kappa_c^3, kappa_c^2 kappa_c', s kappa_c^2 :  D = 0 (no obstruction)

    Uniformly: for distinct colours c_1..c_j,
        D( s^(3-j) kappa_c1 .. kappa_cj ) = (3-j)! * (minor of A_pq obtained
        by DELETING rows and columns c_1..c_j),
    and D = 0 whenever a colour repeats.  Verified exactly.  So an
    s-carrying degree-3 monomial blocks only if the complementary minor of
    the pair block vanishes; j = 3 gives the empty minor 1, whence
    kappa_0 kappa_1 kappa_2 can never block at degree 3.

    FORCING F1 (the kappa_c^3 side).  The coefficient of K_cc^3 in E_w is
    exactly the MONOCHROME-c SLICE error: the h=3 error built from the
    colour-c row of every p-block and q-block,
        E^(c) = [3 s_c r_c^2 x + r_c^3]_full,  s_c = A_pq[c][c],
        r_c from A_pu[c][.], A_qu[c][.].
    Hence kappa_c^3 in I_3  =>  E^(c) is not identically zero.  (Every
    element of I_3 has zero K_cc^3-coefficient when E^(c) == 0, while
    kappa_c^3 has coefficient 1.)  Contrapositive: a pair whose
    monochrome-c slice error vanishes cannot be blocked by kappa_c^3 at
    degree 3 -- a coordinate-regime forcing of exactly the shape Lemma J.1
    wants.  Measured: the converse FAILS (slice nonzero but kappa_c^3 out
    of the span occurs), so F1 is strictly necessary.

    This is the exact h=3 analogue of the P2 h=2 facts (there the obstruction
    space is L^2 (x) L^2, the nine 2x2 minors, and the same antisymmetry
    gives "kappa_c kappa_c' never blocks" and "s^2 forces rank A_pq <= 1").
    The obstruction is degree-3 only: Sym^1 * ker(det d) = Sym^4, so from
    degree 4 on there is no determinantal obstruction -- consistent with
    P2's observation that minimal blocking degrees 2,3,4,5 all occur.

(a) FORCINGS.  The consequence table above is a set of necessary conditions
    on the LOCAL data of the pair (the block A_pq alone) for degree-3
    blocking by an s-carrying monomial.  Verified numerically here.

(c) MEMBERSHIP TEST.  ``blocking_certificate`` decides, by exact rational
    linear algebra on the graded pieces, the minimal degree d <= max_degree
    at which some L-monomial lies in I_d, and returns the monomial.

Run: python3 wsplit_h3_structure.py [--random N] [--max-degree D]
"""

from __future__ import annotations

import itertools
import json
import random
import sys
from fractions import Fraction

import wsplit_core as core
import wsplit_sources as sources
from wsplit_core import (CUBIC_MONOMIALS, COLORS, NCAP, dense_rows,
                         error_matrix, kidx, require)
from wsplit_dichotomy import linear_forms
from wsplit_structural import independent_rows

PERMUTATIONS = tuple(
    (perm, sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j]) % 2)
    for perm in itertools.permutations(range(3))
)
LNAMES = ("s", "kappa_0", "kappa_1", "kappa_2")


# ------------------------------------------------------------------ FACT 1


def det_pairing(cubic: dict):
    """<det(d), G>: the canonical projection onto the determinant line."""
    total = 0
    for perm, inversions in PERMUTATIONS:
        mono = tuple(sorted(kidx(i, perm[i]) for i in range(3)))
        total += (-1) ** inversions * cubic.get(mono, 0)
    return total


def mixed_determinant(m1, m2, m3):
    """D(M1,M2,M3): coefficient of xyz in det(x M1 + y M2 + z M3)."""
    total = 0
    for perm, inversions in PERMUTATIONS:
        sign = (-1) ** inversions
        for assign in itertools.permutations(range(3)):
            mats = (m1, m2, m3)
            term = 1
            for row in range(3):
                term *= mats[assign[row]][row][perm[row]]
            total += sign * term
    return total


def matrix_of_form(form) -> list:
    return [[form[kidx(i, j)] for j in COLORS] for i in COLORS]


def verify_fact1(source) -> dict:
    matrix = error_matrix(source)
    bad = [w for w in core.WORDS if det_pairing(matrix[w]) != 0]
    return {"components": len(matrix), "det_pairing_nonzero": len(bad)}


def verify_fact1_granular(source, word) -> dict:
    """Control: the cancellation happens group-by-group, as the proof says.

    Group the r^3 configurations by the set X of p-sites and check that each
    group's det-pairing vanishes; same for the s r^2 x groups.
    """
    s_form = core.form_s(source)
    s_matrix = matrix_of_form(s_form)
    pvec = {a: [core.block(source, core.P, a, i, word[core.SITE_SLOT[a]])
                for i in COLORS] for a in core.U}
    qvec = {a: [core.block(source, core.Q, a, j, word[core.SITE_SLOT[a]])
                for j in COLORS] for a in core.U}

    def det3(cols):
        total = 0
        for perm, inversions in PERMUTATIONS:
            term = (-1) ** inversions
            for row in range(3):
                term *= cols[row][perm[row]]
            total += term
        return total

    groups_r3 = {}
    for matching in core.MATCHINGS_U:
        for orientation in itertools.product((0, 1), repeat=3):
            xs, ys = [], []
            for (a, b), flip in zip(matching, orientation):
                xs.append(b if flip else a)
                ys.append(a if flip else b)
            key = tuple(sorted(xs))
            # sign-free grouping: value is det[p_xs] * det[q_ys]
            groups_r3.setdefault(key, 0)
            groups_r3[key] += det3([pvec[x] for x in xs]) * det3([qvec[y] for y in ys])

    groups_sr2x = {}
    for matching in core.MATCHINGS_U:
        for skip in range(3):
            edges = [e for n, e in enumerate(matching) if n != skip]
            for orientation in itertools.product((0, 1), repeat=2):
                xs, ys = [], []
                for (a, b), flip in zip(edges, orientation):
                    xs.append(b if flip else a)
                    ys.append(a if flip else b)
                key = (tuple(sorted(xs)), matching[skip])
                groups_sr2x.setdefault(key, 0)
                groups_sr2x[key] += mixed_determinant(
                    s_matrix,
                    [[pvec[xs[0]][i] * qvec[ys[0]][j] for j in COLORS]
                     for i in COLORS],
                    [[pvec[xs[1]][i] * qvec[ys[1]][j] for j in COLORS]
                     for i in COLORS])
    return {"r3_groups": len(groups_r3),
            "r3_groups_nonzero": sum(1 for v in groups_r3.values() if v),
            "sr2x_groups": len(groups_sr2x),
            "sr2x_groups_nonzero": sum(1 for v in groups_sr2x.values() if v)}


# ------------------------------------------- L-monomials and membership


def l_monomials(degree: int) -> list:
    """All monomials in L of the given total degree, as exponent tuples."""
    out = []
    for exps in itertools.product(range(degree + 1), repeat=4):
        if sum(exps) == degree:
            out.append(exps)
    return sorted(out, reverse=True)


def l_monomial_name(exps) -> str:
    parts = []
    for name, power in zip(LNAMES, exps):
        if power:
            parts.append(name if power == 1 else f"{name}^{power}")
    return "*".join(parts)


def expand_l_monomial(exps, forms) -> dict:
    result = {(): Fraction(1)}
    for name, power in zip(LNAMES, exps):
        form = forms[name]
        for _ in range(power):
            nxt: dict = {}
            for mono, coef in result.items():
                for k in range(NCAP):
                    if form[k]:
                        key = tuple(sorted(mono + (k,)))
                        nxt[key] = nxt.get(key, 0) + coef * form[k]
            result = {m: c for m, c in nxt.items() if c}
    return result


def monomial_basis(degree: int) -> tuple:
    return tuple(itertools.combinations_with_replacement(range(NCAP), degree))


BASIS_CACHE: dict = {}
INDEX_CACHE: dict = {}


def basis(degree: int):
    if degree not in BASIS_CACHE:
        BASIS_CACHE[degree] = monomial_basis(degree)
        INDEX_CACHE[degree] = {m: n for n, m in enumerate(BASIS_CACHE[degree])}
    return BASIS_CACHE[degree], INDEX_CACHE[degree]


def graded_piece(generators, degree: int) -> list:
    """Spanning set of I_degree from degree-3 generators."""
    base, index = basis(degree)
    multipliers = monomial_basis(degree - 3) if degree > 3 else ((),)
    out = []
    for row in generators:
        for mult in multipliers:
            vec = [Fraction(0)] * len(base)
            for cidx, coef in enumerate(row):
                if coef:
                    key = tuple(sorted(CUBIC_MONOMIALS[cidx] + mult))
                    vec[index[key]] += coef
            out.append(vec)
    return out


def echelon(vectors):
    rows, pivots = [], []
    for vec in vectors:
        cur = list(vec)
        for pcol, brow in zip(pivots, rows):
            if cur[pcol]:
                factor = cur[pcol] / brow[pcol]
                cur = [a - factor * b for a, b in zip(cur, brow)]
        pcol = next((c for c in range(len(cur)) if cur[c]), None)
        if pcol is None:
            continue
        rows.append(cur)
        pivots.append(pcol)
    return rows, pivots


def reduces_to_zero(rows, pivots, target) -> bool:
    cur = list(target)
    for pcol, brow in zip(pivots, rows):
        if cur[pcol]:
            factor = cur[pcol] / brow[pcol]
            cur = [a - factor * b for a, b in zip(cur, brow)]
    return not any(cur)


def blocking_certificate(source, max_degree: int = 5) -> dict:
    """Minimal-degree L-monomial blocking certificate at this pair."""
    matrix = error_matrix(source)
    rows = [r for r in dense_rows(matrix) if any(r)]
    forms = linear_forms(source)
    dead = all(v == 0 for v in forms["s"])
    if not rows:
        return {"E_is_zero": True, "dead_edge": dead,
                "blocked": dead, "degree": None, "monomials": [],
                "span_dim": 0}
    generators, rank = independent_rows(rows)
    out = {"E_is_zero": False, "dead_edge": dead, "span_dim": rank,
           "blocked": False, "degree": None, "monomials": [],
           "all_degree3": {}}
    for degree in range(3, max_degree + 1):
        base, index = basis(degree)
        piece = graded_piece(generators, degree)
        ech, pivots = echelon(piece)
        hits = []
        for exps in l_monomials(degree):
            poly = expand_l_monomial(exps, forms)
            if not poly:
                continue
            target = [Fraction(0)] * len(base)
            for mono, coef in poly.items():
                target[index[mono]] = coef
            if reduces_to_zero(ech, pivots, target):
                hits.append(l_monomial_name(exps))
        if degree == 3:
            out["all_degree3"] = {l_monomial_name(e): (l_monomial_name(e) in hits)
                                  for e in l_monomials(3)}
        if hits:
            out.update({"blocked": True, "degree": degree, "monomials": hits})
            return out
    return out


# ---------------------------------------------------- forcing predictions


def degree3_obstructions(source) -> dict:
    """D(m) for every degree-3 L-monomial, from the pair block alone."""
    forms = linear_forms(source)
    mats = {name: matrix_of_form(form) for name, form in forms.items()}
    out = {}
    for exps in l_monomials(3):
        chosen = []
        for name, power in zip(LNAMES, exps):
            chosen.extend([mats[name]] * power)
        out[l_monomial_name(exps)] = mixed_determinant(*chosen)
    return out


def monochrome_slice_nonzero(matrix, c: int) -> bool:
    """Is the colour-c monochrome slice error (the K_cc^3 coefficient) != 0?"""
    key = tuple(sorted((kidx(c, c),) * 3))
    return any(matrix[w].get(key, 0) for w in core.WORDS)


def main() -> int:
    args = sys.argv[1:]
    n_random = int(args[args.index("--random") + 1]) if "--random" in args else 25
    max_degree = int(args[args.index("--max-degree") + 1]
                     ) if "--max-degree" in args else 3
    stage_degree = int(args[args.index("--stage-degree") + 1]
                       ) if "--stage-degree" in args else 5

    print("== (b) FACT 1 at h=3: the determinant line annihilates every E_w ==")
    rng = random.Random(20260815)
    fact1 = []
    for trial in range(4):
        src = core.random_source(rng)
        rec = verify_fact1(src)
        fact1.append(rec)
        require(rec["det_pairing_nonzero"] == 0, rec)
        print(f"  random source {trial}: {rec['det_pairing_nonzero']}/729 "
              f"components with nonzero det-pairing")
    granular = verify_fact1_granular(core.random_source(rng), core.WORDS[57])
    print(f"  granular control: r^3 groups {granular['r3_groups']} "
          f"(nonzero {granular['r3_groups_nonzero']}), "
          f"s r^2 x groups {granular['sr2x_groups']} "
          f"(nonzero {granular['sr2x_groups_nonzero']})")
    require(granular["r3_groups_nonzero"] == 0
            and granular["sr2x_groups_nonzero"] == 0, granular)

    print("== (a) degree-3 blocking: obstruction vs. actual membership ==")
    stats = {}
    violations = []
    samples = []
    for trial in range(n_random):
        src = core.random_source(rng, zero_prob=Fraction(1, 2) if trial % 2 else None)
        cert = blocking_certificate(src, max_degree=max_degree)
        obstruction = degree3_obstructions(src)
        matrix = error_matrix(src)
        for c in COLORS:
            name = f"kappa_{c}^3"
            if cert.get("all_degree3", {}).get(name):
                require(monochrome_slice_nonzero(matrix, c),
                        ("F1 violated: kappa_c^3 blocks with a zero "
                         "monochrome slice", c))
        for name, present in cert.get("all_degree3", {}).items():
            entry = stats.setdefault(name, {"in_span": 0, "total": 0,
                                            "obstruction_nonzero": 0})
            entry["total"] += 1
            entry["in_span"] += 1 if present else 0
            if obstruction[name] != 0:
                entry["obstruction_nonzero"] += 1
            if present and obstruction[name] != 0:
                violations.append((trial, name, str(obstruction[name])))
        samples.append({"span_dim": cert["span_dim"], "degree": cert["degree"],
                        "monomials": cert["monomials"][:4]})
    require(not violations, ("FACT 1 forcing violated", violations[:3]))
    for name in sorted(stats, key=lambda n: -stats[n]["in_span"]):
        entry = stats[name]
        print(f"  {name:28s} in span {entry['in_span']:3d}/{entry['total']:3d}"
              f"   D != 0 in {entry['obstruction_nonzero']:3d} sources")
    blocked = sum(1 for s in samples if s["degree"])
    print(f"  blocked (degree <= {max_degree}): {blocked}/{len(samples)}")

    print(f"== (c) membership test on the near-exact source "
          f"(degrees 3..{stage_degree}) ==")
    physical = sources.load_stage_a()
    stage = []
    for p, q in itertools.combinations(range(8), 2):
        src = sources.rechart(physical, p, q)
        cert = blocking_certificate(src, max_degree=stage_degree)
        cert["pair"] = [p, q]
        matrix = error_matrix(src)
        cert["monochrome_slice_nonzero"] = [
            monochrome_slice_nonzero(matrix, c) for c in COLORS]
        stage.append(cert)
        print(f"  ({p},{q}) span={cert['span_dim']:3d} dead={cert['dead_edge']!s:5s}"
              f" blocked={cert['blocked']!s:5s} deg={cert['degree']}"
              f" {cert['monomials'][:3]}")

    payload = {"fact1": fact1, "granular_control": granular,
               "degree3_statistics": stats, "random_samples": samples,
               "stage_a": stage, "max_degree": max_degree,
               "stage_degree": stage_degree}
    with open("h3_structure.json", "w") as handle:
        json.dump(payload, handle, indent=1, sort_keys=True, default=str)
    print("wrote h3_structure.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
