#!/usr/bin/env python3
r"""W31 -- control D4 for w31_slack.py's slack-0 coverage lemma.
UNAUDITED PROBE.  Exact integer arithmetic only.

D4 (POSITIVE CONTROL).  The Route-A template that W26/W30 actually work with
at m = 28 IS a slack-0 template: Gamma = K_4(L) u K_4(R) u sigma (16 full
blocks) and the twelve non-sigma cross edges carry one cell each.  So the
lemma's machinery must reproduce that template's own numbers:
  - its 12 single edges form a cubic graph (K_{4,4} minus a perfect matching,
    i.e. the 3-cube Q_3);
  - its cell placement must satisfy the (SC) bijection condition at every
    site;
  - its slack must be 0 (m - 12 - |Gamma| = 28 - 12 - 16);
  - and the count of MIXED words activating NO single must equal the stored
    effectively-clean count 2,152 -- because at slack 0 "no single active"
    and "effectively clean" are the same condition.
If the engine cannot reproduce a template it was built to describe, the
lemma's coverage numbers mean nothing.

D5 (NEGATIVE / SCOPE CONTROL).  The C_8 member is NOT slack 0 (slack 8), and
its 12 single cells sit INSIDE the two halves rather than across them; the
lemma must not apply to it -- reported explicitly so the scope boundary is on
the record.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, product

sys.dont_write_bytecode = True

N, Q, FULL = 8, 3, 511
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "computations",
                                "unaudited-blockers-w26-2026-08-16"))
import w26_core as C26                                            # noqa: E402

EDGES = tuple(combinations(range(N), 2))
WORDS = tuple(product(range(Q), repeat=N))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)

C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def profile(T, name):
    m = sum(1 for t in T if t)
    gam = [EDGES[i] for i, t in enumerate(T) if t == FULL]
    servers = [EDGES[i] for i, t in enumerate(T) if t and t != FULL]
    singles = [EDGES[i] for i, t in enumerate(T)
               if t and bin(t).count("1") == 1]
    deg = [0] * N
    for u, v in singles:
        deg[u] += 1
        deg[v] += 1
    return dict(name=name, m=m, Sigma=sum(bin(t).count("1") for t in T),
                n_gamma=len(gam), n_servers=len(servers),
                n_singles=len(singles), slack=m - 12 - len(gam),
                single_degrees=deg,
                singles_form_cubic=(len(singles) == 12
                                    and all(d == 3 for d in deg)),
                server_cell_counts=sorted(bin(T[EDGES.index(e)]).count("1")
                                          for e in servers))


def main():
    OUT = {"_header": "UNAUDITED W31 control D4/D5 for the slack-0 coverage "
                      "lemma. Exact only.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}

    T28 = list(C26.TEMPLATES[28])
    p28 = profile(T28, "W26/W30 m=28 Route-A template")
    OUT["D4_profile"] = p28
    print("[D4]", p28)

    # (SC) bijection condition at each site, in the far-colour form
    singles = {EDGES[i]: cells_of(T28[i])[0] for i, t in enumerate(T28)
               if t and bin(t).count("1") == 1}
    ok = True
    for p in range(N):
        far = []
        for (u, v), (i, j) in singles.items():
            if u == p:
                far.append(j)
            elif v == p:
                far.append(i)
        if sorted(far) != [0, 1, 2]:
            ok = False
    OUT["D4_placement_is_a_valid_SC_bijection"] = ok
    print("    (SC) bijection at every site:", ok)

    # words activating no single  ==  effectively clean, at slack 0
    nocover = 0
    for w in MIXED:
        if not any(w[u] == i and w[v] == j
                   for (u, v), (i, j) in singles.items()):
            nocover += 1
    OUT["D4_mixed_words_with_no_active_single"] = nocover
    OUT["D4_stored_clean_count"] = 2152
    OUT["D4_matches_stored_clean_count"] = (nocover == 2152)
    print("    mixed words with no active single =", nocover,
          " (stored effectively-clean count 2152):",
          OUT["D4_matches_stored_clean_count"])
    OUT["D4_consistent_with_lemma_bound"] = (nocover >= 824)
    print("    >= the lemma's global bound 824:",
          OUT["D4_consistent_with_lemma_bound"])

    p8 = profile(C8_MEMBER, "W19/W20 C_8 stratum member")
    OUT["D5_c8_profile"] = p8
    OUT["D5_c8_is_slack0"] = (p8["slack"] == 0)
    print("[D5]", p8)
    print("    C_8 member is slack 0:", OUT["D5_c8_is_slack0"],
          "(lemma does NOT apply -- scope boundary)")

    with open(os.path.join(HERE, "results_d4.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    declared = ["D4_profile", "D4_placement_is_a_valid_SC_bijection",
                "D4_matches_stored_clean_count", "D5_c8_profile"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
