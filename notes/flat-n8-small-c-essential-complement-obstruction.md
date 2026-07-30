# The order-eight flat core cannot have one or two cubic vertices

## 1. Outcome

Let \(B\) have eight sites and let arbitrary endpoint-ordered aggregate
blocks satisfy

\[
                         H_B(A)=\Delta_{B,3}.                    \tag{1}
\]

Assume that the source is entry-minimal and that every canonical
transition on every good fan is flat.  Use the notation of
[`flat-cubic-boundary-core-order-eight-reduction.md`](flat-cubic-boundary-core-order-eight-reduction.md):

\[
 C=\{u:\deg_{\rm good}(u)\geq3\},
 \qquad X=B\setminus C.                                      \tag{2}
\]

Every vertex of \(C\) is then a diagonal cubic vertex, while every vertex
of \(X\) has at least five bad neighbours.  The boundary-core theorem
leaves \(1\leq |C|\leq4\).

This note eliminates the two small cases.

**Theorem 1 (small-\(C\) obstruction).**  Under the displayed hypotheses,

\[
                              |C|\notin\{1,2\}.                \tag{3}
\]

Consequently every surviving globally flat order-eight source would have

\[
                         |C|\in\{3,4\},\qquad |X|\in\{5,4\}.  \tag{4}
\]

The proof uses only the deletion-essential endpoint lemma and the pure
cofactor carried by an essential edge.  It does not enumerate supports,
matchings, or colour assignments.

The equality case for \(|C|=2\) is useful independently.  If
\(C=\{p,q\}\), it would force six distinct anchors

\[
 \{x_0,x_1,x_2\}\mathbin{\dot\cup}
 \{y_0,y_1,y_2\}=X,                                        \tag{5}
\]

where \(p\) is joined diagonally to \(x_c\) in colour \(c\) and \(q\)
is joined diagonally to \(y_c\).  The good graph induced on \(X\) would
be a perfect matching, and the exact four-site cofactors would obey

\[
 H_{X\setminus\{x_c,y_d\}}(A)=
 \begin{cases}
  0,&c\ne d,\\[2mm]
  (a_cb_c)^{-1}e_c^{\otimes4},&c=d,
 \end{cases}                                                \tag{6}
\]

for the nonzero cubic-port weights \(a_c,b_c\).  The contradiction comes
from coupling (6)'s anchor geometry to the pure six-site cofactor of any
internal bad edge.

## 2. Essential-incidence budget on the exceptional set

For a site \(u\), call a neighbour \(v\) **essential at \(u\)** when

\[
 \sum_{z\notin\{u,v\}}
       \operatorname{im}_{V_u}A_{uz}\ne V_u.                 \tag{7}
\]

Thus a pair is bad exactly when it is essential at at least one endpoint.
The
[`target-flattening essential-star theorem`](target-flattening-essential-star-pair-bound.md)
gives at most three essential neighbours at any site.  Its equality case
says more: if a site has three essential neighbours, all its other incident
aggregate blocks vanish, so its total bad degree is at most three.

Every \(x\in X\) has at most two good neighbours and therefore

\[
                            \deg_{\rm bad}(x)\geq5.            \tag{8}
\]

It follows that no \(x\in X\) has three essential neighbours.  Write
\(t_x\) for their number.  Then

\[
                               t_x\leq2.                       \tag{9}
\]

Every bad edge internal to \(X\) consumes an essential incidence at one
or both of its endpoints.  Hence, if \(e_X\) denotes the number of such
edges,

\[
                    e_X\leq\sum_{x\in X}t_x\leq2|X|.          \tag{10}
\]

This is the sharper boundary count unavailable before passing to the
order-eight exceptional set.

## 3. One cubic vertex is impossible

Suppose \(|C|=1\), so \(|X|=7\).  The unique vertex of \(C\) has exactly
three bad neighbours, all in \(X\).  If \(b\) is the number of bad
\(C\)-\(X\) edges, then \(b=3\).  Summing (8) over \(X\) and using (10)
would give

\[
            35\leq 2e_X+b\leq 2(14)+3=31,                    \tag{11}
\]

a contradiction.

## 4. Equality structure with two cubic vertices

Now suppose \(C=\{p,q\}\) and \(|X|=6\).  Let \(e_C\) be the indicator
of a bad edge \(pq\), and let \(b\) again count bad edges crossing from
\(C\) to \(X\).  Each vertex of \(C\) has bad degree three, so

\[
                              b+2e_C=6,
 \qquad b\leq6.                                             \tag{12}
\]

On the other hand, (8) and (10) give

\[
                   30\leq2e_X+b\leq24+b.                    \tag{13}
\]

Thus equality holds everywhere:

\[
 b=6,\qquad e_C=0,\qquad e_X=12.                            \tag{14}
\]

In particular, \(A_{pq}=0\), every cubic port at \(p\) and \(q\) crosses
to \(X\), and the internal good graph on the six vertices of \(X\) has
exactly \(15-12=3\) edges.

Equality in (10) has four further consequences:

1. every \(x\in X\) has exactly two essential neighbours;
2. both of those neighbours lie in \(X\);
3. every internal bad edge is essential at exactly one endpoint;
4. every crossing edge from \(C\) is nonessential at its \(X\)-endpoint.

Fix \(x\in X\), and call its two essential neighbours \(r,s\).  By the
essential-edge purity lemma, deleting \(r\), respectively \(s\), from the
\(x\)-star leaves coordinate planes

\[
        \sum_{z\ne x,r}\operatorname{im}_{V_x}A_{xz}
             =\ker e_i^*,
 \qquad
        \sum_{z\ne x,s}\operatorname{im}_{V_x}A_{xz}
             =\ker e_j^*.                                  \tag{15}
\]

The two essential witness covectors are independent, so \(i\ne j\).
Every block at a nonessential neighbour of \(x\) belongs to both planes.
Consequently all such blocks have their mode-\(x\) support in the common
coordinate line

\[
                         \ker e_i^*\cap\ker e_j^*=\mathbb Ce_k
 \quad(\{i,j,k\}=\{0,1,2\}).                               \tag{16}
\]

The six cubic ports cover \(X\) without overlap.  Indeed, the three ports
at either cubic centre have distinct neighbours.  If both \(p\) and \(q\)
met the same \(x\), their crossing edges would be nonessential at \(x\),
so (16) would force their two diagonal colours to agree.  But then the
constant coefficient in that colour would be zero: the unique required
ports at \(p\) and \(q\) would conflict at \(x\).  This contradicts (1).

We may therefore label the ports as in (5), with

\[
 A_{p x_c}=a_c e_c^{(p)}\otimes e_c^{(x_c)},\qquad
 A_{q y_c}=b_c e_c^{(q)}\otimes e_c^{(y_c)},
 \qquad a_cb_c\ne0.                                        \tag{17}
\]

If \(a(z)\) denotes the colour of the unique crossing anchor at
\(z\in X\), its nonzero diagonal block belongs to the common line (16).
Thus that line is now identified exactly:

\[
 \text{every block nonessential at }z\text{ has mode-}z\text{ support in }
                         \mathbb C e_{a(z)}.              \tag{17a}
\]

Every vertex of \(X\) has one crossing bad edge.  Equality in (13) says
that its internal bad degree is four, so its one remaining internal edge
is good.  The three internal good edges are therefore a perfect matching.

Finally expand (1) first at \(p\) and then at \(q\).  The \((c,d)\)
slice in the two named modes has the unique forced ports \(px_c,qy_d\),
and hence

\[
 a_cb_d e_c^{(x_c)}\otimes e_d^{(y_d)}\otimes
 H_{X\setminus\{x_c,y_d\}}(A)
 =\delta_{cd}e_c^{\otimes X}.                              \tag{18}
\]

This proves the exact cofactor table (6), with all internal cancellation
retained.

## 5. The complementary pure edge contradiction

Choose any internal bad edge \(uv\) of \(X\).  By the equality structure
above it is essential at exactly one endpoint.  The essential-edge purity
lemma in
[`flat-degree-four-essential-purity-nullity-export.md`](flat-degree-four-essential-purity-nullity-export.md)
supplies a colour \(k\) and a nonzero scalar \(\beta\) such that

\[
                    H_{B\setminus\{u,v\}}(A)
                       =\beta e_k^{\otimes6}.                  \tag{19}
\]

Neither \(x_k\) nor \(y_k\) can be one of \(u,v\).  If, for example,
\(x_k\) were deleted, then the remaining \(p\)-star would have no port
with mode-\(p\) colour \(k\); contracting the left side of (19) by
\(e_k^*\) at \(p\) would give zero, contrary to \(\beta\ne0\).  The same
argument applies to \(y_k\) at \(q\).

There are exactly two further exceptional vertices

\[
                  \{r,s\}=X\setminus\{u,v,x_k,y_k\}.          \tag{20}
\]

Contract (19) by \(e_k^*\) in the \(p\)- and \(q\)-modes.  The only
surviving ports are \(px_k\) and \(qy_k\), after which the two remaining
sites must be paired together.  Therefore

\[
                       A_{rs}=\frac{\beta}{a_kb_k}
                              e_k^{(r)}\otimes e_k^{(s)}.       \tag{21}
\]

In particular this aggregate block is nonzero.  Both \(r\) and \(s\)
have anchor colour different from \(k\), since the only two anchor-colour
\(k\) vertices are \(x_k,y_k\).

But the pair \(rs\) has a nonessential endpoint.  If it is good, it is
nonessential at both endpoints; if it is bad, every internal bad edge is
essential at exactly one endpoint.  At a nonessential endpoint, say
\(r\), equation (16) says that the mode-\(r\) support of \(A_{rs}\) lies
in the coordinate line determined by the crossing anchor at \(r\).  That
line has colour different from \(k\), whereas (21) has mode-\(r\) support
\(\mathbb Ce_k\).  This is impossible.

The contradiction eliminates \(|C|=2\), completes the proof of Theorem 1,
and leaves only the \(|C|=3,4\) matching-cut boundary of the globally flat
order-eight branch.

## 6. Scope and next gate

The argument is over \(\mathbb C\), but uses only finite-dimensional
linear algebra and exact matching-tensor expansions.  It permits arbitrary
complex cancellation, parallel decorated sources after aggregation, zero
blocks, and endpoint-ordered blocks.  Entry-minimality and global fan
flatness enter only through the theorem making every site of \(C\) a
diagonal cubic vertex.

No new finite search is needed.  The remaining globally flat cases have
three or four cubic vertices, hence five or four exceptional vertices.
Their constant-colour occurrence cuts are already large enough that the
fourth-matching localization can be attacked directly; the small-core
essential-incidence escape proved here is no longer available.
