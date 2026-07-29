# A one-slice covering lemma and forced rank-one incident edges

This note records a dense-support consequence of the diagonal target which
does not assume a cubic support graph.

## 1. One slice at every mode

Let (m\ge2), let (V_j=\mathbb C^3) with basis
(e_0,e_1,e_2), and suppose

\[
 \sum_{r=0}^2 c_r e_r^{\otimes m}
 =\sum_{j=1}^m x_j^{(j)}\otimes P_j,\qquad c_0c_1c_2\ne0,       \tag{1}
\]

where the (j)-th summand is a slice centered at mode (j).
Terms with (P_j=0) are to be omitted.

**One-slice covering lemma.**  For each (r\in\{0,1,2\}), at least one
nonzero term in (1) has (x_j\in\mathbb C^*e_r).

**Proof.**  For every retained term put

\[
 U_j=\{(\alpha(e_0),\alpha(e_1),\alpha(e_2)):
                    \alpha(x_j)=0\}\subseteq\mathbb C^3.
\]

This space has dimension at least two.  At a mode with no retained term set
(U_j=\mathbb C^3).  Contract (1) by arbitrary covectors represented by
(u_j\in U_j).  Every slice on the right vanishes, so

\[
 \sum_{r=0}^2c_r\prod_{j=1}^m u_{j,r}=0
 \quad\text{on }U_1\times\cdots\times U_m.                  \tag{2}
\]

Let \(\ell_{j,r}\in U_j^*\) be restriction of the (r)-th coordinate.
Equation (2) is the pure-tensor dependence

\[
 \sum_{r=0}^2 c_r
   \ell_{1,r}\otimes\cdots\otimes\ell_{m,r}=0.              \tag{3}
\]

We claim that each of its three displayed pure tensors is zero.  If exactly
two were nonzero, they would be proportional, so their two coordinate
functionals would be proportional in every mode.  The vanishing third pure
tensor supplies a mode where its coordinate functional is zero.  At that
mode all three coordinate restrictions would span dimension at most one,
contrary to the fact that the coordinate restrictions span
(U_j^*), whose dimension is at least two.

If all three pure tensors were nonzero, use the elementary classification
of a three-term dependence of decomposable tensors.  In a minimal such
dependence, all three factor vectors are proportional in every mode except
possibly one.  (Contract one mode by a functional killing one factor; the
remaining two pure tensors must be proportional in every other mode.)
At any one of the other modes, the three coordinate restrictions would
again span only one dimension, a contradiction.  A nonminimal dependence
reduces to the preceding two-term case.  One nonzero term is plainly
impossible.  Thus all three pure tensors in (3) vanish.

For each (r), therefore, some (j) has
(\ell_{j,r}=0), or (U_j\subseteq\{u:u_r=0\}).  Both spaces are
two-dimensional, so equality holds.  By annihilators this is precisely
(x_j\in\mathbb C^*e_r).  The corresponding term was retained, so
(P_j\ne0).  This proves the lemma. \(\square\)

## 2. Application to every star of a matching tensor

Assume now that (H_B(A)=\Delta_{B,3}), with (|B|\ge4), and fix a
vertex (p).  Put

\[
 C_{pj}=H_{B\setminus\{p,j\}}(A),\qquad
 L_{pj}(\lambda)=(\lambda\otimes\operatorname{id})A_{pj}.
\]

Contracting the star expansion at (p) by
(\lambda\in V_p^*) gives

\[
 \sum_{r=0}^2\lambda(e_r)e_r^{\otimes(B\setminus\{p\})}
 =\sum_{j\ne p}L_{pj}(\lambda)^{(j)}\otimes C_{pj}.          \tag{4}
\]

Take (\lambda) in the irreducible torus
(T=\{\lambda:\lambda(e_0)\lambda(e_1)\lambda(e_2)\ne0\}).
For a fixed color (r), the one-slice covering lemma says that (T) is
covered by the finitely many locally closed sets

\[
 S_{j,r}=\{\lambda\in T:
 C_{pj}\ne0,\ L_{pj}(\lambda)\in\mathbb C^*e_r\}.           \tag{5}
\]

One of these sets is Zariski dense in (T).  For that (j), every
non-(r) coordinate linear form of (L_{pj}) vanishes on a dense set and
hence identically, while its (r)-coordinate form is nonzero.  We obtain:

**Forced incident-edge theorem.**  For every ordered pair consisting of a
vertex (p) and a color (r), there is an active neighbor (j) and a
nonzero vector (a_{pj,r}\in V_p) such that

\[
 A_{pj}=a_{pj,r}\otimes e_r^{(j)},\qquad C_{pj}\ne0.         \tag{6}
\]

In particular, every vertex has at least three distinct active incident
matrices of rank one.  This conclusion keeps arbitrary endpoint asymmetry:
the factor (a_{pj,r}) has not yet been proved to be (e_r), or even a
coordinate vector.  Equivalently, the graph consisting of active rank-one
underlying matrices has minimum degree at least three.

One must not strengthen the density argument incorrectly.  The globally
coordinate-image maps obtained from the dense sets in (5) need only cover a
generic (\lambda).  On a zero hyperplane of their remaining linear form,
an edge map with larger image may land exceptionally in the missing
coordinate line.  Thus the common annihilator of the globally rank-one maps
can still meet (T).  Only when (p) has exactly three active neighbors
does the pointwise covering force every one of the three maps to be
nonvanishing on all of (T); the separate cubic-vertex lemma then upgrades
them to same-color coordinate tensors.  That stronger result is recorded in
`proofs/prism-plus-one-edge-obstruction.md`.

## 3. Current limitation

Equation (6) supplies rank-one coordinate anchors even in a complete
support, where the cubic-vertex argument itself says nothing.  It does not
yet force the opposite endpoint factor (a_{pj,r}) to be a coordinate
vector, and an edge selected by the theorem at one endpoint need not be
selected at the other endpoint.  A global proof still has to turn the
directed family (6), together with the exceptional axial loci in (5), into
cancellation rigidity.

## 4. Entry-minimal stars are linearly irredundant

There is one more exact condition available after choosing, among all
realizations of the same target, one with the fewest nonzero aggregate
matrix entries.  Fix (p), and for every active coordinate
(A_{pj}(k,l)\ne0) form its global contribution tensor

\[
 T_{pjkl}=e_k^{(p)}\otimes e_l^{(j)}\otimes C_{pj}.           \tag{7}
\]

**Local irredundancy lemma.**  The tensors (7), indexed by all nonzero
entries on edges incident to (p), are linearly independent.

**Proof.**  A linear dependence among them gives scalars
(d_{pjkl}), supported only on currently nonzero entries, such that changing
(A_{pj}(k,l)) to (A_{pj}(k,l)+t d_{pjkl}) leaves the star expansion,
and hence the entire matching tensor, unchanged for every (t).  Choose a
nonzero coefficient (d_{pjkl}) and set
(t=-A_{pj}(k,l)/d_{pjkl}).  This makes at least one existing entry zero,
creates no new nonzero entry, and contradicts entry-minimality. \(\square\)

This is stronger than saying every underlying edge is active, but it still
allows Koszul-type irredundant slice decompositions of a pure tensor.  A
successful use must combine (7) with the fact that each (C_{pj}) is itself
a smaller hafnian tensor; linear irredundancy alone does not collapse the
star to three terms.
