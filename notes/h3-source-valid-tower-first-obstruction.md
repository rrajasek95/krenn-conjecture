# First obstructions for a source-valid fourth Hasse–Schmidt tower

After
[`h3-descent-defect-row-space-invisibility.md`](h3-descent-defect-row-space-invisibility.md),
the only object that can still rescue the four-cube route is the one named
by the
[fourth-Hasse cone audit](h3-full-hasse-cone-d4-descent-obstruction.md):
a **source-valid fourth Hasse–Schmidt tower** — operators \(D_1,\dots,D_4\)
with \(D_n(xy)=\sum_{i+j=n}D_i(x)D_j(y)\) and \(D_n(I)\subseteq I\) for the
source ideal \(I=(H_m,\,H_0-u)\), \(m_8=01211222\).

This note proves three exact structural facts about any such tower.  The
first kills the four-cube template outright; the other two pin where any
replacement construction must get its mass.

Krenn's conjecture remains open.  Nothing here changes the certified
spine.

## T1.  The template is impossible

*(An earlier draft framed this as a "circularity"; an independent audit
showed that framing was false — \(1\in I\) can never hold — and the
corrected statement below is stronger.)*

Fix conventions: \(J=\{z_1,\dots,z_4\}\) is the four-direction set of
the fourth-Hasse audit (its (3)); \(I=(H_m,H_0-u)\) is its bounded
source ideal, \(u\) a variable; a tower is a multi-index Hasse–Schmidt
family with \(D_J=D_{z_1}\cdots D_{z_4}\) (disjoint singletons, binomial
factors one); source-valid means \(D_S(I)\subseteq I\) for every \(S\).
Weaker readings of "preserves every EqSystem equation" (preserving
\(\sqrt I\), or \(I:u^\infty\)) are noted below.

The four-cube template with tower \(D\) is

\[
 s^D=\sum_{S\subseteq J}D_S(A)\,r_0[J\setminus S]-B\,r_m[J],
\]

and its target — the \(r_0[\varnothing]\)-coefficient — is \(D_J(A)\),
**by definition of the template** (no verification needed; the checker's
anchor sweep only cross-references the coordinate case
\(\partial_JA=1\), which it recomputes from the base encoding: each
four-edge set of \(A\) lies in exactly one monomial).

Couple with the cap as \(n=s^D-\lambda T\).  Target zero forces
\(\lambda=D_J(A)\), and the boundary is \(\lambda Yw\).  Suppose \(D\)
is source-valid; then \(A\in I\) gives \(\lambda=D_J(A)\in I\).  Two
facts finish it:

1. Both generators of \(I\) are **weight-4 homogeneous** for
   \(\operatorname{wt}(\text{edge})=1\), \(\operatorname{wt}(u)=4\)
   (checked), so \(I\) contains no nonzero element of weight \(<4\).  In
   particular no nonzero rational lies in \(I\): \(\lambda\) cannot be a
   unit.
2. If instead \(\lambda\in I\) is accepted, the boundary
   \(\lambda Yw\in I\cdot Yw\) vanishes on the source quotient — the
   chain carries no descent information.

So **no source-valid tower admits an informative four-cube template**:
an unconditional impossibility.  There is no saturation escape either:
the checker verifies the witness point (all pure edges \(1\), mixed
edges \(0\), \(u=90\)) where \(H_m=0\) and \(H_0-u=0\) with
\(u=90\ne0\).  Hence \(V(I)\) is nonempty and meets \(\{u\ne0\}\):
neither \(1\in I\), nor \(u^k\in I\), nor \(1\in\sqrt I\) holds, and
the same conclusion follows under the weaker readings of
source-validity.  (Emptiness of this two-generator variety is *not* the
open case — that is the nine-row system; no conjecture-level equivalence
is claimed here.)

The transversality \(\Psi_J(H_m)=1\) of the coordinate tower is thus
necessary for an informative template and unattainable source-faithfully.

**Scope of T1.**  This kills the template shape \(s^D\) within the
smallest cone's cap coupling, not every chain in a prolonged complex.  A
general chain can instead carry unit \(r_0[\varnothing]\)-coefficient
directly and try to cancel the descent defect through the cascade of
higher-jet output equations.  That escape is not excluded here — T2
constrains it.

## T2.  The \(\varphi\)-filtration: source-validity first bites at order four

Let \(\varphi\) be the pure-colour specialization, and call an edge
variable **mixed** when its colour pair is not \((0,0)\) (the
\(\varphi\)-convention — *not* "two different colours").  Every edge
variable of every monomial of \(A\) is mixed: an edge covering site 0
(\(m_8\)'s only pure site) has colour pair \((0,m_s)\) with
\(m_s\ne0\), and an edge not covering site 0 has both endpoints
coloured \(1\) or \(2\).  Both cases are verified exhaustively, along
with squarefreeness of every monomial (four distinct edge variables),
on which the multilinear expansion below depends.
Consequently, for **any** Hasse–Schmidt tower whatsoever:

* \(\varphi(D_n(A))=0\) for \(n\le3\), automatically.  In the multilinear
  expansion \(D_n(M)=\sum_{n_1+\dots+n_4=n}\prod_iD_{n_i}(e_i)\), a total
  order below four forces some \(n_i=0\), and \(\varphi(D_0(e_i))
  =\varphi(e_i)=0\).  The \(\varphi\)-shadow of source-validity is
  vacuous through order three.
* At order four, exactly one distribution per monomial survives —
  \((1,1,1,1)\) — giving the exact identity

\[
 \varphi\bigl(D_4(A)\bigr)
   =\sum_{M\in A}\ \prod_{e\in M}\varphi\bigl(D_1(e)\bigr)
   =\operatorname{Haf}_A(\varphi\circ D_1).
\]

Source-validity (\(D_4(A)\in I\), so \(\varphi(D_4(A))\in(H_0-u)\))
therefore imposes its first nontrivial condition at order four, and it is
a hafnian condition on the order-one pure parts:

\[
 \boxed{\operatorname{Haf}_A(\varphi\circ D_1)\in(H_0-u).}
\]

This matches, and sharpens, the fourth-Hasse audit's finding that "the
first component capable of supporting the \(q\)-zero unit is the
order-four generator": the unit and the first source-validity constraint
live at the same order, and both are hafnians of order-one data.  The
proof is the displayed expansion; the checker's \(90\times35\) sweep is a
**consistency check of the composition bookkeeping** (its only
falsifiable content is that \((1,1,1,1)\) is the unique zero-free
composition of four into four parts), not an independent test.

The \(\varphi\)-filtration counts are: \(0,0,0,90\) surviving residuals at
\(|S|=1,2,3,4\) — only the ninety full matchings reach the pure sector.

## T3.  Constant-coefficient rigidity of the order-one faces

The 360 residual three-edge monomials \(M\setminus\{e\}\), over all
\((M,e)\) with \(M\in A\) and \(e\in M\), are pairwise distinct (a
residual determines its missing edge as the unique \(m_8\)-coloured edge
on the two uncovered sites, hence determines \(M\)).  Therefore

\[
 \sum_ec_e\,\partial_eA=0,\ c_e\in\mathbb Q,\ e\ \text{ranging over the
 edge variables occurring in }A
 \qquad\Longrightarrow\qquad c=0 :
\]

the syzygy space of the order-one faces starts in positive degree.  Any
tower component built from constant vector fields is either free of
relations or trivial; mass must enter through genuinely polynomial
coefficients, where the degree grading (assign \(u\) weight four) already
excludes membership of the degree-three derivatives \(\partial_eA\) in
\(I\).

## What remains after T1–T3

Within the smallest bounded cone, and modulo the companion note's scope
item 3 (rows with a \(\varphi\)-surviving edge-degree-0 boundary term
are not excluded), the four-cube route has one live shape: a prolonged
chain with unit \(r_0[\varnothing]\)-coefficient whose higher-jet output
cascade cancels the descent defect, built from a source-valid tower.  T2 says any
\(\varphi\)-visible mass such a cascade uses must enter at order four
through \(\operatorname{Haf}_A(\varphi\circ D_1)\), and T1 says the template's own
target coupling is unavailable.  Constructing such a chain — or
proving the cascade forces \(\varphi\)-triviality and hence closing the
route — is the sharp open question this note leaves.

## Scope

1. Finite, \(h=3\), direct-free, bounded model of the fourth-Hasse audit,
   word \(m_8=01211222\).
2. T1's argument is a proof given its inputs: the template's target is
   \(D_J(A)\) by definition; the weight-4 homogeneity of both
   generators and the witness point are machine-checked; source-validity
   is the strong ideal-preservation reading, with the weaker readings
   covered by the witness point.  T2's identity is proved by the
   displayed expansion (the sweep is bookkeeping); T3 by exhaustion over
   the 360 residuals.
3. Nothing here constructs a tower, decides the cascade question, or
   closes the route beyond the template.  Krenn's conjecture remains
   open.

## Verification

Run

~~~text
python3 computations/verify_h3_source_valid_tower_first_obstruction.py
python3 -O computations/verify_h3_source_valid_tower_first_obstruction.py
python3 -I computations/verify_h3_source_valid_tower_first_obstruction.py
python3 -S computations/verify_h3_source_valid_tower_first_obstruction.py
python3 -I -S computations/verify_h3_source_valid_tower_first_obstruction.py
~~~

Runtime is under one second.  The checker verifies that every \(A\)-edge
is mixed, the \(\varphi\)-filtration counts \((0,0,0,90)\), the composition bookkeeping over
all \(90\times35\) Hasse distributions, the vanishing of every
total-order-\(\le3\) distribution, the weight-4 homogeneity of both
generators of \(I\), the witness point on \(V(I)\cap\{u\ne0\}\), the
coordinate transversality \(\partial_JA=1\) recomputed from the base
encoding, and the pairwise distinctness of the 360 residuals.  Its frozen ledger digest is

~~~text
085191a1e2be1ed842fe80c71b38083e630c755fb0221e67b14a7c023845dbb5
~~~

Mutation-tested: perturbing the filtration table, purifying the word,
breaking the weight table, moving the witness point off the variety,
inverting the transversality check, breaking squarefreeness, and
inverting the residual-distinctness check each raise under both
`python3` and `python3 -O`, with a message naming the broken property.
