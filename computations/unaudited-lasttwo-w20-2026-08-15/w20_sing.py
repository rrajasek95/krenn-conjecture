#!/usr/bin/env python3
"""W20 -- Singular harness with the MANDATORY guards (conventions 5,6,11,
13,14).  UNAUDITED.

  * Singular prints errors on stdout and STILL RETURNS 0  -> every run is
    scanned for lines starting with '?' and for 'error occurred'  (item 11).
  * `LIB "elim.lib";` is required before sat                    (item 14).
  * `list LL = sat(I,J); ideal S = LL[1];` (never `sat(...)[1]`) (item 11).
  * SEVERE (item 13): naming a polynomial after a RING VARIABLE silently
    rebinds it and manufactures FALSE KILLS.  Every emitted script is passed
    through check_script(), which (a) refuses generator names clashing with
    ring variables, (b) RE-SCANS THE FINAL TEXT: every `poly X =` / `ideal
    X =` / `int X =` / `list X =` declaration in the script must use a
    zz-prefixed name, and no ring variable may be zz-prefixed.
"""
from __future__ import annotations

import os
import re
import subprocess
import tempfile

RESERVED = {"e1", "mult", "I", "L", "M", "N", "T", "R", "Z", "Q", "std",
            "reduce", "ideal", "poly", "ring", "int", "list", "matrix",
            "sat", "groebner", "quit", "if", "else", "for", "while",
            "return", "def", "number", "vector", "module", "map", "proc",
            "size", "nvars", "var", "gen", "kill", "system", "option"}

DECL = re.compile(r"^\s*(poly|ideal|int|list|matrix|number|intvec|ring|map)"
                  r"\s+([A-Za-z_][A-Za-z_0-9]*)\s*=")


class SingularError(RuntimeError):
    pass


def check_script(script, varnames):
    """the no-shadowing guard, applied to the FINAL EMITTED TEXT."""
    vs = set(varnames)
    bad = sorted(vs & RESERVED)
    if bad:
        raise SingularError("ring variables use reserved identifiers: %s" % bad)
    zz = sorted(v for v in vs if v.startswith("zz"))
    if zz:
        raise SingularError("ring variables are zz-prefixed: %s" % zz[:8])
    for ln in script.splitlines():
        m = DECL.match(ln)
        if not m:
            continue
        kind, nm = m.group(1), m.group(2)
        if kind == "ring":
            continue
        if nm in vs:
            raise SingularError("SHADOWING: declaration `%s %s =` collides "
                                "with a ring variable" % (kind, nm))
        if not nm.startswith("zz"):
            raise SingularError("declaration `%s %s =` is not zz-prefixed"
                                % (kind, nm))
        if nm in RESERVED:
            raise SingularError("reserved identifier declared: %s" % nm)
    return True


def run_singular(script, varnames, timeout=1800):
    check_script(script, varnames)
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script)
        path = fh.name
    try:
        p = subprocess.run(["Singular", "-q", "--no-warn", path],
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    out = p.stdout + p.stderr
    bad = [ln for ln in out.splitlines()
           if ln.strip().startswith("?") or "error occurred" in ln]
    if bad:
        raise SingularError("Singular reported errors:\n" + "\n".join(bad[:8])
                            + "\n--- output ---\n" + out[:3000])
    return out, "OK"


def head(varnames, order="dp", char=0):
    return ['LIB "elim.lib";',
            "ring zzr = %d,(%s),%s;" % (char, ",".join(varnames), order)]


def sat_ideal(gens_name, nonzero_prod):
    """emit the saturation block, list form (item 11)."""
    return ["poly zzP = %s;" % nonzero_prod,
            "ideal zzJ = zzP;",
            "list zzL = sat(%s,zzJ);" % gens_name,
            "ideal zzS = zzL[1];"]


def guard_selftest():
    """POSITIVE CONTROL for the guard: a shadowing script must be refused."""
    ok = {}
    good = "\n".join(head(["a", "b"]) + ["poly zzg1 = a*b;", "quit;"])
    ok["good_accepted"] = check_script(good, ["a", "b"])
    bad = "\n".join(head(["a", "b"]) + ["poly a = a*b;", "quit;"])
    try:
        check_script(bad, ["a", "b"])
        ok["shadow_refused"] = False
    except SingularError:
        ok["shadow_refused"] = True
    bad2 = "\n".join(head(["a", "b"]) + ["poly g1 = a*b;", "quit;"])
    try:
        check_script(bad2, ["a", "b"])
        ok["unprefixed_refused"] = False
    except SingularError:
        ok["unprefixed_refused"] = True
    try:
        check_script(good, ["zza", "b"])
        ok["zzvar_refused"] = False
    except SingularError:
        ok["zzvar_refused"] = True
    # and a live run whose stdout carries a '?' error must raise
    try:
        run_singular("\n".join(head(["a"]) + ["nosuchproc(1);", "quit;"]), ["a"])
        ok["stdout_error_caught"] = False
    except SingularError:
        ok["stdout_error_caught"] = True
    return ok


if __name__ == "__main__":
    print(guard_selftest())
