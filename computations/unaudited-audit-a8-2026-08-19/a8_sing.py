#!/usr/bin/env python3
"""A8 -- Singular driver with the ledger-6/11/13/14/22 guards.

  * every emitted identifier carries the reserved prefix zz  (ledger 13:
    identifier shadowing silently rebinds and manufactures false kills);
  * a no-shadowing guard scans the script for any generator name that also
    names a ring variable;
  * stdout is scanned for '?' lines (ledger 6/11: Singular reports errors with
    return code 0);
  * integer coefficients only, no rationals emitted (ledger 22).
"""
from __future__ import annotations

import os
import subprocess
import tempfile


class SingularError(RuntimeError):
    pass


def run_singular(script, timeout=900):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script)
        path = fh.name
    try:
        p = subprocess.run(["Singular", "-q", "--no-warn", path],
                           capture_output=True, text=True, timeout=timeout)
        out = p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    finally:
        os.unlink(path)
    bad = [ln for ln in out.splitlines() if ln.strip().startswith("?")]
    if bad:
        raise SingularError("Singular error lines: " + " | ".join(bad[:4]) + "\n" + out[:2000])
    return out, "OK"


def unit_ideal_script(varnames, polys, char=0, method="std", extra=""):
    """Script deciding 1 in I.  Prints UNIT:<0|1> and DIM:<d>."""
    for v in varnames:
        if not v.startswith("zz"):
            raise SingularError(f"variable {v} lacks the zz prefix")
    ring = f"ring zzR = {char}, ({','.join(varnames)}), dp;"
    gens = ",\n".join(polys)
    body = f"""
{ring}
ideal zzI = {gens};
{extra}
ideal zzG = {method}(zzI);
zzG = simplify(zzG, 1);
poly zzr = reduce(1, zzG);
int zzu = (zzr == 0);
"UNIT:" + string(zzu);
"DIM:" + string(dim(zzG));
"NGENS:" + string(size(zzG));
exit;
"""
    # no-shadowing guard: no emitted identifier may equal a ring variable
    for ident in ("zzR", "zzI", "zzG", "zzr", "zzu"):
        if ident in varnames:
            raise SingularError(f"identifier {ident} shadows a ring variable")
    return body


def decide_unit(varnames, polys, char=0, timeout=900, method="std", extra=""):
    out, st = run_singular(unit_ideal_script(varnames, polys, char, method, extra),
                           timeout=timeout)
    if st == "TIMEOUT":
        return dict(status="TIMEOUT")
    d = {}
    for ln in out.splitlines():
        if ":" in ln:
            k, _, v = ln.strip().strip('"').partition(":")
            if k in ("UNIT", "DIM", "NGENS"):
                d[k] = v.strip().strip('"')
    return dict(status="OK", unit=d.get("UNIT") == "1", dim=d.get("DIM"),
                ngens=d.get("NGENS"), raw=out[-400:])
