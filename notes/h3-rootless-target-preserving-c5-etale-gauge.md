# A target-preserving étale C5 gauge removes the selected pure-Eq defects

## Outcome

Let

\[
 (a,b,c,d,e)=
 (q_{12}^{12},q_{23}^{21},q_{34}^{11},
       q_{45}^{12},q_{15}^{12})
\]

be a nonzero selected cycle in the rootless \(m=12112\) packet. On its
Laurent torus there is an explicit degree-two finite étale cover and a
site-colour diagonal gauge which

1. fixes all three normalized GHZ target coefficients;
2. sends \(a,b,c,d,e\) identically to \(1\);
3. fixes the marked colour-zero cells \(u_v=a_{xv}^{00}\) and
   \(t=a_{pq}^{00}\);
4. preserves zero target, \(W\), ordinary residue, fine labels, support,
   activity, and goodness; and
5. commutes with the non-Euler colour-zero stabilizer jets.

Consequently all five selected-monomial defects

\[
                 (a-b,c-d,e-a,b-c,d-e)(H_0-u)e_{\rm Eq}
\]

vanish identically on the normalized slice. They are not a
target-preserving gauge invariant.

This does not yet construct the collision edges on the general
selected-cycle chart. After normalization the full four-site companions
have the form

\[
                             h_v'=1+R_v,               \tag{1}
\]

where \(R_v\) is the sum of the two off-cycle matching terms. The physical
edge between adjacent faces has remaining response boundary

\[
                              R_v-R_w.                 \tag{2}
\]

Thus the exact C5 specialization \(R_1=\cdots=R_5=0\) has clean physical
zero-anchor edges and the usual degree-five compatibility. In the general
chart the proof gate is no longer a reduced pure-Eq face; it is
source-faithful cancellation or descent of (2).

The result reframes, but does not contradict, the universal polynomial
obstruction of commit 9fd0de3. That theorem excludes a homogeneous
polynomial correction in the original coordinates. The present result uses
the target-stabilizer orbit and a finite étale local slice. It constructs no
primitive anchor cell.

The local construction genuinely descends through the quadratic cover. Its
deck transformation is an exact finite target-stabilizer element which
fixes every internal \(m\)-decorated cell, every ordinary-residue companion,
and the marked zero-colour cells. No site-Euler homotopy is needed. This is
algebraic descent on the chosen nonzero C5 chart, not a proof that these
charts cover every rootless packet.

## 1. Explicit normalization

Let \(z_i\) scale the selected colour axis \(m_i\) at odd site \(i\). The
five normalization equations are

\[
 a z_1z_2=b z_2z_3=c z_3z_4=d z_4z_5=e z_5z_1=1.     \tag{3}
\]

The unsigned vertex-edge incidence matrix of \(C_5\) has determinant \(2\).
Adjoin

\[
                         s^2={bd\over ace}.             \tag{4}
\]

Then one solution is

\[
\begin{aligned}
 z_1&=s,&
 z_2&=a^{-1}s^{-1},&
 z_3&=ab^{-1}s,\\
 z_4&=ba^{-1}c^{-1}s^{-1},&
 z_5&=acb^{-1}d^{-1}s.
\end{aligned}                                          \tag{5}
\]

Substitution verifies (3), including the final equation by (4). Since
\(s\) is a unit and the derivative of (4) with respect to \(s\) is \(2s\),
the cover is finite étale in characteristic zero. Its deck involution sends
all \(z_i\) to \(-z_i\).

Set every unlisted local-axis scale equal to one. To preserve the target,
use the external site \(x=0\) for the two corrections

\[
 t_{0,1}=\left(\prod_{i=1}^5t_{i,1}\right)^{-1},
 \qquad
 t_{0,2}=\left(\prod_{i=1}^5t_{i,2}\right)^{-1},
 \qquad t_{0,0}=1.                                    \tag{6}
\]

Leave sites \(p,q=6,7\) unchanged. For each colour \(c\),

\[
                         \prod_{i=0}^7t_{i,c}=1,       \tag{7}
\]

so the local diagonal action fixes
\(\Delta_{8,3}=\sum_c e_c^{\otimes8}\) coefficientwise. It is an exact
target stabilizer, not a projective rescaling.

## 2. Physical typing

The action is diagonal and never changes a site, colour, or matching label.
It therefore preserves the fine grading and every support-defined
activity/goodness condition. Since it fixes the target, the complete
full-nine equations are carried isomorphically to themselves. Zero target,
\(W\), and ordinary-residue readouts stay zero; a nonzero character merely
rescales their labelled rows.

More explicitly, every \(m\)-decorated matching \(N\) on
\(F_v=D\setminus\{v\}\) has the same character

\[
                          \prod_{i\ne v}z_i,            \tag{8}
\]

independently of its route. Hence all three ordinary-residue companions for
one \(v\) are rescaled together. The non-Euler weights are supported only
on colour zero, whereas every selected cycle endpoint has colour one or
two. Their first vector fields and mixed correction have zero component in
all five normalized coordinates. The target torus is abelian, so it
commutes with those jets. Finally every colour-zero scale in the explicit
gauge is one, so \(u_v,t\) themselves are fixed and their marked
normalization remains coefficient one.

This also answers the possible connection objection for the required
mixed jet: it is tangent to the slice. Fibrewise, one first chooses the
target-preserving gauge at the given source and then transports the entire
literal source/Hasse complex by that fixed diagonal automorphism. No
source-labelled derivative or endpoint order is discarded.

### Étale transition and descent

Changing \(s\) to \(-s\) changes every \(z_i\) in (5) by \(-1\). To retain
the target correction (6), the deck element also multiplies the external
axis \((0,1)\) by \(-1\); its \((0,2)\) axis is unchanged because the word
\(12112\) has three colour-one and two colour-two sites. Thus the nontrivial
deck transformation is

\[
 g_{i,m_i}=-1\ (i=1,\ldots,5),\qquad g_{0,1}=-1,
 \qquad g=1\text{ on every other axis}.                \tag{9}
\]

For each colour, the product of its eight signs is one, so (9) fixes the
GHZ target exactly. Every internal \(m\)-decorated edge has two \(-1\)
endpoints and is fixed. Hence \(q_m\), all \(R_v\), all fifteen response
companions, and the normalized PP subcomplex are literally deck-invariant.
The marked \(u_v,t\) cells are also fixed.

Faithfully flat Galois descent therefore carries a physical PP edge
constructed on the normalized cover back to the selected-cycle chart. This
does not require choosing a branch of \(s\) in the base ring. The
site-Euler homotopy of commit 8423678 is neither necessary nor applicable:
at an odd site (9) changes one colour axis and fixes the other two, whereas
a site-Euler gauge scales all three axes equally. Treating (9) as a
site-Euler boundary would also reintroduce the anchor--ordinary-residue
conservation that the non-Euler construction was designed to avoid.

This proves local algebraic descent, not global chart-cover. A separate
source theorem must still select a nonzero C5 in every relevant packet or
route its complement.

## 3. What happens to the PP edges

For each face \(F_v\), exactly one of its three perfect matchings uses only
cycle edges. On the slice its monomial is \(1\), so (1) holds. In the
physical PP edge between adjacent faces, the two selected missing
multipliers are also \(1\). Therefore its pure-Eq defect is literally

\[
                            (1-1)(H_0-u)e_{\rm Eq}=0.  \tag{10}
\]

The companion boundary is not automatically zero:

\[
                    h_v'-h_w'=(1+R_v)-(1+R_w)=R_v-R_w.
\]

On the exact C5 specialization every off-cycle \(m\)-decorated cell
vanishes, so every \(R_v=0\). The five PP edges are then physical
zero-anchor edges and their oriented boundary is the standard \(C_5\)
incidence. The degree-five top is its usual signed cellular compatibility.

On the general selected-cycle torus, (2) is the precise residual. A proof
must show that the complete common-\(q\) response/Hasse module cancels these
five tail differences, or that any nonzero tail routes to an already
certified clean/active landing. The reduced pure-Eq generator isolated by
commit 9fd0de3 is unnecessary on this slice, but the tail comparison remains
unproved.

## 4. Relation to Theorem A

The tails \(R_v-R_w\) are not yet literal instances of Theorem A's typed
common-tail C4 edge. Each summand of \(R_v\) is a two-edge internal matching
on \(F_v\); after the missing-edge multiplication it is a repeated-site
three-edge monomial. Adjacent faces generally have unequal physical tails,
and the complete PP coefficient provides no endpoint-star column or common
decorated complement identifying them.

They are naturally inputs to the same source-exhaustivity mechanism:
expand (2) into labelled matching occurrences, join equal-tail typed
switches, and route a first unequal tail to a nonflat carrier or Hall
incidence. But the present Theorem A starts from a synchronized one-bad
endpoint packet and assumes precisely that typed endpoint attachment. No
committed theorem supplies it for these internal rootless companions.
Therefore the remaining B comparison may eventually be discharged by a
shared connectivity theorem, but it is not currently reduced to Theorem A.
The exact missing bridge is a source-labelled attachment of each nonzero
\(R_v-R_w\) occurrence to a complete endpoint-star column with the same
decorated tail.

## 5. The tempting common-vertex shear

The sign in the suggested algebraic redefinition is correct:

\[
 r_i'=r_i+(H_0-u)e_{\rm Eq}
 \quad\Longrightarrow\quad
 a r_i'-b r_j'
 =a r_i-b r_j+(a-b)(H_0-u)e_{\rm Eq}.                 \tag{11}
\]

Equation (11) is not by itself a physical polar completion. It shears the
fixed ridge output coordinate by a pure Eq row and therefore changes the
terminal embedding; it is not a new source chain with zero readouts. The
étale normalization avoids this identification: it kills the coefficient
in (10) inside a target-preserving physical frame and leaves the ridge
coordinates untouched.

## Verification and scope

Run

~~~~text
python3 computations/verify_h3_rootless_target_preserving_c5_etale_gauge.py
python3 -O computations/verify_h3_rootless_target_preserving_c5_etale_gauge.py
python3 -I -S computations/verify_h3_rootless_target_preserving_c5_etale_gauge.py
~~~~

The checker pins the zero-anchor collision obstruction, both the non-Euler
physical jet and the site-Euler conservation theorem, the denominator PP
module, and the pentagon interface. It
verifies the unsigned determinant, the Laurent formulas (4)-(5), all five
normalized edges, all three exact GHZ characters, the fifteen uniform
ordinary-residue route characters, the explicit deck descent, non-Euler
slice tangency, the five vanishing pure-Eq defects, and the \(1+R_v\)
decomposition.

This is a characteristic-zero target-stabilizer slice theorem on the
selected nonzero C5. It proves clean physical edges on the exact C5
specialization. It does not cancel the general residual tails (2), descend
a global polynomial identity without the étale gauge, or construct the
primitive anchor.

Frozen ledger SHA-256:

~~~~text
f72555e82171a2dbc6196e8705a2cf1d0077dcad5301090f212d82bdc146fdb8
~~~~
