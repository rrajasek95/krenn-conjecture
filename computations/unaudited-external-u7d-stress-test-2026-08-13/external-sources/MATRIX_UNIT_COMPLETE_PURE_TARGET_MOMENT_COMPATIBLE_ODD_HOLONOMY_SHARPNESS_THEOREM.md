# Matrix-unit complete pure-target moment-compatible odd-holonomy sharpness

## Status

This is an exact eight-vertex sharpness theorem over `Q`, together with an
exact complex-analytic consequence over `C` from the preceding
[`GHZ moment-balanced gauge theorem`](MATRIX_UNIT_GHZ_MOMENT_BALANCED_GAUGE_AND_UNIT_PHASE_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md).

There is a complete `r=1` matrix-unit table on all `28` physical pairs with
the following simultaneous properties:

1. every physical amplitude is `1` or `-1`;
2. all three pure target coefficients are exactly one, each from a unique
   compatible perfect matching;
3. three active words form the exact three-step binomial transport cycle of
   the preceding
   [`phase-holonomy theorem`](MATRIX_UNIT_PHASE_HOLONOMY_AND_MINIMAL_PURE_COFACTOR_FLOW_REDUCTION_THEOREM.md),
   with invariant holonomy `H=-1=(-1)^3`;
4. the complete endpoint-label support has a strictly positive integral
   balance with common colour loads `(7,7,7)`;
5. all three colour-nonrigidity sets are nonempty and proper; and
6. a different mixed word has one compatible term of weight one.

The strict balance lets the unit-phase table be moved by a positive
GHZ-preserving diagonal gauge to a representative whose **actual squared
physical amplitudes** have vertex-independent colour loads.  That gauge
preserves the three pure coefficients, the three binomial cancellations,
the exact Laurent value `H=-1`, and the nonzero exposed mixed coefficient.

Thus complete physical support, all pure target coordinates, strict
endpoint balance, the actual moment normal form, and proper nonrigidity do
not by themselves exclude odd binomial active holonomy.  Additional mixed
coefficient equations are load-bearing.

The displayed table has a nonzero mixed coefficient and is **not** a
Krenn--Gu witness or counterexample.  It does not realize
`Delta_(8,3)`.  The `r=1` matrix-unit branch and the global Krenn--Gu
conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. Complete matrix-unit table

Use vertices `0,...,7`.  For a physical pair `ij` with `i<j`, write

```text
ij=(ell_i,ell_j;lambda_ij).
```

Take the following complete table:

```text
01=(0,0; 1)  02=(0,0; 1)  03=(0,0; 1)  04=(0,0; 1)
05=(1,2; 1)  06=(1,1; 1)  07=(2,2; 1)

12=(0,1;-1)  13=(0,0; 1)  14=(1,0;-1)  15=(1,1; 1)
16=(2,2; 1)  17=(0,0; 1)

23=(1,1; 1)  24=(0,1;-1)  25=(2,2; 1)  26=(0,0; 1)
27=(2,0; 1)

34=(2,2; 1)  35=(0,1; 1)  36=(1,0; 1)  37=(1,1; 1)

45=(0,0; 1)  46=(1,1; 1)  47=(1,1; 1)

56=(0,1; 1)  57=(1,1; 1)

67=(1,1; 1).
```

Every one of the `28` physical pairs occurs and has one nonzero matrix-unit
entry.  This is complete physical `r=1` support; it is not a claim that the
table has the full target tensor.

For a word `chi in {0,1,2}^8`, let `F(chi)` be the complete set of perfect
matchings whose endpoint labels induce `chi`, and put

```text
c_chi=sum_(M in F(chi)) product_(e in M) lambda_e.   (1)
```

## 2. Pure targets and the exact binomial cycle

The three constant-word fibres are singletons:

```text
F(0^8)={03|17|26|45},
F(1^8)={06|15|23|47},
F(2^8)={07|16|25|34}.                               (2)
```

Every edge in (2) has weight one.  Hence

```text
c_(0^8)=c_(1^8)=c_(2^8)=1.                          (3)
```

Now take

```text
chi_0=00001111,
chi_1=00110011,
chi_2=01010101.                                     (4)
```

Their complete compatible fibres are

```text
F(chi_0)={01|24|35|67, 02|13|46|57},
F(chi_1)={01|23|45|67, 04|12|37|56},
F(chi_2)={02|14|36|57, 04|15|26|37}.                (5)
```

In each line of (5), the first or second displayed term is the selected
offdiagonal transport term of weight `-1`, while the other is its incoming
diagonal term of weight `1`.  Therefore

```text
c_(chi_0)=c_(chi_1)=c_(chi_2)=0.                    (6)
```

Use the cross cores, bridges, and residual matchings

```text
E_0=24|35,  B_0=23|45,  P_0=01|67,
E_1=12|56,  B_1=15|26,  P_1=04|37,
E_2=14|36,  B_2=46|13,  P_2=02|57.                 (7)
```

The full offdiagonal terms are `E_i union P_i`; the bridge-normalized
diagonal terms are `B_i union P_i`.  Equation (5) is exactly the cyclic
incoming/outgoing arrangement from the phase-holonomy theorem.

Let

```text
z=sum_(i=0)^2 (1_(B_i)-1_(E_i)).                    (8)
```

The endpoint-label incidence of `z` vanishes.  Its support consists of the
twelve pairwise distinct bridge and cross edges, so `z` is nonzero.  The
associated Laurent invariant is

```text
H=lambda^z
 =product_i lambda(B_i)/lambda(E_i)
 =-1=(-1)^3.                                        (9)
```

Thus the odd binomial cycle survives after all missing physical pairs and
all three pure target coordinates have been supplied.

## 3. Strict positive endpoint balance

The following numbers are **auxiliary incidence-dual weights**, not
physical amplitudes and not squared physical amplitudes:

```text
p01=1  p02=1  p03=4  p04=1  p05=6  p06=1  p07=7

p12=4  p13=1  p14=3  p15=4  p16=7  p17=1

p23=3  p24=2  p25=1  p26=4  p27=6

p34=7  p35=2  p36=3  p37=1

p45=3  p46=1  p47=4

p56=4  p57=1

p67=1.                                               (10)
```

Every `p_e` is a positive integer.  Direct collection at each labelled
endpoint gives

```text
sum_(e incident to v, ell_v(e)=c) p_e=7             (11)
```

for every vertex `v` and every colour `c`.  Thus the support satisfies the
strict endpoint-balance hypothesis of the moment theorem, with all three
common loads equal to seven.

For clarity, the unit physical amplitudes in Section 1 are not themselves
moment-balanced: their endpoint counts vary with the vertex.  Equation
(10) proves polystability of the **label support** and is used only to obtain
the positive gauge below.

## 4. Exact moment-compatible representative

Apply Theorem 1 of the preceding moment-balanced gauge theorem to the fixed
support in Section 1 and the nonzero amplitude vector `lambda`.  Equation
(11) makes its exponential squared-norm functional coercive and strictly
convex on the real zero-colour-sum GHZ torus modulo the edgewise stabilizer.
It therefore has a unique edge-exponent minimizer.

Write its positive local factors as `s_(v,c)`, with

```text
product_v s_(v,c)=1                                 (12)
```

for every colour, and define

```text
lambda'_ij=s_(i,ell_i(ij))s_(j,ell_j(ij))lambda_ij. (13)
```

The critical-point equation gives positive actual squared amplitudes
`mu_ij=|lambda'_ij|^2` and positive numbers `q_c` such that

```text
sum_(e incident to v, ell_v(e)=c) mu_e=q_c          (14)
```

for every `v,c`.  No assertion is made that `mu_e=p_e` or that `q_c=7`.

Every matching inducing a fixed word `chi` is multiplied by the same
nonzero character

```text
kappa_chi=product_v s_(v,chi(v)).                   (15)
```

Consequently

```text
c'_chi=kappa_chi c_chi.                             (16)
```

For a constant word, (12) makes `kappa_(c^8)=1`, so all three pure
coefficients in (3) remain exactly one.  Equations (6) remain zero.  Since
`z` has zero endpoint character, (9) is unchanged exactly, not merely in
phase.

This proves existence of a complete physical table simultaneously in the
actual moment normal form and on the odd binomial holonomy boundary.  The
existence is an exact consequence of coercive strict convexity; a numerical
approximation to the minimizing gauge is neither used nor claimed.

## 5. The unavoidable nonwitness boundary

Let

```text
eta=00000100.                                       (17)
```

Its complete compatible fibre is

```text
F(eta)={04|17|26|35}.                               (18)
```

The unique matching in (18) is offdiagonal and has weight one.  Therefore

```text
c_eta=1.                                            (19)
```

After moment gauge, (16) gives `c'_eta=kappa_eta`, which is positive and in
particular nonzero.  Hence neither the original table nor its
moment-balanced representative realizes `Delta_(8,3)`.

The support also has the exact colour-nonrigidity sets

```text
S_0=S_1={1,2,3,4,5,6},
S_2={0,7}.                                          (20)
```

All three are nonempty and proper, and positive gauge leaves them
unchanged.  Thus adding proper nonrigidity to the hypotheses does not repair
the failed odd-cycle sign argument.

## 6. Proof-topology consequence and exact frontier

The earlier sparse sharpness table left open whether completion, pure
normalization, or the moment constraint would eliminate odd binomial
holonomy.  Sections 1--5 answer that question negatively and update the
matrix-unit proof DAG by the sharpness node `U7D`:

```text
complete nonzero r=1 physical support:                    PRESENT;
all three pure target coefficients exactly one:           PRESENT;
strict positive endpoint balance:                         PRESENT;
actual squared-amplitude moment-balanced representative:  EXISTS over C;
all three nonrigidity sets nonempty and proper:            PRESENT;
three exact binomial active-cycle fibres:                  PRESENT;
odd invariant holonomy H=-1:                              PRESENT;
all mixed target coefficients zero:                       FALSE;
displayed table is a Krenn--Gu witness:                    FALSE;
odd binomial holonomy excluded on the full witness locus:  UNKNOWN;
aggregate holonomy excluded:                              UNKNOWN;
pure cofactor branching/cycles excluded:                  UNKNOWN;
deeper-blocker branch excluded:                           UNKNOWN;
r=1 matrix-unit branch excluded:                          UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

Any successful continuation through the binomial-holonomy branch must use
mixed target equations beyond the three cycle fibres.  Complete support,
pure normalization, magnitude balance, and the sign of an odd cycle cannot
supply the missing contradiction.

## Replay

```powershell
python claims/arbitrary-order/verify_matrix_unit_complete_pure_target_moment_compatible_odd_holonomy_sharpness.py
python claims/arbitrary-order/audit_matrix_unit_complete_pure_target_moment_compatible_odd_holonomy_sharpness.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_complete_pure_target_moment_compatible_odd_holonomy_sharpness.py claims/arbitrary-order/audit_matrix_unit_complete_pure_target_moment_compatible_odd_holonomy_sharpness.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_complete_pure_target_moment_compatible_odd_holonomy_sharpness.py claims/arbitrary-order/audit_matrix_unit_complete_pure_target_moment_compatible_odd_holonomy_sharpness.py
```

The primary verifier enumerates all `105` perfect matchings, checks the
complete word fibres, exact coefficients, strict balance, incidence rank,
nonrigidity sets, circulation, holonomy, and a nontrivial exact GHZ gauge.
The independent no-import audit uses a separately encoded row table,
bitmask matching traversal, packed ternary words, direct endpoint ledgers,
and an independently assembled numerator/denominator character census.
The moment-balanced representative is justified by the written coercive
strict-convexity theorem, not by a finite numerical optimization.
