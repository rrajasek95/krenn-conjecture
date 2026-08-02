# An exact all-spokes L0-incidence survivor, excluded at L1

Research evidence only. Krenn's conjecture remains open and the certified
spine is unchanged.

## Outcome

The sole `1I+3R+2Z` all-spokes support envelope really does meet the
exceptional linear-incidence locus left by the preceding endpoint audit. An
exact one-cell repair gives

\[
\operatorname{rank}D=55,
\qquad \operatorname{rank}D_{\rm mixed}=53,
\qquad e_0,e_1\in\operatorname{im}D.                       \tag{1}
\]

Thus the rank-
\(55/53\) necessary locus is nonempty; it cannot be discarded as an artifact
of rank counting. The packet retains the selected generic-kernel equation,
exactly the five universal gauge directions, and literal R2 at every root.

It is nevertheless **not** a full endpoint survivor. The two overlapping L1
systems leave two genuine star modes apiece, but the enlarged span of all four
compatible factored products misses both pure targets. This exclusion also
holds on the packet's full nonzero local diagonal torus.

The independent companion checker is
[`verify_level_two_one_invertible_three_rank_one_all_spokes_incidence_survivor_l1_obstruction.py`](../computations/verify_level_two_one_invertible_three_rank_one_all_spokes_incidence_survivor_l1_obstruction.py).

## 1. Exact one-cell repair

Keep the endpoint matrices

\[
X_0=\begin{pmatrix}-1&2\\1&-1\end{pmatrix},\quad
X_1=\binom10(1,1),\quad
X_2=\binom01(1,2),\quad
X_3=\binom11(2,3),\quad X_4=X_5=0,             \tag{2}
\]

and potentials

\[
(\nu_0,\ldots,\nu_5)=(1,1,1,1,-1,-1).         \tag{3}
\]

The six core blocks are fixed by

\[
2M_{ru}=X_rJX_u^{\mathsf T}\qquad (0\le r<u\le3),           \tag{4}
\]

and `M_45=0`. Use the following eight free core-to-zero spokes:

\[
\begin{array}{c|cc}
ru&M_{ru}^{(0,*)}&M_{ru}^{(1,*)}\\ \hline
04&(1,85)&(0,87)\\
05&(84,87)&(0,28)\\
14&(0,74)&(0,66)\\
15&(0,76)&(37,0)\\
24&(0,46)&(0,23)\\
25&(56,0)&(0,0)\\
34&(0,0)&(29,0)\\
35&(0,51)&(0,96).
\end{array}                                                   \tag{5}
\]

The pinned reference packet differs only in `M_34(0,1)=3`. Changing that one
entry to zero has the exact effect

\[
\begin{array}{c|ccccc}
 &D&D_{\rm mixed}&[D\mid e_0]&[D\mid e_1]&[D\mid e_0,e_1]\\ \hline
\text{reference}&55&54&56&55&56\\
\text{repaired}&55&53&55&55&55.
\end{array}                                                   \tag{6}
\]

Every value in (6) is recomputed over
\(\mathbb Q,\mathbb F_{101},\mathbb F_{32003}\), and
\(\mathbb F_{1000003}\). The repair therefore crosses exactly onto the
necessary linear-L0 incidence profile: both pure targets acquire rational
preimages simultaneously.

## 2. Exact rank and incidence certificates

The checker pins a nonzero `55 x 55` minor of `D` and a nonzero `53 x 53`
minor of `D_mixed`. Their exact determinant digests are respectively

```text
1ac310b475bb7447b59363106fc7d45b168c66a1d005d53d4619acda8100ee33
ce0bef574a72a13560b3af6921c570dd45cd4273f2000611974cf17a697f271f
```

The row and column sets are hard-coded, and the determinants are recomputed
over the rationals rather than inferred from modular ranks. Five independent
vertex-gauge tangents lie in the kernel. The first minor shows that these
exhaust the kernel of the `64 x 60` differential.

Rational RREF with all free variables normalized to zero produces exact
preimages `K_0,K_1` satisfying

\[
DK_0=e_0,\qquad DK_1=e_1.                                  \tag{7}
\]

The two normalized solutions each use 36 cells and are pinned by independent
SHA-256 digests. Because the two pure coordinate rows are independent, (7)
also gives the conceptual upper bound
\(\operatorname{rank}D_{\rm mixed}\le53\); the pinned `53 x 53` minor makes
this an equality. This supplies both sides of every equality in (1), not just
a numerical rank report.

The generic-kernel identities

\[
X_rJX_u^{\mathsf T}=(\nu_r+\nu_u)M_{ru}                    \tag{8}
\]

hold block by block, and with `z=-2` the selected level-two equation is
checked in all 64 rows. The eight planned internal R2 witnesses on roots
`0,1,2,3` retain between 20 and 36 nonzero complementary cofactors. Roots
`4,5` have zero endpoint matrices and preserve their endpoint witness pair.

The canonical packet digest is

```text
85542405155ecda5e9069c80c075953b93eee812fb117d2492bc9f5a57309ebd
```

## 3. Full L1/factored compatibility still fails

For the P/V overlap solve, on all fifteen residual edges,

\[
P_rV_u^{\mathsf T}+V_rP_u^{\mathsf T}=\rho_{ru}M_{ru},      \tag{9}
\]

and solve the analogous Q/U system. Each rational coefficient matrix is
`60 x 27` of rank 24 and nullity 3. In each system one direction is the
vacuous scalar on the forced zero block `M_45`; the remaining star projection
has dimension two. All surviving star modes vanish at sites 4 and 5.

Form all four products of the two U modes with the two V modes and apply the
differential. Enlarging their span by the direct vector `Psi(M)` gives

\[
\begin{array}{c|ccccc}
&\text{products}&+\Psi(M)&+e_0&+e_1&+e_0,+e_1\\ \hline
\operatorname{rank}&4&4&5&5&6.
\end{array}                                                   \tag{10}
\]

The four-product span in (10) is already a linear enlargement of the genuine
bilinear compatible image. Since even that enlargement contains neither pure
target, no shared factored endpoint completion exists for this exact linear
survivor.

## 4. Covariant family and remaining frontier

For arbitrary nonzero diagonal matrices `A_r`, the transformation

\[
X_r\longmapsto A_rX_r,
\qquad M_{ru}\longmapsto A_rM_{ru}A_u                  \tag{11}
\]

preserves (8), endpoint ranks, R2, and all relevant incidences. The checker
audits the exact row/column covariance of all `64*60` differential entries at
a nontrivial rational torus point, then resolves both L1 systems and (10) on
the transformed packet. Consequently (1) supplies a full covariant family of
linear-L0 survivors, all excluded by the same L1/factored obstruction.

This does not close the entire rank-55/53 incidence locus in the all-spokes
envelope. It does two narrower things exactly: it proves that locus is
nonempty, and it closes the first explicit point and its diagonal torus after
the full overlapping endpoint equations are imposed. Other deformations of
the eight free spokes remain open.
