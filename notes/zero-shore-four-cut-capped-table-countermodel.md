# The capped four-cut table has an exact twelve-port countermodel

## 1. Outcome

The induced-zero four-cut reduction produces, after capping every physical
site outside the union of the sparse row supports, a degree-eight tensor on
at most twenty-four ports.  The four row frames and that capped tensor obey
the same 81-entry diagonal response table as the original common-power
system.  This note records a sharp warning about that finite interface.

There is an exact twelve-port system in which

* every one of the twelve rows is supported at one physical site;
* its sole local component is on the required target coordinate axis;
* each of the four triples of rows is aggregate-injective; and
* all 81 four-row products give exactly the ternary diagonal table.

Thus injectivity, support at most two, coordinate anchors, and the complete
capped response table are jointly consistent.  A contradiction at this
frontier must use the fact that the capped degree-eight tensor is the
projection of **one common matching power**.  Treating that tensor as an
arbitrary four-hole response loses essential information.

The construction below is not a source for the original conjecture: no
quadratic whose common power produces the capped tensor is supplied.  In
fact Section 4 excludes the most literal attempted lift, a quadratic
supported on one fixed perfect matching of the twelve ports.  That narrow
no-lift statement does not exclude a general quadratic, cancellation among
many internal matchings, or a cap of a matching power on a larger set.

## 2. Twelve ports and four injective frames

Work over any characteristic-zero field.  Let

\[
 P=H_0\sqcup H_1\sqcup H_2,
 \qquad
 H_c=\{h_{c,0},h_{c,1},h_{c,2},h_{c,3}\}.
 \tag{1}
\]

At every port \(x\) take a local three-space with distinguished independent
vectors \(e_0^{(x)},e_1^{(x)},e_2^{(x)}\), and use the site-square-zero
algebra

\[
 {\cal R}_P=\bigotimes_{x\in P}
       \left(\mathbb C\oplus V_x\right),
 \qquad V_xV_x=0.                                      \tag{2}
\]

For the four ordered shore endpoints \(j=0,1,2,3\), define the oriented
row of colour \(c\) by

\[
                  p^{(j)}_c=e_c^{(h_{c,j})}.           \tag{3}
\]

No row at the opposite endpoint is identified with (3); the notation is
endpoint-oriented.  Every row has physical support one and its unique
component is a target-coordinate anchor.  For fixed \(j\), the three rows
occupy three distinct direct-summand sites \(h_{0,j},h_{1,j},h_{2,j}\).
They are therefore linearly independent in
\(\bigoplus_{x\in P}V_x\).  This proves aggregate injectivity of all four
frames without any genericity assumption.

For each colour put

\[
 E_c=\bigotimes_{x\in P\setminus H_c}e_c^{(x)}
       \in({\cal R}_P)_8,
 \qquad
                         \overline Q=E_0+E_1+E_2.       \tag{4}
\]

The tensor \(E_c\) has exactly the four holes \(H_c\).  It is important
that \(\overline Q\) is introduced as an arbitrary capped four-hole tensor,
not as a divided power.

## 3. The complete 81-entry calculation

For a colour tuple \({\bf c}=(c_0,c_1,c_2,c_3)\), the four row factors in

\[
              \left(\prod_{j=0}^3p^{(j)}_{c_j}\right)E_g          \tag{5}
\]

occupy the four distinct ports \(h_{c_j,j}\).  Multiplication by \(E_g\)
is nonzero precisely when every one of those ports is a hole of \(E_g\).
By (1),

\[
 \{h_{c_j,j}:0\le j\le3\}\subseteq H_g
       \quad\Longleftrightarrow\quad
 c_0=c_1=c_2=c_3=g.                                  \tag{6}
\]

There is consequently no termwise inference from a cancelling aggregate
here: (6) is a literal multiplication rule in the capped algebra.  Summing
the three sectors of (4) gives all 81 identities

\[
 \boxed{
 \left(\prod_{j=0}^3p^{(j)}_{c_j}\right)\overline Q
   =\delta_{c_0=c_1=c_2=c_3}
      \bigotimes_{x\in P}e_{c_0}^{(x)}.}
                                                               \tag{7}
\]

Every nonzero coefficient in (7) is exactly one.  Hence the example also
retains the normalization of the target, rather than only its support.
There are three nonzero rows and seventy-eight zero rows.

If the four named shore vertices are adjoined formally, their six mutual
aggregate blocks may all be set to zero.  Equation (7) is then exactly the
capped interface of the induced-zero four-cut equation.  It is not the
uncapped source equation until common-power provenance for \(\overline Q\)
has been established.

## 4. A precisely scoped no-lift lemma

The simplest possible lift of (4) would put a quadratic on six independent
physical pairs.

**Lemma 4.1 (no fixed-perfect-matching lift).**  Let \(M\) be a perfect
matching of \(P\), and let

\[
                     q=\sum_{e\in M}B_e,
 \qquad 0\ne B_e\in V_x\otimes V_y\quad(e=\{x,y\}).   \tag{8}
\]

Then \(q^{[4]}\ne\overline Q\).  The same conclusion holds if zero blocks
are initially allowed in (8).

**Proof.**  A nonzero sector of \(q^{[4]}\) uses four distinct edges of
\(M\); its four-hole set is the union of the two omitted edges.  Equality
with (4) would force each \(H_c\) to be the union of two edges of \(M\).
The three disjoint four-sets would therefore partition \(M\) into three
two-edge groups.

The coefficient at the hole set \(H_0\) is the tensor product of the four
blocks on the matching edges contained in \(H_1\cup H_2\).  Equality with
\(E_0\), a nonzero simple tensor whose local factors are all \(e_0\),
forces every one of those four two-site blocks to be a nonzero scalar
multiple of \(e_0\otimes e_0\).  This is the elementary uniqueness of
factors of a nonzero simple tensor, applied across the four disjoint edge
factors.

The coefficient at the hole set \(H_1\) similarly forces every block on
the edges in \(H_0\cup H_2\) to be a nonzero scalar multiple of
\(e_1\otimes e_1\).  An edge inside \(H_2\) is subject to both conclusions,
which is impossible because \(e_0,e_1\) are independent at both endpoints.
Thus no lift (8) exists.  If a block in (8) were zero, at least one of the
three required diagonal coefficients would already be zero, so allowing
zero blocks does not change the conclusion. \(\square\)

This lemma assumes literally that every nonzero block of \(q\) lies on one
fixed physical perfect matching.  In particular, each four-hole sector then
has only one physical matching support and cannot contain cancellation.
It says nothing about an arbitrary block graph, entangled sums within
cofactor sectors, or auxiliary sites removed by a cap.

## 5. Exact frontier

Let \(D\) be the complement of a four-vertex zero shore in the actual
source and let

\[
                         Q=q^{[m-4]}.                  \tag{9}
\]

If \(P\) is the union of the twelve sparse row supports (at most twenty-four
ports in the support-two case), capping \(D\setminus P\) sends \(Q\) to a
four-hole tensor \(\overline Q\) and preserves the full diagonal response
table.  The construction (1)--(7) proves that no theorem about an arbitrary
such \(\overline Q\) can close the route.

The missing condition is exact and physical:

\[
 \boxed{\overline Q\text{ must be one decomposable cap of the single
 common divided power }q^{[m-4]}.}                     \tag{10}
\]

A useful next lemma must propagate identities among the four-hole sectors
which follow from (10), for example common-power derivative or hafnian
cofactor recurrences.  It may not replace (10) by independent response
tensors, and it must allow arbitrary complex cancellation between the
matchings contributing to one sector.  Lemma 4.1 only disposes of the
independent-pair boundary of this provenance problem.

## 6. Exact audit

The standalone checker
[verify_zero_shore_four_cut_capped_table_countermodel.py](../computations/verify_zero_shore_four_cut_capped_table_countermodel.py)

* constructs the site-square-zero algebra on all twelve ports and checks
  every one of the 81 products in (7) over the integers;
* verifies support one, the coordinate anchor, and rank three for each of
  the four ordered row frames;
* confirms that the only nonzero response tuples are
  \((0,0,0,0),(1,1,1,1),(2,2,2,2)\), each with coefficient one; and
* enumerates all \(11!!=10395\) perfect matchings of the twelve ports,
  finds exactly \(3^3=27\) for which all three \(H_c\)'s are unions of
  matching edges, and verifies the incompatible pair of coordinate demands
  in Lemma 4.1 for every one of those 27 candidates.

The finite enumeration audits only the fixed-perfect-matching subcase.
The 81-row tensor calculation and the proof of the provenance frontier are
uniform statements in the displayed algebra.
