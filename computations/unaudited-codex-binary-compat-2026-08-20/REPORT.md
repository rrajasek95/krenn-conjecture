# Three-binary compatibility audit — COUNTEREXAMPLE (UNAUDITED)

**Verdict.** The proposed standalone route

> three exact binary restrictions on palettes `01`, `02`, and `12` cannot
> share their pure layers

is false.  The W40/T3a point extends to an explicit four-dimensional Laurent
family of compatible exact binary triples.  The family even satisfies every
level-4 ternary equation at `N=8`; it fails exactly three genuinely
trichromatic `(3,3,2)` equations.  Thus binary compatibility, by itself,
cannot close the ternary problem.

Status: **UNAUDITED COUNTEREXAMPLE / symbolic probe**, not a certified-spine
result.  Nothing here claims a fully exact ternary source.

## 1. Exact original-cell compatibility condition

Let `B^01`, `B^02`, `B^12` be endpoint-ordered `2 x 2` principal blocks on
every edge `uv`.  They have a common `3 x 3` cellwise amalgam `A_uv` if and
only if, on every edge,

```
B^01_uv[0,0] = B^02_uv[0,0],
B^01_uv[1,1] = B^12_uv[1,1],
B^02_uv[2,2] = B^12_uv[2,2].
```

These are the complete overlap conditions: two distinct principal binary
blocks intersect in only the pure cell of their shared colour.  Subject to
the 84 displayed equalities (three per edge), the amalgam is unique: its
pure cells are the shared values, while `A_uv[a,b]` for `a != b` is the
corresponding cell of `B^ab`.  No auxiliary `B/Eq` or null-graph object is
involved.

Each binary block is exact precisely when, for its two-colour words,

```
sum_{M perfect matching of K8} product_{uv in M} B^ab_uv[w_u,w_v]
    = 1  if w is constant,
    = 0  otherwise.
```

These equations say nothing about amplitudes of words containing all three
colours.  That logical gap is realised, rather than merely possible, by the
family below.

## 2. Four-parameter counterfamily

Work over `Z[s^+-1,t^+-1,a^+-1,b^+-1]`.  Begin with the W33-D5 twisted `4+4`
`01` source:

```
A01[0,0]=A23[0,0]=A45[0,0]=A67[0,0]=1
A03[1,1]=A12[1,1]=A47[1,1]=A56[1,1]=1
A04[0,1]=A05[1,0]=1
A17[0,1]=A34[1,0]=-1.
```

Add the following cells and leave every unlisted cell zero:

```
A12[0,2]=A24[2,1]=s,
A06[0,2]=A67[2,1]=t,
A04[2,2]=a,
A13[2,2]=b,
A26[2,2]=-s*t,
A57[2,2]=-1/(a*b*s*t).
```

The parameters occur as literal cells, so this is an embedded four-torus,
not a dimension count inferred from a tangent calculation.  Direct symbolic
perfect-matching expansion gives:

- all `3 * 2^8 = 768` binary word equations exactly;
- all 4,881 ternary words in the level-4 system exactly;
- only the following three full-exactness failures:

```
w=01110222: H_w = 1/(s*a*b),
w=12221000: H_w = s*b,
w=20002111: H_w = -a.
```

All have profile `(3,3,2)` and are nonzero everywhere on the parameter
torus.  Consequently this family cannot itself specialize to a fully exact
ternary source, but it decisively refutes binary incompatibility as a
standalone theorem.

## 3. Controls and evidence

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  computations/unaudited-codex-binary-compat-2026-08-20/audit_binary_compat.py
```

The executed manifest in `results.json` records:

1. exact equality of all 252 cells with W40's stored integral point;
2. symbolic raw matching checks of all 768 binary equations;
3. symbolic raw matching checks of all 4,881 level-4 equations;
4. a positive object passing all 84 overlap equalities and reaching the full
   checker, with exact reconstruction of the original `A_uv` source;
5. a rational point `(s,t,a,b)=(1,1,1,1)` checked on all 6,561 words by both
   explicit 105-perfect-matching enumeration and an independent recursive
   hafnian engine;
6. a must-fire mutation breaking one shared pure equality;
7. a must-fire mutation breaking binary exactness.

Every declared control executed.  The proof of the family is over an
integer Laurent ring, so the conclusion over `Q/C` is not inferred from a
finite-field experiment.

Primary artifact: `results.json`.  Source: `audit_binary_compat.py`.

## 4. Consequence for the attack plan

Kill the theorem “pairwise exact binary restrictions with shared pure layers
are incompatible.”  A viable binary-projection route must use additional
trichromatic information.  For `N=8`, the sharp remaining interface visible
here is the `(3,3,2)` layer: even binary exactness plus every off-count-at-most
4 equation leaves exactly these uncancelled amplitudes on this adversarial
family.  Any successor lemma should therefore name and use `(3,3,2)`
equations explicitly; null-graph or shared-pure-layer data alone are
insufficient.

## Provenance

The family was translated from W40/T3a into original cells and then checked
by the standalone script above.  Read-only inputs:

```
30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f  W40/results_t3.json
a54e7ca117409ff4424f6186eec11a1bc55ce805d31b9a9ce50b1c7c7ba9e044  W40/run_03_x4point.py
0a9559ac37f7b28ee7e5a0b591e7a41d0b756f4f7bb1526217c54e516ed2ab3c  W40/w40_core.py
f48243576129f91082e596f2ec99b2575eac10e5f6638e91e5b024d213f3ca7b  W33/REPORT.md
```
