# Pure full-nine rows do not kill the cubic rank-two hafnian residue

## 1. Outcome

Work on six residual sites \(W\) with the physical full-nine equations

\[
 d_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2.                                  \tag{1}
\]

Fix an off-diagonal cell \((a,b)\), put

\[
 \alpha=d_{ab},\qquad R=p_as_b,
\]

and fix a physical colour \(c\). The exact rank-two hafnian update on
the pure \(c^6\)-slice is

\[
\boxed{
 \operatorname {haf}(\alpha Q+uv^{\mathsf T}+vu^{\mathsf T})
 =\sum_{k=0}^3\alpha^{3-k}k!
   \sum_{\substack{|I|=|J|=k\\I\cap J=\varnothing}}
     u_Iv_J\operatorname {haf}Q[W\setminus(I\cup J)].} \tag{2}
\]

Here \(Q\) is the pure-\(c\) scalarization of \(q\), \(u,v\) are the
pure-\(c\) scalarizations of \(p_a,s_b\), and
\(u_I=\prod_{x\in I}u_x\), \(v_J=\prod_{x\in J}v_x\). The diagonal of
the displayed rank-two matrix is irrelevant to the hafnian and is killed
in the site-square-zero algebra.

The off-diagonal top row kills exactly the \(k=0,1\) terms. If

\[
 C(Q)_{xy}=\begin{cases}
 \operatorname {haf}Q[W\setminus\{x,y\}],&x\ne y,\\
 0,&x=y,
 \end{cases}                                             \tag{3}
\]

then it says

\[
                  \alpha\operatorname {haf}(Q)+u^{\mathsf T}C(Q)v=0,
                                                               \tag{4}
\]

and hence

\[
\boxed{
 \chi_c
 =2\alpha\!\!\sum_{\substack{|I|=|J|=2\\I\cap J=\varnothing}}
     u_Iv_JQ_{W\setminus(I\cup J)}
   +6\sum_{|I|=3}u_Iv_{W\setminus I}.}                  \tag{5}
\]

In the first sum, \(Q_{W\setminus(I\cup J)}\) means the unique
\(Q_{xy}\) on the two-element complement. Formula (5) is exactly

\[
 [X_c](\alpha R^{[2]}q+R^{[3]})
       =[X_c](\alpha q+R)^{[3]}.                         \tag{6}
\]

The pure coefficients of all nine rows, literal shared-star/Segre
factorization, and good-star injectivity do **not** force (5) to vanish.
Section 4 gives an integral packet satisfying all 27 constant-colour
coefficients of (1), with an invertible direct block and rank-three star
triples even on each pure scalarization, for which

\[
                             \boxed{\chi_2=-28.}          \tag{7}
\]

The \(22\) anchor is not hidden in the direct term: \(d_{22}=0\), and its
response coefficient is exactly one.

The first missing object is the four-hole, two-site-cofactor compound

\[
 (K_Q)_{I,J}
   =\mathbf1_{I\cap J=\varnothing}\,
      Q_{W\setminus(I\cup J)},\qquad |I|=|J|=2.          \tag{8}
\]

The nine pure rows constrain only the first-cohafnian sandwich
\(P^{\mathsf T}C(Q)S\). They do not constrain
\((u^{\{2\}})^{\mathsf T}K_Qv^{\{2\}}\), the first term of (5), or its
required cancellation with the complete three-star term. The physical
Hamming-one second polars are the first all-word rows which retain this
lower \(q^{[1]}\)-cofactor level, although an additional source-valid
contraction is still needed to identify their entries with the selected
contraction in (8). The packet below deliberately fails even that first
omitted all-word layer: in the selected \(01\)-row, the one-defect word
\(022222\) has coefficient \(-1\). Thus this is a pure-word
counterpacket, not a complete all-word source and not a counterexample to
Krenn's conjecture.

## 2. Proof of the rank-two update

Represent the pure-\(c\) quadratic as

\[
                         q_c=\sum_{x<y}Q_{xy}z_xz_y.
\]

The pure-\(c\) part of \(R=p_as_b\) has off-diagonal matrix

\[
                         B_{xy}=u_xv_y+v_xu_y.           \tag{9}
\]

In a perfect matching contributing to
\(\operatorname {haf}(\alpha Q+B)\), suppose exactly \(k\) edges are
taken from \(B\). Expand each such edge into one of its two orientations.
The endpoints receiving the \(u\)-factors form a \(k\)-set \(I\), the
endpoints receiving the \(v\)-factors form a disjoint \(k\)-set \(J\),
and the oriented update edges are a bijection \(I\to J\). There are
\(k!\) such bijections. The remaining \(6-2k\) vertices are matched by
\(Q\), contributing
\(\alpha^{3-k}\operatorname {haf}Q[W\setminus(I\cup J)]\).
This partitions every expanded matching term uniquely and proves (2).

The \(k=0\) term is
\(\alpha^3\operatorname {haf}Q\). The \(k=1\) term is

\[
 \alpha^2\sum_{x\ne y}u_xv_y
   \operatorname {haf}Q[W\setminus\{x,y\}]
 =\alpha^2u^{\mathsf T}C(Q)v.                           \tag{10}
\]

Equation (4), multiplied by \(\alpha^2\), cancels these two terms. For
\(k=2\), the complementary hafnian is the single remaining \(Q\)-edge;
for \(k=3\), it is the empty hafnian \(1\). These are precisely the two
terms in (5).

Equivalently, if \(J_3\) is the complement-incidence matrix on
three-subsets and \(u^{\{k\}}=(u_I)_{|I|=k}\), then

\[
 \chi_c=2\alpha (u^{\{2\}})^{\mathsf T}K_Qv^{\{2\}}
          +6(u^{\{3\}})^{\mathsf T}J_3v^{\{3\}}.       \tag{11}
\]

This is the divided-power form of the second and third polars of the
six-by-six hafnian in the rank-two direction
\(uv^{\mathsf T}+vu^{\mathsf T}\).

## 3. What all nine pure rows actually know

For one physical colour \(c\), let
\(P,S\in\operatorname {Mat}_{6\times3}\) have columns equal to the
pure-\(c\) scalarizations of \(p_i,s_j\), and put
\(H=\operatorname {haf}Q\). Taking the \(X_c\)-coefficient in all nine
rows of (1) gives the single matrix identity

\[
                         \boxed{P^{\mathsf T}C(Q)S=E_{cc}-Hd.} \tag{12}
\]

In particular, the \(cc\) diagonal anchor says only

\[
             p_c^{\mathsf T}C(Q)s_c=1-Hd_{cc}.          \tag{13}
\]

It is another entry of the same first-cohafnian pairing. It contains no
entry of \(K_Q\).

Shared-star factorization gives the literal identities

\[
       (p_is_j)(p_ks_\ell)=(p_is_\ell)(p_ks_j),          \tag{14}
\]

but (14) assigns no value to their contraction against the lower
cofactor \(q\). Multiplying a top-degree six-site identity by another
positive-degree form gives zero and cannot recover that contraction.
Goodness says that the two triples of linear forms are independent. It
supplies no injectivity statement for the square-free second-Veronese
contraction in (8). Thus the first new label-polarized datum is, for
example,

\[
 \Lambda^{(c)}_{ik;j\ell}
       =[X_c](p_is_j)(p_ks_\ell)q,                      \tag{15}
\]

whose repeated selected entry gives
\([X_c]R^{[2]}q=\tfrac12\Lambda^{(c)}_{aa;bb}\). A
source-valid continuation must control (15), for example by transporting
the Hamming-one second-polar data to this four-hole contraction, and prove
the specific cancellation

\[
 2\alpha (u^{\{2\}})^{\mathsf T}K_Qv^{\{2\}}
       =-6(u^{\{3\}})^{\mathsf T}J_3v^{\{3\}}.          \tag{16}
\]

No pure top row, including (13), supplies (16).

## 4. An exact integral pure-word counterpacket

Let the sites be \(0,\ldots,5\), let \(z_x^r\) denote colour \(r\) at
site \(x\), and set

\[
 q=\sum_{r=0}^2
       (z_0^rz_1^r+z_2^rz_3^r+z_4^rz_5^r).             \tag{17}
\]

Take the invertible three-cycle direct block

\[
 d=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix}.    \tag{18}
\]

For every pure colour use the same first-star matrix \(U\), whose rows
are indexed by sites and columns by endpoint labels:

\[
 U=\begin{pmatrix}
 1&1&0\\
 1&0&0\\
 1&0&1\\
 1&0&0\\
 1&0&0\\
 1&0&0
 \end{pmatrix}.                                        \tag{19}
\]

Use the following second-star matrices \(S_r\):

\[
\begin{aligned}
S_0&=\begin{pmatrix}
 2&-1& 1\\0&0&-1\\0&0&0\\-1&0&0\\0&0&0\\0&0&0
\end{pmatrix},\\[1mm]
S_1&=\begin{pmatrix}
 1&-2& 1\\0&1&-1\\0&0&0\\-1&0&0\\0&0&0\\0&0&0
\end{pmatrix},\\[1mm]
S_2(t)&=\begin{pmatrix}
 1&1&0\\0&0&-1\\0&1&0\\-1&0&1\\0&t&0\\0&-3-t&0
\end{pmatrix}.
                                                               \tag{20}
\end{aligned}
\]

Define the actual shared stars by

\[
 p_i=\sum_{r,x}U_{xi}z_x^r,
 \qquad
 s_j=\sum_{r,x}(S_r)_{xj}z_x^r.                        \tag{21}
\]

For every \(r\), the pure scalar matrix of (17) is the unit matching
\(01\mid23\mid45\). Its hafnian is one and its cohafnian matrix \(C\)
is the same unit matching matrix. Since

\[
 U^{\mathsf T}Cv
       =\begin{pmatrix}
          \sum_xv_x\\v_1\\v_3
         \end{pmatrix},                                \tag{22}
\]

direct multiplication in (20) gives

\[
             \boxed{U^{\mathsf T}CS_r=E_{rr}-d
                     \quad(r=0,1,2).}                  \tag{23}
\]

The parameter \(t\) drops out of (23). Combining (17)--(23), for every
pure physical colour \(r\), gives all nine scalar equations

\[
 [X_r]\bigl(d_{ij}q^{[3]}+p_is_jq^{[2]}\bigr)
       =(d+U^{\mathsf T}CS_r)_{ij}
       =(E_{rr})_{ij}.                                  \tag{24}
\]

Thus all 27 constant-word coefficients hold. The matrices \(U,S_0,S_1\),
and \(S_2(t)\) all have column rank three. The two global star triples
are therefore good; in fact their restriction to every pure colour is
already injective. Equation (21) makes every Segre rectangle (14)
literal. For the emphasized anchor,

\[
 d_{22}=0,
 \qquad [X_2]p_2s_2q^{[2]}=(U^{\mathsf T}CS_2)_{22}=1.  \tag{25}
\]

Now take \(a=0,b=1,c=2\). Then \(\alpha=d_{01}=1\), and on the pure
colour-two slice

\[
 u=(1,1,1,1,1,1)^{\mathsf T},
 \qquad
 v(t)=(1,0,1,0,t,-3-t)^{\mathsf T}.                    \tag{26}
\]

The first-cohafnian pairing is

\[
                       u^{\mathsf T}Cv=\sum_xv_x=-1,    \tag{27}
\]

so the selected top row is \(1-1=0\) for every \(t\). Since \(u\) is
the all-ones vector, the two remaining layers in (5) reduce to elementary
symmetric polynomials on the appropriate complements:

\[
\begin{aligned}
 [X_2]R^{[2]}q&=-4t^2-12t-10,\\
 [X_2]R^{[3]}&=-12t^2-36t-18,\\
 \chi_2(t)&=-16t^2-48t-28.                             \tag{28}
\end{aligned}
\]

At \(t=0\), the three contributions to the first line from the internal
matching edges \(01,23,45\) are \(-6,-6,2\), while
\(6e_3(1,0,1,0,0,-3)=-18\). Hence

\[
                         \chi_2(0)=-10-18=-28,          \tag{29}
\]

proving the claimed nonvanishing without any case census.

Finally, (24) is not an all-word assertion. At the Hamming-one word

\[
                           (0,2,2,2,2,2),               \tag{30}
\]

the direct \(q^{[3]}\)-coefficient in the selected \(01\)-row is zero.
The only possible response completion uses the response on the physical
edge \(01\) and the two internal edges \(23,45\); its coefficient is

\[
 U_{0,0}(S_2)_{1,1}+(S_0)_{0,1}U_{1,0}
                         =1\cdot0+(-1)\cdot1=-1.        \tag{31}
\]

This explicit first-layer failure is exactly why the packet makes no
claim about the complete tensor equations.

## 5. Audit and sharp scope

The dependency-free
[checker](../computations/verify_h3_pure_nine_rank_two_hafnian_update_boundary.py)
checks (2) on the displayed packet, all 27 identities (24), the ranks,
all shared Segre rectangles in the site-square-zero algebra, the layer
values (28)--(29), and the mixed failure (31).

The exact conclusion is only

\[
 \boxed{\text{pure full-nine}+\text{shared stars}+\text{goodness}
        \not\Longrightarrow\chi_c=0.}
\]

A positive physical proof must use at least the omitted Hamming-one
second-polar/four-hole cofactor data (and then its compatibility with the
third-polar term), or another all-word/overlap identity that implies the
same cancellation. No weakening to the three diagonal pure anchors can
supply it.
