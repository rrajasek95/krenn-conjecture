"""realroot -- certified real-root counting for zero-dimensional ideals over Q.

PERMANENT ENGINE MODULE.  Built for W39 (MUB(6)) but deliberately generic:
the only input is a list of polynomial generators over Q in named variables.

WHY IT EXISTS.  The campaign's standard verdict is "the ideal is the unit
ideal over ZZ, hence infeasible over any field".  That instrument is blind
to problems whose objects are the REAL points of a NONEMPTY zero-dimensional
scheme (MUB(6) is exactly such a problem: the MU-vector ideal has vdim 156 /
162 and is never unit).  This module supplies the missing verdict.

THEORY (Hermite 1856; Basu-Pollack-Roy, "Algorithms in Real Algebraic
Geometry", Thm 4.100).  Let I be zero-dimensional in Q[x_1..x_n], and
A = Q[x]/I with monomial basis B = {b_1..b_D} (D = vdim).  Let Tr(a) denote
the trace of the multiplication endomorphism m_a of A.  Define the symmetric
bilinear form
        H[i][j] = Tr(m_{b_i b_j}).
Then
        rank(H)      = number of DISTINCT complex points of V(I),
        signature(H) = number of DISTINCT real points of V(I).
Both are counts WITHOUT multiplicity (unlike vdim).

VIEWS (two-view discipline, ledger 26).  Two INDEPENDENT computations of the
real-point count must agree before any number is reported:
  VIEW A (this file, primary): trace form assembled here from bulk normal
          forms, then exact rational LDL^T with symmetric pivoting.
  VIEW B (cross-check): Singular's rootsmr.lib matbil/symsignature.
          NB rootsur.lib SHADOWS rootsmr.lib's `nrroots` -- the library-level
          instance of hazard ledger 13.  Never call `nrroots`; call
          `matbil(poly(1), kbase(g), g)` then `symsignature`.
  VIEW C (optional, for isolation as well as counting): certified interval
          root isolation, rootisolation.lib.

DISCIPLINE.  Exact rational arithmetic everywhere (fractions.Fraction); no
floating point anywhere in the verdict path.  Singular is used only as a
Groebner/normal-form engine; every number it returns is re-derived here.
Callers must check `ok` and `singular_error_lines` (hazards 6/11).
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from fractions import Fraction

SINGULAR = "Singular"


# --------------------------------------------------------------------------
# Singular driver
# --------------------------------------------------------------------------
def _run_singular(script: str, timeout: int, workdir: str, name: str):
    path = os.path.join(workdir, name)
    with open(path, "w") as fh:
        fh.write(script)
    try:
        p = subprocess.run([SINGULAR, "-q", path], capture_output=True,
                           text=True, timeout=timeout)
        out, rc, to = p.stdout, p.returncode, False
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        rc, to = -1, True
    errs = [l for l in out.splitlines() if l.strip().startswith("?")]
    return {"stdout": out, "returncode": rc, "timeout": to,
            "singular_error_lines": errs, "script_path": path}


def _emit_dump(gens, variables, dumpfile, order="dp"):
    """Singular script: std, kbase, and a BULK reduction of all products
    b_i*b_j (i<=j) written one polynomial per line to `dumpfile`."""
    v = ",".join(variables)
    L = [f'ring zzR = 0,({v}),{order};',
         "option(redSB);",
         "ideal zzI = " + ",".join(f"({g})" for g in gens) + ";",
         "ideal zzG = std(zzI);",
         'if (zzG[1]==1) { "ZZSTATUS UNIT"; quit; }',
         "int zzdim = dim(zzG);",
         'if (zzdim != 0) { "ZZSTATUS NOTZERODIM"; string(zzdim); quit; }',
         "ideal zzB = kbase(zzG);",
         "int zzD = size(zzB);",
         '"ZZSTATUS OK";',
         '"ZZD"; string(zzD);',
         '"ZZVDIM"; string(vdim(zzG));',
         '"ZZBASIS";',
         "int zzi, zzj;",
         "for (zzi=1; zzi<=zzD; zzi++) { string(zzB[zzi]); }",
         # bulk products, reduced elementwise by std basis (C level)
         "ideal zzP;",
         "int zzc = 0;",
         "for (zzi=1; zzi<=zzD; zzi++) { for (zzj=zzi; zzj<=zzD; zzj++) "
         "{ zzc = zzc+1; zzP[zzc] = zzB[zzi]*zzB[zzj]; } }",
         "ideal zzN = reduce(zzP, zzG);",
         f'link zzL = ":w {dumpfile}"; ',
         "for (zzi=1; zzi<=zzc; zzi++) { write(zzL, string(zzN[zzi])); }",
         "close(zzL);",
         '"ZZDONE"; string(zzc);',
         "quit;"]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------
# exact polynomial-string parsing (no eval, no floats)
# --------------------------------------------------------------------------
def _parse_terms(s: str):
    """Parse a Singular polynomial string into [(coeff Fraction, monomial str)].
    Monomial string is the canonical Singular monomial with coefficient
    stripped, e.g. 'x^2*y'.  '0' -> []."""
    s = s.strip().replace(" ", "")
    if s in ("", "0"):
        return []
    # split on top-level +/- (Singular never emits parentheses in normal forms)
    parts, cur, i = [], "", 0
    while i < len(s):
        ch = s[i]
        if ch in "+-" and i > 0 and s[i - 1] not in "^*/(":
            parts.append(cur)
            cur = ch
        else:
            cur += ch
        i += 1
    parts.append(cur)
    out = []
    for p in parts:
        if not p:
            continue
        sign = Fraction(1)
        if p[0] == "+":
            p = p[1:]
        elif p[0] == "-":
            sign = Fraction(-1)
            p = p[1:]
        factors = p.split("*")
        coeff = sign
        mon = []
        for f in factors:
            if not f:
                continue
            if "/" in f and not any(c.isalpha() for c in f):
                num, den = f.split("/")
                coeff *= Fraction(int(num), int(den))
            elif f.replace("^", "").isdigit() and not any(c.isalpha() for c in f):
                if "^" in f:
                    b, e = f.split("^")
                    coeff *= Fraction(int(b)) ** int(e)
                else:
                    coeff *= Fraction(int(f))
            else:
                mon.append(f)
        out.append((coeff, "*".join(mon) if mon else "1"))
    return out


# --------------------------------------------------------------------------
# exact rank / signature of a rational symmetric matrix
# --------------------------------------------------------------------------
def rank_signature(H):
    """Exact rank and signature of a symmetric matrix of Fractions, by
    symmetric Gaussian reduction (congruence).  Handles zero diagonal with the
    standard 2x2 hyperbolic step, which contributes (+1,-1) to the signature.

    Returns (rank, signature, n_pos, n_neg).
    """
    n = len(H)
    A = [row[:] for row in H]
    idx = list(range(n))
    pos = neg = 0
    size = n
    while size > 0:
        # find a nonzero diagonal entry among the active block
        piv = -1
        for i in range(size):
            if A[i][i] != 0:
                piv = i
                break
        if piv >= 0:
            # move pivot to position 0
            if piv != 0:
                A[0], A[piv] = A[piv], A[0]
                for r in range(size):
                    A[r][0], A[r][piv] = A[r][piv], A[r][0]
            d = A[0][0]
            if d > 0:
                pos += 1
            else:
                neg += 1
            for i in range(1, size):
                f = A[i][0] / d
                if f != 0:
                    for j in range(1, size):
                        A[i][j] -= f * A[0][j]
            A = [row[1:size] for row in A[1:size]]
            size -= 1
            continue
        # all diagonal entries zero: look for a nonzero off-diagonal
        found = None
        for i in range(size):
            for j in range(i + 1, size):
                if A[i][j] != 0:
                    found = (i, j)
                    break
            if found:
                break
        if found is None:
            break                       # remaining block is identically zero
        i, j = found
        # congruence e_i -> e_i + e_j makes the (i,i) entry 2*A[i][j] != 0
        for k in range(size):
            A[i][k] = A[i][k] + A[j][k]
        for k in range(size):
            A[k][i] = A[k][i] + A[k][j]
        # loop continues; the pivot branch will now fire
    return pos + neg, pos - neg, pos, neg


# --------------------------------------------------------------------------
# main entry point -- VIEW A
# --------------------------------------------------------------------------
def real_root_count(gens, variables, workdir=None, timeout=3000, tag="job",
                    order="dp", keep=False):
    """Certified count of the DISTINCT real points of V(gens) over Q.

    Returns a dict with keys: ok, status, D (vdim), n_distinct_complex (=rank),
    n_real (=signature), plus diagnostics.  `status` is one of
    'OK' | 'UNIT' | 'NOTZERODIM' | 'SINGULAR_ERROR' | 'TIMEOUT'.
    """
    own = workdir is None
    workdir = workdir or tempfile.mkdtemp(prefix="realroot_")
    dumpfile = os.path.join(workdir, f"{tag}_nf.txt")
    if os.path.exists(dumpfile):
        os.remove(dumpfile)
    script = _emit_dump(gens, variables, dumpfile, order=order)
    r = _run_singular(script, timeout, workdir, f"{tag}_dump.sing")
    res = {"tag": tag, "singular_error_lines": r["singular_error_lines"],
           "returncode": r["returncode"], "timeout": r["timeout"],
           "workdir": workdir}
    if r["timeout"]:
        res.update(ok=False, status="TIMEOUT")
        return res
    if r["singular_error_lines"]:
        res.update(ok=False, status="SINGULAR_ERROR")
        return res
    out = r["stdout"].splitlines()
    txt = [l.strip() for l in out if l.strip()]
    if "ZZSTATUS UNIT" in txt:
        res.update(ok=True, status="UNIT", D=0, n_distinct_complex=0, n_real=0)
        return res
    if "ZZSTATUS NOTZERODIM" in txt:
        res.update(ok=False, status="NOTZERODIM")
        return res
    if "ZZSTATUS OK" not in txt:
        res.update(ok=False, status="NO_STATUS")
        return res
    i = txt.index("ZZD")
    D = int(txt[i + 1])
    vd = int(txt[txt.index("ZZVDIM") + 1])
    bstart = txt.index("ZZBASIS") + 1
    basis = txt[bstart:bstart + D]
    index = {m: k for k, m in enumerate(basis)}
    if len(index) != D:
        res.update(ok=False, status="BASIS_NOT_DISTINCT")
        return res

    # pass 1: trace vector  t_k = sum_i coeff_{b_i}( NF(b_k * b_i) )
    t = [Fraction(0)] * D
    with open(dumpfile) as fh:
        c = 0
        for i_ in range(D):
            for j_ in range(i_, D):
                line = fh.readline()
                c += 1
                terms = _parse_terms(line)
                if i_ == j_:
                    for coeff, mon in terms:
                        if index.get(mon) == i_:
                            t[i_] += coeff
                else:
                    for coeff, mon in terms:
                        k = index.get(mon)
                        if k == i_:
                            t[j_] += coeff     # diagonal (j_,j_) of m_{b_i}
                        if k == j_:
                            t[i_] += coeff     # diagonal (i_,i_) of m_{b_j}
    # pass 2: Hermite matrix
    H = [[Fraction(0)] * D for _ in range(D)]
    with open(dumpfile) as fh:
        for i_ in range(D):
            for j_ in range(i_, D):
                line = fh.readline()
                s = Fraction(0)
                for coeff, mon in _parse_terms(line):
                    k = index.get(mon)
                    if k is not None and t[k]:
                        s += coeff * t[k]
                H[i_][j_] = s
                H[j_][i_] = s
    rank, sig, npos, nneg = rank_signature(H)
    if not keep and own:
        pass
    res.update(ok=True, status="OK", D=D, vdim=vd, n_products=c,
               n_distinct_complex=rank, n_real=sig, n_pos=npos, n_neg=nneg)
    return res


# --------------------------------------------------------------------------
# VIEW B -- independent cross-check via Singular's rootsmr.lib
# --------------------------------------------------------------------------
def real_root_count_view_b(gens, variables, workdir=None, timeout=3000,
                           tag="jobB", order="dp"):
    """Cross-check using rootsmr.lib matbil/symsignature.

    HAZARD: rootsur.lib (auto-loaded by rootsmr.lib) redefines `nrroots` with
    an incompatible signature -- ledger 13 at library scope.  We never call
    `nrroots`; matbil/symsignature are unaffected.
    """
    workdir = workdir or tempfile.mkdtemp(prefix="realrootB_")
    v = ",".join(variables)
    L = ['LIB "rootsmr.lib";',
         f'ring zzR = 0,({v}),{order};',
         "option(redSB);",
         "ideal zzI = " + ",".join(f"({g})" for g in gens) + ";",
         "ideal zzG = std(zzI);",
         'if (zzG[1]==1) { "ZZSTATUS UNIT"; quit; }',
         'if (dim(zzG)!=0) { "ZZSTATUS NOTZERODIM"; quit; }',
         "ideal zzB = kbase(zzG);",
         "matrix zzM = matbil(poly(1), zzB, zzG);",
         '"ZZSTATUS OK";',
         '"ZZVDIM"; string(vdim(zzG));',
         '"ZZRANK"; string(nrows(zzM));',
         '"ZZSIG"; string(symsignature(zzM));',
         "quit;"]
    r = _run_singular("\n".join(L) + "\n", timeout, workdir, f"{tag}.sing")
    txt = [l.strip() for l in r["stdout"].splitlines() if l.strip()
           and not l.strip().startswith("// **")]
    res = {"tag": tag, "singular_error_lines": r["singular_error_lines"],
           "timeout": r["timeout"], "returncode": r["returncode"]}
    if r["timeout"]:
        res.update(ok=False, status="TIMEOUT")
        return res
    if "ZZSTATUS UNIT" in txt:
        res.update(ok=True, status="UNIT", n_real=0)
        return res
    if "ZZSTATUS OK" not in txt:
        res.update(ok=False, status="NO_STATUS", stdout_tail=txt[-8:])
        return res
    res.update(ok=True, status="OK",
               vdim=int(txt[txt.index("ZZVDIM") + 1]),
               n_real=int(txt[txt.index("ZZSIG") + 1]))
    return res
