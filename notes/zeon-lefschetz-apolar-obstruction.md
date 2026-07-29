# The GHZ apolar algebra is already strong Lefschetz

## Outcome

The most direct Lefschetz/apolar/Hessian/Jordan obstruction in the
square-zero formulation cannot distinguish the forbidden tensor.  In fact,
for every even `n=2m`, the apolar algebra of

\[
 \Delta_{n,3}=\sum_{r=0}^2\prod_{v=1}^n x_{v,r}
\]

contains an explicit quadratic, supported only on pairs of distinct sites,
whose multiplication maps have the strongest possible Lefschetz property:

\[
 \Theta^{m-k}:G_k\longrightarrow G_{n-k}
 \quad\text{is an isomorphism for every }0\leq k\leq m. \tag{1}
\]

The same algebra also has an ordinary strong Lefschetz linear form, so every
classical higher Hessian of the target is nonzero at one common point.  Thus
a proof cannot come from a vanishing Hessian, a short Jordan chain, failure
of unimodality, or failure of a quadratic element to reach the socle.  It
has to retain information about the *particular source quadratic* before
passing to the target's apolar quotient.

This is compatible with the border degeneration in `notes/tensor-route.md`:
all the properties below are properties of the target itself and therefore
hold equally at an exact point or a boundary point.

## 1. Square-zero matching formulation

Let

\[
 \mathcal A=\bigotimes_{v=1}^n(\mathbb C\oplus V_v),
 \qquad V_vV_v=0,
\]

and give `V_v` support degree `{v}`.  For

\[
 Q=\sum_{u<v}A_{uv}\in\mathcal A_2
\]

one has

\[
 [\exp Q]_B=\frac{Q^m}{m!}=H_B(A),\qquad n=2m. \tag{2}
\]

Indeed, a product of edge tensors vanishes exactly when two selected edges
share a site.  Every perfect matching occurs in `Q^m` in all `m!` orders.
Consequently the conjectural equation is precisely

\[
                         Q^m=m!\Delta_{n,3}.             \tag{3}
\]

Only (3)'s top support is prescribed; all lower powers of `Q` are free.

## 2. Exact apolar algebra of the target

Work in the ordinary differential-operator ring on the `3n` variables and
put

\[
 G=\mathbb C[\partial_{v,r}:1\leq v\leq n,0\leq r<3]
      /\operatorname {Ann}(\Delta_{n,3}).                  \tag{4}
\]

The relations making this quotient finite are themselves square-zero by
site.  For a nonempty set `S` and a color `r`, write

\[
 z_{S,r}=\left[\prod_{v\in S}\partial_{v,r}\right].
\]

Then an exact basis of `G` is

\[
 1;\qquad z_{S,r}\ (0<|S|<n,\ 0\leq r<3);\qquad \omega,   \tag{5}
\]

where all three full derivatives `z_{B,r}` represent the same socle
generator `omega`.  To see this, a differential monomial which repeats a
site kills the target, as does one which uses two different colors.  A
proper same-color derivative leaves one distinct same-color monomial, while
all three full same-color derivatives leave the constant one.

In particular

\[
 h_0=h_n=1,\qquad h_k=3\binom nk\quad(0<k<n).              \tag{6}
\]

For nonempty disjoint supports the multiplication is

\[
 z_{S,r}z_{T,s}=\begin{cases}
 z_{S\cup T,r},&r=s,\ |S\cup T|<n,\\
 \omega,&r=s,\ S\cup T=B,\\
 0,&r\ne s.
 \end{cases}                                               \tag{7}
\]

Products with overlapping supports are zero.  Thus `G` consists of three
Boolean branches, mutually annihilating away from the common unit, with
their three top elements identified to one socle.

## 3. An explicit quadratic strong Lefschetz element

Set

\[
 L=\sum_{v=1}^n\sum_{r=0}^2z_{\{v\},r},\qquad
 \Theta=\sum_{r=0}^2\sum_{u<v}z_{\{u,v\},r}.              \tag{8}
\]

The multiplication rules give the exact identity

\[
                              \Theta=\frac{L^2}{2}.         \tag{9}
\]

For `2j<n`,

\[
 \Theta^j=\frac{(2j)!}{2^j}
       \sum_{r=0}^2\sum_{|S|=2j}z_{S,r},                  \tag{10}
\]

whereas at the common socle

\[
                 \Theta^m=\frac{3(2m)!}{2^m}\,\omega\ne0. \tag{11}
\]

Now fix `1<=k<=m`.  On a branch `r`, multiplication by
`Theta^(m-k)`, after identifying a target `(n-k)`-set with its complementary
`k`-set, is a nonzero scalar times the disjointness matrix

\[
 K_{n,k}(R,S)={\bf1}_{R\cap S=\varnothing},
 \qquad |R|=|S|=k.                                        \tag{12}
\]

Its eigenvalues are

\[
 (-1)^j\binom{n-k-j}{k-j},
 \quad\text{with multiplicity }
 \binom nj-\binom n{j-1},\qquad 0\leq j\leq k.            \tag{13}
\]

Every eigenvalue is nonzero when `n>=2k`.  Hence each of the three branch
maps is invertible.  For `k=0`, (11) is the required nonzero map from the
unit to the one-dimensional socle.  This proves (1).

For completeness, the spectrum in (13) follows from the usual subset
filtration.  On functions of a `k`-set `S`, let `U_j` be spanned by the
indicators `1_(T subset S)` with `|T|=j`.  These spaces are nested and, for
`j<=k<=n/2`, their successive dimensions are
`binom(n,j)-binom(n,j-1)`.  If `K=K_(n,k)`, then

\[
 (K1_{T\subseteq -})(R)
 =\binom{n-k-j}{k-j}{\bf1}_{T\cap R=\varnothing}.
\]

Inclusion--exclusion writes the last indicator as
`sum_(J subseteq T)(-1)^|J| 1_(J subseteq R)`.  Modulo `U_(j-1)`, only
`J=T` remains.  Thus `K` acts on `U_j/U_(j-1)` by the scalar in (13),
with the asserted multiplicity; `U_k` is the full function space.  This
also proves invertibility without a genericity assumption.

Equivalently, one can obtain the invertibility in (13) from the usual
`sl_2` operators on the Boolean algebra: multiplication by
`sum_v z_v`, square-free differentiation, and their degree commutator.
Equation (12) is the matrix of the resulting hard-Lefschetz isomorphism.

The complete Jordan type of multiplication by `Theta` is therefore the
maximal type permitted by (6).  With `h_{-2}=h_{-1}=0`, it has

\[
 h_k-h_{k-2}\quad\text{blocks of length }m-k+1
 \quad(0\leq k\leq m).                                    \tag{14}
\]

Thus even a Jordan-type test tailored to a degree-two matching generator
passes as strongly as possible on the target apolar algebra.

## 4. Ordinary and higher Hessians also do not vanish

The linear form `L` is itself strong Lefschetz.  For `1<=k<=m`, the map

\[
 L^{n-2k}:G_k\longrightarrow G_{n-k}                       \tag{15}
\]

has, on each branch, the same disjointness matrix (12), multiplied by
`(n-2k)!`; for `k=0`, `L^n=3n! omega` is nonzero.  By the standard
apolar multiplication--higher-Hessian correspondence, every higher
Hessian determinant of `Delta_(n,3)` is therefore nonzero at the point
where all `3n` variables equal one.

The ordinary Hessian can be seen without any correspondence theorem.  At
that point it is block diagonal in the three colors, with each block equal
to `J_n-I_n`.  Hence

\[
 \det\operatorname {Hess}(\Delta_{n,3})(\mathbf1)
 =\left((-1)^{n-1}(n-1)\right)^3\ne0.                     \tag{16}
\]

## 5. Exact scope of the obstruction

The element `Theta` is of exactly the allowed support type: it is a sum of
same-color tensors on pairs of distinct sites.  Nevertheless, (11) lives
in the one-dimensional socle of the *apolar quotient*, where the three
full-color monomials have already been identified.  It therefore does not
give a source realization of (3).

This pinpoints the information loss.  Passing from a hypothetical source
`Q` to the intrinsic apolar algebra of its desired top tensor forgets both

* which degree-two class came from the source coefficients, and
* the three-dimensional span of the separate full-color tensors before the
  apolar socle identifies them.

Accordingly, a viable square-zero invariant must be a relative invariant of
the pair `(Q,Q^m)`, or use lower-support components of `exp(Q)`.  Any
criterion depending only on the Hilbert function, Lefschetz maps, higher
Hessians, or Jordan type of the target's apolar algebra is exhausted by the
counterexample above.

`computations/verify_zeon_lefschetz.py` independently builds the matrices
(12), checks full rank over a prime for every `n<=12`, verifies the Hilbert
and Jordan dimension identities, and checks (11) and (16) exactly.
