# The uncompressed one-hole cofactor kernel

## 1. The exact consequence for an invertible deleted edge

Use the notation and cross-product convention of
`notes/two-vertex-annihilation-identities.md`.  Thus `p,q` are fixed,
`R=B\setminus{p,q}`, and

\[
 \gamma_{u,r}=\alpha^TC_{u,r}\beta,
 \qquad C_{u,r}=A_{pu}K_rA_{qu}^T.                         \tag{1}
\]

Put

\[
 C_{pq}:=H_R(A)\in\bigotimes_{u\in R}V_u.                 \tag{2}
\]

If `A_pq` is invertible, the one-hole identity proves more than the
existence of zero cross matrices.  For every hole `w in R`, contraction of
`C_pq` at all other sites by the coupled cross products is the zero vector:

\[
 \boxed{
  \left\langle C_{pq},\bigotimes_{u\in R\setminus\{w\}}
                    \gamma_u(\alpha,\beta)\right\rangle
       =0\in V_w\quad\text{identically in }\alpha,\beta .} \tag{3}
\]

Indeed, comparison of the arbitrary hole covector gives

\[
 \alpha_r\beta_r\prod_{u\ne w}\gamma_{u,r}
 = (\alpha^TA_{pq}\beta)T_{w,r}.                           \tag{4}
\]

The divisor on the right is irreducible of matrix rank three.  It cannot
divide a nonzero cross factor, whose matrix rank is at most two.  Hence the
left side of (4) is the zero polynomial, and then the integral-domain
property gives `T_w,r=0`.  This proves (3) coordinate by coordinate.

At an entry-minimal realization a nonzero `A_pq` has `C_pq!=0`; otherwise
every cell on `pq` could be deleted without changing the matching tensor.
Thus (3) asks for a nonzero matching tensor in the simultaneous kernel of
a family of multiply-and-symmetrize maps.

## 2. The transverse six-anchor branch at eight sites

Now specialize to `|B|=8`, so `|R|=6`.  The forced incident-edge theorem
gives three different directed anchor sites from `p` and three from `q`.
This section treats the sharp branch in which selected anchor sets

\[
 R=U\mathbin{\dot\cup}V,\qquad |U|=|V|=3,                 \tag{5}
\]

are disjoint.  For `u in U` and `v in V`, write

\[
 A_{pu}=a_ue_{r_u}^T,\qquad A_{qv}=b_ve_{s_v}^T,           \tag{6}
\]

where each of `(r_u)_(u in U)` and `(s_v)_(v in V)` is a permutation of
the three colors.

At a `p`-anchor,

\[
 \gamma_u=(\alpha^Ta_u)\bigl(e_{r_u}\times(\beta^TA_{qu})\bigr).
                                                                    \tag{7}
\]

Assume the opposite star is transverse there:

\[
 \operatorname{rank}A_{qu}[:,\{0,1,2\}\setminus\{r_u\}]=2. \tag{8}
\]

After removing the scalar `alpha^T a_u`, substitution by `gamma_u`
defines a rank-two map

\[
 \phi_u:V_u\longrightarrow L_\beta,qquad
 \ker\phi_u=\mathbb Ce_{r_u},quad
 W_u:=\operatorname{im}\phi_u\subset L_\beta,             \tag{9}
\]

where `L_beta` is the three-dimensional space of linear forms in `beta`.
Thus `W_u` is a plane.  Symmetrically, assume

\[
 \operatorname{rank}A_{pv}[:,\{0,1,2\}\setminus\{s_v\}]=2 \tag{10}
\]

at every `q`-anchor.  Removing the scalar `beta^T b_v` gives a quotient
map with kernel `C e_s_v` and image a plane `Z_v` in the linear forms
`L_alpha`.

The failure of (8) or (10) is precisely an additional projected-rank
degeneracy of the kind seen in the zero-witness countermodel.  We next
classify the transverse branch.

## 3. Multiplying three planes of linear forms

Let `L` be three-dimensional and let `W_0,W_1,W_2` be distinct planes in
`L`.  Consider

\[
 \mu:W_0\otimes W_1\otimes W_2\longrightarrow\operatorname{Sym}^3L,
 \qquad f_0\otimes f_1\otimes f_2\longmapsto f_0f_1f_2.    \tag{11}
\]

**Lemma 3.1 (three-plane Koszul kernel).**  If the three plane normals are
linearly independent, then `ker mu` is one-dimensional.  More explicitly,
let `ell_ij` span `W_i intersect W_j`.  Up to nonzero scalar,

\[
 \kappa_W=
 \ell_{20}\otimes\ell_{01}\otimes\ell_{12}
 -\ell_{01}\otimes\ell_{12}\otimes\ell_{20}              \tag{12}
\]

spans the kernel (with the factors placed in the order `W_0,W_1,W_2`).
Multiplication of any two different planes is injective.

**Proof.**  Independent normals allow a change of coordinates with

\[
 W_0=\langle y,z\rangle,\quad
 W_1=\langle z,x\rangle,\quad
 W_2=\langle x,y\rangle.                                  \tag{13}
\]

The eight basis products are seven different cubic monomials: `xyz`
occurs twice and every other product once.  This proves (12) and the
one-dimensional assertion.  For two distinct planes, their intersection
is a line; the four products of adapted bases are four different quadratic
monomials, proving injectivity. `QED`

If the normals are dependent, either two planes coincide or all three
planes contain a common nonzero linear form.  Thus failure of the lemma's
general-position hypothesis is exactly a coincident-plane or shared-factor
geometry.

## 4. Exact quotient classification

Let

\[
 \overline C_{pq}\in
 \bigotimes_{u\in U}(V_u/\mathbb Ce_{r_u})\otimes
 \bigotimes_{v\in V}(V_v/\mathbb Ce_{s_v})                \tag{14}
\]

be the quotient of the six-site cofactor.  Identify its local factors with
the image planes `W_u,Z_v` using (9)--(10).

**Theorem 4.1 (transverse quotient web).**  Suppose the three `W_u` have
independent normals, and so do the three `Z_v`.  Then the six one-hole
identities (3) imply

\[
             \overline C_{pq}\in
             \mathbb C(\kappa_U\otimes\kappa_V),           \tag{15}
\]

where `kappa_U` and `kappa_V` are the two three-plane kernels (12).

**Proof.**  Omit a hole `w in U`.  After removing the nonzero scalar
linear factors in (7), the quotient of (3) is the tensor product of:

1. the identity at `W_w` and the injective two-plane multiplication map at
   the other two `U` sites; and
2. the three-plane multiplication map on all `V` sites.

Its kernel is therefore

\[
       (W_{u_0}\otimes W_{u_1}\otimes W_{u_2})
       \otimes\mathbb C\kappa_V.                           \tag{16}
\]

The holes in `V` symmetrically put the quotient cofactor in

\[
       \mathbb C\kappa_U\otimes
       (Z_{v_0}\otimes Z_{v_1}\otimes Z_{v_2}).            \tag{17}
\]

The intersection of (16) and (17) is the line in (15). `QED`

Thus the uncompressed identities do force an exact normal form.  Their
failure branches are concrete: anchor collisions, a rank drop in (8) or
(10), coincident planes, or a common linear factor.  Unfortunately, the
normal form itself is compatible with six-site matching structure.

## 5. The quotient web is exactly matching-realizable

At every local factor the two pure factors occurring in (12) are
independent.  Local basis changes therefore put

\[
 \kappa_U=e_0^{\otimes U}-e_1^{\otimes U},\qquad
 \kappa_V=e_0^{\otimes V}-e_1^{\otimes V}.                 \tag{18}
\]

There is an eight-edge exact realization of their product.  Label
`U={0,1,2}`, `V={3,4,5}` and use only

\[
       01,02,45,35,23,24,13,14.                            \tag{19}
\]

Put the following rank-one binary matrices on them, oriented by increasing
vertex order:

\[
\begin{array}{c|cccccccc}
uv&01&02&45&35&23&24&13&14\\ \hline
A_{uv}&e_0e_0^T&e_1e_1^T&e_0e_0^T&e_1e_1^T&
e_0e_0^T&-e_0e_1^T&-e_1e_0^T&e_1e_1^T.
\end{array}                                                \tag{20}
\]

The support graph has exactly four perfect matchings:

\[
 01|23|45,\quad 01|24|35,\quad
 02|13|45,\quad 02|14|35.                                 \tag{21}
\]

Their tensors are respectively the four group-constant binary strings
with coefficients `+1,-1,-1,+1`.  Hence

\[
 H_6(A)=
 (e_0^{\otimes U}-e_1^{\otimes U})\otimes
 (e_0^{\otimes V}-e_1^{\otimes V})
 =\kappa_U\otimes\kappa_V.                                \tag{22}
\]

Embedding the binary spaces into the three-dimensional quotient factors
and undoing the local basis changes realizes every nonzero tensor on the
line (15).

Therefore Theorem 4.1 cannot finish the argument by combining (3) only
with the fact that `C_pq` is a six-site matching tensor.  A continuation
must retain the anchor-line lift terms discarded in (14), or impose the
one-hole systems belonging to overlapping pairs among the six anchor
sites.

That overlapping-pair test is carried out in
`notes/all-one-hole-system-countermodel.md`.  The web has an exact
three-color lift which satisfies the full one-hole systems for all `28`
pairs simultaneously, and even the full two-hole systems for every pair
inside the six-site web.  The first surviving detector is the full
two-hole identity for the central pair, including its correction matrix.

## 6. Exact audit

`computations/verify_one_hole_cofactor_kernel.py` checks over the integers
that:

1. pair-plane multiplication is injective;
2. the three-plane multiplication map has the one-dimensional kernel
   (12);
3. the combined six one-hole quotient map has rank `63` on its
   `64`-dimensional domain and kernel exactly
   `C(kappa_U tensor kappa_V)`; and
4. the eight matrices (20) have precisely the four supported perfect
   matchings (21) and matching tensor (22).
