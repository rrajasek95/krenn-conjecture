# Eleven branches suffice for the colour-swap-twisted F3 slice

This note gives the exact source-gauge quotient of the pure-diagonal branches
in `computations/search_f3_translation_invariant_n8.py --twisted`.  It is a
finite-field symmetry reduction only.  It makes no characteristic-zero
claim.

## 1. The initial 36 branches are exhaustive

Let `lambda(u)=u&1`, and let `sigma=(1 2)` act on the three colours.  The
twisted translation action sends a vertex/colour pair `(u,c)` to
`(u+t,sigma^lambda(t)(c))`.  Since `sigma` fixes colour zero, the distinguished
pure row is again a scalar difference row

\[
 b=(b_d)_{d\ne0}\in F_3^7.
\]

There are exactly 882 rows with scalar hafnian one.  The stabilizer of
`lambda` in `GL(3,2)` has order 24.  Together with simultaneous field
negation, it partitions those 882 rows into exactly the 36 disjoint orbits
listed as `TWISTED_PURE_ORBIT_REPS`.  Their sizes are

```text
8 6 24 24 12 12 6 6 24 24 24 24 48 48 24 48 24 48
24 24 8 8 24 24 24 24 24 48 48 24 24 12 48 12 24 24
```

and sum to 882.

## 2. Full branch-effective source gauges

The following computations also show that the reduction is not missing a
larger monomial source gauge.

First, a vertex permutation which retains difference-only dependence is
affine.  There are `8*168=1344` such permutations.  Preserving the twist
forces its linear part to stabilize `lambda`, leaving `8*24=192`.  A common
colour permutation must centralize `sigma`, so only the identity and `sigma`
itself occur.  Exhausting all 168 linear maps and all six colour permutations
finds exactly these `24*2=48` compatible linear/colour pairs.

Second, write a local diagonal sign gauge as
`g_(u,c)=(-1)^x_(u,c)`.  Requiring it to preserve the twisted source
identifications for arbitrary entries gives 378 distinct binary equations in
24 exponents, of rank 18.  Their full 64-element solution space is

\[
 x_{u,c}=h\mathbin\cdot u+k_{\sigma^{\lambda(u)}c},
 \qquad h\in F_2^3,\quad k_0,k_1,k_2\in F_2.          \tag{1}
\]

Every gauge (1) fixes the three pure target coefficients.  On the colour-zero
pure row its only effect is the common character
`b_d -> (-1)^(h.d)b_d`; the three base-colour signs have no further branch
effect.

Finally, consider every colour-independent difference sign
`B_d -> (-1)^s_d B_d`.  Requiring its product to be one on each of the 105
perfect matchings gives a binary matching system of rank three.  Its complete
16-element kernel is

\[
 s_d=\epsilon+h\mathbin\cdot d,
 \qquad \epsilon\in F_2,\quad h\in F_2^3.             \tag{2}
\]

Thus (2) consists exactly of global sign and common difference characters;
there are no other coefficient-preserving difference signs.  Combining
(1), (2), and the 24-element linear stabilizer gives the full action relevant
to pure-row branching:

\[
 (T_{\epsilon,h,M}b)_d
 =(-1)^{\epsilon+h\cdot Md}b_{Md},
 \quad M\in\operatorname{Stab}(\lambda).              \tag{3}
\]

Each character in (3) has product one over the four differences of every
perfect matching, while global sign occurs four times.  Hence (3) preserves
all `n=8` matching coefficients exactly, not just their support.

## 3. The eleven gauge classes

The 36 normalized branches form the following eleven classes under (3):

```text
{0}
{1}
{2,3}
{4,5}
{6,7}
{8,9,10,11,12,13}
{14,15,16,17,18,19}
{20,21,22,23}
{24,25,26,27,28,29}
{30,32,34}
{31,33,35}
```

Consequently an exhaustive twisted SAT sweep needs only

```text
0 1 2 4 6 8 14 20 24 30 31
```

and every omitted branch is exactly equisatisfiable to the least element of
its displayed class.

## 4. Exact audit

Run

```sh
.venv/bin/python computations/verify_f3_twisted_pure_orbits.py
```

The checker reconstructs all 882 scalar rows and 36 initial orbits, exhausts
the affine and colour normalizers, solves the local-gauge and matching-sign
systems over `F2`, constructs all eleven augmented orbits, and checks explicit
maps from all 36 representatives to the eleven bases.  Its terminal line is

```text
PASS scalar_solutions=882 base_orbits=36 gauge_classes=11 difference_signs=16 affine_normalizer=192 colour_centralizer=2 diagonal_gauges=64 minimal_branches=11
```

`--solve-bases` reruns all eleven production CNFs, while repeated
`--solve-orbit I` options select individual branches.  Any returned SAT model
is independently checked by enumerating all `3^8` colourings.
