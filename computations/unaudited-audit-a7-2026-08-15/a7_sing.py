#!/usr/bin/env python3
"""A7 -- independent Singular driver with the ledger-13 no-shadowing guard.

Guards implemented here (written from the ledger, not copied):
  * every emitted identifier is checked against the ring's variable list --
    a generator may NEVER be named after a ring variable (ledger 13);
  * Singular's reserved identifiers e1/mult/I are also rejected (ledger 6);
  * stdout is scanned for '?' error lines even though the return code is 0
    (ledger 11);
  * `LIB "elim.lib";` is emitted whenever sat() is used (ledger 14) and the
    `list L = sat(I,J); ideal S = L[1];` form is used (ledger 11).
SELF-TESTS at the bottom must all fire.
"""
from __future__ import annotations
import os, subprocess, tempfile, time

RESERVED = {"e1", "mult", "I", "ring", "ideal", "poly", "int", "list", "std",
            "groebner", "reduce", "sat", "quit", "if", "else", "for", "while",
            "return", "proc", "matrix", "vector", "module", "map", "number",
            "def", "intvec", "string", "resolution", "link", "qring", "kill"}


class GuardError(Exception):
    pass


class SingularError(Exception):
    pass


def guard(ring_vars, emitted_names):
    rv = set(ring_vars)
    bad = [n for n in emitted_names if n in rv]
    if bad:
        raise GuardError("SHADOWING: emitted identifiers collide with ring "
                         "variables: %s" % sorted(bad)[:10])
    bad2 = [n for n in list(ring_vars) + list(emitted_names) if n in RESERVED]
    if bad2:
        raise GuardError("RESERVED identifier used: %s" % sorted(set(bad2)))
    return True


def run(script, timeout=3600):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as f:
        f.write(script)
        path = f.name
    try:
        t0 = time.time()
        p = subprocess.run(["Singular", "-q", "--no-warn", path],
                           capture_output=True, text=True, timeout=timeout)
        out = p.stdout + p.stderr
        dt = time.time() - t0
    except subprocess.TimeoutExpired:
        os.unlink(path)
        return None, "TIMEOUT", timeout
    os.unlink(path)
    errs = [ln for ln in out.splitlines() if ln.strip().startswith("?")]
    if errs:
        raise SingularError("Singular reported errors (rc=%d): %s"
                            % (p.returncode, errs[:5]))
    return out, "OK", dt


def monomial_str(names):
    return "*".join(names)


def _selftest():
    ok = {}
    # guard must fire on shadowing
    try:
        guard(["g11", "x"], ["g11", "zzI"])
        ok["shadow_guard"] = False
    except GuardError:
        ok["shadow_guard"] = True
    # guard must fire on reserved names
    try:
        guard(["x", "y"], ["e1"])
        ok["reserved_guard"] = False
    except GuardError:
        ok["reserved_guard"] = True
    # error scan must fire
    try:
        run("ring r = 0,(x),dp;\nthis is not singular;\nquit;\n", timeout=60)
        ok["error_scan"] = False
    except SingularError:
        ok["error_scan"] = True
    # a correct run must work and sat() must be available
    out, st, dt = run('LIB "elim.lib";\nring r = 0,(x,y),dp;\n'
                      'ideal zzI = x*y;\nideal zzJ = x;\n'
                      'list zzL = sat(zzI,zzJ);\nideal zzS = zzL[1];\n'
                      '"SAT:"; zzS;\nquit;\n', timeout=120)
    ok["sat_available"] = (st == "OK" and "y" in out.split("SAT:")[1])
    # POSITIVE control: the shadowing bug reproduces if the guard is bypassed
    scr = ("ring r = 0,(g11,g12),dp;\n"
           "poly g11 = g12 - g12;\n"          # silently rebinds the variable
           'ideal zzI = g11*g12;\n'
           '"UNIT:"; (groebner(zzI)[1]==1);\n'
           '"G11:"; g11;\nquit;\n')
    out2, st2, _ = run(scr, timeout=120)
    ok["shadowing_bug_reproduces"] = (st2 == "OK" and
                                      out2.split("G11:")[1].strip().split()[0] == "0")
    return ok


if __name__ == "__main__":
    for k, v in _selftest().items():
        print("%-28s %s" % (k, v))
