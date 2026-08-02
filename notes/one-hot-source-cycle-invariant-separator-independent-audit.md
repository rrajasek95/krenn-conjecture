# Independent audit of the full-source cycle separator

## Outcome

The separator in commit `09950e6` is sound in its stated scope.  It is a
regular invariant on the **full arbitrary \(3\times3\) endpoint-colour
source**, not merely a monomial identity on the one-hot support.  For a
mixed supported perfect matching \(M\),

\[
 I_M=H_{m(M)}Q_M,
 \qquad
 Q_M=\prod_{e\in E(G)\setminus M}a_e^{c(e)c(e)}          \tag{1}
\]

is invariant under the diagonal port torus

\[
 T_\Delta=\{(\lambda_{v,c}):\prod_v\lambda_{v,c}=1
                         \text{ for }c=0,1,2\}.          \tag{2}
\]

It has degree \(3n/2\), takes value one at the all-unit one-hot source and
along its normalized Laurent orbit, and vanishes on the exact GHZ fiber.
Consequently its value really separates the closed all-unit source orbit
from every exact source in the affine quotient by \(T_\Delta\).

The polystability statements are also correct.  The all-unit orbit is
closed, and a nonempty closed \(T_\Delta\)-invariant exact fiber contains a
closed orbit.  Polystability as a Boolean property therefore supplies no
separation by itself; the values of (1) do.

This is a statement for the port torus (2).  It is not, as written, an
invariant for a larger group containing colour permutations, nor is it a
quotient by all local general linear transformations.  It also does not
prove that the exact fiber is empty: its vanishing there uses one of the
defining mixed-output equations.

## 1. Character calculation on the full source

Let

\[
 W=\bigoplus_{u<v}\mathbb C^3_u\otimes\mathbb C^3_v,
 \qquad a_{uv}^{ij}\in W,
\]

with no sparsity or rank restriction.  For a word
\(m\in\{0,1,2\}^B\), every complete-graph perfect matching \(N\) contributes

\[
                         \prod_{uv\in N}a_{uv}^{m_um_v}   \tag{3}
\]

to \(H_m\).  Under \(A\mapsto\lambda A\), the factor incident to a vertex
\(v\) in (3) contributes \(\lambda_{v,m_v}\), independently of which vertex
is paired with \(v\).  Thus every monomial, including those using
off-diagonal coordinates \(a_{uv}^{ij}\) with \(i\ne j\), has the same
character

\[
                         \chi_m=\prod_v\lambda_{v,m_v}.  \tag{4}
\]

Now let \(G\) be properly three-edge-coloured and cubic, and let \(M\) have
colour word \(m(M)\).  At \(v\), \(Q_M\) contains the two supported edges
whose colours differ from \(m_v\).  Hence a term (3) of \(H_{m(M)}\), after
multiplication by \(Q_M\), uses each of the three ports
\((v,0),(v,1),(v,2)\) exactly once.  Its transformation factor is therefore

\[
             \prod_{v,c}\lambda_{v,c}
             =\prod_c\left(\prod_v\lambda_{v,c}\right)=1. \tag{5}
\]

This proves invariance term by term on all of \(W\); variables which vanish
on the one-hot chart have not been discarded.  Equivalently, \(Q_M\) has
the inverse of character (4) after restriction to (2).

The degrees follow only from incidence.  A cubic graph on \(n\) vertices
has \(3n/2\) edges, \(M\) has \(n/2\) edges, and its complement has \(n\)
edges.  Therefore

\[
                  \deg H_{m(M)}=n/2,\qquad
                  \deg Q_M=n,\qquad
                  \deg I_M=3n/2.                         \tag{6}
\]

## 2. Boundary and exact-fiber values

At the all-unit one-hot source \(A_*\), a supported colour word determines
its matching.  Indeed, at every vertex the requested colour selects the
unique incident edge of that colour.  Thus the only surviving term of
\(H_{m(M)}(A_*)\) is the term indexed by \(M\), and

\[
                         H_{m(M)}(A_*)=Q_M(A_*)=1.        \tag{7}
\]

For a normalized Laurent source, the complete support product has order
zero.  If the matching term has order \(d_M\), its complement has order
\(-d_M\), so \(I_M(A(t))=1\).  This is also forced by invariance because the
punctured Laurent family is a single \(T_\Delta\)-orbit of \(A_*\).

If \(A\) is in the exact GHZ fiber, every mixed output coordinate is zero.
The separator is chosen only for a mixed word, so

\[
                         H_{m(M)}(A)=0,\qquad I_M(A)=0.   \tag{8}
\]

Since (1) is regular and invariant, (7)--(8) imply

\[
       \pi_W(A_*)\notin\pi_W\bigl(H^{-1}(\Delta)\bigr)
                         \quad\text{in }W/\!/T_\Delta.  \tag{9}
\]

This refines, rather than contradicts, the earlier observation that the
normalized one-hot chart is one torus orbit.  Every invariant is constant
on that chart; the new invariant is the constant one there.  Equation (9)
compares that orbit with sources outside the chart which satisfy the exact
mixed equations.

## 3. Closed-orbit statements

The support product

\[
                         P_G=\prod_{e\in E(G)}a_e^{c(e)c(e)} \tag{10}
\]

contains every nonzero coordinate of \(A_*\) with exponent one.  Its port
incidence is one everywhere, so it is invariant by (5), and it is nonzero
at \(A_*\).  In character-lattice language, the supported weights obey the
strictly positive relation

\[
 \sum_{e\in E(G)}\operatorname{wt}(a_e^{c(e)c(e)})
                   =\sum_{v,c}e_{v,c}=0
                         \quad\text{in }X^*(T_\Delta).   \tag{11}
\]

The affine torus orbit criterion now makes \(T_\Delta A_*\) closed.  One
can also see this directly: invariance and nonvanishing of \(P_G\) prevent
an orbit-closure point from losing a supported coordinate, while inside the
support coordinate torus the orbit is a closed subtorus coset.

The exact fiber is closed and \(T_\Delta\)-invariant by equivariance of the
output map and the fact that (2) fixes \(\Delta\).  If it is nonempty, the
standard affine reductive-orbit theorem gives it a closed orbit (or choose
an orbit of minimum dimension and use the dimension drop in the boundary
of a nonclosed torus orbit).  This conditional statement does not assume
that the exact fiber exists.

## 4. Scope

The audit establishes precisely the following.

- The acting group is \(T_\Delta\), the diagonal port-torus component of
  the exact GHZ stabilizer.  A single \(I_M\) need not be fixed by additional
  finite colour permutations.
- The result concerns the affine source quotient \(W/\!/T_\Delta\).  It
  does not automatically transfer to a quotient by a different or larger
  source group.
- Proper three-edge-colouring and the presence of a mixed supported
  matching are essential to the displayed separator.
- The factor \(H_{m(M)}\) puts \(I_M\) in the ideal of the exact mixed
  equations.  A proof of nonexistence still needs independent source
  information which forces a conflicting nonzero value.

Within these labels, the primary theorem and its quotient and polystability
conclusions are correct.

## 5. Independent executable audit

The dependency-free checker
[audit_one_hot_source_cycle_invariant_separator_independent.py](../computations/audit_one_hot_source_cycle_invariant_separator_independent.py)
reconstructs the prism and six vertex-to-triangle expansions without
importing the primary checker.  It then:

- expands \(H_m\) over perfect matchings of the **complete** graph,
  exhaustively through \(n=12\) and on a deterministic 257-term sample at
  \(n=14,16,18\);
- constructs every full-source monomial with its endpoint-ordered colours,
  exercises off-diagonal \(a_{uv}^{ij}\), and checks its port character;
- performs exact dense-source equivariance tests with all nine endpoint
  coordinates nonzero through \(n=10\);
- verifies the degrees, one-hot value, Laurent order cancellation, and
  mixed-generator factorization; and
- checks the coefficient-one positive character relation certifying the
  closed source orbit.

The complete-graph term counts exhaustively checked per separator at
\(n=6,8,10,12\) are \(15,105,945,10395\).  Normal, optimized, isolated, and
no-site-library runs agree with digest

    8cf60dc8264744cc7a5ac903e628bba91e615845afda4372057497322632f482
