# The complete h=3 output packet still lacks the carrier map

## Outcome

The smallest committed \(h=3\) augmented output packet has 45 literal rows:

~~~text
lower_6, Eq_6, Yw_6, physical-W_6, target_6, ores_6,
ainc, eta/sigma_7, q.
~~~

Its unconditional physical inventory consists of six \(r0\), six cap, six
split-response, and one placed Cartan column. These 19 columns are
independent. Granting the still-conditional primitive anchor gives rank 20
and necessarily carries physical \(q=1\). The completed full-alpha \(M_v\)
output is already in the rank-19 span and adds no column.

This is the most complete available protected/anchor/terminal/\(q\) row
packet. It is not the carrier boundary

\[
                         D_Q:B_Q\longrightarrow Z_Q.    \tag{1}
\]

The 45-row matrix is an output-side reduced-Eq map. The degree-two
common-carrier desuspension

\[
 \chi:\widetilde C^{(4)}\longrightarrow Q_1,            \tag{2}
\]

its reinsertion map \(\pi\), its vertical kernel, and its physical-\(q\)
input comparison have not been constructed. Therefore

\[
 L_1=-{1\over6}(r-2q)\chi|_{\ker\pi}                    \tag{3}
\]

is not yet a matrix, and the actual rank equality

\[
        \operatorname {rank}D_Q
        =\operatorname {rank}[D_Q\mid L_1]              \tag{4}
\]

cannot presently be evaluated numerically without inventing source
columns.

The first absent source column before (3) is the pointed common-carrier
primitive residue section

\[
                p=(-Q,-\operatorname {ores})            \tag{5}
\]

in word \(01211222\), repeated grade \(P3+K2\), together with its input
comparison and physical-\(q\) transport. Ordinary residue separates (5)
from every currently relevant reduced-Eq correction. Thus the first
cell/\(c_0\) debt is genuinely prior to the second \(c_1\) cell.

Conditionally granting (2), (5), and the common-\(H_0\) comparison, the
second-cell rank can be evaluated sharply. Even under the optimistic
assumption that every protected, anchor, terminal, and \(q\) entry of the
new filtered faces is zero, the strongest one-\(R=\mathbb Q[\beta]\)
generator misses the pure weighted face by one rank.

## 1. Complete available augmented block

The 45 rows count as

\[
 6+6+6+6+6+6+1+7+1=45.                                \tag{6}
\]

The unconditional columns have rank

\[
                 6+6+6+1=19.                           \tag{7}
\]

The physical covector

\[
                 q+\sum_i\operatorname {lower}_i
                    +\operatorname {ainc}               \tag{8}
\]

annihilates all 19 columns. The conditional primitive anchor also obeys
(8), with \((ainc,q)=(-1,1)\), and raises the rank to 20. The selected
full-alpha Cartan completion has zero ordinary residue, protected \(W\),
target, anchor incidence, and physical \(q\), with its exact eta/sigma
packet. It remains an output cell: the input equality and physical \(q\)
transport are explicitly open.

This distinction prevents reusing the rank-19 output matrix as \(D_Q\).
It has the right list of readout names, but the wrong domain, chain degree,
word-to-carrier comparison, and source differential.

## 2. Conditional second-cell rank

After granting the first pointed/common-carrier cell, work to first order
over \(\mathbb Q[\beta]/(\beta^2)\) in the filtered basis

~~~text
(p, beta*p, c1, beta*c1).
~~~

The strongest one-generator package is

\[
 dG=p+\beta c_1,\qquad
 \beta dG=\beta p.                                      \tag{9}
\]

Its two columns are

~~~text
(1,0,0,1), (0,1,0,0),
~~~

of rank two. Neither

~~~text
p       = (1,0,0,0),
beta*c1 = (0,0,0,1)
~~~

is in their span; adjoining either raises the rank to three. The primitive
anti-diagonal covector

\[
                         (1,0,0,-1)                    \tag{10}
\]

annihilates both columns in (9), reads \(1\) on \(p\), and reads \(-1\)
on \(\beta c_1\).

The companion checker extends this four-row block by all 45 physical rows
and sets the latter entries of the formal faces to zero. This is the most
favourable possible no-leakage assumption. The same rank jump survives,
so protected/anchor/terminal/\(q\) bookkeeping cannot remove the need for a
column with nonzero \(\beta c_1\) coordinate. Nonzero physical dressing may
add further debts but cannot create that missing filtered coordinate from
the old columns.

Adjoining one second column \((0,0,0,1)\) raises the rank to three and also
puts \(p\) in the span via (9). The coarse signature is necessary, not yet
a physical construction. The source-valid version is a first-moment
nullhomotopy

\[
 d\Gamma_1(z)
     =-{1\over6}(r-2q)\chi(z),\qquad z\in\ker\pi.        \tag{11}
\]

Its full 45-row boundary must be computed in the physical carrier grade.
An unshifted \(c_1\) column is not a substitute: it occupies the \(c1\)
coordinate, while (11) occupies \(\beta c1\); the checker verifies that
forgetting this distinction changes the rank.

## 3. Exact next finite test

Once \(\pi,\chi\), and a cycle basis \(z_1,\ldots,z_s\) are constructed,
form the literal columns

\[
 L_{1,j}=-{1\over6}(r-2q)\chi(z_j)\in Z_Q.              \tag{12}
\]

Include every row in (6), now at the correct carrier degree, in \(D_Q\).
Then the second cell exists exactly when

\[
 \boxed{
 \operatorname {rank}D_Q
 =\operatorname {rank}[D_Q\mid L_{1,1}\ \cdots\ L_{1,s}].} \tag{13}
\]

If (13) fails, exact linear duality supplies \(\lambda\) and \(z_j\) with

\[
                   \lambda D_Q=0,\qquad
                   \lambda L_{1,j}\ne0.                 \tag{14}
\]

Because the matrix in (13) includes the complete protected, anchor,
terminal, and physical-\(q\) rows, (14) is then eligible for the physical
generator/Fredholm alternative. Before (2) and the correctly graded
\(D_Q\) exist, the anti-diagonal (10) is only the exact filtered carrier
dual, not a physical terminal.

## 4. Sharp construction target

The dependency order is explicit.

1. Construct the pointed residue/common-\(H_0\) column (5), its input map,
   and physical-\(q\) transport. This defines \(\pi,\chi\) and lands the
   \(c_0\) comparison in one augmented carrier module.
2. Compute a basis of \(\ker H(\pi)\) and the literal 45-row columns (12).
3. Construct one \(\Gamma_1(z_j)\) per independent image column, or exhibit
   the physical covector (14).

The first absent column in the actual inventory is item 1. Conditional on
item 1, the rank calculation proves that item 3 requires one additional
filtered source direction already in the smallest one-dimensional
path-residue sector. Both may be faces of one enriched pointed comparison
family, but one free \(R\)-generator does not make them separate
boundaries.

## Verification

Run

~~~text
python3 computations/verify_h3_c1_complete_augmented_carrier_rank_gate.py
python3 -O computations/verify_h3_c1_complete_augmented_carrier_rank_gate.py
python3 -I -S computations/verify_h3_c1_complete_augmented_carrier_rank_gate.py
~~~

The checker pins the full reduced-Eq augmentation, direct-free pointed
composition gate, weighted \(c_1\) Bockstein gate, and literal \(M_v\)
scope. It recomputes the 45-row ranks and the conditional 49-row filtered
rank with exact rational arithmetic.
