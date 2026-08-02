# Distinct invertible potentials close a \(2I+1R+3Z\) branch

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let a binary six-site packet satisfy the generic-kernel equations

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix},                 \tag{1}
\]

and residual R2. Suppose the endpoint ranks are

\[
                              (2,2,1,0,0,0).                     \tag{2}
\]

Call the invertible sites \(0,1\), the nonzero rank-one site \(r=2\),
and the zero sites \(Z=\{3,4,5\}\). If

\[
                              \nu_0\ne\nu_1,                    \tag{3}
\]

then

\[
                              \operatorname{rank}d\Psi_M\le48. \tag{4}
\]

Thus the entire distinct-invertible-potential branch misses rank 55. The
proof uses only the generic-kernel equation, R2 at the invertible roots,
and exact cofactor support. No L0 or L1 equation is used.

Together with the
[equal-core-potential closure](level-two-two-invertible-one-rank-one-three-zero-equal-core-potential-closure.md),
the only multiplier boundary not covered by these two results is

\[
                              \nu_0=\nu_1\ne\nu_r.               \tag{5}
\]

## The R2 dichotomy forces a coordinate shore factor

Write

\[
                              X_r=ab^{\mathsf T}.                 \tag{6}
\]

The three core numerators on \(01,0r,1r\) are nonzero, so

\[
 \nu_0+\nu_1\ne0,\qquad
 \nu_0+\nu_r\ne0,\qquad
 \nu_1+\nu_r\ne0.                                               \tag{7}
\]

In particular \(M_{01}\) is invertible, while

\[
 M_{ir}=c_i a^{\mathsf T}\ne0\qquad(i=0,1)                       \tag{8}
\]

for nonzero column vectors \(c_i\). At either invertible root, the
invertible edge \(01\) is not a pure-column R2 witness. The common factor
\(a\) gives the following exact dichotomy.

* If \(a\) is a physical coordinate vector, both blocks in (8) supply one
  common R2 witness colour.
* If both coordinates of \(a\) are nonzero, neither block in (8) is pure,
  so it supplies no R2 witness.

Define the two zero-attachment sets

\[
 A=\{z\in Z:\nu_z=-\nu_0\},\qquad
 B=\{z\in Z:\nu_z=-\nu_1\}.                                   \tag{9}
\]

Only vertices in \(A\) can carry nonzero \(0z\) blocks, and only vertices
in \(B\) can carry nonzero \(1z\) blocks. Under (3), these sets are
disjoint. In the noncoordinate branch, R2 would require at least two
distinct zero-site witness labels at each invertible root, hence

\[
                              |A|\ge2,\qquad |B|\ge2,             \tag{10}
\]

which is impossible for three zero sites. Therefore \(a\) is a coordinate
vector. Both rank-one edges supply one common witness, and R2 forces

\[
                              |A|\ge1,\qquad |B|\ge1.             \tag{11}
\]

After possibly swapping the two physical colours at \(r\), take
\(a=e_0\). This preserves differential rank and makes both blocks in (8)
supported in shore column zero.

## Eleven zero-sum support envelopes

Every edge touching a zero endpoint has zero numerator in (1), so its
entire binary block is arbitrary exactly at zero multiplier sum and
otherwise vanishes. The disjoint nonempty sets \(A,B\) lead to two cases.

### The attachment sets exhaust \(Z\)

Up to swapping the invertible roots, \(|A|=2\), \(|B|=1\). No edge from
\(A\) to \(B\) is live, by the first inequality in (7). The edge internal
to the doubled set \(A\) is live precisely when \(\nu_0=0\). The
rank-one site attaches to every member of \(A\), every member of \(B\),
or neither, according as \(\nu_r=\nu_0\), \(\nu_r=\nu_1\), or neither.
If \(\nu_0=0\), attachment to \(A\) is forbidden by
\(\nu_0+\nu_r\ne0\). Hence there are

\[
                              3+2=5                               \tag{12}
\]

support envelopes.

### One zero site is left over

Now \(|A|=|B|=1\); call the leftover vertex \(c\). The rank-one site can
attach to \(A\), to \(B\), to \(c\), or to none of them. Independently,
\(c\) can have a zero-sum edge to \(A\), to \(B\), or to neither.
The core constraints (7) remove the incompatible combinations. Up to
interchanging \(A,B\), the six survivors are

\[
\begin{split}
 &(r\!\to A,c\!\to A),\quad(r\!\to A,c\!\to B),\quad
   (r\!\to A,c\text{ isolated}),\\
 &(r\!\to c,c\text{ otherwise isolated}),\quad
   (r\text{ unattached},c\!\to A),\quad
   (r\text{ unattached},c\text{ isolated}).                     \tag{13}
\end{split}
\]

For example, if \(r\) attaches to \(c\), then
\(\nu_c=-\nu_r\); an additional edge from \(c\) to \(A\) or \(B\)
would contradict one of the last two inequalities in (7). Equations
(12)--(13) give eleven envelopes in total.

## Exact cofactor bounds

A cell column of \(d\Psi_M\) obtained by varying edge \(e\) is zero unless
the support on the four complementary vertices admits a perfect matching
with the required local colours. Enumerating the fifteen edge choices and
the sixteen complementary binary words gives

\[
\begin{array}{c|c|c}
\text{zero-site pattern}&\text{rank-one/leftover pattern}
 &\text{potentially active cell columns}\\ \hline
2+1& r\to A&32\\
2+1& r\to B&28\\
2+1& r\text{ unattached}&20\\
2+1,\ A\text{ internal}&r\to B&48\\
2+1,\ A\text{ internal}&r\text{ unattached}&36\\ \hline
1+1+1&r\to A,\ c\to A&32\\
1+1+1&r\to A,\ c\to B&36\\
1+1+1&r\to A,\ c\text{ isolated}&16\\
1+1+1&r\to c&24\\
1+1+1&r\text{ unattached},\ c\to A&28\\
1+1+1&r\text{ unattached},\ c\text{ isolated}&12.
\end{array}                                                       \tag{14}
\]

The count is cell-specific: the two core-to-rank-one blocks are restricted
to their common shore column, while every zero-multiplier block is an
arbitrary \(2\times2\) block. Since every column outside the counted sets
is identically zero, (14) directly yields

\[
                              \operatorname{rank}d\Psi_M\le48,  \tag{15}
\]

proving (4). Degenerate members are already contained in these support
closures.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_one_rank_one_three_zero_distinct_invertible_potential_closure.py](../computations/verify_level_two_two_invertible_one_rank_one_three_zero_distinct_invertible_potential_closure.py)
verifies the coordinate/noncoordinate R2 dichotomy, the five plus six
support classification, inequivalence of all eleven support graphs, and
every local-colour complementary cofactor. It obtains the exact active-cell
counts in (14) and records modular calibration ranks

\[
                              27,27,19,41,30,26,30,16,22,23,12
\]

over two prime fields. It passes normal, optimized, and isolated Python.
