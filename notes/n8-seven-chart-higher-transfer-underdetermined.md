# The seven-chart incidence does not determine its higher transfer

## Result

The exact lex contraction of the 31 by 31 support-incidence matrix leaves
the seven target chart types

\[
                   R_{25},R_{26},R_{27},R_{28},R_{29},R_{30},R_{31}
\]

and the seven repaired zero-column types

\[
                   C_{18},C_{19},C_{21},C_{23},C_{26},C_{29},C_{31}.
\]

On these critical spaces the transferred **incidence** differential is
exactly zero.  In particular, the first support layer does not cancel chart
types 27--31.

It also does not decide whether a later filtered differential cancels them.
The 31-chart ledger specifies the leading map $D_0$, but it specifies no
higher operator $\delta$.  Exact reconstruction of the contraction shows
that every rational 7 by 7 higher differential is compatible with the same
leading incidence as an abstract filtered complex.  Consequently no
two-chart reduction follows from the incidence data alone.

## Exact contraction

Let $D_0:C_1\to C_0$ be the orbit-incidence matrix.  Lexicographic column
elimination produces 24 normalized pivot sources $u_p$, with

\[
                    D_0u_p=e_p+\text{later rows},
\]

and seven zero representatives $z_c$.  Reduction in increasing pivot-row
order defines

\[
 h:C_0\longrightarrow C_1,
 \qquad
 \pi:C_0\longrightarrow H_0,
 \qquad
 \Sigma:H_1\longrightarrow C_1,
 \qquad
 p:C_1\longrightarrow H_1.
\]

The checker verifies on every one of the 31 row and column basis vectors

\[
 D_0h+i_H\pi=I_{C_0},\qquad
 hD_0+\Sigma p=I_{C_1},\qquad
 \pi D_0=0,\qquad D_0\Sigma=0,
\]

as well as $\pi i_H=I$, $p\Sigma=I$, and $hi_H=0$.  The frozen exact
maps have the following census.

| map | nonzero rational entries | largest denominator |
|---|---:|---:|
| $\Sigma$ | 49 | 32 |
| $\pi$ | 67 | 6 |
| $h$ | 185 | 48 |
| $p$ | 7 | 1 |

Their joint exact digest is
`b95373b7649341779195f5a3dfd018783c77dc731c8bef5a9b152590dbc4ee66`.

Since $D_0\Sigma=0$, the critical map supplied by this layer is zero.
This is also forced by the already certified rank 24: the 24 matched pairs
account for the entire rank of $D_0$.

## Why the higher transfer is underdetermined

For any matrix $B:H_1\to H_0$, introduce a formal filtration-one
perturbation

\[
                       \delta_B=i_H Bp.
\]

It has the same leading differential $D_0$.  Because $hi_H=0$, one has
$h\delta_B=0$, so the homological-perturbation series terminates
immediately and gives

\[
 \Omega_B
 =\pi\delta_B(I+h\delta_B)^{-1}\Sigma
 =\pi i_HBp\Sigma
 =B.                                                        \tag{1}
\]

The checker evaluates (1) on all 49 elementary matrices.  It thereby
certifies that all transferred ranks 0 through 7 occur while the leading
31-chart incidence remains unchanged.

For example, the rank-five choice

\[
 C_{18}\mapsto R_{27},\quad
 C_{19}\mapsto R_{28},\quad
 C_{21}\mapsto R_{29},\quad
 C_{23}\mapsto R_{30},\quad
 C_{26}\mapsto R_{31}
\]

has total generic rank $24+5=29$ and leaves exactly $R_{25},R_{26}$ in
the target cokernel.  The zero choice leaves all seven target types.  This
rank-five map is an underdetermination witness, not a claim that the actual
hafnian Macaulay differential realizes it.

## Minimal missing data

Suppose the first unrecorded part has filtration $r>0$.  The first
possible critical differential is

\[
                          \Omega_r=\pi\delta_r\Sigma.
\]

Thus the minimal information needed to decide the first higher page is the
7 by 7 compressed block $\pi\delta_r\Sigma$: 49 rational coefficients
after orbit normalization.  Counts of mixed factors, ordinary chart
adjacency, and the 31 by 31 leading incidence do not determine these
coefficients.

If that first block does not settle the five extra types, the full transfer
requires the finite sequence

\[
 \pi\delta\Sigma-\pi\delta h\delta\Sigma
 +\pi\delta h\delta h\delta\Sigma-\cdots .                 \tag{2}
\]

The minimal combinatorial input for (2) is:

1. the higher-filter output monomial orbits of each of the seven zero-column
   syzygies, with exact signed coefficients and stabilizer normalizations;
2. the higher-filter outputs of every matched source reached after applying
   $h$ to those rows; and
3. the filtration increment of every such transition, so that the finite
   path bound and the page of each cancellation are known.

Equivalently, one needs the source-labelled higher Macaulay columns on the
finite $h\delta$-reachable subgraph.  Row-side support incidence alone
forgets both the syzygy provenance and the higher outputs, precisely the
data used by (2).

## Consequence for the two-chart strategy

Types 27--31 survive the exact first-layer contraction.  They reduce to
types 25/26 if and only if the actual higher transfer kills the five
classes $R_{27},\ldots,R_{31}$ while retaining the desired two-dimensional
quotient (possibly over several filtration pages).  Establishing that
statement now has a sharp
computational target: build the source-labelled first unrecorded
$\delta_r$, compress it to $\pi\delta_r\Sigma$, and continue along the
reachable matched paths only when necessary.

## Reproduction

```sh
python3 computations/verify_n8_seven_chart_transfer.py
```

The script reconstructs the incidence from the matching model, verifies all
contraction identities over $\mathbb Q$, replays all 49 elementary formal
transfers, realizes every rank 0--7, and freezes the full census.
