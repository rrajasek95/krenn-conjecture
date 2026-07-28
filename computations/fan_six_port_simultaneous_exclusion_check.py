#!/usr/bin/env python3
"""Exact audits for the simultaneous six-port response-table exclusion.

This checker supports notes/good-pair-fan-six-port-simultaneous-exclusion.md.
It verifies, with exact integer/rational arithmetic:

  1. the reconstruction layer: at N=8 the full divided matching power
     h^[4] of an arbitrary integer aggregate family with the three literal
     zero blocks A_ru=A_rv=A_rw=0 satisfies, termwise,
       * the two-slot pair-contraction identity
         a_cd q^[m-1] + p_c s_d q^[m-2],
       * the three 27-row triple-cofactor tables of the good-pair fan note,
       * the 81-row four-slot common-origin system p_c T_def, and
       * the statement that each of the three tables decomposes sectorwise
         into that same 81-row system (table-exchange redundancy);
     the same resummation identities are verified again at N=10;
  2. the annihilator classification for site-square-zero linear forms
     (exhaustively over F_3 as a sanity sweep, by randomized exact rational
     nullspaces, and by parameter-uniform characteristic-zero Singular
     saturation certificates);
  3. the collapse: if the six off-diagonal products p_c s_d (c != d) vanish
     and the s-triple is linearly independent, all twelve vectors live in a
     single site factor V_x, so every diagonal product p_c s_c vanishes too
     (exhaustive class census over F_3, randomized exact rational Rado
     transversal tests, and the engineered positive family);
  4. nonvacuity of the gauge-rigid full-rank chart at |W|=4 and |W|=6:
     integer block families, all blocks of nonzero integer determinant,
     whose source-Hessian kernel over Q is exactly the vertex-gauge space
     (certified by an exact mod-p rank lower bound plus exact integer gauge
     independence and exact integer gauge annihilation).

Finite-field sweeps are sanity/nonvacuity evidence only; every closure step
quoted by the note is either a uniform characteristic-zero proof in the note
or a parameter-uniform Singular saturation certificate over Q replayed here.

Run from the repository root:
    uv run python computations/fan_six_port_simultaneous_exclusion_check.py
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from fractions import Fraction
from itertools import combinations, product
from math import factorial
from random import Random

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SINGULAR = "/usr/local/bin/Singular"
JSON_OUT = os.path.join(
    REPO, "computations", "fan_six_port_simultaneous_singular_certificates.json"
)

LEDGER: dict[str, object] = {}


# ---------------------------------------------------------------------------
# Exact site-square-zero algebra over the integers.
# An element is a dict: key = tuple of (site, colour) pairs with strictly
# increasing sites, value = integer coefficient.  V_x has dimension 3.
# ---------------------------------------------------------------------------


def strip(elem: dict) -> dict:
    return {k: v for k, v in elem.items() if v}


def add(a: dict, b: dict, scale: int = 1) -> dict:
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + scale * v
    return strip(out)


def merge_keys(ka: tuple, kb: tuple):
    """Merge two sorted site-disjoint keys; None if sites collide."""
    out = []
    i = j = 0
    na, nb = len(ka), len(kb)
    while i < na and j < nb:
        sa, sb = ka[i][0], kb[j][0]
        if sa == sb:
            return None
        if sa < sb:
            out.append(ka[i])
            i += 1
        else:
            out.append(kb[j])
            j += 1
    out.extend(ka[i:])
    out.extend(kb[j:])
    return tuple(out)


def mul(a: dict, b: dict) -> dict:
    out: dict = {}
    if len(a) > len(b):
        a, b = b, a
    for ka, va in a.items():
        for kb, vb in b.items():
            key = merge_keys(ka, kb)
            if key is None:
                continue
            out[key] = out.get(key, 0) + va * vb
    return strip(out)


def divided_power(h: dict, k: int) -> dict:
    """h^[k] = h^k / k!, exact (asserts integrality at every step)."""
    out: dict = {(): 1}
    for step in range(1, k + 1):
        out = mul(out, h)
        nxt = {}
        for key, val in out.items():
            assert val % step == 0, "divided power integrality failed"
            nxt[key] = val // step
        out = nxt
    return out


def contract(elem: dict, slots: list[tuple[int, int]]) -> dict:
    """Extract the coefficient of prod e_c^(site) for the given slots."""
    want = dict(slots)
    out: dict = {}
    for key, val in elem.items():
        entries = dict(key)
        if all(entries.get(s) == c for s, c in want.items()):
            rest = tuple(p for p in key if p[0] not in want)
            out[rest] = out.get(rest, 0) + val
    return strip(out)


# ---------------------------------------------------------------------------
# Aggregate block families.
# blocks[(i, j)] (i < j) is a 3x3 integer matrix, row index at endpoint i,
# column index at endpoint j (endpoint-ordered storage).
# ---------------------------------------------------------------------------


def random_blocks(n: int, rng: Random, zero_pairs=()) -> dict:
    blocks = {}
    zero = {tuple(sorted(p)) for p in zero_pairs}
    for i, j in combinations(range(n), 2):
        if (i, j) in zero:
            blocks[i, j] = [[0] * 3 for _ in range(3)]
        else:
            blocks[i, j] = [
                [rng.choice((-2, -1, -1, 1, 1, 2, 2, 3, 0)) for _ in range(3)]
                for _ in range(3)
            ]
    return blocks


def block_entry(blocks: dict, a: int, ca: int, b: int, cb: int) -> int:
    """Coefficient of e_ca^(a) e_cb^(b) in the aggregate quadratic."""
    if a < b:
        return blocks[a, b][ca][cb]
    return blocks[b, a][cb][ca]


def quadratic(blocks: dict, sites) -> dict:
    """The quadratic internal to the given site set."""
    out: dict = {}
    for i, j in combinations(sorted(sites), 2):
        for a, b in product(range(3), repeat=2):
            v = block_entry(blocks, i, a, j, b)
            if v:
                key = ((i, a), (j, b))
                out[key] = out.get(key, 0) + v
    return strip(out)


def row(blocks: dict, vertex: int, colour: int, targets) -> dict:
    """Endpoint-oriented colour row from `vertex` into `targets`."""
    out: dict = {}
    for x in sorted(targets):
        for b in range(3):
            v = block_entry(blocks, vertex, colour, x, b)
            if v:
                out[((x, b),)] = out.get(((x, b),), 0) + v
    return strip(out)


def sector(elem: dict, site: int, colour: int) -> dict:
    """Coefficient of e_colour^(site) (keys that contain that site factor)."""
    out: dict = {}
    for key, val in elem.items():
        entries = dict(key)
        if entries.get(site) == colour:
            rest = tuple(p for p in key if p[0] != site)
            out[rest] = out.get(rest, 0) + val
    return strip(out)


def degree_zero_at(elem: dict, site: int) -> dict:
    return strip({k: v for k, v in elem.items() if site not in dict(k)})


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for idx in range(1, len(vertices)):
        b = vertices[idx]
        rest = vertices[1:idx] + vertices[idx + 1 :]
        for tail in perfect_matchings(rest):
            yield ((a, b),) + tail


# ---------------------------------------------------------------------------
# Part 1a: two-slot pair-contraction identity at N=8 (general blocks).
# ---------------------------------------------------------------------------


def check_pair_identity() -> None:
    n, m = 8, 4
    rng = Random(20260727)
    blocks = random_blocks(n, rng)
    h = quadratic(blocks, range(n))
    h4 = divided_power(h, m)
    assert all(len(k) == n for k in h4), "h^[m] must be top degree"

    for r, u in ((0, 1), (2, 5)):
        W = [x for x in range(n) if x not in (r, u)]
        qW = quadratic(blocks, W)
        q3 = divided_power(qW, m - 1)
        q2 = divided_power(qW, m - 2)
        nontrivial = 0
        for c, d in product(range(3), repeat=2):
            lhs = contract(h4, [(r, c), (u, d)])
            a_cd = block_entry(blocks, r, c, u, d)
            p_c = row(blocks, r, c, W)
            s_d = row(blocks, u, d, W)
            rhs = add(
                {k: a_cd * v for k, v in q3.items()},
                mul(mul(p_c, s_d), q2),
            )
            assert strip(lhs) == strip(rhs), f"pair identity fails at {(r,u,c,d)}"
            nontrivial += bool(lhs)
        assert nontrivial >= 6, "pair identity check must not be vacuous"
    LEDGER["pair_identity_pairs_checked"] = 2 * 9


# ---------------------------------------------------------------------------
# Part 1b: the three tables and the 81-row common-origin system at N=8.
# ---------------------------------------------------------------------------


def build_named_data(blocks: dict, n: int):
    r, u, v, w = 0, 1, 2, 3
    Y = list(range(4, n))
    data = {
        "Y": Y,
        "qY": quadratic(blocks, Y),
        "p": [row(blocks, r, c, Y) for c in range(3)],
        "s": [row(blocks, u, d, Y) for d in range(3)],
        "t": [row(blocks, v, e, Y) for e in range(3)],
        "g": [row(blocks, w, f, Y) for f in range(3)],
        "buv": [[block_entry(blocks, u, d, v, e) for e in range(3)] for d in range(3)],
        "buw": [[block_entry(blocks, u, d, w, f) for f in range(3)] for d in range(3)],
        "bvw": [[block_entry(blocks, v, e, w, f) for f in range(3)] for e in range(3)],
    }
    return data


def T_def(data: dict, m: int, d: int, e: int, f: int) -> dict:
    """The shared four-slot cofactor response
    (b^uv_de g_f + b^uw_df t_e + b^vw_ef s_d) q_Y^[m-3] + s_d t_e g_f q_Y^[m-4]."""
    qY = data["qY"]
    beta = add(
        add(
            {k: data["buv"][d][e] * val for k, val in data["g"][f].items()},
            {k: data["buw"][d][f] * val for k, val in data["t"][e].items()},
        ),
        {k: data["bvw"][e][f] * val for k, val in data["s"][d].items()},
    )
    out = mul(beta, divided_power(qY, m - 3))
    out = add(
        out,
        mul(
            mul(mul(data["s"][d], data["t"][e]), data["g"][f]),
            divided_power(qY, m - 4),
        ),
    )
    return out


def table_response(blocks: dict, n: int, named: tuple[int, int], spectator: int, m: int):
    """The nine near-top cofactor responses R^{ab}_{de} for the deleted triple
    (r, a, b), on W = B \\ {r,a,b} (spectator remains inside W)."""
    r = 0
    a, b = named
    W = [x for x in range(n) if x not in (r, a, b)]
    qW = quadratic(blocks, W)
    qm2 = divided_power(qW, m - 2)
    qm3 = divided_power(qW, m - 3)
    rows_a = [row(blocks, a, d, W) for d in range(3)]
    rows_b = [row(blocks, b, e, W) for e in range(3)]
    direct = [[block_entry(blocks, a, d, b, e) for e in range(3)] for d in range(3)]
    resp = {}
    for d, e in product(range(3), repeat=2):
        resp[d, e] = add(
            {k: direct[d][e] * v for k, v in qm2.items()},
            mul(mul(rows_a[d], rows_b[e]), qm3),
        )
    return W, resp


def check_tables_and_common_origin_n8() -> None:
    n, m = 8, 4
    rng = Random(20260728)
    blocks = random_blocks(n, rng, zero_pairs=[(0, 1), (0, 2), (0, 3)])
    for pair in ((0, 1), (0, 2), (0, 3)):
        assert all(all(x == 0 for x in rrow) for rrow in blocks[pair])
    h = quadratic(blocks, range(n))
    h4 = divided_power(h, m)
    data = build_named_data(blocks, n)
    p = data["p"]

    # h^[m] equals the sum over perfect matchings of the block products.
    total: dict = {}
    count = 0
    for matching in perfect_matchings(tuple(range(n))):
        count += 1
        term: dict = {(): 1}
        for i, j in matching:
            edge = quadratic(blocks, (i, j))
            term = mul(term, edge)
            if not term:
                break
        total = add(total, term)
    assert strip(total) == strip(h4), "h^[4] != sum over perfect matchings"
    LEDGER["n8_perfect_matchings"] = count

    # Triple-table identities (fan note Prop 4.1) for all three named pairs.
    spectator = {(1, 2): 3, (1, 3): 2, (2, 3): 1}
    for (a, b), spec in spectator.items():
        W, resp = table_response(blocks, n, (a, b), spec, m)
        nontrivial = 0
        for c, d, e in product(range(3), repeat=3):
            lhs = contract(h4, [(0, c), (a, d), (b, e)])
            rhs = mul(p[c], resp[d, e])
            assert strip(lhs) == strip(rhs), f"table identity fails {(a,b,c,d,e)}"
            nontrivial += bool(lhs)
        assert nontrivial >= 9, "table identity check must not be vacuous"

    # Four-slot common-origin system, three sector decompositions, exchange.
    shared = {}
    for d, e, f in product(range(3), repeat=3):
        shared[d, e, f] = T_def(data, m, d, e, f)
    assert sum(bool(v) for v in shared.values()) >= 9

    nontrivial = 0
    for c, d, e, f in product(range(3), repeat=4):
        lhs = contract(h4, [(0, c), (1, d), (2, e), (3, f)])
        rhs = mul(p[c], shared[d, e, f])
        assert strip(lhs) == strip(rhs), f"81-system fails {(c,d,e,f)}"
        nontrivial += bool(lhs)
    assert nontrivial >= 27, "81-system check must not be vacuous"

    # Sector decomposition of each table reproduces the same 81 responses.
    _, resp_uv = table_response(blocks, n, (1, 2), 3, m)
    _, resp_uw = table_response(blocks, n, (1, 3), 2, m)
    _, resp_vw = table_response(blocks, n, (2, 3), 1, m)
    for d, e, f in product(range(3), repeat=3):
        s_uv = sector(resp_uv[d, e], 3, f)
        s_uw = sector(resp_uw[d, f], 2, e)
        s_vw = sector(resp_vw[e, f], 1, d)
        want = strip(shared[d, e, f])
        assert strip(s_uv) == want, f"uv sector fails {(d,e,f)}"
        assert strip(s_uw) == want, f"uw sector fails {(d,e,f)}"
        assert strip(s_vw) == want, f"vw sector fails {(d,e,f)}"
        # The spectator-free part of each response is invisible to every p_c.
        for c in range(3):
            assert not mul(p[c], degree_zero_at(resp_uv[d, e], 3))
            assert not mul(p[c], degree_zero_at(resp_uw[d, f], 2))
            assert not mul(p[c], degree_zero_at(resp_vw[e, f], 1))

    # Matching-partition ledger for one table (direct edge vs three stars).
    r, u, v = 0, 1, 2
    W = tuple(x for x in range(n) if x not in (r, u, v))
    direct = three_star = 0
    for matching in perfect_matchings(tuple(range(n))):
        edges = {tuple(sorted(e)) for e in matching}
        if any(e in edges for e in ((r, u), (r, v))):
            continue
        if (u, v) in edges:
            direct += 1
        else:
            three_star += 1
    assert direct == 15 and three_star == 60
    LEDGER["n8_table_matching_partition"] = {"direct": direct, "three_star": three_star}


# ---------------------------------------------------------------------------
# Part 1c: resummation identities again at N=10 (no full h^[5] needed).
# ---------------------------------------------------------------------------


def check_resummation_n10() -> None:
    n, m = 10, 5
    rng = Random(20260729)
    blocks = random_blocks(n, rng, zero_pairs=[(0, 1), (0, 2), (0, 3)])
    data = build_named_data(blocks, n)
    shared = {}
    for d, e, f in product(range(3), repeat=3):
        shared[d, e, f] = T_def(data, m, d, e, f)

    _, resp_uv = table_response(blocks, n, (1, 2), 3, m)
    _, resp_uw = table_response(blocks, n, (1, 3), 2, m)
    _, resp_vw = table_response(blocks, n, (2, 3), 1, m)
    qY = data["qY"]
    assert sum(bool(v) for v in shared.values()) >= 9
    for d, e, f in product(range(3), repeat=3):
        want = strip(shared[d, e, f])
        assert strip(sector(resp_uv[d, e], 3, f)) == want
        assert strip(sector(resp_uw[d, f], 2, e)) == want
        assert strip(sector(resp_vw[e, f], 1, d)) == want
    # Spectator-free part of the (u,v) response equals the literal
    # b q_Y^[m-2] + s t q_Y^[m-3] block, and every p_c kills it by degree.
    qm2 = divided_power(qY, m - 2)
    qm3 = divided_power(qY, m - 3)
    for d, e in product(range(3), repeat=2):
        base = add(
            {k: data["buv"][d][e] * v for k, v in qm2.items()},
            mul(mul(data["s"][d], data["t"][e]), qm3),
        )
        assert strip(degree_zero_at(resp_uv[d, e], 3)) == strip(base)
        for c in range(3):
            assert not mul(data["p"][c], base)
    LEDGER["n10_resummation_checked"] = 27 * 3


# ---------------------------------------------------------------------------
# Part 2: annihilator classification.
# Linear forms on k sites with V_x = F^3; Ann(p) = {s : ps = 0}.
# ---------------------------------------------------------------------------


def ann_matrix_rows(k: int):
    """Row labels ((i,a),(j,b)) for the pair components of a product."""
    labels = []
    for i, j in combinations(range(k), 2):
        for a, b in product(range(3), repeat=2):
            labels.append((i, a, j, b))
    return labels


def ann_matrix(pvec, k: int, labels):
    """Matrix of s -> ps in coordinates s_{(x,c)}; entries from pvec."""
    rows = []
    for i, a, j, b in labels:
        rowv = [0] * (3 * k)
        rowv[3 * j + b] = pvec[3 * i + a]
        rowv[3 * i + a] = pvec[3 * j + b]
        rows.append(rowv)
    return rows


def nullspace_mod(rows, mod: int):
    """Nullspace basis of the matrix over F_mod."""
    if not rows:
        return []
    ncols = len(rows[0])
    mat = [list(r) for r in rows]
    pivots = []
    rank = 0
    for col in range(ncols):
        piv = next((i for i in range(rank, len(mat)) if mat[i][col] % mod), None)
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        inv = pow(mat[rank][col] % mod, mod - 2, mod)
        mat[rank] = [x * inv % mod for x in mat[rank]]
        for i in range(len(mat)):
            if i != rank and mat[i][col] % mod:
                f = mat[i][col] % mod
                mat[i] = [(x - f * y) % mod for x, y in zip(mat[i], mat[rank])]
        pivots.append(col)
        rank += 1
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free:
        vec = [0] * ncols
        vec[fc] = 1
        for rix, pc in enumerate(pivots):
            vec[pc] = (-mat[rix][fc]) % mod
        basis.append(vec)
    return basis


def rref_mod(vectors, mod: int):
    """Canonical reduced row echelon form (tuple of tuples) over F_mod."""
    mat = [list(v) for v in vectors if any(x % mod for x in v)]
    if not mat:
        return ()
    ncols = len(mat[0])
    rank = 0
    for col in range(ncols):
        piv = next((i for i in range(rank, len(mat)) if mat[i][col] % mod), None)
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        inv = pow(mat[rank][col] % mod, mod - 2, mod)
        mat[rank] = [x * inv % mod for x in mat[rank]]
        for i in range(len(mat)):
            if i != rank and mat[i][col] % mod:
                f = mat[i][col] % mod
                mat[i] = [(x - f * y) % mod for x, y in zip(mat[i], mat[rank])]
        rank += 1
    return tuple(tuple(r) for r in mat[:rank])


def support_of(pvec, k: int):
    return tuple(x for x in range(k) if any(pvec[3 * x + c] % 3 for c in range(3)))


def check_annihilator_f3() -> None:
    """Exhaustive trichotomy over F_3 on 3 sites; targeted sweep on 4 sites."""
    k = 3
    labels = ann_matrix_rows(k)
    counts = {0: 0, 1: 0, 3: 0}
    from itertools import product as iproduct

    for pvec in iproduct(range(3), repeat=9):
        if not any(pvec):
            continue
        supp = support_of(pvec, k)
        basis = nullspace_mod(ann_matrix(pvec, k, labels), 3)
        dim = len(basis)
        if len(supp) >= 3:
            assert dim == 0
        elif len(supp) == 2:
            assert dim == 1
            x, y = supp
            vec = basis[0]
            anti = [0] * 9
            for c in range(3):
                anti[3 * x + c] = pvec[3 * x + c]
                anti[3 * y + c] = (-pvec[3 * y + c]) % 3
            assert rref_mod([vec], 3) == rref_mod([anti], 3)
        else:
            assert dim == 3
            (x,) = supp
            expect = []
            for c in range(3):
                e = [0] * 9
                e[3 * x + c] = 1
                expect.append(e)
            assert rref_mod(basis, 3) == rref_mod(expect, 3)
        counts[dim] += 1
    assert counts == {0: 3 ** 9 - 1 - 78 - 2028, 1: 2028, 3: 78}
    LEDGER["f3_three_site_forms"] = {
        "support>=3": counts[0],
        "support==2": counts[1],
        "support==1": counts[3],
    }

    # Four ambient sites: all forms of support <= 2, plus random support >= 3.
    k = 4
    labels4 = ann_matrix_rows(k)
    checked = 0
    for supp in list(combinations(range(k), 1)) + list(combinations(range(k), 2)):
        locals_ = [range(1, 27)] * len(supp)
        for vals in product(*locals_):
            pvec = [0] * (3 * k)
            for site, code in zip(supp, vals):
                for c in range(3):
                    pvec[3 * site + c] = (code // 3 ** c) % 3
            if support_of(pvec, k) != supp:
                continue
            dim = len(nullspace_mod(ann_matrix(pvec, k, labels4), 3))
            assert dim == (3 if len(supp) == 1 else 1)
            checked += 1
    rng = Random(7)
    for _ in range(2000):
        pvec = [rng.randrange(3) for _ in range(12)]
        if len(support_of(pvec, k)) >= 3:
            assert not nullspace_mod(ann_matrix(pvec, k, labels4), 3)
    LEDGER["f3_four_site_low_support_forms"] = checked


# Exact rational linear algebra -------------------------------------------------


def q_nullspace(rows):
    if not rows:
        return []
    ncols = len(rows[0])
    mat = [[Fraction(x) for x in r] for r in rows]
    pivots = []
    rank = 0
    for col in range(ncols):
        piv = next((i for i in range(rank, len(mat)) if mat[i][col] != 0), None)
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        inv = Fraction(1, 1) / mat[rank][col]
        mat[rank] = [x * inv for x in mat[rank]]
        for i in range(len(mat)):
            if i != rank and mat[i][col] != 0:
                f = mat[i][col]
                mat[i] = [x - f * y for x, y in zip(mat[i], mat[rank])]
        pivots.append(col)
        rank += 1
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free:
        vec = [Fraction(0)] * ncols
        vec[fc] = Fraction(1)
        for rix, pc in enumerate(pivots):
            vec[pc] = -mat[rix][fc]
        basis.append(vec)
    return basis


def q_rank(rows) -> int:
    if not rows:
        return 0
    ncols = len(rows[0])
    mat = [[Fraction(x) for x in r] for r in rows]
    rank = 0
    for col in range(ncols):
        piv = next((i for i in range(rank, len(mat)) if mat[i][col] != 0), None)
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        for i in range(len(mat)):
            if i != rank and mat[i][col] != 0:
                f = mat[i][col] / mat[rank][col]
                mat[i] = [x - f * y for x, y in zip(mat[i], mat[rank])]
        rank += 1
    return rank


def check_annihilator_rational() -> None:
    rng = Random(20260730)
    k = 5
    labels = ann_matrix_rows(k)
    for size in (1, 2, 3, 4):
        for _ in range(15):
            supp = rng.sample(range(k), size)
            pvec = [0] * (3 * k)
            for site in supp:
                while all(pvec[3 * site + c] == 0 for c in range(3)):
                    for c in range(3):
                        pvec[3 * site + c] = rng.randrange(-4, 5)
            dim = len(q_nullspace(ann_matrix(pvec, k, labels)))
            assert dim == {1: 3, 2: 1, 3: 0, 4: 0}[size]
    LEDGER["rational_annihilator_samples"] = 60


# ---------------------------------------------------------------------------
# Part 3: the collapse.
# ---------------------------------------------------------------------------


def check_collapse_f3() -> None:
    """Honest class census over F_3 on three ambient sites.

    Enumerate every nonzero linear form, group by its annihilator subspace,
    compute all pairwise intersections of distinct annihilator spaces, build
    the class graph, and enumerate every ordered class triple whose three
    pairwise intersections are nonzero.  For each such triple decide by
    exhaustive search whether an independent s-triple exists, and whenever it
    does, verify the collapse conclusions.
    """
    k = 3
    labels = ann_matrix_rows(k)
    class_of_form: dict[tuple, int] = {}
    classes: list[tuple] = []
    class_members: dict[int, list[tuple]] = {}
    from itertools import product as iproduct

    for pvec in iproduct(range(3), repeat=9):
        if not any(pvec):
            continue
        basis = nullspace_mod(ann_matrix(pvec, k, labels), 3)
        canon = rref_mod(basis, 3)
        if canon not in class_of_form:
            class_of_form[canon] = len(classes)
            classes.append(canon)
            class_members[class_of_form[canon]] = []
        class_members[class_of_form[canon]].append(pvec)

    nonzero_classes = [i for i, c in enumerate(classes) if c]
    dim_census = {}
    for i in nonzero_classes:
        dim_census[len(classes[i])] = dim_census.get(len(classes[i]), 0) + 1
    # 1,014 antipodal lines (3 supports x 26*26/2) and 3 coordinate factors.
    assert dim_census == {1: 1014, 3: 3}
    LEDGER["f3_collapse_classes"] = {
        "total_annihilator_classes": len(classes),
        "nonzero_annihilator_classes": len(nonzero_classes),
        "antipodal_lines": dim_census[1],
        "coordinate_factors": dim_census[3],
    }

    def space_vectors(canon):
        """All vectors of the F_3 span of the canonical basis."""
        basis = list(canon)
        vecs = set()
        for coeffs in iproduct(range(3), repeat=len(basis)):
            v = [0] * 9
            for cf, b in zip(coeffs, basis):
                for idx in range(9):
                    v[idx] = (v[idx] + cf * b[idx]) % 3
            vecs.add(tuple(v))
        return vecs

    def inter(c1, c2):
        v = space_vectors(classes[c1]) & space_vectors(classes[c2])
        return rref_mod([list(x) for x in v], 3)

    pair_inter: dict[tuple, tuple] = {}
    for c1 in nonzero_classes:
        for c2 in nonzero_classes:
            pair_inter[c1, c2] = inter(c1, c2)

    adjacency = {
        (c1, c2)
        for (c1, c2), val in pair_inter.items()
        if val
    }
    # Discovered structure: intersections of distinct annihilator spaces
    # vanish, so the adjacency relation is exactly the diagonal.
    assert adjacency == {(c, c) for c in nonzero_classes}

    def independent_triple_exists(b0, b1, b2):
        v0 = [v for v in space_vectors(b0) if any(v)]
        v1 = [v for v in space_vectors(b1) if any(v)]
        v2 = [v for v in space_vectors(b2) if any(v)]
        for s0 in v0:
            for s1 in v1:
                if rref_mod([list(s0), list(s1)], 3).__len__() < 2:
                    continue
                for s2 in v2:
                    if len(rref_mod([list(s0), list(s1), list(s2)], 3)) == 3:
                        return True
        return False

    admitting = []
    for c0 in nonzero_classes:
        for c1 in nonzero_classes:
            if (c0, c1) not in adjacency:
                continue
            for c2 in nonzero_classes:
                if (c0, c2) not in adjacency or (c1, c2) not in adjacency:
                    continue
                b2 = pair_inter[c0, c1]
                b1 = pair_inter[c0, c2]
                b0 = pair_inter[c1, c2]
                if independent_triple_exists(b0, b1, b2):
                    admitting.append((c0, c1, c2))

    # Whenever an independent s-triple exists, all p_c share one single-site
    # support and the candidate spaces live at that same site, so every
    # diagonal product p_c s_c vanishes.
    assert admitting, "collapse configuration must be realizable"
    for c0, c1, c2 in admitting:
        assert c0 == c1 == c2
        members = class_members[c0]
        supports = {support_of(p, k) for p in members}
        assert len(supports) == 1
        (supp,) = supports
        assert len(supp) == 1
        site = supp[0]
        span = space_vectors(classes[c0])
        for vec in span:
            assert support_of(vec, k) in ((), (site,))
        # p_c s_c = 0 for every member and every candidate diagonal choice.
        for p in members:
            prod_rows = ann_matrix(p, k, labels)
            for s in span:
                image = [
                    sum(rv * sv for rv, sv in zip(rowv, s)) % 3 for rowv in prod_rows
                ]
                assert not any(image)
    LEDGER["f3_collapse_admitting_class_triples"] = len(admitting)


def rado_independent_transversal(bases) -> bool:
    """Rado: an independent transversal exists iff every subfamily's span
    has dimension at least the subfamily size (subspaces over Q)."""
    for size in (1, 2, 3):
        for subset in combinations(range(3), size):
            stacked = []
            for d in subset:
                stacked.extend(bases[d])
            if q_rank(stacked) < size:
                return False
    return True


def check_collapse_rational() -> None:
    rng = Random(20260731)
    k = 4
    labels = ann_matrix_rows(k)
    positives = negatives = 0
    for trial in range(300):
        kind = trial % 5
        pvecs = []
        if kind == 0:
            site = rng.randrange(k)
            for _ in range(3):
                v = [0] * (3 * k)
                while all(x == 0 for x in v[3 * site : 3 * site + 3]):
                    for c in range(3):
                        v[3 * site + c] = rng.randrange(-3, 4)
                pvecs.append(v)
        else:
            for _ in range(3):
                size = rng.choice((1, 1, 2, 2, 3))
                supp = rng.sample(range(k), size)
                v = [0] * (3 * k)
                for site in supp:
                    while all(v[3 * site + c] == 0 for c in range(3)):
                        for c in range(3):
                            v[3 * site + c] = rng.randrange(-3, 4)
                pvecs.append(v)
        anns = [q_nullspace(ann_matrix(p, k, labels)) for p in pvecs]

        # Intersection of two subspaces via solving membership equations.
        def inter_basis(bas1, bas2):
            if not bas1 or not bas2:
                return []
            cols = []
            for b in bas1:
                cols.append(list(b))
            for b in bas2:
                cols.append([-x for x in b])
            rows = [[cols[j][i] for j in range(len(cols))] for i in range(3 * k)]
            sol = q_nullspace(rows)
            out = []
            for vec in sol:
                comb = [Fraction(0)] * (3 * k)
                for cf, b in zip(vec[: len(bas1)], bas1):
                    comb = [x + cf * y for x, y in zip(comb, b)]
                if any(comb):
                    out.append(comb)
            reduced = []
            for v in out:
                if q_rank(reduced + [v]) > len(reduced):
                    reduced.append(v)
            return reduced

        B = [
            inter_basis(anns[1], anns[2]),
            inter_basis(anns[0], anns[2]),
            inter_basis(anns[0], anns[1]),
        ]
        exists = rado_independent_transversal(B)
        supports = [
            tuple(x for x in range(k) if any(p[3 * x + c] != 0 for c in range(3)))
            for p in pvecs
        ]
        one_site_common = (
            all(len(s) == 1 for s in supports) and len(set(supports)) == 1
        )
        assert exists == one_site_common, f"Rado mismatch at trial {trial}"
        if exists:
            positives += 1
            site = supports[0][0]
            for basis in B:
                for vec in basis:
                    supp = tuple(
                        x for x in range(k) if any(vec[3 * x + c] != 0 for c in range(3))
                    )
                    assert supp in ((), (site,))
        else:
            negatives += 1
    assert positives >= 40 and negatives >= 100
    LEDGER["rational_collapse_trials"] = {"admitting": positives, "blocked": negatives}


# ---------------------------------------------------------------------------
# Part 4: nonvacuity of the gauge-rigid full-rank chart (|W| = 4 and 6).
# ---------------------------------------------------------------------------


def det3_int(a) -> int:
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def check_gauge_rigidity(nw: int, seed: int, prime: int = 1_000_003) -> None:
    rng = Random(seed)
    while True:
        q = {}
        for i, j in combinations(range(nw), 2):
            while True:
                a = [[rng.randrange(1, 9) for _ in range(3)] for _ in range(3)]
                if det3_int(a) != 0:
                    q[i, j] = a
                    break
        # exact integer top-power columns of Z -> Z * q^[nw/2-1]
        qelem = {}
        for (i, j), mat in q.items():
            for a, b in product(range(3), repeat=2):
                if mat[a][b]:
                    qelem[((i, a), (j, b))] = mat[a][b]
        power = divided_power(qelem, nw // 2 - 1)
        labels = []
        columns = []
        for i, j in combinations(range(nw), 2):
            for a, b in product(range(3), repeat=2):
                base = {((i, a), (j, b)): 1}
                col = mul(base, power)
                labels.append((i, j, a, b))
                columns.append(col)
        word_index = {}
        rows = []
        for col in columns:
            vec = {}
            for key, val in col.items():
                if key not in word_index:
                    word_index[key] = len(word_index)
                vec[word_index[key]] = val
            rows.append(vec)
        # mod-p rank of the (exact integer) multiplication matrix
        pivots: dict[int, dict[int, int]] = {}
        for original in rows:
            col = {r: v % prime for r, v in original.items() if v % prime}
            while col:
                piv = min(col)
                if piv not in pivots:
                    inv = pow(col[piv], prime - 2, prime)
                    pivots[piv] = {r: v * inv % prime for r, v in col.items()}
                    break
                f = col[piv]
                base = pivots[piv]
                for r, v in base.items():
                    nv = (col.get(r, 0) - f * v) % prime
                    if nv:
                        col[r] = nv
                    elif r in col:
                        del col[r]
        rank_p = len(pivots)
        domain = 9 * (nw * (nw - 1) // 2)
        if rank_p != domain - (nw - 1):
            continue
        # exact integer gauge vectors, exact independence, exact annihilation
        gauges = []
        for t in range(nw - 1):
            alpha = [0] * nw
            alpha[t] = 1
            alpha[-1] = -1
            gvec = []
            gelem = {}
            for i, j in combinations(range(nw), 2):
                scal = alpha[i] + alpha[j]
                for a, b in product(range(3), repeat=2):
                    gvec.append(scal * q[i, j][a][b])
                    if scal * q[i, j][a][b]:
                        gelem[((i, a), (j, b))] = scal * q[i, j][a][b]
            gauges.append((gvec, gelem))
        assert q_rank([g[0] for g in gauges]) == nw - 1
        for _, gelem in gauges:
            assert not mul(gelem, power), "gauge must be annihilated exactly"
        # Over Q: rank >= rank_p, so ker_Q <= nw-1; the gauge space is an
        # exactly annihilated (nw-1)-dimensional subspace, hence ker_Q is
        # exactly the vertex-gauge space.  All blocks have nonzero integer
        # determinant, so G_3 is the complete graph on nw >= 3 vertices:
        # connected, spanning, nonbipartite.
        LEDGER[f"gauge_rigid_W{nw}"] = {
            "domain": domain,
            "rank_mod_p": rank_p,
            "kernel_dim_over_Q": nw - 1,
            "all_blocks_rank3_over_Q": True,
        }
        return


# ---------------------------------------------------------------------------
# Part 5: parameter-uniform Singular saturation certificates over Q.
# ---------------------------------------------------------------------------


def singular_scripts() -> dict[str, str]:
    c1 = """LIB "elim.lib";
ring R = 0,(a1,a2,a3,t1,t2,t3),dp;
ideal I;
int i,j;
for (i=1; i<=3; i++) { for (j=1; j<=3; j++) { I = I, var(i)*var(3+j); } }
I = simplify(I,2);
int bad = 0;
int w;
for (w=1; w<=3; w++) {
  ideal S = sat(I, ideal(var(w)));
  ideal SS = std(S);
  for (j=1; j<=3; j++) { if (reduce(var(3+j),SS) != 0) { bad = 1; } }
  if (reduce(1,SS) == 0) { bad = 1; }
  kill S; kill SS;
}
if (bad == 0) { "C1PASS"; } else { "C1FAIL"; }
quit;
"""
    c2 = """LIB "elim.lib";
ring R = 0,(a1,a2,a3,b1,b2,b3,c1,c2,c3,d1,d2,d3),dp;
ideal I;
int i,j;
for (i=1; i<=3; i++) { for (j=1; j<=3; j++) {
  I = I, var(i)*var(9+j) + var(6+i)*var(3+j);
} }
I = simplify(I,2);
poly m1 = c1*a2-c2*a1; poly m2 = c1*a3-c3*a1; poly m3 = c2*a3-c3*a2;
poly n1 = d1*b2-d2*b1; poly n2 = d1*b3-d3*b1; poly n3 = d2*b3-d3*b2;
int bad = 0;
int wi, wj;
for (wi=1; wi<=3; wi++) { for (wj=1; wj<=3; wj++) {
  ideal S = sat(I, ideal(var(wi)*var(3+wj)));
  ideal SS = std(S);
  if (reduce(m1,SS) != 0) { bad = 1; }
  if (reduce(m2,SS) != 0) { bad = 1; }
  if (reduce(m3,SS) != 0) { bad = 1; }
  if (reduce(n1,SS) != 0) { bad = 1; }
  if (reduce(n2,SS) != 0) { bad = 1; }
  if (reduce(n3,SS) != 0) { bad = 1; }
  if (reduce(1,SS) == 0) { bad = 1; }
  kill S; kill SS;
} }
if (bad == 0) { "C2PASS"; } else { "C2FAIL"; }
quit;
"""
    c3 = """LIB "elim.lib";
ring R = 0,(a1,a2,a3,b1,b2,b3,c1,c2,c3,u1,u2,u3,v1,v2,v3,w1,w2,w3),dp;
ideal I;
int i,j;
for (i=1; i<=3; i++) { for (j=1; j<=3; j++) {
  I = I, var(i)*var(12+j) + var(9+i)*var(3+j);
  I = I, var(i)*var(15+j) + var(9+i)*var(6+j);
  I = I, var(3+i)*var(15+j) + var(12+i)*var(6+j);
} }
I = simplify(I,2);
int bad = 0;
int wi, wj, wk, k;
for (wi=1; wi<=3; wi++) { for (wj=1; wj<=3; wj++) { for (wk=1; wk<=3; wk++) {
  ideal S = sat(I, ideal(var(wi)*var(3+wj)*var(6+wk)));
  ideal SS = std(S);
  for (k=10; k<=18; k++) { if (reduce(var(k),SS) != 0) { bad = 1; } }
  if (reduce(1,SS) == 0) { bad = 1; }
  kill S; kill SS;
} } }
if (bad == 0) { "C3PASS"; } else { "C3FAIL"; }
quit;
"""
    return {"C1": c1, "C2": c2, "C3": c3}


def run_singular() -> dict:
    scripts = singular_scripts()
    transcript = {}
    with tempfile.TemporaryDirectory() as tmp:
        for name, text in scripts.items():
            path = os.path.join(tmp, f"{name}.sing")
            with open(path, "w", encoding="ascii") as fh:
                fh.write(text)
            proc = subprocess.run(
                [SINGULAR, "-q", path],
                capture_output=True,
                text=True,
                timeout=600,
                check=False,
            )
            out = proc.stdout.strip()
            assert f"{name}PASS" in out.splitlines(), f"Singular {name} failed: {out}"
            transcript[name] = {
                "input_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "output": out,
                "witness_charts": {"C1": 3, "C2": 9, "C3": 27}[name],
                "status": "PASS",
            }
    LEDGER["singular_certificates"] = {
        k: {"witness_charts": v["witness_charts"], "status": v["status"]}
        for k, v in transcript.items()
    }
    return transcript


# ---------------------------------------------------------------------------
# Part 6: the diagonal endgame is a two-line tensor fact; record it.
# ---------------------------------------------------------------------------


def check_diagonal_endgame() -> None:
    for wsize in (1, 4, 6):
        words = []
        for c in range(3):
            words.append(tuple((x, c) for x in range(wsize)))
        assert len(set(words)) == 3
    # a_00 q^[t] = X_0 and a_11 q^[t] = X_1 need q^[t] proportional to two
    # different single words; distinct nonzero words are independent.
    LEDGER["diagonal_endgame"] = "distinct pure colour words are independent"


def main() -> None:
    check_pair_identity()
    print("pair-contraction identity: PASS")
    check_tables_and_common_origin_n8()
    print("N=8 tables, 81-row common-origin system, exchange redundancy: PASS")
    check_resummation_n10()
    print("N=10 resummation identities: PASS")
    check_annihilator_f3()
    print("annihilator trichotomy (exhaustive F_3 sanity sweep): PASS")
    check_annihilator_rational()
    print("annihilator trichotomy (exact rational samples): PASS")
    check_collapse_f3()
    print("collapse class census over F_3: PASS")
    check_collapse_rational()
    print("collapse Rado transversal tests over Q: PASS")
    check_gauge_rigidity(4, 20260724)
    check_gauge_rigidity(6, 20260725)
    print("gauge-rigid full-rank chart nonvacuity (|W|=4,6): PASS")
    check_diagonal_endgame()
    transcript = run_singular()
    print("Singular saturation certificates C1,C2,C3: PASS")
    payload = {"ledger": LEDGER, "singular": transcript}
    with open(JSON_OUT, "w", encoding="ascii") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
    print(f"ledger written to {os.path.relpath(JSON_OUT, REPO)}")
    print("fan six-port simultaneous exclusion checks: PASS")


if __name__ == "__main__":
    main()
