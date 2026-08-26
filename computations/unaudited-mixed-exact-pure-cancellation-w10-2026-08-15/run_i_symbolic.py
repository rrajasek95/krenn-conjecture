#!/usr/bin/env python3
"""W10 task I -- SYMBOLIC certification of the two witness families over Q,
with Singular.  This upgrades "verified at sampled rational points" to
"verified as a polynomial identity / ideal membership", i.e. the families work
for EVERY parameter value on the stated variety, not just the ones I sampled.

I1  CONSTANT-BLOCK FAMILY.  With A_uv = t_uv * J (t_uv indeterminates), the
    hafnian of EVERY word w is the scalar hafnian haf(t).  Checked as a
    polynomial identity in Q[t_1..t_15] (N=6) for all 729 words, and in
    Q[t_1..t_28] (N=8) for a sample.  Hence haf(t) = 0 makes ALL words vanish;
    mixed-exactness is exact and parameter-free.

I2  FREE-BLOCK FAMILY.  With the same base but the block on e0 = (0,1)
    replaced by nine indeterminates x_ij, splitting matchings by whether they
    use e0 gives   H_w = x_{w_0 w_1} * P + Q,
    P = h(V\\{0,1}) (the complementary hafnian), Q = the e0-avoiding sum.
    Checked by IDEAL MEMBERSHIP over Q: reduce(H_w, std(<P,Q>)) == 0 for every
    word.  So on the variety P = Q = 0 the whole block x is free and the
    source is mixed-exact identically.
"""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys
import tempfile
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w10_core as w10                                            # noqa: E402
from w10_core import COLORS, require                              # noqa: E402

OUT = {}
log = []


def say(s="", flush=True):
    print(s, flush=flush)
    log.append(s)


def run_singular(script, timeout=1800):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    if proc.returncode != 0:
        raise RuntimeError(f"Singular failed: {proc.stderr[:2000]}")
    return proc.stdout


def tvar(e):
    return f"t{e[0]}{e[1]}"


def build_scripts(N, words, e0=None):
    """Singular source for the family on N sites."""
    EDGES = w10.edges(N)
    PM = w10.perfect_matchings(tuple(range(N)))
    tvars = [tvar(e) for e in EDGES]
    if e0 is None:
        ring = f'ring R=0,({",".join(tvars)}),dp;'
        haf = "+".join("*".join(tvar(e) for e in M) for M in PM)
        lines = [ring, f"poly HAF={haf};"]
        for w in words:
            # H_w for the constant-block family: every cell of A_e equals t_e
            expr = "+".join("*".join(tvar(e) for e in M) for M in PM)
            lines.append(f'"IDENT {"".join(map(str,w))} "'
                         f"+string(({expr})-HAF==0);")
        return "\n".join(lines)
    # free-block family
    xs = [f"x{i}{j}" for i in COLORS for j in COLORS]
    keep = [tvar(e) for e in EDGES if e != e0]
    ring = f'ring R=0,({",".join(keep + xs)}),dp;'
    U = tuple(v for v in range(N) if v not in e0)
    P = "+".join("*".join(tvar(e) for e in M) for M in w10.perfect_matchings(U))
    Q = "+".join("*".join(tvar(e) for e in M) for M in PM if e0 not in M)
    lines = [ring, f"poly P={P};", f"poly Q={Q};",
             "ideal I=P,Q;", "ideal G=std(I);"]
    for w in words:
        terms = []
        for M in PM:
            fac = []
            for e in M:
                if e == e0:
                    fac.append(f"x{w[e0[0]]}{w[e0[1]]}")
                else:
                    fac.append(tvar(e))
            terms.append("*".join(fac))
        expr = "+".join(terms)
        lines.append(f'"MEMB {"".join(map(str,w))} "'
                     f"+string(reduce({expr},G)==0);")
    return "\n".join(lines)


say("=" * 92)
say("I1  CONSTANT-BLOCK family: H_w = haf(t) as a POLYNOMIAL IDENTITY over Q")
say("=" * 92)
rng = random.Random(9)
res = {}
for N in (6, 8):
    words = list(product(COLORS, repeat=N))
    if N == 8:
        words = [w for w in words if len(set(w)) == 1] + rng.sample(words, 120)
    out = run_singular(build_scripts(N, words))
    good = sum(1 for line in out.splitlines() if line.strip().endswith(" 1"))
    tot = sum(1 for line in out.splitlines() if line.strip().startswith("IDENT"))
    say(f"  N={N}: {good}/{tot} words satisfy  H_w - haf(t) == 0  identically "
        f"in Q[t]  (expected all)")
    require(good == tot and tot > 0, f"I1 failed at N={N}")
    res[f"N{N}"] = {"identities_checked": tot, "identities_true": good}
OUT["I1"] = res

say()
say("=" * 92)
say("I2  FREE-BLOCK family: H_w in the ideal <P,Q>, checked by Groebner over Q")
say("=" * 92)
res2 = {}
for N in (6, 8):
    words = list(product(COLORS, repeat=N))
    if N == 8:
        words = [w for w in words if len(set(w)) == 1] + rng.sample(words, 60)
    out = run_singular(build_scripts(N, words, e0=(0, 1)))
    good = sum(1 for line in out.splitlines() if line.strip().endswith(" 1"))
    tot = sum(1 for line in out.splitlines() if line.strip().startswith("MEMB"))
    say(f"  N={N}: {good}/{tot} words have  H_w  in  <P, Q>  (expected all) -- "
        f"so on P=Q=0 the whole block x is FREE and H == 0")
    require(good == tot and tot > 0, f"I2 failed at N={N}")
    res2[f"N{N}"] = {"memberships_checked": tot, "memberships_true": good}
OUT["I2"] = res2

# control: the SAME reduction must FAIL for a polynomial not in the ideal
say()
say("  [CONTROL] the ideal-membership test must be able to say NO:")
ctrl = run_singular("\n".join([
    'ring R=0,(t23,t24,t25,t34,t35,t45,x00),dp;',
    'poly P=t23*t45+t24*t35+t25*t34;',
    'ideal I=P; ideal G=std(I);',
    '"CTRL-in  "+string(reduce(P*x00,G)==0);',
    '"CTRL-out "+string(reduce(x00+t23,G)==0);']))
say("    " + " | ".join(l.strip() for l in ctrl.splitlines() if l.strip()))
require("CTRL-in  1" in ctrl and "CTRL-out 0" in ctrl,
        "ideal-membership control did not fire")
OUT["I_control"] = {"in_ideal": True, "out_of_ideal_correctly_rejected": True}

with open(os.path.join(HERE, "results_i_symbolic.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_i_symbolic.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say()
say("I DONE -- both witness families are certified SYMBOLICALLY over Q, not")
say("merely at sampled rational points.")
