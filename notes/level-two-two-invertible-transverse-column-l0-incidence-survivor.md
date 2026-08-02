# A dense transverse packet survives linear L0 incidence

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

There is an exact packet on the dense transverse-column potential ray with

\[
 \operatorname{rank}D=55,\qquad
 \operatorname{rank}D_{\mathrm{mixed}}=53,\qquad
 e_{0^6},e_{1^6}\in\operatorname{im}D,
 \qquad D=d\Psi_M.                                             \tag{1}
\]

Over
\(\mathbf Q,\mathbf F_{101},\mathbf F_{32003},\mathbf F_{1000003}\), its
five incidence ranks are

\[
\begin{array}{c|c}
\text{matrix}&\text{rank over all four fields}\\ \hline
D&55\\
D_{\mathrm{mixed}}&53\\
[D\mid e_{0^6}]&55\\
[D\mid e_{1^6}]&55\\
[D\mid e_{0^6}\mid e_{1^6}]&55.
\end{array}                                                     \tag{2}
\]

Thus linear L0 incidence alone does not close the dense transverse normal
form. This is not a factored-L0 or overlapping-L1 completion. It is also
not an R2 survivor: literal R2 exits remain at roots \(1,2,3,4,5\) but fail
at the invertible root \(0\).

## Exact packet

Keep the normalized transverse endpoint matrices and potentials

\[
\begin{aligned}
 X_0=X_1&=I_2,&
 X_2&=e_0e_0^{\mathsf T},&
 X_3&=e_0e_1^{\mathsf T},&
 X_4=X_5&=0,\\
 \nu&=\tfrac12(1,1,1,1,-1,-1).
\end{aligned}                                                   \tag{3}
\]

The six determined core blocks are

\[
 M_{01}=J,\qquad
 M_{02}=M_{12}=e_1e_0^{\mathsf T},\qquad
 M_{03}=M_{13}=M_{23}=e_0e_0^{\mathsf T},                      \tag{4}
\]

and \(M_{45}=0\). On the eight zero-multiplier edges take

\[
\begin{array}{c|c@{\qquad}c|c}
04&\begin{pmatrix}1&85\\0&87\end{pmatrix}&
05&\begin{pmatrix}84&87\\0&28\end{pmatrix}\\[6pt]
14&\begin{pmatrix}0&74\\0&66\end{pmatrix}&
15&\begin{pmatrix}0&76\\37&0\end{pmatrix}\\[6pt]
24&\begin{pmatrix}0&46\\0&23\end{pmatrix}&
25&\begin{pmatrix}56&0\\0&0\end{pmatrix}\\[6pt]
34&\begin{pmatrix}0&3\\29&0\end{pmatrix}&
35&\begin{pmatrix}0&51\\0&96\end{pmatrix}.
\end{array}                                                     \tag{5}
\]

These are the earlier structured incidence-survivor blocks with the single
cell \(M_{04}(0,0)\) changed from \(0\) to \(1\). With the transverse core
(4), the unlifted packet has ranks \(54/52\); this one-cell lift gives the
exact \(55/53\) ranks in (1).

## Generic kernel and selected rows

All changes in (5) occur on edges with zero multiplier sum. Therefore the
60 scalar generic-kernel equations remain exact. With direct selected value
\(-1\), all 64 selected level-two rows vanish. The matching tensor has
support \(28/64\).

The differential has nullity five. Its five independent trace-zero vertex
gauges lie in the kernel, so they span the full differential kernel. The
universal 256 endpoint-slice identities and Euler relation

\[
                              D(M)=3\Psi(M)                    \tag{6}
\]

are also exact. Together with (2), these facts establish precisely the
necessary linear L0 tangent-incidence condition and nothing stronger.

## R2 boundary and invertible spokes

At root \(0\), the determined edges \(02,03\) are pure in output column
zero. The lifted block \(04\) and the full block \(05\) are not pure in
either column, while both endpoint stars are nonzero outside the selected
binary outputs. Hence root \(0\) has no output-one R2 witness.

The other five roots retain two distinct pure-column witnesses. The exact
R2 status is therefore

\[
                     \text{passing roots }(1,2,3,4,5),
                     \qquad\text{failing root }(0).             \tag{7}
\]

This failure is not caused by a singular zero-spoke degeneration. Both zero
sites have invertible core spokes:

\[
 \det M_{04}=87,\quad \det M_{34}=-87,\qquad
 \det M_{05}=2352,\quad \det M_{15}=-2812.                     \tag{8}
\]

Thus the packet isolates the intersection of the exact L0 incidence locus
with a one-root R2 boundary.

## Exact audit and scope

The standard-library checker
[verify_level_two_two_invertible_transverse_column_l0_incidence_survivor.py](../computations/verify_level_two_two_invertible_transverse_column_l0_incidence_survivor.py)
verifies the one-cell replacement scope, all generic-kernel and selected
rows, the exact rational and three-prime ranks in (2), the five-dimensional
gauge kernel, the universal L0 identities, every rootwise pure-column
table, and the spoke determinants (8). It passes normal, optimized, and
isolated Python.

The remaining sharp question is whether the dense transverse incidence
locus meets full R2. This packet does not answer it. Nor does it classify
factored L0 or overlapping L1 on the incidence locus.

The first bounded follow-up,
[the site-\(4\) one-cell obstruction](level-two-two-invertible-transverse-column-one-cell-r2-obstruction.md),
excludes every affine lift supported on a zero entry of one site-\(4\)
spoke. General simultaneous motion of the free cells remains open.
