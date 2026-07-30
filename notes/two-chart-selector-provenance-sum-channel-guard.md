# The two-chart Bianchi packet transports the selector sum class

## 1. Outcome

Fix a completed two-label square in a full-nine `pq` chart.  Write its
direct matrix as \(d\), let \(\Delta\) be the diagonal matrices, and put

\[
 \mathcal Q_d={\rm Mat}_2/(\Delta+\mathbb C d),
 \qquad
 \omega_d(X)=d_{21}X_{12}-d_{12}X_{21}.                 \tag{1}
\]

When \((d_{12},d_{21})\ne(0,0)\), \(\mathcal Q_d\) is one-dimensional
and \(\omega_d\) is its coordinate.  At one decorated residual edge let

\[
 H=R_{\bullet k}F_{\bullet l}^{\mathsf T},\qquad
 G=E_{\bullet l}T_{\bullet k}^{\mathsf T},\qquad
 B=H+G,                                                     \tag{2}
\]

where the six fixed-label physical blocks are

\[
 P=A_{pq},\ R=A_{pr},\ E=A_{ps},\ T=A_{qr},\ F=A_{qs},\ U=A_{rs},
 \qquad d=P.                                                \tag{3}
\]

Thus \(B\) is the literal edge-coefficient response table of the
direct-zero selector family.  The two oriented curvatures are

\[
 K_H=u d-H,\qquad K_G=u d-G,\qquad u=U_{kl}.                \tag{4}
\]

The exact overlap packet separates into a difference channel and a sum
channel:

\[
 K_H-K_G=-(H-G),\qquad
 K_H+K_G=2ud-B.                                             \tag{5}
\]

The Bianchi/cyclic relation controls the first channel algebraically.
Even if its crossed response is granted as a separately admitted
selector-family row, modulo \(\Delta+\mathbb C d\) the second channel is
exactly

\[
                         [K_H+K_G]=-[B].                    \tag{6}
\]

Consequently a class-zero crossed difference \(J=H-G\) says nothing
about the desired sum class.  A second orientation gives the negative of
the same difference, not the sum.

The normal and direct-double companions do not change this conclusion.
Put \(h=m-1\geq2\) for the canonical pair-cap coefficient.  Their three
fixed-label direct-double tables, all indexed back in the `pq` square,
are

\[
 \begin{aligned}
 M_0&=h(H+G)+ud,\\
 M_H&=H+hG+hud,\\
 M_G&=hH+G+hud.
 \end{aligned}                                             \tag{7}
\]

They satisfy

\[
 M_0-M_H=-(h-1)K_H,\qquad
 M_0-M_G=-(h-1)K_G.                                        \tag{8}
\]

These are not three independently admitted selector-family rows.
After the power-free connection and normal row cancel the star grades,
each difference in (8) remains paired with the internal curvature term.
With

\[
             Z_0=z^{[h-1]},\qquad Z_1=z^{[h-2]},
\]

the remaining associated-graded two-term slice is

\[
 (M_0-M_H)Z_0+K_HzZ_1=0,
 \qquad zZ_1=(h-1)Z_0,                                    \tag{9}
\]

and similarly for \(G\).  Thus the literal source-valid object is the
total zero row in (9).  Declaring \(M_0-M_H\), \(K_Hz\), or a formal
crossed matrix separately source-valid discards a filtration grade.

There is an exact integral guard on one completed two-label compression in
each of the three overlapping pair presentations `pq`, `pr`, and `ps`.
Every one of its four fixed-label crossed rows has zero \(\omega\)-class,
while three of the four decorated coefficient sums have nonzero class in
every chart.  It also makes every direct-double table in (7) at the
displayed \((\alpha,\alpha)\) coefficient nonzero in the quotient, but
(9) cancels it exactly.  Hence the actual two-chart
Bianchi/normal/direct-double packet does **not** by
itself close the selector provenance obstruction.

The missing input is now precise: one literal, grade-preserving
coefficient-cut row whose response has nonzero \(\omega_d\)-class after
all of its normal and internal components have been cancelled.  Equivalently,
one must split the sum channel (6), rather than add another cyclic
difference.

This is a static selector-family statement.  It neither supplies nor
replaces the three \(u^2,uv,v^2\) Macaulay prolongations along a physical
cap line.

## 2. Fixed-label direct-double ledger

For a canonical `pq` cap, the coefficient at residual sites `r,s` and
fixed physical labels \(k,l\) is

\[
 M_0=h\bigl(R_{\bullet k}F_{\bullet l}^{\mathsf T}
             +E_{\bullet l}T_{\bullet k}^{\mathsf T}\bigr)
       +U_{kl}P.                                             \tag{10}
\]

Present the same four-cut through the `pr` cap, while retaining \(i,j\)
as the matrix indices of the original `pq` selector.  Its coefficient is

\[
 M_H=R_{\bullet k}F_{\bullet l}^{\mathsf T}
       +hE_{\bullet l}T_{\bullet k}^{\mathsf T}
       +hU_{kl}P.                                            \tag{11}
\]

The `ps` presentation gives

\[
 M_G=hR_{\bullet k}F_{\bullet l}^{\mathsf T}
       +E_{\bullet l}T_{\bullet k}^{\mathsf T}
       +hU_{kl}P.                                            \tag{12}
\]

Equations (8) follow immediately.  They are the full-label form of the
direct-double companion

\[
 M_{pq;rs}-M_{pr;qs}=-(m-2)(AU-BF).                          \tag{13}
\]

At the preceding filtration grade the curvature equation has coefficient
one on \(K_Hz\).  Multiplication by \(Z_1=z^{[h-2]}\), together with
\(zZ_1=(h-1)Z_0\), proves (9) with no cancellation of a common power.
The power-free connection and its normal companion cancel the remaining
terms exactly as in the canonical overlap calculation.

Adding the two equations in (8) exposes the unresolved channel:

\[
 2M_0-M_H-M_G=-(h-1)(K_H+K_G).                              \tag{14}
\]

Modulo \(\Delta+\mathbb C d\), the right side is
\((h-1)[B]\).  But its internal-grade mate in (9) is the negative of the
same class.  Subtracting the equations instead produces only
\(K_H-K_G=-J\).  This proves algebraically that opposite orientation and
the shared \((L,M)\) packet transport the sum class between grades; they
do not annihilate it.

If \([J]=0\), then \([H]=[G]=[B]/2\), and in characteristic zero

\[
 [M_0]=h[B],\qquad [M_H]=[M_G]={h+1\over2}[B].              \tag{15}
\]

Thus any one of these tables would close the one-scalar obstruction if a
new argument made it an admitted row by itself.  The known packet makes
only the paired totals (9) admissible.

## 3. An integral four-label-choice triangle guard

Use the same two physical labels \(\alpha,\beta\) at all four sites and
take the endpoint-ordered block compressions

\[
 P=R=E=D:=\begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad
 T=F=U=C:=\begin{pmatrix}0&1\\1&2\end{pmatrix}.             \tag{16}
\]

Both matrices are invertible.  There is no label permutation between
charts: the first coordinate is always \(\alpha\), the second always
\(\beta\), and reverse physical blocks are the displayed transposes
(which happen to be equal).

For the `pq` chart and probes \(k,l\in\{\alpha,\beta\}\), put

\[
 H_{kl}=D_{\bullet k}C_{\bullet l}^{\mathsf T},\qquad
 G_{kl}=D_{\bullet l}C_{\bullet k}^{\mathsf T}.              \tag{17}
\]

The `pr` and `ps` charts have the same table after the literal cyclic
reindexing of the physical sites.  Direct calculation gives

\[
\begin{array}{c|c|c|c}
(k,l)&J_{kl}=H_{kl}-G_{kl}&B_{kl}=H_{kl}+G_{kl}&
          \omega_D(B_{kl})\\ \hline
(\alpha,\alpha)&0&\begin{pmatrix}0&2\\0&2\end{pmatrix}&2\\[1mm]
(\alpha,\beta)&\begin{pmatrix}1&1\\1&0\end{pmatrix}&
             \begin{pmatrix}1&3\\1&4\end{pmatrix}&2\\[1mm]
(\beta,\alpha)&-\begin{pmatrix}1&1\\1&0\end{pmatrix}&
             \begin{pmatrix}1&3\\1&4\end{pmatrix}&2\\[1mm]
(\beta,\beta)&0&\begin{pmatrix}2&4\\4&8\end{pmatrix}&0.
\end{array}                                                  \tag{18}
\]

Here

\[
 \begin{pmatrix}1&1\\1&0\end{pmatrix}
       =D+\operatorname {diag}(0,-2),                         \tag{19}
\]

so every one of the four fixed-label crossed rows belongs to
\(\Delta+\mathbb C D\).  Both diagonal anchors are already in \(\Delta\).
Changing either residual label within this two-label square, changing the
deleted pair from `pq` to `pr` or `ps`, or reversing the Bianchi orientation
therefore adds no class.  Nevertheless the first three literal
edge-coefficient sums in (18) have the unique nonzero selector-provenance
class.

At the \((\alpha,\alpha)\) coefficient, \(u=C_{\alpha\alpha}=0\),
\(H=G=\left(\begin{smallmatrix}0&1\\0&1\end{smallmatrix}\right)\),
and for the eight-site value \(h=3\),

\[
 M_0=3B=\begin{pmatrix}0&6\\0&6\end{pmatrix},\qquad
 M_H=M_G=4H=\begin{pmatrix}0&4\\0&4\end{pmatrix}.           \tag{20}
\]

Their \(\omega_D\)-values are \(6,4,4\).  Also

\[
 K_H=K_G=-H,\qquad
 M_0-M_H=2H=-2K_H.                                           \tag{21}
\]

Thus (20) does not hide a zero direct-double class.  It displays the
nonzero class which (9) cancels against the adjacent internal curvature
grade.

The blocks (16) are genuine endpoint-ordered physical block data.  After
extending the remaining blocks arbitrarily, the power-free connection,
normal, curvature, direct-double, and cyclic Bianchi identities therefore
hold polynomially with the fixed labels shown.  The selector maps can also
be made injective simultaneously in the three displayed charts without
altering (16): choose two further sites \(a,b\), give the two \(p\)-stars
distinct coordinates at \(a\), and give the two \(q\)-, \(r\)-, and
\(s\)-stars distinct coordinates at \(b\).  In each chart the four
products then contain four private monomials \(x_i y_j\).  Thus the local
guard may be taken with \(K=\ker(\Phi|_{D^\perp})=0\) in every displayed
chart; its nonzero classes are not an artefact of selector noninjectivity.

The blocks are not asserted to extend to a global exact ternary GHZ
source.  In particular, the guard does not realize the full-nine top
equations, cleanliness, goodness, or a physical Macaulay cap line.  It
uses from full nine only the consequence that the target functionals give
the diagonal subspace \(\Delta\), and then tests everything the universal
overlap packet can add at the displayed coefficient.  It is therefore not
a countermodel to the complete full-nine system; additional coupled
full-nine rows remain a possible way to kill the class.  Nor does it test
the complementary `qr`, `qs`, and `rs` selector quotients.

The guard's exact scope is the isolated implication at issue: those
universal source identities, the two diagonal anchors, even granting all
labeled crossed differences in the displayed square, and all three pair
presentations do not force
\(\omega_D(B)=0\) and do not supply a filtered row representing \(B\).

The dependency-free
[checker](../computations/verify_two_chart_selector_provenance_sum_channel_guard.py)
audits all four labeled rows in all three physical charts, the quotient
identities in (5), (6), (8), (14), and (15), and the explicit tables
(18)--(21).
