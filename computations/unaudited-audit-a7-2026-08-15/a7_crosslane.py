#!/usr/bin/env python3
"""A7 -- TARGET 5: do the W16 / W19 / W20 engines agree with MINE on the
m=26 template's full fibre data?

Compares, word by word, the SET of supported perfect matchings (not just its
size) computed by
  * a7_core.fibre           (mine, bitmask-recursion matchings)
  * a7_core.fibre_dp        (mine, subset DP -- independent route)
  * w16_core.support
  * w19_core.support
  * w20_core (whatever its support routine is called)
on 200 random words (fixed seed) AND on all 6561 words for the fibre SIZE.
A matching-index comparison requires the three lanes to use the same PM
indexing; that is checked first by comparing the PM lists themselves.
"""
from __future__ import annotations
import os, sys, json, random, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import W8_IMMUNE, WORDS, MIXED, fibre, fibre_dp, PMS, EDGES

HERE = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.dirname(HERE)
LANES = {
    "w16": os.path.join(COMP, "unaudited-residual2-w16-2026-08-15", "w16_core.py"),
    "w19": os.path.join(COMP, "unaudited-forcing-w19-2026-08-15", "w19_core.py"),
    "w20": os.path.join(COMP, "unaudited-lasttwo-w20-2026-08-15", "w20_core.py"),
    "w8":  os.path.join(COMP, "unaudited-template-kill-w8-2026-08-15", "w8_core.py"),
}


def load(name, path):
    sys.path.insert(0, os.path.dirname(path))
    spec = importlib.util.spec_from_file_location("lane_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def support_of(mod, T, w):
    for nm in ("support", "fibre", "supp"):
        f = getattr(mod, nm, None)
        if callable(f):
            try:
                return list(f(T, w))
            except TypeError:
                pass
    return None


def main():
    res = {}
    T = W8_IMMUNE[26]
    rnd = random.Random(20260815)
    sample = [tuple(rnd.randrange(3) for _ in range(8)) for _ in range(200)]
    mods = {}
    for k, p in LANES.items():
        try:
            mods[k] = load(k, p)
        except Exception as e:
            res.setdefault("load_errors", {})[k] = str(e)
    # PM indexing agreement
    pmcmp = {}
    for k, mod in mods.items():
        P = getattr(mod, "PMS", None)
        if P is None:
            pmcmp[k] = "no PMS"
            continue
        Pl = [tuple(sorted(tuple(sorted(e)) for e in m)) for m in P]
        Ml = [tuple(sorted(tuple(sorted(e)) for e in m)) for m in PMS]
        pmcmp[k] = dict(same_length=(len(Pl) == len(Ml)),
                        same_order=(Pl == Ml),
                        same_set=(sorted(Pl) == sorted(Ml)))
    res["PM_indexing"] = pmcmp
    print("PM indexing vs mine:", json.dumps(pmcmp))
    # EDGES agreement
    ecmp = {k: (list(map(tuple, getattr(m, "EDGES", []))) == list(EDGES))
            for k, m in mods.items()}
    res["EDGES_identical"] = ecmp
    print("EDGES identical:", ecmp)
    # support-set comparison on the 200 sampled words
    cmp200 = {}
    for k, mod in mods.items():
        bad_set = bad_size = tested = 0
        for w in sample:
            mine = fibre(T, w)
            theirs = support_of(mod, T, w)
            if theirs is None:
                bad_set = bad_size = -1
                break
            tested += 1
            if len(theirs) != len(mine):
                bad_size += 1
            if sorted(theirs) != sorted(mine):
                bad_set += 1
        cmp200[k] = dict(tested=tested, size_mismatches=bad_size,
                         set_mismatches=bad_set)
    res["sample200"] = cmp200
    print("200-word comparison (m=26):", json.dumps(cmp200))
    # full 6561-word size comparison
    full = {}
    for k, mod in mods.items():
        bad = 0
        for w in WORDS:
            th = support_of(mod, T, w)
            if th is None:
                bad = -1
                break
            if len(th) != len(fibre(T, w)):
                bad += 1
        full[k] = bad
    res["all6561_size_mismatches"] = full
    print("all-6561 fibre-size mismatches:", full)
    # my own two routes on all 6561
    own = sum(1 for w in WORDS if len(fibre(T, w)) != fibre_dp(T, w))
    res["own_two_routes_mismatches"] = own
    print("my direct vs my DP on all 6561:", own)
    # MUTATION control: a corrupted template must produce mismatches
    Tm = list(T)
    Tm[5] ^= 1
    mut = 0
    if "w19" in mods:
        for w in sample:
            if sorted(support_of(mods["w19"], Tm, w)) != sorted(fibre(T, w)):
                mut += 1
    res["mutation_control_mismatches"] = mut
    print("MUTATION control (corrupt template vs true) mismatches:", mut)
    json.dump(res, open(os.path.join(HERE, "results_crosslane.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
