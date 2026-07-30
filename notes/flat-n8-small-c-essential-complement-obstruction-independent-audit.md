# Independent audit: the order-eight small-\(C\) obstruction

## Verdict

**PASS.**  The theorem in
[the primary note](flat-n8-small-c-essential-complement-obstruction.md)
is correct over the intended field \(\mathbb C\), conditional on the two
results it cites:

1. the endpoint-support and essential-incidence theorem in
   [`target-flattening-essential-star-pair-bound.md`](target-flattening-essential-star-pair-bound.md);
2. the essential-edge purity lemma and the entry-minimal cubic-star
   conclusion in
   [`flat-degree-four-essential-purity-nullity-export.md`](flat-degree-four-essential-purity-nullity-export.md),
   as assembled in
   [`flat-cubic-boundary-core-order-eight-reduction.md`](flat-cubic-boundary-core-order-eight-reduction.md).

The proof retains arbitrary endpoint order, arbitrary complex cancellation,
zero aggregate blocks, and arbitrary parallel decorated sources after
aggregation.  In particular, its final step does not select one decorated
edge or assume that a matching monomial is individually uncancelled: after
the two cubic ports are forced, the remaining two-site matching tensor is
the single aggregate block \(A_{rs}\).

No mathematical repair is required.  Two provenance clarifications would
be harmless but are not needed for correctness: the assertion
\(A_{pq}=0\) after (14) uses cubicity together with \(b=6\), not merely
the fact that \(pq\) is good; and the independence asserted before (15)
is the equality-witness independence from the essential-subspace lemma,
combined with uniqueness of the coordinate annihilator in the purity
lemma.

## 1. Essential-incidence ledger

For an oriented pair \((x,z)\), write

\[
 S_x^{(z)}=\sum_{w\notin\{x,z\}}
                  \operatorname{im}_{V_x}A_{xw}.
\]

The target flattening gives full total support \(V_x\).  Therefore the
deleted endpoint star is noninjective exactly when
\(S_x^{(z)}\subsetneq V_x\), and an unordered edge is bad exactly when it
has at least one essential endpoint.  A zero block cannot be essential at
either endpoint, because deleting it does not change the full total
support.

The essential-subspace lemma permits at most three essential neighbours at
one site.  If there are three, its equality case makes every other incident
aggregate block zero.  Zero pairs are good, so such a site has bad degree
exactly three.  Every \(x\in X\), however, has at most two good neighbours
among its seven possible neighbours and hence bad degree at least five.
Thus its number \(t_x\) of essential incidences satisfies

\[
                              t_x\leq2.
\]

Every bad edge internal to \(X\) contributes at least one to
\(\sum_{x\in X}t_x\).  Consequently

\[
                     e_X\leq\sum_{x\in X}t_x\leq2|X|.
\]

This counts endpoint incidences rather than aggregate entries, so an edge
essential at both endpoints is correctly counted twice and parallel
decorated sources cause no change.

## 2. The cases \(|C|=1\) and \(|C|=2\)

If \(|C|=1\), the cubic vertex has exactly three bad neighbours.  Summing
the lower bound five over the seven vertices of \(X\) gives

\[
 35\leq2e_X+3\leq 2(14)+3=31,
\]

so this case is impossible.

Now let \(C=\{p,q\}\).  Put \(e_C=1\) when \(pq\) is bad and let \(b\)
be the number of crossing bad edges.  Cubicity gives

\[
 b+2e_C=6,
\]

while the six lower bounds on \(X\) and the essential-incidence estimate
give

\[
 30\leq2e_X+b\leq24+b.
\]

Since \(b\leq6\), every inequality is an equality:

\[
 b=6,\qquad e_C=0,\qquad e_X=12,
 \qquad \sum_{x\in X}t_x=12.
\]

The equality consequences in the primary note follow without a hidden
regularity assumption.  Every \(x\) has \(t_x=2\).  All twelve internal
bad edges must consume exactly one essential incidence, and all twelve
available incidences have thereby been used.  Hence no crossing edge is
essential at its \(X\)-endpoint.  Each \(x\) has total bad degree exactly
five: one crossing bad edge and four internal bad edges.  Its unique
remaining internal edge is good, so the three internal good edges form a
perfect matching.

Finally, each of \(p,q\) has all three bad incidences crossing to \(X\).
Because an entry-minimal globally flat \(C\)-vertex has exactly its three
diagonal cubic blocks and no others, this also proves \(A_{pq}=0\).

## 3. Coordinate flags and the disjoint anchor cover

Fix \(x\in X\), and let \(r,s\) be its two essential neighbours.  For
each essential edge, the purity lemma says that the corresponding deleted
support is a coordinate plane:

\[
 S_x^{(r)}=\ker e_i^*,\qquad
 S_x^{(s)}=\ker e_j^*.
\]

The witness covectors for two distinct essential subspaces are independent
by the proof of the essential-subspace lemma.  The purity lemma makes each
annihilator a unique coordinate line, so \(i\ne j\).  If \(z\) is a
nonessential neighbour of \(x\), its mode-\(x\) support occurs in both
deleted sums and therefore lies in

\[
                 \ker e_i^*\cap\ker e_j^*=\mathbb Ce_k.
\]

The three cubic ports at one centre have distinct physical neighbours.  If
the \(p\)- and \(q\)-stars shared an anchor \(x\), both crossing edges
would be nonessential at \(x\), and the common-line result would force
their two diagonal colours to agree.  The constant coefficient in that
colour would then have no compatible perfect matching: both \(p\) and
\(q\) would be forced to use the same site \(x\).  Its required target
coefficient is one, a contradiction.  Hence the two triples of anchors
are disjoint and, because \(|X|=6\), cover \(X\):

\[
 X=\{x_0,x_1,x_2\}\mathbin{\dot\cup}
   \{y_0,y_1,y_2\}.
\]

At an anchor \(z\), its crossing block is nonessential at \(z\), nonzero,
and has mode-\(z\) support \(\mathbb Ce_{a(z)}\).  It therefore identifies
the common nonessential line exactly with
\(\mathbb Ce_{a(z)}\), as claimed in (17a).

## 4. Audit of the two-centre cofactor table

Write the six cubic blocks as

\[
 A_{px_c}=a_c e_c^{(p)}\otimes e_c^{(x_c)},\qquad
 A_{qy_d}=b_d e_d^{(q)}\otimes e_d^{(y_d)},
 \qquad a_cb_d\ne0.
\]

Contract the complete identity first in mode \(p\) by \(e_c^*\) and then
in mode \(q\) by \(e_d^*\).  Cubicity makes the displayed two ports the
only survivors, while their anchors are distinct.  Thus, with physical
slot order restored,

\[
 a_cb_d,e_c^{(x_c)}\otimes e_d^{(y_d)}\otimes
 H_{X\setminus\{x_c,y_d\}}(A)
 =\delta_{cd}e_c^{\otimes X}.
\]

The two displayed one-site factors are nonzero.  For \(c\ne d\), tensor
factor cancellation therefore gives a zero four-site cofactor.  For
\(c=d\), it gives

\[
 H_{X\setminus\{x_c,y_c\}}(A)
       =(a_cb_c)^{-1}e_c^{\otimes4}.
\]

This is exactly table (6).  It is an identity for the complete aggregate
cofactor and retains every internal matching and cancellation term.

## 5. Audit of the complementary pure-edge contradiction

Choose an internal bad edge \(uv\).  The incidence equality proves that
it is essential at exactly one endpoint.  The endpoint-reversed form of
the essential-edge purity lemma is available if that endpoint is the
second one; in either orientation it supplies a unique colour \(k\) and
\(\beta\ne0\) such that

\[
                    H_{B\setminus\{u,v\}}(A)
                       =\beta e_k^{\otimes6}.
\]

Neither \(x_k\) nor \(y_k\) is deleted.  If \(x_k\in\{u,v\}\), then the
remaining \(p\)-star has no block with mode-\(p\) colour \(k\), so
contracting at \(p\) by \(e_k^*\) kills the left side but not the right.
The argument at \(q\) excludes deletion of \(y_k\).

Let

\[
 \{r,s\}=X\setminus\{u,v,x_k,y_k\}.
\]

After contracting the pure cofactor in modes \(p,q\) by \(e_k^*\), the
ports \(px_k\) and \(qy_k\) are forced.  The residual site set is exactly
\(\{r,s\}\).  Its matching tensor is not a selected monomial but the
complete aggregate block itself:

\[
 a_kb_k,e_k^{(x_k)}\otimes e_k^{(y_k)}\otimes A_{rs}
 =\beta e_k^{(x_k)}\otimes e_k^{(y_k)}
          \otimes e_k^{(r)}\otimes e_k^{(s)}.
\]

Hence

\[
                A_{rs}=\frac{\beta}{a_kb_k}
                        e_k^{(r)}\otimes e_k^{(s)}\ne0.
\]

There is no factorial, sign, orientation, or parallel-source ambiguity in
this expansion.  Each physical perfect matching is counted once, and all
parallel decorated cells on \(rs\) have already been summed into
\(A_{rs}\).

Only \(x_k,y_k\) have anchor colour \(k\), so both \(r,s\) have different
anchor colours.  The pair \(rs\) has a nonessential endpoint: both if it
is good, and exactly one if it is one of the internal bad edges.  At such
an endpoint, say \(r\), the common-line result forces the mode-\(r\)
support of \(A_{rs}\) into \(\mathbb Ce_{a(r)}\).  The displayed nonzero
pure block instead has support \(\mathbb Ce_k\), with \(a(r)\ne k\).
This is the required contradiction.

## 6. Scope check

The argument uses entry-minimality and global fan flatness only upstream,
to invoke the diagonal cubic structure at \(p,q\).  The incidence count,
coordinate flags, cofactor table, and final contradiction are exact tensor
arguments after aggregation.  They make no genericity, positivity,
supportwise-noncancellation, symmetry, or order-minimality assumption.
