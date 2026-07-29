# An arbitrary \(A_{23}\) block plus the adjacent \(A_{25}\) line still cannot activate a fourth cut

## 1. Result and exact scope

Keep the seven internal aggregate cells

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
35&E_{10},
\end{array}
\]

and allow the two adjacent blocks

\[
 A_{23}=X\in\operatorname{Mat}_{3\times3}(\mathbb C),
 \qquad
 A_{25}=E_{00}+tE_{11},\quad t\in\mathbb C,                \tag{1}
\]

to vary. Allow all \(108\) entries of the two boundary stars \(i6,i7\),
\(0\leq i<6\), and all nine entries of \(A_{67}\) to be arbitrary
complex numbers.

No such system satisfies the complete quotient identities on cuts
\(2,3,4\) together with cut \(0\), \(1\), or \(5\), while retaining the
three unit diagonal target fibres.

This is a genuine two-internal-block extension, but a narrow one:
\(A_{25}\) moves only on the affine line in (1), the other seven internal
blocks stay fixed, and no claim is made for an arbitrary second block or
for the global Krenn conjecture.

The exact checker is
[verify_three_cut_internal_23_arbitrary_block_adjacent_25_line_fourth_cut_obstruction.py](../computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_line_fourth_cut_obstruction.py).
Its exact reconnaissance and symbolic helper are
[explore_three_cut_internal_23_adjacent_25_11.py](../computations/explore_three_cut_internal_23_adjacent_25_11.py)
and
[test_three_cut_internal_23_adjacent_25_11_x12_crossratio_symbolic.py](../computations/test_three_cut_internal_23_adjacent_25_11_x12_crossratio_symbolic.py).

## 2. Stabilizing torus and honest modulus count

Use the same five effective characters \(r_0,c_0,c_2,r_1,r_2\) on
\(X=(x_{ab})\) as in the arbitrary-\(A_{23}\) theorem:

\[
\begin{array}{c|ccc}
&b=0&b=1&b=2\\ \hline
a=0&r_0c_0&r_0^2&r_0c_2\\
a=1&r_1c_0&r_1r_0&r_1c_2\\
a=2&r_2c_0&r_2r_0&r_2c_2.
\end{array}                                               \tag{2}
\]

There is a sixth independent character \(\tau\) which scales \(t\).
One literal extension to the internal site colours is

\[
\begin{gathered}
 g_{2,0}=g_{3,1}=g_{4,0}=r_0,\qquad g_{5,0}=r_0^{-1},\\
 g_{3,0}=c_0,\quad g_{3,2}=c_2,\quad
 g_{2,1}=r_1,\quad g_{2,2}=r_2,\\
 g_{0,1}=r_1^{-1},\qquad g_{1,2}=c_2^{-1},\qquad
 g_{5,1}=\tau/r_1,
\end{gathered}                                            \tag{3}
\]

with every unlisted internal factor equal to one. All seven fixed cells
and the base cell \(E_{00}\) of \(A_{25}\) have factor one, while

\[
                  g_{2,1}g_{5,1}=\tau.                   \tag{4}
\]

As usual, take

\[
 g_{6,c}=1,\qquad
 g_{7,c}=\left(\prod_{i=0}^{5}g_{i,c}\right)^{-1}          \tag{5}
\]

to keep all three diagonal target coefficients exactly one. Boundary
entries are only rescaled by nonzero factors and remain arbitrary.

An independent kernel computation starts with all \(18\) internal
site-colour scalars and the eight fixed-cell equations. Their stabilizer
has dimension \(10\); its effective character rank on the nine entries of
\(X\) is \(5\), and adjoining \(t\) raises the rank to \(6\). In
particular, every \(t\ne0\) is normalized to one without changing any
\(X\)-modulus.

The proof does not pretend that all dense \(X\) lie in finitely many
orbits. Across the \(512\) support masks of \(X\), the numbers having
respectively \(0,1,2,3,4\) torus moduli are

\[
                         328,\ 132,\ 42,\ 9,\ 1.          \tag{6}
\]

The coordinate quotients below erase the unused moduli exactly. The sole
modulus that survives a retained chart is the already known rectangle
cross-ratio \(\lambda\).

## 3. No \(Xt\) terms and the tenth coordinate block

Edges \(23\) and \(25\) share site \(2\), so no perfect matching contains
both. The checker verifies the resulting finite-difference identity on
every even subset of the six internal sites and every one of the nine
cells of \(X\). Thus the full matching tensor, every deleted-pair
cofactor, every boundary atom, and every cylinder column are affine
separately in \(X\) and \(t\), with no \(x_{ab}t\) term.

Let \(R_{ab}\) be the \(35\)-coordinate output block of \(x_{ab}\), and
let \(T\) be the corresponding output block of the moving \(E_{11}\) in
\(A_{25}\). Exact endpoint-ordered enumeration gives

\[
 |T|=35,\qquad
 |T\cap R_{10}|=|T\cap R_{11}|=|T\cap R_{12}|=9,          \tag{7}
\]

and

\[
 T\cap R_{ab}=\varnothing
 \quad\text{for }a\ne1,\qquad T\cap\operatorname{supp}(u_+)=\varnothing.
                                                               \tag{8}
\]

The four \(t\)-dependent deleted-pair cofactors are

\[
                         03,\quad04,\quad13,\quad34.      \tag{9}
\]

The pure targets satisfy

\[
 [0^6]\notin T,\qquad [1^6]\in T,\qquad[2^6]\notin T.     \tag{10}
\]

Every outside-support chart retains \(T,R_{11},R_{22}\), possibly with
additional \(R_{ab}\), and therefore preserves targets \(1,2\). The
old-locus charts use the class-dependent target pairs in (22). If an
omitted \(R_{ab}\) overlaps \(T\), the overlap is killed rather than
silently resurrected. The checker verifies that each omitted coefficient
then vanishes term by term from the projected boundary map and leaves all
six projected cylinder spans unchanged. Those coefficients remain
arbitrary complex values, not sampled zero/one values.

For any coordinate quotient \(\pi\) and actual common normal

\[
 N_z=C_2\cap C_3\cap C_4\cap C_z,
\]

the proof uses only the safe containment

\[
 \pi N_z\subseteq
 \pi C_2\cap\pi C_3\cap\pi C_4\cap\pi C_z
 =\overline N_z.                                         \tag{11a}
\]

It never assumes that projection commutes with intersection. Proving a
unit ideal modulo the possibly larger \(\overline N_z\) is therefore a
valid contradiction.

## 4. The \(480\) outside-support masks

Order the four entries outside the old five-cell locus by

\[
                         x_{10},x_{12},x_{20},x_{22}.      \tag{11}
\]

First-nonzero classification again partitions the \(480\) masks as

\[
                          256+128+64+32.                  \tag{12}
\]

With \(T\) retained, the quotient charts are

\[
\begin{array}{c|c|c|c}
\text{first cell}&\text{earlier forced zeros}&
\text{retained \(X\)-blocks}&\dim\overline N_{0,1,5}\\ \hline
x_{10}&-&10,11,21,22&2\\
x_{12}&10&12,11,21,22&1\\
x_{20}&10,12&10,20,11,21,22&2\\
x_{22}&10,12,20&10,12,20,11,21,22&1.
\end{array}                                               \tag{13}
\]

Here a retained forced-zero block keeps fixed cofactor equations but adds
no variable term. In every finite chart the safe projected common normal
is identical for final cut \(0,1,5\), contains the projected direct tensor,
and contains neither pure target \(1\) nor pure target \(2\).

Write

\[
 d=2{\bf1}_{x_{11}\ne0}+4{\bf1}_{x_{22}\ne0},
 \qquad b={\bf1}_{x_{21}\ne0}.                            \tag{14}
\]

The \(27\) finite retained-chart ideals have the following generator
counts:

\[
\begin{array}{c|c|c}
\text{family}&(d,b)&\text{generator counts}\\ \hline
x_{10}&
(0,0),(0,1),(2,0),(2,1),(4,0),(4,1),(6,0),(6,1)&
380,484,432,536,492,596,544,648\\
x_{12}&
(0,0),(0,1),(2,0),(2,1),(4,0),(4,1),(6,0)&
384,488,436,540,496,600,548\\
x_{20}&
(0,0),(0,1),(2,0),(2,1),(4,0),(4,1),(6,0),(6,1)&
440,544,492,596,552,656,604,708\\
x_{22}&
(4,0),(4,1),(6,0),(6,1)&
496,600,548,652.
\end{array}                                               \tag{15}
\]

Every reduced characteristic-zero standard basis is \([1]\).

## 5. The rectangle cross-ratio remains locked

The sole dependent retained support is

\[
                 \{x_{11},x_{12},x_{21},x_{22}\}.         \tag{16}
\]

Normalize

\[
 x_{12}=x_{11}=x_{22}=t=1,\qquad
 \lambda=x_{21}={x_{12}x_{21}\over x_{11}x_{22}}.         \tag{17}
\]

Span each projected cylinder at \(\lambda=0,1\) and intersect the four
expanded cylinders. For each final cut \(z=0,1,5\), the same safe plane is

\[
\begin{aligned}
 P_t=\langle e,v_t\rangle,\qquad
 e={}&[002100],\\
 v_t={}&[121200]+[001100]+[001200]+[002200]+[111110]
          +[221221].
\end{aligned}                                             \tag{18}
\]

The added word \([221221]\) is the direct contribution of the moving
\(A_{25}\) cell. It does not affect the exact functional

\[
             \ell_\lambda=[002100]^*-\lambda[001100]^*.   \tag{19}
\]

For every raw column of \(C_z(\lambda)\), the checker verifies that the
constant, linear, and quadratic coefficients of
\(\ell_\lambda(C_z(\lambda))\) vanish. Hence a vector
\(\alpha e+\beta v_t\) in the actual projected intersection satisfies
\(\alpha=\lambda\beta\), and therefore

\[
              \pi N_z(\lambda)\subseteq
              \langle v_t+\lambda e\rangle
              =\langle\pi H_S(\lambda)\rangle.             \tag{20}
\]

The resulting \(648\)-generator ideal is computed in the ordinary
polynomial ring

\[
                   \mathbb Q[\lambda,p^1,p^2,q^1,q^2]     \tag{21}
\]

and has reduced basis \([1]\). Thus no exceptional complex value of
\(\lambda\) survives.

## 6. The remaining \(32\) old-locus masks

For

\[
 L=\{x_{00},x_{01},x_{02},x_{11},x_{21}\},
\]

every support has no \(X\)-modulus, even after \(t\) is normalized. The
five interval quotients from the audited \(A_{23}\)-plane theorem extend
after retaining \(T\):

\[
\begin{array}{c|c|c|c|c|c|c}
\text{class}&|S|&P&\text{colours}&|\ker\pi|&
\dim\overline N&\text{generators}\\ \hline
x_{00}=0&16&\varnothing&0,2&141&1&292\\
x_{00}\ne0,\ x_{11}=x_{21}=0&4&\varnothing&1,2&107&1&376\\
x_{00}x_{21}\ne0,\ x_{11}=0&4&00,21&1,2&72&2&612\\
x_{00}x_{11}\ne0,\ x_{21}=0&4&00,11&1,2&71&3&560\\
x_{00}x_{11}x_{21}\ne0&4&00,11,21&1,2&71&3&664.
\end{array}                                               \tag{22}
\]

For every member of each interval, the projected boundary term list,
direct tensor, and all three final-cut normals agree exactly with the
representative. All five characteristic-zero ideals have reduced basis
\([1]\).

## 7. Literal shared-star equations and exact certificates

For boundary colours \(a,b\), write

\[
 p^a_{i,c}=A_{i6}[c,a],\qquad
 q^b_{i,c}=A_{i7}[c,b],\qquad r_{ab}=A_{67}[a,b].
\]

Literal endpoint-ordered matching expansion gives

\[
\begin{aligned}
 H_{ab}={}&r_{ab}H_S(X,t)+\beta_{X,t}(p^a,q^b),\\
 \beta_{X,t}(p,q)={}&
 \sum_{i<j}\sum_{c,d}
 \left(p_{i,c}q_{j,d}+p_{j,d}q_{i,c}\right)
 e_c^{(i)}e_d^{(j)}\otimes H_{S\setminus\{i,j\}}(X,t).
\end{aligned}                                             \tag{23}
\]

The checker assigns distinct nonzero rational values to all nine entries
of \(X\), the moving \(A_{25}\) coefficient, all \(108\) star entries,
and all nine entries of \(A_{67}\), using disjoint numerical ranges.
Direct eight-site matching enumeration
agrees with (23) on all nine boundary slices.

Each unit calculation retains two diagonal fibres and both ordered
off-diagonal fibres, using the same \(72\) star variables. A solution of
the full \(108\)-variable system must restrict to this packet. Since
\(\pi H_S\) belongs to every safe normal, arbitrary \(A_{67}\) is absorbed.
Every polynomial is a necessary projected consequence of the actual
system; a unit ideal over \(\mathbb Q\) remains a unit after scalar
extension to \(\mathbb C\).

In total the nonzero-\(t\) proof checks

\[
             5\text{ old-locus ideals}
             +27\text{ finite outside ideals}
             +1\text{ symbolic ideal}.                   \tag{24}
\]

For \(t=0\), the independently audited arbitrary-\(A_{23}\) theorem
applies directly. This exhausts every \(t\in\mathbb C\).

## 8. Reproduction

From the repository root, run

    uv run python computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_line_fourth_cut_obstruction.py

The clean locked-environment run on 2026-07-27 ended with

    arbitrary A23 plus A25=E00+tE11 fourth-cut obstruction: PASS
    t=0 inherited audited theorem; t!=0 normalized independently: PASS
    512 A23 masks partitioned 32+480; full modulus census exact: PASS
    35-cell t block, overlaps 9+9+9, and no X*t terms: PASS
    5 old-locus + 27 finite outside + Q[lambda] ideals: PASS
    projected normals and every killed arbitrary coefficient: PASS
    endpoint order, 108 shared-star entries, ordered fibres, A67: PASS
    ...
    outside_x12_crossratio_lambda: N=1, generators=648, 72.619s: PASS
    parallel exact-Q wall time: 164.567s

The complete process took \(166.70\) seconds of wall time. The \(33\)
Singular jobs run in parallel, so their individual timings do not sum to
this wall time.

## 9. Consequence and next frontier

With the other seven internal cells fixed, neither an arbitrary
\(A_{23}\) nor the adjacent deformation \(A_{25}=E_{00}+tE_{11}\) repairs
the missing fourth cut.

The next exact local extensions are now concrete:

1. test the other eight one-cell directions in \(A_{25}\), prioritizing
   cells whose output block preserves two pure targets;
2. allow a two-dimensional affine slice in \(A_{25}\), where the two new
   cells may introduce their first genuine torus cross-ratio;
3. perturb an internal edge disjoint from \(23\), where mixed matching
   terms \(x_{ab}t\) appear and the present affine-separation argument no
   longer applies.

Only the family (1) is proved here.
