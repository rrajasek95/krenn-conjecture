# Coordinate spikes leave a square-anisotropic pencil or a pure-inverse relocation kernel

## 1. Outcome

Work in the clean off-target intrinsic scalar-unit radial normal form on
\(2h\) residual sites, \(h\geq3\):

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
      +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,
 \qquad \alpha\ne0,                                      \tag{1}
\]

\[
 Q=q^{[h]}\notin D:=\operatorname {span}\{X_a,X_b,X_c\},
 \qquad r=R_{aa},\qquad G=\alpha q+r,
 \qquad G^{[h]}=\alpha^{h-1}X_a,                         \tag{2}
\]

and

\[
 R_{jk}rH=\lambda_{jk}Q,
 \qquad R_{jk}q^{[h-1]}=\delta_{jk}X_j
 \qquad(j,k\in\{b,c\}).                                \tag{3}
\]

Here

\[
 rH=G^{[h-1]}-\alpha^{h-1}q^{[h-1]},                    \tag{4}
\]

and maximum-anchor extremality has already supplied
\(\Lambda=(\lambda_{jk})\ne0\).  Assume in this note that \(\Lambda\) is
a coordinate spike.  The open-Segre branch is not reconsidered.

There is one positive descent lemma on the off-diagonal spike.

> **Theorem 1.1 (square-zero off-diagonal spike descent).**  Suppose, after
> possibly swapping \(b,c\), that
> \[
> \Lambda=\begin{pmatrix}0&\lambda\\0&0\end{pmatrix},
> \qquad\lambda\ne0.                                     \tag{5}
> \]
> For \(\beta,\gamma\in\mathbb C^*\), put
> \[
> D_{\beta,\gamma}=\beta E_{bb}+\gamma E_{cc},\qquad
> W_{\beta,\gamma}=\beta R_{bb}+\gamma R_{cc}.           \tag{6}
> \]
> Then \(D_{\beta,\gamma}\in\ker\lambda\), and the cap
> \(E_{aa}+zD_{\beta,\gamma}\) is active for every \(z\ne0\).  If
> \[
>                         W_{\beta,\gamma}^{[2]}=0,        \tag{7}
> \]
> that cap is clean for every \(z\), and the certified active-clean-pair
> theorem gives the raw order descent.

Indeed, the exact clean error is

\[
 \mathcal E(E_{aa}+zD_{\beta,\gamma})
   =\sum_{m=2}^h z^m
      W_{\beta,\gamma}^{[m]}G^{[h-m]}.                   \tag{8}
\]

In characteristic zero, (7) says \(W_{\beta,\gamma}^2=0\), so every
higher divided power in (8) is zero.  No matching power or carrier has
been cancelled.

The literal complementary Plücker rectangle makes the surviving boundary
particularly explicit:

\[
 R_{bb}R_{cc}=R_{bc}R_{cb},                               \tag{9}
\]

and hence

\[
 \boxed{
 W_{\beta,\gamma}^{[2]}
   =\beta^2R_{bb}^{[2]}
      +\beta\gamma R_{bc}R_{cb}
      +\gamma^2R_{cc}^{[2]}.}                             \tag{10}
\]

Consequently, on a no-descent off-diagonal spike branch,

\[
 \boxed{
 \beta^2R_{bb}^{[2]}+\beta\gamma R_{bc}R_{cb}
      +\gamma^2R_{cc}^{[2]}\ne0
      \quad\text{for every }\beta\gamma\ne0.}           \tag{11}
\]

Thus the off-diagonal spike is reduced to a literal **square-anisotropic
binary pencil**.  This is stronger than merely saying that its active
kernel matrices have rank two.

A diagonal spike behaves differently.  If, for example,
\(\Lambda=\lambda E_{bb}\), every stationary complementary direction has
\(K_{bb}=0\), whereas activity requires both \(K_{bb},K_{cc}\ne0\).
Every active direction therefore has nonzero first radial coefficient
\(\lambda K_{bb}Q\).  The primitive-square and pure-inverse packet remains
literal, but it does not by itself relocate the anchor.  Sections 2--4
identify the exact residual rather than claiming such a relocation.

## 2. Exact Hermite endpoint form of a spike

Put

\[
 \rho=\alpha^{-1}r,\qquad q_t=q+t\rho,\qquad
 F_{jk}(t)=R_{jk}q_t^{[h-1]}.                             \tag{12}
\]

Since \(q_1=\alpha^{-1}G\), equations (3)--(4) give

\[
 \boxed{
 F_{jk}(0)=\delta_{jk}X_j,\qquad
 F_{jk}(1)=\delta_{jk}X_j+\alpha^{1-h}\lambda_{jk}Q.}    \tag{13}
\]

Differentiation retains the ordered four-star square:

\[
 \boxed{
 F'_{jk}(t)=\alpha^{-1}R_{jk}r q_t^{[h-2]}
            =\alpha^{-1}R_{ja}R_{ak}q_t^{[h-2]}.}         \tag{14}
\]

The integral of (14) is exactly the endpoint jump in (13).  More
explicitly,

\[
 H=\alpha^{h-2}\int_0^1q_t^{[h-2]},dt,                  \tag{15}
\]

so (14) integrates to
\(\alpha^{1-h}R_{jk}rH=\alpha^{1-h}\lambda_{jk}Q\).

Every polynomial of degree at most \(h-1\) with fixed values at zero and
one has a unique residual multiple of \(t(t-1)\).  Therefore an
off-diagonal spike as in (5) has the exact form

\[
 \begin{aligned}
 F_{bb}(t)&=X_b+t(t-1)U_{bb}(t),\\
 F_{bc}(t)&=t\mu Q+t(t-1)U_{bc}(t),\\
 F_{cb}(t)&=t(t-1)U_{cb}(t),\\
 F_{cc}(t)&=X_c+t(t-1)U_{cc}(t),
 \end{aligned}
 \qquad \mu=\alpha^{1-h}\lambda,                        \tag{16}
\]

where \(\deg U_{jk}\le h-3\).  A diagonal spike at \(bb\) instead has

\[
 \begin{aligned}
 F_{bb}(t)&=X_b+t\mu Q+t(t-1)U_{bb}(t),\\
 F_{bc}(t)&=t(t-1)U_{bc}(t),\\
 F_{cb}(t)&=t(t-1)U_{cb}(t),\\
 F_{cc}(t)&=X_c+t(t-1)U_{cc}(t).
 \end{aligned}                                           \tag{17}
\]

Equations (16)--(17) are consequences of all four complementary rows and
the full divided-difference carrier.  They do not determine the second
normal polar in (10), or its top suspension

\[
             W_{\beta,\gamma}^{[2]}G^{[h-2]}.             \tag{18}
\]

That is the first coefficient left after the square-zero descent lemma.
The zeroth Hermite moment in (15) cannot be desuspended or multiplied into
(18) without an additional source-valid comparison.

## 3. Why the diagonal pure inverse does not yet relocate an anchor

For a diagonal spike at \(uu\), \(u\in\{b,c\}\), the selected packet is

\[
 A_{uu}=R_{ua},\qquad B_{uu}=R_{au},
 \qquad A_{uu}q^{[h-1]}=B_{uu}q^{[h-1]}=0,               \tag{19}
\]

\[
 A_{uu}B_{uu}H=\lambda_{uu}Q,\qquad
 C_{uu}=q^{[h-1]}+{\alpha\over\lambda_{uu}}R_{uu}H,
 \qquad rC_{uu}=X_a.                                     \tag{20}
\]

The pure-factor lemma gives an \(a\)-pure local component of each of
\(p_a,s_a\).  If, for example,
\((p_a)_x=c_xe_a^{(x)}\), the exact residue is

\[
 \kappa_x=s_aC_{uu}-c_x^{-1}X_a^{\widehat x},
 \qquad p_a\kappa_x=0.                                  \tag{21}
\]

There is a symmetric class in \(\ker m_{s_a}\).  Goodness makes the star
maps injective as linear maps of the colour labels; it does not make
multiplication by one global star form faithful in the site-square-zero
algebra.  Thus (21) cannot be set to zero, split into two distinct pure
sites, or used for a source rewrite without a new kernel-vanishing theorem.

This is the exact diagonal-spike obstruction.  Maximum-anchor extremality
supplies \(\lambda_{uu}\ne0\), but it does not annihilate (21).  A positive
diagonal-spike continuation must construct a source-valid relocation which
kills these multiplication-kernel classes while retaining all nine rows;
the pure inverse alone is not that construction.

## 4. Six-site coordinate-spike guards

The next two guards show that the selected primitive and pure-inverse
packets are physically consistent.  They also expose exactly where the
complementary diagonal targets enter Theorem 1.1.

Take \(h=3,\alpha=1\), sites \(0,\ldots,5\), and write \(x_i^d\) for colour
\(d\) at site \(i\).  Set

\[
 \begin{aligned}
 q={}&x_0^ax_3^b+x_1^bx_5^a+x_2^ax_4^a
       +x_3^bx_4^a+x_3^ax_5^a,\\
 p_a={}&x_0^a,\qquad s_a=x_1^a-x_2^a,
 \qquad r=p_as_a,\qquad H=q+\tfrac12r.                  \tag{22}
 \end{aligned}
\]

Put

\[
 Q=x_0^ax_1^bx_2^ax_3^bx_4^ax_5^a.                     \tag{23}
\]

Direct matching expansion gives

\[
 q^{[3]}=Q,\qquad rq^{[2]}=X_a-Q,\qquad r^{[2]}=0,
 \qquad(q+r)^{[3]}=X_a.                                 \tag{24}
\]

Thus the exceptional row, the off-target condition, and unary cleanliness
are all literal in both guards.

### 4.1 Off-diagonal spike

Choose

\[
 p_b=x_3^b,\qquad p_c=x_0^b,\qquad
 s_b=x_0^a,\qquad s_c=x_4^a.                             \tag{25}
\]

Both endpoint triples are linearly independent.  If

\[
 U=x_0^bx_1^ax_2^ax_3^ax_4^ax_5^a,\qquad
 V=x_0^bx_1^bx_2^ax_3^bx_4^ax_5^a,                      \tag{26}
\]

the complete table of physical left sides in (1) is

\[
 \begin{array}{c|ccc}
  &a&b&c\\ \hline
 a&X_a&0&0\\
 b&0&Q&0\\
 c&U-V&0&0.
 \end{array}                                             \tag{27}
\]

Hence exactly six of the nine rows hold: the failures are the unselected
\(ca\) primitive row and the two complementary diagonal targets.  The
radial packet is the genuine off-diagonal spike

\[
 \Lambda=\begin{pmatrix}0&-1\\0&0\end{pmatrix}.          \tag{28}
\]

For the selected entry \(uv=bc\), both primitive rows and the pure inverse
are exact:

\[
 R_{ba}q^{[2]}=R_{ac}q^{[2]}=0,\qquad
 R_{ba}R_{ac}H=-Q,                                      \tag{29}
\]

\[
                       r\bigl(q^{[2]}-R_{bc}H\bigr)=X_a. \tag{30}
\]

Now take the active rank-two kernel direction

\[
 D=E_{bb}+E_{cc},\qquad W=R_{bb}+R_{cc}.                 \tag{31}
\]

This guard has the especially sharp identities

\[
 WrH=0,\qquad Wq^{[2]}=Q,\qquad W^{[2]}=0.               \tag{32}
\]

The literal cap error against the desired three diagonal targets is

\[
 (q+r+zW)^{[3]}-(X_a+zX_b+zX_c)
                     =z(Q-X_b-X_c).                     \tag{33}
\]

Thus the response already satisfies the square-zero hypothesis of Theorem
1.1.  It fails to descend for one precise reason: the missing \(bb,cc\)
rows make its old response \(Q\), rather than \(X_b+X_c\).  Declaring those
targets abstractly would be illegal.  Under the actual full-nine rows the
same square-zero kernel response would instead be clean and would descend.

### 4.2 Diagonal spike

Keep (22), but choose

\[
 p_b=x_0^b,\qquad p_c=x_3^b,\qquad
 s_b=x_0^a,\qquad s_c=x_4^a.                             \tag{34}
\]

Again both stars are good.  The physical row table is

\[
 \begin{array}{c|ccc}
  &a&b&c\\ \hline
 a&X_a&0&0\\
 b&U-V&0&0\\
 c&0&Q&0.
 \end{array}                                             \tag{35}
\]

Exactly five rows hold, and

\[
 \Lambda=\begin{pmatrix}0&0\\0&-1\end{pmatrix}.         \tag{36}
\]

For the selected diagonal entry \(uv=cc\), one still has

\[
 R_{ca}q^{[2]}=R_{ac}q^{[2]}=0,\qquad
 R_{ca}R_{ac}H=-Q,\qquad
 r\bigl(q^{[2]}-R_{cc}H\bigr)=X_a.                      \tag{37}
\]

Thus exceptional cleanliness, goodness, the diagonal radial spike, both
selected primitive rows, the primitive square, and the pure inverse coexist
in the literal physical algebra.  The guard is not a full source: both
complementary diagonal rows, \(ba\), and \(cb\) fail.  Its purpose is to
show that no contradiction or anchor relocation follows from (19)--(20)
alone.

For this fixed \(q,p_a,s_a\), the checker also exhausts the sparse stratum
in which each of \(p_b,p_c,s_b,s_c\) is one of the eighteen coordinate
one-site forms and both triples remain good.  Among all genuine coordinate
radial spikes in that finite stratum, six rows is the exact maximum for an
off-diagonal spike and five is the exact maximum for a diagonal spike.
This is a support-stratum census, not a classification of aggregate complex
stars.

## 5. Exact surviving boundary

The coordinate-spike branch is now split as follows.

1. **Off-diagonal spike.**  The active stationary kernel survives.  If its
   binary diagonal response pencil meets the square-zero locus, Theorem 1.1
   gives the exact descent.  Otherwise every active member satisfies the
   square-anisotropy condition (11).  The first uncontrolled top coefficient
   is the second polar (18), with its Plücker cross term in (10).
2. **Diagonal spike.**  No active stationary kernel direction exists.
   The exact pure inverse exposes \(a\)-pure local components, but a
   source-valid anchor relocation is blocked by the multiplication-kernel
   classes (21).

The missing positive inputs are correspondingly precise:

\[
 \boxed{
 \begin{array}{l}
 \text{off diagonal: a source-valid comparison forcing a square-zero}\
 \text{member of (10), or controlling }W^{[2]}G^{[h-2]};\\[1mm]
 \text{diagonal: a full-nine relocation theorem killing (21) while}\
 \text{preserving the complementary diagonal target rows.}
 \end{array}}                                             \tag{38}
\]

The dependency-free checker
[`verify_scalar_unit_coordinate_spike_square_polar_boundary.py`](../computations/verify_scalar_unit_coordinate_spike_square_polar_boundary.py)
audits every coefficient of (22)--(37), both star ranks, both coordinate
spike matrices, all selected primitive-square and pure-inverse relations,
the Plücker rectangle, the square-zero active response and cap error, the
exact reduced support of \(q\), and the exact sparse-stratum row maxima.
It derives the Hermite derivative and endpoint--integral identities in the
formal divided-power basis uniformly for \(3\le h\le12\), specializes
\(H=q+\tfrac12r\) to the physical packet, and checks the actual endpoint
jumps in both guards.  It uses explicit runtime failures and runs unchanged
under optimized Python.

This note proves the square-zero off-diagonal descent and isolates the two
remaining coordinate-spike obstructions.  It does not eliminate the
square-anisotropic pencil, construct the diagonal relocation, produce a new
full exact source, or prove Krenn's conjecture.
