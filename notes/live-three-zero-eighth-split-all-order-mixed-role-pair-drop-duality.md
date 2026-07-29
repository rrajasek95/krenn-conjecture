# The eighth split: all-order mixed-role pair-drop duality

## 1. Uniform statement

Fix the eighth split and allow arbitrary common-pole order:

\[
                    h=8,\qquad p=8+k,\qquad k\ge1,
                    \qquad M=k+18.                       \tag{1}
\]

Choose \(d\) repeated exceptional classes at formal role two and
\(s=10-2d\) singleton classes at formal role one, where
\(0\le d\le4\).  Every chosen repeated class is an exact double except
that at most one may be an exact triple.  Assume the structural
noncollision/nonopposite conditions and the usual fact that at most one
singleton value is zero.

Lowering two formal layers gives a role-eight core.  Require every such
core to be legal, with one permitted exception: if a chosen triple and a
zero singleton occur, their joint drop may be the unique illegal core.
Let \(A\) be the polynomial of the \(k+8\) complementary labels after
the full role-ten selection, and let \(c\) be its number of distinct
roots.

**Theorem 1.1 (all-order mixed-role duality).**  If every isolated-star
pivot vanishes, the legal pair-drop lifts span the exact
four-dimensional kernel of the selected rows.  Those rows have an
injective two-dimensional relation space

\[
                         \mathcal S\subseteq
                         \mathbb C[z]_{\le c-4}.          \tag{2}
\]

The theorem is uniform in \(k\).  In particular:

1. \(c<5\) is impossible by dimension;
2. if \(c=5\), then \(\mathcal S=\mathbb C[z]_{\le1}\);
3. every simple complementary root is a root of the Wronskian of
   \(\mathcal S\), so more than \(2c-10\) simple roots are impossible;
4. when \(c=5\), one simple complementary root already gives an
   immediate exact-residue contradiction.

This is a theorem about a selected formal configuration, not a statement
that every collision profile in every \(k\)-row admits such a
configuration.  No all-\(k\) census closure is claimed here.

## 2. Why the kernel is independent of \(k\)

Put

\[
                L=d+s=10-d,\qquad D=11-d.               \tag{3}
\]

For a repeated layer \(x\) and singleton layer \(r\), the cubic-gauge
factors are

\[
              f_x(z)=z^2-x^2,\qquad
              f_r(z)=(z-r)(z+r)^2.                      \tag{4}
\]

If \(b\) of the two lowered layers are singletons, the legal Hermite
core represents \(L-b\) classes.  Its nonzero residual has degree at
most \(L-b-3=7-d-b\), while its two lift factors have degree \(4+b\).
Every lift therefore belongs to \(\mathbb C[z]_{\le D}\), independently
of \(k\).

Existence and nonvanishing are the formal pair-drop case of
[the higher-split collision-exchange theorem](live-three-zero-higher-split-collision-exchange-wronskian.md),
Sections 3--4.  The mixed factors and exact selected rows appear
explicitly in
[the fourth-order mixed model](live-three-zero-eighth-split-k4-four-triple-mixed-layer-closure.md),
Sections 2--3, while the one-missing-edge extension is proved in
[the fifth-order unified kernel](live-three-zero-eighth-split-k5-unified-pair-drop-linear-plane-closure.md),
Sections 2--4.  None of those kernel steps uses the common-pole order.

For completeness, the numerical invariants are recalled.  The \(d\)
selected repeated rows have exact local order two and the \(s\)
singleton rows have exact local order one:

\[
              P\longmapsto(B_xP)''(-x),\qquad
              P\longmapsto(B_rP)'(-r),                  \tag{5}
\]

with nonzero local units.  For a \(q\)-dimensional common kernel, forced
Wronskian weight minus the degree-\(D\) cap is

\[
 d(q-2)+s(q-1)-q(D+1-q)=q^2-2q-10>0
                         \qquad(q\ge5).                 \tag{6}
\]

The local gcd corrections are likewise independent of \(k\).  Thus the
selected-row kernel has dimension at most four.

Let \(W\) be the legal-lift span and
\(U_i=W\cap f_i\mathbb C[z]\).  The legal-pair graph is \(K_L\) or
\(K_L\) with only the triple--zero edge missing.  Even at a missing-edge
endpoint, all neighbor factors have degree

\[
                         25-4d>D.                       \tag{7}
\]

Hence every \(U_i\) has dimension at least two.  A hypothetical
three-dimensional \(W\) has saturated parity minors of degree

\[
             1+2L=3+2(L-1)=2D-1,                       \tag{8}
\]

where the second expression is used when a singleton is zero.  Removing
the gcd gives \(W=G(z)\mathcal E(z^2)\) with
\(\dim\mathcal E=3\).  Let \(m\) count the selected singleton nodes \(r\)
for which \(G(-r)=0\).  The exact order-one row (5) makes each such zero
at least double, so these nodes cost at least \(2m\) gcd degrees.
The remaining singleton squares would force

\[
 2(s-m)\le
 3\left(\left\lfloor{11-d-2m\over2}\right\rfloor-2\right),              \tag{9}
\]

which is false for every \(0\le d\le4\) and admissible \(m\), unless the
square-variable cap is already too small for a three-space.  Therefore

\[
                         W=K,\qquad\dim K=4.             \tag{10}
\]

## 3. Uniform dual degree

Let \(Q\) be the product of the \(d\) role-two plus-pole factors and
\(H\) the product of the \(s\) selected singleton plus-pole factors.
The lifted rational functions are

\[
 F_P(z)={A(z)P(z)\over
              (z+\mu)^{k+1}Q(z)^3H(z)^2}.               \tag{11}
\]

Their numerator and denominator degrees are

\[
 (k+8)+(11-d)=k+19-d,\qquad
 (k+1)+3d+2s=k+21-d,                                   \tag{12}
\]

so the decay is always \(O(z^{-2})\).

There are \(10-d\) selected rows on a \(12-d\) dimensional polynomial
space.  Equation (10) gives rank \(8-d\), hence exactly two row
relations.  A relation among the distinct principal parts has the form

\[
                   {N(z)\over Q(z)^3H(z)^2},
                   \qquad\deg N\le7.                    \tag{13}
\]

Indeed, the selected denominator has degree \(3d+2s=20-d\), while the
relation annihilates \(D+1=12-d\) moments.

Write

\[
 g=\prod_{A(a)=0}(z-a)^{\operatorname{ord}_a(A)-1},
 \qquad R={A\over g},\qquad D_A={A'\over g}.             \tag{14}
\]

Then \(\deg R=c\), \(\deg D_A=c-1\), and
\(\operatorname{LC}(D_A)=\deg A=k+8\).  Exact
differentiation gives

\[
 {d\over dz}{(z+\mu)^{k+1}N\over A}
 ={(z+\mu)^kg\over A^2}\mathcal E_{A,k}(N),             \tag{15}
\]

where

\[
 \mathcal E_{A,k}(N)=
 R\bigl((z+\mu)N'+(k+1)N\bigr)-(z+\mu)D_AN.             \tag{16}
\]

For \(n=\deg N\le7\), the nominal leading coefficient is

\[
                         n+(k+1)-(k+8)=n-7.              \tag{17}
\]

At \(n=7\) it cancels, and at \(n\le6\) the nominal degree is already at
most \(c+6\).  Selected-pole contact therefore gives

\[
                  \mathcal E_{A,k}(N)=Q^2H S_N,
                  \qquad S_N\in\mathbb C[z]_{\le c-4},  \tag{18}
\]

because \(\deg(Q^2H)=2d+s=10\).  The map \(N\mapsto S_N\)
is injective: a zero image makes
\((z+\mu)^{k+1}N/A\) constant, and evaluation at \(-\mu\)
forces that constant and \(N\) to vanish.  This proves (2).

## 4. Consequences that do not require a census

At a simple root \(r\) of \(A\), (15) has local form

\[
                         {B_r(z)S(z)\over(z-r)^2},
                         \qquad B_r(r)\ne0.              \tag{19}
\]

The zero residue gives one Robin row on \(\mathcal S\), so every simple
root divides the Wronskian of a basis.  That Wronskian has degree at most
\(2(c-4)-2=2c-10\), proving the simple-root criterion in Theorem 1.1.
If \(c=5\), equation (2) is the full linear space; choosing
\(S=z-r\) in (19) gives the contradiction \(B_r(r)=0\).

Complementary repeated-pole arguments can also be transported across
orders, but they require enough interchangeable selected/outside
classes in the particular profile.  For example, at a complementary
double \(u\), the logarithmic equation contains \(k/(u+\mu)\) instead
of \(5/(u+\mu)\); this term cancels in a selected/outside swap, leaving
the same order-independent quadratic map

\[
                         t\longmapsto{5u+t\over u^2-t^2}.               \tag{20}
\]

This observation is only a local corollary.  A profile is not credited
without a separate legality, choice, and fibre-cardinality audit.

## 5. Exact audit

[verify_live_three_zero_eighth_split_all_order_mixed_role_pair_drop_duality.py](../computations/verify_live_three_zero_eighth_split_all_order_mixed_role_pair_drop_duality.py)
checks every \(d=0,\ldots,4\) kernel invariant, both parity counts, all
absorbed-singleton inequalities, the \(k\)-symbolic decay and numerator
degree, the exact derivative identity, the leading cancellation
\(n-7\), the target degree \(c-4\), and the order-independent
complementary singleton and double-swap calculations.  It intentionally
contains no collision-census credit.
