# Every rank-six completion fails the first two pure rows and one mixed row

## Result

The all-split obstruction in `a5c61ce` extends to every nondegenerate
rank-six site-diagonal completion of the scalar-zero response guard.
The particular rank-one polarization identity used there is not invariant
under changing the completion.  Nevertheless, the physical rows

\[
 C_{000000}(P,S)=E_{00},\qquad
 C_{222222}(P,S)=E_{22},\qquad
 C_{002101}(P,S)=0                                  \tag{1}
\]

are incompatible with the five fixed response edges in every completion.
Thus there is no smallest completion to carry on to the remaining six pair
rows: the first three already give a completion-independent contradiction.

The exact checker is
`computations/verify_h3_scalar_zero_packet_rank6_completion_obstruction.py`.

## 1. Exhaustive active completion coordinates

Only ten response ports occur in the contracted quadratic.  Name them

```text
site 0: a=x00, g=x01, i=x02
site 1: b=x10, h=x11
site 2: c=x20, j=x22
site 3: e=x30
site 4: d=x40
site 5: f=x50.
```

Their five prescribed pairings are

\[
 \langle a,d\rangle=\langle g,h\rangle
 =\langle i,j\rangle=\langle b,e\rangle=1,
 \qquad \langle c,f\rangle=-1,                       \tag{2}
\]

and every other pairing between different physical sites is zero.  Pairings
within one site are precisely the free site-diagonal completion entries.

Order the active ports in four groups

\[
 x=(a,g,i),\quad y=(d,h,j),\quad z=(b,c),\quad w=(e,f).
\]

Every active symmetric completion, with no quotient or genericity
assumption, has the unique block form

\[
G=\begin{pmatrix}
 A&I&0&0\\
 I&D&E&0\\
 0&E^{\mathsf T}&B&F\\
 0&0&F^{\mathsf T}&W
\end{pmatrix},                                       \tag{3}
\]

where

\[
\begin{gathered}
A=A^{\mathsf T}\in\operatorname {Mat}_3,\qquad
D=\operatorname {diag}(\delta,\eta,\theta),\\
E=\begin{pmatrix}0&0\\ \beta&0\\0&\gamma\end{pmatrix},
\quad B=\operatorname {diag}(\rho,\sigma),
\quad F=\operatorname {diag}(1,-1),
\quad W=\operatorname {diag}(\epsilon,\phi).
                                                               \tag{4}
\end{gathered}
\]

These are exactly fifteen free parameters: six in `A`, three in `D`, two
in `E`, and four in `B,W`.

Two explicit invertible row and column operations reduce (3) to five pivot
rows plus

\[
 R=\begin{pmatrix}
 I-DA&-EFW\\
 -E^{\mathsf T}A&F-BFW
 \end{pmatrix}.                                      \tag{5}
\]

Consequently

\[
                         \operatorname {rank}G
                   =5+\operatorname {rank}R.          \tag{6}
\]

The checker verifies the two matrix equivalences symbolically in the full
polynomial ring over all fifteen parameters.  This is the promised
exhaustive completion parameterization, not a sample of charts.

The ten active ports always have rank at least five.  A full latent lift of
rank six therefore has exactly two cases:

1. `rank R=1`: the active ports already span the latent six-space;
2. `rank R=0`: the active block is a nondegenerate five-space and the silent
   ports add exactly one orthogonal completion direction.

Conversely, every rank-six completion restricts to one of these two active
cases.  Silent ports have zero prescribed pairing outside their own site;
their remaining same-site entries are precisely a site-local Gram extension.
Modulo congruence, the second case is a one-dimensional nondegenerate
stabilization.  The obstruction below works in the full six-space and hence
does not distinguish these two cases.

## 2. The old rank-one identity is completion-dependent

The identity in `a5c61ce` used the fact that the two ports in each relevant
pure cofactor were proportional in its chosen lift.  This need not hold.

For example set

\[
 A=D=I_3,\quad E=0,\quad
 B=\operatorname {diag}(0,1),\quad
 W=\operatorname {diag}(0,1).                         \tag{7}
\]

Then `rank R=1` and `rank G=6`.  The pair `b,e` has Gram matrix

\[
                         \begin{pmatrix}0&1\\1&0\end{pmatrix},
\]

so the global form

\[
 C_{000000}=b\otimes e+e\otimes b
\]

has rank two, rather than being a square of one covector.  Thus the earlier
three-form Laurent identity is not an invariant of all completions.

## 3. The three physical rows force an isotropic plane

Fix any completion and any complementary Lagrangian split `L=P+S`.  Write

\[
 b=(x,y),\qquad j=(u,v),qquad x,u\in P^*,\ y,v\in S^*.
\]

The mixed equation in (1) is

\[
                         xv^{\mathsf T}+uy^{\mathsf T}=0. \tag{8}
\]

The two pure equations say, for the corresponding mates `e,i`,

\[
 C(b,e)=E_{00},\qquad C(i,j)=E_{22}.                  \tag{9}
\]

Because the row and column axes in (9) are distinct, (8)--(9) imply

\[
 \langle b,b\rangle=\langle j,j\rangle
 =\langle b,j\rangle=0,                              \tag{10}
\]

and `b,j` are linearly independent.  A short intrinsic proof is as follows.
If one projection of `b` vanishes, (8) puts `j` in the same Lagrangian and
the distinct matrix-unit axes make them independent.  Otherwise (8) gives
`u=lambda*x` and `v=-lambda*y`.  Rank one in the first pure row forces one
of `x,y` onto the `0` axis; rank one in the second forces the other onto the
distinct `2` axis.  Hence `x.y=0`, proving (10), and the sign change makes
`b,j` independent.

The checker independently verifies this implication by an exact Groebner
replay over the 27 entries of (8)--(9): both norms reduce to zero in a
127-element reduced basis.  Adjoining the equations `j=lambda*b` makes the
ideal the unit ideal.

Let `e` and `i` be the pure mates.  The physical response pairings give

\[
 \langle b,e\rangle=\langle j,i\rangle=1,qquad
 \langle b,i\rangle=\langle j,e\rangle
 =\langle e,i\rangle=0.                              \tag{11}
\]

Thus

\[
 U=\langle b,j,e,i\rangle
\]

is a nondegenerate four-space.  In that basis its Gram matrix is

\[
 \begin{pmatrix}
 0&0&1&0\\0&0&0&1\\1&0&\epsilon&0\\0&1&0&\phi
 \end{pmatrix},                                      \tag{12}
\]

whose determinant is one for arbitrary same-site norms.

## 4. The two remaining leaves kill the completion

Put `W=U^perp`.  Since the full latent space is nondegenerate of dimension
six, `W` is nondegenerate of dimension two.

The leaf response ports `d=x40` and `f=x50` are orthogonal to all four
vectors in `U`, hence lie in `W`.  They are nonzero because they pair with
their mates `a,c`, and

\[
                              \langle d,f\rangle=0.    \tag{13}

The port `g=x01` is orthogonal to `b,j,e,d,f`; its `U`-component is therefore
a multiple of `j`.  The port `h=x11` is orthogonal to `j,e,i,d,f`; its
`U`-component is a multiple of `e-epsilon*b`.  These two lines are mutually
orthogonal by (12).

Their `W`-components are both orthogonal to `d,f`.  If `d,f` are independent,
they span `W`, so both components vanish.  If they are dependent, (13) makes
their common line isotropic; in a nondegenerate two-space its orthogonal is
the same line, so the two components are again mutually orthogonal.  Hence

\[
                              \langle g,h\rangle=0.    \tag{14}

But the fixed response contains the edge `x01*x11` with coefficient one.
Thus (14) contradicts the original physical quadratic.

This contradiction uses every possible site-diagonal completion and both
silent-extension cases.  It also shows why testing the remaining six pair
rows is unnecessary.

## Scope and reproduction

The theorem classifies all symmetric completions at the active-port level,
including the active-rank-five stabilization boundary, and proves that no
nondegenerate rank-six full completion satisfies (1).  It does not classify
higher-rank latent factorizations; those are not three-channel response
factorizations.

```text
python3 computations/verify_h3_scalar_zero_packet_rank6_completion_obstruction.py --mode structural
python3 -O computations/verify_h3_scalar_zero_packet_rank6_completion_obstruction.py --mode full
python3 -I -S computations/verify_h3_scalar_zero_packet_rank6_completion_obstruction.py --mode exhaustive
```

All modes return the same frozen ledger digest.
