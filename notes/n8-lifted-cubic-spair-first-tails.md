# The nine cubic tangent generators lift and close at first order

## Exact bounded statement

Write the relevant sparse tangent variables as

\[
 a=z_{3712},\qquad e=z_{1301},\qquad
 (r,s,t)=(z_{0420},z_{0421},z_{0422}).
\]

The reduced Gröbner basis of the 39 quadratic second-lift obstructions adds
exactly the nine monomials

\[
 a^2r,a^2s,a^2t,
 ar^2,ars,art,as^2,ast,at^2.
\tag{1}
\]

All nine have two-term lifts to the literal mixed-equation ideal.  If
\(Q_i\) denotes the full normal-eliminated lift of the correspondingly
numbered sparse quadratic, then the first three are

\[
 C_{40}=-aQ_{11}+eQ_{14},\qquad
 C_{41}=-aQ_6+eQ_{10},\qquad
 C_{42}=-aQ_1+eQ_5,
\tag{2}
\]

and the remaining six are

\[
\begin{aligned}
 C_{43}&=-tQ_{11}+z_{0402}Q_{32}, &
 C_{44}&=-tQ_6+z_{0401}Q_{32}, &
 C_{45}&=-tQ_1+z_{0400}Q_{32},\\
 C_{46}&=-sQ_6+z_{0401}Q_{28}, &
 C_{47}&=-sQ_1+z_{0400}Q_{28}, &
 C_{48}&=-rQ_1+z_{0400}Q_{24}.
\end{aligned}
\tag{3}
\]

Exact normal-coordinate elimination through cubic order verifies that the
first post-cancellation tail of every one of the 36 cubic-cubic critical
pairs reduces to zero by the 39 quadrics and the nine cubics (1).  These
tails occur in degrees five or six.  For the first genuinely coupled pair

\[
 S_{40,41}=sC_{40}-tC_{41},
\tag{4}
\]

the checker additionally lifts its first reduction and verifies that the
degree-six tail also reduces to zero.  Thus this pair closes through degree
six.

## What this says about an all-orders proof

The calculation exposes a much smaller target than another large pure jet.
Let

\[
 G=(Q_1,\ldots,Q_{39},C_{40},\ldots,C_{48}).
\]

An all-orders proof follows if the lifted critical-pair remainders can be
assembled into a finite vector identity

\[
 R=M(z)R+B(z)G,\qquad M(z)\in\operatorname{Mat}(\mathfrak m).
\tag{5}
\]

Indeed \(I-M\) is invertible over the completed local ring, so (5) gives
\(R\in(G)\).  This is the useful ``unit-loop'' formulation of the local
standard-basis problem: it replaces unbounded jet expansion by a finite
matrix certificate.  Equivalently, one may lift a Schreyer basis of the 48
tangent initial forms and show that all its remainders have such a
contracting reduction.

A precise complete-filtered version is useful.  Let \(g\) be the tangent
standard basis, \(G=g+\delta\) its normal-eliminated lift,
\(\Sigma\) a Schreyer matrix for \(g\), \(h\) the deterministic tangent
division homotopy, and \(\pi\) its standard-monomial projection.  A lifted
syzygy matrix has the form \(\Sigma+U\), where

\[
 U=-h\delta(\Sigma+U).
\tag{6}
\]

Because \(h\delta\) raises the filtration, (6) has the unique formal
solution

\[
 U=-(I+h\delta)^{-1}h\delta\Sigma.
\]

The complete all-orders obstruction is therefore

\[
 \boxed{\Omega=\pi\delta(I+h\delta)^{-1}\Sigma.}
\tag{7}
\]

The 344-pair audit proves that the lowest filtered coefficient of \(\Omega\)
is zero.  It does not prove \(\Omega=0\).  A finite remainder presentation
\(\Omega=M(z)\Omega\) with every entry of \(M\) in the maximal ideal would
finish the argument by completeness (equivalently Nakayama), and is the
exact matrix still missing from the unit-loop approach.

## Completion of the first-tail Schreyer audit

The companion checker

```sh
python3 computations/verify_n8_lifted_all_spair_first_tails.py
```

performs the same lift-then-reduce operation on every overlapping pair in
the other two classes.  There are 201 quadratic-quadratic overlaps and 107
quadratic-cubic overlaps.  All 308 first lifted tails reduce to zero.  The
remaining 540 quadratic-quadratic pairs and 244 quadratic-cubic pairs have
coprime leading monomials and are covered by Buchberger's product criterion.
Together with the 36 cubic-cubic pairs above, this is an exact first-tail
audit of all 344 nontrivial pair overlaps.

## Scope still open

The two checkers cover every critical-pair class through its first lifted
tail, but they do not yet produce the finite matrix (5).  For (4), the first
explicitly unverified tail is degree seven.  The zero first-tail reductions
for all 344 overlaps, and the extra closure through degree six for (4), are
evidence for a contracting closure, not by themselves an all-orders
membership proof.

The subsequent exact embedded-deformation calculation is recorded in
[`n8-cubic-deformation-class-radical-trivial.md`](n8-cubic-deformation-class-radical-trivial.md).
It shows that the compatible cubic tail is a genuine nonzero \(T^1\) class,
so formal rigidity does not supply (5).  Crucially, that class vanishes on
all five reduced Ferrers branches, making branchwise radical membership a
strictly smaller remaining target than full local ideal membership.

## Direct finite local-order experiment

There is also a finite ambient formulation with the 196 linear-pivot mixed
equations, 39 literal quadratic lifts, and nine compact cubics in the
original 252 translated variables.  Its input has 244 generators and 63,428
terms.  Guarded Singular runs with a local degree order over
\(\mathbb Q\), over \(\mathbf F_{32003}\), and with a local Rees parameter
all exceeded the exploratory memory cap before returning a basis.  The
guarded reproducer is

```sh
python3 computations/analyze_n8_ambient_local_standard_basis.py
```

This is a computational limitation, not evidence against the local
standard-basis statement.  Formula (7) explains the smaller object a custom
sparse implementation should compute instead of materializing the full
ambient Mora basis.

## Reproduction

```sh
python3 computations/verify_n8_lifted_cubic_spair_first_tails.py
```

All arithmetic is exact over \(\mathbb Q\); every \(Q_i\) retains literal
mixed-equation provenance through the existing cokernel back substitution.
