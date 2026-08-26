"""Shared reconstruction library for REPAIR TASK 1 (K chain map).

HOW TO RUN: these scripts expect to sit next to a `computations/` tree that is a
`git archive` of the pinned HEAD (see PINNED_HEAD.txt) plus a PINNED_HEAD.txt
file, i.e.

    mkdir run && cd run && git archive <PINNED_HEAD> | tar -x
    cp <this dir>/*.py . && git rev-parse <PINNED_HEAD> > PINNED_HEAD.txt
    python3 step1_physical.py   # then step2 ... step9 in order
                                # (step5/6/8 need step2's operator_state.pkl)

Everything here is rebuilt from the committed constructors in the pinned
snapshot; nothing is copied as a literal from a checker's ledger.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import importlib.util
import sys
from pathlib import Path

SNAP = Path(__file__).resolve().parent
PINNED_HEAD = (SNAP / "PINNED_HEAD.txt").read_text().strip()


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, SNAP / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def modules():
    saved = sys.argv
    sys.argv = [saved[0]]
    try:
        m = {}
        m["aff"] = load(
            "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py",
            "r1_aff")
        m["order6"] = load(
            "computations/verify_h3_residual_q_order6_missing_face_probe.py",
            "r1_o6")
        m["repair"] = load(
            "computations/verify_h3_residual_q_order5_generator_repair.py",
            "r1_rp")
        m["commutator"] = load(
            "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
            "r1_cm")
        m["base"] = load(
            "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
            "r1_bs")
        return m
    finally:
        sys.argv = saved


MISSING = frozenset(((0, 7, 1, 1), (2, 4, 1, 1)))


def build_operator_columns(m, verbose=True):
    """Rebuild the 8,580-column bounded order-six operator block.

    Row keys: (0, product, monomial)          literal source rows
              (1, product, sel, monomial)     first Spencer / D1 rows
              (2, pair_of_cells)              grade-forgotten pair shadow
    """
    aff, order6, repair, commutator, base = (
        m["aff"], m["order6"], m["repair"], m["commutator"], m["base"])
    system = repair.build_system(base, commutator)
    sixth = order6.build_exact_sixth_derivatives(system)
    fifth = aff.exact_derivatives_of_order(system, 5)
    seventh = aff.exact_derivatives_of_order(system, 7)

    metadata = set()
    for _pi, directions in sixth:
        if not MISSING.issubset(directions):
            continue
        for coeff in order6.eligible_coefficients(repair, commutator, directions):
            metadata.add((coeff, directions))

    columns = []
    shifts = []
    for coeff, directions in sorted(metadata, key=repr):
        col = Counter()
        for pi in range(3):
            for rem, val in sixth.get((pi, directions), {}).items():
                col[(0, pi, tuple(sorted(rem + coeff)))] += val
        for (ccoef, cdirs), cw in aff.endpoint_composition_antisymmetric(
                (coeff, directions)).items():
            for sel, mult in Counter(cdirs).items():
                rest = list(cdirs)
                rest.remove(sel)
                rest = tuple(rest)
                tbl = {5: fifth, 6: sixth, 7: seventh}.get(len(rest))
                assert tbl is not None, "endpoint composition changed order"
                for pi in range(3):
                    for rem, val in tbl.get((pi, rest), {}).items():
                        col[(1, pi, sel, tuple(sorted(rem + ccoef)))] += (
                            cw * mult * val)
        for l, r in combinations(range(6), 2):
            col[(2, tuple(sorted((directions[l], directions[r]))))] += 1
        shifts.append(repair.degree_subtract(
            repair.colour_degree(coeff), repair.colour_degree(directions)))
        columns.append(((coeff, directions),
                        {row: val for row, val in col.items() if val}))
    order = sorted(range(len(columns)), key=lambda i: (repr(shifts[i]), i))
    columns = [columns[i] for i in order]
    shifts = [shifts[i] for i in order]
    if verbose:
        print("operator columns rebuilt:", len(columns), flush=True)
    return columns, shifts


# ---------------------------------------------------------------- physical

def physical_row(base, word):
    """The committed 90-term direct-free presentation row for a word."""
    return tuple(base.full_row(tuple(word)))


def shadow2_of_monomial(monomial):
    """Codimension-two (pair) shadow of a physical 4-cell matching monomial."""
    return [tuple(sorted(pair)) for pair in combinations(monomial, 2)]


def shadow2(chain):
    """chain: {monomial: coefficient} -> {(2, pair): coefficient}."""
    out = Counter()
    for monomial, coefficient in chain.items():
        for pair in shadow2_of_monomial(monomial):
            out[(2, pair)] += coefficient
    return Counter({k: v for k, v in out.items() if v})


# physical involutions (rebuilt from the descent checker's definitions)
ENDPOINT_SWAP = {0: 1, 1: 0}
TAIL_SITES = (2, 5)


def permute_cell(cell, swap=ENDPOINT_SWAP):
    left, right, a, b = cell
    left = swap.get(left, left)
    right = swap.get(right, right)
    if left < right:
        return (left, right, a, b)
    return (right, left, b, a)


def s_act(monomial, swap=ENDPOINT_SWAP):
    return tuple(sorted(permute_cell(cell, swap) for cell in monomial)), 1


def w_act(monomial, tail_sites=TAIL_SITES):
    """Simultaneous signed tail Weyl action on a matching monomial.

    Colour 1 -> 2 with sign -1, colour 2 -> 1, at the two tail sites.
    Returns (image_monomial, sign).
    """
    cells = list(monomial)
    sign = 1
    for site in tail_sites:
        pos = [i for i, c in enumerate(cells) if site in c[:2]]
        assert len(pos) == 1, "matching incidence changed"
        i = pos[0]
        left, right, a, b = cells[i]
        if left == site:
            if a == 1:
                a, sign = 2, -sign
            elif a == 2:
                a = 1
        else:
            if b == 1:
                b, sign = 2, -sign
            elif b == 2:
                b = 1
        cells[i] = (left, right, a, b)
    return tuple(sorted(cells)), sign


def act_on_chain(chain, action):
    out = Counter()
    for monomial, coefficient in chain.items():
        image, sign = action(monomial)
        out[image] += sign * coefficient
    return Counter({k: v for k, v in out.items() if v})


# -------------------------------------------------------- exact linear algebra

def rref_rank(vectors):
    """Exact rank over Q of an iterable of sparse dict vectors."""
    basis = {}
    for vec in vectors:
        v = {k: Q(x) for k, x in vec.items() if x}
        while v:
            p = min(v, key=repr)
            if p not in basis:
                inv = Q(1) / v[p]
                basis[p] = {k: x * inv for k, x in v.items()}
                break
            c = v[p]
            for k, x in basis[p].items():
                r = v.get(k, Q(0)) - c * x
                if r:
                    v[k] = r
                else:
                    v.pop(k, None)
    return len(basis), basis


def solve_exact(columns, target):
    """Solve sum_j x_j col_j = target exactly over Q.

    columns: list of dict vectors.  Returns
    (feasible, particular_solution_dict, kernel_basis(list of dicts),
     rank, separator or None).
    The separator, when infeasible, is a functional on rows killing every
    column but not the target (left-null certificate).
    """
    rows = sorted({r for c in columns for r in c} | set(target), key=repr)
    n = len(columns)
    # augmented tableau: row -> {col: value}, plus rhs column n, plus
    # provenance columns n+1.. tracking the row combination used.
    tab = []
    for i, r in enumerate(rows):
        vec = {}
        for j, c in enumerate(columns):
            if c.get(r):
                vec[j] = Q(c[r])
        rhs = Q(target.get(r, 0))
        prov = {i: Q(1)}
        tab.append([vec, rhs, prov])
    pivots = {}
    for i in range(len(tab)):
        vec, rhs, prov = tab[i]
        while True:
            common = set(vec) & set(pivots)
            if not common:
                break
            p = min(common)
            pv, prhs, pprov = tab[pivots[p]]
            c = vec[p]
            for k, x in pv.items():
                r2 = vec.get(k, Q(0)) - c * x
                if r2:
                    vec[k] = r2
                else:
                    vec.pop(k, None)
            rhs -= c * prhs
            for k, x in pprov.items():
                r2 = prov.get(k, Q(0)) - c * x
                if r2:
                    prov[k] = r2
                else:
                    prov.pop(k, None)
        if vec:
            p = min(vec)
            inv = Q(1) / vec[p]
            vec = {k: x * inv for k, x in vec.items()}
            rhs *= inv
            prov = {k: x * inv for k, x in prov.items()}
            tab[i] = [vec, rhs, prov]
            pivots[p] = i
        else:
            tab[i] = [vec, rhs, prov]
            if rhs:
                separator = {rows[k]: x for k, x in prov.items()}
                return False, None, None, len(pivots), separator
    # back substitution for a particular solution
    sol = {}
    for p in sorted(pivots, reverse=True):
        vec, rhs, _ = tab[pivots[p]]
        val = rhs - sum(x * sol.get(k, Q(0)) for k, x in vec.items() if k != p)
        if val:
            sol[p] = val
    free = [j for j in range(n) if j not in pivots]
    kernel = []
    for f in free:
        vec_k = {f: Q(1)}
        for p in sorted(pivots, reverse=True):
            vec, _rhs, _ = tab[pivots[p]]
            val = -sum(x * vec_k.get(k, Q(0)) for k, x in vec.items() if k != p)
            if val:
                vec_k[p] = val
        kernel.append(vec_k)
    # verify
    check = Counter()
    for j, x in sol.items():
        for r, v in columns[j].items():
            check[r] += x * v
    check = {r: v for r, v in check.items() if v}
    assert check == {r: Q(v) for r, v in target.items() if v}, \
        "particular solution reconstruction failed"
    for kv in kernel:
        chk = Counter()
        for j, x in kv.items():
            for r, v in columns[j].items():
                chk[r] += x * v
        assert not {r: v for r, v in chk.items() if v}, "kernel vector is not null"
    return True, sol, kernel, len(pivots), None
