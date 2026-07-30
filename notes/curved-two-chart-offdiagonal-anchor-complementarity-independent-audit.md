# Independent audit: two-chart off-diagonal/anchor complementarity

## 1. Verdict

The concrete algebra in
[`curved-two-chart-offdiagonal-anchor-complementarity.md`](curved-two-chart-offdiagonal-anchor-complementarity.md)
passes an independent exact audit.  Direct matching enumeration over
\(\mathbb Q\), starting from the two displayed literal cell tables rather
than from the claimed chart formulas, confirms all of the following.

* The first complementary packet has zero global matching tensor.  In both
  the \(pq\)- and \(pr\)-charts all six off-diagonal rows therefore hold,
  while exactly the three diagonal target anchors fail.
* The endpoint-degenerate packet has global matching tensor exactly \(X_0\).
  In both charts all six off-diagonal rows and the complete physical
  \(E_{00}\) row hold, while exactly the \(X_1,X_2\) diagonal anchors fail.
* All four endpoint-star triples have rank three for each packet, the two
  advertised endpoints are clean in each chart, and the curvature values
  are respectively \(-18\) and \(-72\).
* The second packet really has \(q^{[2]}\ne0\) in both charts.  Its second
  Omega column is exactly zero and its first is nonzero.  The first packet's
  two Omega columns have exactly the displayed coefficients and are
  independent in both charts.
* The diagonal-row dependency packet also passes: it has exactly the nine
  claimed global words, the three diagonal rows, the six single-word
  off-diagonal failures, curvature \(1\), clean endpoints, four injective
  stars, and the two displayed independent Omega pairs.

There is no coefficient, sign, divided-power, endpoint-order, or rank error
in these claims.  The source verifier passes, but the audit below goes beyond
it by tying curvature to the literal cell tables and checking every displayed
Omega coefficient rather than only the zero/nonzero/proportionality type.

The proposed identification with a cross-word Riccati/Koszul \(H^1\) class
does **not** have the same status.  The six-cycle, literal overlap connection,
curvature coefficient, target-row gauge law, and separate Riccati--leakage
identity are exact.  No complex, comparison map, or injectivity theorem
identifying the Omega obstruction with a cross-word \(H^1\) class is supplied.
That identification is a well-motivated analogy and a proposed next lemma,
not a proved structural theorem.

Two presentational defects do not affect the computations: equations (51)
and (53) in the primary note lack display-math delimiters, and the schematic
``corresponding transition'' in (58) must mean the transition normalized by
\(1/3\).  If it means the raw transition of the Bianchi-connection note, a
factor \(1/3\) is missing.

The audited versions had SHA-256 hashes

```text
41706ebd33e6164b7bbc769b620f7bee7629ce40d975334d5a263e36a046548e  notes/curved-two-chart-offdiagonal-anchor-complementarity.md
8b15ae2c610d64788bb3e21ae322e5a140e7b258b7bcd11490fbe15bd8543aae  computations/verify_curved_two_chart_anchor_complementarity.py
715148e06499a9bddebf0985fb490423fe0b93cd8a9928a40840ce621b6e1f4a  notes/curved-two-chart-omega-diagonal-row-guard.md
40b5b8ae9172ce6879c9541499c4a4f5914d6aa6cc3521e9b85bb3f1c3100935  notes/overlapping-pair-cap-bianchi-connection.md
93d3f5797a9fbb97b363696e02f66c3af400e2429c64bd1f99bb0d9349710265  notes/curved-two-root-polarization-and-four-cut-square.md
c5133a158c3caf75b82b536801e3119c790a9b13dd6021099bd424f89848d0fd  notes/cross-word-selector-riccati-leakage-guard.md
2070f6c05c12701378c8fb30e1612d337fb95a8569a79a1779fda299f48983a1  notes/selector-macaulay-double-jet-and-offdiagonal-hexagon.md
d40ed51d709c9744d1868a98a0e5bd052d65ee7d8b409eba9d14d61de0745635  notes/selector-macaulay-and-cross-word-riccati-independent-audit.md
```

## 2. Audit conventions and method

For a six-site chart let

\[
 L_{ij}=a_{ij}q^{[3]}+P_iS_jq^{[2]}.
\]

Thus a full physical chart has \(L_{ij}=0\) for \(i\ne j\) and
\(L_{ii}=X_i\).  For the two endpoints used in the note put

\[
 \sigma=a_{00},\qquad F_0=\sigma q+P_0S_0,
 \qquad R=-P_1S_1-P_2S_2.
\]

Since the second endpoint has scalar zero, the exact two-root polarization
at \(h=3\) is

\[
 \Omega_0=RF_0^{[2]}-\sigma^2T_1,
 \qquad \Omega_1=R^{[2]}F_0,
 \qquad T_1=-X_1-X_2.                                      \tag{A1}
\]

I used a fresh sparse matching enumerator with rational coefficients.  It
recursively pairs the eight physical sites for the global tensor and,
independently, enumerates disjoint edge sets for \(q^{[2]},q^{[3]}\), the
nine \(L_{ij}\), \(F_0^{[3]}\), \(R^{[3]}\), and (A1).  Star ranks were
row-reduced over \(\mathbb Q\).  This did not import the primary verifier.
As cross-checks, both

```text
python3 computations/verify_curved_two_chart_anchor_complementarity.py
python3 computations/verify_overlapping_pair_cap_bianchi_connection.py
```

pass; the latter reports all ten symbolic connection identities over
\(\mathbb Z[R]\).

One terminology point matters.  At the scalar-zero endpoint, cleanliness
means \(R^{[3]}=0\), since the term \(s^{h-1}T\) in the clean error vanishes.
It does **not** imply the separate physical row \(Rq^{[2]}=T_1\).  The
primary note states this correctly in Section 4.1.  Accordingly, “clean
binary-target endpoint” in the outcome must not be read as “physical binary
row”; both complementary guards deliberately omit that row.

## 3. The diagonal-row dependency

The integral dependency packet has one perfect matching for every ordered
pair \((i,j)\in\{0,1,2\}^2\), all with coefficient one, and no other
nonzero global word.  Hence its global tensor is

\[
 \sum_{i,j}Y_{ij}.
\]

In either chart, direct enumeration gives

\[
 q^{[3]}=0,qquad L_{ii}=X_i,qquad
 L_{ij}=Y_{ij}|_{W}\quad(i\ne j),                         \tag{A2}
\]

where the six restricted mixed words in (A2) are distinct and have
coefficient one.  This verifies that the failure is exactly the six
off-diagonal rows, not merely that at least one such row fails.

For the \(pq\)-chart the endpoint checks are

\[
 F_0^{[3]}=X_0,qquad Rq^{[2]}=-X_1-X_2,qquad R^{[3]}=0,
\]

and the Omega pair is exactly

\[
 \Omega_0^{pq}=-(ds)_1(ac)_1(br)_0,qquad
 \Omega_1^{pq}=(ds)_1(cr)_2(ab)_0.                         \tag{A3}
\]

For the \(pr\)-chart it is

\[
 \Omega_0^{pr}=-(bd)_1(ac)_1(qs)_0,qquad
 \Omega_1^{pr}=(bd)_1(cq)_2(as)_0.                         \tag{A4}
\]

The monomials in each pair are different, so both pairs are independent.
All four star ranks are three.  Reading the all-zero direct entries from
the literal table gives

\[
 (A,B,C,E,F,U)=(1,1,0,0,0,1),qquad AU-BF=1.
\]

This independently confirms the dependency claimed in Section 2 of the
primary note.

## 4. The independent-column off-diagonal guard

### 4.1 Complete rows and failures

For the first table (28), the internal quadratics are

\[
 q_{pq}=2(rd)_0+3(rs)_0+(rd)_2,qquad
 q_{pr}=(qd)_0+6(qs)_0+(qd)_2.
\]

All terms in either quadratic meet at \(r\), respectively \(q\).  Therefore

\[
 q_{pq}^{[2]}=q_{pr}^{[2]}=q_{pq}^{[3]}=q_{pr}^{[3]}=0.       \tag{A5}
\]

The only direct chart cell is \(a_{00}=6\), so (A5) gives, in both
charts,

\[
 (L_{01},L_{02},L_{10},L_{12},L_{20},L_{21})=(0,0,0,0,0,0),
 \qquad L_{00}=L_{11}=L_{22}=0.                              \tag{A6}
\]

The six off-diagonal equations are exactly correct, and comparison with
the required diagonal values shows that precisely \(X_0,X_1,X_2\) fail.
A direct eight-site enumeration gives the stronger global check

\[
                         \operatorname{Match}^{[4]}=0;          \tag{A7}
\]

the literal support has no perfect matching.

### 4.2 Stars, endpoints, and exact Omega pairs

The four ordered star ranks are

\[
 \operatorname{rank}P^{pq}=operatorname{rank}S^{pq}
 =\operatorname{rank}P^{pr}=operatorname{rank}T^{pr}=3.       \tag{A8}
\]

This can be seen without a determinant choice: the first endpoint has the
private coordinates \((c,0),(a,1),(b,2)\); the second endpoint in the
\(pq\)-chart has \((s,0),(r,1),(d,2)\), and in the \(pr\)-chart has
\((s,0),(q,1),(d,2)\).

Direct matching enumeration gives, in both charts,

\[
                         F_0^{[3]}=36X_0,qquad R^{[3]}=0,      \tag{A9}
\]

so \(K_0\) and \(K_1\) are clean.  For clarity, define the coordinate
words by their nonzero coloured sites:

\[
\begin{array}{lll}
Y_1^{pq}:&(ar)_1,&b,c,d,s\text{ have colour }0,\\
Y_2^{pq}:&(bd)_2,&a,c,r,s\text{ have colour }0,\\
Z^{pq}:&(ar)_1(bd)_2(cs)_0,&\\[1mm]
Y_1^{pr}:&(aq)_1,&b,c,d,s\text{ have colour }0,\\
Y_2^{pr}:&(bd)_2,&a,c,q,s\text{ have colour }0,\\
Z^{pr}:&(aq)_1(bd)_2(cs)_0.&
\end{array}
\]

The exact expansions are

\[
\boxed{\begin{aligned}
 \Omega_0^{pq}&=36X_1+36X_2-12Y_1^{pq}-12Y_2^{pq},&
 \Omega_1^{pq}&=6Z^{pq},\\
 \Omega_0^{pr}&=36X_1+36X_2-12Y_1^{pr}-6Y_2^{pr},&
 \Omega_1^{pr}&=3Z^{pr}.
\end{aligned}}                                                \tag{A10}
\]

This reproduces (41) and (45), including the asymmetric \(-6\) and \(3\)
in the \(pr\)-chart.  In each chart \(\Omega_0\) contains pure words while
\(\Omega_1\) is a distinct single mixed word, so the columns are nonzero
and independent.

### 4.3 Literal curvature

Reading the six all-zero direct cells from table (28), rather than inserting
the claimed constants, gives

\[
 (A,B,C,E,F,U)=(6,6,1,0,6,3),qquad AU-BF=-18.                 \tag{A11}
\]

On the four-site common complement put
\(x=e_0^{(a)}+e_0^{(b)}+e_0^{(c)}\) and \(y=e_0^{(d)}\).  The
selected raw overlap data have

\[
 z=v=0,qquad t=2y,qquad f=xy,qquad g=2xy,qquad
 H=6x,qquad N=3x.
\]

Then both power-free overlap equations are literal identities; the
four-cut one reads

\[
 3f+tH-6g-yN=(3+12-12-3)xy=0=(AU-BF)z.                       \tag{A12}
\]

Thus the nonzero scalar curvature is genuinely tied to one aggregate
packet even though its selected product with \(z\) vanishes in this guard.

Because the line has activity divisor \(tu=0\) and the two columns in
(A10) are independent, neither chart has an active clean point.

## 5. The exactly-one-zero, nonzero-\(q^{[2]}\) guard

### 5.1 Common power and all nine rows

For table (48), direct enumeration gives exactly

\[
\begin{aligned}
q_{pq}^{[2]}&=\frac1{12}(ab)_0(rd)_0
                 +\frac12(ab)_0(rs)_0\ne0,\\
q_{pr}^{[2]}&=-\frac1{12}(ab)_0(qd)_0
                 -\frac12(ab)_0(qs)_0\ne0,\\
q_{pq}^{[3]}&=q_{pr}^{[3]}=0.
\end{aligned}                                                 \tag{A13}
\]

Each monomial of either square contains the two sites \(a,b\) and the
chart's central site \(r\), respectively \(q\).  This gives the claimed
collision in every off-diagonal response.  The complete row result in
both charts is

\[
 L_{00}=X_0,qquad
 (L_{01},L_{02},L_{10},L_{12},L_{20},L_{21})=(0,0,0,0,0,0),
 \qquad L_{11}=L_{22}=0.                                     \tag{A14}
\]

In particular, the physical \(E_{00}\) equation—not only endpoint
cleanliness—is exact.  Its two surviving cofactors contribute
\(\frac12X_0+\frac12X_0\).  The only failed physical rows are the two
missing anchors \(X_1,X_2\).  Direct global enumeration agrees:

\[
                         \operatorname{Match}^{[4]}=X_0.       \tag{A15}
\]

### 5.2 Stars, endpoints, and the full Omega expansion

All four star ranks again equal three.  In the \(pq\)-chart the second
triple uses the independent coordinates \((s,0),(r,1),(r,2)\); in the
\(pr\)-chart it uses \((s,0),(q,1),(q,2)\).  The reuse of a physical site
does not lower rank because the colour coordinates are independent.

The \(rd,rs\), respectively \(qd,qs\), terms cancel from \(F_0\).  In
both charts the remaining cross-shore permanent is \(36\), while the
extra edge \(-\frac12(ab)_0\) cannot enter a perfect matching.  Hence

\[
 F_0^{[3]}=36X_0,qquad R^{[2]}=R^{[3]}=0.                    \tag{A16}
\]

Both endpoints are clean and \(\Omega_1=0\).  A full expansion, stronger
than the nonvanishing assertion in the primary note, is as follows.  Let

\[
\begin{array}{lll}
\widehat Y_1^{pq}:&(ar)_1,&b,c,d,s\text{ have colour }0,\\
\widehat Y_2^{pq}:&(br)_2,&a,c,d,s\text{ have colour }0,\\
\widehat Y_1^{pr}:&(aq)_1,&b,c,d,s\text{ have colour }0,\\
\widehat Y_2^{pr}:&(bq)_2,&a,c,d,s\text{ have colour }0.
\end{array}
\]

Then

\[
\boxed{\begin{aligned}
 \Omega_0^{pq}&=36X_1+36X_2
                 -12\widehat Y_1^{pq}-12\widehat Y_2^{pq},&
 \Omega_1^{pq}&=0,\\
 \Omega_0^{pr}&=36X_1+36X_2
                 -12\widehat Y_1^{pr}-12\widehat Y_2^{pr},&
 \Omega_1^{pr}&=0.
\end{aligned}}                                                \tag{A17}
\]

Thus the nonzero column is certified not only by its pure component but by
its complete coefficient list.

### 5.3 Literal curvature and overlap

The literal direct entries are

\[
 (A,B,C,E,F,U)=(6,6,1,0,6,-6),qquad AU-BF=-72.                \tag{A18}
\]

For the selected all-zero four-cut, let
\(\alpha=(ab)_0\),
\(x=e_0^{(a)}+e_0^{(b)}+e_0^{(c)}\), and
\(y=e_0^{(d)}\).  The common data are

\[
 z=-\frac1{12}\alpha,quad t=-y,quad v=0,quad
 f=-\frac12\alpha+xy,quad g=-\frac12\alpha-xy,quad
 H=6x,quad N=-6x.
\]

The raw transition is \(\Delta=At-By=-12y\).  The first overlap and its
four-cut coefficient are, respectively,

\[
 ft-gy=\alpha y=\Delta z,qquad
 Uf+tH-Fg-yN=6\alpha=(AU-BF)z.                                \tag{A19}
\]

This directly verifies the selected nontrivial connection and curvature
identity instead of relying only on the general fact that the charts came
from one table.

Since \(\Omega_0\ne0\), \(\Omega_1=0\), and every active point has
\(t\ne0\), the joining pencil again has no active clean point.

## 6. What is proved about the six-cycle and Riccati gauge

Three ingredients invoked in Section 7 of the primary note are exact.

1. In the formal source-index polynomial ring, the six products
   \(p_is_j\), \(i\ne j\), form the edge ring of
   \(K_{3,3}\setminus\{00,11,22\}\).  Its integer incidence kernel has
   rank one, so its primitive toric binomial is the alternating hexagon.
   This uniqueness is a formal Segre/toric statement; the site-square-zero
   algebra can have additional collision and top-degree relations.
2. At the eight-site boundary, with
   \(B_{pq}^{ij}=p_i s_j+(a_{pq}^{ij}/3)q_{pq}\), the normalized literal
   overlap identity on a common triple complement is

   \[
   B_{pq}^{ij}t_k-B_{pr}^{ik}y_j
     =\frac{a_{pq}^{ij}t_k-a_{pr}^{ik}y_j}{3}\,z.              \tag{A20}
   \]

   Its fourth-site coefficient contains the exact curvature minor
   \(AU-BF\).  Equation (A20) is the normalized form of the power-free
   Bianchi connection; no common power is cancelled.
3. Independent endpoint row changes give exactly

   \[
   \widetilde B_{kl}q^{[2]}
      =\sum_iG_{ki}H_{li}X_i.                                 \tag{A21}
   \]

   Separately, on the hypotheses of the cross-word selector chart, the
   normalized direct block \(C=A^{-\mathsf T}aB^{-1}\) satisfies the
   audited Riccati--leakage identity

   \[
   \Lambda_{ab}=F(\alpha^2-\xi C_{ab}).                       \tag{A22}
   \]

These facts justify the qualitative diagnosis: without diagonal anchors,
oblique row flags can drift, and a literal coefficient cut is the degree at
which the off-diagonal hexagon can first interact with a target word.

They do not establish a common \(H^1\) obstruction.  In particular:

* no cochain groups, differential, boundary/gauge subspace, or actual
  \(H^1=\ker d_1/\operatorname{im}d_0\) are defined for the Omega pencil;
* the toric six-cycle relation is not by itself a cohomology class in the
  homogeneous overlap-correction complex;
* (A20) constrains cap representatives, but no construction sends a bad
  pair \((\Omega_0,\Omega_1)\) to a nonzero overlap class;
* the matrices in (A21) are arbitrary endpoint row changes, while those in
  (A22) are moving selector-normalization matrices.  Their left-right
  actions are related representations of \(\mathrm{GL}_3\times
  \mathrm{GL}_3\), but the needed identification of the actual matrices
  along the physical overlap has not been made; and
* most importantly, no coefficient-cut comparison map has been defined and
  proved injective on the curvature/good-star open set.

Thus “the same anchored gauge complex” and “the same \(H^1\) obstruction”
should currently be read as a conjectural structural dictionary.  The
primary note itself correctly acknowledges the decisive missing implication
in its last paragraphs.  Its anchored overlap-injectivity lemma is a valid
candidate sufficient statement, but it is not proved here or in the cited
dependency notes.

## 7. Final scope

The two literal guards prove the advertised complementarity sharply:
diagonal rows alone and off-diagonal rows alone each meet the bad-Omega
locus even after imposing literal two-chart provenance, nonzero curvature,
clean endpoints, and good stars.  The nonzero-\(q^{[2]}\) guard further
shows that one unary anchor is not enough; the two complementary binary
anchors are genuinely used by any positive result.

This is a correct obstruction to separated-row arguments.  It is not a
proof of the full-nine Omega-incidence lemma, an anchored overlap
exactness theorem, or Krenn's conjecture.
