# One shared gauge-coupled packet reaches \(6R\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Start with the rank-\(42/40\) three-edge repair that supplies complete R2
witness pairs at roots \(0,1,2,3\).  In the integrated gauge-coupled
member the right endpoint-star weights are

\[
                         r_4=17,\qquad r_5=19.             \tag{1}
\]

First add two pure-one cells

\[
                   M_{24}(11)=r_4=17,\qquad
                   M_{25}(11)=-r_5=-19.                   \tag{2}
\]

The two new mixed-slice contributions cancel by

\[
                   M_{24}(11)r_5+M_{25}(11)r_4=0.         \tag{3}
\]

Because the two cells share root \(2\), they cannot form a complementary
matching with each other.  They therefore introduce no quadratic
pollution in either pure slice.  The same right-weight cancellation also
permits

\[
\begin{array}{ll}
 M_{04}(11)=-17,&M_{05}(11)=19,\\
 M_{14}(11)=-17,&M_{15}(11)=19.
\end{array}                                                   \tag{4}
\]

Finally, with left endpoint-star weights \(\ell_0=11,\ell_1=13\), add

\[
                  M_{04}(00)=11,\qquad M_{14}(00)=13.       \tag{5}
\]

This pair shares root \(4\) and obeys the corresponding left-weight
relation, so it also preserves the slices.  These steps give rank
\(50/48\).

There is one further exact affine line through this packet.  Its direction
has the six nonzero cell changes

\[
\begin{array}{c|rrrrrr}
\text{cell}&01(00)&01(10)&03(00)&03(10)&05(00)&15(00)\\ \hline
\Delta&13&13&-26&-26&-22&-26.
\end{array}                                                   \tag{6}
\]

Every four-slice coefficient is quadratic in the residual packet.  Direct
evaluation at parameters \(0,1,2\) gives the same exact target at all three
points, so the entire affine line preserves the four slices.  At parameter
one, the original endpoint stars still give

\[
       (T_{00},T_{01},T_{10},T_{11})
                  =(e_{0^6},0,0,e_{1^6})                    \tag{7}
\]

literally, while the residual differential ranks rise to

\[
                 \operatorname{rank}D=51,\qquad
                 \operatorname{rank}D_{\rm mixed}=49.       \tag{8}
\]

The new cells give roots \(4\) and \(5\) their missing output-one
witnesses.  All six roots now have complete R2 witness pairs with nonzero
complementary cofactors.  Hence, for every subset \(A\subseteq\{0,\ldots,5\}\),
one may set

\[
 X_i=h_i e_0^{\mathsf T}\quad(i\in A),\qquad
 X_i=0\quad(i\notin A).                                     \tag{9}
\]

The common input line is isotropic, so every pair numerator and the
selected level-two tangent vanish.  All \(64\) active subsets satisfy the
generic-kernel equations, literal selected and L0 slices, and R2 at every
active root.  In particular one shared four-slice construction now covers
every endpoint-rank pattern \(kR+(6-k)Z\), \(0\le k\le6\), reaching the
all-rank-one case at rank \(51/49\).

There is also no rank-one restriction when exactly one selected endpoint
is active.  With all other selected matrices zero, every pair numerator
and the literal rare/rare slice vanish for an arbitrary \(2\)-by-\(2\)
matrix at that root.  Since all six roots have the witness pairs in
(10), the same packet realizes \(1I+5Z\), with the invertible site placed
at any of the six roots, at rank \(51/49\).

This construction is a stronger compatibility witness, not a
rank-\(55\) survivor and not a closure of any full endpoint-rank stratum.

## L1 boundary

For the all-six common-isotropic activation, the shared packet does not
extend to the overlapping L1 equations.  The system for the nonzero
selected column has size \(60\)-by-\(27\), rank \(25\), and nullity two;
both kernel vectors are vacuous edge scalars and neither contains a star
mode.  The zero selected-column system has rank \(13\), nullity \(14\),
and twelve independent star modes, but there is no mode from the first
system with which to form a factored tangent.  Adding the allowed direct
\(\Psi(M)\) column gives a one-dimensional span; adjoining either pure
target raises its rank to two, and adjoining both raises it to three.
Thus this exact \(6R\) packet lies on the shared L0/R2 boundary and
supplies no full-L1 survivor.

This failure concerns the displayed all-six activation.  It is not a
uniform L1 theorem for the entire endpoint-rank stratum.

The six displayed \(1I+5Z\) placements also fail L1 on this packet.  At
each possible invertible root, both \(60\)-by-\(27\) systems have rank
\(23\), nullity four, two independent star modes, and two vacuous modes.
All four products between the two star-mode bases map to zero under the
residual differential.  Even after adding the direct \(\Psi(M)\) column,
the span contains neither pure target.  Thus the single-invertible cases
are likewise shared-L0/R2 witnesses only.

An exhaustive L1 span census over the \(64\) common-isotropic rank-one
subsets sharpens the scope:

\[
\begin{array}{c|c|c|c}
|A|&\dim(\text{nonzero-column star space})
 &\dim(\text{direct + factored span})&\text{pure-target incidence}\\ \hline
0&12&51&\text{both}\\
1&2&18\text{ or }20&\text{at most one}\\
2&1&12&\text{neither}\\
3,4,5,6&0&1&\text{neither}.
\end{array}
\]

Thus the zero-active \(6Z\) case is the only member of this displayed
subset family whose complete L1 factored span contains both pure targets.
For \(6Z\), the original exact endpoint stars are themselves L1 modes
because both selected columns vanish, so the shared construction is
genuinely compatible there.  Every nonempty active subset fails a
necessary L1 incidence condition on this packet.

## Exact witnesses

The checker uses

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0&03&02\\
1&12&13\\
2&23&20\\
3&32&31\\
4&45&42\\
5&54&52.
\end{array}                                                   \tag{10}
\]

The standard-library checker
[verify_level_two_six_rank_one_gauge_coupled_repair.py](../computations/verify_level_two_six_rank_one_gauge_coupled_repair.py)
verifies the cancellation relations, the three-point affine-line identity,
all four exact differential slices, rational and three-prime ranks, the
twelve pure-column witnesses and their cofactors, and all \(64\) literal
eight-site rank-one active-subset cases.  It also checks one invertible
selected matrix at each of the six roots and the complete all-six L1 kernel.
It also checks all six single-invertible L1 kernels and their four zero
product outputs, plus the complete \(64\)-subset rank-one L1 span census.
Every span test includes the allowed direct \(\Psi(M)\) column.  It is
intended to run normally, with -O, and with -I -S.
