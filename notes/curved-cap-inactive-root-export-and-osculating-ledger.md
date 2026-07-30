# Inactive clean roots export exact lower-colour or nilpotent packets

## 1. Outcome

The common-root problem on the active cap line has one useful exact
boundary which does not appear in a raw gcd statement.

Let an exact source on \(2m\ge8\) sites be capped at a physical pair,
leaving \(2h=2m-2\) sites, so \(h=m-1\ge3\).  On any affine cap line
\(K(w)\), write

\[
 s(w)=s_0+ws_1,\qquad r(w)=r_0+wr_1,\qquad
 T(w)=T_0+wT_1,
\]

and put

\[
 F(w)=s(w)x+r(w)=F_0+wF_1.
\]

The pair rows and the clean error are

\[
 s(w)x^{[h]}+r(w)x^{[h-1]}=T(w),                       \tag{1}
\]

\[
 {\cal E}(w)=F(w)^{[h]}-s(w)^{h-1}T(w).                \tag{2}
\]

Suppose \(w=0\) is a clean but inactive point.

* If \(s_0\ne0\), then the canonical effective quadratic
  \(y_0=F_0/s_0\) is already an exact source for the colours whose
  coefficients in \(T_0\) are nonzero:

  \[
                         y_0^{[h]}={T_0\over s_0}.       \tag{3}
  \]

  Thus a root on one diagonal activity hyperplane is not an amorphous
  exception: generically it exports an exact two-colour source.
* If \(s_0=0\), then the root exports the exact nilpotent response packet

  \[
              r_0x^{[h-1]}=T_0,\qquad r_0^{[h]}=0.       \tag{4}
  \]

  In particular, if \(T_0\ne0\), then \(r_0\ne0\).  The mechanism in the
  current curved guard, where both \(s_0\) and \(r_0\) vanish at a
  nonzero target, is therefore excluded by one transverse pair row of
  every exact source.

More is forced when the clean error has a repeated inactive root.  If
\({\cal E}(w)\) is divisible by \(w^\nu\), with
\(1\le\nu\le h+1\), then the first \(\nu\) explicit polarization
tensors in (7) below vanish.  The extreme
pure-activity case

\[
                         {\cal E}(w)=w^hR              \tag{5}
\]

is therefore an order-\((h-1)\) osculating packet, not merely a polynomial
whose roots happen to be badly placed.  At the first \(8\to6\) boundary,
an \(s=0\) pure-activity root satisfies

\[
 r_0^{[3]}=0,\qquad F_1r_0^{[2]}=0,\qquad
 F_1^{[2]}r_0=s_1^2T_0.                                \tag{6}
\]

This reduction does not yet prove an active root exists.  It replaces the
sharp guard by two source-compatible residuals: a lower-colour exact cap,
or a nonzero nilpotent Hermite packet.  Either can be coupled across two
curvature lines; the literal zero-data root of the guard cannot.

## 2. The exact jet ledger

Use the convention that \(\binom ab=0\) outside \(0\le b\le a\), and
omit the corresponding whole term before interpreting its powers.
Divided-power polarization gives

\[
 (F_0+wF_1)^{[h]}
   =\sum_{j=0}^{h}w^jF_1^{[j]}F_0^{[h-j]}.
\]

Hence the coefficient of \(w^j\) in (2) is

\[
\begin{aligned}
 J_j={}&F_1^{[j]}F_0^{[h-j]}\\
 &-\binom{h-1}{j}s_0^{h-1-j}s_1^jT_0
  -\binom{h-1}{j-1}s_0^{h-j}s_1^{j-1}T_1,
 \qquad 0\le j\le h.                                   \tag{7}
\end{aligned}
\]

Therefore

\[
 w^\nu\mid{\cal E}(w)\quad(1\le\nu\le h+1)
 \quad\Longleftrightarrow\quad
 J_0=\cdots=J_{\nu-1}=0.                               \tag{8}
\]

In particular, (5) is equivalent to

\[
 J_0=\cdots=J_{h-1}=0,\qquad J_h=R.                    \tag{9}
\]

No coordinate choice in the top tensor is involved.  Equations (7)--(9)
are tensor identities and retain cancellation among all matching terms.

At a root with \(s_0=0\), one has \(F_0=r_0\).  The \(j=0\) equation in
(9) gives \(r_0^{[h]}=0\).  Equation (1) at \(w=0\) gives the other half
of (4).  If \(h\ge3\), the next and penultimate jet equations reduce to

\[
 F_1r_0^{[h-1]}=0,\qquad
 F_1^{[h-1]}r_0=s_1^{h-1}T_0.                          \tag{10}
\]

For \(h=3\), these are exactly the last two equations in (6).

At a root with \(s_0\ne0\), \(J_0=0\) says

\[
 F_0^{[h]}=s_0^{h-1}T_0.
\]

Dividing by \(s_0^h\) proves (3).  An invertible diagonal change at one
remaining site normalizes every nonzero coefficient of \(T_0/s_0\).
This is the same endpoint normalization used in the exact clean-pair
descent theorem; zero target coefficients simply remain absent.

## 3. Specialization to the canonical curvature line

The canonical transition theorem supplies

\[
                         K(z)=E_{ab}+zI.                \tag{11}
\]

Its target coefficients are completely explicit.

If \(a\ne b\), then

\[
                         \kappa_0(z)=\kappa_1(z)
                         =\kappa_2(z)=z.                \tag{12}
\]

The colour-activity boundary is \(z=0\).  The curvature construction chose
\(A_{pq}(a,b)\ne0\), so \(s(0)\ne0\); a clean root there gives an exact
matching-base-locus quadratic \(y^{[h]}=0\).
The other possible inactive point is the unique zero of \(s(z)\).

If \(a=b\), then

\[
 \kappa_a(z)=1+z,\qquad \kappa_c(z)=z\quad(c\ne a).      \tag{13}
\]

There are two colour boundaries:

* \(z=0\) retains only \(X_a\);
* \(z=-1\) retains the other two pure targets with coefficient \(-1\).

Consequently a clean root at \(z=-1\) with \(s(-1)\ne0\) is an exact
binary cap.  If \(s(-1)=0\), it must instead satisfy

\[
 r(-1)x^{[h-1]}=-\sum_{c\ne a}X_c,\qquad
 r(-1)^{[h]}=0,                                        \tag{14}
\]

so \(r(-1)\ne0\).

For the
[full-good-fan curved guard](curved-full-good-fan-pure-activity-root-guard.md),
the line is \(E_{00}+zI\) and both \(s(-1)\) and \(r(-1)\) are zero.
Equation (14) pinpoints its failed transverse equation: the source side
vanishes while the exact target side is \(-X_1-X_2\).  Thus that guard is
sharp for curvature/Bianchi but cannot realize even the first inactive
packet required by the complete pair rows.

## 4. Exact remaining curved target

Let \(g(z)\) be the gcd of the coordinate polynomials of
\({\cal E}(K(z))\), as in
[the augmented-gauge criterion](augmented-e2-gauge-clean-cap-polynomial.md).
If \(g\) has a root outside the finite activity set, the exact clean-pair
theorem gives the desired \(N\mapsto N-2\) descent.  If \(g\) is
nonconstant but every root is inactive, Sections 1--3 export, at every
root, one of:

1. an exact unary/binary/base-locus effective quadratic;
2. a nonzero nilpotent response packet (4);
3. the higher jet equations (7) when the inactive factor is repeated.

The pure-activity-power endpoint is the maximal jet packet (9).  A
positive continuation can therefore target a concrete statement:
two curvature lines of one good fan cannot carry only mutually compatible
lower-colour/nilpotent packets while satisfying their common transverse
target rows.  This is smaller than proving an arbitrary vector-polynomial
common-root theorem and retains the exact source provenance.

No executable is needed: (7) is the divided-power binomial formula, while
(1), (3), and (4) are direct consequences of the already audited physical
pair-cap and exact clean-pair identities.
