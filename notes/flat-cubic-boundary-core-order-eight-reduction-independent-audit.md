# Independent audit: the globally flat branch has only an order-eight core

## 1. Verdict

The theorem in
[`flat-cubic-boundary-core-order-eight-reduction.md`](flat-cubic-boundary-core-order-eight-reduction.md)
is **PASS**, under its stated hypotheses: \(N\geq8\), an entry-minimal
ternary exact aggregate source, and vanishing of every canonical transition
on every good fan.  The deductions

\[
 |X|\leq7,
 \qquad |C|\leq5,
 \qquad N\notin\{10,12,14,\ldots\}
\]

are valid over arbitrary complex weights and retain all cancellation.  At
\(N=8\), every fourth matching supplied by three selected constant fibres
localizes to an exact zero coefficient on an even subset
\(Y\subseteq X\) of size four or six.

No mathematical change to the boundary-core theorem is required.  Two
minor notation repairs are advisable before reusing the open-rail lemma:

1. \(D_c\) is the **forced occurrence matching covering \(C\)**, generally
   only a partial perfect matching of \(B\).  A \(C\!-\!C\) occurrence is
   listed once, while occurrences of different colours on the same
   physical pair remain distinct.
2. The \(c/d\) rail graph is a two-coloured occurrence multigraph; a pair
   carrying both a \(c\)- and a \(d\)-occurrence is a parallel two-cycle.
   In the cycle-switch proof one should switch a selected full constant
   matching \(M_c\), not call the partial \(D_c\) a full matching.  Equations
   (11) and (18) already justify the same switch without making a selection.

These clarifications handle parallel sources and do not alter any bound.

## 2. Zero pairs, flat centres, and cubicity

For a site \(u\), let \(L_{u\leftarrow x}\) be the mode-\(u\) support of
\(A_{ux}\).  Exactness gives

\[
                       \sum_{x\ne u}L_{u\leftarrow x}=V_u.
\]

If \(A_{uv}=0\), then \(L_{u\leftarrow v}=0\), so deleting \(v\) leaves
the displayed span equal to \(V_u\).  The same argument at \(v\) proves

\[
                         A_{uv}=0\Longrightarrow uv\text{ is good}.
                                                               \tag{A1}
\]

Thus every bad pair is aggregate-active.  This is a statement about the
aggregate endpoint-colour cell tensor; parallel original sources with the
same endpoint colours have already been summed, which is legitimate
because the full matching tensor is the hafnian polynomial in those
aggregate cells.

Now let \(u\in C\).  It has at least three good neighbours, so they form a
good fan at \(u\).  Global flatness and the flat exact-fan theorem kill
every block from \(u\) to a good neighbour.  Hence every active incident
pair is bad.  The pure-port partition theorem then applies to the entire
\(u\)-star.  Its entry-minimal strengthening leaves exactly one port for
each colour, namely

\[
 A_{u f_c(u)}=a_{u,c}e_c^{(u)}\otimes e_c^{(f_c(u))},
 \qquad a_{u,c}\ne0,
 \qquad c=0,1,2.                                      \tag{A2}
\]

There are no other active blocks, and (A1) makes every other pair good.
The three displayed active pairs were killed if good and therefore are
bad.  Consequently

\[
                          \deg_{\rm bad}(u)=3.             \tag{A3}
\]

If both endpoints of one displayed edge lie in \(C\), applying (A2) at
both ends forces the same colour and the same underlying aggregate cell;
there is no hidden endpoint-order assumption here.

The only minimality used is minimum nonzero **aggregate-entry** support
among ternary exact sources.  This reduction is legitimate: every
aggregate cell can be represented by one decorated degree-two source, and
the exact port surgery replaces a fibre of \(t>1\) nonzero ports by one
cell.  It strictly reduces aggregate-entry support and preserves the full
target tensor.

## 3. Constant fibres and exact core factorization

Fix \(c\in\{0,1,2\}\).  At every \(u\in C\), a constant-\(c\) perfect
matching is forced to use the occurrence \(u f_c(u)\).  Since the target
coefficient is one, at least one nonzero constant-(c) matching exists.
It follows immediately that these forced occurrences cannot conflict:

* if \(f_c(u)=v\in C\), then \(f_c(v)=u\), and the one physical occurrence
  is counted once;
* two different vertices of \(C\) cannot have the same \(x\in X\) as
  their colour-\(c\) partner.

Thus \(D_c\) is an occurrence matching covering \(C\).  It covers a subset
\(Z_c\subseteq X\), and its complement \(Y_c=X\setminus Z_c\) is even.
Every constant-\(c\) matching contains \(D_c\), and deleting \(D_c\) is a
weight-preserving bijection onto the constant-\(c\) matching fibre on
\(Y_c\).  Hence, with every \(C\!-\!C\) cell multiplied only once,

\[
 1=w(D_c)\,[e_c^{\otimes Y_c}]H_{Y_c}(A).                \tag{A4}
\]

In particular the residual coefficient is nonzero.  The same proof works
for an arbitrary colouring \(\xi\).  If its forced occurrences at \(C\)
conflict or disagree at their opposite endpoint, its fibre is empty.
Otherwise they form an occurrence matching \(F_\xi\) covering \(C\) and
\(Z_\xi\subseteq X\), and restriction/extension is a bijection giving

\[
 [e_\xi]H_B(A)=w(F_\xi)
 [e_{\xi|Y_\xi}]H_{Y_\xi}(A),
 \qquad Y_\xi=X\setminus Z_\xi.                         \tag{A5}
\]

This is an equality of complete coefficients, not of selected terms, so
arbitrary cancellation on \(Y_\xi\) is retained.

Choose one nonzero aggregate-cell monomial \(M_c\) from each constant
fibre.  Their differently coloured cells are distinct occurrences even
when they lie on the same physical pair.  The standard three-one-factors
lemma supplies a fourth occurrence matching \(R\) because \(N\geq8\).
Its induced colouring is mixed, and it is the only compatible matching
inside the selected occurrence union.  Formula (A5) gives a nonzero
selected residual monomial on \(Y=Y_{\xi_R}\) inside the zero coefficient

\[
                     [e_{\xi_R|Y}]H_Y(A)=0.              \tag{A6}
\]

Here \(Y\) cannot be empty because \(H_\varnothing=1\).  It cannot have
two sites because \(H_{\{x,y\}}=A_{xy}\), and the one aggregate cell used
by \(R\) is nonzero.  Since \(Y\subseteq X\) is even and \(|X|\leq7\),

\[
                              |Y|\in\{4,6\}.              \tag{A7}
\]

This also verifies that no positivity or termwise-vanishing inference is
present in the fourth-matching localization.

## 4. Exceptional-set and order counts

Every \(x\in X\) has at most two good neighbours, hence at least \(N-3\)
bad neighbours.  Its bad degree within \(X\) is therefore at least

\[
                       N-3-|C|=|X|-3.                    \tag{A8}
\]

The bad graph is \(4\)-degenerate, as proved by the target-flattening
theorem.  If \(|X|\geq8\), its induced subgraph on \(X\) would have minimum
degree at least five, a contradiction.  Thus \(|X|\leq7\).

The case \(X=\varnothing\) is impossible: (A2) says that the whole source
is exactly the three selected constant one-factors, while the fourth
matching has a mixed singleton fibre.  For \(x\in X\), at most
\(|X|-1\) bad neighbours lie in \(X\), so

\[
 \deg_{\rm bad}(x,C)\geq N-3-(|X|-1)=|C|-2.              \tag{A9}
\]

For a fixed colour, constant-fibre existence permits at most one
colour-\(c\) incidence from \(C\) into a given \(x\).  Summing the three
colours gives \(\deg_{\rm bad}(x,C)\leq3\), and hence \(|C|\leq5\).
Therefore \(N\leq12\).

Let \(b=|E_{\rm bad}(C,X)|\).  Equations (A3) and (A9) give

\[
                       |X|(|C|-2)\leq b\leq3|C|.          \tag{A10}
\]

For \(N=12\), the only sizes are \((|C|,|X|)=(5,7)\), and (A10) reads
\(21\leq b\leq15\).

For \(N=10\), only three size pairs remain.

* If \((|C|,|X|)=(5,5)\), equality in (A10) makes all three edges at each
  \(C\)-site cross to \(X\).  Each selected \(M_c=D_c\) is a perfect
  matching between the two five-sets.  Every fourth matching in their
  union also covers all of \(X\) by its forced \(C\!-\!X\) edges, so
  \(Y=\varnothing\), contradicting (A7).
* If \((|C|,|X|)=(4,6)\), equality again makes every cubic edge cross.
  Each selected constant matching has four crossing edges and its one
  residual \(X\!-\!X\) occurrence.  Any perfect matching in the selected
  union must cover all four (C)-sites by crossing edges and then use one
  \(X\!-\!X\) occurrence, so its residual set has size two.  This
  contradicts (A7).
* If \((|C|,|X|)=(3,7)\), summing the at-least-seven bad degrees over
  \(X\), and subtracting at most \(b\leq9\) cross incidences, gives
  \(2e(X)\geq40\), hence \(e(X)\geq20\).  A \(4\)-degenerate graph on
  seven vertices has at most
  \(4\cdot7-\binom52=18\) edges, a contradiction.

This eliminates every even \(N\geq10\).  At \(N=8\), (A7) gives
\(|X|\geq4\), while \(|X|\leq7\); hence \(1\leq|C|\leq4\).

## 5. Open Kempe rails

For distinct colours \(c,d\), form the two-coloured **occurrence
multigraph** on \(C\) from the internal occurrences of \(D_c\cup D_d\).
Every vertex has at most one incidence of each colour.  Thus every
component is an alternating path, an isolated vertex, or an alternating
cycle; two differently coloured occurrences on one physical pair form a
cycle of length two.

An alternating cycle \(P\subseteq C\) is impossible.  Start with any
selected full constant-\(c\) matching \(M_c\) and replace its \(c\)-edges
on \(P\) by the \(d\)-edges.  Nothing on \(X\) changes.  Equivalently,
apply (A5) and (A4) to the colouring which is \(d\) on \(P\) and \(c\)
elsewhere.  Its coefficient is

\[
 \frac{\prod_{e\in D_d\cap E(P)}w(e)}
      {\prod_{e\in D_c\cap E(P)}w(e)},                  \tag{A11}
\]

which is nonzero, contradicting the mixed target coefficient.  This
argument works unchanged for a parallel two-cycle because the two
occurrence weights are distinct nonzero aggregate cells.

Every remaining path has exactly two missing \(c/d\) incidences into
\(X\), counted with multiplicity; an isolated \(C\)-vertex has two.  A
site of \(X\) receives at most one forced incidence of each colour, so
there are at most \(2|X|\) path-end incidences and hence at most \(|X|\)
paths.  Within the selected \(c/d\) occurrence network, a path has exactly
the two alternating matching states: all its \(c\)-occurrences or all its
\(d\)-occurrences.  This last sentence does not claim that the full source
on \(X\) has only two states; all residual core blocks and cancellation
remain inside (A5).

## 6. Lightweight checks and scope

The existing exact scripts were rerun:

```text
python3 computations/verify_target_flattening_essential_star_pair_bound.py
target-flattening essential-star pair bound: PASS

python3 computations/verify_triple_matching_rewrite.py
verified three selected constant fibres and the exact two-term mixed fibre
```

The first script audits the support-span/essentiality input and the
\(4\)-degenerate bad-graph bound.  The second checks occurrence-level
bookkeeping in the presence of extra cancellation cells and demonstrates
why the conclusion must stop at a bounded zero response rather than claim
uniqueness.  Neither finite check is used to prove the uniform order
reduction.

The result closes only the globally flat entry-minimal branch above order
eight.  It does not close the remaining \(N=8\) four-/six-site core, nor
the alternative in which some good-fan transition has nonzero curvature.
