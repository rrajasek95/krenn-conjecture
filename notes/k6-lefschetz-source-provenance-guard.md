# The weighted K6 Lefschetz inverse does not preserve source-valid tangents

## 1. Outcome

The explicit middle-Lefschetz inverse for the six-site matching algebra is
useful aggregate linear algebra, but invertibility alone does not produce the
source-valid own-edge lift needed on the rootless selector chart.

More sharply, consider the rank-one complete-graph torus used in the
[selector/Jacobian guard](selector-hall-base-packing-and-block-jacobian-guard.md#6-a-fixed-source-mixed-torus-guard-with-no-own-edge-lift).
At a nonzero torus point its scalar internal edges have the form

\[
                         q_{xy}=t_xt_y,\qquad t_x\ne0.       \tag{1}
\]

On this very packet the *weighted* middle-Lefschetz map is an isomorphism.
Indeed it is diagonally equivalent to the uniform Kneser-disjointness matrix
whose inverse was audited in
[the related-work note](related-work-and-lean-artifacts.md#2-matching-algebra-lefschetz-inverse).
Nevertheless the physical block-evaluation Jacobian contains no own-edge
coordinate vector.  Thus the inverse recovers aggregate edge coefficients,
but it does not certify that the recovered coefficient comes from a variation
of the fixed source probes.

Consequently a decorated-to-aggregated comparison theorem cannot consist
only of the following two steps:

1. form four-set matching-algebra coefficients from a physical packet; and
2. apply the K6 Lefschetz inverse to isolate one edge.

It must additionally prove that the isolated edge lies in the image of the
literal site-probe Jacobian (or replace that requirement by a genuinely
source-provenant coefficient-dark argument).  The torus guard misses exactly
the three diagonal target tensors, so this first result proves that an
anchored input is essential rather than something the matching-algebra
inverse can replace.  Section 5 gives a stronger exact packet: even one
complete diagonal row, together with the invertible K6 map and separated
selectors, does not force source-validity.

There is one useful positive refinement.  The four-cycle covector obstructing
an own-edge lift lies in the eigenvalue-one summand of the K6 disjointness
matrix.  Transporting it through the inverse therefore leaves only four
four-set cuts, with the same alternating support as the selected curvature
minor.  The live comparison target is sparse; it is not a dense fifteen-case
inversion.

## 2. The weighted matching-Lefschetz map

Let

\[
 E=\binom{[6]}2,\qquad {\cal F}=\binom{[6]}4.
\]

For an edge array \(q=(q_e)_{e\in E}\), define

\[
 \begin{aligned}
 T_q:\mathbb C^E&\longrightarrow\mathbb C^{\cal F},\\
 (T_q\beta)_V&=\sum_{e\subset V}\beta_e q_{V\setminus e}.
 \end{aligned}                                               \tag{2}
\]

Here \(V\setminus e\) is an edge whenever \(e\subset V\).  Formula (2) is
the multiplication map from degree one to degree two in the apolar matching
algebra, with Lefschetz element \(L_q=\sum_e q_eY_e\).  Equivalently, it is
the polarized product of the two edge quadratics: the \(V\)-coordinate is
the sum over the six ordered choices of which edge in a two-matching carries
\(\beta\).

Let \(W_{V,e}=1_{e\subset V}\) be the uniform incidence matrix.  For a
nonzero vertex-factor point (1), put

\[
                         t_e=\prod_{x\in e}t_x,
             \qquad     t_V=\prod_{x\in V}t_x.                \tag{3}
\]

If \(e\subset V\), then

\[
                         q_{V\setminus e}=\frac{t_V}{t_e}.
\]

Therefore, with diagonal matrices indexed as indicated,

\[
                 \boxed{T_q=D_{\cal F}(t_V)\,W\,D_E(t_e^{-1}).}
                                                                    \tag{4}
\]

The audited uniform inverse gives immediately

\[
                 T_q^{-1}=D_E(t_e)\,W^{-1}\,D_{\cal F}(t_V^{-1}).
                                                                    \tag{5}
\]

In particular \(T_q\) is invertible at every nonzero vertex-factor point;
no genericity or hafnian nonvanishing is needed.

## 3. The physical tangent remains only six-dimensional

Realize (1) by fixed rank-one physical blocks

\[
                         Q_{xy}=\ell_x\otimes\ell_y
\]

and probes \(u_x\) satisfying \(\ell_x(u_x)=t_x\).  If

\[
                         \eta_x=\frac{\ell_x(\xi_x)}{t_x},
\]

then the edge part of the literal probe differential is

\[
 \begin{aligned}
 J_t:\mathbb C^6&\longrightarrow\mathbb C^E,\\
 (J_t\eta)_{xy}&=t_xt_y(\eta_x+\eta_y).
 \end{aligned}                                               \tag{6}
\]

Fix an edge \(e=xy\) and choose distinct \(z,w\notin e\).  Define an edge
covector supported on the four-cycle \(xy,zw,xz,yw\) by

\[
 \lambda_{xy}=\frac1{t_xt_y},\qquad
 \lambda_{zw}=\frac1{t_zt_w},\qquad
 \lambda_{xz}=-\frac1{t_xt_z},\qquad
 \lambda_{yw}=-\frac1{t_yt_w}.                              \tag{7}
\]

For every \(\eta\), equations (6)--(7) give

\[
 \begin{aligned}
 \lambda(J_t\eta)
   &=(\eta_x+\eta_y)+(\eta_z+\eta_w)
       -(\eta_x+\eta_z)-(\eta_y+\eta_w)=0.                  \tag{8}
 \end{aligned}
\]

But \(\lambda(\mathbf e_{xy})=1/(t_xt_y)\ne0\).  Hence

\[
                         \boxed{\mathbf e_e\notin\operatorname{im}J_t}
                         \qquad(e\in E).                     \tag{9}
\]

Combining (5) and (9) displays the exact provenance failure.  The aggregate
four-set vector \(T_q\mathbf e_e\) has the unique matching-algebra preimage
\(\mathbf e_e\), but that preimage is not a physical tangent of the fixed
rank-one source.  Applying an invertible aggregate comparison cannot create
the missing source lift.

## 4. The inverse transports a four-cycle to four cuts

Let \(c\in\mathbb C^E\) be the unweighted four-cycle vector

\[
                 c_{xy}=c_{zw}=1,\qquad
                 c_{xz}=c_{yw}=-1,                            \tag{10}
\]

with every other coordinate zero.  Its signed sum at every vertex is zero.
If rows of \(W\) are indexed by complementary edges, direct inspection gives

\[
                              Wc=c.                            \tag{11}
\]

For example, the only supported edge disjoint from \(xy\) is \(zw\), with
the same coefficient.  An unsupported edge sees either no supported
disjoint edge or two coefficients with opposite signs.  Thus \(c\) lies in
the nine-dimensional eigenvalue-one summand of the Kneser disjointness
matrix, and \(W^{-1}c=c\).

Write the weighted edge covector (7) as

\[
                         \lambda^{\mathsf T}
                           =c^{\mathsf T}D_E(t_e^{-1}).
\]

Transporting it to the four-set side with (5) gives

\[
 \begin{aligned}
 \mu^{\mathsf T}
   &=\lambda^{\mathsf T}T_q^{-1}\\
   &=c^{\mathsf T}W^{-1}D_{\cal F}(t_V^{-1})
     =c^{\mathsf T}D_{\cal F}(t_V^{-1}).                     \tag{12}
 \end{aligned}
\]

In complementary-edge indexing, therefore,

\[
                         \boxed{\mu_V=\frac{c_{V^c}}{t_V}.}   \tag{13}
\]

Only four four-set cuts occur.  Equations (8) and (12) imply

\[
                         \mu^{\mathsf T}T_qJ_t=0,             \tag{14}
\]

whereas

\[
                   \mu^{\mathsf T}T_q\mathbf e_e
                     =\lambda_e=\frac{c_e}{t_e}              \tag{15}
\]

on a supported cycle edge.  Hence the prospective diagonal-anchor
comparison does not need a fifteen-case inversion.  The inverse reduces any
candidate source comparison to the four literal cuts in (13).  A positive
proof would still have to construct a grade-preserving physical four-cut
packet whose alternating contribution is nonzero; a diagonal anchor alone
does not do this, as Proposition 5.1 shows.

The relation to curvature is exact at first order.  For an edge array \(a\)
on the four displayed vertices, put

\[
                  \kappa(a)=a_{xy}a_{zw}-a_{xz}a_{yw}.         \tag{16}
\]

The vertex-factor point \(q_e=t_e\) has \(\kappa(q)=0\), and for every edge
variation \(\beta\),

\[
 \begin{aligned}
 d\kappa_q(\beta)
   &=t_zt_w\beta_{xy}+t_xt_y\beta_{zw}
       -t_yt_w\beta_{xz}-t_xt_z\beta_{yw}\\
   &=t_{\{x,y,z,w\}}\,\lambda(\beta).                         \tag{17}
 \end{aligned}
\]

Combining (12) and (17) gives the sparse comparison identity

\[
       \boxed{\quad
       \mu^{\mathsf T}T_q\beta
          =\frac{d\kappa_q(\beta)}{t_{\{x,y,z,w\}}}.
       \quad}                                                  \tag{18}
\]

Thus the four-cycle covector is precisely the normal derivative of the
four-site rank-one/flat locus.  The physical probe variations (6) are
tangent to that locus, explaining (14), while an own-edge direction is
detected by its curvature derivative.

The selected source curvature has the same literal form

\[
                         A_{pq}A_{rs}-A_{pr}A_{qs}\ne0.         \tag{19}
\]

Equation (18) is not yet an identification of that *finite bilinear
coefficient* with the linearized scalar packet on which \(T_q\) acts.
It does show exactly what a successful full-nine comparison must preserve:
the normal curvature class.  It also isolates a four-cut comparison lemma,
rather than a dense K6 inverse, as the natural place to prove preservation.

## 5. One complete diagonal row is still insufficient

The unanchored torus above can be sharpened without losing its dense K6
geometry.  Work in the six-site square-zero algebra, put

\[
 \omega=(1,1,0,0,0,0),\qquad
 w_x=e_{\omega_x}^{(x)},\qquad c_x=e_0^{(x)},
\]

and set

\[
                         q=\sum_{x<y}w_xw_y.                   \tag{20}
\]

In the physical-label space with basis
\(\epsilon_0,\epsilon_1,\epsilon_2\), define

\[
\begin{array}{lll}
 u_0=\epsilon_1,&u_1=\epsilon_2,&
 u_2=\frac12(\epsilon_0-\epsilon_1-\epsilon_2),\\
 v_3=\epsilon_1,&v_4=\epsilon_2,&
 v_5=\epsilon_0-\epsilon_1-\epsilon_2.
\end{array}                                                   \tag{21}
\]

Thus

\[
 U=u_0+u_1+u_2=\frac12(\epsilon_0+\epsilon_1+\epsilon_2),
 \qquad V=v_3+v_4+v_5=\epsilon_0.                             \tag{22}
\]

Put \(B_0=U-u_0\), \(B_1=U-u_1\), and use the endpoint convention
\((ps^{\mathsf T})_{ij}=p_is_j\).  Define the vector-valued stars by

\[
\begin{array}{c|cc}
x&p|_x&s|_x\\ \hline
0&u_0w_0+B_0c_0&-Vc_0\\
1&u_1w_1-\frac13B_1c_1&\frac13Vc_1\\
2&u_2w_2&0\\
3,4,5&0&v_xw_x .
\end{array}                                                   \tag{23}
\]

Finally take

\[
                         a=-\frac15UV^{\mathsf T}.             \tag{24}
\]

Its only nonzero column is column zero, with
\(a_{00}=a_{10}=a_{20}=-1/10\).

**Proposition 5.1 (dense one-anchor guard).**  The complete tensor identity

\[
                  \boxed{\quad
                  a q^{[3]}+ps^{\mathsf T}q^{[2]}=E_{00}X_0
                  \quad}                                      \tag{25}
\]

holds.  Hence all six off-diagonal rows and the entire \(00\) diagonal row,
including every literal coefficient cut of that row, are exact.  The only
missing full-nine equations are the \(11\) and \(22\) diagonal rows.

**Proof.**  The complete rank-one quadratic (20) has

\[
                         q^{[3]}=15X_\omega.                   \tag{26}
\]

Using only the baseline \(w_x\)-parts of (23), the response is
\(3UV^{\mathsf T}X_\omega\): after choosing the \(p\)-site and \(s\)-site,
the remaining four vertices have three perfect matchings.  This cancels
\(15aX_\omega\).

There are only three further word types.  Replacing site zero alone gives

\[
                 3\bigl(B_0V^{\mathsf T}
                       -(U-u_0)V^{\mathsf T}\bigr)=0,
\]

and replacing site one alone gives

\[
                 3\bigl(-B_1V^{\mathsf T}/3
                       +(U-u_1)V^{\mathsf T}/3\bigr)=0.
\]

Replacing both sites gives the all-zero word and coefficient

\[
 \begin{aligned}
 3\bigl(B_0(V/3)^{\mathsf T}
      +(-B_1/3)(-V)^{\mathsf T}\bigr)
   &=(B_0+B_1)V^{\mathsf T}\\
   &=E_{00},
 \end{aligned}                                               \tag{27}
\]

because \(B_0+B_1=\epsilon_0\).  No other word occurs, proving (25).
\(\square\)

At the mixed probe \(\omega\), the two separated selector matrices have
rows

\[
 {\cal P}=\begin{pmatrix}u_0^{\mathsf T}\\u_1^{\mathsf T}\\u_2^{\mathsf T}
             \end{pmatrix},
 \qquad
 {\cal S}=\begin{pmatrix}v_3^{\mathsf T}\\v_4^{\mathsf T}\\v_5^{\mathsf T}
             \end{pmatrix},
\]

with

\[
                         \det{\cal P}=\frac12,\qquad
                         \det{\cal S}=1.                       \tag{28}
\]

The opposite-shore rows vanish at that probe.  Moreover \(Q_{xy}=1\),
so \(T_Q=W\), \(|\det W|=1458\), and the full aggregate inverse is
available (the complementary-edge ordering in the checker has determinant
\(-1458\)).  With \(\alpha=a_{10}=-1/10\),

\[
 K_*=\operatorname{tr}(a)E_{10}-\alpha I
       =\frac1{10}(I-E_{10}),
\]

and an exact permanent calculation gives

\[
                  \operatorname{per}({\cal P}K_*{\cal S}^{\mathsf T})
                            =\frac7{2000}\ne0.                 \tag{29}
\]

Nevertheless \(dQ_{xy}=\eta_x+\eta_y\) and all three target differentials
vanish at \(\omega\), so the four-cycle covector (7) excludes every
source-valid own-edge tangent.  The literal anchor does not become a
coordinate anchor in selector normalization:

\[
             {\cal P}^{-\mathsf T}\epsilon_0=(1,1,2)^{\mathsf T},
 \qquad      {\cal S}^{-\mathsf T}\epsilon_0=(1,1,1)^{\mathsf T}. \tag{30}
\]

Thus (25) is simultaneously a one-anchor, separated-Hall,
invertible-Lefschetz packet and an exact own-edge no-go.

It also explains why the sparse transport in Section 4 is not yet the
curvature bridge.  For the *bare uniform aggregate padding*
\(C_V(X_0)=X_0\) at \(Q=1\), the four-cycle has coefficient sum
\(1+1-1-1=0\), so that padded anchor is invisible to the alternating
functional.  This is not a statement about an as-yet undefined decorated
overlap map.  At a weighted vertex-factor point, (13) has the four factors
\(t_V^{-1}\); cancellation or noncancellation then depends on the literal
physical cut map, and a bare diagonal row supplies no canonical weighted
normalization.

More fundamentally, the selected quantity
\(A_{pq}A_{rs}-A_{pr}A_{qs}\) mixes direct, endpoint-star, and internal
grades across two physical charts, whereas the K6 cycle in (10) uses four
internal residual-edge slots in one chart.  The Bianchi overlap has the same
alternating pattern, but identifying the two requires a source-faithful,
grade-preserving overlap map before multiplication by the common power.

## 6. Exact scope

The fixed-source torus packet in the cited selector/Jacobian guard has
injective fixed-label endpoint selectors, a nonzero Hall response, all six
off-diagonal tensor rows, and every target-zero scalar row.  Its independent
audit verifies (6)--(9).  It is not a full-nine source: its defect is exactly

\[
                         0=X_0,\qquad0=X_1,\qquad0=X_2.       \tag{31}
\]

The present calculation adds the maximal-rank, invertible aggregate K6
Lefschetz hypothesis to that packet and the guard still survives.  Therefore
the explicit K6 inverse is not, by itself, the missing own-edge theorem.
Proposition 5.1 adds one of these rows and the guard still survives.  A
narrower candidate mechanism is:

> transport two differently labelled diagonal anchors and a crossed
> four-index target-zero row such as \((r,r;s,s)\) through a
> source-faithful two-chart overlap which preserves the weighted
> complementary-four-set normalization in (13) and the
> direct/star/internal grades of the curvature class (19).

Two anchors by themselves still leave the audited relative diagonal gauge;
the crossed zero row is itself invariant under that torus unless it enters
through an overlap map injective on the residual character.  This candidate
is not proved sufficient or minimal.  Neither the old unanchored torus nor
Proposition 5.1 guards the combined two-anchor, crossed-row, faithful-overlap
hypothesis.

The dependency-free checker
[verify_k6_matching_lefschetz_inverse.py](../computations/verify_k6_matching_lefschetz_inverse.py)
verifies the uniform inverse, the weighted diagonal equivalence (4)--(5),
the eigenvector identity (11), the transported covector (12)--(13), and a
four-cycle certificate (7)--(9) for every edge at one exact nonzero rational
torus point.

The separate lightweight checker
[verify_k6_one_anchor_lefschetz_guard.py](../computations/verify_k6_one_anchor_lefschetz_guard.py)
enumerates all \(9\cdot3^6\) coefficients of (25), checks (28)--(30), and
verifies the four-cycle obstruction for every requested edge.
