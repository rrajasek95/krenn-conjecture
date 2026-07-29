# Flat low-degree stars have a three-anchor transversal defect

## 1. Outcome

The centre-dark alternative in
[`canonical-transition-pencil-fan-dichotomy.md`](canonical-transition-pencil-fan-dichotomy.md)
leaves a centre with at most six nonzero aggregate blocks.  The forced
incident-edge theorem in [`slice-cover.md`](slice-cover.md) already gives
three distinct active neighbours \(a_0,a_1,a_2\) such that

\[
 A_{p a_c}=u_c^{(p)}\otimes e_c^{(a_c)},\qquad u_c\ne0,
 \qquad c=0,1,2.                                           \tag{1}
\]

This note gives a uniform, cancellation-safe description of everything
left at degrees four, five, and six.  Quotient the three anchor sites by
their displayed coordinate lines.  If \(r\) is any remaining neighbour,
write \(\bar C_r\) for the resulting quotient of its complementary
matching tensor

\[
                 C_r=H_{B\setminus\{p,r\}}(A).             \tag{2}
\]

Then the residual star has at most three terms and is literally zero:

\[
          \boxed{\quad
          \sum_{r\in R} A_{pr}^{(p,r)}\otimes\bar C_r=0,
          \qquad |R|\le3.\quad}                            \tag{3}
\]

For every \(r\in R\), let \(U_r\subseteq V_p\) be the centre-side image
of \(A_{pr}\), viewed as a map \(V_r^*\to V_p\).  The new point is that
(3) has an exact transversal alternative.

**Low-degree residual theorem.**  If the spaces \((U_r:r\in R)\) admit
linearly independent representatives, then

\[
                         \bar C_r=0\qquad(r\in R).          \tag{4}
\]

Consequently a degree-at-most-six star satisfies at least one of:

1. every residual cofactor belongs to the three-anchor partition kernel
   in (11) below;
2. two residual matrices have rank one and the same centre factor line;
3. there are three residual matrices and all three centre images lie in
   one common plane (so all three matrices have rank at most two).

There is no graph subcase enumeration.  The alternatives are the three
possible failures of the linear Hall--Rado criterion for at most three
subspaces of a three-space.

This is a real reduction, not a closure of the conjecture.  Alternative 3
is sharp already at the tensor level: the ordinary two-dimensional
Grassmann--Plücker identity gives three nonzero rank-two residual terms
through one common centre plane.  Thus the natural degree-six residue is a
matchgate plane, while alternative 1 is a three-slice cofactor kernel.  A
continuation must use the unquotiented target rows or overlap another
centre to eliminate these two structures.

## 2. The anchor quotient produces a short zero circuit

Assume

\[
                         H_B(A)=\Delta_{B,3}
                         =\sum_{c=0}^2e_c^{\otimes B}.      \tag{5}
\]

Fix \(p\in B\), and let \(N_p=\{j:A_{pj}\ne0\}\).  The star expansion is

\[
 \Delta_{B,3}=\sum_{j\in N_p}
       A_{pj}^{(p,j)}\otimes C_j,
 \qquad C_j=H_{B\setminus\{p,j\}}(A).                    \tag{6}
\]

Choose the three distinct active anchors in (1), supplied by the forced
incident-edge theorem.  Put

\[
 \pi_c:V_{a_c}\longrightarrow
       Q_c:=V_{a_c}/\mathbb C e_c,
 \qquad
 R=N_p\setminus\{a_0,a_1,a_2\}.                            \tag{7}
\]

Apply \(\pi_0\otimes\pi_1\otimes\pi_2\) at the three anchor
sites, and the identity at every other site, to (6).  The colour-\(c\)
target summand dies at \(a_c\).  The selected anchor term also dies at
that site because of (1).  What remains is exactly (3), where

\[
 \bar C_r=
  (\pi_0\otimes\pi_1\otimes\pi_2\otimes\operatorname{id})C_r.
                                                                    \tag{8}
\]

If \(|N_p|\le6\), then \(|R|\le3\).  Notice that (3) is obtained before
choosing a centre covector and before selecting a matching monomial.  It
therefore retains arbitrary endpoint matrices and complex cancellation.

## 3. The residual transversal lemma

We use an abstract tensor statement.  Let \(P,V_1,\ldots,V_k,W\) be
finite-dimensional vector spaces, with \(1\le k\le3\).  Suppose

\[
 A_i\in P\otimes V_i\setminus\{0\},\qquad
 C_i\in\bigotimes_{j\ne i}V_j\otimes W,
\]

and, after restoring the factors to the same order,

\[
                         \sum_{i=1}^k A_i\otimes C_i=0.     \tag{9}
\]

Let \(U_i\subseteq P\) be the image of the contraction map
\(V_i^*\to P\) defined by \(A_i\).

**Lemma 3.1 (transversal kills the residual cofactors).**  If there are
linearly independent vectors \(u_i\in U_i\), then every \(C_i=0\).

**Proof.**  Choose covectors \(\phi_i\in V_i^*\) and put
\(u_i(\phi_i)=(\operatorname{id}\otimes\phi_i)A_i\).  The wedge

\[
 u_1(\phi_1)\wedge\cdots\wedge u_k(\phi_k)                 \tag{10}
\]

is a polynomial in the \(\phi_i\), and by hypothesis it is not
identically zero.  Hence the tuples for which the displayed vectors are
independent form a nonempty Zariski-open set.

Contract (9) by arbitrary \(\phi_1,\ldots,\phi_k\) and by an arbitrary
covector on \(W\).  On that open set it becomes a linear combination of
the independent vectors \(u_i(\phi_i)\).  Its coefficient at \(u_i\) is
the corresponding contraction of \(C_i\); importantly, that coefficient
does not use \(\phi_i\).  Independence makes every coefficient zero on a
dense open set.  Each is a multilinear polynomial, so it vanishes
identically.  Varying all covectors separates tensors and gives
\(C_i=0\) for every \(i\).  \(\square\)

Apply Lemma 3.1 to (3), with \(P=V_p\) and with \(W\) containing the
three anchor quotient spaces and every non-residual site.  This proves
(4).

When (4) holds, exactness of tensor products over a field identifies its
meaning before quotienting:

\[
 \boxed{
 C_r\in
 \sum_{c=0}^2
 e_c^{(a_c)}\otimes
 \bigotimes_{v\in B\setminus\{p,r,a_c\}}V_v
 \qquad(r\in R).}                                         \tag{11}
\]

Thus each residual complementary matching tensor is covered by three
fixed one-site slices, one at each anchor and with the three different
target colours.  Equation (11), rather than termwise vanishing of
matchings, is the exact partition-kernel branch.

## 4. The only possible transversal defects

For completeness, recall the linear Hall--Rado criterion: subspaces
\(U_1,\ldots,U_k\) admit independent representatives if and only if

\[
       \dim\sum_{i\in I}U_i\ge |I|
       \qquad\text{for every }I\subseteq\{1,\ldots,k\}.     \tag{12}
\]

A short proof is by induction.  If a proper nonempty \(I\) has equality,
choose representatives inside its sum and apply induction in the quotient
to the remaining spaces.  If every proper inequality is strict, choose
any nonzero representative from the last space and quotient by its line;
all inequalities for the other spaces remain valid, so induction applies.

All \(U_i\) here are nonzero.  For \(k\le3\), failure of (12) is therefore
exactly one of:

\[
 \begin{array}{c|c}
 k&\text{failure}\ \\ \hline
 1&\text{none},\\
 2&U_1=U_2\text{ is one line},\\
 3&U_i=U_j\text{ is one line for some pair, or }
       \dim(U_1+U_2+U_3)\le2.
 \end{array}                                               \tag{13}
\]

Since tensor rank of \(A_i\in P\otimes V_i\) equals \(\dim U_i\),
(13) proves the three alternatives stated in Section 1.  More explicitly:

* at degree four, the one residual cofactor necessarily satisfies (11);
* at degree five, either both residual cofactors satisfy (11), or both
  residual blocks are rank one with one common centre factor;
* at degree six, either all three residual cofactors satisfy (11), two
  residual blocks share one rank-one centre factor, or all three residual
  blocks factor through one common centre plane.

The degree-five conclusion slightly sharpens the two-extra rank-one branch
in [`local-algebra.md`](local-algebra.md): the two rank-one matrices do not
merely have rank one; their factors at the common centre are proportional.

## 5. Sharp guards

None of the three residual structures can be rejected at the level of one
abstract star equation.

### 5.1 The partition-kernel branch

The four-site identity (1) in [`local-algebra.md`](local-algebra.md) adds
one nonzero extra slice to the three diagonal slices and cancels it through
one anchor slice.  Its extra cofactor is killed by the corresponding anchor
quotient.  Thus (11) is sharp even with a nonzero extra term.

### 5.2 The common-line branch

Let \(a\in V_p\), \(x\in V_r\), \(y\in V_s\), and \(Z\) be nonzero.
The two residual terms

\[
 (a\otimes x)_{pr}(y\otimes Z)_{sK}
 -(a\otimes y)_{ps}(x\otimes Z)_{rK}=0                  \tag{14}
\]

are the same tensor with opposite signs.  Both incident matrices are rank
one and share the centre factor \(a\).  Adding (14) to the three diagonal
anchor terms gives an exact five-port star decomposition.

### 5.3 The common-plane branch

Let \(H\) be two-dimensional with alternating bracket
\([u,v]=u_0v_1-u_1v_0\).  Put copies of \(H\) inside the centre and the
three residual local spaces.  Then

\[
 [p,x][y,z]-[p,y][x,z]+[p,z][x,y]=0                      \tag{15}
\]

identically.  The three incident pair forms in (15) all have rank two and
their centre images are the same plane \(H\); the three opposite cofactors
are nonzero.  Multiplying by an arbitrary tensor on all remaining sites
and adding the three diagonal anchor terms gives an exact six-port star
decomposition.  Hence the plane alternative is precisely a Plücker or
matchgate residue, not an artifact of the proof.

These guards are abstract star decompositions, not Krenn sources.  Their
role is exact: the next step must use the fact that the \(C_r\)'s in (2)
are overlapping matching tensors of one common source, or use the full
transverse target equations.  Repeating slice rank or quotienting only the
three anchors cannot close either (11) or (15).

## 6. Interface with the flat-fan branch

If every canonical transition at a good fan centre \(p\) vanishes, the
flat-fan theorem makes \(A_{pq}=0\) on the whole good fan.  For the
standard fan this leaves at most six exceptional neighbours, so the
present theorem applies verbatim.

The resulting uniform boundary is therefore:

\[
 \boxed{
 \begin{array}{c}
 \text{nonzero physical curvature (hence an active cap line), or}\\
 \text{a three-anchor cofactor kernel, a shared centre line, or a}\\
 \text{common rank-two centre plane on at most three residual ports.}
 \end{array}}                                               \tag{16}
\]

This does not yet turn the curved branch into a clean cap, and it does not
yet eliminate the flat branch.  It does remove arbitrary degree-four to
degree-six centre matrices from the latter: every survivor is now a short
partition/Segre circuit with one of the explicit geometries in (16).

The checker
[`verify_flat_fan_low_degree_residual_transversal.py`](../computations/verify_flat_fan_low_degree_residual_transversal.py)
audits the three-anchor quotient kernel, the common-line cancellation, the
Plücker guard, and the Hall--Rado alternatives on all subspaces of
\(\mathbb F_2^3\).  The proof of Lemma 3.1 is the characteristic-zero
multilinear argument above; the finite checker is only a structural audit.
