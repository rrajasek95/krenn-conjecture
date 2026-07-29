# Higher splits: the constant-core common-pole root bound

## 1. Result

Put

\[
 h=t-r-1,\qquad p=h+k,\qquad k\ge1.
\tag{1}
\]

Assume that all isolated-star pivots vanish.  Fix two exceptional value
classes \(A,B\), select respectively \(r,s\ge1\) labels from them, and put

\[
                         j=h-r-s\ge1.                     \tag{2}
\]

Suppose that there are at least \(2k+1\) further value classes \(x\) such
that \(A^rB^sx^j\) is available and its complement contains a singleton
value class.

**Theorem 1.1.**  This configuration is impossible on the
no-extra-singular stratum.

The selected core represents three value classes, so its Hermite residual
is a nonzero constant.  The common pole has order \(k+1\); its zero-residue
condition, as the role \(x^j\) moves, clears to a nonzero polynomial of
degree at most \(2k\).  The \(2k+1\) candidate values give too many roots.

For \(k=1\), this recovers the interchangeable-role part of
[the constant-core role-swap theorem](live-three-zero-higher-split-k1-constant-core-role-swap.md).
Unlike the unequal-role clause of that note, the present theorem is uniform
in \(k\).

## 2. The constant residual and common-pole coefficient

For a legal selection

\[
                            R_x=A^rB^sx^j,                 \tag{3}
\]

the simultaneous-Hermite singleton-row lemma gives a nonzero rational
dependence \(F_x=Q_x/D_x\).  Its complement has \(p+2\) labels.  Since
three value classes are represented,

\[
 \deg D_x=(k+1)+h+3=p+4,\qquad
 \deg Q_x\le p+2.                                         \tag{4}
\]

All \(p+2\) complementary row jets divide \(Q_x\), so

\[
                         Q_x=q_xP_{N_x},\qquad q_x\in\mathbb C^*.
\tag{5}
\]

Thus \(F_x=O(z^{-2})\).  Every selected exceptional pole has zero simple
residue, and there is no residue at infinity.  The residue at the only
remaining pole, \(-\mu\), therefore vanishes.

Write \(w=z+\mu\).  Relative to the full unselected exceptional multiset,
selecting \(j\) labels at \(x\) multiplies the regular common-pole cofactor
by

\[
 \rho_{j,x}(w)=
 {1\over(w-(x+\mu))^j(w+(x-\mu))^{j+1}}.                 \tag{6}
\]

All factors independent of the moving role, including the fixed roles at
\(A,B\), form a power series \(U(w)\) with

\[
                         U(0)\ne0.                        \tag{7}
\]

The scalar \(\rho_{j,x}(0)\) is structurally nonzero.  After dividing it
out, put

\[
 \widehat\rho_{j,x}(w)=
 \left(1-{w\over x+\mu}\right)^{-j}
 \left(1+{w\over x-\mu}\right)^{-(j+1)}.                 \tag{8}
\]

The residue at a pole of order \(k+1\) is the coefficient of \(w^k\) in
its regular cofactor.  Hence every candidate \(x\) satisfies

\[
                 [w^k]\,U(w)\widehat\rho_{j,x}(w)=0.      \tag{9}
\]

No denominator used here vanishes: structural admissibility gives
\(x\ne\mu\) and \(x+\mu\ne0\).  A possible zero exceptional value is a
singleton, can occur only when \(j=1\), and is harmless because then
\(\mu\ne0\).

## 3. The exact \(2k\) degree bound

Write

\[
 U(w)=\sum_{a\ge0}u_aw^a,\qquad
 \widehat\rho_{j,x}(w)=\sum_{\ell\ge0}r_\ell(x)w^\ell.
\tag{10}
\]

Each \(r_\ell(x)\) has denominator dividing
\((x^2-\mu^2)^\ell\).  Therefore

\[
 N(x):=(x^2-\mu^2)^k
       [w^k]\,U(w)\widehat\rho_{j,x}(w)                  \tag{11}
\]

is a polynomial satisfying

\[
                              \deg N\le2k.                 \tag{12}
\]

The essential point is that \(N\) is never the zero polynomial, regardless
of the fixed background \(U\).  As \(x\to\infty\),

\[
 r_\ell(x)=c_\ell x^{-\ell}+O(x^{-\ell-1}),               \tag{13}
\]

where

\[
\begin{split}
c_\ell
 &= [X^\ell](1-X)^{-j}(1+X)^{-(j+1)}\\
 &=(-1)^\ell\sum_{m=0}^{\lfloor\ell/2\rfloor}
             \binom{j+m-1}{m}\ne0.                       \tag{14}
\end{split}
\]

Indeed,
\((1-X)^{-j}(1+X)^{-(j+1)}
=(1-X^2)^{-j}(1+X)^{-1}\), and all terms in the last sum
have the same sign.

If the rational function before clearing in (11) were identically zero,
then

\[
 0=\sum_{\ell=0}^k u_{k-\ell}r_\ell(x).                  \tag{15}
\]

Letting \(x\to\infty\) first gives \(u_k=0\).  Multiplying successively by
\(x,x^2,\ldots,x^k\) and using (13)--(14) gives

\[
                   u_{k-1}=u_{k-2}=\cdots=u_0=0.          \tag{16}
\]

This contradicts (7).  Hence \(N\ne0\).

## 4. Root contradiction and audit

Equation (9) makes every candidate value a root of \(N\).  The values are
distinct and the clearing factor is nonzero at them.  At least \(2k+1\)
roots contradict (12), proving Theorem 1.1.

[verify_live_three_zero_higher_split_constant_core_common_pole.py](../computations/verify_live_three_zero_higher_split_constant_core_common_pole.py)
checks the normalized role factor and residue coefficient, the denominator
and degree bounds for \(1\le k\le8\), the nonzero asymptotic coefficients
(14), the triangular nonidentity argument, the possible zero class, and
the exact incremental profile counts in the first higher rows.
