#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- the 8-word KILL CERTIFICATE for the m=20 survivor.

The certificate uses only EIGHT of the template's 162 live words and is
checkable by hand.  Every fibre below is recomputed from the template here;
nothing is hard-coded except the word list and the final Singular query.

    w1 = 00011000 :  x24_01 x56_00 + x26_00 x45_10            = 0
    w2 = 00011020 :  x24_01 x56_02 + x26_02 x45_10            = 0
    w3 = 00111000 :  x24_11 x56_00 + x26_10 x45_10            = 0
    w4 = 00111020 :  x24_11 x56_02 + x26_12 x45_10            = 0
    w5 = 00100000 :  x15_00 x26_10 + x16_00 x25_10            = 0
    w6 = 00100020 :  x15_00 x26_12 + x16_02 x25_10            = 0
    w7 = 00000020 :  x12_00 x56_02 + x15_00 x26_02 + x16_02 x25_00 = 0
    c0 = 00000000 :  x12_00 x56_00 + x15_00 x26_00 + x16_00 x25_00 != 0

    w1,w2 => x56_00 / x56_02 = x26_00 / x26_02   (divide; x24_01, x45_10 != 0)
    w3,w4 => x56_00 / x56_02 = x26_10 / x26_12
    w5,w6 => x26_10 / x26_12 = x16_00 / x16_02   (x15_00, x25_10 != 0)
    hence, with lambda := x56_00 / x56_02  (nonzero),
           x56_00 = lambda x56_02,  x26_00 = lambda x26_02,  x16_00 = lambda x16_02
    hence  F(0^8) = lambda * F(00000020) = lambda * 0 = 0,
    contradicting the constant word 0^8.  QED.

(The printed fibres carry the common factors x07_00 x13_01 / x07_00 x34_00,
which are nonzero and were divided out above.)
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w12_core as C  # noqa: E402
from run_t4_calibration import load_survivor  # noqa: E402

WORDS = ["00011000", "00011020", "00111000", "00111020",
         "00100000", "00100020", "00000020"]
CONST = "00000000"


def poly(sysv, word):
    monos = sysv.mixed_eqs.get(word) or sysv.const_eqs.get(word)
    return monos


def to_singular(sysv, monos, names):
    return "+".join("*".join(names[v] for v in mono) for mono in monos)


def main():
    geo = C.geometry()
    T = load_survivor()
    sysv = C.ValueSystem(geo, T)
    out = {"template": list(T)}

    # 1. recompute the fibres from the template
    rows = []
    for s in WORDS + [CONST]:
        w = tuple(int(ch) for ch in s)
        monos = poly(sysv, w)
        assert monos is not None, f"word {s} has an empty fibre"
        rows.append({"word": s, "mixed": geo.is_mixed(w), "size": len(monos),
                     "monomials": [[sysv.varname(v) for v in m]
                                   for m in monos]})
        print(f"{s} {'mixed' if geo.is_mixed(w) else 'CONSTANT':8s} "
              f"|fibre|={len(monos)}  "
              + " + ".join("*".join(sysv.varname(v) for v in m)
                           for m in monos))
    out["fibres"] = rows

    # 2. machine verification: on {all cells != 0} the seven mixed equations
    #    force F(0^8) = 0, i.e. 1 lies in <F_w1..F_w7, t*(prod vars)*F(c0)-1>.
    used = set()
    for s in WORDS + [CONST]:
        for m in poly(sysv, tuple(int(ch) for ch in s)):
            used.update(m)
    used = sorted(used)
    names = {v: f"y{k}" for k, v in enumerate(used)}
    varlist = [names[v] for v in used]
    gens = [to_singular(sysv, poly(sysv, tuple(int(ch) for ch in s)), names)
            for s in WORDS]
    cpoly = to_singular(sysv, poly(sysv, tuple(int(ch) for ch in CONST)), names)
    prod = "*".join(varlist)
    script = "\n".join([
        f'ring RC=0,({",".join(varlist)},t),dp;',
        "ideal I=" + ",".join(gens) + ";",
        f"ideal J=I,t*({prod})*({cpoly})-1;",
        "ideal G=std(J);",
        '"CERT "+string(reduce(1,G)==0);'])
    with open(os.path.join(HERE, "survivor_certificate.sing"), "w") as fh:
        fh.write(script + "\nquit;\n")
    res = C.run_singular(script, timeout=900)
    verified = "CERT 1" in res
    out["variables_used"] = [sysv.varname(v) for v in used]
    out["singular_output"] = res.strip()
    out["certificate_verified"] = verified
    print(f"\nSINGULAR verification (7 mixed equations + all cells nonzero "
          f"forces F(0^8)=0): {verified}")

    # 3. mutation controls: each of the seven equations must be NECESSARY
    drops = {}
    for k in range(len(WORDS)):
        sub = [g for n, g in enumerate(gens) if n != k]
        sc = "\n".join([
            f'ring RD=0,({",".join(varlist)},t),dp;',
            "ideal I=" + ",".join(sub) + ";",
            f"ideal J=I,t*({prod})*({cpoly})-1;",
            "ideal G=std(J);",
            '"DROP "+string(reduce(1,G)==0);'])
        r = C.run_singular(sc, timeout=900)
        drops[WORDS[k]] = ("DROP 1" in r)
        print(f"  MUTATION: drop {WORDS[k]} -> still a kill? "
              f"{drops[WORDS[k]]}  (False = that word is load-bearing)")
    out["mutation_drop_one_equation"] = drops

    # 4. mutation control on the target: the SAME seven equations must NOT
    #    force the OTHER constant words to vanish.
    others = {}
    for s in ("11111111", "22222222"):
        w = tuple(int(ch) for ch in s)
        monos = poly(sysv, w)
        vs = sorted({v for m in monos for v in m} | set(used))
        nm = {v: f"z{k}" for k, v in enumerate(vs)}
        vl = [nm[v] for v in vs]
        g2 = [to_singular(sysv, poly(sysv, tuple(int(ch) for ch in t)), nm)
              for t in WORDS]
        c2 = to_singular(sysv, monos, nm)
        sc = "\n".join([
            f'ring RE=0,({",".join(vl)},t),dp;',
            "ideal I=" + ",".join(g2) + ";",
            f"ideal J=I,t*({'*'.join(vl)})*({c2})-1;",
            "ideal G=std(J);",
            '"OTHER "+string(reduce(1,G)==0);'])
        r = C.run_singular(sc, timeout=900)
        others[s] = ("OTHER 1" in r)
        print(f"  CONTROL: do the same 7 equations force F({s})=0? "
              f"{others[s]}  (False expected: the certificate is specific)")
    out["control_other_constants"] = others

    with open(os.path.join(HERE, "results_t1d_certificate.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote results_t1d_certificate.json")


if __name__ == "__main__":
    main()
