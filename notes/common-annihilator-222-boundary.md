# The three-`K_2` common-annihilator boundary is impossible

This is a self-contained insert for the last disconnected case in
[`common-annihilator-plane-obstruction.md`](common-annihilator-plane-obstruction.md).
It gives a non-SAT compression of the exhaustive apex calculation.  The
companion checker is
[`verify_common_annihilator_222_boundary.py`](../computations/verify_common_annihilator_222_boundary.py).

## Setup and target coefficients

Write the two sites of each class as directed half-edges of the class
triangle:

\[
 U_0=\{01,02\},\qquad U_1=\{10,12\},\qquad
 U_2=\{20,21\}.
\]

For compact coefficient certificates below, use the numerical order

\[
                 (01,02,10,12,20,21)=(0,1,2,3,4,5).
\]

The proposed three components of the mixed-cofactor graph are

\[
                 01\!-!10,\qquad02\!-!20,\qquad12\!-!21. \tag{1}
\]

Consequently, every other mixed pair is a hole whose complementary
projected four-site cofactor is zero.  There are nine such holes.

For an ordered edge `uv`, let `x_uv^(st)` denote the scalar projected edge
coefficient with color `s` at `u` and color `t` at `v`.  Name the twelve
target-target entries on the three cross-class `K_2,2`s by

\[
\begin{array}{c|c|cccc}
\text{target}&\text{row/column sites}&\multicolumn{4}{c}{\text{entries}}\\ \hline
2&(01,02)\times(10,12)&a=x_{01,10}^{22}&b=x_{01,12}^{22}
                              &e=x_{02,10}^{22}&f=x_{02,12}^{22}\\
1&(01,02)\times(20,21)&c=x_{01,20}^{11}&d=x_{01,21}^{11}
                              &g=x_{02,20}^{11}&h=x_{02,21}^{11}\\
0&(10,12)\times(20,21)&i=x_{10,20}^{00}&j=x_{10,21}^{00}
                              &k=x_{12,20}^{00}&l=x_{12,21}^{00}.
\end{array}                                                \tag{2}
\]

Every edge in the pure four-set `S_r=R\U_r` has no coefficient transverse
to `e_r` at both endpoints.  Applied also to the two same-class edges, this
kills the same-class matching in each target coefficient.  Hence the three
nonzero pure coefficients are exactly

\[
 P_2=af+be\ne0,\qquad P_1=ch+dg\ne0,\qquad
 P_0=il+jk\ne0.                                          \tag{3}
\]

Choose a target-aligned apex `A_r in S_r`: all three incident projected
edge forms have endpoint factor `e_r` there.  An apex triple is written
`(A_0,A_1,A_2)`.

## Five scalar obstruction motifs

Simultaneously permuting the three classes and colors gives twelve apex
orbits.  They group into five scalar motifs:

\[
\begin{array}{c|c|c}
\text{motif}&\text{apex representatives (orbit size)}&
             \text{nonzero pure coefficients used}\\ \hline
A&(10,01,01)_6,(10,02,02)_6&P_1,P_2\\
B&(10,02,10)_6,(10,20,10)_6&P_0,P_2\\
C&(10,02,01)_6,(10,02,12)_6,(10,20,01)_6&P_0,P_1,P_2\\
D&(10,01,02)_6,(10,20,02)_6,(10,21,02)_2&P_0,P_1,P_2\\
E&(12,02,01)_6,(12,20,01)_2&P_0,P_2.
\end{array}                                                \tag{4}
\]

The orbit sizes in (4) sum to `64`.  After applying the endpoint-line
zeros at the displayed apices, selected scalar coefficients of the nine
zero cofactors give the following equations:

\[
\begin{array}{c|l}
A&df=bh=bg=ah=0,\\
B&fi=ek=bi=ak=0,\\
C&el=ek=df=cf=0,\\
D&ak=a\nu=bh=bg=0,\qquad \mu\nu+fi=0,\\
E&fj=fi=bi=b\sigma=0,\qquad ek+\rho\sigma=0.
\end{array}                                                \tag{5}
\]

The four auxiliary entries in the last two rows are

\[
 \mu=x_{02,10}^{20},\quad \nu=x_{12,20}^{20},\qquad
 \rho=x_{02,12}^{20},\quad \sigma=x_{10,20}^{20}.       \tag{6}
\]

For direct auditing, encode a zero coefficient by `(uv;c_1c_2c_3c_4)`,
where `uv` is the deleted mixed pair and the colors are placed on the
sorted complementary four-set.  The coefficients used to obtain (5) are

\[
\begin{array}{c|l}
A&(24;1221),(24;2121),(25;2121),(34;2121),\\
B&(05;2020),(05;2200),(15;2020),(15;2200),\\
C&(04;2200),(05;2200),(24;1221),(25;1221),\\
D&(05;2020),(15;2200),(15;2220),(24;2121),(25;2121),\\
E&(04;2020),(05;2020),(05;2200),(15;2020),(15;2220).
\end{array}                                                \tag{7}
\]

Expanding the three perfect matchings in each coefficient in (7), then
removing the apex-forced and target-transverse terms, gives (5) directly.
In rows `A`--`C` every displayed zero coefficient has one surviving
matching monomial.  Row `D` has live-term counts `(2,1,1,1,1)`, and row
`E` has `(1,1,2,1,1)`.  Thus no cancellation or genericity assumption is
being made.

## Contradiction in the five motifs

All arguments below use only that the scalar field is a domain.

* In `A`, if `ch` is nonzero, then `ah=bh=0` makes `a=b=0`; if
  `dg` is nonzero, then `df=bg=0` makes `f=b=0`.  Either possible
  nonzero summand of `P_1` therefore forces `P_2=0`.
* In `B`, a nonzero `il` makes `f=b=0`, while a nonzero `jk` makes
  `e=a=0`.  Either possible nonzero summand of `P_0` forces `P_2=0`.
* In `C`, `P_0\ne0` and `el=ek=0` force `e=0`.  Then `P_2\ne0`
  forces `af\ne0`; the equations `df=cf=0` give `c=d=0`, contrary
  to `P_1\ne0`.
* In `D`, if `be\ne0`, then `bh=bg=0` kills `P_1`.  Otherwise
  `P_2\ne0` forces `af\ne0`.  Now `ak=a\nu=0` gives `k=\nu=0`,
  and `P_0\ne0` forces `il\ne0`.  Thus `fi\ne0` while
  `\mu\nu=0`, contradicting `\mu\nu+fi=0`.
* In `E`, `P_0\ne0` says that at least one of `i,j` is nonzero;
  `fi=fj=0` therefore gives `f=0`.  Now `P_2\ne0` forces
  `be\ne0`.  Hence `bi=b\sigma=0` gives `i=\sigma=0`, and
  `P_0\ne0` forces `jk\ne0`.  This makes `ek\ne0` while
  `\rho\sigma=0`, contradicting `ek+\rho\sigma=0`.

Every orbit in (4) is therefore impossible.  We obtain the promised
boundary theorem.

**Theorem (no three mixed `K_2` components).**  Suppose the three pure
projected four-site cofactors are nonzero pure tensors and each has a
target-aligned apex.  If the mixed-cofactor graph consists of three
two-vertex components, one of each class-pair type, then the nine
complementary zero cofactors contradict the pure coefficients.  Hence this
component pattern cannot occur.

Notice that the nonvanishing of the three cofactors defining the component
edges is not used after it identifies the nine zero holes.  The
contradiction comes entirely from the three pure tensors, their apices,
and those nine zero tensors.
