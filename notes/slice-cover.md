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

We claim that each of the three displayed pure tensors

\[
 T_r=\ell_{1,r}\otimes\cdots\otimes\ell_{m,r}                 \tag{3a}
\]

is zero.  Earlier drafts obtained this from a classification of three-term
dependences of decomposable tensors.  That classification is not needed:
the claim follows by evaluating (3) at finitely many explicitly chosen
points.  Two elementary facts are used.

**(K)**  At every mode the three restrictions
(\ell_{j,0},\ell_{j,1},\ell_{j,2}) span (U_j^*).  Restriction
((\mathbb C^3)^*\to U_j^*) is surjective and carries the three coordinate
functionals to them.  Since (\dim U_j^*\ge2), the three restrictions never
lie in one line.

**(A)**  Let (\ell,\ell') be functionals on (U_j) with (\ell\ne0).

* If (\ell'\notin\mathbb C\ell), some (u\in U_j) has (\ell(u)\ne0)
  and (\ell'(u)=0).  Otherwise (\ell) would vanish on (\ker\ell'),
  putting (\ell) in (\mathbb C\ell') and hence (\ell') in
  (\mathbb C\ell).
* If (\ell'\ne0), some (u\in U_j) has (\ell(u)\ne0) and
  (\ell'(u)\ne0), because a vector space is never the union of two
  proper subspaces.

Suppose (T_0\ne0), that is, (\ell_{j,0}\ne0) at every mode.  Write

\[
 F_s=\{j:\ell_{j,s}\notin\mathbb C\,\ell_{j,0}\}\qquad(s=1,2)
                                                             \tag{3b}
\]

for the modes at which color (s) is *free*.  Evaluating (3) at any point
(u\in U_1\times\cdots\times U_m) gives the scalar identity

\[
 c_0\prod_j\ell_{j,0}(u_j)+c_1\prod_j\ell_{j,1}(u_j)
 +c_2\prod_j\ell_{j,2}(u_j)=0.                               \tag{3c}
\]

*Two distinct free modes.*  Suppose (j_1\in F_1) and (j_2\in F_2) with
(j_1\ne j_2).  Use (A) to choose (u_{j_1}) with
(\ell_{j_1,0}(u_{j_1})\ne0) and (\ell_{j_1,1}(u_{j_1})=0), to choose
(u_{j_2}) with (\ell_{j_2,0}(u_{j_2})\ne0) and
(\ell_{j_2,2}(u_{j_2})=0), and at every remaining mode to choose (u_j)
with (\ell_{j,0}(u_j)\ne0).  The last two products in (3c) vanish and the
first does not, so (c_0=0), which is false.

*One common free mode.*  Suppose (F_1=F_2=\{j_0\}).  Because (m\ge2)
there is a mode (j\ne j_0), and there both (\ell_{j,1}) and
(\ell_{j,2}) lie in (\mathbb C\ell_{j,0}).  All three restrictions at
(j) then lie in one line, contrary to (K).

*A color with no free mode.*  Suppose (F_1=\varnothing), so
(\ell_{j,1}=\alpha_j\ell_{j,0}) at every mode; the case
(F_2=\varnothing) is the same with the two colors exchanged.  Put
(\alpha=\prod_j\alpha_j).  By (K) no mode may have both
(\ell_{j,1}) and (\ell_{j,2}) inside (\mathbb C\ell_{j,0}), so every
mode lies in (F_2) and in particular (\ell_{j,2}\ne0) everywhere.  Use
(A) to choose (u) with (\ell_{j,0}(u_j)\ne0) and
(\ell_{j,2}(u_j)\ne0) at every mode.  Then (3c) reads

\[
 (c_0+c_1\alpha)\prod_j\ell_{j,0}(u_j)
 +c_2\prod_j\ell_{j,2}(u_j)=0.                               \tag{3d}
\]

Now change one coordinate: at one mode (j_2) replace (u_{j_2}) by a
vector with (\ell_{j_2,0}\ne0) and (\ell_{j_2,2}=0), available by (A)
because (j_2\in F_2).  Since (F_1=\varnothing) still holds, (3c) at the
modified point again collapses to the shape (3d); there the second product
vanishes and the first does not, so (c_0+c_1\alpha=0).  Feeding that back
into (3d) at the original point gives (c_2\prod_j\ell_{j,2}(u_j)=0),
which is false.

The three cases are exhaustive: if no two distinct modes can be drawn from
(F_1) and (F_2) respectively, then either one of them is empty or both
equal the same singleton.  Hence (T_0=0), and the same argument with the
colors permuted gives (T_1=T_2=0).

This uses no genericity, no dimension count on a variety, and no
classification of decomposable dependences; each contradiction comes from
one explicitly constructed evaluation point.  It is also field-independent
— fact (A) holds over any field — which is what makes it exhaustively
testable.  `computations/verify_slice_cover_three_term_step.py` enumerates
every configuration of the displayed shape over (\mathbb F_2),
(\mathbb F_3), and (\mathbb F_5) for small (m), confirms the conclusion
of the **three-term step** — not of the covering lemma itself, which that
step is used to prove — and separately confirms that the case analysis above
always supplies the evaluation points it claims.  At (m=2) the first search
finds no identities at all, since three colors need three distinct modes, so
the sharp case is exercised only by the second.

For each (r), therefore, some (j) has
(\ell_{j,r}=0), or (U_j\subseteq\{u:u_r=0\}).  Both spaces are
two-dimensional, so equality holds.  By annihilators this is precisely
(x_j\in\mathbb C^*e_r).  The corresponding term was retained, so
(P_j\ne0).  This proves the lemma. \(\square\)

**Scope of the activity clause.**  The conclusion (P_j\ne0) — equivalently
(C_{pj}\ne0) in section 2 — is retained because other results depend on it,
notably `proofs/prism-plus-one-edge-obstruction.md`.  It is **not** used
inside `proofs/six-site-arbitrary-complex-obstruction.md`: section 3 there
needs only (d_R(v)\ge3), which follows from rank-one-ness together with
distinctness of the three witnesses.  So `SP-K6` would survive the weaker
statement; the stronger one is kept because it is free and other consumers
need it.

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
