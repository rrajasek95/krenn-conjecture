#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- the cut-contradiction kill engine + reason sets.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

THE LEMMA THIS IMPLEMENTS  (own statement; the mechanism is W12's cut
extraction, Theorem W12-B, specialised to its purely combinatorial corner).

    LEMMA W18-A (cut contradiction).
    Let B = L u R with |L| and |R| both even.  For a word w on B write
    ACT(w) for the set of crossing edges pq (p in L, q in R) whose cell
    (w_p, w_q) is occupied.  Call w CLEAN if ACT(w) contains no two
    vertex-disjoint edges.  If w is clean then every T-supported perfect
    matching of B uses ZERO crossing edges (a supported matching uses an even
    number k of crossing edges, and k crossing edges of a matching are
    pairwise disjoint), so

            F_w = F^L_{w|L} . F^R_{w|R}.

    Call a sub-word u on L PINNED if
      (P1) exactly one perfect matching of L is supported at u -- then
           F^L_u is a single squarefree monomial in occupied cells, so it is
           nonzero at any exact source; or
      (P2) u = c^L for a colour c whose constant word c^B is clean -- then
           F^L_c . F^R_c = F_{c^B} != 0 at an exact source, so F^L_c != 0.
    Same definition on R.

    If there are a pinned u on L and a pinned y on R such that the word
    w = (u, y) is MIXED and CLEAN, then the template carries no exact source:
    0 = F_w = F^L_u . F^R_y with both factors nonzero.  QED.

The certificate produced here is exactly the data of that proof, plus a
REASON SET: a partial assignment of cell literals (cell occupied / cell empty)
that already forces the contradiction.  `verify_certificate` re-checks the
whole proof from the certificate alone, and `check_reason_sufficient` re-checks
that the reason set alone suffices (it re-runs the kill test on the "worst
case" completion of the partial assignment).

LEMMA W18-B (deep cut extraction) is the fallback: for pinned u on L, every y
with (u,y) mixed and clean gives F^R_y = 0, a value system on the R-cells
alone; if that system (plus "every R-cell nonzero" plus "F^R_y != 0 for pinned
y") is infeasible, the template is dead.  Decided by Groebner over Q with a
`lift` certificate (an exact polynomial identity 1 = sum h_i g_i).
"""

from __future__ import annotations

from itertools import combinations, product

import w18_core as C


# ------------------------------------------------------------------ cuts

def even_cuts(size=C.N):
    """Unordered even bipartitions {L, R} with 2 <= |L| <= |R|."""
    out = []
    seen = set()
    for k in range(2, size // 2 + 1, 2):
        for L in combinations(range(size), k):
            Ls = frozenset(L)
            Rs = frozenset(range(size)) - Ls
            key = frozenset((Ls, Rs))
            if key in seen:
                continue
            seen.add(key)
            out.append((tuple(sorted(Ls)), tuple(sorted(Rs))))
    return out


CUTS = even_cuts()


def crossing_edges(L, R):
    return [C.EIDX[(min(p, q), max(p, q))] for p in L for q in R]


def cell_of(e, w):
    u, v = C.EDGES[e]
    return (w[u], w[v])


def active_crossing(T, w, cross):
    out = []
    for e in cross:
        i, j = cell_of(e, w)
        if (T[e] >> (3 * i + j)) & 1:
            out.append(e)
    return out


def pairwise_intersecting(edge_ids):
    for a, b in combinations(edge_ids, 2):
        if not (set(C.EDGES[a]) & set(C.EDGES[b])):
            return False
    return True


def crossing_pms(L, R):
    """Indices of the perfect matchings of B that use at least one crossing
    edge of the bipartition (L, R)."""
    key = (tuple(sorted(L)), tuple(sorted(R)))
    if key not in _CPM_CACHE:
        cs = set(crossing_edges(L, R))
        _CPM_CACHE[key] = [n for n, M in enumerate(C.PM_EIDX) if cs & set(M)]
    return _CPM_CACHE[key]


_CPM_CACHE = {}


def is_split(T, w, L, R):
    """No T-supported perfect matching of B at w uses a crossing edge.

    This is the exact hypothesis of Lemma W18-A: it is equivalent to
    F_w = F^L_{w|L} . F^R_{w|R}.  The 'clean' star condition on the active
    crossing edges is the special case that has a small reason set.
    """
    for n in crossing_pms(L, R):
        for e in C.PM_EIDX[n]:
            u, v = C.EDGES[e]
            if not (T[e] >> (3 * w[u] + w[v])) & 1:
                break
        else:
            return False
    return True


def split_reason(T, w, L, R):
    """'off' literals forcing splitness of w, chosen by a greedy set cover."""
    need = []
    for n in crossing_pms(L, R):
        opts = []
        for e in C.PM_EIDX[n]:
            u, v = C.EDGES[e]
            i, j = w[u], w[v]
            if not (T[e] >> (3 * i + j)) & 1:
                opts.append(("off", e, i, j))
        if not opts:
            raise AssertionError("word is not split: no reason exists")
        need.append(set(opts))
    chosen = []
    left = list(need)
    while left:
        tally = {}
        for s in left:
            for lit in s:
                tally[lit] = tally.get(lit, 0) + 1
        best = max(tally, key=lambda k: (tally[k], k))
        chosen.append(best)
        left = [s for s in left if best not in s]
    return [list(x) for x in _minimal_cover(need, chosen)]


def clean_reason(T, w, cross):
    """(is_clean, reason) -- reason = list of ('off', e, i, j) literals that
    already force cleanness of w for this cut.

    Cleanness of w for a bipartition means ACT(w) has no two disjoint edges.
    Crossing edges of a bipartition form a complete bipartite graph, which is
    triangle-free, so a pairwise-intersecting set of them is a STAR: all its
    edges share one endpoint (or the set has < 2 edges).  The reason therefore
    switches OFF every crossing cell not incident to the chosen centre.
    """
    act = active_crossing(T, w, cross)
    if len(act) > 1:
        common = set(C.EDGES[act[0]])
        for e in act[1:]:
            common &= set(C.EDGES[e])
        if not common:
            return False, None
        centre = min(common)
    elif len(act) == 1:
        centre = C.EDGES[act[0]][0]
    else:
        centre = C.EDGES[cross[0]][0] if cross else 0
    reason = []
    for e in cross:
        if centre in C.EDGES[e]:
            continue
        i, j = cell_of(e, w)
        reason.append(("off", e, i, j))
    return True, reason


# ------------------------------------------------------------ half sides

def side_pms(sites):
    return C._pms(tuple(sorted(sites)))


_PM_CACHE = {}


def pms_of(sites):
    key = tuple(sorted(sites))
    if key not in _PM_CACHE:
        _PM_CACHE[key] = side_pms(key)
    return _PM_CACHE[key]


def supported_pms(T, sites, sub):
    """Indices (into pms_of(sites)) of PMs of `sites` supported at sub."""
    colour = dict(zip(sorted(sites), sub))
    out = []
    for n, pm in enumerate(pms_of(sites)):
        for (u, v) in pm:
            e = C.EIDX[(u, v)]
            if not (T[e] >> (3 * colour[u] + colour[v])) & 1:
                break
        else:
            out.append(n)
    return out


def half_monomials(T, sites, sub):
    """Monomials of F^side_sub: each a sorted tuple of (e, i, j) cells."""
    colour = dict(zip(sorted(sites), sub))
    out = []
    for pm in pms_of(sites):
        mono = []
        ok = True
        for (u, v) in pm:
            e = C.EIDX[(u, v)]
            i, j = colour[u], colour[v]
            if not (T[e] >> (3 * i + j)) & 1:
                ok = False
                break
            mono.append((e, i, j))
        if ok:
            out.append(tuple(sorted(mono)))
    return sorted(out)


def p1_reason(T, sites, sub):
    """Reason forcing 'exactly one PM of `sites` is supported at sub'."""
    colour = dict(zip(sorted(sites), sub))
    pms = pms_of(sites)
    sup = supported_pms(T, sites, sub)
    if len(sup) != 1:
        return None
    star = sup[0]
    reason = []
    for (u, v) in pms[star]:
        e = C.EIDX[(u, v)]
        reason.append(("on", e, colour[u], colour[v]))
    for n, pm in enumerate(pms):
        if n == star:
            continue
        for (u, v) in pm:
            e = C.EIDX[(u, v)]
            i, j = colour[u], colour[v]
            if not (T[e] >> (3 * i + j)) & 1:
                reason.append(("off", e, i, j))
                break
    return reason


def pinned_subwords(T, sites, cross):
    """{sub: ('P1'|'P2', reason)} for the pinned sub-words on `sites`."""
    out = {}
    sites = tuple(sorted(sites))
    for sub in product(range(C.Q), repeat=len(sites)):
        r = p1_reason(T, sites, sub)
        if r is not None:
            out[sub] = ("P1", r)
    for c in range(C.Q):
        sub = (c,) * len(sites)
        if sub in out:
            continue
        w = (c,) * C.N
        ok, reason = clean_reason(T, w, cross)
        if ok:
            out[sub] = ("P2", reason)
    return out


def join(L, R, u, y):
    w = [0] * C.N
    for k, p in enumerate(sorted(L)):
        w[p] = u[k]
    for k, q in enumerate(sorted(R)):
        w[q] = y[k]
    return tuple(w)


# ------------------------------------------------- LEMMA W18-A: the kill

def find_kill_A(T, cuts=None, want_all=False):
    """Search Lemma W18-A over all even cuts.  Returns a certificate or None."""
    found = []
    for (L, R) in (cuts or CUTS):
        cross = [e for e in crossing_edges(L, R) if T[e]]
        allcross = crossing_edges(L, R)
        pinL = pinned_subwords(T, L, allcross)
        if not pinL:
            continue
        pinR = pinned_subwords(T, R, allcross)
        if not pinR:
            continue
        for u, (kindL, reasonL) in pinL.items():
            for y, (kindR, reasonR) in pinR.items():
                w = join(L, R, u, y)
                if len(set(w)) == 1:
                    continue
                ok, reasonC = clean_reason(T, w, allcross)
                if not ok:
                    continue
                cert = {
                    "lemma": "W18-A",
                    "cut_L": list(L), "cut_R": list(R),
                    "word": list(w),
                    "u": list(u), "y": list(y),
                    "pinL": kindL, "pinR": kindR,
                    "reason": _dedupe(reasonL + reasonR + reasonC),
                }
                if not want_all:
                    return cert
                found.append(cert)
    return found if want_all else None


def _dedupe(reason):
    seen = []
    got = set()
    for lit in reason:
        key = tuple(lit)
        if key in got:
            continue
        got.add(key)
        seen.append(list(lit))
    return seen


# --------------------------------------------------- certificate checks

def verify_certificate(T, cert):
    """Re-prove the kill from the certificate alone.  Returns (ok, notes)."""
    notes = []
    L = tuple(cert["cut_L"])
    R = tuple(cert["cut_R"])
    if sorted(L + R) != list(range(C.N)):
        return False, ["cut is not a bipartition of the 8 sites"]
    if len(L) % 2 or len(R) % 2:
        return False, ["cut sides are not both even"]
    allcross = crossing_edges(L, R)
    w = tuple(cert["word"])
    if len(set(w)) == 1:
        return False, ["the contradiction word is constant, not mixed"]
    u = tuple(cert["u"])
    y = tuple(cert["y"])
    if join(L, R, u, y) != w:
        return False, ["u|y does not equal the recorded word"]
    if not is_split(T, w, L, R):
        return False, ["the contradiction word is not split for this cut"]
    notes.append(f"word {''.join(map(str,w))} is split: no supported matching "
                 f"uses a crossing edge, so F_w = F^L_u . F^R_y")
    for tag, side, sub, kind in (("L", L, u, cert["pinL"]),
                                 ("R", R, y, cert["pinR"])):
        if kind == "P1":
            sup = supported_pms(T, side, sub)
            if len(sup) != 1:
                return False, [f"{tag}: P1 claimed but {len(sup)} supported PMs"]
            notes.append(f"{tag}: F^{tag}_{''.join(map(str,sub))} is one "
                         f"monomial (unique supported matching)")
        elif kind == "P2":
            c = sub[0]
            if any(x != c for x in sub):
                return False, [f"{tag}: P2 claimed on a non-constant sub-word"]
            cw = (c,) * C.N
            if not is_split(T, cw, L, R):
                return False, [f"{tag}: P2 needs the constant word {c}^B split"]
            if not C.fibre(T, cw):
                return False, [f"{tag}: P2 needs a nonempty constant fibre"]
            notes.append(f"{tag}: F^{tag}_{c} != 0 because the constant word "
                         f"{c}^B is split for this cut and F_{{{c}^B}} != 0")
        else:
            return False, [f"{tag}: unknown pinning kind {kind}"]
    notes.append("=> 0 = F_w = F^L_u . F^R_y with both factors nonzero")
    return True, notes


def _minimal_cover(need, chosen):
    """Drop redundant literals from a greedy set cover (exact, cheap)."""
    cover = {lit: {k for k, sset in enumerate(need) if lit in sset}
             for lit in chosen}
    keep = list(chosen)
    for lit in list(chosen):
        rest = [x for x in keep if x != lit]
        got = set()
        for x in rest:
            got |= cover[x]
        if len(got) == len(need):
            keep = rest
    return keep


def _state_map(reason, off_edges):
    """(e,i,j) -> 'on'/'off' from the reason plus the always-empty edges."""
    lits = {}
    for e in off_edges:
        for i in range(C.Q):
            for j in range(C.Q):
                lits[(e, i, j)] = "off"
    for lit in reason:
        kind, e, i, j = lit[0], lit[1], lit[2], lit[3]
        lits[(e, i, j)] = kind
    return lits


def check_reason_sufficient(T, cert, off_edges=()):
    """Does the recorded reason set (plus the always-empty edges) force it?

    The check is purely logical: it re-runs the three ingredients of the
    Lemma W18-A proof (cleanness of the contradiction word, pinning of u,
    pinning of y) treating every cell NOT constrained by the reason as
    possibly-occupied, which is the worst case for all three.
    """
    for lit in cert["reason"]:
        kind, e, i, j = lit[0], lit[1], lit[2], lit[3]
        val = (T[e] >> (3 * i + j)) & 1
        if kind == "on" and not val:
            return False, "reason literal 'on' false in T"
        if kind == "off" and val:
            return False, "reason literal 'off' false in T"
    lits = _state_map(cert["reason"], off_edges)
    L, R = tuple(cert["cut_L"]), tuple(cert["cut_R"])
    allcross = crossing_edges(L, R)
    w = tuple(cert["word"])
    if len(set(w)) == 1:
        return False, "contradiction word is constant"
    if not _split_forced(lits, w, L, R):
        return False, "splitness of the contradiction word not forced"
    for tag, side, sub, kind in (("L", L, tuple(cert["u"]), cert["pinL"]),
                                 ("R", R, tuple(cert["y"]), cert["pinR"])):
        if kind == "P1":
            if not _p1_forced(lits, side, sub):
                return False, f"{tag}: P1 not forced by the reason"
        elif kind == "P2":
            c = sub[0]
            if any(v != c for v in sub):
                return False, f"{tag}: P2 on a non-constant sub-word"
            if not _split_forced(lits, (c,) * C.N, L, R):
                return False, f"{tag}: P2 splitness not forced by the reason"
        else:
            return False, f"{tag}: unknown pinning kind"
    return True, "reason set sufficient"


def _split_forced(lits, w, L, R):
    """Splitness follows if every crossing matching has a cell forced off."""
    for n in crossing_pms(L, R):
        for e in C.PM_EIDX[n]:
            u, v = C.EDGES[e]
            if lits.get((e, w[u], w[v])) == "off":
                break
        else:
            return False
    return True


def _clean_forced(lits, w, cross):
    """Cleanness follows if the crossing cells NOT forced off form a star."""
    maybe = []
    for e in cross:
        i, j = cell_of(e, w)
        if lits.get((e, i, j)) != "off":
            maybe.append(e)
    return pairwise_intersecting(maybe)


def _p1_forced(lits, sites, sub):
    """'exactly one supported PM' follows from the reason literals."""
    colour = dict(zip(sorted(sites), sub))
    pms = pms_of(sites)
    on_pms, maybe = [], []
    for n, pm in enumerate(pms):
        states = []
        for (u, v) in pm:
            e = C.EIDX[(u, v)]
            states.append(lits.get((e, colour[u], colour[v])))
        if all(s == "on" for s in states):
            on_pms.append(n)
        elif any(s == "off" for s in states):
            pass
        else:
            maybe.append(n)
    return len(on_pms) == 1 and not maybe


def minimise_reason(T, cert, off_edges=()):
    """Greedily drop reason literals that are not needed for sufficiency.

    The result is re-checked, so a bug here can only make the nogood WEAKER
    (never unsound): `check_reason_sufficient` is the gate.
    """
    reason = [list(l) for l in cert["reason"]]
    # drop literals on the always-empty edges first (they are tautologies)
    offset = set(off_edges)
    reason = [l for l in reason if l[1] not in offset]
    k = 0
    while k < len(reason):
        trial = dict(cert)
        trial["reason"] = reason[:k] + reason[k + 1:]
        ok, _ = check_reason_sufficient(T, trial, off_edges)
        if ok:
            reason = trial["reason"]
        else:
            k += 1
    out = dict(cert)
    out["reason"] = reason
    return out


# ------------------------------------------- LEMMA W18-O2 (the singleton)

def singleton_reason(T, w):
    """Reason set for 'the mixed word w has a fibre of size one' (O2).

    F_w is then a single squarefree monomial in occupied cells, so it cannot
    vanish -- but exactness forces F_w = 0 for a mixed word.  The reason is the
    four occupied cells of the supporting matching plus, for every other
    perfect matching of K_8, one cell that is empty (greedy set cover).
    """
    fib = C.fibre(T, w)
    if len(fib) != 1 or len(set(w)) == 1:
        return None
    star = fib[0]
    reason = []
    for e in C.PM_EIDX[star]:
        u, v = C.EDGES[e]
        reason.append(("on", e, w[u], w[v]))
    need = []
    for n in range(len(C.PMS)):
        if n == star:
            continue
        opts = set()
        for e in C.PM_EIDX[n]:
            u, v = C.EDGES[e]
            i, j = w[u], w[v]
            if not (T[e] >> (3 * i + j)) & 1:
                opts.add(("off", e, i, j))
        if not opts:
            raise AssertionError("fibre is not a singleton")
        need.append(opts)
    chosen = []
    left = list(need)
    while left:
        tally = {}
        for s in left:
            for lit in s:
                tally[lit] = tally.get(lit, 0) + 1
        best = max(tally, key=lambda k: (tally[k], k))
        chosen.append(best)
        left = [s for s in left if best not in s]
    reason += _minimal_cover(need, chosen)
    return {"lemma": "W18-O2", "word": list(w),
            "reason": _dedupe([list(x) for x in reason])}


def verify_singleton(T, cert):
    w = tuple(cert["word"])
    if len(set(w)) == 1:
        return False, ["the word is constant"]
    fib = C.fibre(T, w)
    if len(fib) != 1:
        return False, [f"fibre size is {len(fib)}, not 1"]
    return True, [f"mixed word {''.join(map(str,w))} has a one-element fibre: "
                  f"F_w is a nonzero monomial but exactness needs F_w = 0"]


def singleton_reason_sufficient(T, cert, off_edges=()):
    for lit in cert["reason"]:
        kind, e, i, j = lit[0], lit[1], lit[2], lit[3]
        val = (T[e] >> (3 * i + j)) & 1
        if (kind == "on") != bool(val):
            return False, "reason literal false in T"
    lits = _state_map(cert["reason"], off_edges)
    w = tuple(cert["word"])
    if len(set(w)) == 1:
        return False, "constant word"
    on_pms, maybe = [], []
    for n in range(len(C.PMS)):
        states = []
        for e in C.PM_EIDX[n]:
            u, v = C.EDGES[e]
            states.append(lits.get((e, w[u], w[v])))
        if all(s == "on" for s in states):
            on_pms.append(n)
        elif any(s == "off" for s in states):
            pass
        else:
            maybe.append(n)
    if len(on_pms) != 1 or maybe:
        return False, "reason does not force a one-element fibre"
    return True, "singleton reason sufficient"


def minimise_singleton_reason(T, cert, off_edges=()):
    reason = [list(l) for l in cert["reason"] if l[1] not in set(off_edges)]
    k = 0
    while k < len(reason):
        trial = dict(cert)
        trial["reason"] = reason[:k] + reason[k + 1:]
        ok, _ = singleton_reason_sufficient(T, trial, off_edges)
        if ok:
            reason = trial["reason"]
        else:
            k += 1
    out = dict(cert)
    out["reason"] = reason
    return out
