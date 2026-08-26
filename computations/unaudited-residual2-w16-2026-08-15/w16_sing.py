#!/usr/bin/env python3
"""W16 -- Singular harness with the A4 trap guards.

TRAPS GUARDED (A4, plan v24):
  * Singular prints errors on stdout and STILL RETURNS 0.  Every run is
    scanned for lines beginning with '?' (and for 'error occurred');
    any hit raises -- a silent wrong SAT/0 verdict is impossible here.
  * `ideal S = sat(I,J)[1];` takes the first GENERATOR.  Never used;
    the helper below emits `list LL = sat(I,J); ideal S = LL[1];`.
  * Singular 4.4 reserves the identifiers e1, mult, I (and a leading
    unary '+' is a parse error).  All emitted variable names are of the
    form z<k>/uu, all emitted polynomials start with a term, never '+'.
"""
from __future__ import annotations
import os, subprocess, tempfile
from fractions import Fraction


class SingularError(RuntimeError):
    pass


def check_no_shadowing(varnames, gennames):
    """HAZARD (found the hard way): declaring `poly g11 = ...` in a ring that
    HAS a variable named g11 silently rebinds the identifier, corrupting every
    later polynomial that mentions it -- with NO error message.  Always guard."""
    clash = sorted(set(varnames) & set(gennames))
    if clash:
        raise SingularError("generator names shadow ring variables: %s"
                            % clash[:10])


def run_singular(script, timeout=900):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script)
        path = fh.name
    try:
        p = subprocess.run(["Singular", "-q", "--no-warn", path],
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        os.unlink(path)
        return None, "TIMEOUT"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    out = p.stdout + p.stderr
    bad = [ln for ln in out.splitlines()
           if ln.strip().startswith("?") or "error occurred" in ln
           or "halt" in ln.lower() and "?" in ln]
    if bad:
        raise SingularError("Singular reported errors:\n" + "\n".join(bad[:8])
                            + "\n--- full output ---\n" + out[:4000])
    return out, "OK"


def poly_str(poly, names):
    """poly = {monomial tuple -> Fraction}; names = {varid -> string}."""
    if not poly:
        return "0"
    terms = []
    for mon, c in sorted(poly.items()):
        assert Fraction(c).denominator == 1, "non-integer coefficient"
        num = int(c)
        s = "+" if num > 0 else "-"
        if abs(num) != 1 or not mon:
            s += str(abs(num))
            if mon:
                s += "*"
        s += "*".join(names[v] for v in mon)
        terms.append(s)
    out = "".join(terms)
    return out[1:] if out.startswith("+") else out       # no leading unary +


def unit_ideal_test(eqs, nonvanish, varids, timeout=900, extra_lines=()):
    """Rabinowitsch: is  {eqs = 0} & {each p in nonvanish != 0}  EMPTY over
    the algebraic closure of Q?   Returns True (empty / infeasible), False
    (feasible), or None (timeout)."""
    names = {v: "z%d" % i for i, v in enumerate(sorted(varids))}
    ring = ",".join(names[v] for v in sorted(varids))
    lines = ["ring r = 0,(%s,uu),dp;" % ring]
    for i, p in enumerate(eqs, 1):
        lines.append("poly q%d = %s;" % (i, poly_str(p, names)))
    prod = "*".join("(%s)" % poly_str(p, names) for p in nonvanish)
    gens = ",".join("q%d" % i for i in range(1, len(eqs) + 1))
    lines.append("ideal Jid = %s,uu*(%s)-1;" % (gens, prod))
    lines.extend(extra_lines)
    lines.append("ideal GB = groebner(Jid);")
    lines.append('"UNIT:"; (GB[1]==1);')
    lines.append("quit;")
    out, st = run_singular("\n".join(lines) + "\n", timeout=timeout)
    if st == "TIMEOUT":
        return None
    tail = out.split("UNIT:")[1].strip().split()[0]
    return tail == "1"
