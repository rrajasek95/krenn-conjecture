# Split zero columns land in a source-provenant one-hole colon module

## 1. Outcome

Work at the first $8\to6$ boundary and keep the original physical label
order.  Write

\[
 d=A_{pq},\qquad d'=A_{pr},\qquad T=A_{qr},
\]

and suppose that the two rank-two direct blocks have common left kernel

\[
 \ker d^{\mathsf T}=\ker(d')^{\mathsf T}=\mathbb C\xi,
 \qquad \operatorname {supp}\xi=\{e,a\},
\]

but split coordinate right kernels

\[
 \ker d=\mathbb Ce_e,
 \qquad \ker d'=\mathbb Ce_b,
 \qquad \{e,a,b\}=\{0,1,2\}.                         \tag{1}
\]

Thus $d_{*e}=0$ and $d'_{*b}=0$, with different literal zero
columns.  On the five-site common complement $D$, put

\[
 Q_{jk}=y_jt_k+\frac{T_{jk}}2z,
 \qquad C_{jk}=Q_{jk}z.                                \tag{2}
\]

The complete 27-row packet has an exact, case-free output.  If

\[
 \mathcal K_x^{(4)}
   =\{H\in\mathcal A_4(D):x_iH=0\text{ for }i=0,1,2\}, \tag{3}
\]

then

\[
                         \boxed{C_{eb}\in\mathcal K_x^{(4)}.}    \tag{4}
\]

Equivalently, define the filtered one-hole colon module

\[
 \mathfrak C_x(z)=
 \frac{\{Q\in\mathcal A_2(D):x_iQz=0\ (i=0,1,2)\}}
      {\operatorname {Ann}_2(z)}.                       \tag{5}
\]

The split boundary supplies the fixed-label, source-provenant class

\[
               \boxed{\mathsf {SC}_{e\mid b}=[Q_{eb}]
                         \in\mathfrak C_x(z).}           \tag{6}
\]

Call this the **split-column one-hole class**.  It is stronger than the
left-kernel relation $LQ_{eb}z=0$, where $L=x(\xi)$, because all
three literal $p$-star rows annihilate the same quartic.  It also keeps
the ordered physical labels $q:e$ and $r:b$; swapping the two right
kernels swaps $(y,d)$ with $(t,d')$ and reverses the displayed order.

The other rows place (4) next to all three target anchors.  If

\[
 \mathcal I_x^{(5)}=\sum_i x_i\mathcal A_4(D),           \tag{7}
\]

then the full packet implies

\[
            y_ez^2, t_bz^2, X_e, X_a, X_b
                    \in\mathcal I_x^{(5)}.              \tag{8}
\]

Thus (6) is not an unlabelled annihilator manufactured after quotienting:
it is the common syzygy of two literal border strips whose adjacent rows
carry the $e$- and $b$-anchors, while the common-left-kernel packet
carries the $e$- and $a$-anchors.

This is **not a closure** of the split boundary.  The class in (6) may be
zero.  In that case $Q_{eb}\in\operatorname {Ann}_2(z)$, which is a
lower one-hole catalecticant boundary; if $Q_{eb}=0$ itself, the exact
effective cell collapses to

\[
                         y_et_b=-\frac{T_{eb}}2z.         \tag{9}
\]

Neither alternative is automatically a common zero row/column or a
physical dark cut.  Conversely, a nonzero class (6) is a genuine named
colon generator to be carried into the rootless Macaulay ledger.  The
available rows do not turn it into a degree-five Macaulay covector.

Section 4 gives a sharp rational five-site guard.  It has split zero
columns, no common zero row or column, rank-three restricted stars,
nonzero selected curvature, a generic $\{e,a\}$-compression of $T$,
both contracted packets, and 26 of the 27 scalarized rows.  Its
$\mathsf {SC}_{e\mid b}$ is nonzero.  The sole missing uncontracted row
is

\[
                         (i,j,k)=(b,e,a).                \tag{10}
\]

That row is invisible to both kernel contractions.  Hence neither
contraction, nor curvature and goodness, reconstructs it.  The guard is a
bounded negative result, not a Krenn counterexample: its top targets are
identified in a one-dimensional quotient, and row (10) fails.

## 2. The two ordered border strips

At the first $h=3$ boundary, the literal 27 rows are

\[
 (d_{ij}t_k+d'_{ik}y_j+T_{jk}x_i)z^{[2]}
       +x_iy_jt_kz=\mathbf1_{i=j=k}X_i.                 \tag{11}
\]

In (11), the displayed exponents are the $h=3$ specialization.  The
all-order formula and its exact normalization are

\[
 (d_{ij}t_k+d'_{ik}y_j+T_{jk}x_i)z^{[h-1]}
       +x_iy_jt_kz^{[h-2]}=\mathbf1_{i=j=k}X_i,          \tag{11a}
\]

\[
 Q_{jk}^{(h)}=y_jt_k+\frac{T_{jk}}{h-1}z,
 \qquad C_{jk}^{(h)}=Q_{jk}^{(h)}z^{[h-2]}.             \tag{11b}
\]

Indeed $zz^{[h-2]}=(h-1)z^{[h-1]}$.  Therefore (11a) is
equivalently

\[
 x_iC_{jk}^{(h)}+(d_{ij}t_k+d'_{ik}y_j)z^{[h-1]}
       =\mathbf1_{i=j=k}X_i.                            \tag{11c}
\]

There is no factorial on either radial term in (11c).  At $h=3$,
$Q_{jk}^{(3)}=Q_{jk}$, $C_{jk}^{(3)}=C_{jk}$, and
$z^{[2]}=z^2/2$, so (11c) becomes the division-safe form

\[
 x_iC_{jk}+\frac12(d_{ij}t_k+d'_{ik}y_j)z^2
       =\mathbf1_{i=j=k}X_i.                            \tag{12}
\]

No common factor has been cancelled.  The order of the two radial terms
is forced by the endpoint order in (11).

The same argument works at every $h\ge3$: replace $C$ below by
$C^{(h)}$ and $z^2/2$ by $z^{[h-1]}$.  In particular the
all-order split class is

\[
 C_{eb}^{(h)}\in
 \mathcal K_x^{(2h-2)}
 :=\{H\in\mathcal A_{2h-2}(D):x_iH=0\ (i=0,1,2)\},     \tag{12a}
\]

on the $(2h-1)$-site common complement.  Equivalently it is represented
by $Q_{eb}^{(h)}$ modulo
$\operatorname {Ann}_2(z^{[h-2]})$.  The remaining proof is written at
the first $h=3$ boundary.

Set $j=e$.  The literal zero column $d_{*e}=0$ gives the first border
strip

\[
 x_iC_{ek}+\frac12d'_{ik}y_ez^2
       =\mathbf1_{i=e=k}X_e.                            \tag{13}
\]

Set $k=b$.  The other zero column $d'_{*b}=0$ gives the transverse
strip

\[
 x_iC_{jb}+\frac12d_{ij}t_bz^2
       =\mathbf1_{i=j=b}X_b.                            \tag{14}
\]

Their common cell is $(j,k)=(e,b)$.  Both radial columns vanish there,
and $e\ne b$, so (13)--(14) reduce to

\[
                         x_iC_{eb}=0\qquad(i=0,1,2).     \tag{15}
\]

This proves (4)--(6) directly from three literal rows.  In particular,
the word `column' in the name of the class refers to the actual ordered
zero columns in (1), not to an abstractly conjugated kernel line.

The remaining members of the strips prove (8).  Since $d$ has rank two
and column $e$ is zero, its columns $d_a,d_b$ are independent.  The
$j=a$ member of (14) has zero target, and some entry of $d_a$ is
nonzero; hence

\[
                         t_bz^2\in\mathcal I_x^{(5)}.    \tag{16}
\]

Similarly, the two nonzero columns $d'_e,d'_a$ are independent.  The
$k=a$ member of (13) gives

\[
                         y_ez^2\in\mathcal I_x^{(5)}.    \tag{17}
\]

Now the $k=e$ member of (13) and the $j=b$ member of (14) put

\[
                         X_e,X_b\in\mathcal I_x^{(5)}.  \tag{18}
\]

Finally contract (12) by the common left kernel.  With $L=x(\xi)$,

\[
                         LC_{jk}=\delta_{jk}\xi_jX_j.   \tag{19}
\]

The $j=k=a$ anchor in (19) puts $X_a$ in the same ideal.  This proves
(8) using the full target labels and no matrix-entry case split.

There is a useful local interpretation.  Write

\[
 H_s=\operatorname {span}\{(x_0)_s,(x_1)_s,(x_2)_s\}
       \subseteq V_s.
\]

The top-degree quotient by (7) is

\[
 \mathcal A_5(D)/\mathcal I_x^{(5)}
       \simeq\bigotimes_{s\in D}(V_s/H_s).              \tag{20}
\]

Consequently (8) says that for each physical label $c$, some common
site has $e_c\in H_s$.  The three witnessing sites need not coincide,
and one blocked site per label is below the two-site physical-dark-cut
threshold.  This is why (8) is incidence data, not a dark cut.

## 3. Why goodness and curvature do not cancel the class

The two good charts make their four full endpoint-star maps injective.
For the shared $p$-star, the common kernel vector has no component at
the opposite deleted endpoint:

\[
 \xi^{\mathsf T}d=\xi^{\mathsf T}d'=0.
\]

Thus $L=x(\xi)$ is the same literal five-site form on both charts and is
nonzero.  This validates the provenance of (19), but injectivity of a
degree-one star map does not imply injectivity of

\[
 \mathcal A_4(D)\longrightarrow\mathcal A_5(D)^3,
 \qquad H\longmapsto(x_0H,x_1H,x_2H).                  \tag{21}
\]

Its kernel is exactly (3).

The selected curvature $AU-BF\ne0$ is equally compatible with (3).
Its entries use one selected nonzero column of $d$, one selected
nonzero column of $d'$, and a fourth-site coefficient.  The split class
instead uses the two *zero* columns and the ordered $qr$-cell $T_{eb}$.
There is no valid division or Bianchi substitution that identifies these
two grades.  The guard below retains both with literal endpoint order.

For a Macaulay conclusion, one would need a chain map sending (6) to one
common functional on the three quadratic shifts of the clean cubics.
Membership in (3) supplies no such map.  If (6) vanishes, the proof must
still eliminate the lower kernel $\operatorname {Ann}_2(z)$; if it does
not vanish, it must show that this particular source-provenant class
creates a rank defect after the nonvanishing Macaulay block is removed.

## 4. A sharp 26-of-27 rational guard

Let

\[
 \mathcal A=\mathbb Q[u_0,\ldots,u_4]/(u_0^2,\ldots,u_4^2),
 \qquad \Omega=u_0u_1u_2u_3u_4,
\]

and put

\[
                         z=u_1u_3+u_2u_4.                \tag{22}
\]

Use $e=0,a=1,b=2$, $\xi=(1,1,0)$, and the three star triples

\[
\begin{aligned}
 x={}&(u_1-u_2,
       u_0-u_2+u_3,
       -u_1-u_4),\\
 y={}&(-u_0-u_3,
       u_3-u_4,
       u_3),\\
 t={}&(u_2,
       -u_1-u_3,
       u_0-u_2+u_4).
                                                               \tag{23}
\end{aligned}
\]

Take

\[
 d=\begin{pmatrix}
 0&-2&-1\\0&2&1\\0&1&0
 \end{pmatrix},\qquad
 d'=\begin{pmatrix}
 1&1&0\\-1&-1&0\\1&-2&0
 \end{pmatrix},\qquad
 T=\begin{pmatrix}
 -1&-3&-1\\1&0&-4\\0&1&-1
 \end{pmatrix}.                                            \tag{24}
\]

Both direct blocks have rank two,

\[
 \xi^{\mathsf T}d=\xi^{\mathsf T}d'=0,
 \qquad de_0=0,
 \qquad d'e_2=0,                                          \tag{25}
\]

and they have neither a zero row nor another common zero column.  Each
coefficient matrix of the three triples in (23) has rank three.  Hence
the restricted stars are already injective, so the four full stars stay
injective after the cross-endpoint components are adjoined.

In the one-dimensional top quotient prescribe

\[
                         X_0=X_1=X_2=-\Omega.             \tag{26}
\]

Direct exact multiplication shows that (11) holds for 26 triples and
has the sole residual

\[
 R_{201}=\Omega.                                          \tag{27}
\]

The omitted row is precisely (10).  It is invisible to the left
contraction because $\xi_b=0$, and invisible to the right contraction
because

\[
 (e_e)_e(e_b)_a=0.
\]

Therefore both contracted packets hold exactly, including the two
nonzero left anchors and the targetless three-row split packet.

The colon generator is explicit:

\[
\begin{aligned}
 Q_{02}
   ={}&( -u_0-u_3)(u_0-u_2+u_4)
          -\frac12(u_1u_3+u_2u_4),\\
 C_{02}=Q_{02}z
   ={}&u_0u_1u_2u_3-u_0u_1u_3u_4
       -u_0u_2u_3u_4-u_1u_2u_3u_4.                     \tag{28}
\end{aligned}
\]

Thus $C_{02}\ne0$, while $x_iC_{02}=0$ for all three $i$.  In
particular $Q_{02}\notin\operatorname {Ann}_2(z)$, and the class (6)
is genuinely nonzero.

The selected curvature is also literal.  At residual site $u_2$, take

\[
 A=d_{01}=-2,\qquad B=d'_{00}=1,\qquad
 F=(y_1)_{u_2}=0,\qquad U=(t_0)_{u_2}=1.
\]

Then

\[
                         AU-BF=-2\ne0.                  \tag{29}
\]

The ordered $\{e,a\}$-compression of $T$ has crossed entries

\[
 T_{ea}=-3,\qquad T_{ae}=1,
 \qquad\det T_{\{e,a\}}=3,                              \tag{30}
\]

so this is not a triangular or singular escape.

The row missing in (27) is, in normalized notation,

\[
 x_bC_{ea}+\frac{d'_{ba}}2y_ez^2=0.                     \tag{31}
\]

It is exactly the adjacent bridge in the first border strip, and it is
not recoverable from the two kernel contractions.  The guard therefore
sets a sharp boundary for any proof which silently replaces the 27 rows
by those contractions.

This residual is **not** the split targetless carrier itself: that carrier
is the three-row cell $(j,k)=(e,b)$, and all three of those rows hold in
the guard.  Row (31) is its ordered adjacent-column analogue
$(i,j,k)=(b,e,a)$.  It couples the $q:e$ strip to the other nonzero
column $r:a$ of $d'$; its invisibility is exactly
$\xi_b=0$ and $(e_b)_a=0$, not a relabelling of the generic
noncoordinate target cross.

Two limitations are essential.  First, (27) says the guard does not
satisfy the full uncontracted packet.  Second, (26) identifies the three
pure target tensors; a physical ternary source has independent
$X_0,X_1,X_2$ with all mixed decorated words zero.  The guard is only a
rational square-free coefficient guard.  It proves compatibility of a
nonzero split-column colon class with the other listed algebraic data,
not compatibility with a Krenn source.

Finally, decorating the unrelated clean cubics by $s^3,t^3$ gives the
six shifted quintics

\[
 s^5,s^4t,s^3t^2,s^2t^3,st^4,t^5,
\]

whose Macaulay matrix has rank six.  Hence the existence of (28), by
itself, does not force a degree-five Macaulay dual.

## 5. Exact stopping point

The split-coordinate boundary has a clean, non-enumerative landing:

* the complete rows give the ordered border strips (13)--(14);
* their intersection is the split-column one-hole class (6);
* the adjacent rows place all three physical targets in the same
  $p$-star top ideal, as in (8); and
* goodness and selected curvature do not make the one-hole
  multiplication map (21) injective.

This does not force a common zero row/column or a physical dark cut.  A
successful continuation must use the uncontracted bridge (31), with the
independent target tensors still present, to do one of two things:

1. kill $\mathsf {SC}_{e\mid b}$ and then eliminate its lower
   $\operatorname {Ann}_2(z)$ boundary; or
2. map the nonzero class through all three clean-error shifts to a common
   Macaulay covector.

Repeating the targetless contraction or cancelling $z$ does neither.

The dependency-free
[checker](../computations/verify_split_coordinate_one_hole_colon_boundary.py)
audits the exact kernels and ranks, the 26-row ledger and sole residual,
both contractions, the explicit nonzero colon generator, absence of a
common zero row/column, restricted-star injectivity, the selected
curvature, the generic $T$-compression, and the full-rank formal
Macaulay decoration.
