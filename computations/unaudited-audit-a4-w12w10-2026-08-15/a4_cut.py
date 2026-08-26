#!/usr/bin/env python3
"""AUDIT A4 -- INDEPENDENT implementation of the cut extraction (W12-B).

Written from the STATEMENT of Theorem W12-B, not from w12_cut.py.  Two
deliberate differences from the probe's code:

  * cleanness is decided by the EXACT criterion (no supported perfect
    matching of the whole word uses a crossing edge), computed from the
    fibre engine, and the star criterion is computed alongside so the two
    can be compared;
  * every use of the factorisation F_w = F^L . F^R is VERIFIED monomially
    at the point of use, not assumed;
  * the extracted half-system is decided by a DIRECT Groebner/Rabinowitsch
    test on the half's own cell variables -- no lattice, no Smith form, no
    torus reduction (i.e. an entirely different decision route).
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from itertools import combinations, product

import a4_engine as E

Q = 3


class SingularError(RuntimeError):
    pass


def singular(script, timeout=600):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        p = subprocess.run(["Singular", "-q", "--no-warn", path],
                           capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    if p.returncode != 0 or "?" in p.stdout or "?" in p.stderr:
        raise SingularError((p.stdout + p.stderr)[:2000])
    return p.stdout


def even_cuts(n):
    seen, out = set(), []
    for k in range(2, n - 1, 2):
        for L in combinations(range(n), k):
            Ls = frozenset(L)
            Rs = frozenset(range(n)) - Ls
            key = frozenset((Ls, Rs))
            if key not in seen:
                seen.add(key)
                out.append((Ls, Rs))
    return out


def active_crossing(T, word, L):
    return [(u, v) for k, (u, v) in enumerate(T.edges)
            if ((u in L) != (v in L)) and (k, word[u], word[v]) in T.occ]


def star_like(edges):
    return all(len({a, b, c, d}) < 4
               for (a, b), (c, d) in combinations(edges, 2))


class Cut:
    """One even bipartition of the sites, with the extraction it induces."""

    def __init__(self, T, L, R):
        self.T = T
        self.L = frozenset(L)
        self.R = frozenset(R)
        self.n = T.n
        self._clean_cache = {}

    # ------- cleanness (EXACT criterion) + monomially verified factorisation
    def clean_exact(self, word):
        if word in self._clean_cache:
            return self._clean_cache[word]
        crossing_used = any((u in self.L) != (v in self.L)
                            for M in self.T.fibre_matchings(word)
                            for (u, v) in M)
        self._clean_cache[word] = not crossing_used
        return not crossing_used

    def clean_star(self, word):
        return star_like(active_crossing(self.T, word, self.L))

    def verify_factorisation(self, word):
        """F_w == F^L . F^R monomially (must hold whenever clean_exact)."""
        F = self.T.fibre_poly(word)
        FL = self.T.fibre_poly(word, sites=sorted(self.L))
        FR = self.T.fibre_poly(word, sites=sorted(self.R))
        prod = E.poly_mul(FL, FR) if (FL and FR) else {}
        return F == prod, len(F), len(FL), len(FR)

    # --------------------------------------------------------- pinning
    def pinned(self, side, other):
        """Sub-words on `side` whose half-fibre sum is FORCED nonzero.

        (P1) exactly one supported perfect matching -> a single monomial in
             nonzero cells;
        (P2) c^side where the constant word c^B is clean -> the exactness
             requirement F_{c^B} != 0 factors as F^L_c . F^R_c.
        Returns {subword: 'P1'|'P2'} with the justification recorded.
        """
        side = tuple(sorted(side))
        out = {}
        for sub in product(range(Q), repeat=len(side)):
            w = self._embed(sub, side, 0)   # colours off `side` are irrelevant
            p = self.T.fibre_poly(w, sites=side)
            if len(p) == 1:
                out[sub] = "P1"
        for c in range(Q):
            cw = (c,) * self.n
            if not self.clean_exact(cw):
                continue
            if not self.T.fibre_poly(cw):
                continue       # empty constant fibre: template is dead anyway
            ok, _, nl, nr = self.verify_factorisation(cw)
            assert ok, "clean word failed to factor"
            assert nl and nr
            out.setdefault((c,) * len(side), "P2")
        return out

    def _embed(self, sub, sites, fill):
        w = [fill] * self.n
        for k, v in enumerate(sorted(sites)):
            w[v] = sub[k]
        return tuple(w)

    def _embed2(self, u, usites, y, ysites):
        w = [0] * self.n
        for k, v in enumerate(sorted(usites)):
            w[v] = u[k]
        for k, v in enumerate(sorted(ysites)):
            w[v] = y[k]
        return tuple(w)

    # ------------------------------------------------------ extraction
    def extract(self, tag):
        """tag='R': equations on the R-cells forced by pinned L sub-words."""
        side = tuple(sorted(self.R if tag == "R" else self.L))
        other = tuple(sorted(self.L if tag == "R" else self.R))
        pin_other = self.pinned(other, side)
        pin_side = self.pinned(side, other)
        zeros = {}
        for u, why in pin_other.items():
            for y in product(range(Q), repeat=len(side)):
                w = self._embed2(u, other, y, side)
                if not E.is_mixed(w):
                    continue
                if not self.clean_exact(w):
                    continue
                ok, _, _, _ = self.verify_factorisation(w)
                assert ok, "clean word failed to factor"
                zeros.setdefault(y, (u, why))
        return {"side": side, "other": other, "pinned_other": pin_other,
                "pinned_side": pin_side, "zeros": zeros}


def half_polys(T, sites, sub):
    return T.fibre_poly(_sub_word(T, sites, sub), sites=tuple(sorted(sites)))


def _sub_word(T, sites, sub):
    w = [0] * T.n
    for k, v in enumerate(sorted(sites)):
        w[v] = sub[k]
    return tuple(w)


def decide(T, ex, timeout=300):
    """Decide the extracted half-system.  Returns (verdict, reason, detail)."""
    side = ex["side"]
    zeros = ex["zeros"]
    pin_side = ex["pinned_side"]
    if not zeros:
        return "no-content", "", {}
    clash = sorted(set(zeros) & set(pin_side))
    if clash:
        y = clash[0]
        return ("killed", "a pinned sub-word is forced to vanish",
                {"word": "".join(map(str, y)),
                 "pin_reason": pin_side[y],
                 "forced_by": "".join(map(str, zeros[y][0])),
                 "forced_by_reason": zeros[y][1]})
    # build the half-system polynomials
    eqs, names, varmap = [], {}, {}

    def poly_str(p):
        parts = []
        for mono in p:
            body = "*".join(sorted(varmap[v] for v in mono))
            parts.append(body)
        return "+".join(parts) if parts else "0"

    zpolys = {}
    for y in sorted(zeros):
        p = half_polys(T, side, y)
        if not p:
            continue                      # 0 = 0, no content
        if len(p) == 1:
            return ("killed", "single-monomial equation forced to vanish",
                    {"word": "".join(map(str, y))})
        zpolys[y] = p
    cpolys = {}
    for y in sorted(pin_side):
        p = half_polys(T, side, y)
        if len(p) > 1:                    # single monomials are free
            cpolys[y] = p
    if not zpolys:
        return "no-content", "", {}
    allvars = sorted({v for p in list(zpolys.values()) + list(cpolys.values())
                      for m in p for v in m})
    for k, v in enumerate(allvars):
        varmap[v] = f"v{k}"
    names = [varmap[v] for v in allvars]
    gens = [poly_str(p) for p in zpolys.values()]
    nz = list(names) + [f"({poly_str(p)})" for p in cpolys.values()]
    script = "\n".join([
        f'ring RA=0,({",".join(names)},t),dp;',
        "ideal I=" + ",".join(gens) + ";",
        f"ideal J=I,t*{'*'.join(nz)}-1;",
        "ideal G=std(J);",
        '"UNIT "+string(reduce(1,G)==0);'])
    try:
        res = singular(script, timeout=timeout)
    except Exception as exc:                                   # noqa: BLE001
        return "undecided", f"singular:{type(exc).__name__}", {}
    if "UNIT 1" in res:
        return ("killed", "half-system infeasible (direct Groebner)",
                {"nvars": len(names), "neqs": len(gens),
                 "nnonvanish": len(cpolys)})
    return ("feasible", "", {"nvars": len(names), "neqs": len(gens)})


def cut_kill(T, timeout=120, want_all=False, cheap_only=False):
    """Search all even cuts for a kill.  Returns (verdict, records)."""
    records = []
    halves = []
    for (L, R) in even_cuts(T.n):
        cut = Cut(T, L, R)
        for tag in ("R", "L"):
            ex = cut.extract(tag)
            if not ex["zeros"]:
                continue
            halves.append((cut, tag, ex))
    # cheap pass first
    for cut, tag, ex in halves:
        clash = sorted(set(ex["zeros"]) & set(ex["pinned_side"]))
        singles = [y for y in ex["zeros"]
                   if len(half_polys(T, ex["side"], y)) == 1]
        if clash or singles:
            v, why, det = decide(T, ex, timeout=0)
            rec = {"L": sorted(cut.L), "side": tag, "verdict": v,
                   "reason": why, "detail": det}
            records.append(rec)
            if v == "killed" and not want_all:
                return "killed", records
    if cheap_only:
        return (("killed" if any(r["verdict"] == "killed" for r in records)
                 else "no-kill"), records)
    order = sorted(range(len(halves)), key=lambda k: len(halves[k][2]["side"]))
    for k in order:
        cut, tag, ex = halves[k]
        v, why, det = decide(T, ex, timeout=timeout)
        rec = {"L": sorted(cut.L), "side": tag, "verdict": v,
               "reason": why, "detail": det}
        records.append(rec)
        if v == "killed" and not want_all:
            return "killed", records
    return (("killed" if any(r["verdict"] == "killed" for r in records)
             else "no-kill"), records)
