# Coincident-defect erasure leaves only the exact-six cycle

## 1. Result

The exact-six position audit leaves 256 labelled singular supports in three
orbits:

\[
\begin{array}{c|c}
\text{position graph}&\text{labelled supports}\\ \hline
K_{1,3}\sqcup K_{3,1}&16\\
K_{2,2}\ \text{plus a two-edge star and an empty row}&144\\
C_6\ \text{plus an empty row and column}&96.
\end{array}                                                \tag{1}
\]

**Theorem 1.1.**  The first two orbits in (1) cannot satisfy the full
two-`K_4` matching-tensor equations.  Consequently the only remaining
exact-six position orbit is the six-cycle with an empty block row and
column.

The new local input handles two pulled-back stars whose exceptional
components occur at the same physical site.  As in the separated-defect
case, its six-cell kernel is silent at that site and is incompatible with
the three endpoint colors of the standard right `K_4` quadratic.

The exact checker is
[`verify_two_k4_exact_six_coincident_defect_obstruction.py`](../computations/verify_two_k4_exact_six_coincident_defect_obstruction.py).

## 2. Coincident-defect erasure

Use the four-site square-zero algebra

\[
 \mathcal R=\bigotimes_{i=0}^3(\mathbb F\oplus V_i),
 \qquad V_i^2=0,\qquad\dim V_i=3,                       \tag{2}
\]

over a field of characteristic different from two.  Let `U,W` be
three-spaces and `U_0 subset U` a two-plane.  Suppose `P_i:U -> V_i` and
`S_i:W -> V_i` are isomorphisms for `i!=a`; their two components at `a`
are arbitrary.  Write

\[
                 p_\alpha=\sum_iP_i\alpha,
                 \qquad s_\beta=\sum_iS_i\beta.         \tag{3}
\]

**Lemma 2.1 (coincident defects).**  If `q in R_2` satisfies

\[
                    q p_\alpha s_\beta=0
           \qquad(\alpha\in U_0,\ \beta\in W),          \tag{4}
\]

then either `q=0` or

\[
                           q_{aj}=0\qquad(j\ne a).       \tag{5}
\]

If `P_aU_0=0`, the residual kernel is supported entirely on the triangle
complementary to `a`.  No assertion about its dimension is needed in the
application.

## 3. Proof of the local lemma

Relabel `a=0` and put `T_alpha=q p_alpha`.  Normalize
`S_1=S_2=S_3=I` and write `S_0=A`.  The almost-invertible-star
annihilator from
[`two-k4-exact-four-nonmatching-obstruction.md`](two-k4-exact-four-nonmatching-obstruction.md)
has two cases.

### 3.1. The exceptional component is nonzero

If `A!=0`, every `T_alpha` lies on one generalized-determinant line.  Its
component missing site zero is the full determinant tensor on sites
`1,2,3`, of mode rank three.  Since `U_0` has dimension two, choose
nonzero `alpha` with

\[
                             q p_\alpha=0.               \tag{6}
\]

If `P_0 alpha=0`, the sparse multiplication lemma says immediately that
all blocks of `q` incident with site zero vanish, giving (5).

Otherwise every component of `p_alpha` is nonzero.  The full-support
multiplication kernel has the form

\[
 q_{ij}=z_{ij}p_i\otimes p_j,qquad
 z_{ij}+z_{ik}+z_{jk}=0.                                \tag{7}
\]

For independent `alpha' in U_0`, the missing-zero component of
`q p_(alpha')` is supported in a two-plane at each of sites `1,2,3` and
hence has mode rank at most two.  It cannot be a nonzero member of the
determinant line, so `q p_(alpha')=0`.  The component on `123` kills
`z_12,z_13,z_23`; the four triangle equations in (7) then kill the three
remaining scalars in characteristic different from two.  Thus `q=0`.

### 3.2. The exceptional component is zero

If `A=0`, the common annihilator consists of cubics supported on the
triangle `123`.  Therefore the components of `q p_alpha` on the three
triples containing site zero vanish for every `alpha in U_0`.

Normalize the restrictions of `P_1,P_2,P_3` to `U_0`, and reduce
`P_0|U_0` to rank `d=0,1,2` normal form.  The three overlapping
two-plane Koszul equations have exact kernel dimensions

\[
\begin{array}{c|ccc}
d&0&1&2\\ \hline
\dim\text{ simultaneous kernel}&27&0&0.
\end{array}                                             \tag{8}
\]

For `d=0`, coefficient comparison first kills every block incident with
site zero; the entire 27-dimensional quadratic space on the complementary
triangle is invisible because neither inserted factor can occupy site
zero.  For `d=1,2`, the alternating boundary relations on the three
overlapping triples have zero common kernel.  Thus (8) gives (5) or `q=0`,
completing the proof of Lemma 2.1.

## 4. Effective-Hessian contradiction

Suppose two block rows `r,s` each contain at most one singular block and
their exceptional blocks lie in the same physical column `a`.  Let `0,t`
be the complementary left vertices, put `c=kappa(0t)`, and define

\[
 p_{i,x}=\sum_j\operatorname {row}_x(B_{ij})^{(j)},
 \qquad q_{\rm eff}=q_R+p_{0,c}p_{t,c}.                 \tag{9}
\]

For colors `x!=c` and arbitrary `y`, the nonconstant left word colored
`c` at `0,t` and `x,y` at `r,s` has unique compatible internal edge `0t`.
Its full matching equation is exactly

\[
                         q_{\rm eff}p_{r,x}p_{s,y}=0.    \tag{10}
\]

The hypotheses of Lemma 2.1 hold.  If `q_eff=0`, the identity
`q_R=-p_(0,c)p_(t,c)` puts all three incident right-`K_4` endpoint colors
at every site into a two-plane.  If instead the blocks of `q_eff` incident
with site `a` vanish, the identical contradiction occurs just at `a`.
The standard `K_4` uses its three distinct coordinate axes there, which
span dimension three.

Combining this with the separated-defect theorem gives the useful uniform
form:

**Proposition 4.1.**  No two block rows can each contain at most one
singular block.  The transposed assertion holds for block columns.

## 5. Exact-six consequences

For the first orbit in (1), take the representative

\[
 (0,1),(0,2),(0,3),(1,0),(2,0),(3,0).                  \tag{11}
\]

Rows 1 and 2 each have their sole singular block in column zero, so the
coincident form of Proposition 4.1 excludes it.

For the second orbit, take

\[
 (0,0),(0,1),(1,0),(1,1),(2,2),(2,3).                  \tag{12}
\]

Columns 2 and 3 each have their sole singular block in row 2.  Apply the
transposed proposition.  Thus only the six-cycle orbit survives.  Its row
and column degree partitions are both `(2,2,2,0)`, so it contains no pair
to which Proposition 4.1 applies.

## 6. Exact audit

Run

```text
python computations/verify_two_k4_exact_six_coincident_defect_obstruction.py
```

The checker verifies the kernel table (8), all twelve coincident-defect
rank normal forms, silence of every residual kernel at the exceptional
site, all 729 coefficients of (10) on a nontrivial
`K_(1,3) sqcup K_(3,1)` chart, and the exact orbit census

\[
                         16+144+96=256.                 \tag{13}
\]

The first 160 labelled supports are removed; the 96 labelled six-cycles
are the precise remaining exact-six position boundary.
