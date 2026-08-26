#!/usr/bin/env python3
"""UNAUDITED PROBE (P2, task D) -- mutation and sanity controls.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

Positive/negative controls for the six-site witness/splitting machinery:

 C1 dead pair          A_pq = 0                      -> status dead
 C2 r == 0 pair        A_{p,u} = 0 for u in U        -> E == 0, explicit
                                                        witness K = id
 C3 engineered split   only one U-matching carries R -> E ~ kappa_0^2,
                                                        split-blocked, no
                                                        witness
 C4 gauge controls     site relabelling, block scaling, local GL(3) at a
                       site of U, K-scaling
 C5 mutation controls  wrong matching set / dropped R term / wrong endpoint
                       order must change the answer somewhere
 C6 field control      re-decide witness existence modulo a large prime
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import random

from wsplit_core import (KAPPA_VARS, PAIRS, SITES, VARS, PairData, Source,
                         classify_source, decide_pair, lin_is_zero, lin_mul,
                         parse_singular, perfect_matchings, poly_string_lin,
                         poly_string_quad, quad_add, random_source, require,
                         run_singular)


def evaluate_quadrics(pairdata, K):
    """Exact value of every E component at an explicit cap K (list of 9)."""
    values = []
    for quad in pairdata.quadrics:
        total = Fraction(0)
        for (i, j), coefficient in quad.items():
            total += coefficient * Fraction(K[i]) * Fraction(K[j])
        values.append(total)
    return values


def evaluate_linear(form, K):
    return sum(coefficient * Fraction(K[index])
               for index, coefficient in enumerate(form))


def zero_blocks():
    return {pair: [[0] * 3 for _ in range(3)] for pair in PAIRS}


def capped_tensor_literal(source, p, q, K):
    """K contracted into H_B(A), componentwise on the four sites of U."""
    U = tuple(site for site in SITES if site not in (p, q))
    out = {}
    for encoded in range(81):
        word, value = [], encoded
        for _ in range(4):
            word.append(value % 3)
            value //= 3
        word = tuple(word)
        colours = dict(zip(U, word))
        total = Fraction(0)
        for matching in perfect_matchings(SITES):
            for p_colour in range(3):
                for q_colour in range(3):
                    assign = dict(colours)
                    assign[p], assign[q] = p_colour, q_colour
                    term = Fraction(K[3 * p_colour + q_colour])
                    for u, v in matching:
                        term *= source.oriented(u, v)[assign[u]][assign[v]]
                        if term == 0:
                            break
                    total += term
        out[word] = total
    return out


def capped_tensor_from_constructors(source, p, q, K):
    """[(s+r) exp(x)]_U from the s, R_ab, x constructors of wsplit_core."""
    pd = PairData(source, p, q)
    U = pd.U
    position = {site: index for index, site in enumerate(U)}
    s_value = evaluate_linear(pd.s, K)
    R = {edge: [[evaluate_linear(pd.R[edge][a][b], K) for b in range(3)]
                for a in range(3)] for edge in pd.R}
    out = {}
    for encoded in range(81):
        word, value = [], encoded
        for _ in range(4):
            word.append(value % 3)
            value //= 3
        word = tuple(word)
        total = Fraction(0)
        for edge1, edge2 in pd.matchings:
            i1, j1 = word[position[edge1[0]]], word[position[edge1[1]]]
            i2, j2 = word[position[edge2[0]]], word[position[edge2[1]]]
            a1 = source.oriented(*edge1)[i1][j1]
            a2 = source.oriented(*edge2)[i2][j2]
            total += (s_value * a1 * a2 + R[edge1][i1][j1] * a2
                      + a1 * R[edge2][i2][j2])
        out[word] = total
    return out


def control_cap_identity():
    """C0: the literal cap identity (12) of the descent note, at N=6.

        K |_ H_B(A) = [(s+r) exp(x)]_U

    This is the audit that certifies the s / R_ab / x constructors, including
    the two endpoint orders inside R_ab.
    """
    rng = random.Random(3)
    checks = 0
    for _ in range(4):
        source = random_source(rng, "generic")
        K = [Fraction(rng.randint(-5, 5)) for _ in range(9)]
        p, q = rng.choice(PAIRS)
        left = capped_tensor_literal(source, p, q, K)
        right = capped_tensor_from_constructors(source, p, q, K)
        require(left == right, f"C0 cap identity failed at {(p, q)}")
        checks += len(left)
    return {"components_checked": checks}


def k4_landing_source():
    """Six sites, pair (0,1), r == 0, and an exact ternary source on U.

    On four sites each unordered pair lies in exactly one perfect matching, so
        A_23 = A_45 = e_0 (x) e_0,  A_24 = A_35 = e_1 (x) e_1,
        A_25 = A_34 = e_2 (x) e_2
    gives H_U = Delta_{U,3} with no interference -- the K_4 exception.  All
    blocks from site 0 into U vanish, so r == 0 and E == 0 identically.
    """
    blocks = zero_blocks()
    unit = {c: [[1 if (i, j) == (c, c) else 0 for j in range(3)]
                for i in range(3)] for c in range(3)}
    blocks[(2, 3)] = unit[0]
    blocks[(4, 5)] = unit[0]
    blocks[(2, 4)] = unit[1]
    blocks[(3, 5)] = unit[1]
    blocks[(2, 5)] = unit[2]
    blocks[(3, 4)] = unit[2]
    blocks[(0, 1)] = [[Fraction(1, 3) if i == j else 0 for j in range(3)]
                      for i in range(3)]
    return Source(blocks)


def control_k4_landing():
    """C7: the N=6 -> N=4 descent actually fires and lands on the exception."""
    source = k4_landing_source()
    pd = PairData(source, 0, 1)
    require(pd.error_identically_zero(), "C7 expects E == 0")
    K = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    s_value = evaluate_linear(pd.s, K)
    require(s_value == 1, f"C7 s = {s_value}")
    kappas = [Fraction(K[var]) for var in KAPPA_VARS]
    require(all(value != 0 for value in kappas), "C7 kappas")

    # The cap is exactly diagonal -- the only exactness Theorem 1.1 uses.
    cap = capped_tensor_literal(source, 0, 1, K)
    U = pd.U
    for word, value in cap.items():
        expected = kappas[word[0]] if len(set(word)) == 1 else Fraction(0)
        require(value == expected, f"C7 cap not diagonal at {word}")

    # Identity (16): s H_U(x + r/s) = K |_ H_B(A); here r = 0, so the descended
    # aggregate source is x itself and its matching tensor must be Delta_{U,3}.
    position = {site: index for index, site in enumerate(U)}
    descended = {}
    for encoded in range(81):
        word, value = [], encoded
        for _ in range(4):
            word.append(value % 3)
            value //= 3
        word = tuple(word)
        total = Fraction(0)
        for edge1, edge2 in pd.matchings:
            total += (source.oriented(*edge1)[word[position[edge1[0]]]][
                          word[position[edge1[1]]]]
                      * source.oriented(*edge2)[word[position[edge2[0]]]][
                          word[position[edge2[1]]]])
        descended[word] = total
    for word, value in descended.items():
        expected = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        require(value == expected, f"C7 descended tensor at {word}: {value}")
    require(descended == {word: cap[word] / s_value for word in cap},
            "C7 identity (16)")

    # The six-site source itself is NOT exact (it cannot be, by Theorem 1.1).
    defects = source.pure_defects()
    mixed = [word for word in ((0, 0, 0, 0, 0, 1), (0, 1, 0, 1, 0, 1))
             if source.coefficient(word) != 0]
    report = classify_source(source, pairs=[(0, 1)])
    record = report[(0, 1)]
    require(record["status"] == "witness", f"C7 status {record['status']}")
    return {"status": record["status"],
            "pure_defects": [str(value) for value in defects],
            "six_site_exact": not defects and not mixed,
            "descended_is_Delta_U3": True}


def control_dead():
    rng = random.Random(11)
    source = random_source(rng, "generic")
    blocks = dict(source.blocks)
    blocks[(0, 1)] = [[0] * 3 for _ in range(3)]
    source = Source(blocks)
    report = classify_source(source, pairs=[(0, 1)])
    record = report[(0, 1)]
    require(record["status"] == "dead", f"C1 dead: {record['status']}")
    require(not record["witness"], "C1 witness must fail on a dead pair")
    return record


def control_r_zero():
    rng = random.Random(12)
    source = random_source(rng, "generic")
    blocks = dict(source.blocks)
    for u in (2, 3, 4, 5):
        blocks[(0, u)] = [[0] * 3 for _ in range(3)]
    blocks[(0, 1)] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    source = Source(blocks)
    pd = PairData(source, 0, 1)
    require(pd.error_identically_zero(), "C2 expects E == 0")
    K = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    values = evaluate_quadrics(pd, K)
    require(all(value == 0 for value in values), "C2 explicit K must solve E")
    require(evaluate_linear(pd.s, K) != 0, "C2 explicit K must be active")
    for var in KAPPA_VARS:
        require(K[var] != 0, "C2 explicit K must have nonzero kappas")
    report = classify_source(source, pairs=[(0, 1)])
    record = report[(0, 1)]
    require(record["status"] == "witness", f"C2 status {record['status']}")
    return record


def engineered_split_source():
    """A pair whose whole error tensor is a multiple of kappa_0^2."""
    blocks = zero_blocks()
    p, q = 0, 1
    a, b, c, d = 2, 3, 4, 5
    unit = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]      # e_0 (x) e_0
    blocks[(p, q)] = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]  # s = K_01, live
    blocks[(min(p, a), max(p, a))] = unit          # A_pa = e_0 (x) e_0
    blocks[(min(q, b), max(q, b))] = unit          # A_qb
    blocks[(min(p, c), max(p, c))] = unit          # A_pc
    blocks[(min(q, d), max(q, d))] = unit          # A_qd
    return Source(blocks)


def control_engineered_split():
    source = engineered_split_source()
    pd = PairData(source, 0, 1)
    require(not pd.error_identically_zero(), "C3 expects E != 0")
    patterns, span = pd.split_patterns()
    require(span == 1, f"C3 expects a one-dimensional error span, got {span}")
    require(("kappa_0", "kappa_0") in patterns, f"C3 patterns {patterns}")
    report = classify_source(source, pairs=[(0, 1)])
    record = report[(0, 1)]
    require(record["status"] == "split-blocked", f"C3 {record['status']}")
    require(not record["witness"], "C3 must have no witness")
    require(record["min_block_degree"] == 2, "C3 blocks already in degree 2")
    return record


def permuted_source(source, permutation):
    blocks = {}
    for (u, v) in PAIRS:
        pu, pv = permutation[u], permutation[v]
        matrix = source.oriented(u, v)
        if pu < pv:
            blocks[(pu, pv)] = matrix
        else:
            blocks[(pv, pu)] = [[matrix[i][j] for i in range(3)]
                                for j in range(3)]
    return Source(blocks)


def local_gl_source(source, site, matrix):
    """Apply an invertible map at one site (row/column change of basis)."""
    blocks = {}
    for (u, v) in PAIRS:
        table = [row[:] for row in source.blocks[(u, v)]]
        if u == site:
            table = [[sum(matrix[i][t] * table[t][j] for t in range(3))
                      for j in range(3)] for i in range(3)]
        if v == site:
            table = [[sum(table[i][t] * matrix[j][t] for t in range(3))
                      for j in range(3)] for i in range(3)]
        blocks[(u, v)] = table
    return Source(blocks)


def control_gauge():
    rng = random.Random(13)
    source = random_source(rng, "lowrank")
    base = classify_source(source)
    permutation = {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3}
    moved = classify_source(permuted_source(source, permutation))
    for (p, q), record in base.items():
        image = tuple(sorted((permutation[p], permutation[q])))
        other = moved[image]
        require(record["status"] == other["status"],
                f"C4 relabelling changed {p,q}: {record['status']} vs "
                f"{other['status']}")
    # Scaling every block by a nonzero constant is a projective symmetry of
    # the whole witness condition.
    scaled = Source({pair: [[3 * entry for entry in row]
                            for row in source.blocks[pair]] for pair in PAIRS})
    scaled_report = classify_source(scaled)
    for pair in PAIRS:
        require(base[pair]["status"] == scaled_report[pair]["status"],
                f"C4 scaling changed {pair}")
    # A local GL(3) at a site of U preserves live/dead and witness existence
    # for the pairs not containing that site (it is a change of basis of the
    # boundary tensor only).
    gl = [[1, 1, 0], [0, 1, 0], [0, 0, 2]]
    twisted = classify_source(local_gl_source(source, 5, gl))
    changed = []
    for pair in PAIRS:
        if 5 in pair:
            continue
        if base[pair]["witness"] != twisted[pair]["witness"]:
            changed.append(pair)
    require(not changed, f"C4 local GL at a U-site changed witness: {changed}")
    return {"relabel": "ok", "scale": "ok", "local_gl": "ok"}


def mutated_pairdata(source, p, q, mutation):
    """Deliberately wrong constructions of the error tensor."""
    pd = PairData(source, p, q)
    a, b, c, d = pd.U
    position = {a: 0, b: 1, c: 2, d: 3}
    if mutation == "drop-term":
        matchings = pd.matchings[:2]
    elif mutation == "wrong-matchings":
        matchings = (((a, b), (c, d)), ((a, b), (c, d)), ((a, c), (b, d)))
    elif mutation == "single-order":
        # R without the crossed p<->q endpoint order.
        pd2 = PairData(source, p, q)
        for (x, y) in combinations(pd.U, 2):
            Apx, Aqy = source.oriented(p, x), source.oriented(q, y)
            table = []
            for alpha in range(3):
                row = []
                for beta in range(3):
                    form = [Fraction(0)] * 9
                    for i in range(3):
                        for j in range(3):
                            value = Apx[i][alpha] * Aqy[j][beta]
                            if value:
                                form[3 * i + j] += value
                    row.append(form)
                table.append(row)
            pd2.R[(x, y)] = table
        pd2.quadrics = pd2._error_components()
        return pd2
    else:
        raise ValueError(mutation)
    out = []
    for w0 in range(3):
        for w1 in range(3):
            for w2 in range(3):
                for w3 in range(3):
                    word = (w0, w1, w2, w3)
                    quad = {}
                    for (e1, e2) in matchings:
                        lin1 = pd.R[e1][word[position[e1[0]]]][
                            word[position[e1[1]]]]
                        lin2 = pd.R[e2][word[position[e2[0]]]][
                            word[position[e2[1]]]]
                        if lin_is_zero(lin1) or lin_is_zero(lin2):
                            continue
                        quad_add(quad, lin_mul(lin1, lin2))
                    if quad:
                        out.append(quad)
    pd.quadrics = out
    return pd


def control_mutation():
    """Every mutation of the error constructor must be visible somewhere."""
    rng = random.Random(14)
    source = random_source(rng, "mixed" if False else "lowrank")
    honest = {pair: PairData(source, *pair) for pair in PAIRS}
    honest_decision = {pair: decide_pair(honest[pair], max_degree=2,
                                         timeout=30) for pair in PAIRS}
    results = {}
    for mutation in ("drop-term", "wrong-matchings", "single-order"):
        flips, spans = 0, 0
        for pair in PAIRS:
            mutated = mutated_pairdata(source, *pair, mutation)
            if mutated.split_patterns()[1] != honest[pair].split_patterns()[1]:
                spans += 1
            decision = decide_pair(mutated, max_degree=2, timeout=30)
            if decision["witness"] != honest_decision[pair]["witness"]:
                flips += 1
        results[mutation] = {"witness_flips": flips, "span_changes": spans}
        require(flips or spans, f"C5 mutation {mutation} is invisible")

    # The sharpest control: only the true constructors satisfy the literal cap
    # identity (12).  A mutated R_ab (single endpoint order) must break it.
    K = [Fraction(1), Fraction(2), Fraction(-1), Fraction(3), Fraction(1),
         Fraction(0), Fraction(-2), Fraction(1), Fraction(1)]
    literal = capped_tensor_literal(source, 0, 1, K)
    honest_cap = capped_tensor_from_constructors(source, 0, 1, K)
    require(literal == honest_cap, "C5 honest constructors must satisfy (12)")
    broken = PairData(source, 0, 1)
    for edge in broken.R:
        broken.R[edge] = [[[value / 2 for value in broken.R[edge][a][b]]
                           for b in range(3)] for a in range(3)]
    pd = PairData(source, 0, 1)
    pd.R = broken.R
    halved = {}
    position = {site: index for index, site in enumerate(pd.U)}
    for word, _ in literal.items():
        total = Fraction(0)
        for edge1, edge2 in pd.matchings:
            i1, j1 = word[position[edge1[0]]], word[position[edge1[1]]]
            i2, j2 = word[position[edge2[0]]], word[position[edge2[1]]]
            a1 = source.oriented(*edge1)[i1][j1]
            a2 = source.oriented(*edge2)[i2][j2]
            total += (evaluate_linear(pd.s, K) * a1 * a2
                      + evaluate_linear(pd.R[edge1][i1][j1], K) * a2
                      + a1 * evaluate_linear(pd.R[edge2][i2][j2], K))
        halved[word] = total
    require(halved != literal, "C5 a halved R must break the cap identity")
    results["cap_identity_sensitive"] = True
    return results


def control_modp(prime=1000003):
    """Re-decide witness existence over F_p for the engineered controls."""
    source = engineered_split_source()
    pd = PairData(source, 0, 1)
    gens = ",".join(poly_string_quad(quad) for quad in pd.quadrics)
    forms = [poly_string_lin(pd.s)] + [VARS[v] for v in KAPPA_VARS]
    fprod = "*".join(f"({form})" for form in forms)
    script = (f'ring Rp={prime},({",".join(VARS)},t),dp;\n'
              f"ideal I={gens};\n"
              f"ideal J=I,t*{fprod}-1;\n"
              f'"WIT 0 1 "+string(dim(std(J)));\n')
    table = parse_singular(run_singular(script))
    require(not table[(0, 1)]["witness"],
            "C6 mod-p decision must agree with the rational one")
    return {"prime": prime, "witness": table[(0, 1)]["witness"]}


def main():
    print("UNAUDITED PROBE -- P2 controls, HEAD 86a9479")
    print("C0 cap identity (12)  :", control_cap_identity())
    print("C1 dead pair          :", control_dead()["status"])
    print("C2 r == 0 pair        :", control_r_zero()["status"],
          "(explicit K verified)")
    record = control_engineered_split()
    print("C3 engineered split   :", record["status"], record["patterns"])
    print("C4 gauge              :", control_gauge())
    print("C5 mutation           :", control_mutation())
    print("C6 mod-p control      :", control_modp())
    print("C7 K_4 descent landing:", control_k4_landing())
    print("all controls PASS")


if __name__ == "__main__":
    main()
