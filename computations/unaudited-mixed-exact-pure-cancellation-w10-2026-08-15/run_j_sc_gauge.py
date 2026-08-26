#!/usr/bin/env python3
"""W10 task J -- the coordinator's question: does MIXED-EXACTNESS alone force
the slice-cover condition (SC)?  And what exactly does the slice-cover
derivation consume?

(SC) [notes/slice-cover.md section 2, "Forced incident-edge theorem"]: for
every vertex p and colour r there is a neighbour j with A_pj = a (x) e_r^{(j)}
and C_pj != 0.  Its TEMPLATE shadow is W8's `fie_ok`: all cells of A_pj lie in
column r at j.

J1  (SC) is a TEMPLATE-level, GAUGE-INVARIANT condition (verified).
J2  MIXED-EXACT alone does NOT force (SC): W10's witnesses are mixed-exact and
    fail (SC) at EVERY (vertex,colour) slot -- 18/18 at N=6, 24/24 at N=8.
J3  MIXED-EXACT + all three pure coefficients NONZERO DOES force (SC):
    by Lemma W10-G such a source is gauge-equivalent, with the same template,
    to an EXACT source, which satisfies (SC) by the committed theorem; and (SC)
    is gauge-invariant (J1).  So the derivation consumes exactly "the pure
    coefficients are nonzero", not "they equal 1".
    (Reading the note: the derivation contracts the star expansion into
     eq (4), whose LEFT side is sum_r lambda(e_r) H_{r^N} e_r^{(x)(B\\p)}.  With
     all three H_{r^N} != 0 this is a rank-3 diagonal tensor on the torus and
     the covering lemma applies verbatim; if some H_{r^N} = 0 the left side
     drops rank and the argument does not apply as written.)
J4  At N=6 the hypothesis of J3 is EMPTY (Corollary W10-6), so at six sites
    (SC) is not available for mixed-exact sources at all.
"""
from __future__ import annotations
import json, os, random, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE, os.path.join(REPO, "computations",
                             "unaudited-template-kill-w8-2026-08-15")):
    if p not in sys.path:
        sys.path.insert(0, p)
import w10_core as w10                                            # noqa: E402
from w10_core import COLORS, require                              # noqa: E402
import w8_core as w8                                              # noqa: E402

OUT = {}; log = []
def say(s="", flush=True):
    print(s, flush=flush); log.append(s)

def sc_unserved(src, size):
    tpl = w10.template_of(src, size)
    masks = []
    for e in w10.edges(size):
        mk = 0
        for (i, j) in tpl[e]:
            mk |= 1 << (3 * i + j)
        masks.append(mk)
    fd = w8.fie_demands(w8.geometry(size), masks)
    return sum(1 for k, v in fd.items() if not v)

say("=" * 92)
say("J1  (SC) is gauge-invariant (template-level)")
say("=" * 92)
rng = random.Random(31337)
bad = tot = 0
for trial in range(40):
    size = 6 if trial % 2 == 0 else 8
    src = w10.zero_source(size)
    for e in w10.edges(size):
        style = rng.random()
        for i in COLORS:
            for j in COLORS:
                if style < 0.4 and j != rng.randrange(3):
                    continue
                if rng.random() < 0.5:
                    src[e][i][j] = F(rng.randint(-5, 5) or 2, rng.randint(1, 3))
    g = [[F(rng.randint(-5, 5) or 3, rng.randint(1, 3)) for _ in COLORS]
         for _ in range(size)]
    a = sc_unserved(src, size)
    b = sc_unserved(w10.apply_gauge(src, size, g), size)
    tot += 1
    if a != b:
        bad += 1
say(f"  {tot} random (source, gauge) pairs: {bad} changed their (SC) count "
    f"(expected 0)")
require(bad == 0, "(SC) is not gauge invariant?!")
OUT["J1"] = {"pairs": tot, "changes": bad}

say()
say("=" * 92)
say("J2  MIXED-EXACT alone does NOT force (SC) -- the W10 witnesses")
say("=" * 92)
b = json.load(open(os.path.join(HERE, "results_b_witness_n6.json")))
rows = []
for key in ("WA", "WA2"):
    src = w10.src_from_repr(b[key]["source"], 6)
    u = sc_unserved(src, 6)
    rows.append({"witness": key, "N": 6, "sc_unserved": u, "of": 18})
    say(f"  N=6 {key:4s}: mixed-exact, (SC) unserved {u}/18")
for rec in b["WC"]:
    src = w10.src_from_repr(rec["source"], 6)
    u = sc_unserved(src, 6)
    rows.append({"witness": rec["label"], "N": 6, "sc_unserved": u, "of": 18})
c = json.load(open(os.path.join(HERE, "results_c_n8.json")))
for rec in c["C1_sweep"]:
    rows.append({"witness": f"N8 m={rec['m']}", "N": 8,
                 "sc_unserved": rec["S1_forced_incidence_failures"], "of": 24})
say(f"  N=6: all {len([r for r in rows if r['N']==6])} witnesses have (SC) "
    f"unserved = 18/18 (every slot).")
say(f"  N=8: all {len([r for r in rows if r['N']==8])} witnesses have (SC) "
    f"unserved = 24/24 (every slot).")
require(all(r["sc_unserved"] == r["of"] for r in rows), "some witness serves SC")
OUT["J2"] = rows

say()
say("=" * 92)
say("J3/J4  what the slice-cover derivation actually consumes")
say("=" * 92)
say("  Lemma W10-G: mixed-exact + all three pures NONZERO  =>  gauge-equivalent")
say("  (same template) to EXACT  =>  (SC) holds for the gauged source  =>  (by")
say("  J1) (SC) holds for the original.  So (SC) needs the pure coefficients")
say("  to be NONZERO, not to be 1.")
say("  At N=6 that hypothesis is EMPTY (Corollary W10-6: some pure must vanish),")
say("  so at six sites (SC) is unavailable for mixed-exact sources -- the class")
say("  'mixed-exact + (SC)' at N=6 is a genuinely separate object, not a")
say("  consequence of mixed-exactness.")
OUT["J3"] = {"sc_from": "mixed-exact + all three pures nonzero",
             "sc_not_from": "mixed-exactness alone (J2, 26 witnesses)",
             "n6_hypothesis_empty": True}

with open(os.path.join(HERE, "results_j_sc_gauge.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_j_sc_gauge.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("J DONE")
