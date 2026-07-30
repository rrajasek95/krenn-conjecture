# Sparse-star propagation at the six-site rootless packet

## 1. Outcome

Work on the off-diagonal scalar-zero packet at the first boundary, so the
residual set \(W\) has six sites and

\[
 r q^{[2]}=-\alpha\Delta_{6,3},\qquad r^{[3]}\ne0,
 \qquad r=\sum_{i,j}K_{ij}p_i s_j.                    \tag{1}
\]

Here \(K\) is invertible.  The two sparse alternatives in the good-star
selector lemma behave differently.

1. If either endpoint star is supported on at most two residual sites,
   then \(r^{[3]}=0\).  Thus type 2 is excluded immediately by the
   rootless condition; neither the response equation nor the other
   endpoint is needed.
2. If the restriction of one endpoint star away from an exceptional site
   \(x\) has rank at most one, then, after a change of row basis and
   absorbing \(K\) into the other star,

   \[
                    r=LM+E_x,                         \tag{2}
   \]

   where \(L,M\) are supported on the five sites \(W\setminus\{x\}\) and
   every edge of \(E_x\) contains \(x\).  At six residual sites this gives
   the exact factorization

   \[
                    r^{[3]}=E_x(LM)^{[2]}.             \tag{3}
   \]

   In particular every top matching in the clean error uses exactly one
   exceptional edge and two edges from one decomposable shore channel.

The last normal form is not itself contradictory.  A six-site packet is
given below with both endpoint stars injective, an invertible cap matrix,
an exact scalar-zero physical response, and \(r^{[3]}\ne0\), while one
endpoint has precisely the rank-one-away-from-\(x\) form.  Its target is
unary and it does not satisfy the other eight pair rows.  Thus the
remaining type-3 proof has to use the full ternary diagonal of the
canonical scalar-zero cap or couple the omitted pair rows; injectivity of
the opposite endpoint and nonnilpotence alone do not close it.

## 2. Two-site support is incompatible with rootlessness

Let the \(p\)-star be supported on \(S\subseteq W\), with

\[
                              |S|\le2.                 \tag{4}
\]

Every nonzero decorated edge occurring in

\[
                         r=\sum_{i,j}K_{ij}p_i s_j     \tag{5}
\]

has a \(p\)-endpoint in \(S\).  A monomial in \(r^{[3]}\) is a matching of
three such edges.  Its three \(p\)-endpoints must be three distinct
physical sites, since the site-square-zero relations kill every collision.
This is impossible when \(|S|\le2\).  Hence

\[
                              r^{[3]}=0.                \tag{6}
\]

This contradicts the second equation in (1).  The same argument applies
with the two endpoint stars interchanged.  More generally, on \(2h\)
residual sites, support on at most \(h-1\) sites kills \(r^{[h]}\).

## 3. Normal form for the rank-one exceptional shore

Suppose instead that the restriction of the \(p\)-star to
\(W\setminus\{x\}\) has rank at most one.  Choose a basis of its
three-dimensional row domain in which

\[
 p_0=L+\ell_x,\qquad p_1,p_2\in V_x,                  \tag{7}
\]

with \(L\) supported off \(x\).  Since \(K\) is invertible, absorb it and
the dual row-basis change into the other endpoint triple and write

\[
                         r=\sum_{i=0}^2p_i t_i.        \tag{8}
\]

Split \(t_0=M+m_x\) into its off-\(x\) and at-\(x\) parts.  The only term
of (8) not incident with \(x\) is \(LM\).  All remaining terms can be
collected into an exceptional star quadratic \(E_x\), proving (2).

Put \(Q=LM\).  Every edge of \(E_x\) contains \(x\), so

\[
                         E_x^{[2]}=0.                  \tag{9}
\]

The quadratic \(Q\) is supported on only the five sites
\(W\setminus\{x\}\).  A third matching power requires six distinct sites,
and therefore

\[
                           Q^{[3]}=0.                  \tag{10}
\]

The divided-power binomial expansion now gives

\[
 (Q+E_x)^{[3]}
   =Q^{[3]}+E_xQ^{[2]}+E_x^{[2]}Q+E_x^{[3]}
   =E_xQ^{[2]},                                        \tag{11}
\]

which is (3).  Consequently rootlessness forces both
\(E_x\ne0\) and \((LM)^{[2]}\ne0\).  In particular the exceptional site
must occur in every surviving top matching of the scalar-zero clean
error.  This is the exact incidence statement that a coupling argument
may export to an overlapping cap chart.

The five-site support in (10) is essential.  Formula (3) is a
first-boundary statement; on six or more sites off \(x\), a decomposable
quadratic \(LM\) can have a nonzero third matching power.

## 4. A smallest physical-row guard for type 3

Let \(W=\{0,1,2,3,4,5\}\), take \(x=0\), and write \(z_{ic}\) for colour
\(c\) at site \(i\).  Products containing two variables at one site are
zero.  Define the first endpoint rows

\[
 p_0=z_{10}+z_{20},\qquad p_1=z_{00},\qquad p_2=z_{01}, \tag{12}
\]

and transformed second-endpoint rows

\[
 t_0=z_{30}+z_{40},\qquad
 t_1={1\over6}z_{50},\qquad
 t_2=z_{02}.                                           \tag{13}
\]

Both triples define injective star maps.  The restriction of the first
triple away from site \(0\) has rank one.  Choose the invertible physical
cap covector

\[
 K=\begin{pmatrix}1&0&0\\0&0&1\\0&1&0\end{pmatrix}, \qquad
 \det K=-1,\qquad \operatorname{diag}K=(1,0,0),        \tag{14}
\]

and define the original second star by \(t=Ks\).  It is injective because
\(K\) is invertible.  With direct block orthogonal to \(K\) (for example
the zero direct block), this is a scalar-zero cap row.  Its response
quadratic is

\[
\begin{aligned}
 r&=\sum_i p_i t_i\\
  &=(z_{10}+z_{20})(z_{30}+z_{40})
       +{1\over6}z_{00}z_{50},                         \tag{15}
\end{aligned}
\]

because \(p_2t_2=z_{01}z_{02}=0\) is a same-site collision.  Set the
internal quadratic \(q=r\).  If

\[
 Q=(z_{10}+z_{20})(z_{30}+z_{40}),\qquad
 E={1\over6}z_{00}z_{50},                              \tag{16}
\]

then

\[
 Q^{[2]}=2z_{10}z_{20}z_{30}z_{40},\qquad
 r^{[3]}=EQ^{[2]}={1\over3}X_0.                        \tag{17}
\]

Therefore the complete contracted physical row is exact:

\[
                  r q^{[2]}=r r^{[2]}=3r^{[3]}=X_0
                           =T(K).                      \tag{18}
\]

This guard retains all of the following simultaneously:

* an invertible scalar-zero cap matrix;
* injective stars at both endpoints;
* the type-3 exceptional-shore form at one endpoint;
* a literal top-tensor response with no unwanted words; and
* nonzero scalar-zero clean error \(r^{[3]}\).

It is not a Krenn source.  In particular (18) is only the \(K\)-contracted
row and the diagonal of \(K\) is unary, whereas the off-diagonal canonical
scalar-zero cap has three nonzero diagonal entries and the complete nine
pair equations.  The guard proves that neither opposite-star injectivity
nor the matching-power condition can replace those missing physical rows.

## 5. Remaining positive target

After the type-2 closure, the sparse branch of the rootless packet is
reduced to one bounded statement.  In the normal form

\[
 r=LM+E_x,\qquad r^{[3]}=E_x(LM)^{[2]},                \tag{19}
\]

use either

\[
 r q^{[2]}=-\alpha(X_0+X_1+X_2)                       \tag{20}
\]

together with the other eight pair rows, or an overlapping canonical
chart, to force \(E_x(LM)^{[2]}=0\) or a registered one-neighbour/low-degree
star.  Equation (19) says exactly where to contract: every clean-error
coordinate has one leg at \(x\), while its remaining four legs lie in the
second divided power of a single decomposable quadratic.  A proof that
uses only one contracted lower-palette row cannot work, by (12)--(18).

This closes the two-site sparse alternative and replaces the other sparse
alternative by a single exceptional-edge/decomposable-shore coupling
problem; no support enumeration is involved.
