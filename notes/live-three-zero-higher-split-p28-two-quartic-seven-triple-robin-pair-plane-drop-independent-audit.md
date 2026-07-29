# Independent audit: the \(p=28\) \(4^2 3^7 1\) Robin pair-plane drop

## 1. Verdict and exact scope

The strengthened theorem in
[the primary note](live-three-zero-higher-split-p28-two-quartic-seven-triple-robin-pair-plane-drop.md)
passes an independent reconstruction:

\[
 \boxed{\text{among the seven fixed-baseline moving-triple selections,
 at most three can have }q=6.}
\]

Equivalently, at least four of those seven selected-row kernels have
dimension at most five.  The proof really uses only four hypothetical
maximal selections.  It does not assume that all seven are maximal.

The baseline must be fixed: the same singleton value \(s\) is left
complementary in every selection, and in the profile containing one double,
that same double is selected in role two every time.  The result is a
dimension drop, not a contradiction to either collision profile.  In
particular, this audit supplies no theorem saying that a selected kernel of
dimension at most five is impossible at \(p=28\).

## 2. Selection bookkeeping and the exact common lift

The two residual parameter tuples are

\[
                 (e,a,b,u)=(2,7,0,1),(2,7,1,-1).
\]

For the first tuple, selecting the moving triple in role two and \(h\)
singletons leaves one fixed singleton \(s\).  For the second tuple, selecting
the moving triple, the unique double, and \(h-2\) singletons again leaves one
fixed singleton.  In both cases the relation complement is exactly

\[
                         4^2 3^6 1_i1_s,                    \tag{1}
\]

of mass \(28\) on ten value classes.  A six-dimensional selected kernel
therefore has a four-dimensional exact row-relation space

\[
             \mathcal S_i\subseteq\mathbb C[z]_{\leq6}.
                                                                    \tag{2}
\]

For completeness, the selected-row Wronskian gap is zero at \(q=6\) and
equals \(12\) at \(q=7\) for each of the six \(p=28\) splits.  Its
successive difference is positive thereafter.  Thus every selected kernel
has dimension at most six; this is the cap needed to turn “at most three
with \(q=6\)” into “at least four with \(q\le5\).”

Restoring the moving triple uses

\[
               B_i=(z-i)^2(z+i)^2=(z^2-i^2)^2.             \tag{3}
\]

The local jet calculation behind this transport can be checked without any
formula for the regular unit.  After absorbing the nonzero factor
\((z+i)^2\) and the other baseline factors into a regular function \(R\),

\[
       \left.\frac{d^3}{dz^3}\big((z-i)^2R(z)\big)\right|_{z=i}
                              =6R'(i).                       \tag{4}
\]

Thus the selected exact first-order row at the residual singleton \(i\)
becomes the restored exact third-order row.  At every other baseline node,
\(B_i\) is a structural unit, so ordinary product-rule transport gives the
same exact row belonging to the restored baseline.  Hence

\[
 B_i\mathcal S_i=\mathcal T_i\subseteq\mathcal K
                  \subseteq\mathbb C[z]_{\leq10},
 \qquad \dim\mathcal T_i=4,                                \tag{5}
\]

where \(\mathcal K\) is independent of \(i\) and has the common multiplicity
pattern

\[
                              4^2 3^7 1_s.                  \tag{6}
\]

This also audits the claimed common singleton row.  The exact baseline row
at \(s\) is \((U_sP)'(s)=0\), with the same regular unit \(U_s\) for every
transported space.  Since \(U_s(s)\ne0\), division by it gives

\[
                       L_s(P)=P'(s)+\beta P(s)=0,           \tag{7}
\]

for one scalar \(\beta=U_s'(s)/U_s(s)\) independent of \(i\).  Structural
separation gives \(s\ne\pm i\), even when \(s=0\), so no transport factor
vanishes at this row.

## 3. The common-kernel bound and exact pair planes

If \(\mathcal K\) contained a seven-space, its two order-four, seven
order-three, and one order-one exact rows would force Wronskian weight

\[
                 2(7-4)+7(7-3)+(7-1)=40,                  \tag{8}
\]

whereas the degree-ten cap is

\[
                         7(11-7)=28.                       \tag{9}
\]

The local correction after removing a common factor of order \(g\) is
\(7g+\max(0,7-m+g)\) for \(g\le m\), and \(7g\) for \(g>m\); it never lowers
the base exact-row cost \(\max(0,7-m)\).  Thus

\[
                              \dim\mathcal K\le6.           \tag{10}
\]

For two distinct moving values \(i,j\), structural nonopposition makes
\(B_i,B_j\) coprime.  Consequently

\[
 B_i\mathbb C[z]_{\le6}\cap B_j\mathbb C[z]_{\le6}
                      =B_iB_j\mathbb C[z]_{\le2}.          \tag{11}
\]

This ambient intersection is three-dimensional.  The restriction of
\(L_s\) to it is nonzero: writing \(P_{ij}=B_iB_j\),

\[
 L_s(P_{ij}q)=P_{ij}(s)q'(s)
     +\big(P_{ij}'(s)+\beta P_{ij}(s)\big)q(s),             \tag{12}
\]

and \(P_{ij}(s)\ne0\).  Its Robin kernel

\[
 \mathcal A_{ij}:=\ker\left(L_s\bigm|
                         P_{ij}\mathbb C[z]_{\le2}\right) \tag{13}
\]

therefore has dimension two.

On the other hand, two four-spaces inside an at-most-six-space meet in
dimension at least two.  Since their intersection is contained in (13),
every pair of maximal selections satisfies

\[
                    \boxed{\mathcal T_i\cap\mathcal T_j
                                      =\mathcal A_{ij}}.    \tag{14}
\]

If \(\dim\mathcal K<6\), the lower bound would exceed the Robin-plane
dimension, so that case is already contradictory.  No equality branch is
being discarded.

Put \(x=z-s\), \(a_i=i^2\), and

\[
 \gamma_{ij}=\beta+\frac{P_{ij}'(s)}{P_{ij}(s)}
 =\beta+\frac{4s}{s^2-a_i}+\frac{4s}{s^2-a_j}.             \tag{15}
\]

A direct substitution in (12) gives the following basis of (13):

\[
 X_{ij}=x^2P_{ij},\qquad
 Y_{ij}=P_{ij}(1-\gamma_{ij}x).                             \tag{16}
\]

This retains the full \(ij\)-dependence of the Robin slope.

## 4. What four maximal selections force

Choose four hypothetical maximal values with distinct squares
\(a_0,a_1,a_2,a_3\).  Among their six pairs, use

\[
                         01,02,03,12,13.                    \tag{17}
\]

The coefficient determinant of the five even quartics
\((t-a_i)^2(t-a_j)^2\), in the basis \(1,t,\ldots,t^4\), is

\[
\begin{aligned}
 4&(a_0-a_1)^4(a_0-a_2)(a_0-a_3)\\
  &\quad\cdot(a_1-a_2)(a_1-a_3)(a_2-a_3)^2\ne0.            \tag{18}
\end{aligned}
\]

Therefore the \(X\)-members of just those five pair planes span

\[
                  \mathcal V=(z-s)^2\mathbb C[z^2]_{\le4},
                  \qquad\dim\mathcal V=5.                 \tag{19}
\]

No fifth maximal selection has entered the argument.

## 5. The branch \(s\ne0\)

Write every degree-ten polynomial uniquely as

\[
                     R(z)=E(t)+zO(t),\qquad t=z^2,
                     \quad\deg E\le5,\ \deg O\le4.        \tag{20}
\]

Consider

\[
                  \Psi_s(R)=2sE(t)+(t+s^2)O(t).             \tag{21}
\]

The six even coefficient columns give the minor \((2s)^6\), so this map
has rank six when \(s\ne0\).  Its kernel is exactly \(\mathcal V\): if
\(\Psi_s(R)=0\), then

\[
             R=(t+s^2-2sz)q(t)=(z-s)^2q(t),
             \qquad q\in\mathbb C[t]_{\le4}.               \tag{22}
\]

For the second Robin-plane member, exact parity substitution gives

\[
 \Psi_s(Y_{ij})=
 \bigl(2s+\gamma_{ij}(s^2-t)\bigr)
                   (t-a_i)^2(t-a_j)^2.                     \tag{23}
\]

The affine factor is nonzero because \(s\ne0\).  The two images for the
pairs \(12\) and \(13\) cannot be proportional: a common nonzero
polynomial would be divisible by

\[
                    (t-a_1)^2(t-a_2)^2(t-a_3)^2,            \tag{24}
\]

of degree six, while each image in (23) has degree at most five.  Thus
\(\mathcal K\) contains the five directions in \(\mathcal V\) and two
independent quotient directions.  This gives
\(\dim\mathcal K\ge7\), contradicting (10).

## 6. Both branches at \(s=0\)

At \(s=0\), every \(P_{ij}\) is even and \(P_{ij}'(0)=0\), so

\[
 X_{ij}=t(t-a_i)^2(t-a_j)^2,\qquad
 Y_{ij}=(1-\beta z)(t-a_i)^2(t-a_j)^2.                    \tag{25}
\]

Equation (18) now gives the two five-spaces

\[
             t\mathbb C[t]_{\le4},\qquad
             (1-\beta z)\mathbb C[t]_{\le4}.              \tag{26}
\]

If \(\beta\ne0\), they meet trivially: comparison of odd parts in
\(tq=(1-\beta z)r\) gives \(r=0\), then \(q=0\).  Their ten-dimensional
direct sum cannot lie in \(\mathcal K\).

If \(\beta=0\), their span is exactly

\[
                 \mathbb C[t]_{\le4}+t\mathbb C[t]_{\le4}
                         =\mathbb C[z^2]_{\le5}.            \tag{27}
\]

It has dimension six, so containment and (10) force equality with
\(\mathcal K\).  But its Wronskian is

\[
 \operatorname{Wr}(1,z^2,z^4,z^6,z^8,z^{10})=Cz^{15},
 \qquad C\ne0.                                             \tag{28}
\]

Every active triple value is nonzero, while its exact order-three baseline
row would force Wronskian weight at least \(6-3=3\) there.  Equation (28)
has no such zero.  Thus even one of the four active triple rows contradicts
(27).  Equivalently, using the whole fixed baseline gives the larger forced
nonzero-node weight

\[
                         2(6-4)+7(6-3)=25.                  \tag{29}
\]

This confirms explicitly that the exceptional parity branch does not use
maximality of any of the remaining three selections.

## 7. Conclusion and scope guard

Every set of four maximal moving-triple selections leads to a contradiction,
in all three cases \(s\ne0\), \(s=0,\beta\ne0\), and
\(s=\beta=0\).  Therefore at most three of the seven selections have
dimension six, and at least four have dimension at most five.

Two limitations remain and should be preserved in any registry entry:

1. the seven selections form one fixed-\(s\), fixed-other-roles family;
   the theorem does not compare families with different complementary
   singleton choices; and
2. a \(q\le5\) selection is only a dimension drop at \(p=28\), not a
   collision-profile closure.

The independent checker
[verify_live_three_zero_higher_split_p28_two_quartic_seven_triple_robin_pair_plane_drop_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_two_quartic_seven_triple_robin_pair_plane_drop_independent_audit.py)
does not import the primary checker.  It reconstructs both residual
selections at all six \(p=28\) splits, the exact local transport, all
Wronskian gaps and gcd corrections, the pair-plane dimensions, determinant
(18), quotient (23), both zero-singleton branches, and the even-space
Wronskian.
