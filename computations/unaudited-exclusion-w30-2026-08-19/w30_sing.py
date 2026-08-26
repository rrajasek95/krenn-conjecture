#!/usr/bin/env python3
"""W30 SINGULAR HARNESS.  UNAUDITED.  Exact only.

Full ledger discipline, enforced here so no caller can skip it:
  * every user identifier is zz-prefixed (ledger 13);
  * a NO-SHADOWING GUARD runs over every emitted script -- no generator name
    may collide with a ring variable (ledger 13, the W16 false-kill);
  * stdout is parsed for '?' lines because Singular returns 0 on error
    (ledger 6/11);
  * LIB "elim.lib" is emitted before any sat, and sat is used in the LIST
    form  list zzL = sat(I,J); ideal zzS = zzL[1];  (ledger 11/14);
  * all coefficients are integers -- callers must clear denominators before
    emission (ledger 22; sound here because every generator is homogeneous
    in the block cells);
  * char 0 AND two primes = 1 mod 3 (ledger 19).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PRIMES = (13, 31)                       # both = 1 mod 3 (ledger 19)


class ShadowError(Exception):
    pass


def guard_no_shadow(script, varnames):
    """ledger 13: a declaration `poly zzg = ...` whose name is a RING
    VARIABLE silently rebinds it, with no error and return code 0."""
    bad = []
    for mm in re.finditer(r'\b(?:poly|ideal|matrix|number|int|list|def)\s+'
                          r'([A-Za-z_][A-Za-z_0-9]*)', script):
        nm = mm.group(1)
        if nm in varnames:
            bad.append(nm)
        if not nm.startswith("zz"):
            bad.append("NON_ZZ:" + nm)
    if bad:
        raise ShadowError("shadowing/naming violations: %s" % sorted(set(bad)))
    return True


def run(script, varnames, timeout=1800):
    """emit, guard, run, and parse stdout for '?' error lines."""
    guard_no_shadow(script, varnames)
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False,
                                     dir=HERE) as fh:
        fh.write(script)
        path = fh.name
    try:
        pr = subprocess.run(["Singular", "-q", "--no-warn", path],
                            capture_output=True, text=True, timeout=timeout)
        out = pr.stdout
        err = pr.stderr
    except subprocess.TimeoutExpired:
        return dict(ok=False, timeout=True, stdout="", qlines=[],
                    note="TIMEOUT after %ds" % timeout)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    q = [ln for ln in out.splitlines() if ln.lstrip().startswith("?")]
    q += [ln for ln in err.splitlines() if ln.lstrip().startswith("?")]
    return dict(ok=(not q), timeout=False, stdout=out, stderr=err, qlines=q)


def ringdecl(ch, varnames, order="dp"):
    return "ring zzr = %s,(%s),%s;\n" % (ch, ",".join(varnames), order)


def sat_and_test(idealname, satname):
    """emit the LIST-form saturation + the unit-ideal test."""
    return ("list zzL = sat(%s, %s);\n"
            "ideal zzS = zzL[1];\n"
            "zzS = std(zzS);\n"
            "int zzunit = (size(zzS) == 1 and leadmonom(zzS[1]) == 1);\n"
            "\"UNIT=\", zzunit;\n"
            "\"DIMENSION=\", dim(zzS);\n"
            "\"NGENS=\", size(zzS);\n" % (idealname, satname))


def selftest():
    """the harness's own controls: the guard must FIRE on a shadowing
    script, must PASS a clean one, and sat/list must behave."""
    res = {}
    vs = ["zzx", "zzy"]
    try:
        guard_no_shadow("poly zzx = 1;", vs)
        res["guard_fires_on_shadow"] = False
    except ShadowError:
        res["guard_fires_on_shadow"] = True
    try:
        guard_no_shadow("poly zzg1 = 1;", vs)
        res["guard_passes_clean"] = True
    except ShadowError:
        res["guard_passes_clean"] = False
    try:
        guard_no_shadow("poly g1 = 1;", vs)
        res["guard_fires_on_non_zz"] = False
    except ShadowError:
        res["guard_fires_on_non_zz"] = True
    # a script Singular rejects, to prove the '?'-parse works (rc is 0)
    r = run('LIB "elim.lib";\nring zzr=0,(zzx),dp;\npoly zzg1 = +zzx;\n'
            'quit;\n', ["zzx"])
    res["qparse_catches_unary_plus"] = (not r["ok"]) and bool(r["qlines"])
    # positive: a genuinely unit ideal
    r2 = run('LIB "elim.lib";\nring zzr=0,(zzx,zzy),dp;\n'
             'ideal zzi = zzx, zzx-1;\nideal zzs = std(zzi);\n'
             '"UNIT=", (size(zzs)==1 and leadmonom(zzs[1])==1);\nquit;\n',
             ["zzx", "zzy"])
    res["unit_detect"] = ("UNIT= 1" in r2["stdout"].replace("  ", " "))
    # negative: a non-unit ideal must NOT be reported unit
    r3 = run('LIB "elim.lib";\nring zzr=0,(zzx,zzy),dp;\n'
             'ideal zzi = zzx*zzy;\nideal zzs = std(zzi);\n'
             '"UNIT=", (size(zzs)==1 and leadmonom(zzs[1])==1);\nquit;\n',
             ["zzx", "zzy"])
    res["nonunit_detect"] = ("UNIT= 0" in r3["stdout"].replace("  ", " "))
    # sat in LIST form
    r4 = run('LIB "elim.lib";\nring zzr=0,(zzx,zzy),dp;\n'
             'ideal zzi = zzx*zzy;\nlist zzL = sat(zzi, ideal(zzy));\n'
             'ideal zzs = zzL[1];\n"SAT=", zzs;\nquit;\n', ["zzx", "zzy"])
    res["sat_list_form"] = ("zzx" in r4["stdout"])
    return res


if __name__ == "__main__":
    import json
    r = selftest()
    print(json.dumps(r, indent=1))
    assert all(r.values()), "HARNESS SELFTEST FAILED: %s" % r
    print("HARNESS SELFTEST OK")
