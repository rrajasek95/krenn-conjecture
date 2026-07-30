# Two full inactive root rows and injective stars do not couple the curved charts

## 1. Outcome

At \(N=8\), the following proposed two-chart lemma is false:

> two overlapping coordinate caps with nonzero physical curvature cannot
> both be clean and inactive if their complete six-site target rows hold
> and both deleted endpoint-star maps are injective.

There is a rational aggregate packet with two overlapping pairs \(pq\)
and \(pr\) such that:

1. the complete \(E_{00}\)-contraction at each pair is its exact unary
   target tensor, including every transverse zero row;
2. both coordinate caps are clean, so both inactive roots export genuine
   exact unary effective quadratics;
3. all four deleted endpoint-star maps at \(pq\) and \(pr\) have rank
   three;
4. the same source cells have
   \[
       A_{pq}(0,0)A_{rs}(0,0)
       -A_{pr}(0,0)A_{qs}(0,0)=1;                       \tag{1}
   \]
5. the two four-cut charts share their literal \((L,M)\) packet and obey
   the clean and physical target equations.

This is not an exact ternary source.  It deliberately fails the other
pair-covector target rows.  It therefore isolates the missing hypothesis:
full transverse coefficients at the two inactive roots, even together
with good-star injectivity and the physical curvature square, do not
couple the endpoint colours which are invisible to those roots.  A
positive two-chart theorem must use at least one additional independent
covector row on each canonical line, or an equivalent propagation from
the unused endpoint colours into the root packet.

## 2. The seven selected cells

Use sites

\[
                   (p,q,r,s,u,v,w,x)=(0,1,2,3,4,5,6,7)
\]

and colours \(0,1,2\).  Put the following \((0,0)\)-cells in the aggregate
blocks:

\[
\begin{array}{c|ccccccc}
\text{pair}&pq&pr&rs&uv&wx&qu&sv\\ \hline
\text{weight}&1&1&1&1&\frac12&1&1.
\end{array}                                                   \tag{2}
\]

Thus the physical support of these cells is the six-cycle

\[
                 p-q-u-v-s-r-p
\]

together with the disjoint edge \(wx\).  Its two perfect matchings are

\[
                 pq\mid rs\mid uv\mid wx,
 \qquad          pr\mid qu\mid sv\mid wx,                     \tag{3}
\]

and each has weight \(1/2\).

Add only the following four rank-padding cells:

\[
\begin{aligned}
 A_{ps}(1,1)=A_{ps}(2,2)&=1,\\
 A_{qr}(1,1)=A_{qr}(2,2)&=1.                                  \tag{4}
\end{aligned}
\]

All undisplayed aggregate entries are zero.  The padding in (4) is
invisible to an \(E_{00}\)-contraction at either \(pq\) or \(pr\): at
\(pq\) it has the wrong \(p\)- or \(q\)-endpoint colour, and at \(pr\)
it has the wrong \(p\)- or \(r\)-endpoint colour.

## 3. Both complete coordinate-root rows are exact

First contract \(p,q\) in colours \(0,0\).  On the six residual sites
\(\{r,s,u,v,w,x\}\), let \(q_{pq}\) be the internal quadratic.  Its
nonzero cells are

\[
                         rs,\ sv,\ uv,\ wx                    \tag{5}
\]

with the weights inherited from (2).  The direct-edge contribution has
the unique matching

\[
                         rs\mid uv\mid wx
\]

of weight \(1/2\).  The two selected endpoint stars are the single cells
\(pr\) and \(qu\); their product is the effective residual cell \(ru\).
Its complement has the unique matching

\[
                         sv\mid wx
\]

of weight \(1/2\).  Consequently the complete pair row is

\[
 A_{pq}(0,0)q_{pq}^{[3]}
 +(p_0q_0)q_{pq}^{[2]}
 =\frac12X_0+\frac12X_0=X_0.                            \tag{6}
\]

No other residual colour word occurs, because every cell visible to this
contraction is a \((0,0)\)-cell.

The \(pr\)-chart is symmetric.  Its internal cells are

\[
                         qu,\ sv,\ uv,\ wx,                    \tag{7}
\]

the direct contribution is \(qu\mid sv\mid wx\), and the product of the
selected endpoint stars \(pq\) and \(rs\) is the residual cell \(qs\).
The complementary matching is \(uv\mid wx\).  Hence

\[
 A_{pr}(0,0)q_{pr}^{[3]}
 +(p_0r_0)q_{pr}^{[2]}=X_0.                              \tag{8}
\]

Equations (6)--(8) are tensor equalities on all \(3^6\) residual words,
not selected scalar coefficients.

## 4. Both inactive roots are genuinely clean

At \(N=8\), after using the exact physical pair row, the clean error has
the useful form

\[
 {\cal E}(K)=s(K)q\,r(K)^{[2]}+r(K)^{[3]}.                \tag{9}
\]

For \(K=E_{00}\) in the \(pq\)-chart, \(s=1\) and \(r=p_0q_0\) is the
single residual cell \(ru\).  Thus \(r^{[2]}=0\), and (9) gives
\({\cal E}_{pq}(E_{00})=0\).  Equivalently, the effective quadratic

\[
                         y_{pq}=q_{pq}+ru
\]

has exactly the two matchings displayed in Section 3 and satisfies

\[
                         y_{pq}^{[3]}=X_0.                     \tag{10}
\]

Likewise \(r=p_0r_0\) is the single residual cell \(qs\) in the \(pr\)
chart, so

\[
                         y_{pr}=q_{pr}+qs,\qquad
                         y_{pr}^{[3]}=X_0.                     \tag{11}
\]

Both clean points are inactive because \(E_{00}\) retains only target
colour zero.  Thus these are actual lower-colour exports, not the
zero-data root of the old curved guard.

## 5. The four good-star maps

After deleting \(q\), the three rows of the \(p\)-star have the distinct
output coordinates

\[
                         (r,0),\ (s,1),\ (s,2),                \tag{12}
\]

coming respectively from \(pr\) and the two padding cells on \(ps\).
After deleting \(r\), the same star has coordinates

\[
                         (q,0),\ (s,1),\ (s,2).                \tag{13}
\]

The \(q\)-star after deleting \(p\) has coordinates

\[
                         (u,0),\ (r,1),\ (r,2),                \tag{14}
\]

and the \(r\)-star after deleting \(p\) has

\[
                         (s,0),\ (q,1),\ (q,2).                \tag{15}
\]

Each displayed triple is linearly independent in the direct sum of the
remaining local spaces.  Hence both endpoint-star maps at both pairs have
rank three.  Notice exactly why this gives no contradiction: the rank-two
padding uses endpoint colours \(1,2\), while both inactive root
contractions see endpoint colour \(0\) only.

## 6. Curvature and the shared four-cut packet

Cut at \(p,q,r,s\), all in colour zero.  In the standard notation,

\[
 (A,B,C,E,F,U)=(1,1,0,0,0,1),\qquad AU-BF=1.             \tag{16}
\]

On \(D=\{u,v,w,x\}\), put

\[
                         z=uv+\frac12wx.                       \tag{17}
\]

The selected star rows are

\[
                         x=t=0,\qquad y=e_u,\qquad v=e_v.
\]

Therefore the two effective interiors and their shared rows are

\[
\begin{aligned}
 f&=z,& g&=z,\\
 L&=e_u,& H&=N=e_v,\\
 M&=AU+BF+EC=1.                                          \tag{18}
\end{aligned}
\]

Since

\[
 z^{[2]}=\frac12X_0^D,\qquad e_ue_vz=\frac12X_0^D,
\]

both nonlinear clean rows are the full pure target row:

\[
 Mf^{[2]}+LHf=X_0^D,\qquad
 Mg^{[2]}+LNg=X_0^D.                                    \tag{19}
\]

The complete physical four-cut row holds as well, because it is simply
the coefficient form of the already proved tensor equalities (6) and
(8).  Thus the guard survives the literal shared \((L,M)\), the nonzero
curvature coordinate, and the complete root target rows simultaneously.

## 7. Exact scope of the obstruction

This packet does not prescribe the \(E_{11}\), \(E_{22}\), or
off-diagonal pair contractions.  Indeed those are where (4) was placed,
and they do not form the missing ternary target system.  Therefore the
construction is not a Krenn counterexample and does not show that a whole
canonical line can have only inactive clean roots.

It does prove a sharp routing statement.  Neither of the following can
close the all-inactive branch:

* applying every transverse coefficient row only at the two known
  coordinate roots; or
* adding aggregate good-star injectivity to those two root tensors.

The next sufficient-looking input is one additional independent covector
row on each line.  For a diagonal line this can be the binary boundary
\(E_{00}-I\), or the scalar-zero row when those points differ.  Such a row
forces the padding colours in (4) to enter the same physical response
packet.  Equivalently, a positive proof may show directly that a
lower-colour root packet and the complementary scalar-zero packet cannot
both satisfy their six-site equations on the two charts with
\(AU-BF\ne0\).  The present guard identifies that complementary-row
coupling, rather than more Bianchi algebra or rank counting, as the
missing hypothesis.
