#!/usr/bin/env python3
"""UNAUDITED PROBE -- W5 task B: COEXISTENCE OF THE THREE MONOCHROME SLICES.

Pinned HEAD: 181a4c084a91f1518c2bdfe2f574b9a7df1b1830

Task A settles the scalar half of J.1b in the negative: the pure
normalisation haf(w_c) = 1 is gauge-vacuous, so any forcing must come from
the MIXED equations.  This script isolates exactly how the mixed equations
see the monochrome slices, and measures the (colour x pair) dirtiness
pattern on the available near-exact / shadow data.

B1  STAGE_A (the committed near-exact eight-site source, 6559/6561 rows):
    the full 3 x 28 slice table, with det A_pq, rank A_pq, the P1 blocking
    verdicts, and -- crucially -- WHY each clean slice is clean (support
    collapse vs cancellation).

B2  THE EXACTNESS LAWS FOR SLICES (derived here, verified as identities on
    random sources, so they hold for every source, exact or not).  Write
    w_c(u,v) = A_uv[c][c] for the colour-c slice and
    C^(c)_ab = haf(w_c | B \\ {a,b}) for its hafnian cofactor.

    L1 (one off-colour site; word = c everywhere, d at a):
          H_word = sum_{b != a} A_ab[d][c] * C^(c)_ab .
        Exactness => the off-diagonal (d,c)-row at a is ORTHOGONAL to the
        colour-c cofactor vector at a.  (Laplace expansion; the "derivative
        of haf along a field" the identity hunt asked for -- it exists, but
        it constrains the OFF-DIAGONAL data, not the slice error.)

    L2 (two off-colour sites a, b; word = c everywhere, d at a and b):
          H_word = w_d(a,b) C^(c)_ab
                   + sum_{u != v} A_au[d][c] A_bv[d][c] C^(c)_{ab,uv},
          C^(c)_{ab,uv} = haf(w_c | B \\ {a,b,u,v}).
        So the slice cofactors are the CONSTANT TERM of a quadratic system
        in the off-diagonals.

    L3 (any two-colour word with even classes S, S^c):
          H_word = haf(w_c|_S) haf(w_d|_{S^c}) + (crossing terms),
        the crossing terms carrying >= 2 off-diagonal factors.

    COROLLARY (diagonal/monomial regime).  If every block is diagonal
    (A_uv[i][j] = 0 for i != j) then L2 forces w_d(a,b) C^(c)_ab = 0 for all
    a<b and all c != d; hence at a FULL-RANK pair (all three diagonal
    entries nonzero) ALL THREE slice cofactors C^(c)_pq vanish.

B3  P2's six-site shadow fleet (48 hill-climbs, 42 all-blocked, 36
    pure-normalisable): the 3 x 15 slice table per shadow.

B4  Mutation controls: does STAGE_A's slice cleanliness survive
    perturbation?  (Isolates support-driven cleanliness from accident.)

Run: python3 run_b_coexistence.py
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, product

import slice_core as sc
from slice_core import ekey, haf, require

P1DIR = ("/Users/rishi/workplace/krenn-conjecture/computations/"
         "unaudited-witness-splitting-p1-2026-08-15")
P2DIR = ("/Users/rishi/workplace/krenn-conjecture/computations/"
         "unaudited-witness-splitting-p2-2026-08-15")
COLORS = (0, 1, 2)


def U_of(pair, n):
    return tuple(a for a in range(n) if a not in pair)


def slice_report(source, n=8):
    """Per colour and pair: the scalar slice error, its |.|-version, det/rank."""
    pairs = list(combinations(range(n), 2))
    slices = {c: sc.monochrome_slice(source, c, n) for c in COLORS}
    rec = {"haf_pure": {c: str(haf(slices[c], tuple(range(n))))
                        for c in COLORS},
           "pairs": {}}
    for pair in pairs:
        U = U_of(pair, n)
        blk = source[ekey(*pair)]
        entry = {"det": str(sc.det3(blk)), "rank": sc.rank3(blk),
                 "slice_error": {}, "abs_slice_error": {},
                 "clean": [], "clean_by_support": []}
        for c in COLORS:
            val = sc.slice_error(slices[c], pair[0], pair[1], U)
            av = sc.slice_error_abs(slices[c], pair[0], pair[1], U)
            entry["slice_error"][c] = str(val)
            entry["abs_slice_error"][c] = str(av)
            if val == 0:
                entry["clean"].append(c)
                entry["clean_by_support"].append(av == 0)
        rec["pairs"][f"{pair[0]},{pair[1]}"] = entry
    return rec


def block_b1(out):
    print("== B1  STAGE_A: the 3 x 28 monochrome slice table ==")
    if P1DIR not in sys.path:
        sys.path.insert(0, P1DIR)
    import wsplit_sources as p1src            # noqa: E402
    physical = p1src.load_stage_a()
    defects = p1src.ghz_defects(physical)
    rec = slice_report(physical, 8)
    rec["ghz_defect_rows"] = defects
    # which words are the defects?
    bad = []
    for word in product(COLORS, repeat=8):
        target = 1 if len(set(word)) == 1 else 0
        if sc.ghz_row(physical, word) != target:
            bad.append("".join(map(str, word)))
    rec["defect_words"] = bad
    print(f"  GHZ defect rows: {defects}  words {bad}")
    print(f"  pure coefficients haf(w_c): {rec['haf_pure']}")
    # P1's blocking verdicts, for the cross-tab
    with open(f"{P1DIR}/h3_structure.json") as fh:
        p1 = json.load(fh)
    verdict = {tuple(e["pair"]): e for e in p1["stage_a"]}
    hdr = ("  pair  rank det!=0 | scalar-clean colours | tensor-clean (P1) "
           "| blocked deg")
    print(hdr)
    fullrank_all_dirty = []
    fullrank = 0
    for pair in combinations(range(8), 2):
        key = f"{pair[0]},{pair[1]}"
        e = rec["pairs"][key]
        v = verdict[pair]
        tensor_clean = [c for c in COLORS
                        if not v["monochrome_slice_nonzero"][c]]
        det_nonzero = e["det"] != "0"
        if det_nonzero:
            fullrank += 1
            if not e["clean"]:
                fullrank_all_dirty.append(pair)
        print(f"  {pair}  {e['rank']}   {str(det_nonzero):5s} | "
              f"{e['clean']}{' (support)' if all(e['clean_by_support']) and e['clean'] else ''}"
              f" | {tensor_clean} | {v['blocked']} {v['degree']}")
        e["tensor_clean_colours"] = tensor_clean
        e["p1_blocked"] = v["blocked"]
        e["p1_degree"] = v["degree"]
    rec["full_rank_pairs"] = fullrank
    rec["full_rank_pairs_with_all_three_slices_dirty"] = [
        list(p) for p in fullrank_all_dirty]
    n_clean = sum(len(rec["pairs"][f"{a},{b}"]["clean"])
                  for a, b in combinations(range(8), 2))
    n_cancel = sum(1 for a, b in combinations(range(8), 2)
                   for flag in rec["pairs"][f"{a},{b}"]["clean_by_support"]
                   if not flag)
    rec["clean_slice_count"] = n_clean
    rec["clean_by_cancellation_count"] = n_cancel
    print(f"  full-rank pairs: {fullrank}/28; of these, "
          f"{len(fullrank_all_dirty)} have ALL THREE slices dirty: "
          f"{fullrank_all_dirty}")
    print(f"  clean (colour,pair) slots: {n_clean}/84, of which "
          f"{n_cancel} by cancellation and {n_clean - n_cancel} by support")
    out["B1_stage_a"] = rec


def block_b2(rng, out):
    print("== B2  the exactness laws L1, L2, L3 (exact identity checks) ==")
    if P1DIR not in sys.path:
        sys.path.insert(0, P1DIR)
    import wsplit_core as p1core             # noqa: E402
    rec = {"L1": 0, "L2": 0, "L3": 0}
    for _ in range(4):
        src = p1core.random_source(rng, -5, 5)
        slices = {c: sc.monochrome_slice(src, c) for c in COLORS}
        cof = {c: {e: sc.cofactor(slices[c], tuple(range(8)), *e)
                   for e in combinations(range(8), 2)} for c in COLORS}
        # L1
        for a in range(8):
            for c, d in [(x, y) for x in COLORS for y in COLORS if x != y]:
                word = tuple(d if t == a else c for t in range(8))
                lhs = sc.ghz_row(src, word)
                rhs = sum(src[ekey(a, b)][d][c] if a < b
                          else src[ekey(a, b)][c][d]
                          for b in range(8) if b != a
                          for _ in [0]) * 0
                rhs = 0
                for b in range(8):
                    if b == a:
                        continue
                    entry = (src[(a, b)][d][c] if a < b
                             else src[(b, a)][c][d])
                    rhs += entry * cof[c][ekey(a, b)]
                require(lhs == rhs, ("L1 failed", a, c, d))
                rec["L1"] += 1
        # L2
        for a, b in combinations(range(8), 2):
            for c, d in [(x, y) for x in COLORS for y in COLORS if x != y]:
                word = tuple(d if t in (a, b) else c for t in range(8))
                lhs = sc.ghz_row(src, word)
                rhs = src[(a, b)][d][d] * cof[c][(a, b)]
                rest = [t for t in range(8) if t not in (a, b)]
                for u in rest:
                    for v in rest:
                        if u == v:
                            continue
                        ea = src[(a, u)][d][c] if a < u else src[(u, a)][c][d]
                        eb = src[(b, v)][d][c] if b < v else src[(v, b)][c][d]
                        sub = tuple(t for t in rest if t not in (u, v))
                        rhs += ea * eb * haf(slices[c], sub)
                require(lhs == rhs, ("L2 failed", a, b, c, d))
                rec["L2"] += 1
        # L3: the class-respecting part of an even split is the product of
        # the two slice hafnians.
        for c, d in [(0, 1), (1, 2), (0, 2)]:
            for S in combinations(range(8), 4):
                Sc = tuple(t for t in range(8) if t not in S)
                word = tuple(c if t in S else d for t in range(8))
                lhs = sc.ghz_row(src, word)
                respecting = haf(slices[c], S) * haf(slices[d], Sc)
                crossing = 0
                for matching in sc.perfect_matchings(tuple(range(8))):
                    if all((x in S) == (y in S) for x, y in matching):
                        continue
                    term = 1
                    for x, y in matching:
                        term *= src[ekey(x, y)][word[min(x, y)]][
                            word[max(x, y)]]
                        if term == 0:
                            break
                    crossing += term
                require(lhs == respecting + crossing, "L3 failed")
                rec["L3"] += 1
                break                      # one split per colour pair is enough
    print(f"  L1 verified on {rec['L1']} words, L2 on {rec['L2']}, "
          f"L3 on {rec['L3']}")

    # COROLLARY: diagonal (monomial) regime.
    diag_hits = {"sources": 0, "full_rank_pairs": 0, "cofactors_forced": 0}
    for _ in range(200):
        src = p1core.random_source(rng, -4, 4)
        for e in src:                             # kill all off-diagonals
            for i in COLORS:
                for j in COLORS:
                    if i != j:
                        src[e][i][j] = 0
        slices = {c: sc.monochrome_slice(src, c) for c in COLORS}
        diag_hits["sources"] += 1
        for pair in combinations(range(8), 2):
            blk = src[ekey(*pair)]
            if sc.det3(blk) == 0:
                continue
            diag_hits["full_rank_pairs"] += 1
            # L2 with all off-diagonals zero says w_d(a,b) C^(c)_ab = 0.
            for c in COLORS:
                for d in COLORS:
                    if d == c:
                        continue
                    word = tuple(d if t in pair else c for t in range(8))
                    lhs = sc.ghz_row(src, word)
                    require(lhs == src[ekey(*pair)][d][d]
                            * sc.cofactor(slices[c], tuple(range(8)), *pair),
                            "diagonal-regime L2 reduction")
                    diag_hits["cofactors_forced"] += 1
        if diag_hits["sources"] >= 3:
            break
    rec["diagonal_regime"] = diag_hits
    print("  diagonal regime: L2 reduces to w_d(a,b) C^(c)_ab = 0 "
          f"({diag_hits['cofactors_forced']} instances); so exactness + "
          "full rank at (p,q) => all three slice cofactors C^(c)_pq vanish")
    out["B2_laws"] = rec


def tensor_slice_error_n6(blocks, p, q, c):
    """The h=2 analogue of P1's tensor slice error: the coefficient of
    K_cc^2 in E_w, over all 81 boundary words w on U (|U| = 4).

    Returns the list of the 81 coefficients (all zero == TENSOR-clean, the
    condition F1 needs; the scalar slice error is the w = c^4 entry)."""
    U = tuple(a for a in range(6) if a not in (p, q))

    def blk(u, v, cu, cv):
        return (blocks[(u, v)][cu][cv] if u < v else blocks[(v, u)][cv][cu])

    out = []
    for word in product(COLORS, repeat=4):
        col = dict(zip(U, word))
        total = 0
        for matching in sc.perfect_matchings(U):
            prod_r = 1
            for a, b in matching:
                prod_r *= (blk(p, a, c, col[a]) * blk(q, b, c, col[b])
                           + blk(p, b, c, col[b]) * blk(q, a, c, col[a]))
            total += prod_r
        out.append(total)
    return out


def shadow_slice_row(blocks, n=6):
    """Per-pair slice data for a six-site source."""
    slices = {c: sc.monochrome_slice(blocks, c, n) for c in COLORS}
    rec = {"pure": {c: str(haf(slices[c], tuple(range(n)))) for c in COLORS},
           "pairs": {}, "full_rank_pairs": 0, "full_rank_all_three_dirty": 0,
           "full_rank_all_three_tensor_dirty": 0,
           "clean_by_support": 0, "clean_by_cancellation": 0}
    for pair in combinations(range(n), 2):
        U = U_of(pair, n)
        clean, tclean, supp = [], [], []
        for c in COLORS:
            val = sc.slice_error(slices[c], pair[0], pair[1], U)
            if val == 0:
                clean.append(c)
                by_support = sc.slice_error_abs(
                    slices[c], pair[0], pair[1], U) == 0
                supp.append(by_support)
                rec["clean_by_support" if by_support
                    else "clean_by_cancellation"] += 1
            if not any(tensor_slice_error_n6(blocks, pair[0], pair[1], c)):
                tclean.append(c)
        det = sc.det3(blocks[pair])
        rec["pairs"][f"{pair[0]},{pair[1]}"] = {
            "clean": clean, "tensor_clean": tclean,
            "clean_by_support": supp, "det_nonzero": det != 0,
            "rank": sc.rank3(blocks[pair])}
        if det != 0:
            rec["full_rank_pairs"] += 1
            if not clean:
                rec["full_rank_all_three_dirty"] += 1
            if not tclean:
                rec["full_rank_all_three_tensor_dirty"] += 1
    return rec


def block_b3(out):
    print("== B3  P2's six-site shadow fleet: the 3 x 15 slice table ==")
    with open(f"{P2DIR}/results_c.json") as fh:
        p2 = json.load(fh)
    hunts = p2["hunts"]
    rows = []
    skipped = 0
    shadow_blocks = []
    for rec in hunts:
        if "blocks" not in rec:
            skipped += 1
            continue
        blocks = {}
        for key, tab in rec["blocks"].items():
            a, b = eval(key)                              # noqa: S307
            blocks[(a, b)] = [[Fraction(v) for v in row] for row in tab]
        shadow_blocks.append(blocks)
        row = shadow_slice_row(blocks)
        row.update({"seed": rec["seed"], "stratum": rec["stratum"],
                    "all_live_blocked": rec["all_live_blocked"],
                    "pure_normalisable": rec["pure_normalisable"]})
        rows.append(row)
    # the committed all-blocked example ships separately
    with open(f"{P2DIR}/example_all_blocked.json") as fh:
        ex = json.load(fh)
    blocks = {}
    for key, tab in ex["blocks"].items():
        a, b = eval(key)                                  # noqa: S307
        blocks[(a, b)] = [[Fraction(v) for v in row] for row in tab]
    slices = {c: sc.monochrome_slice(blocks, c, 6) for c in COLORS}
    exrec = {"source": "example_all_blocked.json",
             "pure": {c: str(haf(slices[c], tuple(range(6))))
                      for c in COLORS},
             "pairs": {}}
    fr = fr_dirty = 0
    for pair in combinations(range(6), 2):
        U = U_of(pair, 6)
        cl = [c for c in COLORS
              if sc.slice_error(slices[c], pair[0], pair[1], U) == 0]
        det = sc.det3(blocks[pair])
        exrec["pairs"][f"{pair[0]},{pair[1]}"] = {
            "clean": cl, "det_nonzero": det != 0,
            "rank": sc.rank3(blocks[pair])}
        if det != 0:
            fr += 1
            if not cl:
                fr_dirty += 1
    exrec["full_rank_pairs"] = fr
    exrec["full_rank_all_three_dirty"] = fr_dirty
    print(f"  committed all-blocked example: pure {exrec['pure']}, "
          f"full-rank pairs {fr}, of which all-three-slices-dirty {fr_dirty}")
    out.setdefault("B3_example", exrec)

    tot = len(rows)
    allb = [r for r in rows if r["all_live_blocked"]]
    fr_total = sum(r["full_rank_pairs"] for r in allb)
    fr_dirty = sum(r["full_rank_all_three_dirty"] for r in allb)
    fr_tdirty = sum(r["full_rank_all_three_tensor_dirty"] for r in allb)
    print(f"  shadows: {tot}; all-live-blocked: {len(allb)}; "
          f"full-rank pairs across the fleet: {fr_total}")
    print(f"  full-rank pairs with ALL THREE slices dirty (scalar): "
          f"{fr_dirty}/{fr_total};  tensor: {fr_tdirty}/{fr_total}")
    hist = {}
    for r in allb:
        k = (r["full_rank_pairs"], r["full_rank_all_three_dirty"])
        hist[str(k)] = hist.get(str(k), 0) + 1
    print(f"  (full-rank pairs, of which all-three-dirty) histogram: {hist}")
    supp = sum(r["clean_by_support"] for r in allb)
    canc = sum(r["clean_by_cancellation"] for r in allb)
    print(f"  clean (colour,pair) slots across the fleet: support {supp}, "
          f"cancellation {canc}")

    # ---- CONTROLS ----------------------------------------------------------
    rng = random.Random(31337)
    ctl = {}
    # C1 dense random six-site sources: how often is a full-rank pair
    #    all-three-dirty?
    tot_fr = dirty_fr = 0
    for _ in range(60):
        blocks = {e: [[rng.randint(-6, 6) for _ in COLORS] for _ in COLORS]
                  for e in combinations(range(6), 2)}
        row = shadow_slice_row(blocks)
        tot_fr += row["full_rank_pairs"]
        dirty_fr += row["full_rank_all_three_dirty"]
    ctl["dense_random"] = {"full_rank_pairs": tot_fr,
                           "all_three_dirty": dirty_fr}
    print(f"  CONTROL dense random sources: {dirty_fr}/{tot_fr} full-rank "
          f"pairs have all three slices dirty")
    # C2 support-matched randomisation of each shadow: keep the zero pattern,
    #    randomise every nonzero entry.  Isolates SUPPORT from exactness.
    tot_fr = dirty_fr = 0
    for blocks in shadow_blocks:
        rnd = {e: [[(rng.randint(-6, 6) or 1) if blocks[e][i][j] != 0 else 0
                    for j in COLORS] for i in COLORS] for e in blocks}
        row = shadow_slice_row(rnd)
        tot_fr += row["full_rank_pairs"]
        dirty_fr += row["full_rank_all_three_dirty"]
    ctl["support_matched"] = {"full_rank_pairs": tot_fr,
                              "all_three_dirty": dirty_fr}
    print(f"  CONTROL support-matched randomisation of the fleet: "
          f"{dirty_fr}/{tot_fr} full-rank pairs all-three-dirty")
    # C3 rank-matched random sources: same per-pair ranks, random otherwise.
    tot_fr = dirty_fr = 0
    for blocks in shadow_blocks:
        rnd = {}
        for e, tab in blocks.items():
            r = sc.rank3(tab)
            if r == 0:
                rnd[e] = [[0] * 3 for _ in range(3)]
                continue
            cols = [[rng.randint(-4, 4) for _ in range(r)] for _ in range(3)]
            rows_ = [[rng.randint(-4, 4) for _ in range(3)] for _ in range(r)]
            rnd[e] = [[sum(cols[i][k] * rows_[k][j] for k in range(r))
                       for j in range(3)] for i in range(3)]
        row = shadow_slice_row(rnd)
        tot_fr += row["full_rank_pairs"]
        dirty_fr += row["full_rank_all_three_dirty"]
    ctl["rank_matched"] = {"full_rank_pairs": tot_fr,
                           "all_three_dirty": dirty_fr}
    print(f"  CONTROL rank-matched random sources: {dirty_fr}/{tot_fr} "
          f"full-rank pairs all-three-dirty")
    out["B3_shadows"] = {"rows": rows, "histogram": hist,
                         "all_blocked": len(allb),
                         "full_rank_pairs_total": fr_total,
                         "full_rank_all_three_dirty_total": fr_dirty,
                         "full_rank_all_three_tensor_dirty_total": fr_tdirty,
                         "clean_by_support": supp,
                         "clean_by_cancellation": canc,
                         "controls": ctl, "skipped_records": skipped}


def block_b4(rng, out):
    print("== B4  mutation controls on STAGE_A ==")
    if P1DIR not in sys.path:
        sys.path.insert(0, P1DIR)
    import wsplit_sources as p1src           # noqa: E402
    physical = p1src.load_stage_a()
    base = slice_report(physical, 8)
    base_clean = sum(len(base["pairs"][k]["clean"]) for k in base["pairs"])
    res = {"baseline_clean_slots": base_clean, "mutations": []}
    # M1 dense perturbation of every entry (destroys support AND exactness)
    for eps_num in (1, 3):
        src = {e: [[physical[e][i][j] + Fraction(eps_num * rng.randint(-3, 3),
                                                 100)
                    for j in COLORS] for i in COLORS] for e in physical}
        rep = slice_report(src, 8)
        clean = sum(len(rep["pairs"][k]["clean"]) for k in rep["pairs"])
        res["mutations"].append({"kind": f"dense perturbation eps~{eps_num}/100",
                                 "clean_slots": clean})
        print(f"  dense perturbation ({eps_num}/100): clean slots "
              f"{clean}/84 (baseline {base_clean})")
    # M2 support-preserving perturbation (only nonzero entries move)
    src = {e: [[(physical[e][i][j] * Fraction(100 + rng.randint(-9, 9), 100)
                 if physical[e][i][j] != 0 else 0)
                for j in COLORS] for i in COLORS] for e in physical}
    rep = slice_report(src, 8)
    clean = sum(len(rep["pairs"][k]["clean"]) for k in rep["pairs"])
    res["mutations"].append({"kind": "support-preserving perturbation",
                             "clean_slots": clean})
    print(f"  support-preserving perturbation: clean slots {clean}/84 "
          f"(baseline {base_clean})")
    # M3 gauge mutation: rescale one site's blocks -- must not move anything
    lam = Fraction(3, 5)
    src = {e: [[physical[e][i][j] * (lam if 0 in e else 1) for j in COLORS]
               for i in COLORS] for e in physical}
    rep = slice_report(src, 8)
    clean = sum(len(rep["pairs"][k]["clean"]) for k in rep["pairs"])
    require(clean == base_clean, "gauge mutation moved the pattern")
    res["mutations"].append({"kind": "site-0 gauge rescale (control)",
                             "clean_slots": clean})
    print(f"  site gauge rescale (control): clean slots {clean}/84 -- "
          "unchanged, as the gauge theorem requires")
    # M4 colour permutation control
    perm = (1, 2, 0)
    src = {e: [[physical[e][perm.index(i)][perm.index(j)] for j in COLORS]
               for i in COLORS] for e in physical}
    rep = slice_report(src, 8)
    clean = sum(len(rep["pairs"][k]["clean"]) for k in rep["pairs"])
    require(clean == base_clean, "colour permutation moved the count")
    res["mutations"].append({"kind": "colour permutation (control)",
                             "clean_slots": clean})
    print(f"  colour permutation (control): clean slots {clean}/84 -- "
          "unchanged, as equivariance requires")
    out["B4_mutations"] = res


def main():
    rng = random.Random(770077)
    out = {"note": "UNAUDITED PROBE W5 task B",
           "head": "181a4c084a91f1518c2bdfe2f574b9a7df1b1830"}
    block_b1(out)
    block_b2(rng, out)
    block_b3(out)
    block_b4(rng, out)
    with open("results_b_coexistence.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=str)
    print("wrote results_b_coexistence.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
