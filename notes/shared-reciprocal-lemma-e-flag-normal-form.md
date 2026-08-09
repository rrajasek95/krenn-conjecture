# Lemma E reduces the shared-reciprocal goodness gap to two scalar-unit packets

## 1. Outcome

Let `pq,pr` be shared reciprocal selected rank-one arms of an exact ternary
matching source.  In endpoint order write

\[
 A_{pq}=\lambda E_{ba},\qquad A_{pr}=\mu E_{dc},\qquad a\ne c. \tag{1}
\]

The outer labels `a,c` are distinct because the two arcs leaving `p` are two
of its one-per-target-colour witnesses.  Lemma E gives the following exact
normal form.

1. If either deleted endpoint star of `pq` is singular, then `a=b` and
   `A_pq=lambda E_aa`; similarly a singular endpoint of `pr` forces `c=d`.
   Thus every non-diagonal reciprocal arm is automatically good at both
   endpoints.
2. One bad arm contributes one pure target term by itself.  Its complete
   pair response is the sum of the other two pure targets: this is exactly
   the unary-top scalar-unit / binary-response packet already isolated in
   [`scalar-unit-binary-residual-target-branch.md`](scalar-unit-binary-residual-target-branch.md).
3. If both arms are bad, their direct matching terms contribute two distinct
   pure targets separately.  Expanding the exact source at `p` leaves a
   single-colour remainder through the other `p`-ports.

The third statement is the useful new reduction.  It does **not** force an
adjacent cubic pair.  When both singular flags occur at the shared endpoint,
all remaining `p`-ports lie on the third target line; that line may be
distributed over two or more physical neighbours.  The checker freezes a
partially cofactor-faithful full-output packet with all four Lemma-E flags, full
three-dimensional endpoint spans, and four nonzero neighbours at each of
`p,q,r`.  It satisfies the displayed pure-deletion and output equations but
does not impose that the final two shared-site remainder cofactors arise from
the same block family.  The common five-site odd-star cofactors **are**
simultaneously realized by one literal internal block family.  Coupling them
to the remaining six-site cofactors is the exact source-level gate.

Consequently Lemma E alone does not prove the requested alternative

\[
 \text{both arms good}\quad\hbox{or}\quad
 \text{adjacent-cubic descent}.                              \tag{2}
\]

It replaces the goodness gap by two compact packets: the one-bad
scalar-unit packet and the two-bad single-colour port packet.

## 2. Why a bad coordinate arm is diagonal

Suppose first that `q` is essential at `p`.  Lemma E2 says that some nonzero
row of `A_pq` is a scalar multiple of the matching target coordinate row.
The coordinate matrix in (1) has only row `b` and only column `a`, so this is
possible only when `a=b`; the essential colour is then `a`.  Applying the
same argument to the transposed block at `q` gives the identical conclusion
when `p` is essential at `q`.  Hence either endpoint flag makes the whole arm
the diagonal unit

\[
                         A_{pq}=\lambda E_{aa}.          \tag{3}
\]

Lemma E3 simultaneously gives

\[
                  H_{B\setminus\{p,q\}}=\lambda^{-1}X_a. \tag{4}

\]

The direct-arm part of the full matching expansion is therefore literally

\[
       A_{pq}H_{B\setminus\{p,q\}}=X_a.                  \tag{5}

\]

No division by a residual tensor and no termwise noncancellation assertion is
used.  Exactness then says that all matchings not using `pq` sum to
`X_b+X_c`, for the two complementary colours.  This is the complete one-bad
normal form.

## 3. Two bad arms peel two pure targets

If both arms are bad, relabel the third colour by `t`.  Equations (3)--(5)
hold on both arms, with distinct colours `a,c`.  Expanding at the common site
`p`, with `C=B\setminus{p,q,r}`, gives the exact identity

\[
\begin{aligned}
 \Delta_{B,3}
 &=A_{pq}H_{B\setminus\{p,q\}}
   +A_{pr}H_{B\setminus\{p,r\}}
   +\sum_{x\in C}A_{px}H_{B\setminus\{p,x\}}\\
 &=X_a+X_c+\sum_{x\in C}A_{px}H_{B\setminus\{p,x\}}.
                                                               \tag{6}
\end{aligned}

\]

Thus

\[
             \boxed{\sum_{x\in C}A_{px}H_{B\setminus\{p,x\}}=X_t.}
                                                               \tag{7}

\]

This is stronger than a support count: it is a literal tensor identity from
the complete exact source.  The endpoint flags add the following row
conditions, also termwise:

| flag | Lemma-E1 consequence |
|---|---|
| `q` essential at `p` | row `a` of every `A_px`, `x!=q`, is zero |
| `p` essential at `q` | row `a` of every `A_qx`, `x!=p`, is zero |
| `r` essential at `p` | row `c` of every `A_px`, `x!=r`, is zero |
| `p` essential at `r` | row `c` of every `A_rx`, `x!=p`, is zero |

In particular, when both shared-endpoint flags are present, every `A_px` for
`x in C` has mode-`p` support in the line `span(e_t)`.  Equation (7) makes at
least one such block nonzero.

If exactly one of these residual blocks is nonzero, `p` has exactly three
nonzero incident blocks.  The equality case of the essential-subspace lemma
and the cubic-vertex theorem then make `p` a literal coordinate-cubic site.
If two or more are nonzero, the third line is distributed and `p` is not
cubic.  Even the first branch supplies an adjacent-cubic descent only after
one of its three neighbours is independently proved cubic.

## 4. Exhaustive flag classification

Record the flags in the order

```text
(q essential at p, p essential at q,
 r essential at p, p essential at r).
```

Modulo exchange of the two arms there are ten flag orbits:

| number of flags | orbits | bad-arm types |
|---:|---:|---|
| 0 | 1 | both arms good |
| 1 | 2 | one bad arm; flag shared or outer |
| 2 | 4 | one double-essential arm, or two singly bad arms in `PP`, `PO`, `OO` position |
| 3 | 2 | one double-essential arm plus one shared/outer flag on the other |
| 4 | 1 | both arms double-essential |

The weight-four orbit must not be silently omitted.  The exact four-site
one-factorization source has all four flags on two shared arms.  All its
sites are cubic, so it is consistent with adjacent-cubic descent, but it
proves that four flags are not forbidden by Lemma E or exactness as a formal
matter.  At order eight the four-flag case remains inside the two-bad packet
(6)--(7) until additional cofactor provenance is used.

At weight zero the committed
[`shared reciprocal flat bicase unit`](shared-reciprocal-flat-bicase-unit.md)
forces a nonflat transition; since both arms are good, this is the curved
doubly-good overlap branch.  Every positive-weight orbit has at least one
diagonal scalar-unit arm and therefore lands in one of Sections 2--3.

## 5. Compact counterguard and its exact scope

The checker uses `N=8`, colours `(a,c,t)=(0,1,2)`, and five common residual
sites.  The internal cells

```text
45:00, 67:00, 36:11, 57:11
```

simultaneously realize all five common odd-star cofactors `K_x`, with

\[
 A_{r3}K_3=X_0\quad\text{on }\{r\}\cup C,
 \qquad A_{q4}K_4=X_1\quad\text{on }\{q\}\cup C.        \tag{8}

\]

Two distinct `p`-ports, each carrying half of `X_2`, give (7).  Dummy blocks
whose selected formal cofactor is zero make the endpoint stars at `p,q,r`
full-dimensional and give each endpoint four nonzero physical neighbours.
All four E1 zero-row conditions hold.  The resulting formal expansion has
all 6,561 output coefficients of `Delta`, including all diagonal and
off-diagonal rows.

This is a **partially cofactor-faithful counterguard**, not a Krenn
counterexample.  The five `K_x` in (8) really are the deleted hafnians of
the displayed common internal family; however, the two half-`X_2` cofactors
in (7) are still formal and are not asserted to come from that same family.
The packet shows precisely
why row algebra, endpoint spans, and Lemma E do not by themselves force
cubicity: the missing theorem must use the common matching provenance to
couple (7) to (8), rule out the distributed third-line ports, or turn them
into a source descent.

The sharp next source-level target is therefore:

> **Distributed scalar-unit overlap lemma (open).**  In the two-bad packet
> (6)--(7), common hafnian provenance either concentrates the third-line
> remainder on a port adjacent to a cubic site, or produces an exact
> `N -> N-2` permanent-null completion.

For a one-bad orbit, the corresponding target remains the
anchor-preserving nine-row Hamiltonization/source-descent problem already
identified in the scalar-unit notes.  Repeating selected-graph or
endpoint-rank counts cannot close either packet.

## 6. Reproduction

```sh
python3 computations/verify_shared_reciprocal_lemma_e_flag_normal_form.py
python3 -O computations/verify_shared_reciprocal_lemma_e_flag_normal_form.py
```

The checker independently enumerates the ten flag orbits, verifies the
pure-deletion peeling identities and the four-flag relaxed packet over the
rationals, reconstructs all five odd-star cofactors from one internal block
family, and reconstructs the exact four-site four-flag source.
