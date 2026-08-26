#!/usr/bin/env python3
"""A6 / TARGET A step 1-2: independent fibre data + clean-word claims."""
from __future__ import annotations

import json
from itertools import product

import a6_engine as E

T = E.M24
V = E.Vars(T)
GM = set(E.gamma_matchings(T))
out = {}

# ---------------------------------------------------------------- audit
a = E.audit(T)
out["audit"] = dict(m=a["m"], sigma=a["sigma"], n_full=len(a["full"]),
                    full=[list(e) for e in a["full"]],
                    n_single=len(a["singles"]),
                    singles={f"{u}{v}": [c // 3, c % 3]
                             for (u, v), c in a["singles"].items()},
                    n_partial_other=len(a["partial"]),
                    const_fibres=a["consts"], min_mixed_fibre=a["min_mixed"],
                    hist=dict(sorted(a["hist"].items())))
out["n_gamma_matchings"] = len(GM)
out["gamma_matchings"] = [list(map(list, E.MATCHINGS[i])) for i in sorted(GM)]

# ------------------------------------------------ every fibre contains F(Gamma)
out["F_Gamma_subset_of_every_fibre"] = all(
    GM <= set(E.fibre(T, w)) for w in E.WORDS)

# ---------------------------------------- effectively clean vs syntactically clean
singles = a["singles"]          # (u,v) -> cell


def active_singles(w):
    res = []
    for (u, v), c in singles.items():
        if w[u] == c // 3 and w[v] == c % 3:
            res.append((u, v))
    return res


eclean, sclean, eclean_mixed, sclean_mixed = [], [], [], []
for w in E.WORDS:
    f = set(E.fibre(T, w))
    ec = (f == GM)
    sc = not active_singles(w)
    if sc and not ec:
        raise SystemExit("syntactically clean but fibre bigger: %s" % (w,))
    if ec:
        eclean.append(w)
        if len(set(w)) > 1:
            eclean_mixed.append(w)
    if sc:
        sclean.append(w)
        if len(set(w)) > 1:
            sclean_mixed.append(w)

out["counts"] = dict(effectively_clean_all=len(eclean),
                     effectively_clean_mixed=len(eclean_mixed),
                     syntactically_clean_all=len(sclean),
                     syntactically_clean_mixed=len(sclean_mixed),
                     eclean_constants=[list(w) for w in eclean
                                       if len(set(w)) == 1],
                     sclean_constants=[list(w) for w in sclean
                                       if len(set(w)) == 1])

# ------------------------------------------------------- binomial shape check
LEFT = (0, 1, 2, 3)


def binomial_shape(w):
    """P_L(x)P_R(y) + A07 A14 A23 A56, built directly from the 7 matchings'
    definition -- but assembled by an independent factorisation formula."""
    PL = {}
    for (e1, e2) in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        PL = E.padd(PL, {tuple(sorted((V.vw(e1, w), V.vw(e2, w)))): 1})
    PR = {}
    for (e1, e2) in (((4, 5), (6, 7)), ((4, 7), (5, 6))):
        PR = E.padd(PR, {tuple(sorted((V.vw(e1, w), V.vw(e2, w)))): 1})
    extra = {tuple(sorted((V.vw((0, 7), w), V.vw((1, 4), w),
                           V.vw((2, 3), w), V.vw((5, 6), w)))): 1}
    return E.padd(E.pmul(PL, PR), extra), PL, PR


bad = []
for w in eclean:
    H = E.Hpoly(T, V, w)
    B, _, _ = binomial_shape(w)
    if H != B:
        bad.append(list(w))
out["binomial_shape_holds_on_all_effectively_clean"] = (not bad)
out["binomial_shape_failures"] = bad[:10]

# a control: on some NON-effectively-clean word the shape must FAIL
ctrl = []
for w in E.WORDS:
    if set(E.fibre(T, w)) != GM:
        B, _, _ = binomial_shape(w)
        ctrl.append(E.Hpoly(T, V, w) == B)
        if len(ctrl) > 200:
            break
out["control_shape_fails_off_clean"] = dict(checked=len(ctrl),
                                            n_agreeing=sum(ctrl))

# ---------------------------------------------------- 0^8 effectively clean
z = (0,) * 8
out["zero_word"] = dict(
    active_singles=[list(e) for e in active_singles(z)],
    fibre_size=len(E.fibre(T, z)),
    fibre_equals_FGamma=(set(E.fibre(T, z)) == GM),
    other_constants={"1^8": len(E.fibre(T, (1,) * 8)),
                     "2^8": len(E.fibre(T, (2,) * 8))},
    one_eight_extra=[list(map(list, E.MATCHINGS[i]))
                     for i in E.fibre(T, (1,) * 8) if i not in GM],
    two_eight_extra=[list(map(list, E.MATCHINGS[i]))
                     for i in E.fibre(T, (2,) * 8) if i not in GM],
)

# crossing-parity argument, verified by brute force:
# no perfect matching of K8 containing (0,4) has all other edges supported at 0^8
cnt = 0
for mi, m in enumerate(E.MATCHINGS):
    if (0, 4) in m:
        if all(E.occ(T, E.EIDX[e], E.cell(E.EIDX[e], z)) for e in m):
            cnt += 1
out["zero_word"]["supported_matchings_through_04"] = cnt
# crossing edges supported at 0^8
cross = [(u, v) for (u, v) in E.EDGES if u < 4 <= v
         and E.occ(T, E.EIDX[(u, v)], E.cell(E.EIDX[(u, v)], z))]
out["zero_word"]["supported_crossing_edges_at_0^8"] = [list(e) for e in cross]

json.dump(out, open("results_A1_fibres.json", "w"), indent=1)
for k, v in out.items():
    if k in ("gamma_matchings", "audit"):
        continue
    print(k, "=", json.dumps(v)[:600])
print("audit:", json.dumps(out["audit"])[:800])
