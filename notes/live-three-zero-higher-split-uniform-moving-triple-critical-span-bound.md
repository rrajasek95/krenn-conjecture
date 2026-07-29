# Higher splits: a uniform critical moving-triple span bound

## 1. Statement

Let \(r\ge4\), and work at the first row-relation mass threshold

\[
                         p=r(r+3).                            \tag{1}
\]

Consider an exact moving-triple common-lift family.  Restoring the moving
triple gives a common baseline of mass

\[
                      p+2=(r+1)(r+2)                         \tag{2}
\]

on \(c\) value classes, all of multiplicity at most \(r\).  For every
moving value \(i\) whose selected row kernel has the maximal possible
dimension \(r+2\), the relation space and its quartic transport are

\[
\begin{aligned}
 \mathcal S_i&\subseteq\mathbb C[z]_{\le c-4},
       &\dim\mathcal S_i&=r,\\
 B_i&=(z-i)^2(z+i)^2,
       &B_i\mathcal S_i=\mathcal T_i&\subseteq\mathcal K
                                   \subseteq\mathbb C[z]_{\le c}.
                                                               \tag{3}
\end{aligned}

Here “exact common lift” includes the following essential baseline-row
hypothesis.  If the restored multiplicities are
\(m_1,\ldots,m_c\), then \(1\le m_\nu\le r\),
\(\sum_\nu m_\nu=(r+1)(r+2)\), and \(\mathcal K\) is annihilated at
the corresponding distinct nodes by the exact order-\(m_\nu\) rows with
locally invertible coefficients.  These are the rows used in the
Wronskian estimate below; the containments displayed in (3) alone would
not imply the theorem.
\]

Distinct moving values are nonzero and pairwise nonopposite.

**Theorem 1.1 (critical span bound).**  If

\[
                              c=r+5,                           \tag{4}
\]

then at most three moving-triple selections can have selected kernel
dimension \(r+2\).

Combined with the subcritical coprime-intersection bound, this gives

\[
\begin{array}{c|c}
c\le r+4&\text{at most one maximal selection},\\
c=r+5&\text{at most three maximal selections}.
\end{array}                                                    \tag{5}
\]

This theorem forces dimension drops inside a moving family.  It does not
by itself close the underlying collision profile.

For \(r=4\), (4) is the \(p=28\), \(4^3 3^6\) baseline.  Its six moving
triple values therefore include at least three selected kernels of
dimension at most five, strengthening the existence-only conclusion of
the profile-specific
[even--odd span note](live-three-zero-higher-split-p28-three-quartic-six-triple-even-odd-span-drop.md).

## 2. The common kernel has dimension at most \(r+2\)

The common baseline in (2) has polynomial degree \(c\).  If
\(\mathcal K\) contained an \((r+3)\)-space, its exact rows would force
Wronskian weight

\[
                         (r+3)c-(r+1)(r+2),                   \tag{6}
\]

while the degree-\(c\) cap would be

\[
                         (r+3)(c-r-2).                        \tag{7}
\]

The forced weight exceeds the cap by

\[
 (r+3)c-(r+1)(r+2)-(r+3)(c-r-2)=2(r+2)>0.                   \tag{8}
\]

All exact-row gcd corrections are nonnegative.  Hence

\[
                              \dim\mathcal K\le r+2.           \tag{9}
\]

## 3. Critical pair intersections are complete

Take two maximal moving selections \(i\ne j\).  By (3) and (9),

\[
 \dim(\mathcal T_i\cap\mathcal T_j)
       \ge 2r-(r+2)=r-2.                                     \tag{10}
\]

The quartics \(B_i,B_j\) are coprime, so at the critical class count
\(c=r+5\),

\[
\begin{aligned}
 B_i\mathbb C[z]_{\le c-4}\cap
 B_j\mathbb C[z]_{\le c-4}
   &=B_iB_j\mathbb C[z]_{\le c-8}\\
   &=B_iB_j\mathbb C[z]_{\le r-3}.                           \tag{11}
\end{aligned}
\]

The last space has dimension \(r-2\).  Thus both inequalities are
equalities and

\[
          \boxed{\mathcal T_i\cap\mathcal T_j
                 =B_iB_j\mathbb C[z]_{\le r-3}}.             \tag{12}
\]

If the preliminary bound (9) were strict, (10) would already exceed the
ambient dimension in (11); hence (12) covers every surviving branch.

## 4. Four active values force the whole ambient polynomial space

Suppose four distinct moving values are maximal, and put

\[
                         t=z^2,\qquad a_i=i^2.                \tag{13}
\]

The four squares are distinct.  For the five pairs

\[
                          01,\ 02,\ 03,\ 12,\ 13,             \tag{14}
\]

the coefficient determinant of

\[
                         (t-a_i)^2(t-a_j)^2                  \tag{15}
\]

in \(1,t,t^2,t^3,t^4\) is

\[
\begin{aligned}
 4&(a_0-a_1)^4(a_0-a_2)(a_0-a_3)\\
  &\qquad\cdot(a_1-a_2)(a_1-a_3)(a_2-a_3)^2,                \tag{16}
\end{aligned}
\]

which is nonzero.  Therefore the pair products in (12) span

\[
                         \mathbb C[z^2]_{\le4}.               \tag{17}
\]

Since (12) contains every multiple of each pair product of degree at most
\(r-3\), it follows that

\[
       \mathbb C[z^2]_{\le4}\,
       \mathbb C[z]_{\le r-3}\subseteq\mathcal K.             \tag{18}
\]

The left side is the full space \(\mathbb C[z]_{\le r+5}\).  Indeed,
for \(r\ge4\), the five exponent intervals

\[
 [0,r-3],\ [2,r-1],\ [4,r+1],\ [6,r+3],\ [8,r+5]            \tag{19}
\]

cover every integer from \(0\) through \(r+5\).  Thus (18) forces

\[
                         \dim\mathcal K\ge r+6,               \tag{20}
\]

contrary to (9).  Four maximal selections are impossible, proving
Theorem 1.1.

For \(c\le r+4\), the ambient pair intersection in (11) has dimension at
most \(r-3\), strictly below (10), so even two maximal selections are
impossible.  This recovers the first line of (5).

## 5. Exact audit

[verify_live_three_zero_higher_split_uniform_moving_triple_critical_span_bound.py](../computations/verify_live_three_zero_higher_split_uniform_moving_triple_critical_span_bound.py)
checks the threshold and Wronskian identities for a wide exact range of
\(r\), the critical and subcritical intersection dimensions, the symbolic
determinant (16), the monomial-interval cover (19), and the \(p=28\)
corollary.

The
[independent audit](live-three-zero-higher-split-uniform-moving-triple-critical-span-bound-independent-audit.md)
reconstructs the exact-row and gcd hypotheses, all intersection dimensions,
the determinant and multiplication span, and the specialization to
\(4^3 3^6\).  It also records explicitly that the conclusion is a
dimension drop rather than a profile closure.
