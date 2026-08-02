# Minimal two-cell R2 restoration forces the rank back below 55

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let \(M^\circ\) be the rank-\(54/52\), full-R2 transverse boundary packet
from the
[one-cell analyses](level-two-two-invertible-transverse-column-site5-one-cell-r2-obstruction.md).
Consider the genuinely two-cell plane

\[
 M(s,t)=M^\circ+sE_{04(0,0)}+tE_{05(0,0)}.                    \tag{1}
\]

The first move is the rank-raising incidence lift: away from the R2 locus,
the calibration \(M(1,0)\) has

\[
 \operatorname{rank}D=55,\qquad
 \operatorname{rank}D_{\rm mixed}=53,\qquad
 e_{0^6},e_{1^6}\in\operatorname{im}D.                         \tag{2}
\]

The second move is the smallest support change capable of restoring the
output-one witness lost at root \(0\). The exact result is:

\[
 M(s,t)\text{ has full literal R2}
 \quad\Longleftrightarrow\quad
 s=0\ \text{or}\ t=-84,                                       \tag{3}
\]

and on both lines in (3),

\[
                         \operatorname{rank}D\le54.             \tag{4}
\]

Thus this minimal two-cell repair plane contains no full-R2
rank-\(55/53\) linear-L0 incidence survivor.

## Exact R2 locus

The only blocks moved in (1) are

\[
 M_{04}(s)=
 \begin{pmatrix}s&85\\0&87\end{pmatrix},
 \qquad
 M_{05}(t)=
 \begin{pmatrix}84+t&87\\0&28\end{pmatrix}.                    \tag{5}
\]

At root \(0\), the fixed edges \(02,03\) provide output-zero witnesses.
Among all incident blocks, \(M_{04}\) is an output-one pure column exactly
when \(s=0\), while \(M_{05}\) is an output-one pure column exactly when
\(84+t=0\). There is no other output-one witness. All other roots retain
fixed witnesses outside the two moved cells. This proves (3) over
\(\mathbf C\), not just on a sampled grid.

The four audited support representatives are

\[
\begin{array}{c|c}
(s,t)&\text{failing R2 roots}\\ \hline
(0,0)&\varnothing\\
(0,-84)&\varnothing\\
(1,0)&\{0\}\\
(1,-84)&\varnothing.
\end{array}                                                     \tag{6}
\]

## Exact incidence calibrations

For the same four points, the five-rank signatures

\[
 \bigl(
 \operatorname{rank}D,\operatorname{rank}D_{\rm mixed},
 \operatorname{rank}[D\mid e_{0^6}],
 \operatorname{rank}[D\mid e_{1^6}],
 \operatorname{rank}[D\mid e_{0^6}\mid e_{1^6}]
 \bigr)                                                         \tag{7}
\]

are

\[
\begin{array}{c|c}
(s,t)&\text{signature}\\ \hline
(0,0)&(54,52,54,54,54)\\
(0,-84)&(53,51,53,53,53)\\
(1,-84)&(54,52,54,54,54)\\
(1,0)&(55,53,55,55,55).
\end{array}                                                     \tag{8}
\]

So the plane displays the tradeoff exactly: the generic incidence lift
has the desired \(55/53\) signature but fails R2, while the minimal support
repair restores R2 and simultaneously restores a sixth kernel direction.

Both plane directions lie on zero-potential-sum edges. Therefore the
generic-kernel equation and all selected level-two rows hold identically
throughout (1). Since edges \(04\) and \(05\) share root \(0\), no perfect
matching uses both; the selected identities have no \(st\) term. The exact
checker audits all four bidegree corners.

## Polynomial kernels on the two R2 lines

On line A, \(s=0\), write

\[
                   D_A(t)=D_A^{(0)}+tD_A^{(1)}.
\]

There is an integral degree-one tangent
\(x_A(t)=x_{A,0}+tx_{A,1}\) with
\(D_A(t)x_A(t)=0\).

On line B, \(t=-84\), write

\[
                   D_B(s)=D_B^{(0)}+sD_B^{(1)}.
\]

There is an integral degree-four tangent
\(x_B(s)=\sum_{j=0}^4s^jx_{B,j}\) with
\(D_B(s)x_B(s)=0\).

For each line, the checker verifies every coefficient identity

\[
 D_\bullet^{(0)}x_{\bullet,j}
 +D_\bullet^{(1)}x_{\bullet,j-1}=0,                             \tag{9}
\]

including the two endpoint coefficients. At parameter value \(2\), the
polynomial tangent and the five universal vertex gauges have rank six.
They are therefore independent over the corresponding rational-function
field. Every \(55\)-minor vanishes identically, and specialization proves
(4) at every complex point of both lines.

The sparse integral kernel data decode to 5,857 bytes with SHA-256
\(3392f3490091d86f0c8d24fcc1173e052c6c763b823fd228c14a8bcf8f30803b\).
The standard-library checker
[verify_level_two_two_invertible_transverse_column_minimal_r2_restoration_plane.py](../computations/verify_level_two_two_invertible_transverse_column_minimal_r2_restoration_plane.py)
audits the plane, the exact R2 strata, generic-kernel and selected rows,
both polynomial kernels, gauge independence, and all ranks in (8).

## Remaining scope

This theorem handles the smallest two-cell support repair for the
\(04(0,0)\) incidence lift. It does not classify the analogous
\(04(1,0)\), root-\(1\), or higher-dimensional repair families. More
general simultaneous changes can create alternative pure witnesses while
moving additional entries, so the full 32-scalar incidence/R2 intersection
remains open.
