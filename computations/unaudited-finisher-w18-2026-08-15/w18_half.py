#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- LEMMA W18-D: the cut-local monomial-ratio kill.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

    Fix an even bipartition B = L u R, write SIDE for one of the two halves
    and OTHER for the other.  A sub-word u on OTHER is PINNED when
      (P1) exactly one perfect matching of OTHER is supported at u, or
      (P2) u = c^OTHER and the constant word c^B is SPLIT for the cut (no
           supported perfect matching of B at c^B uses a crossing edge) and
           has a nonempty fibre.
    In both cases F^OTHER_u != 0 at any exact source.  Then for every sub-word
    y on SIDE with (u, y) mixed and split,

        0 = F_{(u,y)} = F^OTHER_u . F^SIDE_y      =>      F^SIDE_y = 0,

    and for every PINNED y on SIDE, F^SIDE_y != 0.  That is a monomial system
    in the occupied cells of the SIDE-internal edges alone -- all nonzero --
    and Lemma W18-C's ratio engine (module w18_ratio) decides it.  On a
    four-site side the fibres have at most three terms however thick the
    whole-B fibres are, which is why this layer bites where the whole-B
    lattice has no binomial relations to work with.

The certificate is (i) the cut and side, (ii) for every equation used, the
justification that makes it an equation (a pinned u and a split word, or the
pinning of y itself), and (iii) the ratio-engine certificate.  `verify_D`
re-checks all three from the template with the slow reference code.
"""

from __future__ import annotations

import numpy as np

import w18_core as C
import w18_fast as F
import w18_kill as K
import w18_ratio as RA


def side_varindex(sites):
    """POSITIONAL index of every cell of every side-internal edge.

    Deliberately independent of the template: the exponent vectors of a
    certificate then mean the same thing for every completion of a partial
    assignment, which is what lets a Lemma W18-D kill carry a REASON SET.
    Unoccupied cells simply never appear in a monomial.
    """
    idx = {}
    sites = tuple(sorted(sites))
    for a in sites:
        for b in sites:
            if a >= b:
                continue
            e = C.EIDX[(a, b)]
            for i in range(3):
                for j in range(3):
                    idx[(e, i, j)] = len(idx)
    return idx


def side_monomials(T, sites, idx, sub):
    colour = dict(zip(sorted(sites), sub))
    out = []
    for pm in K.pms_of(sites):
        vec = [0] * len(idx)
        ok = True
        for (u, v) in pm:
            e = C.EIDX[(u, v)]
            i, j = colour[u], colour[v]
            if not (T[e] >> (3 * i + j)) & 1:
                ok = False
                break
            vec[idx[(e, i, j)]] += 1
        if ok:
            out.append(tuple(vec))
    return sorted(out)


def _pins(cnt, side, split_colours):
    out = {}
    for i in np.nonzero(cnt == 1)[0]:
        out[int(i)] = "P1"
    for c in split_colours:
        out[side.const_index[c]] = "P2"
    return out


def build(T, cut, want_R, occ, compat):
    """(nvars, zeros, nonzeros, justification) for one side of one cut."""
    side = cut.sideR if want_R else cut.sideL
    other = cut.sideL if want_R else cut.sideR
    split = ~compat[cut.crossing_pms].any(axis=0)
    # (P2) needs only splitness of the constant word: if its fibre were empty
    # the template would already be dead (F_{c^B} = 0 contradicts exactness),
    # and if it is nonempty then F^L_c . F^R_c = F_{c^B} != 0 forces both.
    cl = [c for c in range(3) if split[F.CONST_WORD_IDX[c]]]
    cnt_other = other.pm_counts(occ)
    pin_other = _pins(cnt_other, other, cl)
    if not pin_other:
        return None
    pairs = cut.pairidx if want_R else cut.pairidx.T        # [other, side]
    rows = sorted(pin_other)
    idxmat = pairs[rows, :]
    good = split[idxmat] & F._MIXED[idxmat]
    zmask = good.any(axis=0)
    if not zmask.any():
        return None
    vidx = side_varindex(side.sites)
    cnt_side = side.pm_counts(occ)
    pin_side = _pins(cnt_side, side, cl)
    zeros, nonzeros, just = {}, {}, {}
    for jy in np.nonzero(zmask)[0]:
        jy = int(jy)
        sub = tuple(int(x) for x in side.subwords[jy])
        monos = side_monomials(T, side.sites, vidx, sub)
        if not monos:
            continue
        r = int(np.nonzero(good[:, jy])[0][0])
        iu = rows[r]
        zeros[sub] = monos
        just[sub] = {"role": "zero",
                     "u": [int(x) for x in other.subwords[iu]],
                     "pin": pin_other[iu],
                     "w": [int(x) for x in C.WORDS[int(pairs[iu, jy])]]}
    for jy in sorted(pin_side):
        sub = tuple(int(x) for x in side.subwords[jy])
        if sub in zeros:
            continue
        monos = side_monomials(T, side.sites, vidx, sub)
        if not monos:
            continue
        nonzeros[sub] = monos
        just[sub] = {"role": "nonzero", "pin": pin_side[jy]}
    if not zeros:
        return None
    return len(vidx), zeros, nonzeros, just


def kill_on_side(T, cut, want_R, occ, compat):
    built = build(T, cut, want_R, occ, compat)
    if built is None:
        return None
    n, zeros, nonzeros, just = built
    cert = RA.run(n, zeros, nonzeros)
    if cert is None:
        return None
    cert = RA.compress(cert)
    side = cut.sideR if want_R else cut.sideL
    other = cut.sideL if want_R else cut.sideR
    keys = set()
    if "key" in cert:
        keys.add(cert["key"])
    for g in cert["generators"]:
        keys.add(g["key"])
    return {"lemma": "W18-D", "cut_L": list(cut.L), "cut_R": list(cut.R),
            "side": list(side.sites), "other": list(other.sites),
            "nvars": n,
            "justification": {"".join(map(str, k)): just[k] for k in keys},
            "ratio": _keys_to_str(cert)}


def _keys_to_str(cert):
    out = dict(cert)
    if "key" in out:
        out["key"] = "".join(map(str, out["key"]))
    out["generators"] = [dict(g, key="".join(map(str, g["key"])))
                         for g in out["generators"]]
    return out


def _keys_from_str(cert):
    out = dict(cert)
    if "key" in out:
        out["key"] = tuple(int(c) for c in out["key"])
    out["generators"] = [dict(g, key=tuple(int(c) for c in g["key"]))
                         for g in out["generators"]]
    return out


def find_kill_D(T, occ=None, compat=None, side_sizes=(4,)):
    """Search Lemma W18-D.

    Only sides of the given sizes are used.  Size 4 is the productive case
    (three matchings per side, so fibres have at most three terms); size 2 is
    already covered by Lemma W18-A (a two-site fibre IS a single cell); size 6
    is allowed but very expensive (fifteen matchings, 729 sub-words) and is off
    by default.
    """
    if occ is None:
        occ = F.occupancy(T)
    if compat is None:
        compat = F.support_matrix(occ)
    for cut in F.CUTS:
        for want_R in (True, False):
            side = cut.sideR if want_R else cut.sideL
            if len(side.sites) not in side_sizes:
                continue
            cert = kill_on_side(T, cut, want_R, occ, compat)
            if cert is not None:
                return cert
    return None


# --------------------------------------------------------------- verify

def verify_D(T, cert):
    """Re-prove a Lemma W18-D kill from the template, with reference code."""
    L, R = tuple(cert["cut_L"]), tuple(cert["cut_R"])
    if sorted(L + R) != list(range(C.N)) or len(L) % 2 or len(R) % 2:
        return False, "not an even bipartition"
    sites = tuple(cert["side"])
    other = tuple(cert["other"])
    if tuple(sorted(sites + other)) != tuple(range(C.N)):
        return False, "side/other do not partition the sites"
    if set(sites) not in (set(L), set(R)):
        return False, "side is not one of the two halves"
    vidx = side_varindex(sites)
    if len(vidx) != cert["nvars"]:
        return False, "variable count mismatch"
    zeros, nonzeros = {}, {}
    for skey, j in cert["justification"].items():
        y = tuple(int(c) for c in skey)
        if len(y) != len(sites):
            return False, "justified key has the wrong length"
        monos = side_monomials(T, sites, vidx, y)
        if j["role"] == "zero":
            u = tuple(j["u"])
            w = tuple(j["w"])
            if K.join(other, sites, u, y) != w:
                return False, f"{skey}: u|y is not the recorded word"
            if len(set(w)) == 1:
                return False, f"{skey}: the recorded word is constant"
            if not K.is_split(T, w, L, R):
                return False, f"{skey}: the recorded word is not split"
            if j["pin"] == "P1":
                if len(K.supported_pms(T, other, u)) != 1:
                    return False, f"{skey}: P1 pinning of u fails"
            elif j["pin"] == "P2":
                c = u[0]
                if any(x != c for x in u):
                    return False, f"{skey}: P2 on a non-constant u"
                cw = (c,) * C.N
                if not K.is_split(T, cw, L, R):
                    return False, f"{skey}: P2 pinning of u fails"
            else:
                return False, f"{skey}: unknown pinning"
            zeros[y] = monos
        elif j["role"] == "nonzero":
            if j["pin"] == "P1":
                if len(K.supported_pms(T, sites, y)) != 1:
                    return False, f"{skey}: P1 pinning of y fails"
            elif j["pin"] == "P2":
                c = y[0]
                if any(x != c for x in y):
                    return False, f"{skey}: P2 on a non-constant y"
                cw = (c,) * C.N
                if not K.is_split(T, cw, L, R):
                    return False, f"{skey}: P2 pinning of y fails"
            else:
                return False, f"{skey}: unknown pinning"
            nonzeros[y] = monos
        else:
            return False, f"{skey}: unknown role"
    ok, msg = RA.verify(len(vidx), zeros, nonzeros, _keys_from_str(cert["ratio"]))
    return ok, msg


# ------------------------------------------------------------- reason set

def half_fibre_reason(T, sites, y):
    """Literals fixing exactly which matchings of `sites` are supported at y."""
    colour = dict(zip(tuple(sorted(sites)), y))
    out = []
    for pm in K.pms_of(sites):
        cells = []
        empty = None
        for (u, v) in pm:
            e = C.EIDX[(u, v)]
            i, j = colour[u], colour[v]
            cells.append((e, i, j))
            if empty is None and not (T[e] >> (3 * i + j)) & 1:
                empty = (e, i, j)
        if empty is None:
            out.extend(("on", e, i, j) for (e, i, j) in cells)
        else:
            out.append(("off",) + empty)
    return out


def _pin_reason(T, sites, sub, kind, L, R):
    if kind == "P1":
        r = K.p1_reason(T, sites, sub)
        return [] if r is None else [tuple(x) for x in r]
    return [tuple(x) for x in K.split_reason(T, (sub[0],) * C.N, L, R)]


def reason_D(T, cert):
    """Cell literals that already force this Lemma W18-D kill."""
    L, R = tuple(cert["cut_L"]), tuple(cert["cut_R"])
    sites = tuple(cert["side"])
    other = tuple(cert["other"])
    lits = []
    for skey, j in cert["justification"].items():
        y = tuple(int(c) for c in skey)
        if j["role"] == "zero":
            w = tuple(j["w"])
            lits += [tuple(x) for x in K.split_reason(T, w, L, R)]
            lits += _pin_reason(T, other, tuple(j["u"]), j["pin"], L, R)
        else:
            lits += _pin_reason(T, sites, y, j["pin"], L, R)
        lits += half_fibre_reason(T, sites, y)
    return K._dedupe([list(x) for x in lits])


def reason_D_sufficient(T, cert, reason, off_edges=()):
    """Does `reason` alone force the kill?  Rebuilds the system from it."""
    for lit in reason:
        kind, e, i, j = lit[0], lit[1], lit[2], lit[3]
        if (kind == "on") != bool((T[e] >> (3 * i + j)) & 1):
            return False, "reason literal false in T"
    lits = K._state_map(reason, off_edges)
    L, R = tuple(cert["cut_L"]), tuple(cert["cut_R"])
    sites = tuple(cert["side"])
    other = tuple(cert["other"])
    vidx = side_varindex(sites)
    zeros, nonzeros = {}, {}
    for skey, j in cert["justification"].items():
        y = tuple(int(c) for c in skey)
        monos = _forced_monomials(lits, sites, vidx, y)
        if monos is None:
            return False, f"{skey}: the side fibre is not forced"
        if j["role"] == "zero":
            w = tuple(j["w"])
            if len(set(w)) == 1 or K.join(other, sites, tuple(j["u"]), y) != w:
                return False, f"{skey}: bad recorded word"
            if not K._split_forced(lits, w, L, R):
                return False, f"{skey}: splitness not forced"
            if not _pin_forced(lits, other, tuple(j["u"]), j["pin"], L, R):
                return False, f"{skey}: pinning of u not forced"
            zeros[y] = monos
        else:
            if not _pin_forced(lits, sites, y, j["pin"], L, R):
                return False, f"{skey}: pinning of y not forced"
            nonzeros[y] = monos
    return RA.verify(len(vidx), zeros, nonzeros, _keys_from_str(cert["ratio"]))


def _pin_forced(lits, sites, sub, kind, L, R):
    if kind == "P1":
        return K._p1_forced(lits, sites, sub)
    if kind == "P2":
        if any(x != sub[0] for x in sub):
            return False
        return K._split_forced(lits, (sub[0],) * C.N, L, R)
    return False


def _forced_monomials(lits, sites, vidx, y):
    """Monomials of F^side_y if the reason decides every matching, else None."""
    colour = dict(zip(tuple(sorted(sites)), y))
    out = []
    for pm in K.pms_of(sites):
        states = []
        cells = []
        for (u, v) in pm:
            e = C.EIDX[(u, v)]
            i, j = colour[u], colour[v]
            cells.append((e, i, j))
            states.append(lits.get((e, i, j)))
        if all(s == "on" for s in states):
            vec = [0] * len(vidx)
            for key in cells:
                vec[vidx[key]] += 1
            out.append(tuple(vec))
        elif any(s == "off" for s in states):
            continue
        else:
            return None
    return sorted(out)


def minimise_reason_D(T, cert, reason, off_edges=()):
    reason = [list(l) for l in reason if l[1] not in set(off_edges)]
    k = 0
    while k < len(reason):
        trial = reason[:k] + reason[k + 1:]
        ok, _ = reason_D_sufficient(T, cert, trial, off_edges)
        if ok:
            reason = trial
        else:
            k += 1
    return reason
