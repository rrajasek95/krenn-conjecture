# Exact labelled GHZ normalization after the latent involution

## Result

The involution theorem of `0902a62`, audited physically in `1e17477`, keeps
only

\[
 C(P,S)\subseteq W=\operatorname{span}\{q^{[3]},X_0,X_1,X_2\}.
\]

There is a short exact condition which restores the labelled GHZ tensor in
the quotient by (q^{[3]}).  Let

\[
 X=\operatorname{span}(X_0,X_1,X_2),\qquad
 \overline W=W/\langle q^{[3]}\rangle.
\]

First require that the natural map (X\to\overline W) be injective.  This is
equivalent to

\[
 X\cap\langle q^{[3]}\rangle=0.                          \tag{1}
\]

There are two nondegenerate charts for (1): (q^{[3]}=0), when
(overline W=X), or (q^{[3]}\ne0) and

\[
 \operatorname{rank}(q^{[3]},X_0,X_1,X_2)=4.            \tag{2}
\]

A nonzero (q^{[3]}\in X) is a separate pure-target degeneracy; quotienting
then loses one target direction and the three-slice criterion below is not
applicable.

Assume (1), identify (overline W\) with the fixed labelled target (X), and
write

\[
 \overline C|_{P\times S}=B_0X_0+B_1X_1+B_2X_2,          \tag{3}
\]

where each (B_c:P\times S\to\mathbf Q) is a (3\times3) bilinear form.
Then there are bases (p_0,p_1,p_2) of (P) and (s_0,s_1,s_2) of (S)
such that

\[
 \overline C(p_i,s_j)=\delta_{ij}X_i                    \tag{4}
\]

if and only if

1. every (B_c) has rank at most one;
2. the three left factor lines span (P^*); and
3. the three right factor lines span (S^*).

In matrices, these are exactly

\[
 \operatorname{rank}B_c\le1\quad(c=0,1,2),              \tag{5}
\]

\[
 \operatorname{rank}[B_0\ B_1\ B_2]=3,                 \tag{6}
\]

and

\[
 \operatorname{rank}\begin{bmatrix}B_0\\B_1\\B_2\end{bmatrix}=3. \tag{7}
\]

The exact checker is
[`verify_h3_labelled_ghz_slice_normalization.py`](../computations/verify_h3_labelled_ghz_slice_normalization.py).
It verifies the criterion on a dense nonmonomial positive model and proves
that the 77-cell physical rootless guard fails it sharply.

## Basis-free proof

Regard (B_c) as a map (S\to P^*).  Under (5), a nonzero slice has the
form

\[
 B_c=\ell_c\otimes r_c,qquad
 \ell_c\in P^*,\quad r_c\in S^*.                       \tag{8}
\]

The column space of the horizontal concatenation in (6) is

\[
 \operatorname{span}(\ell_0,\ell_1,\ell_2).
\]

Its rank is three precisely when the three left lines are a basis of (P^*).
In particular, none of the slices can be zero.  Similarly, the row space of
the vertical stack in (7) is

\[
 \operatorname{span}(r_0,r_1,r_2),
\]

so (7) says that the right lines are a basis of (S^*).

Let (L=[\ell_0\ \ell_1\ \ell_2]) and
(R=[r_0\ r_1\ r_2]) in arbitrary starting bases.  Both are invertible.
With

\[
 G=L^{-\mathsf T},\qquad H=R^{-\mathsf T},               \tag{9}
\]

one has

\[
 G^{\mathsf T}B_cH=E_{cc}                               \tag{10}
\]

for all three labelled slices.  Thus (5)--(7) give coefficient **one**, not
merely an unspecified nonzero diagonal coefficient.  Conversely, (4)
plainly has three rank-one slices and both factor spans have rank three.

This also explains the scaling compatibility.  The factorization (8) is
unchanged by

\[
 \ell_c\mapsto t_c\ell_c,qquad r_c\mapsto t_c^{-1}r_c.
\]

After normalization, the residual source-basis freedom is

\[
 p_c\mapsto d_cp_c,qquad s_c\mapsto d_c^{-1}s_c.        \tag{11}
\]

It preserves (4) exactly.  There is no extra slice scalar invariant: the
three nonzero coefficients are absorbed by (9), and (11) is the remaining
three-dimensional torus.

## Polynomial equations appended to the involution system

Let (T) be a candidate involution on the six-dimensional latent space.
For an entirely polynomial formulation, adjoin (6\times3) matrices (U,V)
whose columns are bases of the (+1) and (-1) eigenspaces, together with a
left inverse for ([U\ V]):

\[
 TU=U,\qquad TV=-V,\qquad Z[U\ V]=I_6.                  \tag{12}
\]

On a quotient chart choose three target functionals (lambda_c) satisfying

\[
 \lambda_c(q^{[3]})=0,qquad
 \lambda_c(X_d)=\delta_{cd}.                            \tag{13}
\]

Then the literal slice matrices are

\[
 B_c=U^{\mathsf T}C_{\lambda_c}V.                       \tag{14}
\]

The closed part of the normalization ideal consists of the 27 two-by-two
minors of the three matrices in (14).  The open part is

\[
 I_3([B_0\ B_1\ B_2])\ne0,qquad
 I_3([B_0;B_1;B_2])\ne0.                               \tag{15}
\]

Each determinantal ideal in (15) has 84 maximal minors.  One may either
split into minor charts, or encode the union of charts without choosing a
minor by adjoining variables (y_m,z_n) and the two equations

\[
 \sum_m y_m\Delta_m=1,qquad
 \sum_n z_n\nabla_n=1.                                 \tag{16}
\]

Equivalently, one may skip (5)--(7) and adjoin invertible (G,H) directly,
with

\[
 G^{\mathsf T}B_cH=E_{cc}\quad(c=0,1,2).                \tag{17}
\]

Equations (12)--(17) are a finite exact augmentation of the involution
system.  Unlike an ordinary Plücker resultant, they retain all three fixed
target labels simultaneously.

## Allowed labels and forbidden target mixing

The target basis ((X_0,X_1,X_2)) is physical and fixed.  The allowed
changes in the criterion are arbitrary choices of bases in (P) and (S),
followed after (4) only by the diagonal torus (11).

A colour symmetry is one **simultaneous** permutation of

\[
 (p_0,p_1,p_2),\qquad(s_0,s_1,s_2),\qquad(X_0,X_1,X_2).
\]

If the target labels are held fixed, even that permutation is only a
renaming, not an additional continuous basis change.  An arbitrary
(mathrm{GL}_3) transformation of the target is not allowed.  The checker
starts from the normalized slices (E_{00},E_{11},E_{22}) and applies the
invertible target shear whose first new slice is (E_{00}+E_{11}).  Its rank
is two, showing explicitly that slice rank one is not invariant under target
(mathrm{GL}_3) mixing.

## The 77-cell physical guard fails

Use the literal near-source from `74d4d7b` at endpoints

\[
 (p,q)=(2,3),\qquad U=(0,1,4,5,6,7).
\]

The combined endpoint-star rank is six, its chosen (E_{01}+zI) line is
rootless, and

\[
 \operatorname{rank}(q^{[3]},X_0,X_1,X_2)=4.
\]

The physical quotient slices are exactly

\[
 B_0=0,\qquad B_1=0,\qquad B_2=E_{22}.                  \tag{18}
\]

Thus their ranks are ((0,0,1)), while both concatenation ranks in (6)--(7)
are one.  All 27 closed minors vanish—the guard passes the rank-at-most-one
equations—but it fails both load-bearing rank-three opens.  This is the exact
normalization information discarded by coarse containment and the
anticommutator equations.

## Separate next layer: direct matrix and scalar-zero compatibility

Assume now the nonzero, independent (q^{[3]}) branch.  After (4), coarse
containment has the unique form

\[
 C(p_i,s_j)=\delta_{ij}X_i+d_{ij}q^{[3]}.                \tag{19}
\]

The full-nine equations require the common direct matrix

\[
 a_{ij}=-d_{ij}                                         \tag{20}
\]

to be the literal endpoint block in the same recovered labelled bases.  This
condition is not contained in (5)--(7).

Let the cross block of the response form (J) in those bases be (K).  For
fixed selected labels (a,b), the physical scalar-zero member must satisfy

\[
 K=\operatorname{tr}(a)E_{ab}-a_{ab}I.                  \tag{21}

Equation (21) must be tested on the residual scaling orbit (11); a generic
choice in that torus does not preserve a fixed off-diagonal selected line.
In the bilinear-form convention of `0902a62`, introduce (d_i,e_i) with
(d_ie_i=1).  The exact polynomial equations are

\[
 d_ie_jK_{ij}
 =\operatorname{tr}(a)\delta_{ia}\delta_{jb}
  -d_ae_ba_{ab}\delta_{ij}                              \tag{22}
\]

for all (i,j).  The checker freezes a nonsingular synthetic instance of
(21) and verifies that a generic residual scaling fails (22), preventing this
next compatibility from being treated as automatic.

Equations (20)--(22) are deliberately a separate layer.  The proved theorem
of this note is the exact quotient normalization (5)--(7).  The cases
(q^{[3]}=0) and nonzero (q^{[3]}\in X) must also be split before using
(19)--(22).

## Reproduction

The exact standard-library checker passes normal, optimized, isolated,
no-site, isolated-no-site, and byte-compilation modes.  Its frozen ledger
digest is

```text
8dca337e2e7aa9b24dd5bad0413b8294f7b2d432e8e923562683a4ed8aaaab1f
```
