# Universal occurrence shear and the physical toric lift gate

## Result

The universal centered response deformation has a global, canonical
trivialization on the free ninety-occurrence coordinate space.  It does not
have a strict presentation-preserving lift through the physical
`p,s,q` monomial algebra.  The first obstruction is a literal homogeneous
`2 x 2` toric minor, before any target, anchor, `q`, ridge, eta, or sigma
readout can be pulled back.

This corrects the interpretation of the universal-family frontier.  There is
no abstract Cech or monodromy obstruction.  The missing theorem is a
*physical multiplicative comparison* for the centered Tate generator, not a
splitting of the free occurrence family.

The exact certificate is

```text
computations/verify_h3_universal_occurrence_shear_physical_toric_lift_gate.py
```

with frozen ledger digest

```text
1ed6491c0446cf0f77f811091c5ade86d5d79b0298013b1ec479441ea724e59f
```

## 1. The free shear is globally trivial

Let `u` be the column of the ninety formal occurrence coordinates,
`R=1^T u`, and let `z` be centered: `1^T z=0`.  Define

\[
 M_z=I-\mathbf1z^T.
\]

The matrix determinant lemma and `z^T 1=0` give

\[
 \det M_z=1,
 \qquad M_z^{-1}=I+\mathbf1z^T,
 \qquad
 \mathbf1^TM_zu=R-90z^Tu.
\]

For every site permutation `P`,

\[
 M_{Pz}=PM_zP^{-1}.
\]

Thus the free occurrence family is globally and `S_6`-equivariantly
trivial.  Choosing an unmarked occurrence chart is unnecessary, and there
are no transition functions or Cech monodromy to kill at this level.

## 2. The first physical obstruction is a toric conormal

The occurrence coordinates are not free in the physical source.  They are
degree-four monomials in shared coefficient variables.  Set

\[
 A=p_0s_1,
 \quad B=p_1s_0,
 \quad x=q_{23}q_{45},
 \quad y=q_{24}q_{35}.
\]

Four literal occurrences obey the physical toric identity

\[
 u_{(0,1;24|35)}u_{(1,0;23|45)}
 -u_{(0,1;23|45)}u_{(1,0;24|35)}=Ay\,Bx-Ax\,By=0. \tag{1}
\]

Both terms in (1) have exactly the same literal factor multiset: two `p`,
two `s`, and the same four `q` factors.  Therefore (1) is homogeneous in the
full physical word, fine, and repeated-edge grading; forgetting a grade is
not responsible for the obstruction.

The conormal of (1) evaluated on the constant occurrence direction is

\[
 k=Ay+Bx-Ax-By=(B-A)(x-y).                            \tag{2}
\]

For an infinitesimal rank-one shear

\[
 D(u_M)=-L,
 \qquad L=z^Tu,
\]

Leibniz gives

\[
 D(\text{minor})=-Lk.                                 \tag{3}
\]

Equation (3) is generically nonzero.  For the selected centered direction
`z=e_f-1/90`, its sparse polynomial expansion has 347 monomials; even the
two-coordinate centered direction `e_Ax-e_By` gives a six-monomial nonzero
witness.  Hence `M_z` does not preserve the physical monomial graph ideal
and cannot descend to a strict `p,s,q` algebra automorphism.

This failure precedes all augmented rows.  Until (3) is homotoped, the
purported source map has no well-defined target, anchor, physical `q`, ridge,
eta, or sigma pullback.

## 3. It is not the endpoint `C2,C3` curvature

The complete `S_6` orbit of (2) has ninety oriented elements and rank thirty.
It lies in the matching-standard sector:

\[
 (A_{\rm match}+I)k=0.                               \tag{4}
\]

By contrast, the two target-zero endpoint private curvatures satisfy

\[
 (A_{\rm match}+I)C_i=3C_i.                          \tag{5}
\]

The checker finds `rank(k,C2,C3)=3`.  Thus the toric conormal is neither
`C2` nor `C3`, and the coefficient-only endpoint/matching factorization does
not supply its proper face.  The two packages occupy disjoint matching
eigenspaces.

The prototype `k` is odd under both the endpoint-role site transposition
`(0 1)` and the tail matching transposition `(3 4)`.  This explains why the
aggregate matching face kills it, but killing its linear symbol is not the
same as preserving the nonlinear source relation (1).

## 4. Derived and fixed-fibre meanings

On the universal moving-parameter action groupoid, `L=z^Tu` is invariant
under simultaneous transport of `z` and `u`, while `tau*k=-k`.  Over
characteristic zero,

\[
 d[\tau\mid Lk]=-2Lk.
\]

So the minor is Maschke-contractible in that orbit-relative object.  This
does not contract the selected fixed fibre: `tau` also moves the marked
parameter.  It is exactly the same scope distinction as the committed
semidirect matching-bar guard.

More importantly, if a physical multiplicative Tate comparison is built
with

\[
 d\epsilon=L,
\]

then Leibniz forces the needed proper face:

\[
 d(-\epsilon k)=-Lk.                                 \tag{6}
\]

Thus the rank-thirty toric orbit is not a second independent
conjecture-level generator.  It is a compulsory higher face of the one
centered comparison generator.  A merely linear occurrence-module section
is insufficient; the section must be termwise and multiplicative on the
physical source presentation.

## Shortest remaining theorem

Construct the universal centered generator `epsilon` as a pointed,
termwise multiplicative map into the complete physical AugP2/E14 source,
with its literal word/fine/repeated grade.  Then (6) supplies the toric
proper face, the normalized action-groupoid bar supplies the moving-orbit
matching isotropy, and the existing `B`-natural and `D4` identities transport
the endpoint and target faces.  The physical `q`, cap/ridge, and terminal
rows remain downstream typing obligations of this single comparison.

Scope is canonical `h=3` over the characteristic-zero theorem field.  No
strict `p,s,q` lift, fixed-selected-fibre bar contraction, augmented physical
comparison, or uniform-in-`h` theorem is claimed.

## Verification

Run normally, optimized, and isolated/no-site.  Expected headline:

```text
free occurrence shear: global, det 1, S6-equivariant
strict physical p,s,q lift: NO (-L*(B-A)*(x-y))
toric proper face: matching-standard rank-30 orbit, not C2/C3
multiplicative physical epsilon: would fill face automatically
```
