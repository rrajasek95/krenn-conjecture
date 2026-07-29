# The exact-five singular stratum is empty

## 1. Result

In the two-`K_4` chart with standard ternary equality tensors on both
shores, suppose exactly five cross blocks are singular.

**Theorem 1.1.**  No such block array satisfies the full matching-tensor
equations.

The local theorem behind the obstruction allows both stars in the
six-cell Hessian erasure to have one exceptional component, provided those
components occur at different physical sites.  Its kernel is either zero
or a triangle syzygy avoiding the first exceptional site.  The latter is
just as impossible for the effective right `K_4` quadratic as a zero
kernel: its three incident endpoint colors cannot lie in a two-plane.

The exact audit is
[`verify_two_k4_exact_five_adjacent_centers_obstruction.py`](../computations/verify_two_k4_exact_five_adjacent_centers_obstruction.py).

## 2. Separated-defect Hessian erasure

Let

\[
 \mathcal R=\bigotimes_{i=0}^3(\mathbb F\oplus V_i),
 \qquad V_i^2=0,\qquad\dim V_i=3,                       \tag{1}
\]

over a field of characteristic different from two.  Let `U,W` be
three-spaces and `U_0 subset U` a two-plane.  Suppose

* `P_i:U -> V_i` is invertible except possibly at site `a`;
* `S_i:W -> V_i` is invertible except possibly at site `b`;
* `a!=b`.

Write `p_alpha=sum_i P_i alpha` and `s_beta=sum_i S_i beta`.

**Lemma 2.1 (separated defects).**  If `q in R_2` obeys

\[
                    q p_\alpha s_\beta=0
          \qquad(\alpha\in U_0,\ \beta\in W),           \tag{2}
\]

then either

\[
                         q=0,                            \tag{3}
\]

or every pair block of `q` incident with site `a` vanishes:

\[
                         q_{aj}=0\qquad(j\ne a).         \tag{4}
\]

More precisely, the second case can occur only when `P_a U_0=0`; its
kernel is the one-dimensional alternating triangle syzygy on the three
sites complementary to `a`.

## 3. Two elementary sparse kernels

Relabel `a=0,b=1`.  We use the almost-invertible-star annihilator from
[`two-k4-exact-four-nonmatching-obstruction.md`](two-k4-exact-four-nonmatching-obstruction.md):
if `S_1!=0`, the common cubic annihilator of `s_beta` is one-dimensional,
and its component missing site 1 is a full determinant tensor on sites
`0,2,3`; if `S_1=0`, the annihilator consists of arbitrary cubics missing
site 1.

We also need the following sparse multiplication observation.

**Lemma 3.1.**  If `p_0=0`, every `p_i` for `i=1,2,3` is nonzero, and
`q p=0`, then

\[
                          q_{0j}=0\qquad(j=1,2,3).       \tag{5}
\]

**Proof.**  Normalize `p_1,p_2,p_3` to the first local basis vectors.
In a three-site component containing site zero, a coefficient with a
nonzero color in either occupied endpoint isolates each entry of `q_0j`.
The remaining first-color entries are killed by comparing the two choices
of the third site.  Equivalently, multiplication `R_2 -> R_3` has rank 46;
its eight-dimensional kernel is supported entirely on the triangle
`123`.  \(\square\)

The zero-component case of the almost-invertible-star annihilator uses
three overlapping triangle equations.  Their exact form will also be
useful.

**Lemma 3.2 (overlapping triangles).**  Suppose `P_1,P_2,P_3` are
isomorphisms.  If every component of `q p_alpha` on the triples `012`,
`013`, and `123` vanishes for all `alpha in U_0`, then

\[
\begin{cases}
q=0,&P_0U_0\ne0,\\
q_{0j}=0\ (j=1,2,3),&P_0U_0=0.
\end{cases}                                             \tag{6}
\]

In the second case, `q` is a scalar multiple of the alternating two-plane
triangle syzygy on `123`.

**Proof.**  Normalize `P_i|U_0` for `i=1,2,3` and reduce
`P_0|U_0` by independent basis changes to rank `d=0,1,2` normal form.
Each three-site equation is the two-plane Koszul equation

\[
 q_{ij}P_k\alpha+q_{ik}P_j\alpha+q_{jk}P_i\alpha=0.     \tag{7}
\]

Coefficient comparison on the three overlapping triples gives

\[
\begin{array}{c|ccc}
d&0&1&2\\ \hline
\dim\text{ simultaneous kernel}&1&0&0.
\end{array}                                             \tag{8}
\]

For `d=0`, (7) first kills every block incident with site zero; the
remaining equation on `123` has the single alternating generator.  For
`d=1,2`, the alternating boundary signs on the shared blocks force a scalar
to equal its negative, so characteristic different from two kills it.
\(\square\)

## 4. Proof of separated-defect erasure

Set `T_alpha=q p_alpha`.  First suppose `S_1!=0`.  Every `T_alpha` lies on
the one-dimensional generalized-determinant annihilator line.  Hence some
nonzero `alpha in U_0` satisfies `q p_alpha=0`.

If `P_0 alpha=0`, Lemma 3.1 immediately gives (4).  Otherwise every local
component of `p_alpha` is nonzero.  The full-support multiplication kernel
then has the form

\[
 q_{ij}=z_{ij}p_i\otimes p_j,qquad
 z_{ij}+z_{ik}+z_{jk}=0.                                \tag{9}
\]

Choose `alpha'` independent of `alpha`.  The component of
`q p_(alpha')` missing site 1 is supported in local two-planes at sites
`0,2,3`, so every mode rank is at most two.  A nonzero tensor on the
generalized-determinant line has mode rank three there.  Thus
`q p_(alpha')=0`.  Its component on `123` kills
`z_12,z_13,z_23`, because the two local vectors are independent at those
three invertible sites.  The four triangle sums in (9) then kill
`z_01,z_02,z_03` in characteristic different from two.  Hence `q=0`.

If `S_1=0`, the common annihilator says precisely that the components of
every `q p_alpha` on `012`, `013`, and `123` vanish.  Lemma 3.2 gives
(3) or (4).  This proves Lemma 2.1.

## 5. Application to two block rows

Suppose block rows `r,s` each contain at most one singular block and their
exceptional columns `a,b` are distinct.  Let `0,t` be the complementary
left vertices, put `c=kappa(0t)`, and define

\[
 p_{i,x}=\sum_j\operatorname {row}_x(B_{ij})^{(j)},
 \qquad q_{\rm eff}=q_R+p_{0,c}p_{t,c}.                 \tag{10}
\]

For a left word colored `c` at `0,t` and `x,y` at `r,s`, the sector using
the internal edge `0t` is

\[
                         q_{\rm eff}p_{r,x}p_{s,y}.      \tag{11}
\]

For `x!=c` and arbitrary `y`, the left word is nonconstant and `0t` is its
unique compatible internal edge.  The target and zero-cross coefficients
vanish, so the six hypotheses of Lemma 2.1 hold.

If the lemma gives `q_eff=0`, then `q_R=-p_(0,c)p_(t,c)`.  At every right
site, this puts the three incident endpoint colors of `q_R` in the span of
two local vectors, although they are the three coordinate axes.

If instead every `q_eff` block incident with site `a` vanishes, the same
contradiction occurs just at site `a`: each of the three incident blocks of
`q_R` equals the negative corresponding product block and hence has its
endpoint line in the same two-plane.  Therefore:

**Proposition 5.1.**  Two block rows having at most one singular block each
cannot have their exceptional blocks in distinct columns.  The transposed
statement holds for block columns.

## 6. Exact-five census

Earlier erasure lemmas imply that an exact-five singular support meets all
four rows and all four columns.  Indeed, if one row were missed, the five
edges on the other three rows would include a degree-one row, contradicting
the one-defect theorem; transpose handles columns.

Thus both degree partitions are

\[
                              (2,1,1,1).                 \tag{12}
\]

Consider the three degree-one rows.  If their exceptional columns were all
equal, that column would have degree at least three, contradicting (12) on
the other shore.  Hence two degree-one rows have distinct exceptional
columns, and Proposition 5.1 excludes the support.  This proves Theorem
1.1.

The adjacent-centers orbit requested explicitly has representative

\[
                 (0,0),(0,1),(1,0),(2,2),(3,3),         \tag{13}
\]

the bipartite graph `P_4` plus two disjoint edges.  Rows 1 and 2 already
give the separated pair at columns 0 and 2.

## 7. Exact audit

Run

```text
python computations/verify_two_k4_exact_five_adjacent_centers_obstruction.py
```

The checker verifies the sparse multiplication kernel, the overlapping
triangle nullities `1,0,0`, the complete two-defect erasure rank table for
all twelve rank normal forms, all 729 coefficients of (11) on an exact
adjacent-centers chart, the 288 labelled supports in that position orbit,
and the global count

\[
             4368\text{ exact-five supports}
       \longrightarrow432\text{ with full occupancy}
       \longrightarrow0.                                \tag{14}
\]
