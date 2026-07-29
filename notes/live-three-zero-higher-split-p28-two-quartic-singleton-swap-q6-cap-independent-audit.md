# Independent audit: the \(p=28\) two-quartic singleton-swap \(q=6\) cap

## 1. Verdict

The theorem in
[the primary singleton-swap note](live-three-zero-higher-split-p28-two-quartic-singleton-swap-q6-cap.md)
is correct under the standing higher-split separation hypotheses.

The audit deliberately reconstructed the two formal selections, rather than
reading their counts from the primary checker.  It also checked the two points
most liable to an indexing error:

1. if \(\mathcal S_s\) denotes the relation space for the selection whose
   **complementary** ordinary singleton is \(s\), then the transport to the
   two-point baseline is \(f_t\mathcal S_s\), not
   \(f_s\mathcal S_s\);
2. \(\mathcal S_s\subseteq\mathbb C[z]_{\le6}\), so the cubic transport lies
   in \(\mathbb C[z]_{\le9}\).  The common kernel used in the proof really is
   a kernel in that degree-nine space.

The result remains only a selected-kernel dimension statement.  It does not
close either collision profile.

## 2. Reconstruction of both formal selections

Write the original profile as

\[
                         4^e3^a2^b1^{h+u}.
\]

For both residual tuples one exact triple \(x\) is assigned role two.  In the
second tuple the unique exact double is also assigned role two.  Thus

\[
 d=1+b,\qquad \sigma=h+2-2d,
\]

where \(\sigma\) is the number of selected ordinary-singleton layers.  The
two ledgers are

\[
\begin{array}{c|c|c|c|c}
(e,a,b,u)&d&h+u&\sigma&(h+u)-\sigma\\ \hline
(2,7,0,1)&1&h+1&h&1,\\
(2,7,1,-1)&2&h-1&h-2&1.
\end{array}
\]

Consequently a choice of the complementary ordinary singleton \(s\) means
that every other ordinary singleton is selected.  The selected triple \(x\)
loses two copies and becomes a complementary singleton; the selected exact
double disappears.  In either ledger the complement is therefore exactly

\[
                        4^2 3^6 1_x1_s.                    \tag{1}
\]

It has mass \(28\) and ten value classes.  This verifies that \(x\) is the
fixed simple class in the later two-point comparison, while \(s\) is the
moving complementary simple class.

The selected-row polynomial degree and number of selected rows are

\[
 D=h+3-d,\qquad L=d+\sigma=h+2-d,\qquad D+1=L+2.          \tag{2}
\]

For a \(q\)-space the selected-row Wronskian excess is

\[
 d(q-2)+\sigma(q-1)+\max(0,q-k)-q(D+1-q).                \tag{3}
\]

At all six splits \(h+k=28\), \(22\le h\le27\), equation (3) is zero for
\(q=6\) and twelve for \(q=7\).  Hence every selected kernel has dimension
at most six.

## 3. Why \(q=4\) is legitimately excluded here

The primary note cites Sections 4--5 of the low-role selected-lift theorem.
Its headline low-\(h\) inequality does not hold at \(h=22,\ldots,27\), but
that inequality was used only to force an a priori kernel bound.  It is not
needed after one assumes \(q=4\).

Indeed, for \(d=1,2\) the mixed pair-drop theorem gives a span \(W\) of
dimension at least four because

\[
 2\sigma>
 3\left(\left\lfloor{D\over2}\right\rfloor-2\right).     \tag{4}
\]

If the row kernel \(K\) had dimension four, then \(W=K\).  The singleton
incidence proof can now be applied directly.  Its numerical content was
rechecked as follows.

For a selected singleton, divisibility by
\((z-r)(z+r)^2\) imposes three jet conditions, one of which is already its
exact selected row.  Its incidence space in \(K\) therefore has dimension
at least two.  If such a space were a plane, division by the cubic would
give a pencil in degree

\[
                         N=D-3=h-d.                         \tag{5}
\]

The two worst zero configurations both leave \(N\) distinct nonzero signed
pairs:

\[
       (\sigma-2)+d=N,\qquad
       (\sigma-1)+(d-1)=N.                                 \tag{6}
\]

The second count includes the one possibly missing triple--zero edge.  The
parity determinant is odd of degree at most \(2N-1\), so (6) makes it
identically zero.  The resulting square-pencil cap is \(N-2\), but the
number of other singleton cubics is

\[
             (\sigma-1)-(N-2)=3-d>0.                       \tag{7}
\]

Thus every singleton incidence space is a hyperplane or is absorbed by the
gcd.  For arbitrary numbers \(a_3,a_2\) of absorbed singleton cubics and
repeated quadratics, put \(g=3a_3+2a_2\).  Whenever a four-space can remain,
\(D-g\ge3\), and

\[
 \sigma-a_3
 \ge h+2-2d-\frac{h-d-2a_2}{3}\ge4.                       \tag{8}
\]

If all remaining singleton hyperplanes coincide, one section is divisible
by every selected singleton cubic and every absorbed repeated quadratic.
That is impossible because its required degree exceeds \(D\) by

\[
 3\sigma+2a_2-D=2h+3-5d+2a_2>0.                           \tag{9}
\]

Otherwise two remaining hyperplanes are distinct.  After dividing their
plane intersection by two more cubics, the exact terminal differences are

\[
\begin{aligned}
 2(\sigma-a_3-3)-\bigl(2(D-g-6)-1\bigr)
    &=5-2d+4a_3+4a_2>0,\\
 (\sigma-a_3-2)-\bigl((D-g-6)-2\bigr)
    &=5-d+2a_3+2a_2>0.                                    \tag{10}
\end{aligned}
\]

These are respectively the terminal parity excess and square-pencil-cap
excess.  The low residual degrees are even easier: a plane cannot be formed
after two cubic divisions, or a nonzero cubic cannot fit in the residual
space.  The independent checker exhausts every allowable
\((a_3,a_2)\) at every one of the twelve tuple/split combinations.

Therefore \(q=4\) is impossible here.  Pair drops give \(q\ge4\), and the
\(q=7\) Wronskian excess gives \(q\le6\), so every entry has

\[
                              q\in\{5,6\}.                  \tag{11}
\]

## 4. Exact two-point transport and the degree-nine common kernel

Fix the triple \(x\), and suppose two different ordinary singleton choices
\(s,t\) both have \(q=6\).  Since \(D+1=L+2\), rank-nullity gives a
four-dimensional relation space for each choice.  Equation (1) has ten
classes, so the relation-to-polynomial construction gives

\[
          \mathcal S_s,\mathcal S_t
             \subseteq\mathbb C[z]_{\le10-4}
             =\mathbb C[z]_{\le6},\qquad
          \dim\mathcal S_s=\dim\mathcal S_t=4.             \tag{12}
\]

Here the subscript records the singleton left in the complement.  Thus in
the \(s\)-complement selection, \(t\) is selected.  Restoring \(t\) uses

\[
                   f_t=(z-t)^2(z+t),                        \tag{13}
\]

and the correctly indexed transports are

\[
       f_t\mathcal S_s\subseteq\mathcal K_{s,t},\qquad
       f_s\mathcal S_t\subseteq\mathcal K_{s,t}.            \tag{14}
\]

At the newly restored point the square in \(f_t\) kills the complete first
jet.  At every old row the factor is a local unit, and the product rule is
exactly the usual regular-unit change of normalization.  This includes
\(t=0\), when \(f_t=z^3\); no division by \(t\) occurs.

Since the factor in (13) is cubic, (12)--(14) place the common kernel in

\[
                    \boxed{\mathcal K_{s,t}
                       \subseteq\mathbb C[z]_{\le9}}.       \tag{15}
\]

The restored baseline is

\[
                          4^2 3^6 1_x1_s1_t,                \tag{16}
\]

of mass \(29\).  There are three simple rows in (16): the two moving rows
and the fixed row at \(x\).

## 5. The common kernel has dimension exactly four

If the common kernel contained a five-space, the exact rows in (16) would
force Wronskian weight

\[
 2(5-4)+6(5-3)+3(5-1)=2+12+12=26.                          \tag{17}
\]

A five-space in \(\mathbb C[z]_{\le9}\) has cap

\[
                         5(9+1-5)=25.                        \tag{18}
\]

This one-unit contradiction survives every gcd.  More explicitly, at an
exact order-\(m\) row, if the gcd has local order \(g\le m\), division leaves
an exact order-\(m-g\) row.  Combining its reduced Wronskian weight with the
\(5g\) decrease in the cap gives

\[
        5g+\max(0,5-m+g)\ge\max(0,5-m).                    \tag{19}
\]

If \(g>m\), the row is automatic, but
\(5g>\max(0,5-m)\).  Gcd roots away from the displayed nodes only decrease
the cap.  Thus (17)--(19) prove

\[
                         \dim\mathcal K_{s,t}\le4.           \tag{20}
\]

Each space in (14) is four-dimensional, so both fill the common kernel.

## 6. Coprime intersection and the fixed-row contradiction

For symbolic \(s,t\), the exact resultant of the two transport cubics is

\[
 \operatorname{Res}_z(f_s,f_t)
             =-(s-t)^5(s+t)^4.                              \tag{21}
\]

Distinctness and nonoppositeness make (21) nonzero.  If \(s=0\), then
\(t\ne0\) and (21) is still nonzero, so the zero case is genuinely included.
Consequently

\[
 f_t\mathbb C[z]_{\le6}\cap f_s\mathbb C[z]_{\le6}
       =f_sf_t\mathbb C[z]_{\le3},                         \tag{22}
\]

which has dimension four.  Equations (14), (20), and (22) force

\[
 \mathcal K_{s,t}=f_sf_t\mathbb C[z]_{\le3},\qquad
 \mathcal S_s=f_s\mathbb C[z]_{\le3}.                     \tag{23}
\]

The first equality is a dimension argument in the intersection; the second
comes by cancelling \(f_t\), not by confusing the moving and complementary
indices.

The fixed singleton \(x\) in (1) supplies an exact simple row

\[
                         (U_xS)'(x)=0,\qquad U_x(x)\ne0.     \tag{24}
\]

Structural separation gives

\[
                         f_s(x)=(x-s)^2(x+s)\ne0.           \tag{25}
\]

Put \(S=f_sV\).  In local coordinates at \(x\), the coefficient of
\(V'(x)\) in (24) is exactly

\[
                              U_x(x)f_s(x),                  \tag{26}
\]

which is nonzero by (25).  Hence (24) is a nonzero functional on the full
four-space \(\mathbb C[z]_{\le3}\); it cannot annihilate the space asserted
in (23).  Two \(q=6\) singleton choices for the same \(x\) are impossible.

## 7. Grid consequence and scope

There are seven choices of the selected triple \(x\).  The preceding result
allows at most one \(q=6\) entry in each row, hence at most seven \(q=6\)
entries in the entire grid.  A column is contaminated only if it contains at
least one such entry, so at most seven singleton columns are contaminated.
With \(N=h+1\) and \(N=h-1\), respectively, the number of all-\(q=5\) columns
is at least

\[
             N-7=h-6\quad\hbox{or}\quad N-7=h-8.            \tag{27}
\]

These lower bounds are at least sixteen and fourteen over
\(22\le h\le27\).

Nothing above turns a \(q=5\) selection into a contradiction.  The audited
conclusion is therefore exactly the singleton-swap cap and its grid-level
dimension drop, not closure of \(4^2 3^7 1\) or of either original tuple.

## 8. Independent executable audit

[verify_live_three_zero_higher_split_p28_two_quartic_singleton_swap_q6_cap_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_two_quartic_singleton_swap_q6_cap_independent_audit.py)
checks all twelve tuple/split selections, re-runs every conditional \(q=4\)
incidence inequality through arbitrary absorption, verifies every five-space
gcd correction, factors the universal cubic resultant, computes the
intersection rank both with and without a zero singleton, and tests the
nonzero coefficient in the fixed-simple-row contradiction.
