# A zero shore forces internal-star saturation

## 1. Outcome

The growing zero-shore identity has a cancellation-safe consequence which
does not require sparse shore rows.  Work over \(\mathbb C\), after the
ternary target projection, so
\(V_u=\langle e_0^{(u)},e_1^{(u)},e_2^{(u)}\rangle\).  Let
\(B=C\sqcup D\), \(|B|=N=2m\), \(|C|=h\le m\), and put

\[
                 d=|D|=N-h,\qquad r=m-h,
                 \qquad d=2r+h.                         \tag{1}
\]

Suppose that the blocks internal to \(C\) vanish and that, in the
site-square-zero algebra on \(D\),

\[
 \left(\prod_{j=1}^{h}p_{c_j}^{(j)}\right)q^{[r]}
   =\begin{cases}
       X_c^D,&c_1=\cdots=c_h=c,\\
       0,&\text{otherwise}.
     \end{cases}                                      \tag{2}
\]

For \(u\in D\), let

\[
 W_u(q)=\sum_{v\in D\setminus\{u\}}
       \operatorname {im}\bigl(q_{uv}:V_v^*\longrightarrow V_u\bigr)
       \subseteq V_u                                  \tag{3}
\]

be the local image of the complete internal \(q\)-star.  Then, for every
target colour \(c\),

\[
 \boxed{\quad
   \#\{u\in D:e_c^{(u)}\notin W_u(q)\}\le h.
 \quad}                                                \tag{4}
\]

Consequently, for every set \(T\subseteq\{0,1,2\}\) of \(t\) colours,

\[
 \#\{u\in D:e_c^{(u)}\in W_u(q)\text{ for every }c\in T\}
       \ge d-th.                                       \tag{5}
\]

In particular the complement contains at least

\[
 \begin{array}{c|c}
 \text{local internal-star property}&\text{number of sites}\\ \hline
 e_c\in W_u(q)&N-2h\\
 e_c,e_{c'}\in W_u(q)&N-3h\\
 W_u(q)=V_u&N-4h
 \end{array}                                           \tag{6}
\]

sites, where the second row holds for each fixed colour pair.  For the
good-clique shore \(h=\lceil N/5\rceil\), the last number is nonnegative
for every even \(N\ge16\) and grows linearly (apart from the sharp
\(N=16\) boundary).  Thus the flat alternative is not merely a large
independent shore: it exports a linearly large set of locally full internal
stars on the opposite side.

Equivalently, at each of those \(N-4h\) sites the internal aggregate-star
map

\[
 V_u^*\longrightarrow\bigoplus_{v\in D\setminus\{u\}}V_v,
 \qquad \beta\longmapsto
       \bigl((\beta\otimes\operatorname{id})q_{uv}\bigr)_v       \tag{7}
\]

is injective: its kernel is exactly \(W_u(q)^\perp\).  This gives a direct
bridge back from the arbitrary-frame zero shore to injective-star
geometry on its complement.

Sections 2--5 give complementary algebraic forms of the same obstruction.
The first is a short matching-capacity proof of (4).  The second records
the exact hafnian ideal and apolar ladder which remain after (4); this is a
sharper residual than an arbitrary capped response tensor.

## 2. Scalarization and the capacity contradiction

For a family of local covectors \(\alpha=(\alpha_u)_{u\in D}\), apply the
algebra homomorphism

\[
 \rho_\alpha:\bigotimes_{u\in D}(\mathbb C\oplus V_u)
       \longrightarrow
       \mathbb C[x_u:u\in D]/(x_u^2:u\in D),
 \qquad v\in V_u\longmapsto\alpha_u(v)x_u.             \tag{8}
\]

Write

\[
 \ell_{j,c}(\alpha)=\rho_\alpha(p_c^{(j)}),\qquad
 q_\alpha=\rho_\alpha(q),\qquad x_D=\prod_{u\in D}x_u.
\]

The diagonal row of (2) becomes

\[
 \left(\prod_{j=1}^{h}\ell_{j,c}(\alpha)\right)
          q_\alpha^{[r]}
    =\left(\prod_{u\in D}\alpha_u(e_c^{(u)})\right)x_D. \tag{9}
\]

This is an identity after scalarization, not a selection of one matching
from a cancelling coefficient.

Fix a colour \(c\), and suppose that (4) fails.  Choose a set
\(Z\subseteq D\) of \(h+1\) sites for which
\(e_c^{(u)}\notin W_u(q)\).  Elementary linear separation supplies, for
every \(u\in Z\), a covector

\[
       \alpha_u|_{W_u(q)}=0,
       \qquad \alpha_u(e_c^{(u)})\ne0.                 \tag{10}
\]

At the other sites choose any \(\alpha_u\) nonzero on \(e_c^{(u)}\).
Every scalar edge of \(q_\alpha\) incident with \(Z\) is zero: at its
endpoint \(u\in Z\), (10) annihilates the image of the corresponding block.
The scalar quadratic is therefore supported on only

\[
                    d-(h+1)=2r-1                       \tag{11}
\]

sites.  It has no \(r\)-edge matching, so \(q_\alpha^{[r]}=0\).  The left
side of (9) vanishes, whereas its right side is nonzero by construction.
This contradiction proves (4).

For (5), the union of the exceptional sets in (4), over \(c\in T\), has
order at most \(th\).  Taking \(|T|=1,2,3\) gives (6).  In the last case
the three independent target axes lie in \(W_u(q)\), hence
\(W_u(q)=V_u\).

Notice what was not used: no shore row was localized, no aggregate block
was separated into decorated sources, no matching term was declared
nonzero, and none of the mixed rows of (2) was needed.  Complex
cancellation remains completely inside the scalar divided power until
matching capacity makes that entire power zero.

The coefficient \(h\) in (4) is already sharp at the smallest ternary
source.  In the three-colour \(K_4\) one-factorization, take one vertex as
\(C\).  For each colour, the internal \(q\)-edge of that colour joins two
of the three complement sites, and the third site is the unique exception
to (4).

## 3. Curvature or a sparse cross-interface

Now restore the fact that the shore supplied by the good-clique theorem is
itself a good clique, and let

\[
             F=\{u\in D:W_u(q)=V_u\}.
\]

Thus \(|F|\ge N-4h\).  For each \(x\in C\), at most three deletions
\(u\in D\) make the \(x\)-star noninjective.  This is the
[essential-star bound](target-flattening-essential-star-pair-bound.md)
applied at \(x\).  At the other endpoint, every \(u\in F\) retains
its injective internal \(q\)-star after \(x\) is deleted.  It follows that
there are at most \(3h\) bad incidences in \(C\times F\).

For \(u\in F\), let \(g(u)\) be the number of its good neighbours in
\(C\).  If \(g(u)\ge3\), every three of those neighbours form a good fan
centred at \(u\).  The
[canonical transition-pencil theorem](canonical-transition-pencil-fan-dichotomy.md)
gives the following alternative:

1. one such fan has a nonzero physical transition, and hence a literal
   nonzero \(2\times2\) source minor, an inverse selector, and a generically
   active affine cap line; or
2. every such fan is flat, in which case
   \(A_{ux}=0\) for every good neighbour \(x\in C\).

In the second branch, all nonzero blocks from a vertex with \(g(u)\ge3\)
to \(C\) lie on bad pairs.  A vertex with \(g(u)\le2\) has at least
\(h-2\) bad neighbours.  Since the total number of bad incidences is at
most \(3h\), there are at most

\[
                         \left\lfloor\frac{3h}{h-2}\right\rfloor
\]

such exceptional vertices.  Counting their at most two good incidences in
addition to all bad incidences proves the cancellation-free bound

\[
 \boxed{\quad
 \#\{(x,u)\in C\times F:A_{xu}\ne0\}
    \le 3h+2\left\lfloor\frac{3h}{h-2}\right\rfloor .
 \quad}                                                \tag{12a}
\]

Thus the growing zero shore has a second nonenumerative continuation:
either it immediately returns to the curvature/active-line branch, or its
interface with every forced full internal star is aggregate-sparse, with
asymptotic average degree at most three on the shore side.  Statement
(12a) retains zero blocks, endpoint order, and arbitrary cancellation; it
counts aggregate blocks only after flatness has proved them literally
zero.

## 4. The exact hafnian ideal

Keep \(\alpha_u\) as independent covector variables.  For a
\(2r\)-set \(S\subseteq D\), denote by

\[
             H_S(\alpha)=[x_S]q_\alpha^{[r]}            \tag{12}
\]

the scalar hafnian coefficient, and let \(I_r(q)\) be the ideal generated
by all \(H_S\) in the polynomial ring of the \(\alpha\)-coordinates.  If
\(H=D\setminus S\), let

\[
 P_{\mathbf c,H}(\alpha)
       =[x_H]\prod_{j=1}^{h}\ell_{j,c_j}(\alpha)        \tag{13}
\]

be the corresponding ordered-row permanent.  Taking the top coefficient
in the scalarized version of (2) gives all \(3^h\) identities

\[
 \sum_{\substack{S\subseteq D\\|S|=2r}}
      P_{\mathbf c,D\setminus S}(\alpha)H_S(\alpha)
   =\begin{cases}
      M_c(\alpha),&\mathbf c=c^h,\\
      0,&\text{otherwise},
    \end{cases}                                        \tag{14}
\]

where

\[
                  M_c(\alpha)=\prod_{u\in D}
                                  \alpha_u(e_c^{(u)}).  \tag{15}
\]

Thus

\[
                         M_0,M_1,M_2\in I_r(q),          \tag{16}
\]

while the nonconstant shore words give explicit permanent syzygies among
the same hafnian generators.  Geometrically,

\[
 V(I_r(q))\subseteq V(M_0)\cap V(M_1)\cap V(M_2).      \tag{17}
\]

Equivalently, the internal matching power cannot vanish at a scalarization
which is nonzero on all three target axes at every site.  Formula (4) is
the first uniform block-geometric consequence of this torus exclusion.
It is precisely here that a valuation or UFD argument has useful content:
the only allowed common-hafnian degenerations lie on the displayed target
coordinate boundary.  Merely factoring one diagonal output discards the
mixed syzygies in (14) and is not enough.

## 5. Apolar form and the remaining residual

Let \(\star\) be complement duality in the scalar square-free algebra,

\[
                         \star(x_S)=y_{D\setminus S}.
\]

Multiplication by \(\sum_u a_ux_u\) becomes the directional derivative
\(\sum_u a_u\partial_{y_u}\).  Put

\[
 F_s(\alpha;y)=\star\bigl(q_\alpha^{[r-s]}\bigr),
       \qquad 0\le s\le r.                             \tag{18}
\]

Then \(F_s\) is multiaffine of degree \(h+2s\), and (2) is exactly

\[
 \left(\prod_{j=1}^{h}D_{\ell_{j,c_j}(\alpha)}\right)F_0
   =\begin{cases}
       M_c(\alpha),&\mathbf c=c^h,\\
       0,&\text{otherwise}.
     \end{cases}                                      \tag{19}
\]

The fact that \(F_0\) comes from one common matching power is retained by
the full second-order ladder

\[
 \boxed{\quad
   \Box_{q_\alpha}F_{s+1}=(r-s)F_s\quad(0\le s<r),
   \qquad F_r=y_D,
 \quad}                                                \tag{20}
\]

where

\[
 \Box_{q_\alpha}=
   \sum_{u<v}[x_ux_v]q_\alpha\,
                   \partial_{y_u}\partial_{y_v}.       \tag{21}
\]

Indeed, complement duality sends multiplication by \(q_\alpha\) to
\(\Box_{q_\alpha}\), and
\(q_\alpha q_\alpha^{[k]}=(k+1)q_\alpha^{[k+1]}\).

Equations (14), (19), and (20) isolate the remaining arbitrary-frame
problem without a support census:

> exclude a length-\(r\) multiaffine apolar ladder whose bottom form has
> the complete diagonal derivative table (19), while its internal block
> stars obey the forced incidence profile (5); or turn one of the
> \(N-4h\) full internal stars into an active clean cap.

The abstract capped-table equations alone impose neither the hafnian ideal
membership with its permanent syzygies nor the ladder (20).  These are the
common-power constraints that must be preserved in the next step.

No executable is required: (4) is linear separation plus the exact
capacity count \(d-(h+1)=2r-1\), and (14)--(20) are coefficientwise
identities in the scalar square-free algebra.
