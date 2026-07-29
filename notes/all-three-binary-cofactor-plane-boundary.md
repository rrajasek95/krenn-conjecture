# All three binary faces force cofactor two-planes

## Outcome

Return to the pure color-zero limit and assume

\[
                 \operatorname{haf}C=1,
       \qquad h_{ij}:=\operatorname{haf}C[V\setminus\{i,j\}]\ne0
                                                               \tag{1}
\]

for every pair.  Impose all three complete binary faces `01`, `02`, and
`12`.  There are four exact conclusions.

1. The omitted `12` face kills the local color-cloning counterfamily from
   `cofactor-open-color-cloning-boundary.md`.  At every vertex the two
   first-jet rows must be linearly independent in the cofactor kernel.
2. Thus the cofactor-open problem has a coordinate-free **plane normal
   form**.  One chooses

   \[
       L_i\in\operatorname{Gr}(2,K_i),\qquad
       K_i=\left\{u:\sum_{j\ne i}u_jh_{ij}=0\right\},      \tag{2}
   \]

   and the complete `12` source is the restriction to `L_i x L_j` of one
   canonical cofactor pairing.  Exact `12` equality says that the resulting
   matching tensor lies in the local `GL_2^V` orbit of binary GHZ.
3. The first genuinely ternary equation is an explicit cubic Bianchi
   tensor `Theta_ikp^(rst)`.  It consists of three direct-second-lift times
   first-jet terms plus one three-first-jet permanent.  The equations with
   `r=s=t` are already binary; the six placements using both colors one and
   two are precisely the new degree-three compatibility.
4. At four sites the plane normal form is impossible: every `K_i` already
   has dimension two, and the canonical `01|23` flattening has an explicit
   nonzero `3 by 3` minor throughout the cofactor-open locus.  Binary GHZ
   has flattening rank two.  Thus the earlier four-site clone is genuinely
   only a two-face boundary; no choice of its second direction can repair
   the third face while keeping a cofactor-open leading point.

For `n=6`, this reduces the open branch to six planes in
`Gr(2,4)`, together with two complete binary-contact sections and the cubic
equations below.  No exact cofactor-open binary seed at six sites is
currently available in the repository: the Hamilton, switched, and flat
binary gadgets are all cofactor-sparse, while the known dense cofactor-open
modules solve only endpoint jets.  The standard three-factor six-site
source shows the singular boundary is sharp: all three binary faces and
all mixed cubics are exact, but twelve leading cofactors vanish and one
degree-four genuinely ternary singleton remains.  The subsequent
`uniform-dense-cyclic-plane-obstruction.md` excludes the full
cyclic-equivariant plane system at the constant cofactor-open leading point;
noncyclic planes and nonconstant leading matrices remain open.

## 1. Cofactor kernels and the four forced second blocks

Use directed notation `b_ij^r` for the cell with color
`r in {1,2}` at `i` and color zero at `j`.  For `i<k`, let
`a_ik^(rs)` be the cell with colors `r,s` at `i,k`.  Put

\[
 h_D=\operatorname{haf}C[V\setminus D],\qquad h_V=1.       \tag{3}
\]

The complete coefficients with one and two nonzero-color sites are

\[
             \sum_{j\ne i}b_{ij}^r h_{ij}=0,              \tag{4}
\]

and

\[
 a_{ik}^{rs}h_{ik}
 +\sum_{\substack{j,\ell\notin\{i,k\}\\j\ne\ell}}
       b_{ij}^r b_{k\ell}^s h_{ikj\ell}=0.                \tag{5}
\]

On (1), define the bilinear cofactor connection

\[
 Q_{ik}(u,v)=-{1\over h_{ik}}
  \sum_{\substack{j,\ell\notin\{i,k\}\\j\ne\ell}}
       u_jv_\ell h_{ikj\ell}.                             \tag{6}
\]

Equations (4)--(5) say exactly

\[
 b_i^r\in K_i,qquad
 a_{ik}^{rs}=Q_{ik}(b_i^r,b_k^s).                         \tag{7}
\]

The complete `01` and `02` faces impose, in addition, every higher binary
coefficient and the two terminal normalizations.  For the moment, only
(7) and the third binary face will be needed.

## 2. The third face excludes every common-line jet

Let `A_ik` denote the `2 by 2` block

\[
                       A_{ik}=(a_{ik}^{rs})_{r,s=1,2}.     \tag{8}
\]

The third binary-face hypothesis is

\[
                    H_V(A)=X_1+X_2.                       \tag{9}
\]

**Lemma 2.1 (two-plane necessity).**  Under (1), (4)--(5), and (9),

\[
                       \dim\operatorname{span}
                           \{b_i^1,b_i^2\}=2              \tag{10}
\]

at every vertex `i`.

**Proof.**  If (10) fails, choose a nonzero covector
`xi=(xi_1,xi_2)` with

\[
                         \xi_1b_i^1+\xi_2b_i^2=0.         \tag{11}
\]

By bilinearity of (6), contracting the color factor at `i` by `xi`
annihilates every incident block (8), in either endpoint orientation.
Every perfect-matching term contains exactly one edge incident with `i`,
so the same contraction annihilates `H_V(A)`.  Applied to the right side of
(9), however, it gives

\[
                 \xi_1 e_1^{\otimes(V\setminus i)}
                   +\xi_2 e_2^{\otimes(V\setminus i)},    \tag{12}
\]

which is nonzero.  This is a contradiction. `QED`

In particular, rowwise cloning

\[
                         b_i^2=\lambda_i b_i^1            \tag{13}

\]

cannot survive the third face.  Equations (6)--(7) make every incident
block have the fixed factor `(1,lambda_i)` at site `i`, so its entire
`12` output is locally rank one.  This recovers the decomposable tensor in
the cloning note without coefficient enumeration.

Lemma 2.1 gives the promised normal form.  Let

\[
                         L_i=\operatorname{span}
                                  \{b_i^1,b_i^2\}\subset K_i.          \tag{14}
\]

Regard (6) as a bilinear edge form on `L_i x L_k`, and let

\[
                  \mathcal T(C,L)=H_V((Q_{ik}|_{L_i\times L_k})_{i<k})
                     \in\bigotimes_iL_i^*.                \tag{15}
\]

Choosing the ordered basis `(b_i^1,b_i^2)` at each site identifies (15)
with the tensor in (9).  Changing those bases acts by the corresponding
local `GL_2` matrices.  Hence the basis-free content of the third face is

\[
             \boxed{\ \mathcal T(C,L)
                    \text{ lies in the full-local-rank binary-GHZ orbit.}\ }   \tag{16}
\]

This is strictly stronger than asking the edge forms (8) to have rank two.
The complete bottom binary faces further require each of the two selected
sections `i -> b_i^r` of the planes (14) to be a complete binary-contact
direction through all orders, not merely a tangent vector.

For `n=6`, `dim K_i=4`, so (14) leaves exactly

\[
                           (L_i)_{i=0}^5\in\operatorname{Gr}(2,4)^6.   \tag{17}
\]

This is the sharply parametrized all-three-face survivor.  It replaces the
sixty directed first-jet coordinates by six planes plus their local bases,
while retaining every complex cancellation in (15).

## 3. The first genuinely ternary Bianchi equation

Fix three sites `i<k<p`, write `S={i,k,p}`, and assign them colors
`r,s,t in {1,2}`.  A matching contributing to this coefficient has one of
two forms:

* one `a` edge joins two sites of `S`, and one `b` edge joins the third site
  to a vertex outside `S`; or
* three `b` edges join the three sites injectively to vertices outside
  `S`.

The remaining vertices are paired by `C`.  Direct enumeration therefore
gives

\[
\begin{aligned}
 \Theta_{ikp}^{rst}={}&
 a_{ik}^{rs}\sum_{j\notin S}b_{pj}^t h_{ikpj}
 +a_{ip}^{rt}\sum_{j\notin S}b_{kj}^s h_{ikpj}\\
 &+a_{kp}^{st}\sum_{j\notin S}b_{ij}^r h_{ikpj}\\
 &+\sum_{\substack{j,\ell,q\notin S\\
                    j,\ell,q\text{ distinct}}}
       b_{ij}^r b_{k\ell}^s b_{pq}^t h_{ikpj\ell q}.      \tag{18}
\end{aligned}
\]

The first genuinely ternary compatibility equations are

\[
                      \boxed{\Theta_{ikp}^{rst}=0}         \tag{19}
\]

for the six triples `(r,s,t)` which use both one and two.  The cases `111`
and `222` are already among the complete `01` and `02` binary equations.
After (7) is substituted, (18) is a homogeneous cubic polynomial in the
two cofactor-plane sections.

At six sites, if `R=V\setminus S={u,v,w}`, define

\[
 \ell_{p\mid ik}^t
   =\sum_{j\in R}b_{pj}^t C_{R\setminus\{j\}},             \tag{20}
\]

where `C_{R\setminus{j}}` is the scalar edge on the other two members of
`R`.  Since deleting all six vertices has hafnian one, (18) becomes

\[
 \Theta_{ikp}^{rst}
   =a_{ik}^{rs}\ell_{p\mid ik}^t
    +a_{ip}^{rt}\ell_{k\mid ip}^s
    +a_{kp}^{st}\ell_{i\mid kp}^r
    +\operatorname{per}
       \begin{pmatrix}
        b_{iu}^r&b_{iv}^r&b_{iw}^r\\
        b_{ku}^s&b_{kv}^s&b_{kw}^s\\
        b_{pu}^t&b_{pv}^t&b_{pw}^t
       \end{pmatrix}.                                    \tag{21}
\]

This is a finite connection-plus-permanent equation.  It keeps endpoint
order and all cancellations, and it is the exact first layer omitted by
the three binary faces.

## 4. The cofactor-open four-site chart is impossible

The order-four clone from the preceding note is not a warning for the
all-three-face problem.  In fact the entire cofactor-open order-four chart
is excluded already by (16).

Write the six scalar entries as `c_01,...,c_23` and put

\[
                         H=c_{01}c_{23}+c_{02}c_{13}+c_{03}c_{12}.
                                                                    \tag{22}
\]

At four sites `h_ij` is the scalar entry on the complementary pair, so
cofactor openness says that all six `c_ij` are nonzero.  Each `K_i` has
dimension two.  Lemma 2.1 therefore forces `L_i=K_i`; there is no
Grassmannian choice left.

Choose a basis of `K_i` by making its first two neighbor coordinates the
standard basis and solving (4) in the last coordinate.  Form (15), and
flatten it across `01|23`, with binary words in lexicographic order on both
sides.  Exact simplification gives

\[
\small
F=\begin{pmatrix}
 {H\over c_{01}^2c_{02}c_{03}}&
 {H\over c_{01}^2c_{03}c_{12}}&
 {H\over c_{01}^2c_{02}c_{13}}&
 {H\over c_{01}^2c_{12}c_{13}}\\
 0&0&-{H\over c_{01}c_{02}c_{12}c_{13}}&0\\
 0&-{H\over c_{01}c_{02}c_{03}c_{12}}&0&0\\
 0&-{H\over c_{01}c_{02}c_{12}c_{23}}&
     -{H\over c_{01}c_{02}c_{12}c_{23}}&0
\end{pmatrix}.                                           \tag{23}
\]

The minor in the first three rows and columns is

\[
              -{H^3\over
                 c_{01}^4c_{02}^3c_{03}^2c_{12}^2c_{13}}. \tag{24}
\]

Under (1), `H=1`, so (24) is nonzero.  Hence (23) has rank at least three.
Changing the bases of the four `K_i` applies invertible local maps and does
not change this flattening rank.  On the other hand every flattening of
`X_1+X_2` has rank exactly two.  This contradicts (9).

We have proved:

**Proposition 4.1 (order-four cofactor-open obstruction).**  There is no
four-site simultaneous two-jet with normalized cofactor-open leading
matrix for which all three second-color blocks form exact binary equality.
This uses only the degree-one and degree-two equations through color zero
and the complete `12` face; the higher `01` and `02` equations are not
needed.

Thus the exact clone seed is correctly classified as a two-face
countermodule, not an all-three-face survivor.  The familiar actual
three-color equality on the three one-factors of `K_4` lies on the
cofactor-zero boundary and is not covered by Proposition 4.1.

## 5. The six-site singular boundary survives the cubic layer

The cofactor-open hypothesis cannot be dropped.  On six sites take the
three unit diagonal factors

\[
\begin{aligned}
P_0&=01|23|45,\\
P_1&=05|12|34,\\
P_2&=03|15|24.                                             \tag{25}
\end{aligned}
\]

Every pairwise union is one alternating Hamilton cycle, so all three
principal binary faces are exact.  The union has exactly one further
perfect matching,

\[
                              03|12|45,                    \tag{26}
\]

whose coloring is

\[
                              (2,1,1,2,0,0).               \tag{27}
\]

Consequently every genuinely mixed degree-three coefficient through the
color-zero endpoint is zero; the first error has nonzero-color degree four
and is the singleton (26).

For the scalar leading matrix supported on `P_0`, however, `h_ij` is
nonzero only on the three pairs in `P_0`.  The other twelve two-hole
cofactors vanish.  The direct `11`, `12`, `21`, and `22` cells can therefore
live in second-order-invisible directions and are not governed by (6).
This is exactly how (25) evades the plane normal form.

The exact audit
`computations/verify_all_three_binary_cofactor_planes.py`:

* derives (23) symbolically and verifies the minor (24);
* checks (18) against direct rational matching enumeration for all 160
  labeled three-site sectors of the dense six-site module from
  `color-torus-pure-limit-two-jet-boundary.md`; and
* enumerates all 729 coefficients of (25), verifies all three binary faces,
  all mixed cubics, the twelve zero cofactors, and the sole error (27).

## 6. Exact frontier at six sites

The all-three-face problem on the cofactor-open locus is now reduced to the
following concrete system rather than an unstructured ternary source:

1. `C` is a scalar six-site matrix with `haf(C)=1` and fifteen nonzero
   two-hole cofactors;
2. `L_i in Gr(2,4)` for all six sites;
3. the cofactor-pairing tensor (15) belongs to the binary-GHZ orbit;
4. some ordered bases of the `L_i` give two complete binary-contact
   sections for the `01` and `02` faces; and
5. their 120 genuinely mixed labeled equations (19) vanish.

The count in item 5 is `20` site triples times six mixed color placements.
This is the first genuinely ternary compatibility, not a polarization sum.
The exact checker finds 78 nonzero mixed residuals for the previously
constructed dense rational two-jet, so the equations have real force.

What is not yet proved is that the system in items 1--5 is empty.  Existing
six-site exact binary gadgets do not furnish a point of it: Hamilton and
four-cycle-switch families have many zero scalar cofactors, and the dense
cofactor-open constructions in the torus notes stop before complete binary
equality.  Conversely, no norm inequality presently excludes a dense
binary seed.  At the uniform leading point, however, cyclic plane symmetry
is now impossible: four pure cubic orbit equations have a three-line
radical, and one mixed cubic collapses the swapping branch to local rank
one.  The next useful attack is therefore the noncyclic orbit condition
(16) on `Gr(2,4)^6`, or a one-binary theorem proving that item 4 cannot occur
on the general cofactor-open locus.
