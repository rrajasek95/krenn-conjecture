# A singular scalar-zero cap routes to a null-adjugate row, not directly to a permanent unit

## Result

Retain the literal six-residual-site equations

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2,                                   \tag{1}
\]

with one common physical `q`, and suppose the singular-cap export of
`1c9692f` has produced

\[
\operatorname {rank}K\le2,\qquad K_{00}K_{11}K_{22}\ne0,
 \qquad \sigma(K):=\langle K,a\rangle=0.                \tag{2}
\]

There is a uniform source-valid reduction, but it stops one step before a
clean landing.  The rank-one case is already a one-channel ternary packet.
In the rank-two case choose left and right null vectors

\[
                         \xi^{\mathsf T}K=0,
                         \qquad K\eta=0.                 \tag{3}
\]

Then both null supports have cardinality at least two, their intersection is
nonempty, and contraction of all nine physical rows by the rank-one matrix
`T=xi eta^T` gives

\[
 \boxed{
  \beta q^{[3]}+p(\xi)s(\eta)q^{[2]}
       =\sum_i\xi_i\eta_iX_i,
  \qquad \beta=\langle\xi\eta^{\mathsf T},a\rangle .}   \tag{4}
\]

The number of target labels in (4) is exactly the number of nonzero diagonal
principal cofactors of `K`, hence is one, two, or three.  Thus every singular
two-channel scalar-zero packet routes canonically to a **one-channel** unary,
binary, or ternary null-adjugate row.  In the ternary branch, if `beta != 0`,
this is a target-active rank-one cap.

What does not follow is cleanliness.  Nor does `det K=0`, even together with
the three nonzero diagonal anchors, force an odd/permanent-triangle unit.  An
exact physical common-`q` local guard below has a target-active adjugate cap
whose clean error is nonzero in 63 words, while both `det K` and `per K`
vanish by the same even-cycle cancellation.

The checker is
[`verify_h3_singular_rank2_fullnine_null_adjugate_boundary.py`](../computations/verify_h3_singular_rank2_fullnine_null_adjugate_boundary.py).

## 1. Rank one is already the one-channel boundary

If `rank K=1`, write

\[
                              K=uv^{\mathsf T}.             \tag{R1}
\]

Every `K_ii=u_i v_i` is nonzero, so both vectors have full fixed-label
support.  Contracting (1) by `K` and using `sigma(K)=0` gives immediately

\[
 \boxed{p(u)s(v)q^{[2]}=\sum_i u_i v_iX_i.}              \tag{R2}
\]

Thus the rank-one export is already a direct-dark, one-channel, ternary
scalar-zero packet.  Its matrix permanent is nonzero:

\[
             \operatorname {per}(uv^{\mathsf T})
                 =6\prod_i u_iv_i=6\prod_iK_{ii}\ne0.    \tag{R3}
\]

This still does not make it clean.  On the physical local packet in Section
5, the exact rank-one cap

\[
 \begin{pmatrix}1&-1&1\\1&-1&1\\1&-1&1\end{pmatrix}
\]

is scalar-zero, has all three diagonal targets nonzero, and has nine nonzero
clean-error words.  Hence even the rank-one branch still needs the complete
mixed rows or a physical deletion argument.

## 2. The rank-two null row is literal

Multiply (1) by `xi_i eta_j` and sum over all ordered pairs.  No matching
power is divided and no target quotient is taken:

\[
 \sum_{ij}\xi_i\eta_j a_{ij}q^{[3]}
 +\left(\sum_i\xi_i p_i\right)
  \left(\sum_j\eta_j s_j\right)q^{[2]}
 =\sum_i\xi_i\eta_iX_i.                                \tag{5}
\]

This is (4).  It uses the full nine rows and preserves their word, endpoint,
and target labels.

The common-`q` Hessian realization from `cd2d0b2` commutes with this
contraction coefficientwise.  If

\[
 C_{ij,w}=\sum_{x<y}R_{ij,xy}(w)H_{xy,\bar w},           \tag{6}
\]

then

\[
 \sum_{ij}\xi_i\eta_jC_{ij,w}
 =\sum_{x<y}R_{p(\xi),s(\eta),xy}(w)H_{xy,\bar w}.       \tag{7}
\]

The checker replays (7) on all 729 words, on top of the 1,215 common Hessian
coordinates and their 65,610 ordered disjoint-edge compatibility checks.
Consequently Hessian naturality authorizes (4), but it supplies no additional
scalar equation capable of making its cap clean.

## 3. Exact adjugate and support classification

For rank two,

\[
                \operatorname {adj}(K)=\gamma\eta\xi^{\mathsf T}
                \quad(\gamma\ne0).                     \tag{8}
\]

Therefore the cap in (4) is a nonzero scalar multiple of
`adj(K)^T`, and

\[
 \operatorname {adj}(K)_{ii}=\gamma\eta_i\xi_i.         \tag{9}
\]

Because `K_ii != 0`, neither null vector can be supported on one coordinate:
a coordinate left null would make a physical row of `K` zero, and a
coordinate right null would make a column zero.  Hence

\[
             |\operatorname {supp}\xi|\ge2,
             \qquad |\operatorname {supp}\eta|\ge2.     \tag{10}
\]

Their supports meet.  More sharply, there is no rank-two matrix with
nonzero diagonal and all three principal cofactors zero.  This can be seen
without changing physical target labels.  For bookkeeping only, left-scale
the rows to write

\[
 K=\begin{pmatrix}1&a&b\\c&1&d\\e&f&1\end{pmatrix}.    \tag{11}
\]

The three diagonal cofactors are

\[
                    1-df,\qquad1-be,\qquad1-ac.          \tag{12}
\]

If all vanish, put `x=ade` and `y=bcf`.  Then `xy=1`, while

\[
       0=\det K=1+x+y-df-ac-be=x+y-2.                   \tag{13}
\]

Thus `(x-1)^2=0`, so `x=y=1` over `C`.  Substitution makes all three rows
of (11) proportional, contradicting rank two.  Equations (9)--(13) prove
the exact trichotomy

```text
one live cofactor   <=> unary null-adjugate target,
two live cofactors  <=> binary null-adjugate target,
three live cofactors <=> ternary null-adjugate target.
```

The exhaustive normalized `F_5` audit is a mutation guard, not the proof.
It finds 3,404 rank-two matrices and the following null-support strata:

| `(|supp xi|,|supp eta|,|intersection|)` | count |
|---|---:|
| `(2,2,1)` | 384 |
| `(2,2,2)` | 252 |
| `(2,3,2)` | 816 |
| `(3,2,2)` | 816 |
| `(3,3,3)` | 1,136 |

All three target-support sizes really occur.  The scalar `beta` is not fixed
by `sigma(K)=0`: the two matrix functionals `a -> <K,a>` and
`a -> <xi eta^T,a>` are independent because a rank-two matrix cannot be
proportional to a rank-one matrix.  Pure matrix algebra therefore cannot
choose between the direct-dark and direct-bright null rows.

## 4. The determinant/permanent shortcut fails exactly

Consider

\[
 K=\begin{pmatrix}
 1&-1&0\\
 0&1&-1\\
 -1&0&1
 \end{pmatrix}.                                        \tag{14}
\]

It has

\[
 \operatorname {rank}K=2,\qquad
 \xi=\eta=(1,1,1),\qquad
 \operatorname {adj}(K)=\mathbf1\mathbf1^{\mathsf T}.  \tag{15}
\]

Every diagonal entry and every diagonal cofactor is one.  Nevertheless the
only nonzero permutation monomials are

```text
identity (012):       +1, parity even,
three-cycle (120):    -1, parity even.
```

Consequently

\[
                             \det K=\operatorname {per}K=0. \tag{16}
\]

The nonzero diagonal product is cancelled by an even three-cycle, not by an
odd-holonomy term.  The full normalized `F_5` census confirms that for each
of the one-, two-, and three-cofactor strata there are matrices with zero
permanent and matrices with nonzero permanent.  Thus no implication

```text
det K=0 + K_00 K_11 K_22 != 0  =>  permanent-triangle unit
```

is available.

There is a second categorical problem with multiplying the six permutation
rows: each row in (1) already has full residual site degree six, so products
of two such rows vanish in the site-square-zero algebra.  A valid permanent
certificate must instead come from a same-degree occurrence/Hasse relation;
ordinary commutative multiplication of the top rows does not provide it.

## 5. Physical common-`q` local counterguard and first new row

Insert (14) into the committed 20-cell physical packet of `c8a0383`, whose
direct block is

\[
                         a=-(E_{00}+E_{01}).              \tag{17}
\]

Then

\[
             \langle K,a\rangle=0,
             \qquad
             \langle\operatorname {adj}(K),a\rangle=-2. \tag{18}
\]

The packet is literal: its `p`, `s`, and `q` cells reconstruct every
common-Hessian response coordinate.  It satisfies all nine rows at each of

```text
000000, 111111, 222222, 010122.
```

Contracting those rows by (14) gives `(1,1,1,0)`, exactly the three pure
anchors and selected mixed zero.  Contracting by the adjugate gives the
source-valid target-active rank-one row with `beta=-2`.

Neither cap is clean.  The singular cap has eight nonzero clean-error words;
the first is

\[
                         000101\longmapsto-6.             \tag{19}
\]

The active adjugate has 63; the first is

\[
                         000001\longmapsto-4.             \tag{20}
\]

This shows exactly why “take the adjugate” is a reduction, not the terminal
clean landing.

The packet is **not** a full source.  Of the 6,561 scalar equations it
satisfies 6,455 and fails 106.  The first failure is

\[
  (i,j;w)=(0,0;000011),\qquad
  a_{00}q^{[3]}_w+p_0s_0q^{[2]}_w-\delta_{00}X_{0,w}=1.  \tag{21}
\]

Thus (21), or its complete source-labelled orbit, is the first datum that a
positive terminal proof must use.  The guard rules out a proof from the pure
anchors, one selected mixed row, singular matrix alternation, and shared
Hessian naturality alone.  It is not a full-nine guard and is not presented
as a counterexample to the conjecture.

## Sharp remaining statement

After `1c9692f`, the exact terminal has been reduced to the following.

> **Null-adjugate landing.**  For a literal full-nine source, the unary or
> binary branches of (4) force palette/support descent, or the ternary branch
> forces the target-active rank-one cap in (4) to have zero clean error (or
> else exposes an occupied complete-derivative deletion/unit).

The shortest falsifiable attack is now to append the mixed row family
containing (21) to the null-contracted Hessian system and eliminate its first
clean-error coordinate.  A determinant/permanent expansion that does not
consume this extra word family cannot work, by (14)--(20).

## Reproduction

```text
python3 computations/verify_h3_singular_rank2_fullnine_null_adjugate_boundary.py --mode structural
python3 -O computations/verify_h3_singular_rank2_fullnine_null_adjugate_boundary.py --mode full
python3 -I -S computations/verify_h3_singular_rank2_fullnine_null_adjugate_boundary.py --mode exhaustive
```

All modes print the same frozen ledger digest.
