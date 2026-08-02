# The target stabilizer sees five independent missing face weights

Research reduction only.  This note does not construct the five face
homotopies, the shifted comparison map, a clean cap, or a proof of Krenn's
conjecture.

## 1. Outcome

For the direct-free reset word

\[
                         m=12112,
\]

the five denominator defects are the labelled four-face terms

\[
                         h_vY_0,
             \qquad v=1,\ldots,5.                       \tag{1}
\]

The full sitewise \(\mathfrak {sl}_3\) Casimir separates each such polar
from the old denominator tensor, but it is not compatible with the fixed
GHZ target.  The diagonal stabilizer of that target *is* compatible, and it
already gives a sharper grading statement: the five terms (1) have five
linearly independent stabilizer characters.  None is a character occurring
in the constant-coefficient, initial \(q\)-degree-two old denominator
image.

Consequently a target-compatible equivariant repair cannot be one scalar
cell.  It must contain at least five homogeneous weight components.  One
representation-valued generator may package them, but its weight support has
dimension at least five.  This recovers the five-component lower bound from
the universal denominator calculation without using monomial-support
separation and shows that the lower bound survives after restricting from
the full sitewise group to the true target stabilizer.

There is a tempting but invalid shortcut.  The Chevalley--Eilenberg **chain**
complex of an abelian Lie algebra is contractible on a nonzero-weight
one-dimensional module.  Applying that contraction here adjoins a ghost
\(H\otimes h_vY_0\) whose boundary is the polar.  A chain map sending that
ghost into the physical source resolution is exactly a Cartan/Spencer
homotopy for the polar weight.  Such a homotopy exists on the relevant
source subcomplex only if (1) is already a physical boundary.  Thus the
abelian weight contraction specifies the type of each missing \(\tau_v\);
it does not construct one.

This is useful pruning for the shifted principal-parts search.  Same-power
anchors and the old denominator block live in the wrong initial weights.
The only possible inputs are mixed full-source rows, a non-flat
specialization kernel, or new jet generators carrying the five characters
below.

## 2. The diagonal GHZ stabilizer

Let \(D=\{1,\ldots,5\}\), and let

\[
 T_\Delta=\left\{(t_{x,a})\in(\mathbb G_m)^{D\times\{0,1,2\}}:
              \prod_{x\in D}t_{x,a}=1\quad(a=0,1,2)\right\}.       \tag{2}
\]

It fixes \(\Delta_5=\sum_a e_a^{\otimes5}\) pointwise.  On its Lie algebra
write \(\lambda_{x,a}\) for the diagonal weights, so

\[
                         \sum_x\lambda_{x,a}=0
                         \quad(a=0,1,2).                \tag{3}
\]

Imposing in addition the five local trace-zero equations restricts (2) to
the diagonal stabilizer inside \(SL(3)^5\).  Every rank statement below is
unchanged by that restriction.  It is also unchanged when the five sites
are embedded in the full eight-site stabilizer by putting zero weights on
the other three sites.

For a four-site face \(F_v=D\setminus\{v\}\), the connection-module term

\[
 h_vY_0\longleftrightarrow
       \bigotimes_{x\in F_v}E_{0,m_x}                   \tag{4}
\]

has character

\[
 \chi_v(\lambda)=
       \sum_{x\ne v}(\lambda_{x,0}-\lambda_{x,m_x}).    \tag{5}
\]

If the exposed output factor \(e_0^{(v)}\) is retained, its literal
five-site character is \(\chi_v+\lambda_{v,0}\).  The proof below applies
to both families.

By contrast, every summand \(h_cY_c\) of the old four-site matching tensor
is weight zero in the connection representation.  Retaining an exposed
colour gives only the spectator characters \(\lambda_{v,a}\).  No character
in either family from (5) agrees modulo (3) with one of those old spectator
weights.

## 3. Independence of the five characters

Put

\[
 \delta_x=\epsilon_{x,0}-\epsilon_{x,m_x},\qquad
 X=\sum_x\delta_x.
\]

Then \(\chi_v=X-\delta_v\).  Suppose

\[
                         \sum_v a_v\chi_v=0
                         \quad\hbox{on }\operatorname {Lie}T_\Delta. \tag{6}
\]

Writing \(A=\sum_v a_v\), the character on the left is

\[
                         \sum_x(A-a_x)\delta_x.          \tag{7}
\]

A character vanishes on (3) exactly when its three coefficients at each
site are the same site-independent triple.  At a site with \(m_x=1\), the
local triple in (7) is

\[
                         (t,-t,0),
\]

whereas at a site with \(m_y=2\) it is

\[
                         (u,0,-u).
\]

The word \(12112\) contains both types.  Equality of the two triples forces
\(t=u=0\), and hence the common triple is zero.  Therefore
\(A-a_x=0\) at every site.  Summing gives \(A=5A\), so characteristic zero
forces \(A=0\) and then every \(a_x=0\).  This proves that the five
\(\chi_v\) are independent.

Adding the five exposed weights \(\lambda_{v,0}\) gives another rank-five
family.  One can prove this by the same local-triple comparison; the exact
checker performs the quotient-rank calculation directly.  The calculation
also verifies the rank after adding the local trace-zero equations and after
embedding in eight sites.

## 4. Why weight-space acyclicity is not the source homotopy

Let \(C_\bullet\) be a target-stabilizer-equivariant physical source
complex, and let \(z\) be one of the polar cycles of nonzero character
\(\chi\).  Choose \(H\in\operatorname {Lie}T_\Delta\) with
\(\chi(H)\ne0\).  In the auxiliary Lie-homology Koszul complex,

\[
       \partial(H\otimes z)=H\cdot z=\chi(H)z,          \tag{8}
\]

so that weight summand is contractible.

To turn (8) into a physical boundary one needs a map sending
\(H\otimes z\) to a chain \(s_Hz\in C\) with

\[
                         d(s_Hz)=H\cdot z.              \tag{9}
\]

But (9) implies \(\chi(H)[z]=0\) in physical homology and hence
\([z]=0\).  Conversely, providing (9) for (1) is precisely providing its
missing physical preimage.  The formal stabilizer ghost has therefore only
renamed \(\tau_v\).  There is no global Cartan homotopy
\([d,s_H]=L_H\) on the source resolution either: on degree-zero homology it
would force the torus action on the full source quotient to be trivial,
although that quotient has nonzero weight functions.

Thus the true stabilizer supplies a target-compatible grading and a sharp
five-weight lower bound, not the comparison differential itself.

## 5. Exact verification and scope

The dependency-free checker
[`verify_h3_ghz_stabilizer_face_weight_gate.py`](../computations/verify_h3_ghz_stabilizer_face_weight_gate.py)
computes character ranks over \(\mathbb Q\).  It checks the \(GL\) and
\(SL\) diagonal stabilizers on five sites and after embedding in eight
sites, verifies rank five for both the bare and exposed-output face
characters, and checks that no face character collides with an old
denominator spectator weight.

This note does not rule out one equivariant generator with a five-dimensional
weight decomposition, polynomial multipliers in higher degree, mixed
full-source syzygies, or specialization-created Tor.  It proves that a
scalar target-stabilizer Bockstein and the old initial denominator weights
cannot supply the five face homotopies.
