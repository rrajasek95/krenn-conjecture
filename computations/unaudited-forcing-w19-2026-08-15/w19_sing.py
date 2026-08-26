#!/usr/bin/env python3
"""W19 -- Singular harness with the mandatory guards (conventions 6, 11,
13, 14).

  * Singular prints errors on stdout and STILL RETURNS 0 -> every run is
    scanned for lines starting with '?' and for 'error occurred'.
  * `ideal S = sat(I,J)[1];` takes the first GENERATOR -> always use the
    list form  `list LL = sat(I,J); ideal S = LL[1];`.
  * `LIB "elim.lib";` is required before sat.
  * SEVERE (ledger item 13): naming a polynomial after a RING VARIABLE
    silently rebinds the identifier and manufactures FALSE KILLS.  Every
    emitted script must be passed through check_no_shadowing().
  * Reserved identifiers in Singular 4.4: e1, mult, I; a leading unary '+'
    is a parse error.
"""
from __future__ import annotations
import os
import subprocess
import tempfile
from fractions import Fraction

RESERVED = {"e1", "mult", "I", "L", "M", "N", "T", "R", "Z", "Q", "std",
            "reduce", "ideal", "poly", "ring", "int", "list", "matrix",
            "sat", "groebner", "quit", "if", "else", "for", "while",
            "return", "def", "number", "vector", "module", "map", "proc"}


class SingularError(RuntimeError):
    pass


def check_no_shadowing(varnames, gennames):
    clash = sorted(set(varnames) & set(gennames))
    if clash:
        raise SingularError("generator names shadow ring variables: %s"
                            % clash[:10])
    bad = sorted(set(varnames) & RESERVED) + sorted(set(gennames) & RESERVED)
    if bad:
        raise SingularError("reserved Singular identifiers used: %s" % bad[:10])


def run_singular(script, timeout=900):
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


def poly_str(poly, names):
    """poly = {monomial tuple -> Fraction}; names = {varid -> string}."""
    if not poly:
        return "0"
    terms = []
    for mon, c in sorted(poly.items()):
        c = Fraction(c)
        num, den = c.numerator, c.denominator
        s = "+" if num > 0 else "-"
        s += str(abs(num))
        if den != 1:
            s += "/" + str(den)
        if mon:
            s += "*" + "*".join(names[v] for v in mon)
        terms.append(s)
    out = "".join(terms)
    return out[1:] if out.startswith("+") else out
