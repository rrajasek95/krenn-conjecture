#!/usr/bin/env python3
"""What the transverse pure-word cap rows force at ten sites.

Main results certified here (all characteristic zero, all exact):

THEOREM 1 (boundary-silent capped pair exclusion).  Let A be ANY ten-site
aggregate family, U a six-set, W = {p, q, r, s}.  Suppose the two extra
capped sites r, s are boundary-silent: A_ru = A_su = 0 for every u in U.
Then the three pure-boundary-word transverse rows

    G_i := iota_{U, i^6} H_10(A) = e_i^{(x) W}      (i = 0, 1, 2)

are inconsistent.  Both prism guard families (the four-parameter barrier
and the maximal transverse prism cap slice) are boundary-silent at
{r, s}, so the entire geometry class carrying the known unit-saturation
root covers is excluded by the pure-word part of the eight transverse
rows alone -- no other GHZ coefficient is used.

The proof is a span argument on the (r, s)-slices of the exact
decomposition (verified in the reconstruction script):

    G_i = theta_i * HW + sum_{j,k} M^{(i)}_{jk} e_j^{(p)} e_k^{(q)} (x) A_rs,

    theta_i   = [X_i] x^[3],
    M^{(i)}_jk = [X_i] (ell_j m_k x^[2]).

Reading only the (p,q)-diagonal slices (j,k) = (c,c), every hypothesis
point satisfies, in V_r (x) V_s:

    theta_i N_cc + M^{(i)}_cc R = [i = c = the diagonal colour] e_i e_i,

with R = A_rs and N_cc the (c,c) slice of the internal W-hafnian tensor.
Case split on the number of nonzero theta_i:
  * >= 2 nonzero: every N_cc lies in span(R), hence every e_i e_i does;
  * exactly 1 nonzero (theta_a): colours b, c != a give
    M^{(b)}_bb R = e_b e_b and M^{(c)}_cc R = e_c e_c;
  * all zero: M^{(i)}_ii R = e_i e_i for all i.
In every case at least two of the independent tensors e_0 e_0, e_1 e_1,
e_2 e_2 lie in the span of the single vector R.  Contradiction.

The machine certificate treats theta, M, a, R and the four W-internal
star rows as FREE variables (a sound weakening: any actual family
satisfying the hypotheses projects onto an abstract solution) and proves
the unit ideal in characteristic zero via Singular, using the four-case
saturation cover {theta_0 != 0}, {theta_1 != 0}, {theta_2 != 0},
{theta = 0}.

THEOREM 2 (no pendant capped site).  Under the same three pure-word rows
(with the other blocks fully arbitrary and NO silence assumption
elsewhere), a capped site of degree at most one in the allowed block
graph is impossible.  Certified for both pendant types (pendant to the
other extra site, pendant to a pair site) by unit-ideal certificates.

Every derivation step (slice decomposition, generator lists) is
re-verified against literal matching enumeration on random exact
families before the Singular certificates are emitted.
"""

from __future__ import annotations

import random
import subprocess
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])

import sympy as sp

from cap_selection_lib import (
    alg_add,
    alg_equal,
    alg_mul,
    alg_scale,
    alg_zero,
    block_element,
    contract_pure_boundary,
    divided_power,
    hafnian,
    pair_chart,
    pure_word,
)

SINGULAR = "/usr/local/bin/Singular"
HERE = __file__.rsplit("/", 1)[0]
RNG = random.Random(31337)

WSITES = ("p", "q", "r", "s")
USITES = ("x0", "x1", "x2", "y0", "y1", "y2")
ORDER10 = WSITES + USITES


# ---------------------------------------------------------------------------
# step 0: re-verify the (r,s)-slice generator shape on random silent data
# ---------------------------------------------------------------------------


def random_family(density=3, zero_pairs=(), span=4, seed=None):
    rng = random.Random(seed) if seed is not None else RNG
    fam = {}
    slist = list(ORDER10)
    for i, u in enumerate(slist):
        for v in slist[i + 1 :]:
            if (u, v) in zero_pairs or (v, u) in zero_pairs:
                continue
            cells = {}
            for _ in range(density):
                cu, cv = rng.randrange(3), rng.randrange(3)
                coeff = rng.randint(-span, span)
                if coeff:
                    cells[(cu, cv)] = cells.get((cu, cv), 0) + coeff
            cells = {k: c for k, c in cells.items() if c != 0}
            if cells:
                fam[(u, v)] = cells
    return fam


def block_matrix(fam, u, v):
    """3x3 matrix of the block, rows = colour at u, cols = colour at v."""
    out = [[0] * 3 for _ in range(3)]
    idx_u, idx_v = ORDER10.index(u), ORDER10.index(v)
    key = (u, v) if idx_u < idx_v else (v, u)
    for (c1, c2), coeff in fam.get(key, {}).items():
        if idx_u < idx_v:
            out[c1][c2] = coeff
        else:
            out[c2][c1] = coeff
    return out


def verify_slice_generators():
    zero_pairs = [("r", u) for u in USITES] + [("s", u) for u in USITES]
    fam = random_family(density=3, zero_pairs=zero_pairs)
    a_mat = block_matrix(fam, "p", "q")
    upr = block_matrix(fam, "p", "r")  # u_{j alpha}
    vqs = block_matrix(fam, "q", "s")  # v_{k beta}
    wps = block_matrix(fam, "p", "s")  # w_{j beta}
    zqr = block_matrix(fam, "q", "r")  # z_{k alpha}
    rrs = block_matrix(fam, "r", "s")  # R_{alpha beta}

    _, ell, mrow, x = pair_chart(fam, "p", "q", USITES, ORDER10)
    x3 = divided_power(x, 3)
    x2 = divided_power(x, 2)
    theta = [x3.get(frozenset((u, i) for u in USITES), 0) for i in range(3)]
    msl = [
        [
            [
                alg_mul(alg_mul(ell[j], mrow[k]), x2).get(
                    frozenset((u, i) for u in USITES), 0
                )
                for k in range(3)
            ]
            for j in range(3)
        ]
        for i in range(3)
    ]

    for i in range(3):
        gi = contract_pure_boundary(fam, WSITES, USITES, i, ORDER10)
        for j in range(3):
            for k in range(3):
                for al in range(3):
                    for be in range(3):
                        got = gi.get(
                            frozenset(
                                {("p", j), ("q", k), ("r", al), ("s", be)}
                            ),
                            0,
                        )
                        njk = (
                            a_mat[j][k] * rrs[al][be]
                            + upr[j][al] * vqs[k][be]
                            + wps[j][be] * zqr[k][al]
                        )
                        pred = theta[i] * njk + msl[i][j][k] * rrs[al][be]
                        assert got == pred, (i, j, k, al, be)
    print("[0] (r,s)-slice generator shape re-verified against literal")
    print("    matching enumeration on a random boundary-silent family")


# ---------------------------------------------------------------------------
# Singular helpers
# ---------------------------------------------------------------------------


def run_singular(script, name):
    path = f"{HERE}/cap_selection_{name}.sing"
    with open(path, "w") as fh:
        fh.write(script)
    proc = subprocess.run(
        ["nice", "-n", "10", SINGULAR, "-q", path],
        capture_output=True,
        text=True,
        timeout=3600,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Singular failed for {name}: {proc.stderr}")
    return proc.stdout.strip().splitlines()


# ---------------------------------------------------------------------------
# THEOREM 1 certificate
# ---------------------------------------------------------------------------


def theorem1_certificates():
    # variables: th(i); em(i)(c)  [= M^{(i)}_cc]; ad(c) [= a_cc];
    # R(a)(b); up(c)(a) [= A_pr row c]; vq(c)(b); wp(c)(b); zq(c)(a)
    thv = [f"th{i}" for i in range(3)]
    emv = [f"em{i}{c}" for i in range(3) for c in range(3)]
    adv = [f"ad{c}" for c in range(3)]
    rv = [f"rc{a}{b}" for a in range(3) for b in range(3)]
    upv = [f"up{c}{a}" for c in range(3) for a in range(3)]
    vqv = [f"vq{c}{b}" for c in range(3) for b in range(3)]
    wpv = [f"wp{c}{b}" for c in range(3) for b in range(3)]
    zqv = [f"zq{c}{a}" for c in range(3) for a in range(3)]
    allvars = thv + emv + adv + rv + upv + vqv + wpv + zqv

    gens = []
    for i in range(3):
        for c in range(3):  # diagonal (p,q)-slice (c,c) only
            for al in range(3):
                for be in range(3):
                    n_cc = (
                        f"(ad{c}*rc{al}{be}"
                        f"+up{c}{al}*vq{c}{be}"
                        f"+wp{c}{be}*zq{c}{al})"
                    )
                    target = 1 if (i == c and al == i and be == i) else 0
                    gens.append(f"th{i}*{n_cc}+em{i}{c}*rc{al}{be}-{target}")

    results = {}

    # stratum theta = 0
    script = (
        f"ring S = 0, ({', '.join(allvars)}), dp;\n"
        f"ideal I = {', '.join(gens)}, th0, th1, th2;\n"
        "ideal J = std(I);\n"
        'string out = "ZERO_STRATUM:" + string(reduce(1, J));\n'
        "out;\n"
        "exit;\n"
    )
    lines = run_singular(script, "thm1_zero_stratum")
    results["theta=0"] = [l for l in lines if "ZERO_STRATUM" in l][0]

    # strata theta_i != 0 via saturation
    for i in range(3):
        script = (
            f"LIB \"elim.lib\";\n"
            f"ring S = 0, ({', '.join(allvars)}), dp;\n"
            f"ideal I = {', '.join(gens)};\n"
            f"ideal J = sat(I, ideal(th{i}))[1];\n"
            f'string out = "SAT_TH{i}:" + string(reduce(1, std(J)));\n'
            "out;\n"
            "exit;\n"
        )
        lines = run_singular(script, f"thm1_sat_th{i}")
        results[f"theta_{i}!=0"] = [l for l in lines if f"SAT_TH{i}" in l][0]

    print("[1] THEOREM 1 characteristic-zero certificates (Singular):")
    for stratum, line in results.items():
        tail = line.split(":")[1]
        verdict = "unit ideal" if tail == "0" else f"FAILED ({tail})"
        print(f"    stratum {stratum:<12} -> reduce(1, std) = {tail} : {verdict}")
        assert tail == "0", f"certificate failed on stratum {stratum}"
    print("    cover: any point has some theta_i != 0 or all theta_i = 0;")
    print("    every stratum is empty, so the abstract system is inconsistent")
    print("    and Theorem 1 follows for every actual boundary-silent family.")


# ---------------------------------------------------------------------------
# THEOREM 2 certificates: pendant capped sites
# ---------------------------------------------------------------------------


def verify_pendant_slices():
    """Re-verify the pendant s-slice decompositions on random data."""
    # pendant to r: s has only the rs block
    zero_pairs = [("s", u) for u in USITES] + [("p", "s"), ("q", "s")]
    fam = random_family(density=3, zero_pairs=zero_pairs, seed=99)
    rrs = block_matrix(fam, "r", "s")
    for i in range(3):
        gi = contract_pure_boundary(fam, WSITES, USITES, i, ORDER10)
        # g_i = pure-word contraction of the 8-site family without r, s
        fam8 = {
            k: v for k, v in fam.items() if "r" not in k and "s" not in k
        }
        g8 = contract_pure_boundary(
            fam8, ("p", "q"), USITES, i, ORDER10
        )
        for al in range(3):
            for be in range(3):
                for j in range(3):
                    for k in range(3):
                        got = gi.get(
                            frozenset(
                                {("p", j), ("q", k), ("r", al), ("s", be)}
                            ),
                            0,
                        )
                        pred = rrs[al][be] * g8.get(
                            frozenset({("p", j), ("q", k)}), 0
                        )
                        assert got == pred
    print("[2a] pendant-to-r slice shape  G_i = g_i (x) A_rs : re-verified")

    # pendant to p: s has only the ps block
    zero_pairs = [("s", u) for u in USITES] + [("r", "s"), ("q", "s")]
    fam = random_family(density=3, zero_pairs=zero_pairs, seed=100)
    wps = block_matrix(fam, "p", "s")
    for i in range(3):
        gi = contract_pure_boundary(fam, WSITES, USITES, i, ORDER10)
        fam8 = {
            k: v for k, v in fam.items() if "p" not in k and "s" not in k
        }
        g8 = contract_pure_boundary(
            fam8, ("q", "r"), USITES, i, ORDER10
        )
        for al in range(3):
            for be in range(3):
                for j in range(3):
                    for k in range(3):
                        got = gi.get(
                            frozenset(
                                {("p", j), ("q", k), ("r", al), ("s", be)}
                            ),
                            0,
                        )
                        pred = wps[j][be] * g8.get(
                            frozenset({("q", k), ("r", al)}), 0
                        )
                        assert got == pred
    print("[2b] pendant-to-p slice shape  G_i = A_ps (x)' g'_i : re-verified")


def theorem2_certificates():
    # pendant to r: R_{al be} * g_i[j k] = [i=al=be=j=k]
    rvars = [f"rc{a}{b}" for a in range(3) for b in range(3)]
    gvars = [f"gg{i}{j}{k}" for i in range(3) for j in range(3) for k in range(3)]
    gens = []
    for i in range(3):
        for al in range(3):
            for be in range(3):
                for j in range(3):
                    for k in range(3):
                        target = 1 if i == al == be == j == k else 0
                        gens.append(f"rc{al}{be}*gg{i}{j}{k}-{target}")
    script = (
        f"ring S = 0, ({', '.join(rvars + gvars)}), dp;\n"
        f"ideal I = {', '.join(gens)};\n"
        "ideal J = std(I);\n"
        'string out = "PENDANT_R:" + string(reduce(1, J));\n'
        "out;\n"
        "exit;\n"
    )
    lines = run_singular(script, "thm2_pendant_r")
    tail = [l for l in lines if "PENDANT_R" in l][0].split(":")[1]
    assert tail == "0"
    print("[2c] pendant-to-r abstract system: unit ideal (Singular, char 0)")

    # pendant to p: w_{j be} * g'_i[k al] = [i=be=j=k=al]
    wvars = [f"wp{j}{b}" for j in range(3) for b in range(3)]
    gpvars = [
        f"gp{i}{k}{a}" for i in range(3) for k in range(3) for a in range(3)
    ]
    gens = []
    for i in range(3):
        for be in range(3):
            for j in range(3):
                for k in range(3):
                    for al in range(3):
                        target = 1 if i == be == j == k == al else 0
                        gens.append(f"wp{j}{be}*gp{i}{k}{al}-{target}")
    script = (
        f"ring S = 0, ({', '.join(wvars + gpvars)}), dp;\n"
        f"ideal I = {', '.join(gens)};\n"
        "ideal J = std(I);\n"
        'string out = "PENDANT_P:" + string(reduce(1, J));\n'
        "out;\n"
        "exit;\n"
    )
    lines = run_singular(script, "thm2_pendant_p")
    tail = [l for l in lines if "PENDANT_P" in l][0].split(":")[1]
    assert tail == "0"
    print("[2d] pendant-to-p abstract system: unit ideal (Singular, char 0)")
    print("    a capped site of degree <= 1 is impossible under the three")
    print("    pure-word rows, with all other blocks fully arbitrary")


def main():
    verify_slice_generators()
    theorem1_certificates()
    verify_pendant_slices()
    theorem2_certificates()
    print("THEOREMS 1 AND 2 FULLY CERTIFIED")


if __name__ == "__main__":
    main()
