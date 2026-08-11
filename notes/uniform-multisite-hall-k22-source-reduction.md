# The strict Hall `K2,2` family reduces to one opposite-shore lock

> **Correction (supersedes the original `19b1bbf` wording).**  The axis
> products on oriented edges `03` and `30` occupy different output words,
> as do `12` and `21`.  They are four monomial coefficient rows, not two
> binomial locks.  Moreover, retaining both mandatory core matchings repairs
> the natural overlap ranks to `(3,3,3,3)`.  The corrected unary and
> curvature boundary is
> [`uniform-multisite-hall-k22-unary-incidence-boundary.md`](uniform-multisite-hall-k22-unary-incidence-boundary.md).

## Result

Let the two pure diagonal hole families be cross-intersecting and suppose
both have matching number two.  After relabelling, their strict cores are

```text
colour 1:  01 | 23,        colour 2:  02 | 13.
```

Every additional hole edge lies in the common third matching `03 | 12`.
Orient the four core edges by which endpoint is occupied by the `P`-star.
Of the sixteen orientations,

```text
12 have two common-side sites,
 2 have four common-side sites,
 2 have no common-side site.
```

At a site where both **complete oriented contributions** are nonzero, the
existing Hall-star source identity applies verbatim.  It forces the
crossed active debts, hence either a free off-anchor active carrier, the
co-located Hall lock, or the already isolated triangle route.  If a
selected monomial is nonzero but its complete oriented contribution
cancels, this is precisely the earlier affine line-hitting/joint-kernel
gate; the combinatorial orientation alone does not repair that gap.

Thus only two genuinely opposite effective orientations are new.  They
are equivalent to the shore decomposition

```text
A={0,3}:  p1,s2,          B={1,2}:  p2,s1.
```

When no same-word cancellation mate leaves the selected axis packet, the
four crossed word coefficients force the two pure-zero shore cofactors
`H03,H12` to vanish.  A permanent-null cap kills every mixed quadratic
sector, but leaves exactly two pure repeated-row sectors.  Both mandatory
core matchings plus the unary direct anchor repair the natural overlapping
arms to active ranks `(3,3,3,3)`; a nonzero shore determinant is the exact
remaining curvature datum.

Checker:
`computations/verify_uniform_multisite_hall_k22_source_reduction.py`.

## 1. Strict rectangle and orientation classification

Write

```text
M1={01,23},  M2={02,13},  M3={03,12}.
```

An edge meeting both members of `M2` lies in `M1 union M3`, while an edge
meeting both members of `M1` lies in `M2 union M3`.  Hence `M3` is the only
possible optional part of either strict family.  This is the complete
family statement; no subsets of source cells are enumerated.

For each core edge choose which endpoint is its `P` port.  At every K4
site compare the choices for the two colours.  Direct enumeration of the
four binary choices gives the `12+2+2` histogram above.  The two zero-common
orientations are shore complements; up to swapping endpoints and colours,

```text
p1=a0 e1@0+a3 e1@3,       s1=c1 e1@1+c2 e1@2,
p2=b1 e2@1+b2 e2@2,       s2=d0 e2@0+d3 e2@3.          (1)
```

The important scope point is aggregate effectiveness.  The Hall-star
identity uses a nonzero complete coefficient after fixing the common port,
not merely one nonzero perfect-matching monomial.  If that complete
coefficient vanishes through cancellation, the needed operation is still
the joint-kernel affine modification from the concentration boundary.

## 2. Four distinct crossed coefficients

In (1), `p1 s2` is supported on shore `A`, and `p2 s1` on shore `B`.
Site-square-freeness kills the equal-site products.  The four selected axis
products occupy four different residual output words.  In the absence of a
same-word cancellation mate, their literal coefficient rows are

```text
a0 d3 H03 = 0,          a3 d0 H03 = 0,
b1 c2 H12 = 0,          b2 c1 H12 = 0.                 (2)
```

All eight strict-core star coefficients are nonzero, so (2) gives
`H03=H12=0`.  There is no odd signed holonomy between `03` and `30` because
they are not terms of one polynomial coefficient.  A same-word term leaving
the selected web exposes an off-anchor decorated endpoint cell.  Reselecting its
physical pair gives rank-three deleted stars by the pinned matching-column
lemma and enters the source-provenant good active-minor route.  A dependence
among the same-star five-row lock columns instead gives the exact
anchor-safe deletion of the five-lock theorem.  Otherwise (2) is the exact
cofactor-dark residual.

## 3. Exact permanent-null cap tail

Put

\[
 R=x p_1s_1+r p_1s_2+s p_2s_1+y p_2s_2,
 \qquad xy+rs=0.                                      \tag{3}
\]

The four genuine response tensors give

\[
                 Rq^{[h-1]}=xX_1+yX_2.                \tag{4}
\]

On the K4 core, exact hafnian expansion gives

\[
\begin{aligned}
[1111]R^{[2]}&=2x^2a_0a_3c_1c_2,\\
[2222]R^{[2]}&=2y^2b_1b_2d_0d_3.                     \tag{5}
\end{aligned}
\]

The other four possible colour patterns are

\[
 \text{one star monomial}\,(xy+rs),                  \tag{6}
\]

with star factors respectively

```text
a0 b2 c1 d3,  a0 b1 c2 d3,
a3 b2 c1 d0,  a3 b1 c2 d0.
```

Thus (3) kills all mixed K4 sectors but not (5).  For `h=3`, the outside
edge `q45` multiplies each line of (5).  Its nine decorated components give
eighteen pairwise distinct output words:

```text
1111ab and 2222ab,  a,b in {0,1,2}.
```

The two pure debts therefore cannot cancel one another while both diagonal
cap coefficients remain active.  If `q45=0`, the cap is clean; otherwise
this is exactly a repeated endpoint-use tail.  By the pinned provenance
theorem it is not itself a physical curved witness.

## 4. The strict core repairs the natural overlap

Restore outer endpoints `P,S` and take the selected pure matchings

```text
Q0: PS | 01 | 24 | 35,
Q1: P0 | S1 | 23 | 45,     P3 | S2 | 01 | 45,
Q2: P2 | S0 | 13 | 45,     P1 | S3 | 02 | 45.
```

The natural distinct-head overlap is `P0,S0`.  Cutting either selected arm
removes its own pure matching column, but the second disjoint core matching
restores that colour.  The other diagonal target and the direct unary
matching restore the other two endpoint rows.  Thus the four ranks are

```text
(3,3,3,3).
```

Both arms occur in nonzero selected diagonal-target monomials, so they are
support-active.  The shore determinant
`kappa_A=a0*d3-d0*a3` is the physical transition minor; the analogous
`kappa_B` lives on the other shore.  A nonzero minor reaches the active
four-good curved interface.  What the strict core does not force is that
one of these two minors is nonzero.

## 5. Exact boundary

The uniform strict-rectangle reduction is now:

1. failure of complete oriented effectiveness is the existing affine
   line-hitting/joint-kernel gate;
2. a common effective side enters the Hall-star theorem;
3. a free off-web cancellation mate enters the good active route;
4. a five-row lock kernel gives an anchor-safe deletion;
5. nonzero `kappa_A` or `kappa_B` reaches the active four-good curved
   interface; and
6. otherwise the two shore vectors are proportional, (2) gives
   `H03=H12=0`, and the two factorized tails (5) remain.

This is source-labelled family algebra, not a support census.  It neither
constructs a one-bad source nor proves the opposite residual empty.  The
unary top repairs the missing rank but does not exclude the cofactor-dark
condition: the exact pure-zero matching `01|24|35` has top coefficient one
and both `H03,H12` zero.  The remaining row must therefore couple this
unary matching to a shore cofactor or force a same-word cancellation mate.

## Verification

Run

```text
python3 computations/verify_uniform_multisite_hall_k22_source_reduction.py
python3 -O computations/verify_uniform_multisite_hall_k22_source_reduction.py
python3 -I -S computations/verify_uniform_multisite_hall_k22_source_reduction.py
```

Frozen ledger SHA-256:

```text
d4eb154985c824c9e463ff6db4f6c0c47a42458561583f65bae9e459ca3edad5
```
