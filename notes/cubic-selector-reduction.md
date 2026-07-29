# Cubic selectors, mixed curvature, and a six-edge neighborhood cut

This note gives an exact order-two reduction at any cubic support vertex.
It strengthens the high-degree-core lemma in `notes/induction-route.md`: in
a minimal-order putative three-color realization, a cubic vertex cannot sit
behind an arbitrary sparse neighborhood.  Each of its three neighbors must
send two color-distinct active rows outside the closed neighborhood, so that
cut has at least six underlying edges.

Throughout, endpoint order is retained and every aggregate edge is an
arbitrary `3 by 3` matrix over `C`.

## 1. The selector normal form

Suppose the realization has first been chosen entry-minimal (so every
nonzero underlying matrix has a nonzero full cofactor), and suppose

\[
                  H_B(A)=\sum_{r=0}^2e_r^{\otimes B},       \tag{1}
\]

and a vertex `p` has exactly three nonzero underlying neighbors
`a_0,a_1,a_2`.  Cubic-vertex rigidity (after relabeling the neighbors and
absorbing nonzero scalars) gives

\[
 A_{p a_r}=\lambda_r e_r^{(p)}\otimes e_r^{(a_r)},\qquad
 H_{B\setminus\{p,a_r\}}(A)
       =\lambda_r^{-1}e_r^{\otimes(B\setminus\{p,a_r\})},   \tag{2}
\]

where every `lambda_r` is nonzero.

Fix `r`, write `{r,s,t}={0,1,2}`, put `a=a_r` and

\[
                         U=B\setminus\{p,a\},
 \qquad X=A|_{\binom U2}.                                  \tag{3}
\]

For `h in {s,t}`, define an edge family `R_h` on `U` by

\[
 (R_h)_{uv}=
 (e_h^*\otimes e_h^*)\mathbin{\lrcorner}
 \bigl(A_{pu}\otimes A_{av}+A_{pv}\otimes A_{au}\bigr).  \tag{4}
\]

The first covector in (4) is at `p` and the second at `a`.
Because the only edge at `p` with `e_h` in its `p`-slot is
`p a_h`, the family `R_h` is supported on the star centered at `a_h`.
More explicitly, apart from the harmless endpoint reordering,

\[
 (R_h)_{a_hx}=\lambda_h e_h^{(a_h)}\otimes
                 (e_h^*\otimes\operatorname{id})A_{ax}.    \tag{5}
\]

**Lemma 1.1 (cubic-selector normal form).**  With the preceding notation,

\[
 H_U(X)=\lambda_r^{-1}e_r^{\otimes U},\qquad
 D H_U(X)[R_h]=e_h^{\otimes U}\quad(h=s,t).                 \tag{6}
\]

Moreover, if

\[
                 Q_r:=D^2H_U(X)[R_s,R_t],                  \tag{7}
\]

then for arbitrary scalars `z_s,z_t`,

\[
 H_U(X+z_sR_s+z_tR_t)
  =\lambda_r^{-1}e_r^{\otimes U}
    +z_s e_s^{\otimes U}+z_t e_t^{\otimes U}
    +z_sz_tQ_r.                                             \tag{8}
\]

In particular, if `Q_r=0`, the vertices `p,a_r` can be deleted and the
remaining `|B|-2` vertices admit an exact three-color realization.

**Proof.**  Cap the slots `p,a` in (1), first by
`e_r^* tensor e_r^*`.  Its direct-edge scalar is `lambda_r`, while every
two-cross-edge term vanishes because the other two matrices at `p` have
`p`-factors `e_s,e_t`.  The exact pair-cap formula therefore gives the
first equation in (6).

For `h=s,t`, cap instead by `e_h^* tensor e_h^*`.  The direct-edge scalar
is zero.  Formula (4) is exactly the first-jet family in the pair-cap
formula, and the cap of the target is `e_h^(tensor U)`.  This proves the
other two equations in (6).

No matching can use two `R_h`-edges, since all of them meet `a_h`.
Nor can a matching use three edges from `R_s union R_t`, since those edges
are covered by the two centers `a_s,a_t`.  The multivariate Taylor
expansion of the hafnian consequently stops after the mixed second
derivative and is exactly (8).

If `Q_r=0`, take nonzero `z_s,z_t` in (8).  Its three diagonal
coefficients are nonzero.  An invertible diagonal change of basis at one
remaining vertex normalizes all three to one, and applying that change to
the corresponding endpoints of its incident matrices gives an ordinary
aggregate-edge realization of `Delta_(U,3)`.  This is the asserted
order-two reduction. `QED`

The point is that `Q_r` is not an unspecified cap cumulant.  It has two
fixed, different colors:

\[
 Q_r\in e_s^{(a_s)}\otimes e_t^{(a_t)}\otimes
       \bigotimes_{v\in U\setminus\{a_s,a_t\}}V_v.          \tag{9}
\]

Thus every nonzero coefficient of `Q_r` is visibly mixed.

## 2. Consequence for a minimal-order realization

Call a realization **order-minimal above four** if its order is at least
six and no smaller even order at least six admits three colors.  Once the
six-vertex obstruction is known, any hypothetical realization has such an
order-minimal descendant.

**Theorem 2.1 (six-edge closed-neighborhood cut).**  Let (1) be an
order-minimal realization of order at least eight, chosen entry-minimal
within that order, and let `p` be cubic in its nonzero support graph.
Then all three tensors `Q_0,Q_1,Q_2` in (7) are nonzero.  For each
`r`, there are distinct vertices

\[
 x_{r,s},x_{r,t}\in B\setminus
       \{p,a_0,a_1,a_2\}                                   \tag{10}
\]

such that

\[
 (e_s^*\otimes\operatorname{id})A_{a_rx_{r,s}}\ne0,
 \qquad
 (e_t^*\otimes\operatorname{id})A_{a_rx_{r,t}}\ne0,        \tag{11}
\]

and the complementary matching tensor occurring in the corresponding
summand of `Q_r` is nonzero.  Consequently

\[
                 |\delta_G(\{p,a_0,a_1,a_2\})|\ge6.        \tag{12}
\]

Here `G` is the active underlying support graph.

**Proof.**  If some `Q_r` vanished, Lemma 1.1 would give a three-color
realization on `|B|-2>=6` vertices, contrary to order-minimality.  Hence
all three are nonzero.

Expand `Q_r` using (5).  Every summand chooses one `R_s`-edge at the
center `a_s`, one `R_t`-edge at the center `a_t`, and an `X`-matching on
the remaining vertices.  The free endpoints of those two edges must be
distinct and cannot be `a_s` or `a_t`; they also cannot be `p` or the
deleted vertex `a_r`.  Since the sum is nonzero, at least one summand is
nonzero.  Its two free endpoints give (10), its two row factors give
(11), and its remaining factor is the stated nonzero complementary
matching tensor.

For fixed `r`, (11) supplies two distinct support edges from `a_r` to the
outside of the four-vertex closed neighborhood.  Doing this for all three
values of `r` supplies six distinct underlying cut edges (edges with
different inside endpoints are distinct), proving (12). `QED`

This does not by itself exclude a dense tight-cut-free core.  It does rule
out every proposed uniform reduction in which a cubic selector is assumed
to have a sparse or separable neighborhood: the nonzero mixed curvature is
forced three times, with explicit color rows and nonzero cofactors.
