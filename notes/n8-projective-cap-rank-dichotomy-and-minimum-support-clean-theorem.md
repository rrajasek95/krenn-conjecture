# At eight sites: projective cap rank, a minimum-support clean theorem, and the sharp rank guard

## Outcome

Fix an endpoint-ordered aggregate source on eight sites, a pair `p,q`, and
write

\[
 R=B\setminus\{p,q\},\qquad Q=H_R(A),\qquad
 E=\operatorname{span}\{X_0,X_1,X_2\},
 \quad X_c=e_c^{\otimes R}.
\]

There are three exact conclusions.

1. **Full-source projective-rank dichotomy.**  If
   \(H_B(A)=\Delta_{8,3}\), then for every cap covector `C`

   \[
   \boxed{\quad
   \kappa_{pq}(C)
    =[D H_R(A)[B^C]]
    =\left[\sum_{c=0}^2 C_{cc}X_c\right]
      \in T_R/\langle Q\rangle .\quad}                 \tag{1}
   \]

   Hence a **target-active** zero-error cap exists at this pair precisely
   when

   \[
                0\ne Q=q_0X_0+q_1X_1+q_2X_2,
                \qquad q_0q_1q_2\ne0.                 \tag{2}
   \]

   This is the finite deletion target.  Doubly injective endpoint stars do
   not alter (1); they must be used to force (2).

2. **Minimum-support clean theorem.**  Suppose all 28 pairs are doubly
   aggregate-injective and the aggregate support has the minimum possible
   eight nonzero physical blocks.  Then every active support edge admits an
   active clean cap.  Thus no exact eight-site ternary source can lie in
   this minimum-support stratum, by the proved arbitrary-complex six-site
   obstruction.

3. **Sharp first-order guard.**  One pure-normalized rational `C8` source
   attains that minimum support and the block rank forced on that support,
   has all 28 pairs doubly injective, yet its projective cap-error map has
   rank nine at every pair.  Thus

   \[
                    \kappa_{pq}(C)\ne0
                    \quad\text{for every }C\ne0         \tag{3}
   \]

   at all 28 pairs.  Its eight support edges nevertheless have active clean
   caps.  This separates the linear deletion route from the nonlinear clean
   route exactly.  The guard is one common physical source, not 28
   independently chosen pair charts, but it is not a GHZ source: its first
   displayed mixed residual is `01000000 = 1283/117`.

The checker is
[`verify_n8_support_rank_minimal_projective_cap_error_counterguard.py`](../computations/verify_n8_support_rank_minimal_projective_cap_error_counterguard.py).

## 1. The full-source identity removes the star variables

For an arbitrary cap `C`, put

\[
 s_C=\langle C,A_{pq}\rangle,
\]

and let `B^C` be the exact two-star effective quadratic

\[
 B^C_{ij}=\operatorname{contr}_{p,q}^C
 \bigl(A_{pi}A_{qj}+A_{pj}A_{qi}\bigr).                \tag{4}
\]

Sorting the physical matchings according as they use `pq` gives

\[
 \operatorname{contr}_{p,q}^C H_B(A)
   =s_CQ+D H_R(A)[B^C].                                \tag{5}
\]

If the **complete** source equation is imposed, the same contraction is

\[
 \operatorname{contr}_{p,q}^C\Delta_{8,3}
   =\sum_c C_{cc}X_c.                                  \tag{6}
\]

Subtracting `s_C Q` and passing modulo `Q` proves (1).  This uses all nine
endpoint-colour rows at the pair.  In particular it is not a semisimple
one-cap calculation and does not select a source occurrence.

The quotient ranks are now elementary.

* If `Q=0` or `Q` is outside `E`, the three diagonal columns remain
  independent modulo `Q`.  The rank of `kappa` is three and its kernel is
  exactly the six-dimensional off-diagonal cap space.
* If `0 != Q=sum q_c X_c` lies in `E`, the quotient rank is two and

  \[
       \ker\kappa
       =\{C:\ (C_{00},C_{11},C_{22})=\lambda(q_0,q_1,q_2)\}. \tag{7}
  \]

  The six off-diagonal entries remain arbitrary.  The new diagonal line is
  target-active exactly when all three `q_c` are nonzero.

This also corrects a quantifier trap in the phrase “zero projective cap
error.”  Every off-diagonal cap of an exact target source already has zero
projective error at every pair.  It gives no descent: (6) is zero, and in
(5) the direct and error scalars cancel to the zero contraction.  The
useful statement is **target-active** zero error, which is exactly (2).

If (2) holds, the deleted aggregate array itself has matching tensor
`sum q_c X_c`; an invertible diagonal change at one residual site turns it
into `Delta_(6,3)`.  The six-site theorem excludes this.  Thus a hypothetical
exact eight-site source must keep every deleted cofactor either outside `E`
or on a coordinate face of `E`.  A successful direct support/rank proof has
been reduced to forcing one good pair off those alternatives.

## 2. Minimum support forces the nonlinear clean alternative

Let `G` be the graph of nonzero aggregate blocks and assume every physical
pair is doubly injective.  Every vertex of `G` has degree at least two.  If
`p` had zero or one active neighbour `q`, deleting the pair `p,q` would
leave the `p`-star zero, contradicting injectivity.  The handshake lemma
therefore gives

\[
                            |E(G)|\ge8.                 \tag{8}
\]

Assume equality.  Every vertex has degree two.  Moreover, every active
block has rank three: at an endpoint `p`, delete one of its two neighbours;
the other block is then the sole surviving summand of the injective star.
Thus the total aggregate block rank is at least, and at equality is,

\[
                              8\cdot3=24.               \tag{9}
\]

Fix an active edge `pq`.  Outside that edge, `p` has one neighbour `i` and
`q` has one neighbour `j`.  Formula (4) shows that for every cap `K` the
effective correction `r=B^K` is supported on at most the single physical
pair `ij`; it is zero if `i=j`.  In the site-square-zero algebra,

\[
                              r^2=0.                    \tag{10}
\]

At eight sites the homogeneous clean error is

\[
 {cal E}_{p,q}(K)=\frac{s_Kr^2x}{2}+\frac{r^3}{6},     \tag{11}
\]

so (10) kills it identically.  Since `A_pq` has rank three, one may choose
`K` outside the four hyperplanes

\[
 \langle K,A_{pq}\rangle=0,\qquad K_{00}=0,\qquad
 K_{11}=0,\qquad K_{22}=0.                              \tag{12}
\]

Over `C` their complement is nonempty.  This `K` has
`s_K K_00 K_11 K_22 != 0` and is an active clean cap.  The argument is
local and gives the slightly broader criterion:

> A doubly injective active pair whose two deleted endpoint stars are each
> supported at at most one residual site is actively clean.

The minimum-support theorem follows by applying this criterion to any
support edge.  Notice that it reaches the nonlinear alternative even when
every first-order projective error is nonzero.

## 3. The exact eight-edge guard

Use the cyclic support

\[
                  0-4-1-5-2-6-3-7-0.                  \tag{13}
\]

In stored endpoint order, put the following integral matrices on its eight
edges and zero on the other twenty:

```text
04 [[ 5, 3, 9], [ 4,16,15], [16,13, 7]]
07 [[ 4,16, 1], [13,14, 1], [15, 9, 8]]
14 [[ 4,11, 1], [ 1, 1, 1], [13, 7,14]]
15 [[ 1,17, 8], [15,16, 8], [12, 8, 8]]
25 [[15,10, 1], [14, 4, 6], [10, 4,11]]
26 [[17,14,17], [ 7,10,10], [16,17,13]]
36 [[ 2,16, 8], [13,14, 6], [12,12, 3]]
37 [[15,17, 4], [ 6,17,13], [12,16, 1]]
```

All eight determinants are nonzero.  Before normalization the three pure
coefficients are

\[
                         (1755,44304,4424).              \tag{14}
\]

For each block incident with site zero, multiply row `c` by the reciprocal
of the `c`-th number in (14).  Site multilinearity makes all three pure
coefficients exactly one, while preserving every block rank and every star
rank.

The support is sharp twice over.

* Every pair deletion leaves each endpoint with an invertible retained
  block, so all 28 pairs are doubly injective.
* Removing any support edge leaves one endpoint of degree one.  Deleting
  its other neighbour then leaves a zero star.  Thus the displayed source
  is edge-deletion-minimal for the all-pairs-good property, and (8)--(9)
  prove global minimality of its support size and show that total block rank
  24 is forced within this minimum-support stratum.

For each pair, the checker builds all 729 residual words and the literal
nine-column error matrix

\[
 C\longmapsto D H_R(A)[B^C]
 =\operatorname{contr}_{p,q}^C H_8(A)-\langle C,A_{pq}\rangle Q. \tag{15}
\]

Reduction modulo the prime `1000003` gives

\[
\begin{array}{c|c|c|c}
\text{pair type}&Q&\operatorname{rank}D&
 \operatorname{rank}[D\mid Q]\\ \hline
\text{same shore (12 pairs)}&0&9&9\\
\text{opposite shore (16 pairs)}&\ne0&9&10.
\end{array}                                                \tag{16}
\]

The normalization denominators are units modulo this prime.  Hence every
displayed nonzero minor lifts to a nonzero rational minor, and (16) proves
that the projective map has rank nine at all 28 pairs.  This is (3).

On the other hand, the identity cap is active and clean on all eight
support edges: its direct scalar is positive, its three diagonal readouts
are one, and the correction has the one-edge support used in (10).  Thus
the guard sharply says that projective deletion and clean Schur descent
cannot be identified.

## 4. Why the mixed equations are the first missing hypothesis

The construction is one endpoint-ordered quadratic.  Consequently every
pair response, restriction, and direct-edge/two-star matching identity is
automatically compatible across all 28 charts.  It is not a collection of
independent local shadows.

It nevertheless fails the target equation.  All displayed matrix entries
are positive, and the normalized coefficient of the mixed detector word

\[
                             01000000                    \tag{17}
\]

is exactly `1283/117`, not zero.  This explains the rank jump between (1)
and (16): the complete mixed GHZ equations collapse the projective error
rank from a possible nine to at most three.  Pure normalization, minimum
support, the rank forced on that support, all-pair goodness, and common physical
provenance do not cause that collapse.

Therefore the shortest remaining direct-deletion attack is now precise:

1. use at least one genuinely mixed full-source row to constrain the
   six-site deleted tensor `Q`, not merely the endpoint stars;
2. prove that for some good pair `Q` lies in the open diagonal plane
   `E^times` of (2); or
3. bypass `Q` by proving a local one-edge (or another nilpotent-support)
   condition on `B^K`, as in the minimum-support clean theorem.

The first-order zero-error statement without target activity is already
automatic and carries no descent.

## 5. Reproduction

```sh
python3 computations/verify_n8_support_rank_minimal_projective_cap_error_counterguard.py
python3 -O computations/verify_n8_support_rank_minimal_projective_cap_error_counterguard.py
python3 -I -S computations/verify_n8_support_rank_minimal_projective_cap_error_counterguard.py
```

The frozen exact ledger digest is
`ad98141d3c67d40598571f18d594f2898cd7d1f3352c1f467e4441e3b5b67f25`.
