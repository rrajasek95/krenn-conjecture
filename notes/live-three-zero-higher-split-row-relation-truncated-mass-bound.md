# Higher splits: the row-relation truncated-mass bound

## 1. Uniform dual statement

Use the higher-split formal selection with

\[
 L=h+2-d,\qquad D=h+3-d,
\]

and let \(K\subseteq\mathbb C[z]_{\leq D}\) be its selected-row kernel.
Suppose

\[
                              \dim K=q\geq4.              \tag{1}
\]

Let

\[
             A(z)=\prod_{i=1}^{c}(z-a_i)^{m_i},
             \qquad \sum_{i=1}^{c}m_i=p=h+k             \tag{2}
\]

be the complementary polynomial.  Then every such formal configuration
must satisfy

\[
                 \boxed{\displaystyle
                 \sum_{i=1}^{c}\min(m_i,q-2)
                    \geq(q-2)(q+1).}                    \tag{3}
\]

This condition is independent of \(h,d,k\) except through the existence
of the selected kernel and the complementary multiplicities.

In the first unresolved five-dimensional branch, (3) reads

\[
                         \sum_i\min(m_i,3)\geq18.         \tag{4}
\]

Equivalently, if \(n_j\) counts complementary classes of multiplicity
\(j\), then

\[
              2n_1+n_2\leq3(c-6),                       \tag{5}
\]

or

\[
        p\geq18+\sum_{j\geq4}(j-3)n_j.                   \tag{6}
\]

Thus a \(q=5\) escape needs at least eighteen units of complementary mass
after every class is capped at three.  At the first numerical boundary
\(p=18\), every complementary multiplicity is at most three.

## 2. The relation space has dimension \(q-2\)

The selected rows are \(L\) functionals on a polynomial space of
dimension

\[
                             D+1=L+2.                    \tag{7}
\]

If their common kernel has dimension \(q\), their rank is \(L+2-q\).
Consequently their relation space has dimension

\[
                         r=L-(L+2-q)=q-2.                \tag{8}
\]

The relation-to-polynomial construction in Section 4 of
[the higher-split mixed pair-drop theorem](live-three-zero-higher-split-mixed-pair-drop-five-class-closure.md)
is injective and sends this relation space to an \(r\)-space

\[
                 \mathcal S\subseteq\mathbb C[z]_{\leq c-4}.          \tag{9}
\]

For completeness, if \(N\) is the numerator of a selected-row relation,
that construction is the exact identity

\[
 {d\over dz}{(z+\mu)^{k+1}N\over A}
 ={(z+\mu)^kg\over A^2}\,Q^2H\,S,\qquad S\in\mathcal S, \tag{10}
\]

where

\[
 g=\prod_i(z-a_i)^{m_i-1}.                               \tag{11}
\]

The leading cancellation in the differential operator gives the uniform
degree \(c-4\), and the map is injective because a zero right-hand side
would make the left-hand quotient constant and then zero at \(-\mu\).

## 3. Every complementary multiplicity is a jet condition

At a root \(a_i\) of multiplicity \(m_i\), the right side of (10) has
local form

\[
                  {U_i(z)S(z)\over(z-a_i)^{m_i+1}},
                  \qquad U_i(a_i)\ne0.                  \tag{12}
\]

The residue of a derivative is zero.  Therefore every
\(S\in\mathcal S\) satisfies the exact order-\(m_i\) condition

\[
                         (U_iS)^{(m_i)}(a_i)=0.           \tag{13}
\]

For an \(r\)-dimensional base-point-free polynomial space, an exact
order-\(m_i\) functional forces Wronskian weight at least

\[
                             \max(0,r-m_i).               \tag{14}
\]

Common factors cannot weaken this estimate.  If the gcd of
\(\mathcal S\) has order \(t\leq m_i\) at \(a_i\), division changes
(13) to exact order \(m_i-t\), while lowering the Wronskian degree cap
by \(rt\).  Relative to (14), the correction is

\[
 rt+\max(0,r-m_i+t)-\max(0,r-m_i)\geq0.                 \tag{15}
\]

If \(t>m_i\), the local row becomes automatic, but the correction is
\(rt-\max(0,r-m_i)>0\).  Gcd roots elsewhere only lower the cap.

The Wronskian of the reduced \(r\)-space in (9) has degree at most

\[
                         r\bigl((c-4)+1-r\bigr)
                              =r(c-3-r).                 \tag{16}
\]

Equations (14)--(16) give

\[
                    \sum_i\max(0,r-m_i)\leq r(c-3-r).   \tag{17}
\]

Since

\[
 \sum_i\max(0,r-m_i)=rc-\sum_i\min(m_i,r),               \tag{18}
\]

substitution of \(r=q-2\) proves (3).

## 4. Exact audit of naïve multi-drop lifts

The bound above is a genuine global compatibility input.  A direct
multi-drop does not, by itself, create the triple-factor lifts which
would defeat a five-space.

To see the obstruction exactly, take \(d=0\), so the full formal
selection consists of \(h+2\) singleton layers.  Remove a set \(T\) of
\(t\geq3\) selected layers and insert \(t-2\) complementary labels,
grouped into \(u\) value classes \(y_j\) with positive counts \(b_j\).
The resulting \(h\)-label core represents

\[
                         h+2-t+u                         \tag{19}
\]

classes, so its Hermite residual \(q_T\) has degree at most

\[
                         h-1-t+u.                        \tag{20}
\]

Comparing its exact rational function with the full selected denominator
gives

\[
 P_T=
 q_T\,
 {\displaystyle\prod_{i\in T}(z-r_i)(z+r_i)^2
  \over
  \displaystyle\prod_{j=1}^{u}
       (z-y_j)^{b_j}(z+y_j)^{b_j+1}}.                   \tag{21}
\]

All displayed factors are pairwise coprime under the structural
noncollision/nonopposite hypotheses.  Hence (21) is a polynomial lift if
and only if

\[
 \prod_{j=1}^{u}(z-y_j)^{b_j}(z+y_j)^{b_j+1}
                              \quad\hbox{divides }q_T.   \tag{22}
\]

The required divisor has degree

\[
                         2(t-2)+u,                       \tag{23}
\]

and the residual degree left after division is at most

\[
       (h-1-t+u)-(2t-4+u)=h+3-3t.                       \tag{24}
\]

Thus \(t\leq\lfloor(h+3)/3\rfloor\) is necessary even before any
incidence argument.  For the first new case \(t=3\), (22) asks the
residual to contain one entire cubic factor.  The Hermite row at the
inserted class is only one exact order-\(b_1\) functional; after using
that row, the divisor in (22) still imposes \(2b_1\) independent local
conditions.  The local Hermite condition therefore does not supply the
needed divisibility; a proof would have to extract it from compatibility
among several cores.

In particular, the \(q=5\) Schubert boundary in
[the low-role incidence closure](live-three-zero-higher-split-low-role-selected-lift-incidence-closure.md),
Section 6, can have every pair intersection nonzero while a general
triple intersection is zero.  Any successful multi-drop route must
produce the missing divisibility in (22), or an equivalent compatibility
among several core residuals; pair-drop incidence alone cannot do it.

## 5. Exact audit

[verify_live_three_zero_higher_split_row_relation_truncated_mass_bound.py](../computations/verify_live_three_zero_higher_split_row_relation_truncated_mass_bound.py)
checks the relation dimension and degree, the local gcd corrections, the
equivalence of (3), (5), and (6), and all multi-drop degree identities.
