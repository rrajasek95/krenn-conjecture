"""Transfer test: does U7H survive translation to OUR bicoloured cell model?

UNAUDITED EXTERNAL IMPORT AUDIT.  Nothing here is a repository claim.

Our model (proofs/six-site-arbitrary-complex-obstruction.md, notes/
2026-08-11-signed-matching-holonomy-programme.md):  N vertices, palette
{0,1,2}, cells a_uv(i,j), and for each colouring chi

    H_chi = sum_{M in PM}  prod_{uv in M} a_uv(chi_u, chi_v)  =  haf(W^chi),
    W^chi_uv = a_uv(chi_u, chi_v).

So every colouring fibre IS a pure hafnian of a hollow symmetric matrix, and
the external theorem applies fibrewise.  The question this script settles is
which *minimality quantifier* the import needs:

  (M-vert)  external: R = least-CARDINALITY VERTEX SUBSET with h(R)=0 and a
            supported perfect matching.
  (M-cell)  ours (programme note Problem 2): S = minimal CELL SUPPORT, i.e.
            no cell of S can be deleted while keeping the configuration a
            (near-)counterexample.

Test 1 (structural freedom): for a fixed mixed chi the fibre matrix W^chi is
an *arbitrary* hollow symmetric matrix, because cell (uv, chi_u, chi_v) is a
free parameter used by no constraint that a single-fibre statement sees.  We
verify this by realising a prescribed W^chi inside a full cell system.

Test 2 (the import target): at CELL-minimal 6-vertex configurations, is the
allowed-edge graph of the vanishing mixed fibre connected and matching
covered on all of V?

Test 3 (census stratification): repeat Test 2 across the 19 rank-defect graph
types of proofs/six-site-arbitrary-complex-obstruction.md eq. (7), imposing
the repo's own rank budget (rank-one on R-edges, rank != 1 on F-edges).

Exact arithmetic only.  Run:  python3 transfer_six_vertex.py
"""

from __future__ import annotations

import random
from fractions import Fraction
from itertools import combinations
from typing import Dict, List, Optional, Sequence, Tuple

from u7h_core import (
    GQ,
    ONE,
    ZERO,
    Cell,
    Edge,
    active_cofactor_graph,
    allowed_edge_graph,
    components,
    fibre_coefficient,
    fibre_weights,
    hafnian,
    is_connected,
    is_matching_covered,
    least_cancellation,
    supported_matchings,
)

N = 6
D = 3
VERTS = tuple(range(N))
PAIRS = tuple(combinations(VERTS, 2))
CONSTANT_CHIS = tuple(tuple([c] * N) for c in range(D))


# ------------------------------------------------------------------ helpers


def all_chis() -> List[Tuple[int, ...]]:
    out = []
    def rec(pref):
        if len(pref) == N:
            out.append(tuple(pref))
            return
        for c in range(D):
            rec(pref + [c])
    rec([])
    return out


def mixed_chis() -> List[Tuple[int, ...]]:
    return [c for c in all_chis() if len(set(c)) > 1]


def fibre_live(cells: Dict[Cell, GQ], chi) -> bool:
    return bool(supported_matchings(VERTS, fibre_weights(cells, chi, N)))


def constants_all_nonzero(cells: Dict[Cell, GQ]) -> bool:
    return all(bool(fibre_coefficient(cells, chi, N)) for chi in CONSTANT_CHIS)


def is_cell_minimal(cells: Dict[Cell, GQ], chi_star) -> Tuple[bool, List[Cell]]:
    """S is cell-minimal for the property

        P(S) :=  H_chi_star = 0, fibre chi_star has a supported PM,
                 and all three constant fibres are nonzero.

    Returns (minimal?, list of deletable cells).
    """
    deletable = []
    for c in list(cells):
        trial = dict(cells)
        del trial[c]
        if (
            not fibre_coefficient(trial, chi_star, N)
            and fibre_live(trial, chi_star)
            and constants_all_nonzero(trial)
        ):
            deletable.append(c)
    return (not deletable), deletable


def report_fibre(cells: Dict[Cell, GQ], chi) -> Dict[str, object]:
    w = fibre_weights(cells, chi, N)
    allow_V = allowed_edge_graph(VERTS, w)
    act_V = active_cofactor_graph(VERTS, w)
    R = least_cancellation(VERTS, w)
    out: Dict[str, object] = {
        "chi": chi,
        "H_chi": fibre_coefficient(cells, chi, N),
        "fibre_support": sorted(w),
        "allowed_on_V": sorted(allow_V),
        "active_on_V": sorted(act_V),
        "allowed_eq_active_on_V": allow_V == act_V,
        "connected_on_V": is_connected(VERTS, allow_V) if allow_V else False,
        "matching_covered_on_V": is_matching_covered(VERTS, allow_V),
        "components_on_V": components(VERTS, allow_V),
        "R": R,
    }
    if R is not None:
        A = active_cofactor_graph(R, w)
        out["R_proper"] = len(R) < N
        out["allowed_eq_active_on_R"] = A == allowed_edge_graph(R, w)
        out["connected_on_R"] = is_connected(R, A)
        out["matching_covered_on_R"] = is_matching_covered(R, A)
    return out


# ------------------------------------------------- Test 1 + 2 : the witness


def build_witness() -> Tuple[Dict[Cell, GQ], Tuple[int, ...]]:
    """A cell-minimal 6-vertex configuration whose mixed cancellation has a
    DISCONNECTED allowed-edge graph on V.

    chi* = (0,1,0,1,2,2).  Fibre chi*:  4-cycle 0-1-2-3-0 that cancels,
    plus the isolated matched pair 45.  All three constant fibres are made
    nonzero on disjoint cells, each with a unique perfect matching.
    """
    chi = (0, 1, 0, 1, 2, 2)
    cells: Dict[Cell, GQ] = {}

    def put(u, v, i, j, val):
        cells[(u, v, i, j)] = GQ(val)

    # --- fibre chi*: the cancelling C4 on {0,1,2,3}
    put(0, 1, chi[0], chi[1], 1)     # (0,1,0,1)
    put(1, 2, chi[1], chi[2], -1)    # (1,2,1,0)
    put(2, 3, chi[2], chi[3], 1)     # (2,3,0,1)
    put(0, 3, chi[0], chi[3], 1)     # (0,3,0,1)
    # --- fibre chi*: the far pair
    put(4, 5, chi[4], chi[5], 1)     # (4,5,2,2)

    # --- constant fibres, each a single perfect matching on fresh cells
    for c in range(D):
        put(0, 1, c, c, 1)
        put(2, 3, c, c, 1)
        put(4, 5, c, c, 1)
    return cells, chi


def build_redundant_witness() -> Tuple[Dict[Cell, GQ], Tuple[int, ...]]:
    """The witness plus one deletable cell (0,2,0,0).

    Under chi* it adds the chord 02 to the fibre SUPPORT while lying in no
    perfect matching, so support != allowed there; and it can be deleted
    without breaking P(S), so this configuration is NOT cell-minimal.
    Used as the negative control for `is_cell_minimal` and for the
    support/allowed distinction.
    """
    cells, chi = build_witness()
    cells[(0, 2, chi[0], chi[2])] = GQ(5)
    return cells, chi


def test_witness() -> Dict[str, object]:
    cells, chi = build_witness()
    # the fibre matrix is exactly what we prescribed (Test 1)
    w = fibre_weights(cells, chi, N)
    assert sorted(w) == [(0, 1), (0, 3), (1, 2), (2, 3), (4, 5)], sorted(w)
    assert w[(0, 1)] == GQ(1) and w[(1, 2)] == GQ(-1)
    assert not fibre_coefficient(cells, chi, N)
    assert constants_all_nonzero(cells)
    assert fibre_live(cells, chi)

    minimal, deletable = is_cell_minimal(cells, chi)
    rep = report_fibre(cells, chi)
    rep["cell_support_size"] = len(cells)
    rep["cell_minimal"] = minimal
    rep["deletable_cells"] = deletable
    return rep


# ------------------------------------------- Test 3 : the 19-type F census

# proofs/six-site-arbitrary-complex-obstruction.md eq. (7)
F_TYPES: Dict[str, List[Edge]] = {
    "6P1": [],
    "P2+4P1": [(0, 1)],
    "2P2+2P1": [(0, 1), (2, 3)],
    "P3+3P1": [(0, 1), (1, 2)],
    "3P2": [(0, 1), (2, 3), (4, 5)],
    "P3+P2+P1": [(0, 1), (1, 2), (3, 4)],
    "P4+2P1": [(0, 1), (1, 2), (2, 3)],
    "C3+3P1": [(0, 1), (1, 2), (0, 2)],
    "P5+P1": [(0, 1), (1, 2), (2, 3), (3, 4)],
    "P4+P2": [(0, 1), (1, 2), (2, 3), (4, 5)],
    "P3+P3": [(0, 1), (1, 2), (3, 4), (4, 5)],
    "C3+P2+P1": [(0, 1), (1, 2), (0, 2), (3, 4)],
    "C4+2P1": [(0, 1), (1, 2), (2, 3), (0, 3)],
    "P6": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
    "C3+P3": [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5)],
    "C4+P2": [(0, 1), (1, 2), (2, 3), (0, 3), (4, 5)],
    "C5+P1": [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)],
    "C6": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)],
    "C3+C3": [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)],
}


def random_rank_one(rng, gaussian) -> Dict[Tuple[int, int], GQ]:
    """A nonzero rank-one 3x3 block a = x y^T with exact entries."""
    while True:
        x = [rand_scalar(rng, gaussian, allow_zero=True) for _ in range(D)]
        y = [rand_scalar(rng, gaussian, allow_zero=True) for _ in range(D)]
        if any(bool(v) for v in x) and any(bool(v) for v in y):
            break
    return {(i, j): x[i] * y[j] for i in range(D) for j in range(D) if x[i] and y[j]}


def random_rank_ge_two(rng, gaussian) -> Dict[Tuple[int, int], GQ]:
    """A 3x3 block of rank >= 2 (two supported entries in distinct rows/cols)."""
    a = random_rank_one(rng, gaussian)
    b = random_rank_one(rng, gaussian)
    out: Dict[Tuple[int, int], GQ] = {}
    for k in set(a) | set(b):
        v = a.get(k, ZERO) + b.get(k, ZERO)
        if v:
            out[k] = v
    if matrix_rank(out) >= 2:
        return out
    return {(0, 0): ONE, (1, 1): ONE}


def matrix_rank(block: Dict[Tuple[int, int], GQ]) -> int:
    rows = [[block.get((i, j), ZERO) for j in range(D)] for i in range(D)]
    rank = 0
    col = 0
    for col in range(D):
        piv = None
        for r in range(rank, D):
            if rows[r][col]:
                piv = r
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        pv = rows[rank][col]
        for r in range(D):
            if r != rank and rows[r][col]:
                f = rows[r][col] / pv
                rows[r] = [rows[r][c] - f * rows[rank][c] for c in range(D)]
        rank += 1
    return rank


def rand_scalar(rng, gaussian, allow_zero=False) -> GQ:
    pool = [-2, -1, 0, 1, 2] if allow_zero else [-2, -1, 1, 2]
    re = Fraction(rng.choice(pool))
    if not gaussian:
        return GQ(re, 0)
    return GQ(re, Fraction(rng.choice([0, 0, -1, 1])))


def build_census_instance(rng, ftype: str, gaussian: bool) -> Optional[Dict[Cell, GQ]]:
    """Cells respecting the repo's rank budget for one F-type of eq. (7)."""
    fedges = set(F_TYPES[ftype])
    cells: Dict[Cell, GQ] = {}
    for (u, v) in PAIRS:
        block = random_rank_ge_two(rng, gaussian) if (u, v) in fedges else random_rank_one(rng, gaussian)
        for (i, j), val in block.items():
            cells[(u, v, i, j)] = val
    return cells


def force_fibre_zero(cells: Dict[Cell, GQ], chi) -> Optional[Dict[Cell, GQ]]:
    """Retune ONE cell of fibre chi so that H_chi = 0 exactly, keeping it nonzero."""
    w = fibre_weights(cells, chi, N)
    for e in sorted(w):
        trial = dict(w)
        trial[e] = ZERO
        base = hafnian(VERTS, trial)
        coeff = hafnian(tuple(v for v in VERTS if v not in e), trial)
        if not coeff:
            continue
        z = ZERO - (base / coeff)
        if not z:
            continue
        out = dict(cells)
        out[(e[0], e[1], chi[e[0]], chi[e[1]])] = z
        if not fibre_coefficient(out, chi, N) and fibre_live(out, chi):
            return out
    return None


def prune_to_cell_minimal(cells: Dict[Cell, GQ], chi) -> Dict[Cell, GQ]:
    """Greedily delete cells while P(S) is preserved, giving a cell-minimal S."""
    cur = dict(cells)
    changed = True
    while changed:
        changed = False
        for c in sorted(cur):
            trial = dict(cur)
            del trial[c]
            if (
                not fibre_coefficient(trial, chi, N)
                and fibre_live(trial, chi)
                and constants_all_nonzero(trial)
            ):
                cur = trial
                changed = True
    return cur


def run_census(trials_per_type: int = 12) -> Dict[str, object]:
    rng = random.Random(778899)
    stats = {
        "instances": 0,
        "cell_minimal": 0,
        "connected_on_V": 0,
        "disconnected_on_V": 0,
        "matching_covered_on_V": 0,
        "not_matching_covered_on_V": 0,
        "allowed_ne_active_on_V": 0,
        "R_proper_subset": 0,
        "connected_on_R": 0,
        "matching_covered_on_R": 0,
        "allowed_eq_active_on_R": 0,
        "failures_on_R": [],
    }
    per_type: Dict[str, Dict[str, int]] = {}
    mixed = mixed_chis()
    for ftype in F_TYPES:
        pt = {"instances": 0, "disconnected_on_V": 0, "not_mc_on_V": 0, "R_proper": 0}
        for t in range(trials_per_type):
            gaussian = bool(t % 2)
            cells = build_census_instance(rng, ftype, gaussian)
            if cells is None or not constants_all_nonzero(cells):
                continue
            chi = mixed[rng.randrange(len(mixed))]
            if not fibre_live(cells, chi):
                continue
            forced = force_fibre_zero(cells, chi)
            if forced is None or not constants_all_nonzero(forced):
                continue
            minimal_cells = prune_to_cell_minimal(forced, chi)
            ok, deletable = is_cell_minimal(minimal_cells, chi)
            if not ok:
                continue
            rep = report_fibre(minimal_cells, chi)
            stats["instances"] += 1
            pt["instances"] += 1
            stats["cell_minimal"] += 1
            if rep["connected_on_V"]:
                stats["connected_on_V"] += 1
            else:
                stats["disconnected_on_V"] += 1
                pt["disconnected_on_V"] += 1
            if rep["matching_covered_on_V"]:
                stats["matching_covered_on_V"] += 1
            else:
                stats["not_matching_covered_on_V"] += 1
                pt["not_mc_on_V"] += 1
            if not rep["allowed_eq_active_on_V"]:
                stats["allowed_ne_active_on_V"] += 1
            if rep["R"] is not None:
                if rep.get("R_proper"):
                    stats["R_proper_subset"] += 1
                    pt["R_proper"] += 1
                if rep["connected_on_R"]:
                    stats["connected_on_R"] += 1
                if rep["matching_covered_on_R"]:
                    stats["matching_covered_on_R"] += 1
                if rep["allowed_eq_active_on_R"]:
                    stats["allowed_eq_active_on_R"] += 1
                if not (
                    rep["connected_on_R"]
                    and rep["matching_covered_on_R"]
                    and rep["allowed_eq_active_on_R"]
                ):
                    stats["failures_on_R"].append(
                        {"ftype": ftype, "chi": chi, "R": rep["R"]}
                    )
        per_type[ftype] = pt
    stats["per_type"] = per_type
    return stats


def main() -> None:
    print("=" * 74)
    print("U7H TRANSFER TEST  -- our bicoloured cell model, N=6, palette 3")
    print("=" * 74)

    w = test_witness()
    print("\n[Test 1/2] explicit cell-minimal witness")
    print(f"  chi*                          {w['chi']}")
    print(f"  |S| (cells)                   {w['cell_support_size']}")
    print(f"  cell-minimal                  {w['cell_minimal']}  deletable={w['deletable_cells']}")
    print(f"  H_chi*                        {w['H_chi']}")
    print(f"  fibre support                 {w['fibre_support']}")
    print(f"  allowed on V                  {w['allowed_on_V']}")
    print(f"  allowed == active on V        {w['allowed_eq_active_on_V']}")
    print(f"  components on V               {w['components_on_V']}")
    print(f"  CONNECTED on V                {w['connected_on_V']}      <-- import target")
    print(f"  MATCHING-COVERED on V         {w['matching_covered_on_V']}      <-- import target")
    print(f"  least vertex subset R         {w['R']}   proper={w['R_proper']}")
    print(f"  allowed == active on R        {w['allowed_eq_active_on_R']}")
    print(f"  connected on R                {w['connected_on_R']}")
    print(f"  matching-covered on R         {w['matching_covered_on_R']}")

    assert w["cell_minimal"] is True
    assert w["connected_on_V"] is False
    assert w["matching_covered_on_V"] is False
    assert w["connected_on_R"] is True
    assert w["matching_covered_on_R"] is True
    assert w["allowed_eq_active_on_R"] is True

    print("\n[Test 3] 19-type rank-defect census sweep (eq. (7) of the six-site proof)")
    st = run_census()
    for k in (
        "instances",
        "cell_minimal",
        "connected_on_V",
        "disconnected_on_V",
        "matching_covered_on_V",
        "not_matching_covered_on_V",
        "allowed_ne_active_on_V",
        "R_proper_subset",
        "connected_on_R",
        "matching_covered_on_R",
        "allowed_eq_active_on_R",
    ):
        print(f"  {k:32s} {st[k]}")
    print(f"  failures_on_R                    {st['failures_on_R']}")
    print("\n  per F-type (instances / disconnected on V / not-MC on V / R proper):")
    for ft, pt in st["per_type"].items():
        print(
            f"    {ft:10s} {pt['instances']:3d}  {pt['disconnected_on_V']:3d}  "
            f"{pt['not_mc_on_V']:3d}  {pt['R_proper']:3d}"
        )

    assert not st["failures_on_R"], "external theorem FAILED after transfer"
    print("\nVERDICT")
    print("  on R (external quantifier, M-vert): 0 failures  -> theorem transfers")
    print("  on V (import target, M-cell)      : counterexamples exist -> naive import FAILS")


if __name__ == "__main__":
    main()
