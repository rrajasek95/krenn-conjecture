"""W37 witness decider -- UNAUDITED probe lane (2026-08-20).

Decides, for a pair (p,q) of a source, whether an ADMISSIBLE cap K exists
with E_pq(K) = 0:  K_00 K_11 K_22 != 0, s = <K,A_pq> != 0.

Two routes, both exact:
  (S)  Singular:  ideal( E_w ) + (s - 1) + (t*k00*k11*k22 - 1), test unit.
       (E is homogeneous of degree h in K, so the slice s = 1 loses nothing
        on {s != 0}: the scaling K -> lam K acts transitively on each line.)
  (L)  a cheap structured/random cap SEARCH (one-sided: can only find
       witnesses, never prove BLOCKED).  Used as the positive screen and as
       the ledger-13(b)/18 explicit-point control.

Hazard compliance: ledger 6/11 (parse stdout for '?'), 13 (zzg-prefixed
generator names + no-shadow guard), 22 (denominators cleared before
emission), 19/23 (multi-characteristic re-decision; three-way outcomes).
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import os
import random
import re
import subprocess
import tempfile

import w37_core as C

NCOL = 3
KV = [f"zzk{i}{j}" for i in range(NCOL) for j in range(NCOL)]


# ------------------------------------------------------------------ Singular

class SingularError(RuntimeError):
    pass


def run_singular(script, timeout=900):
    bad = [v for v in ("zzt",) + tuple(KV) if False]
    del bad
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        os.unlink(path)
        return None, "TIMEOUT"
    finally:
        if os.path.exists(path):
            os.unlink(path)
    out = proc.stdout
    for line in out.splitlines():
        if line.strip().startswith("?"):
            raise SingularError(line.strip() + "\n---\n" + out[:2000])
    return out, "OK"


_ASSIGN = re.compile(r"^\s*(?:poly|ideal|int|number|list|matrix)\s+([A-Za-z_]\w*)")


def no_shadow_guard(script, ringvars):
    """Ledger 13(a): no generator may be named after a ring variable."""
    bad = []
    for line in script.splitlines():
        m = _ASSIGN.match(line)
        if m and m.group(1) in ringvars:
            bad.append(line.strip())
    if bad:
        raise SingularError("SHADOWING: " + "; ".join(bad))
    return True


def clear_denoms(polys):
    """Ledger 22: multiply out denominators (E is homogeneous in the blocks,
    so a global rescale changes no verdict)."""
    out = []
    for w, f in polys:
        den = 1
        for c in f.values():
            fr = Fraction(c)
            den = den * fr.denominator // _gcd(den, fr.denominator)
        out.append((w, {e: int(Fraction(c) * den) for e, c in f.items()}))
    return out


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _mon(e):
    parts = [f"{KV[i]}^{k}" if k > 1 else KV[i] for i, k in enumerate(e) if k]
    return "*".join(parts) if parts else "1"


def _poly_txt(f):
    if not f:
        return "0"
    terms = []
    for e, c in sorted(f.items()):
        c = int(c)
        terms.append(("+" if c > 0 else "-") + f"{abs(c)}*{_mon(e)}")
    txt = "".join(terms)
    return txt[1:] if txt.startswith("+") else txt


def singular_decide(src, p, q, sites, char=0, timeout=900, extra_zero=(),
                    ncol=NCOL):
    """Return ('WITNESS'|'BLOCKED'|'UNCHECKED', detail).

    extra_zero: iterable of words on B whose H value is to be TREATED AS
    ZERO (the counterfactual X_k-cleaning experiment).  Implemented by
    subtracting the corresponding term from the W22-M form -- see
    run_a1_falsifier.py.
    """
    polys, s = C.sym_cap_system(src, p, q, sites, ncol)
    if extra_zero:
        raise ValueError("use sym_cap_system_cleaned for the counterfactual")
    polys = clear_denoms(polys)
    sden = 1
    for c in s.values():
        fr = Fraction(c)
        sden = sden * fr.denominator // _gcd(sden, fr.denominator)
    sint = {e: int(Fraction(c) * sden) for e, c in s.items()}
    gens = [_poly_txt(f) for _, f in polys if f]
    gens.append(_poly_txt(sint) + "-" + str(sden))
    gens.append("zzt*" + KV[0] + "*" + KV[4] + "*" + KV[8] + "-1")
    ringvars = KV + ["zzt"]
    script = "\n".join([
        f"ring zzR = {char},({','.join(ringvars)}),dp;",
        "ideal zzI = " + ",\n  ".join(gens) + ";",
        "ideal zzG = std(zzI);",
        'if (dim(zzG) == -1) { "VERDICT:BLOCKED"; } '
        'else { "VERDICT:WITNESS"; }',
        '"DIM:", dim(zzG);',
    ])
    no_shadow_guard(script, set(ringvars))
    out, status = run_singular(script, timeout)
    if status == "TIMEOUT":
        return "UNCHECKED", {"reason": "singular timeout", "char": char}
    if "VERDICT:BLOCKED" in out:
        return "BLOCKED", {"char": char, "raw": out.strip()[-200:]}
    if "VERDICT:WITNESS" in out:
        return "WITNESS", {"char": char, "raw": out.strip()[-200:]}
    return "UNCHECKED", {"reason": "no verdict line", "raw": out[:500]}


# ---------------------------------------------------------------- cap search

def _cap_family(seed=0, extra=()):
    """A structured cap battery: the identity, the antisymmetric caps of
    W25-U3 (I + E_ab - E_ba), permutation/diagonal caps, small integer caps,
    then randoms.  One-sided: finding a cap PROVES witness."""
    caps = []
    idm = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    caps.append([row[:] for row in idm])
    for a, b in combinations(range(3), 2):
        for sgn in (1, -1):
            K = [row[:] for row in idm]
            K[a][b] += sgn
            K[b][a] -= sgn
            caps.append(K)
    for d in product((1, -1, 2, -2), repeat=3):
        K = [[0] * 3 for _ in range(3)]
        for c in range(3):
            K[c][c] = d[c]
        caps.append(K)
    for a, b in product(range(3), repeat=2):
        if a == b:
            continue
        for val in (1, -1, 2, -2, Fraction(1, 2)):
            K = [row[:] for row in idm]
            K[a][b] = val
            caps.append(K)
    for a, b in combinations(range(3), 2):
        for c, d in combinations(range(3), 2):
            for s1 in (1, -1):
                for s2 in (1, -1):
                    K = [row[:] for row in idm]
                    K[a][b] += s1
                    K[b][a] -= s1
                    K[c][d] += s2
                    K[d][c] -= s2
                    caps.append(K)
    caps.extend(extra)
    rng = random.Random(seed)
    for _ in range(600):
        K = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
        for c in range(3):
            if K[c][c] == 0:
                K[c][c] = Fraction(rng.choice([1, -1, 2, -2]))
        caps.append(K)
    return caps


def search_witness(src, p, q, sites, seed=0, extra=(), ncol=NCOL):
    """One-sided witness search.  Returns (K, n_tried) or (None, n_tried)."""
    n_tried = 0
    for K in _cap_family(seed, extra):
        if not C.admissible(src, p, q, K, ncol):
            continue
        n_tried += 1
        if not C.cap_error_def(src, p, q, K, sites, ncol):
            return K, n_tried
    return None, n_tried


def decide_pair(src, p, q, sites=None, chars=(0,), timeout=900, seed=0,
                ncol=NCOL, do_search=True):
    """Full decision with the multi-characteristic re-decision of ledger 19."""
    n = C.sites_of(src)
    if sites is None:
        sites = tuple(x for x in range(n) if x not in (p, q))
    res = {"pair": [p, q], "sites": list(sites)}
    if do_search:
        K, tried = search_witness(src, p, q, sites, seed, ncol=ncol)
        res["search_tried"] = tried
        if K is not None:
            res["verdict"] = "WITNESS"
            res["cap"] = [[str(x) for x in row] for row in K]
            res["route"] = "search"
            return res
    verdicts = {}
    for ch in chars:
        v, d = singular_decide(src, p, q, sites, char=ch, timeout=timeout,
                               ncol=ncol)
        verdicts[str(ch)] = v
        res.setdefault("detail", {})[str(ch)] = d
    res["by_char"] = verdicts
    v0 = verdicts.get("0")
    res["verdict"] = v0 if v0 else list(verdicts.values())[0]
    res["route"] = "singular"
    return res
