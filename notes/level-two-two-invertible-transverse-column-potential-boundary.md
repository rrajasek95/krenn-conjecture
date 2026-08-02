# Non-dense transverse-column potentials close; one dense ray survives

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let a binary six-site residual packet satisfy

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix}.                \tag{1}
\]

Suppose the endpoint ranks are

\[
                              (2,2,1,1,0,0),                    \tag{2}
\]

with invertible sites \(I=\{0,1\}\), rank-one sites
\(T=\{2,3\}\), and zero sites \(Z=\{4,5\}\). Write
\(X_t=a_tb_t^{\mathsf T}\). Assume that the two rank-one sites miss
different selected columns. Up to exchanging their labels and the selected
columns,

\[
                              b_2\in\mathbf C^*e_0,\qquad
                              b_3\in\mathbf C^*e_1.             \tag{3}
\]

If the potential vector is not on the dense ray

\[
                (\nu_0,\ldots,\nu_5)
                    =\tau(1,1,1,1,-1,-1),\qquad\tau\ne0,       \tag{4}
\]

then

\[
                              \operatorname{rank}d\Psi_M\le52. \tag{5}
\]

The sole support envelope not closed by (5) is exactly (4). Unlike the
same-column dense ray, it does not acquire four extra generic-kernel
syzygies: an exact packet on (4) has differential rank \(55\), satisfies all
generic-kernel equations, and has literal residual R2 exits at all six
roots. Thus (4) is a genuine next L0/L1 boundary, not only an enlarged
support calibration.

## Exact transverse core

Independent local basis changes at the four nonzero sites give

\[
 X_0=X_1=I_2,\qquad
 X_2=e_0e_0^{\mathsf T},\qquad
 X_3=e_0e_1^{\mathsf T}.                                      \tag{6}
\]

The six core numerators in (1) are

\[
\begin{array}{c|c}
\text{edge}&X_uJX_v^{\mathsf T}\\ \hline
01&J\\
02,\ 12&e_1e_0^{\mathsf T}\\
03,\ 13,\ 23&e_0e_0^{\mathsf T}.
\end{array}                                                     \tag{7}
\]

Every matrix in (7) is nonzero. Hence all six core potential sums are
nonzero, including

\[
                              \nu_2+\nu_3\ne0.                  \tag{8}
\]

In particular \(M_{23}\) is a determined nonzero rank-one block; there is
no free-cross subcase inside this transverse chart. Each edge incident with
a zero endpoint has zero numerator and is arbitrary exactly when its
potential sum vanishes.

## The 39 potential envelopes

The potential support is therefore controlled by the same nine optional
edges as in the same-column census: the eight core-to-zero edges and
\(45\). Encode the six potentials by signed orbits
\(\{\lambda,-\lambda\}\), with \(0\) treated separately. There are \(4088\)
canonical signed encodings. Requiring all six sums in the core to be
nonzero leaves \(1574\), and quotienting by the independent exchanges

\[
                    0\leftrightarrow1,\qquad
                    2\leftrightarrow3,\qquad
                    4\leftrightarrow5                         \tag{9}
\]

gives exactly \(39\) zero-sum support envelopes. Before quotienting there
are \(131\) labelled support graphs; the local-colour count below is
constant on every orbit in (9).

Use the exact cell support in (7), not an arbitrary rank-one enlargement.
A differential cell column can be nonzero only if the four complementary
sites admit a perfect matching at its local binary word. The exact census is

| potentially active cell columns | number of envelopes |
|---:|---:|
| 4 | 1 |
| 16 | 2 |
| 20 | 6 |
| 28 | 3 |
| 32 | 3 |
| 40 | 9 |
| 44 | 8 |
| 48 | 2 |
| 52 | 4 |
| 60 | 1 |

Every uncounted column vanishes identically on the support closure. Thus the
first \(38\) envelopes have differential rank at most \(52\).

The unique \(60\)-column envelope has every core-to-zero edge live and
\(M_{45}=0\). Its eight zero-sum equations force the four core potentials
to equal one nonzero \(\tau\) and both zero potentials to equal \(-\tau\).
This is precisely (4), proving both the bound (5) and uniqueness of its
exception.

## An exact dense R2 guard

Set \(\tau=\tfrac12\) and use the normalized endpoint matrices (6). Then
every core multiplier sum is one, so take the six core blocks literally
from (7), take \(M_{45}=0\), and choose the eight free core-to-zero blocks
integrally. The checker uses column-one blocks on \(04,14\) and otherwise
deterministic full blocks. The resulting differential ranks are

\[
                  \operatorname{rank}_{\mathbf Q}d\Psi_M
                 =\operatorname{rank}_{101}d\Psi_M
                 =\operatorname{rank}_{1{,}000{,}003}d\Psi_M
                 =55.                                         \tag{10}
\]

This packet has five independent trace-zero gauge directions and the
following planned R2 witnesses:

| root | output \(0\) | output \(1\) |
|---:|---:|---:|
| 0 | \(02\) | \(04\) |
| 1 | \(12\) | \(14\) |
| 2 | \(23\) | \(20\) |
| 3 | \(30\) | missing-\(P_3\) endpoint block |
| 4 | \(p\)-endpoint block | \(q\)-endpoint block |
| 5 | \(p\)-endpoint block | \(q\)-endpoint block |

The two witnesses at each root are distinct and pure in the required
physical output columns. Both zero sites also have invertible rank-one-core
spokes; the displayed determinants are

\[
\begin{array}{c|rr}
z&\det M_{2z}&\det M_{3z}\\ \hline
4&-77&416\\
5&445&-77.
\end{array}                                                     \tag{11}
\]

Thus even the invertible-spoke interior of the dense transverse ray survives
the generic-kernel and R2 screens. With direct selected value \(-1\), all
64 selected level-two rows also vanish. Equation (10) is not presented as
an L0/L1 completion. The subsequent
[linear-L0 obstruction](level-two-two-invertible-transverse-column-l0-obstruction.md)
excludes this exact packet.

## Exact audit and remaining boundaries

The standard-library checker
[verify_level_two_two_invertible_transverse_column_potential_boundary.py](../computations/verify_level_two_two_invertible_transverse_column_potential_boundary.py)
verifies the 60 normalized numerator scalars, all 131 labelled and 39
unlabelled support envelopes, every local-colour complementary matching,
uniqueness of (4), all 60 dense generic-kernel scalars, all 64 selected
rows, the exact rational and two-prime ranks, the five gauges, and every R2
witness. It passes normal, optimized, and isolated Python.

This theorem covers exactly the opposite one-column/one-column chart.
Other choices of the eight free blocks on the dense ray (4), including its
singular zero-spoke degenerations, still require L0/L1 analysis. Mixed
one-column/two-column rank-one pairs are not covered and remain a separate
endpoint geometry. The
same-column zero-multiplier cross \(\nu_2+\nu_3=0\), where \(M_{23}\) is
free, is closed separately by the
[zero-cross rectangle theorem](level-two-two-invertible-same-column-zero-cross-closure.md).
