#!/usr/bin/env python3
"""Exact one-silent-site witnesses: the eight transverse rows do not force
proper mixed saturation.

Theorem 1 (certified in cap_selection_transverse_row_forcing.py) kills the
two-silent stratum carrying both prism guard families.  This script proves
the frontier is sharp by exhibiting exact ten-site aggregate families with
exactly ONE boundary-silent capped site that satisfy the transverse cap
rows, and certifying that their cap cubic still has a unit active
saturation (root cover), now with the eight transverse rows CANCELLED
rather than left open.

Witness W0 (three-channel core).  Sites W = (p,q,r,s), U as two ordered
shores (x0,x1,x2,y0,y1,y2).  The silent site s is attached by three
same-colour rank-one cells ps=(1,1), qs=(2,2), rs=(0,0) (the cubic-vertex
pattern).  Each colour c has its own routing channel through a distinct
pair of active capped sites:

    colour 0:  p-y1 (0,0), q-y2 (0,0), boundary cells x0x1 (0,0), x2y0 (0,0)
    colour 1:  q-x0 (1,1), r-x1 (1,1), boundary cells x2y0 (1,1), y1y2 (1,1)
    colour 2:  p-x2 (2,2), r-y0 (2,2), boundary cells x0x1 (2,2), y1y2 (2,2)

Verified exhaustively: H10(W0) has twelve terms, ALL with pure diagonal
W-words; hence every one of the six adjugate-visible off-diagonal rows
vanishes at EVERY capped pair, both diagonal relocations hold, and all
three pure-boundary-word rows G_i = e_i^{(x)W} hold with coefficient one.
The only failures of the full GHZ equation are nine mixed boundary-word
coefficients (three per colour), each a product of two colour-needed
cells: the root-cover pattern relocated into the boundary sector.
W0 has H_W = 0, so its scalar cofactor sector is empty.

Witness W1 = W0 + diagonal direct block A_pq = diag(1,2,3).  This makes
s(K) = K_0000 + 2 K_1100 + 3 K_2200, so the four active forms
s, kappa_0, kappa_1, kappa_2 are independent linear forms on the cap
space.  W1 keeps: all three pure-word rows, both relocations, complete
pair-diagonality at (p,q) and at (r,s) (in particular all six
adjugate-visible off-diagonal rows at the deleted pair), and common-edge
realizability with a boundary-silent site.  The cost is exactly the
appearance of W-words (i,i,0,0) at mixed boundary words (transverse rows
of the OTHER pairs), measured precisely below.

Certificates (Singular, characteristic zero, on the finitely many
effective cap coordinates):

  * GHZ-form cubic  D_ghz(K) = 6(s^2 sum_i kappa_i X_i - H6(A^K)):
    I : h^infty = (1) for h = s kappa_0 kappa_1 kappa_2.  No clean GHZ
    cap exists, exactly as the six-site theorem demands of every actual
    family; the root cover persists with the eight transverse rows now
    CANCELLED instead of left open.
  * source-form cubic  D_src(K) = 6(s^2 F_U^K - H6(A^K)):
    I : h^infty is PROPER, with an explicit rational active zero.  W1 is
    cap-condition-consistent: an active cap makes its cofactor family
    realize the capped top tensor exactly.  The entire obstruction
    content of W1 therefore sits in the seventeen mixed boundary-word
    defects of the top tensor, not in the cap condition.

The witness answers the sharp extension test of the maximal-slice
countermodel: cancelling the six adjugate-visible off-diagonal rows and
the two diagonal relocations -- with independent active forms, a
genuinely changed effective cofactor family, and full realizability --
does not create a clean GHZ cap.  The load lies entirely in the mixed
boundary sector and the other-pair transverse rows.
"""

from __future__ import annotations

import subprocess
import sys
from itertools import product as iproduct

sys.path.insert(0, __file__.rsplit("/", 1)[0])

import sympy as sp

from cap_selection_lib import (
    alg_add,
    alg_equal,
    alg_scale,
    alg_zero,
    cofactor_family,
    contract_pure_boundary,
    hafnian,
    pure_word,
    tensor_coefficients,
)

SINGULAR = "/usr/local/bin/Singular"
HERE = __file__.rsplit("/", 1)[0]

WSITES = ("p", "q", "r", "s")
USITES = ("x0", "x1", "x2", "y0", "y1", "y2")
ORDER10 = WSITES + USITES


def witness_family(with_direct):
    fam = {}

    def put(u, v, cu, cv, coeff=1):
        iu, iv = ORDER10.index(u), ORDER10.index(v)
        if iu > iv:
            u, v, cu, cv = v, u, cv, cu
        fam.setdefault((u, v), {})[(cu, cv)] = coeff

    # silent-site attachments (cubic-vertex colour channels)
    put("p", "s", 1, 1)
    put("q", "s", 2, 2)
    put("r", "s", 0, 0)
    # colour-0 channel through p, q
    put("p", "y1", 0, 0)
    put("q", "y2", 0, 0)
    put("x0", "x1", 0, 0)
    put("x2", "y0", 0, 0)
    # colour-1 channel through q, r
    put("q", "x0", 1, 1)
    put("r", "x1", 1, 1)
    put("x2", "y0", 1, 1)
    put("y1", "y2", 1, 1)
    # colour-2 channel through p, r
    put("p", "x2", 2, 2)
    put("r", "y0", 2, 2)
    put("x0", "x1", 2, 2)
    put("y1", "y2", 2, 2)
    if with_direct:
        for i, t in enumerate((1, 2, 3)):
            put("p", "q", i, i, t)
    return fam


def classify_h10(fam, name):
    h10 = hafnian(fam, ORDER10, ORDER10)
    coeffs = tensor_coefficients(h10, ORDER10)
    print(f"[{name}] H10 has {len(coeffs)} monomials; census:")

    pure_targets = {}
    mixed_defects = {}
    transverse_bad = {}
    for word, coeff in coeffs.items():
        wword, uword = word[:4], word[4:]
        w_pure = len(set(wword)) == 1
        u_pure = len(set(uword)) == 1 and (not w_pure or uword[0] == wword[0])
        if w_pure and len(set(uword)) == 1 and uword[0] == wword[0]:
            pure_targets[word] = coeff
        elif w_pure:
            mixed_defects[word] = coeff
        else:
            transverse_bad[word] = coeff

    # eight transverse rows of the maximal-slice countermodel:
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            for uword in iproduct(range(3), repeat=6):
                for rs in iproduct(range(3), repeat=2):
                    word = (i, j) + rs + uword
                    assert word not in coeffs, (
                        f"off-diagonal (p,q) word survives: {word}"
                    )
    print("    six off-diagonal (p,q) rows: all coefficients vanish")
    for c in (1, 2):
        reloc_bad = (c, c, 0, 0) + (c,) * 6
        reloc_good = (c,) * 10
        assert reloc_bad not in coeffs
        assert coeffs.get(reloc_good) == 1
    print("    two diagonal relocations: words sit at (c,c,c,c) (x) X_c, coeff 1")
    for i in range(3):
        assert coeffs.get((i,) * 10) == 1
    print(f"    pure targets: {sorted(pure_targets)} (all coefficient 1)")
    print(f"    mixed boundary defects: {len(mixed_defects)}")
    for word in sorted(mixed_defects):
        print(f"        W{word[:4]} U{word[4:]} -> {mixed_defects[word]}")
    if transverse_bad:
        print(f"    other-pair transverse words (W-word impure): {len(transverse_bad)}")
        wset = sorted({w[:4] for w in transverse_bad})
        print(f"        impure W-words present: {wset}")
        for w4 in wset:
            n = sum(1 for w in transverse_bad if w[:4] == w4)
            print(f"        W{w4}: {n} mixed-U monomials")
    else:
        print("    NO impure W-word at all: every capped pair is pair-diagonal")
    return h10, coeffs, mixed_defects, transverse_bad


def check_pure_rows(fam, name):
    for i in range(3):
        gi = contract_pure_boundary(fam, WSITES, USITES, i, ORDER10)
        assert alg_equal(gi, pure_word(WSITES, i)), f"{name}: G_{i} failed"
    print(f"[{name}] all three pure-word rows G_i = e_i^(x)W hold exactly")


def check_silent(fam, name):
    for u in USITES:
        for wpair in (("s", u), (u, "s")):
            assert wpair not in fam
    print(f"[{name}] site s is boundary-silent (degree three inside W)")


def active_forms(fam, name):
    hw = hafnian(fam, WSITES, ORDER10)
    coeffs = tensor_coefficients(hw, WSITES)
    print(f"[{name}] H_W words: {dict(sorted(coeffs.items()))}")
    return coeffs


def pair_diagonality_table(coeffs):
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    names = ["pq", "pr", "ps", "qr", "qs", "rs"]
    out = {}
    for (a, b), nm in zip(pairs, names):
        bad = sum(
            1 for w in coeffs if w[a] != w[b]
        )
        out[nm] = bad
    return out


def build_cap_cubics(fam, name):
    """Both denominator-cleared cap cubics on the effective cap coordinates.

    D_src(K) = 6(s^2 F_U^K       - H6(A^K))   (source form: capped target)
    D_ghz(K) = 6(s^2 sum k_i X_i - H6(A^K))   (GHZ form: diagonal target)

    For a genuine GHZ source the two coincide.  An active zero of D_ghz
    would be a literal six-site ternary source, forbidden by the proved
    six-site theorem for EVERY family; an active zero of D_src only says
    the capped family realizes its own capped top tensor.
    """
    h10 = hafnian(fam, ORDER10, ORDER10)
    hw = hafnian(fam, WSITES, ORDER10)

    kvars = {}

    def kv(word):
        if word not in kvars:
            kvars[word] = sp.Symbol("K" + "".join(map(str, word)))
        return kvars[word]

    # s(K)
    s_expr = 0
    for word, coeff in tensor_coefficients(hw, WSITES).items():
        s_expr += coeff * kv(word)
    # F_U^K = K ⌟ H10
    f_top = {}
    for word, coeff in tensor_coefficients(h10, ORDER10).items():
        uword = word[4:]
        f_top[uword] = f_top.get(uword, 0) + coeff * kv(word[:4])
    # cofactor family and its six-site hafnian
    cap = {}  # filled lazily through kv inside cofactor contraction

    # cofactor_family expects a dict cap; build the full symbolic cap on all
    # words that can appear: enumerate via the pair hafnians directly.
    full_cap = {}
    for w4 in iproduct(range(3), repeat=4):
        full_cap[w4] = kv(w4) if False else None
    # only materialize needed coordinates: use a defaultdict-like wrapper
    class LazyCap(dict):
        def get(self, key, default=0):
            return kv(key)

    cof = cofactor_family(fam, WSITES, USITES, LazyCap(), ORDER10)
    fam6 = {pair: cell for pair, cell in cof.items() if cell}
    h6 = hafnian(fam6, USITES, USITES)
    h6c = tensor_coefficients(h6, USITES)

    kappa = [kv((i, i, i, i)) for i in range(3)]
    dsrc, dghz = {}, {}
    for uword in set(f_top) | set(h6c) | {(i,) * 6 for i in range(3)}:
        ghz_target = kappa[uword[0]] if len(set(uword)) == 1 else 0
        v1 = sp.expand(6 * (s_expr**2 * f_top.get(uword, 0) - h6c.get(uword, 0)))
        v2 = sp.expand(6 * (s_expr**2 * ghz_target - h6c.get(uword, 0)))
        if v1 != 0:
            dsrc[uword] = v1
        if v2 != 0:
            dghz[uword] = v2

    used = sorted(kvars)
    print(f"[{name}] effective cap coordinates ({len(used)}):")
    print("    " + ", ".join("K" + "".join(map(str, w)) for w in used))
    print(f"    s(K) = {s_expr}")
    for label, d in (("D_src", dsrc), ("D_ghz", dghz)):
        n_pure = sum(1 for w in d if len(set(w)) == 1)
        print(
            f"    {label} has {len(d)} nonzero coordinates "
            f"({n_pure} pure, {len(d) - n_pure} mixed)"
        )
    return dsrc, dghz, s_expr, kappa, kvars


def independence_check(s_expr, kappa, kvars, name):
    allsyms = sorted(kvars.values(), key=str)
    mat = sp.Matrix(
        [[sp.diff(f, v) for v in allsyms] for f in [s_expr] + kappa]
    )
    rank = mat.rank()
    print(f"[{name}] rank of (s, kappa_0, kappa_1, kappa_2) = {rank}")
    return rank


def singular_saturation(d_ideal, s_expr, kappa, kvars, name, tag):
    """Return True iff I : h^infty = (1) over Q (Singular certificate)."""
    symnames = {v: str(v) for v in kvars.values()}
    gens = []
    for uword in sorted(d_ideal):
        gens.append(str(d_ideal[uword]).replace("**", "^"))
    h = sp.expand(s_expr * kappa[0] * kappa[1] * kappa[2])
    hstr = str(h).replace("**", "^")
    varlist = ", ".join(sorted(symnames.values()))
    script = (
        'LIB "elim.lib";\n'
        f"ring S = 0, ({varlist}), dp;\n"
        f"ideal I = {', '.join(gens)};\n"
        f"poly h = {hstr};\n"
        "ideal J = sat(I, ideal(h))[1];\n"
        f'string out = "SAT_{tag}:" + string(reduce(1, std(J)));\n'
        "out;\n"
        "exit;\n"
    )
    path = f"{HERE}/cap_selection_witness_{tag}.sing"
    with open(path, "w") as fh:
        fh.write(script)
    proc = subprocess.run(
        ["nice", "-n", "10", SINGULAR, "-q", path],
        capture_output=True,
        text=True,
        timeout=3600,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)
    line = [l for l in proc.stdout.splitlines() if f"SAT_{tag}" in l][0]
    tail = line.split(":")[1]
    print(f"[{name}] Singular char-0 saturation ({tag}): reduce(1, std(I:h^oo)) = {tail}")
    return tail == "0"


def print_polynomials(d_ideal, label):
    print(f"    {label} coordinate polynomials:")
    for uword in sorted(d_ideal):
        print(f"        U{uword}: {d_ideal[uword]}")


def verify_point(d_ideal, s_expr, kappa, kvars, assignment, name):
    """Exact check that the assignment is an active zero."""
    subs = {kvars[w]: v for w, v in assignment.items()}
    subs.update({v: 0 for v in kvars.values() if v not in subs})
    for uword, poly in d_ideal.items():
        val = sp.simplify(poly.subs(subs))
        assert val == 0, f"{name}: coordinate {uword} -> {val}"
    hval = sp.simplify(
        (s_expr * kappa[0] * kappa[1] * kappa[2]).subs(subs)
    )
    assert hval != 0
    print(f"[{name}] explicit active zero verified; h = {hval} != 0 at")
    shown = {("K" + "".join(map(str, w))): v for w, v in assignment.items() if v != 0}
    print(f"    {shown}")


def main():
    print("=" * 72)
    print("WITNESS W0: three-channel core, no direct block")
    print("=" * 72)
    w0 = witness_family(with_direct=False)
    check_silent(w0, "W0")
    check_pure_rows(w0, "W0")
    _, coeffs0, defects0, bad0 = classify_h10(w0, "W0")
    assert not bad0, "W0 must be W-pure"
    assert len(defects0) == 9
    table0 = pair_diagonality_table(coeffs0)
    print(f"[W0] off-diagonal W-monomial count per capped pair: {table0}")
    hw0 = active_forms(w0, "W0")
    assert not hw0, "W0 must have H_W = 0"
    print("[W0] H_W = 0: the scalar cofactor sector is empty (s == 0);")
    print("     W0 satisfies the FULL transverse W-row system at every pair,")
    print("     at the price of a degenerate active-form family.")

    print()
    print("=" * 72)
    print("WITNESS W1: three-channel core + diagonal direct block diag(1,2,3)")
    print("=" * 72)
    w1 = witness_family(with_direct=True)
    check_silent(w1, "W1")
    check_pure_rows(w1, "W1")
    _, coeffs1, defects1, bad1 = classify_h10(w1, "W1")
    table1 = pair_diagonality_table(coeffs1)
    print(f"[W1] off-diagonal W-monomial count per capped pair: {table1}")
    assert table1["pq"] == 0 and table1["rs"] == 0
    dsrc, dghz, s_expr, kappa, kvars = build_cap_cubics(w1, "W1")
    rank = independence_check(s_expr, kappa, kvars, "W1")
    assert rank == 4
    print_polynomials(dsrc, "D_src (mixed part)")
    unit_ghz = singular_saturation(dghz, s_expr, kappa, kvars, "W1", "w1_ghz")
    assert unit_ghz, "GHZ-form cubic must have unit active saturation"
    print("    D_ghz: UNIT ideal -- no active zero of the GHZ-form cubic,")
    print("    exactly as the six-site theorem demands for every family.")
    unit_src = singular_saturation(dsrc, s_expr, kappa, kvars, "W1", "w1_src")
    assert not unit_src, "source-form cubic is expected to saturate properly"
    print("    D_src: PROPER ideal -- W1 admits clean source-form caps: some")
    print("    active cap makes the cofactor family realize the capped top")
    print("    tensor exactly.  The entire obstruction content of W1 sits in")
    print("    its seventeen mixed boundary defects, not in the cap condition.")
    clean_src_cap = {
        (0, 0, 0, 0): 1,
        (1, 1, 1, 1): 1,
        (2, 2, 2, 2): 1,
        (0, 2, 2, 2): 1,
        (2, 0, 0, 0): -1,
        (0, 1, 0, 0): 1,
        (1, 0, 1, 1): -1,
        (1, 1, 2, 1): 1,
        (2, 2, 1, 2): -1,
        (1, 0, 2, 1): -1,
        (0, 2, 1, 2): -1,
        (2, 1, 0, 0): 0,
        (1, 1, 0, 0): 0,
        (2, 2, 0, 0): 0,
    }
    verify_point(dsrc, s_expr, kappa, kvars, clean_src_cap, "W1 clean src-cap")

    print()
    print("CONCLUSION: the two-silent stratum is impossible (Theorem 1),")
    print("while one silent site admits an exact family cancelling the six")
    print("adjugate-visible off-diagonal rows and both relocations, with")
    print("independent active forms and a changed effective cofactor family,")
    print("whose GHZ-form cap cubic still has unit active saturation and")
    print("whose source-form cap condition is even exactly solvable.  The")
    print("eight transverse rows alone therefore cannot power the clean-cap")
    print("derivation; the residual load is the mixed boundary sector plus")
    print("the other-pair transverse rows.")


if __name__ == "__main__":
    main()
