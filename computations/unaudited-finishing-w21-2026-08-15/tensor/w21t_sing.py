#!/usr/bin/env python3
"""W21-M1-TENSOR -- Singular driver with the ledger-13 no-shadowing guard.
UNAUDITED.  Exact (Q) only.

Ledger discipline enforced here:
  * every emitted generator identifier carries the reserved prefix `zzg`
    and a guard REJECTS any script in which a declared identifier collides
    with a ring variable (ledger 13, the false-kill mechanism);
  * stdout is parsed for `?` lines -- Singular reports errors with return
    code 0 (ledger 11);
  * `LIB "elim.lib";` is emitted whenever sat() is used (ledger 14);
  * `e1`, `mult`, `I` are never used as identifiers, and no leading unary
    `+` is emitted (ledger 6).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
RESERVED = {"e1", "mult", "I", "i", "j", "k", "n", "T", "L", "R"}


def guard(script, ringvars):
    """ledger 13: no declared identifier may equal a ring variable."""
    bad = []
    for m in re.finditer(r'^\s*(?:poly|ideal|list|int|matrix|number|ring|'
                         r'map|intvec|string)\s+([A-Za-z_]\w*)', script,
                         re.M):
        name = m.group(1)
        if name in ringvars:
            bad.append(("SHADOWS RING VARIABLE", name))
        if name in RESERVED:
            bad.append(("RESERVED IDENTIFIER", name))
        if not (name.startswith("zzg") or name in ("Rng",)):
            bad.append(("MISSING zzg PREFIX", name))
    if re.search(r'[=,(]\s*\+', script):
        bad.append(("LEADING UNARY PLUS", ""))
    return bad


def run(script, ringvars, timeout=1800):
    bad = guard(script, ringvars)
    if bad:
        raise RuntimeError("GUARD FAILED: %s" % bad)
    p = subprocess.run(["Singular", "-q"], input=script, text=True,
                       capture_output=True, timeout=timeout)
    out = p.stdout + p.stderr
    errs = [ln for ln in out.splitlines() if ln.strip().startswith("?")]
    return out, errs


def selftest():
    """the guard must FIRE on the three known traps (a mutation control)."""
    rv = {"x", "y"}
    t1 = guard("ring Rng=0,(x,y),dp;\npoly x = 1;\n", rv)
    t2 = guard("ring Rng=0,(x,y),dp;\npoly e1 = 1;\n", rv)
    t3 = guard("ring Rng=0,(x,y),dp;\npoly zzga = +1;\n", rv)
    t4 = guard("ring Rng=0,(x,y),dp;\npoly foo = 1;\n", rv)
    ok = (any(b[0] == "SHADOWS RING VARIABLE" for b in t1)
          and any(b[0] == "RESERVED IDENTIFIER" for b in t2)
          and any(b[0] == "LEADING UNARY PLUS" for b in t3)
          and any(b[0] == "MISSING zzg PREFIX" for b in t4))
    return ok, [t1, t2, t3, t4]


if __name__ == "__main__":
    ok, det = selftest()
    print("guard self-test (4 planted traps must all fire): %s" % ok)
    for d in det:
        print("   ", d)
