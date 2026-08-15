# Common-edge integrability kills the minimal dirty outside guard

## Result

The three-channel abstract counterguard of `00a1d52` cannot be realized by
literal eight-site edge matrices sharing one physical pair.

There are three exact obstructions, in increasing algebraic strength.

1. A two-site cap has only boundary degrees zero and two.  Its physical
   signature is `C0=s,C2=r`; `C4=C6=0`.  The guard has a nonzero `C6`.
2. Every coefficient slice of the physical second response `r` is a sum of
   two rank-one `3x3` matrices and therefore has determinant zero.  The guard
   identity `C2=-s x`, with direct block `I_3`, requires the slice `-I_3` at
   each live cell of `x`.
3. For the guard's literal mixed one-factor `x`, the actual pair-cap tensor
   has no pure output coordinate for arbitrary star matrices.  Contracting a
   full GHZ source by any diagonal cap coordinate must give the corresponding
   pure residual tensor.  Hence the realization contains three normalized
   pure source units `0=1`.

The second-response rank argument classifies every direct-block rank.  With
three disjoint live cells in `x`, realization is impossible for ranks three,
two, and one; at rank zero the direct scalar vanishes identically and activity
is impossible.

The exact checker is
[`verify_n8_common_edge_dirty_signature_realization_no_go.py`](../computations/verify_n8_common_edge_dirty_signature_realization_no_go.py).

## 1. Physical two-site boundary grading

Fix the physical cap pair `p,q` and let `U` be the other six sites.  Every
perfect matching of the eight sites has exactly one of two forms.

* It uses `pq`, followed by a perfect matching of `U`.
* It avoids `pq`, sending `p,q` to two distinct sites of `U`, followed by a
  perfect matching of the remaining four sites.

Thus the number of cap-to-boundary edges is zero or two.  Exact enumeration
of all 105 matchings gives

```text
boundary degree 0 : 15 matchings
boundary degree 2 : 90 matchings.
```

For a cap covector `K`, write

\[
 s(K)=\langle K,A_{pq}\rangle                              \tag{1}
\]

and let `r(K)` be the crossed two-site response.  The complete physical cap
identity is

\[
 K\mathbin{\lrcorner}H_8(A)
   =\left[s(K)\exp(x)+r(K)\exp(x)\right]_U
   ={s(K)x^3\over3!}+{r(K)x^2\over2!}.                    \tag{2}
\]

There are no physical `C4` or `C6` response layers for one pair.  Therefore
the guard assignment

\[
 C_6=\sum_i k_iX_i+{s\over3}x^3                          \tag{3}
\]

already fails the boundary grading.  This identifies why the earlier
signature was correctly scoped as abstract: its linear GHZ identity did not
encode the two-site matching partition.

## 2. First nonlinear common-edge identity

The grading obstruction is linear.  The first genuinely common-edge
polynomial identity occurs in `C2=r`.

For a residual pair `a,b` and endpoint colours `alpha,beta`, put

\[
 \begin{aligned}
 u_i&=A_{pa}(i,\alpha),&v_j&=A_{qb}(j,\beta),\\
 x_i&=A_{pb}(i,\beta),&y_j&=A_{qa}(j,\alpha).
 \end{aligned}
\]

The cap-matrix representing that one response coefficient is

\[
 R_{ab}^{\alpha\beta}=uv^T+xy^T.                         \tag{4}
\]

Consequently

\[
                  \boxed{\det R_{ab}^{\alpha\beta}=0}    \tag{5}
\]

identically.  The checker expands the determinant in the twelve independent
star coordinates and obtains the zero polynomial term by term.

If a physical realization satisfied

\[
                         r(K)=-s(K)x                    \tag{6}

for every `K`, coefficient comparison would give

\[
 R_{ab}^{\alpha\beta}
   =-x_{ab}^{\alpha\beta}A_{pq}.                        \tag{7}

Taking determinants in (5)--(7) yields the cellwise identity

\[
       \left(x_{ab}^{\alpha\beta}\right)^3
                         \det A_{pq}=0.                 \tag{8}

For the guard, `A_pq=I_3` and the three cells

```text
01;01, 23;20, 45;12
```

all have coefficient one.  Equation (8) reads `1=0` at each cell.  Thus the
dirty normal form fails already at the second Hasse response; no `C4/C6`
completion can repair it.

Equivalently, the common-edge four-site identity is

\[
 A_{pq}A_{ab}+A_{pa}A_{qb}+A_{pb}A_{qa}=0.              \tag{9}

Flattening (9) in `(p,q)|(a,b)` produces exactly (7).  This is the
source-valid shared-star integrability absent from the abstract guard.

## 3. Classification by the rank of the direct block

Write `D=A_pq` and suppose (7) is required on the three disjoint live edges
of `x`.

### Rank three

Every left side of (7) has rank at most two, while a nonzero multiple of `D`
has rank three.  Therefore even one live cell is impossible.

### Rank two

One live edge is possible and the bound is sharp.  If

\[
 B_{ab}=p_aq_b^T+p_bq_a^T                              \tag{10}
\]

has rank two, then `p_a,p_b` are independent and `q_a,q_b` are independent.
Let a third site `c` be cross-zero to both endpoints:

\[
 B_{ac}=B_{bc}=0.                                      \tag{11}
\]

If `p_c,q_c` are nonzero, the first equality in (11) forces
`p_c parallel p_a`, while the second forces `p_c parallel p_b`, a
contradiction.  If one is zero, either equality forces the other to be zero.
Hence

\[
                           p_c=q_c=0.                   \tag{12}
\]

Every site outside a live rank-two edge is star-zero, so there cannot be a
second live edge.  The guard needs three.

### Rank one

Rank one is subtler and the two-edge bound is sharp.  Put
`D=de^T`.  For a first live edge `0,1`, at least one of the pairs
`p_0,p_1` or `q_0,q_1` is dependent.  After exchanging the two endpoint
roles if necessary, write

\[
 p_0=d,\qquad p_1=\lambda d,qquad
 q_1+\lambda q_0=e.                                   \tag{13}

A site `c` cross-zero to both `0,1` satisfies

\[
 dq_c^T+p_cq_0^T=0,qquad
 \lambda dq_c^T+p_cq_1^T=0.                           \tag{14}

Subtracting `lambda` times the first equation gives

\[
                     p_c(q_1-\lambda q_0)^T=0.          \tag{15}

Generically (15) forces `p_c=q_c=0`.  The only nonzero case is the balanced
normal form

\[
 q_0={e\over2\lambda},\quad q_1={e\over2},\quad
 p_c=a_cd,\quad q_c=-{a_c\over2\lambda}e.              \tag{16}

For any two outside sites it gives

\[
                         B_{cd}=-{a_ca_d\over\lambda}D. \tag{17}

Thus one additional disjoint live edge is possible.  But two additional
edges `23` and `45` require all four parameters
`a_2,a_3,a_4,a_5` nonzero.  Equation (17) then makes the required cross-zero
`B_24` nonzero.  So rank one supports at most two of the three guard edges.

The checker gives exact rational sharpness examples for the rank-two
one-edge and rank-one two-edge bounds.

### Rank zero

If `D=0`, then `s(K)=<K,D>` vanishes for every cap covector.  No cap is
active, and the guard scalar `s=k_0+k_1+k_2` is not realized.

Combining the four cases proves that the three-disjoint-edge dirty signature
is unrealizable at every direct rank.

## 4. The terminal full-GHZ row is a source unit

The determinant obstruction already refutes (6).  There is an even earlier
terminal contradiction if one asks for the full GHZ tensor with the guard's
fixed internal edge family

\[
                         x=01;01+23;20+45;12.            \tag{18}

Its cube is

\[
                              x^3=6e_{012012}.           \tag{19}

Let `r` now be an **arbitrary** physical second response, with all

\[
                         15\cdot9=135                   \tag{20}

decorated residual coordinates allowed.  The checker multiplies every one
of those coordinates by `x^2`.  Twenty-seven products are nonzero and yield
25 distinct full words.  Every one is mixed.  This is immediate
structurally as well: every term of `x^2` contains two of the off-diagonal
edges in (18), so it already fixes unequal site colours.

Therefore the physical cap tensor (2) has zero coefficient at

```text
000000, 111111, 222222
```

for every possible choice of the star matrices.  On the other hand,
contracting the full eight-site GHZ identity with diagonal cap coordinate
`K_bb` gives `X_b` on the six residual sites.  The original source rows are

```text
00000000 : 0 = 1
11111111 : 0 = 1
22222222 : 0 = 1.                                      (21)
```

These are literal normalized pure source units.  The terminal alternative is
therefore a unit, not an active clean `K`; the proposed source does not exist
long enough to enter the clean-cap variety.

## 5. Scope and next residual family

This closes the exact minimal dirty guard.  It does not yet classify every
physical essential outside state.  A general source need not satisfy the
special proportionality `r=-s x`, and its internal `x` need not be the mixed
one-factor (18).

What survives is a much smaller, genuinely physical problem:

> classify essential outside channels whose complete second-response slices
> lie in the rank-at-most-two secant variety (5), with the top identity (2)
> and all three pure normalizations imposed.

The abstract `C4/C6` escape is gone.  Any next counterguard must be built from
literal star factors `A_pa,A_qa` and the physical formula (4).  A terminal-ear
or matching-covered argument is useful only if it controls how these shared
star vectors recur across different residual edges.

## Verification

```text
python3 computations/verify_n8_common_edge_dirty_signature_realization_no_go.py --mode structural
python3 -O computations/verify_n8_common_edge_dirty_signature_realization_no_go.py --mode full
python3 -I -S computations/verify_n8_common_edge_dirty_signature_realization_no_go.py --mode exhaustive
```

All modes have frozen ledger SHA-256
`38b836999bda8978c7dfb85bdf9678bedb713292c5cb7a60c35596986bc2eb4e`.
