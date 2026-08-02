# Non-dense potentials close the same-column \(2I+2R+2Z\) boundary

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let a binary six-site residual packet satisfy the generic-kernel equations

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

\[
                              X_t=a_tb_t^{\mathsf T}\qquad(t\in T).
                                                                    \tag{3}
\]

Assume that both rank-one sites miss the same selected endpoint column.
Equivalently, after exchanging the two selected columns,

\[
                              b_2,b_3\in\mathbf C^*e_0.        \tag{4}
\]

If

\[
                              \nu_2+\nu_3\ne0                 \tag{5}
\]

and the potential vector is not on the equal-core/opposite-zero ray

\[
                (\nu_0,\ldots,\nu_5)
                    =\tau(1,1,1,1,-1,-1),\qquad\tau\ne0,      \tag{6}
\]

then

\[
                              \operatorname{rank}d\Psi_M\le52. \tag{7}
\]

Thus this non-dense same-column branch misses rank \(55\). The theorem uses
only the generic-kernel equations, so it also applies after imposing
residual R2. It is disjoint from the earlier exact guard: that packet has
two nonzero selected columns at both rank-one sites, while the only support
envelope not closed here lies on the guard's potential ray (6).

## The rank-one cross dies covariantly

The four \(I\)-to-\(T\) numerators are nonzero, as are the \(01\)
numerator and its determinant. Consequently

\[
 \nu_0+\nu_1\ne0,
 \qquad \nu_i+\nu_t\ne0\quad(i\in I,t\in T).                  \tag{8}
\]

Moreover,

\[
 X_2JX_3^{\mathsf T}
       =(b_2^{\mathsf T}Jb_3)a_2a_3^{\mathsf T}=0             \tag{9}
\]

by (4). Equation (5) therefore forces

\[
                              M_{23}=0.                         \tag{10}
\]

For the differential-rank calculation, make independent local basis
changes at sites \(2,3\) sending \(a_2,a_3\) to \(e_0\). This does not
select a physical target coordinate and does not change differential rank.
Every \(I\)-to-\(T\) block is then supported in column zero at its
rank-one shore:

\[
                              M_{it}=c_{it}e_0^{\mathsf T}.     \tag{11}
\]

The block \(M_{01}\) is unrestricted for this support bound. Every remaining
edge has a zero endpoint, hence zero numerator, so its whole block is
arbitrary exactly when its potential sum vanishes and is zero otherwise.
This gives a purely covariant support envelope containing the original
packet.

## Exact potential/support boundary map

Only the eight core-to-zero edges and the edge \(45\) can now be optional.
Their support is determined by the relations

\[
                              \nu_u+\nu_v=0.                   \tag{12}
\]

There is a finite exact census. Partition the six potentials into the fixed
point \(0\) and nonzero orbits \(\{\lambda,-\lambda\}\) of negation. Label
each new orbit at its first occurrence and declare that first occurrence
positive. This signed restricted-growth encoding enumerates every possible
zero-sum relation over \(\mathbf C\), without choosing numerical values.

There are \(4088\) signed encodings on six labelled sites. Requiring every
core-pair sum in (8), together with (5), to be nonzero leaves \(1574\).
After quotienting by the independent exchanges

\[
                    0\leftrightarrow1,\qquad
                    2\leftrightarrow3,\qquad
                    4\leftrightarrow5,                         \tag{13}
\]

their zero-sum supports collapse to exactly \(39\) envelopes.

For each envelope, count a cell column of \(d\Psi_M\) only if the four
complementary sites admit a perfect matching at the specified local binary
word. The exact distribution is

| potentially active cell columns | number of envelopes |
|---:|---:|
| 4 | 1 |
| 12 | 2 |
| 16 | 1 |
| 20 | 6 |
| 24 | 3 |
| 28 | 2 |
| 32 | 4 |
| 36 | 3 |
| 40 | 10 |
| 44 | 2 |
| 48 | 3 |
| 52 | 1 |
| 60 | 1 |

Every uncounted differential column is identically zero on the entire
support closure. Hence each of the first \(38\) envelopes has differential
rank at most \(52\), giving (7).

The unique \(60\)-column envelope has all eight core-to-zero edges live and
the zero-zero edge dead. The eight equations

\[
                              \nu_c+\nu_z=0
                  \qquad(c\in I\sqcup T,z\in Z)                \tag{14}
\]

force all four core potentials to equal one nonzero \(\tau\), and both zero
potentials to equal \(-\tau\). Thus the sole dense exception is exactly
(6), not an unclassified extra support type. A deterministic specialization
of this enlarged same-column envelope has differential rank \(55\) modulo
both \(101\) and \(1{,}000{,}003\), so a support-only argument cannot remove
that final ray.

## Exact audit and frontier

The standard-library checker
[verify_level_two_two_invertible_same_column_potential_boundary.py](../computations/verify_level_two_two_invertible_same_column_potential_boundary.py)
enumerates all signed potential encodings, verifies the \(1574\to39\)
support quotient, proves uniqueness of (6), and audits every local-colour
complementary matching. It also calibrates every support envelope over two
prime fields. It passes normal, optimized, and isolated Python.

The formerly exceptional ray (6) is closed by the subsequent
[dense-ray syzygy theorem](level-two-two-invertible-same-column-dense-ray-closure.md),
which gives rank at most \(51\). Thus the full same-missing-column chart
with \(\nu_2+\nu_3\ne0\) is closed. The transverse one-column chart, where
the two missing selected columns differ and
\(b_2^{\mathsf T}Jb_3\ne0\), and the zero-potential cross
\(\nu_2+\nu_3=0\), where \(M_{23}\) is free, remain separate.
