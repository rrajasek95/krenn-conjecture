# A higher-split mixed pair-drop closure with five complementary classes

## 1. Result

Work on the no-extra-singular live-three-zero collision stratum.  Put

\[
 p=h+k,\qquad M=2h+k+2,\qquad h\ge8,\quad k\ge1.          \tag{1}
\]

Suppose a collision profile of total size \(M\) admits the following
formal selection.

- Give role two to \(d\) repeated classes.  Each is an exact double,
  except that at most one may be an exact triple.
- Give role one to \(s=h+2-2d\) singleton classes.
- After removing all \(h+2\) selected labels, the complementary
  multiplicity profile has exactly five distinct classes and at least one
  simple class.
- The exact inequality

  \[
  2(h+2-2d)>
       3\left(\left\lfloor{h+3-d\over2}\right\rfloor-2\right)          \tag{2}
  \]

  holds.

Then the profile is impossible.  The conclusion is uniform in the
common-pole order \(k\).  It allows the unique pair-drop core which can be
illegal when the selected triple is lowered together with a zero
singleton.

For \(h=8\), inequality (2) holds for every \(0\le d\le4\).  The theorem
therefore contains the six simple-complement closures

\[
 3^5 2^2 1^4,\quad3^5 2\,1^6,\quad3^5 1^8,
 \quad3^4 2^3 1^5,\quad3^4 2^2 1^7,\quad3^4 1^{11}       \tag{3}
\]

at \(k=5\), but its statement is not restricted to that census.

## 2. Legal pair-drop lifts

There are

\[
 L=d+s=h+2-d                                                   \tag{4}
\]

formal layers.  Lower two different layers, leaving a role-\(h\) core.
For a lowered repeated value \(x\) and an omitted singleton value \(r\),
the exact lift factors are

\[
                 f_x(z)=z^2-x^2,
        \qquad f_r(z)=(z-r)(z+r)^2.                         \tag{5}
\]

If \(b\in\{0,1,2\}\) lowered layers are singletons, the core represents
\(L-b\) value classes.  The simultaneous-Hermite lemma gives a nonzero
residual of degree at most \(L-b-3\), so every legal lift has degree at
most

\[
                (4+b)+(L-b-3)=h+3-d=:D.                   \tag{6}
\]

The arbitrary-\(h\) residual statement is Section 2 of
[the higher-split collision frontier](live-three-zero-higher-split-collision-frontier.md):
an \(h\)-label core representing \(m_R\) classes and leaving a singleton
has a nonzero Hermite residual of degree at most \(m_R-3\).
The lift from that core is exact.  Adding one more selected label to an
already represented repeated class \(x\) removes \(z-x\) from the
complement and adds \(z+x\) to the plus-pole denominator, so multiplying
the residual by
\[
                         (z-x)(z+x)=f_x(z)
\]
preserves the rational function.  Adding a formerly omitted singleton
class \(r\) removes \(z-r\) from the complement and adds
\((z+r)^2\) to the denominator, so the exact multiplier is
\[
                         (z-r)(z+r)^2=f_r(z).
\]
Applying these two identities to the two lowered layers proves
nonvanishing and membership in the full selected-row kernel for arbitrary
\(h\).  The exact order-two/order-one local rows and their gcd corrections
are spelled out in Sections 2--3 of
[the fourth-order mixed-layer closure](live-three-zero-eighth-split-k4-four-triple-mixed-layer-closure.md).

Every pair is legal if the repeated layers are all doubles.  With one
selected triple, the only possibly illegal pair consists of that triple
and the zero singleton.  Indeed, a lowered double leaves its nonzero mate,
an unlowered selected triple leaves its third label, and an omitted
nonzero singleton leaves itself.  At most one singleton value is zero.
Thus the legal-pair graph is \(K_L\) or \(K_L\) with one edge deleted.

Let \(P_{ij}\ne0\) be the lift for a legal pair and put

\[
 W=\operatorname {span}\{P_{ij}:ij\text{ legal}\}
                 \subseteq\mathbb C[z]_{\le D}.           \tag{7}
\]

## 3. The lift span has dimension at least four

For a formal layer \(i\), set

\[
                         U_i=W\cap f_i\mathbb C[z].        \tag{8}
\]

The degree of the product of all layer factors is

\[
                         2d+3s=3h+6-4d.                   \tag{9}
\]

If \(U_i\) were a line, its generator would be divisible by every legal
neighbor factor.  On the complete graph the smallest neighbor-factor
degree is \(3h+3-4d\), and

\[
                  3h+3-4d>D
\]

because \(d\le(h+2)/2\) and \(h\ge8\).  At an endpoint of the possibly
missing edge the neighbor degree is \(3h+1-4d\).  Here \(s\ge1\), hence
\(d\le(h+1)/2\), and again

\[
                  3h+1-4d>D.                              \tag{10}
\]

Thus every \(U_i\) has dimension at least two.  In particular
\(\dim W\le2\) is impossible: in a two-space all the \(U_i\)'s would be
the whole space, making every member divisible by (9), whose degree is
larger than \(D\).

Assume for contradiction that \(\dim W=3\).  Since every \(U_i\) is a
plane, the parity minors of a basis vanish at both signs of every nonzero
layer value.  They are odd and have degree at most

\[
                         2D-1=2h+5-2d.                    \tag{11}
\]

If no singleton is zero, their forced odd divisor has degree
\(1+2L=2D-1\).  If a singleton is zero, an adapted basis gives a triple
zero at the origin and the other \(L-1\) opposite pairs, again of total
degree \(3+2(L-1)=2D-1\).  The cross-product argument therefore makes the
primitive three-space projectively even:

\[
                         W=G(z){\cal E}(z^2),
                         \qquad\dim{\cal E}=3.             \tag{12}
\]

An absorbed selected singleton costs at least two degrees of \(G\).  To
see the point, its exact row is

\[
                         (B_rP)'(-r)=0,
                         \qquad B_r(-r)\ne0.               \tag{13}
\]

A merely simple zero of \(G\) at \(-r\) would force every primitive
\(E\in{\cal E}\) to vanish at \(r^2\), so the common square factor was not
removed.  This includes \(r=0\).

Let \(m\) be the number of selected singleton nodes \(r\) with
\(G(-r)=0\).  By (13) each such zero is at least double, so the
square-variable degree in (12) is at most

\[
                         n_m=\left\lfloor{D\over2}\right\rfloor-m.    \tag{14}
\]

Every one of the other \(s-m\) singleton squares contributes Wronskian
weight at least two, whereas a primitive three-space of maximum degree
\(n_m\) has Wronskian degree at most \(3(n_m-2)\).  Inequality (2) is the
strict contradiction for \(m=0\); after increasing \(m\) the left side
minus the right side increases by exactly \(m\).  Hence no \(m\) is
possible.  We conclude

\[
                              \boxed{\dim W\ge4}.          \tag{15}
\]

## 4. Two relations fill the linear target

Let \(K_{\rm row}\subseteq\mathbb C[z]_{\le D}\) be the common kernel of
the \(d\) selected order-two rows and \(s\) selected order-one rows.  The
lifts give \(W\subseteq K_{\rm row}\), so (15) gives
\(\dim K_{\rm row}\ge4\).  There are \(L=h+2-d\) rows on a polynomial
space of dimension \(D+1=h+4-d\).  Their relation space therefore has
dimension at least two.

Let \(Q\) be the product of the selected repeated plus-pole factors, \(H\)
the product of the selected singleton plus-pole factors, and \(A\) the
complementary polynomial.  Then

\[
              \deg A=h+k=p,
 \qquad F_P(z)={A(z)P(z)\over
                 (z+\mu)^{k+1}Q(z)^3H(z)^2}.             \tag{16}
\]

A relation among the distinct selected principal parts has numerator

\[
                  {N(z)\over Q(z)^3H(z)^2},
                  \qquad\deg N\le h-1.                   \tag{17}
\]

Indeed, the selected denominator has degree \(2h+4-d\), and the relation
annihilates the \(D+1=h+4-d\) polynomial moments.

Put

\[
 g=\prod_{A(a)=0}(z-a)^{\operatorname{ord}_a(A)-1},
 \qquad R={A\over g},\qquad D_A={A'\over g},              \tag{18}
\]

and let \(c=\deg R\).  Exact differentiation gives

\[
 {d\over dz}{(z+\mu)^{k+1}N\over A}
 ={(z+\mu)^kg\over A^2}{\cal E}_A(N),                    \tag{19}
\]

where

\[
 {\cal E}_A(N)=R\bigl((z+\mu)N'+(k+1)N\bigr)
                    -(z+\mu)D_AN.                        \tag{20}
\]

Since \(\operatorname{LC}(D_A)=h+k\), the nominal leading coefficient
for \(n=\deg N\le h-1\) is

\[
                       n+(k+1)-(h+k)=n+1-h.               \tag{21}
\]

It cancels at \(n=h-1\), and \(\deg{\cal E}_A(N)\le c+h-2\).
The selected-pole contact equations imply

\[
                  {\cal E}_A(N)=Q^2H S_N,
                  \qquad S_N\in\mathbb C[z]_{\le c-4},   \tag{22}
\]

because \(\deg(Q^2H)=2d+s=h+2\).

The relation-to-\(S_N\) map is injective.  If \(S_N=0\), (19) is the
derivative of a constant; evaluation at \(-\mu\), where \(A(-\mu)\ne0\),
forces that constant and \(N\) to vanish.  Distinct principal-part supports
already make the relation-to-\(N\) map injective.

By hypothesis \(c=5\), so the target in (22) is the two-dimensional linear
space.  The relation space has dimension at least two and injects into it;
therefore it has dimension exactly two and

\[
                         {\cal S}=\mathbb C[z]_{\le1}.     \tag{23}
\]

This argument does not require an upper bound on \(\dim K_{\rm row}\).

## 5. The simple complementary root is impossible

Let \(r\) be a simple root of \(A\).  All other factors in (19) are units at
\(r\).  For every \(S\in{\cal S}\), the local form of the exact derivative
is

\[
                         {B_r(z)S(z)\over(z-r)^2},
                         \qquad B_r(r)\ne0.               \tag{24}
\]

Its residue vanishes, so \((B_rS)'(r)=0\) for every linear \(S\).  Taking
\(S=z-r\) gives \(B_r(r)=0\), a contradiction.  This proves the theorem.

## 6. Scope and exact audit

The theorem closes only profiles admitting the displayed selection, the
strict Wronskian inequality (2), and a five-class complement with a simple
root.  It does not close all higher-split collision profiles, the
additional-singular-site escape, or the all-even reduction.

[verify_live_three_zero_higher_split_mixed_pair_drop_five_class_closure.py](../computations/verify_live_three_zero_higher_split_mixed_pair_drop_five_class_closure.py)
checks the degree identities, complete/missing-edge neighbor bounds, exact
monotonic Wronskian inequality, relation dimensions, \(k\)-independent
leading cancellation, local residue, and all six \(h=8,k=5\) applications
in (3).
