# Reciprocal coordinate blocks do not alone give hafnian Schur descent

## Sharp uniform packet

Let an exact (d)-colour matching source on
(B=\{p,q\}\sqcup W), (|W|=2h), have residual quadratic (Q).  For an
endpoint bilinear covector (K), put

\[
 s=\langle K,A_{pq}\rangle
\]

and let (R_K) be the quadratic first jet on (W): on a residual pair
(u,v), its block is the sum of the two ways of matching (p,q) separately,

\[
 (R_K)_{uv}=K\mathbin{\lrcorner}
 \left(A_{pu}\otimes A_{qv}+A_{pv}\otimes A_{qu}\right).
\]

The endpoint cap identity is

\[
 s\,H_W(Q)+D H_W(Q)[R_K]
   =\sum_c\kappa_c(K)X_c,
 \qquad \kappa_c(K)=K(e_c,e_c).                    \tag{1}
\]

If (s\ne0), the unique sign of the natural hafnian Schur update which
matches the constant and one-insertion terms is

\[
                         Q_K=Q+s^{-1}R_K.           \tag{2}
\]

Multiaffinity gives the exact (N)-independent formula

\[
 H_W(Q_K)=s^{-1}\sum_c\kappa_cX_c
   +\sum_{j=2}^{h}s^{-j}R_K^{[j]}Q^{[h-j]}.          \tag{3}
\]

Thus the desired (N\mapsto N-2) construction is equivalent to controlling
the higher-insertion tail in (3).  A literal reciprocal witness pair makes
(A_{pq}=\lambda e_b\otimes e_a) and supplies a nonzero cofactor, so an
appropriate coordinate cap has (s\ne0).  It does **not** force any of the
two-or-more-insertion permanents in (3) to vanish.

The sign-reversed determinant-style update fails even earlier: it has the
wrong one-insertion term in (1).  This sign convention accounts for the
apparent minus sign in matrix Schur-complement notation.

## Smallest endpoint-colour countermodel

The exact rational binary source from `pair-covector-selection-obstruction.md`
realizes

\[
                        H_6(A)=e_0^{\otimes6}+e_1^{\otimes6}.
\]

Its edge (13) is

\[
                         A_{13}=-e_1^{(1)}\otimes e_0^{(3)}.
\]

The complementary four-site cofactor is nonzero.  Therefore the edge is a
literal reciprocal witness: (1\to3) has head colour (0), while
(3\to1) has head colour (1).  In fact every displayed source edge has a
nonzero complementary cofactor.

Write a completely general endpoint covector as

\[
 K=(k_{ij})_{i,j=0,1}.
\]

Then

\[
 s=-k_{10},\qquad \kappa_0=k_{00},\qquad\kappa_1=k_{11}.
\]

On (W=(2,4,5,6)), exact enumeration of the first jet gives

\[
 H_W(R_K)=k_{10}k_{11}
 e_1^{(2)}e_0^{(4)}e_1^{(5)}e_1^{(6)}.
\]

Since (h=2), this is the entire higher tail.  The Schur-updated four-site
source therefore has the mixed coefficient

\[
                    s^{-2}k_{10}k_{11}={k_{11}\over k_{10}}. \tag{4}
\]

Seeing the reciprocal block and retaining both target colours requires
(s\kappa_0\kappa_1\ne0), under which (4) is nonzero.  Hence no completely
general covector cap produces an exact two-colour descent from this
reciprocal pair.  The obstruction is the first (2\times2) insertion
permanent, not a poor choice of cap or a missing scalar normalization.

## Consequence and scope

The strongest safe conclusion is:

> A tensor-active literal reciprocal coordinate block supplies the linear
> hafnian Schur packet (1), but does not by itself annihilate the higher
> insertion tail.  Reciprocal-block descent requires additional global
> source provenance.

This is an exact source counterguard over (mathbb Q), hence over
(mathbb C), but it is binary.  It is not a ternary Krenn counterexample and
does not rule out a theorem using the third-colour equations, another pair,
or a modification not determined by the local Schur packet.  It does rule
out closing the reciprocal branch from literal reciprocity, activity, and
the endpoint cap equations alone.

The remaining uniform target is consequently sharper: use simultaneous
ternary full-nine/source grading to prove that the tail in (3) vanishes or
is a pure rescaling for at least one reciprocal pair.  The majority-cubic
proof succeeds precisely because its coordinate port rows make the only
possible two-insertion permanents cancel; reciprocity supplies no analogous
port geometry.

## Reproduction

```
/Users/rishi/.venv/bin/python3 computations/verify_reciprocal_coordinate_schur_descent_counterguard.py
/Users/rishi/.venv/bin/python3 -O computations/verify_reciprocal_coordinate_schur_descent_counterguard.py
```

Both modes must print ledger SHA-256
`1aa67bccbbb925930fe260408fe359825e38cd27898c6dfdafcde6b46d20499c`.
