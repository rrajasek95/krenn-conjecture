# Independent audit of the full-sitewise \(\mathfrak{sl}_3\) face counterguard

Independent audit of commit `f946561`.  The counterguard is sound in its
stated fixed-face, internal-\(q\)-degree-two scope.  It does not construct a
four-face homotopy, exclude a non-equivariant full-source repair, or prove
Krenn's conjecture.

## Outcome

The five claims that matter are all correct.

1. The coefficient/output module has a literal basis identification

   \[
   \langle h_cY_d:c,d\in\{0,1,2\}^4\rangle
       \simeq \operatorname{End}(\mathbb Q^3)^{\otimes4},
   \qquad h_cY_d\longmapsto\bigotimes_x E_{d_xc_x}.       \tag{1}
   \]

2. The fixed-face denominator tensor is \(I^{\otimes4}\), hence sitewise
   trivial, whereas every desired mixed-to-pure polar is a simple tensor of
   four off-diagonal matrix units and lies in
   \(\operatorname{ad}^{\boxtimes4}\).
3. With trace-form normalization, the local adjoint Casimir eigenvalue is
   exactly 6 and the sum over four sites has eigenvalue 24 on every polar.
4. The CE contracting identity at degree zero has direction

   \[
                        h_{\rm CE}(d_{\rm CE}z)=z,         \tag{2}
   \]

   not \(z=d_{\rm CE}(\text{degree }-1\text{ cochain})\).  It therefore
   does not supply a source preimage.
5. The exact and projective infinitesimal stabilizers of the four-site
   ternary GHZ tensor inside \(\mathfrak{sl}_3^{\oplus4}\) coincide.  Both
   have dimension six and are abelian diagonal.

The independent checker verifies these statements without importing the
primary checker and without using its \(\mathfrak{gl}_3\) matrix-unit
shortcut for the Casimir.

## 1. Literal module and summand placement

For a four-letter coefficient word \(c\), its hafnian \(h_c\) contains the
three perfect-matching monomials on the face.  Their fine colour labels
recover \(c\), so supports belonging to two different words are disjoint.
The independent enumeration obtains 81 linearly independent coefficient
words and 243 distinct monomials.

Pairing those 81 coefficient words with the 81 output words gives 6561
basis pairs.  The map

\[
                   (c,d)\longmapsto((d_x,c_x))_{x=1}^4  \tag{3}
\]

is a checked bijection with the \(9^4=6561\) tensor matrix-unit bases of
\(\operatorname{End}(\mathbb Q^3)^{\otimes4}\).  Under (3),

\[
 \sum_c h_cY_c\longmapsto
 \sum_c\bigotimes_xE_{c_xc_x}=I^{\otimes4}.             \tag{4}
\]

For the five face words `2112`, `1112`, `1212`, `1212`, and `1211`, every
letter is 1 or 2.  Thus

\[
                   h_mY_0\longmapsto\bigotimes_xE_{0m_x} \tag{5}
\]

has four traceless off-diagonal factors.  It lies in the external tensor
product of the four local adjoint summands.  A local adjoint has no invariant
vector: the independently stacked equations \([B_i,X]=0\), with \(X\) in
an explicit traceless basis, have rank eight.  Hence already the first
sitewise factor gives

\[
       \operatorname{Hom}_{\mathfrak{sl}_3^{\oplus4}}
       (\mathbf1,\operatorname{ad}^{\boxtimes4})=0.      \tag{6}
\]

This confirms both the trivial placement of (4) and the nontrivial
external-product placement of (5).

## 2. Casimir normalization

Take the six off-diagonal matrix units together with

\[
 H_{01}=E_{00}-E_{11},\qquad H_{12}=E_{11}-E_{22}       \tag{7}
\]

as an explicit basis \((B_i)\) of \(\mathfrak{sl}_3\).  The audit forms the
Gram matrix \(G_{ij}=\operatorname{tr}(B_iB_j)\), inverts it over
\(\mathbb Q\), and computes

\[
 \Omega(X)=\sum_{i,j}(G^{-1})_{ij}[B_i,[B_j,X]].         \tag{8}
\]

On all nine matrix units the exact result is

\[
              \Omega(X)=6\left(X-\frac{\operatorname{tr}X}{3}I\right).
                                                               \tag{9}
\]

This independently validates the primary checker's observation that the
central \(\mathfrak{gl}_3\) direction can be added without affecting the
commutator action.  Applying the sum of (8) over four sites gives zero on
\(I^{\otimes4}\) and 24 times (5).  Thus the claimed eigenvalue is tied to
the stated trace-form normalization; no conventional Killing-form factor is
being suppressed.

## 3. The CE differential points the other way

Let \(z\) be one polar tensor and let
\(d_{m CE}z(X)=\rho(X)z\).  Using the same trace-dual basis as in (8), the
degree-one-to-degree-zero Casimir homotopy is

\[
 h_{\rm CE}(\phi)
   ={1\over24}\sum_{i,j}(G^{-1})_{ij}\rho(B_i)\phi(B_j), \tag{10}
\]

with a sum over the four direct-product factors.  Substituting
\(\phi=d_{m CE}z\) gives the total Casimir and hence (2).  The independent
sparse tensor calculation verifies this equality exactly and also verifies
that \(d_{m CE}z\ne0\).

But \(C^{-1}(\mathfrak g,V)=0\).  Therefore a zero-cochain is never a CE
boundary merely because the complex is contractible on its nontrivial
summand.  Formula (2) recovers \(z\) from its orbit derivative; it does not
write \(z\) as a CE differential, and it says still less about the distinct
physical denominator differential.  A Spencer/Rees construction would
have to add the jet or ghost on which (10) lands and then prove a typed chain
map into the full source complex.

## 4. Exact and projective GHZ stabilizers

For

\[
                         \Delta=\sum_{a=0}^2e_a^{\otimes4},          \tag{11}
\]

the exact action matrix has 32 columns and rank 26.  Its rational nullspace
has dimension six.  Every one of the 24 off-diagonal action columns is
independent, while the eight diagonal columns have rank two.  The nullspace
basis computed independently has zero coefficient on every off-diagonal
generator, and every pairwise Lie bracket between its six elements is zero.

The same dimension follows from diagonal parameters \(\lambda_{x,a}\).
There are twelve of them, subject to four sitewise trace equations and three
colour-sum equations.  These seven displayed equations have one dependency
and rank six, leaving a six-dimensional kernel.

There is no hidden infinitesimal projective scaling.  Appending \(-\Delta\)
as a possible scalar orbit direction raises the action rank from 26 to 27;
the augmented 33-column kernel still has dimension six, and its scalar
coordinate is identically zero.  Thus both exact stabilization and
stabilization of the GHZ line give the same abelian diagonal Lie algebra in
\(\mathfrak{sl}_3^{\oplus4}\).

## 5. Exact scope

The counterguard separates one fixed face's old internal degree-two
denominator line from its desired polar by a sitewise-equivariant direct
summand.  It soundly rules out manufacturing the polar by applying only
full-sitewise semisimplicity, a Casimir projector, or CE acyclicity to that
old face denominator representation.

It does not rule out:

- a source-provenant full-nine row involving other modules or degrees;
- a non-equivariant cross-word cancellation;
- a relation coupling different deletion faces;
- a specialization-created Tor/Rees transgression; or
- a Spencer construction equipped with a new generator and an actual chain
  map preserving target and ordinary residue.

The full \(\mathfrak{sl}_3^{\oplus4}\) action also does not preserve the
fixed GHZ target.  Restriction to its actual stabilizer removes the
semisimple Casimir mechanism because that stabilizer is abelian.  These are
scope restrictions of the proposed attack, not no-go statements for the
complete source complex.

The dependency-free checker
[`audit_h3_full_sl3_face_casimir_counterguard_independent.py`](../computations/audit_h3_full_sl3_face_casimir_counterguard_independent.py)
uses exact rational arithmetic.  Its frozen ledger digest is

```text
c69a488e752e02cb993978f06da7b44793a5eeb341bdc49a79cb03d8e915f1db
```
