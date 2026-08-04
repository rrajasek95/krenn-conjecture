# The globally flat cubic boundary reduces to an order-eight core

## 1. Outcome

Let \(B\) have even size \(N\geq 8\), and suppose that arbitrary
endpoint-ordered aggregate blocks satisfy

\[
                         H_B(A)=\Delta_{B,3}.                    \tag{1}
\]

Assume that the source is entry-minimal and that every canonical
transition on every good fan is flat.  Here a pair is **good** when both
deleted endpoint-star maps are injective.  The flat-fan theorem together
with
[the exact bad-only-star surgery](flat-degree-four-essential-purity-nullity-export.md)
then says:

\[
 \boxed{\text{every vertex having at least three good neighbours is
 cubic.}}                                                       \tag{2}
\]

This note proves the following uniform boundary-core theorem.

**Theorem 1 (flat boundary-core reduction).**  Put

\[
 \begin{aligned}
 C&=\{u:\deg_{\rm good}(u)\geq3\},\\
 X&=B\setminus C.
 \end{aligned}                                                \tag{3}
\]

Then:

1. every \(u\in C\) has exactly three bad neighbours, one on a nonzero
   diagonal coordinate cell of each colour;
2. \(X\) has at most seven vertices and \(C\) has at most five vertices;
3. the hypotheses are impossible for every even \(N\geq10\).

Consequently the entire globally flat branch at arbitrary order reduces
to \(N=8\).  At \(N=8\), one necessarily has

\[
                   1\leq |C|\leq4,\qquad 4\leq|X|\leq7.         \tag{4}
\]

The remaining cancellation is genuinely bounded.  For any three selected
nonzero constant-colour matching monomials and any fourth matching in
their occurrence union, its mixed coefficient factors as a nonzero forced
boundary product times a matching coefficient on an even set

\[
                            Y\subseteq X,\qquad |Y|\in\{4,6\}.  \tag{5}
\]

Thus no matching or support enumeration at large order remains in this
branch.  The only possible repair is an exact four- or six-site response
inside the exceptional core.  Long cubic regions merely form deterministic
alternating rails between those core sites.

The proof retains arbitrary complex cancellation.  In particular, it
does not assert that a selected fourth matching is uncancellable; it proves
that every cancellation mate differs from it entirely inside \(Y\).

## 2. Zero pairs are good and cubic pairs are forced

The complete mode support at every site is all of \(V_u\cong\mathbb C^3\),
by
[the target-flattening theorem](target-flattening-essential-star-pair-bound.md).
If \(A_{uv}=0\), deleting \(v\) from the \(u\)-star removes no endpoint
support, and likewise at \(v\).
Therefore

\[
                         A_{uv}=0\quad\Longrightarrow\quad uv
                         \text{ is good}.                       \tag{6}
\]

Equivalently, every bad pair is active.

For \(u\in C\), (2) and cubic rigidity give distinct neighbours
\(f_0(u),f_1(u),f_2(u)\) and nonzero scalars \(a_{u,c}\) such that

\[
 A_{u f_c(u)}
     =a_{u,c}e_c^{(u)}\otimes e_c^{(f_c(u))},
       \qquad c=0,1,2,                                      \tag{7}
\]

and every other block at \(u\) is zero.  Flatness killed every active
good block at \(u\), so the three displayed pairs are bad.  Conversely
(6) shows that there are no other bad pairs at \(u\).  Hence

\[
                         \deg_{\rm bad}(u)=3\qquad(u\in C).    \tag{8}
\]

Fix a colour \(c\).  Every matching contributing to the constant-\(c\)
coefficient must use the unique cell (7) at every \(u\in C\).  Since that
coefficient equals one, at least one such matching exists.  It follows
that the edges

\[
                         D_c=\{u f_c(u):u\in C\}              \tag{9}
\]

form a forced occurrence matching covering \(C\), generally only a partial
perfect matching of \(B\).  A \(C\)-\(C\) occurrence is listed once, while
different-colour occurrences on the same physical pair remain distinct.
In particular, for every \(x\in X\),

\[
       \#\{u\in C:f_c(u)=x\}\leq1,\qquad
       \deg_{\rm bad}(x,C)\leq3.                              \tag{10}
\]

The last bound is one edge per colour.  It is a consequence of the
nonzero constant coefficient, not a supportwise noncancellation
assumption: if two cubic vertices forced the same \(c\)-cell partner
\(x\), the constant-\(c\) matching fibre would be empty.

Let \(Z_c=V(D_c)\cap X\) and \(Y_c=X\setminus Z_c\).  If \(w(D_c)\) is
the product of the distinct nonzero cells in (9), expansion over the
forced edges gives the exact scalar identity

\[
  1=w(D_c)\,
       [e_c^{\otimes Y_c}]H_{Y_c}(A).                          \tag{11}
\]

Thus the residual scalar is nonzero.  This is the first instance of the
core factorization proved in Section 4.

## 3. Seven exceptional vertices and five cubic vertices

The bad-pair graph is \(4\)-degenerate.  Each \(x\in X\) has at most two
good neighbours in all of \(B\).  Consequently its degree inside the
induced bad graph on \(X\) is at least

\[
                         |X|-3.                              \tag{12}
\]

If \(|X|\geq8\), this induced graph has minimum degree at least five,
contrary to \(4\)-degeneracy.  Therefore

\[
                              |X|\leq7.                       \tag{13}
\]

If \(X=\varnothing\), (7) makes the whole source three constant-colour
one-factors, and the standard three-one-factors lemma gives an
uncancellable fourth matching.  Hence \(X\ne\varnothing\).

*Attribution.*  The three-one-factors lemma is **Bogdanov's observation**
(Bogdanov 2017), published as Thm 1 of Chandran-Gajjala,
arXiv:2202.05562, and in multigraph form as Thm 1.7 of
Chandran-Gajjala-Illickan, arXiv:2407.00303; see
[`references/REFERENCES.md`](../references/REFERENCES.md).  No priority is
claimed for it here.

For \(x\in X\), at least \(N-3\) of its pairs are bad.  At most
\(|X|-1\) of those neighbours lie in \(X\), so

\[
                 \deg_{\rm bad}(x,C)\geq
                    N-3-(|X|-1)=|C|-2.                       \tag{14}
\]

Together with (10), this gives \(|C|-2\leq3\), and hence

\[
                              |C|\leq5.                       \tag{15}
\]

Equations (13) and (15) already give \(N\leq12\).  Notice the useful
degree gap behind this bound: under global flatness every vertex has bad
degree either exactly three (the vertices in \(C\)) or at least \(N-3\)
(the vertices in \(X\)).

## 4. Exact localization of every matching fibre

Let \(\xi:B\to\{0,1,2\}\) be any colouring.  At every \(u\in C\), a
\(\xi\)-compatible matching is forced to use

\[
                           u f_{\xi(u)}(u).                    \tag{16}
\]

If these forced cells conflict, or if the colour at their other endpoint
does not agree with their diagonal colour, the matching fibre is empty.
Otherwise their distinct underlying edges form a matching \(F_\xi\)
covering \(C\) and a subset \(Z_\xi\subseteq X\).  Put

\[
                           Y_\xi=X\setminus Z_\xi.             \tag{17}
\]

Every remaining edge of a compatible perfect matching has both endpoints
in \(Y_\xi\), and conversely every compatible perfect matching of
\(Y_\xi\) extends uniquely by \(F_\xi\).  Therefore the complete
coefficient, with all cancellation still collected, is

\[
 [e_\xi]H_B(A)=w(F_\xi)\,
       [e_{\xi|Y_\xi}]H_{Y_\xi}(A).                           \tag{18}
\]

The prefactor is nonzero.  Also \(Y_\xi\) is even, since it is the
uncovered set of a matching in an even vertex set.  Formula (18) is the
promised exact boundary-core response: all freedom and all cancellation
live on \(X\).

Choose one nonzero monomial from each constant-colour fibre.  By (11),
this is possible.  Denote the resulting perfect matchings by
\(M_0,M_1,M_2\), treating differently coloured cells on the same pair as
different occurrences.  Their occurrence union \(U\) is locally rainbow
and cubic.  The three-one-factors lemma supplies a fourth perfect matching
\(R\subset U\).  It is mixed, because the only all-\(c\) occurrence at a
cubic vertex is its \(M_c\)-occurrence, so an all-\(c\) matching in \(U\)
would equal \(M_c\).

*Attribution.*  The three-one-factors lemma is **Bogdanov's observation**
(Bogdanov 2017); the occurrence-multigraph form used here is Thm 1.7 of
Chandran-Gajjala-Illickan, arXiv:2407.00303 (the simple-graph form is
Thm 1 of Chandran-Gajjala, arXiv:2202.05562).  See
[`references/REFERENCES.md`](../references/REFERENCES.md).  No priority is
claimed for it here.

Let \(\xi_R\) be the mixed colouring induced by \(R\).  The part of \(R\)
incident with \(C\) is \(F_{\xi_R}\); the remaining part is a nonzero
perfect-matching monomial \(R_Y\) on \(Y=Y_{\xi_R}\subseteq X\).  Since
the target mixed coefficient is zero, (18) says

\[
                 [e_{\xi_R|Y}]H_Y(A)=0,                         \tag{19}
\]

even though its sum contains the nonzero term \(w(R_Y)\).  Thus a
cancellation mate exists, but every such mate differs from \(R\) only on
\(Y\).  Equivalently, every alternating cycle in the symmetric difference
of \(R\) and a mate is contained in \(X\).

The set \(Y\) cannot be empty.  It also cannot have two vertices: on a
two-site set the coefficient in (19) is the single aggregate cell used by
\(R_Y\), which is nonzero.  Hence

\[
                      4\leq |Y|\leq |X|.                       \tag{20}
\]

Combining evenness with (13) sharpens the upper bound to

\[
                            |Y|\in\{4,6\}.                     \tag{21}
\]

This argument is cancellation-safe precisely because it stops at (19):
it does not infer that any individual term in a general mixed fibre
vanishes.

## 5. No bichromatic cubic cycle avoids the core

There is a useful non-enumerative description of the long part of the
source.  Fix distinct colours \(c,d\), and consider the two-coloured
occurrence multigraph on \(C\) formed by the \(c\)- and \(d\)-occurrences
in \(D_c\cup D_d\) whose two endpoints lie in \(C\).  It has maximum
degree two; two differently coloured cells on one physical pair form a
parallel two-cycle.

**Lemma 2 (open Kempe rails).**  This graph has no cycle.  It is a
disjoint union of paths, including isolated vertices, and each path has
exactly two missing \(c/d\) incidences leading to \(X\).  In particular
there are at most \(|X|\leq7\) such paths.

**Proof.**  Suppose that a component \(P\) is a cycle.  Start with any
selected full constant-\(c\) matching \(M_c\), replace its alternating
\(c\)-occurrences on \(P\) by the \(d\)-occurrences, and colour \(P\) by
\(d\) and every other site by \(c\).  Since \(P\subset C\), this switch
does not change the selected residual matching on \(X\).  Formula (18),
followed by (11), gives the mixed coefficient

\[
 \frac{\prod_{e\in D_d\cap E(P)}w(e)}
      {\prod_{e\in D_c\cap E(P)}w(e)}\ne0.                    \tag{22}
\]

This contradicts the target.  Hence no cycle exists.

At every vertex of \(C\) there is one \(c\)-edge and one \(d\)-edge.
The two missing incidences of each path therefore go to \(X\).  By (10),
a site of \(X\) receives at most one incidence of each colour, hence at
most two \(c/d\) incidences.  Counting path ends gives at most \(|X|\)
paths.  \(\square\)

In the binary \(\{c,d\}\)-restriction, each such path has only two
possible matching states: all its \(c\)-edges or all its \(d\)-edges.
Once a state is chosen, it contributes a fixed nonzero product and a
fixed subset of its two core endpoints.  Formula (18) then evaluates the
rest on the uncovered core.  Thus suppressing a path loses no information
in that restriction: it is a deterministic weighted rail between at most
seven exceptional sites, not an additional unbounded matching problem.

## 6. Exclusion of every even order at least ten

Let

\[
                         b=|E_{\rm bad}(C,X)|.                  \tag{23}
\]

Equations (8) and (14) give the two bounds

\[
                         |X|(|C|-2)\leq b\leq3|C|.             \tag{24}
\]

There are no orders above twelve by (13) and (15).  If \(N=12\), then
necessarily \((|C|,|X|)=(5,7)\), but (24) would say \(21\leq b\leq15\).
Thus \(N=12\) is impossible.

It remains to exclude \(N=10\).  The only possible size pairs are

\[
                    (|C|,|X|)=(5,5),(4,6),(3,7).               \tag{25}
\]

For \((5,5)\), (24) forces \(b=15\).  All three edges at every cubic
vertex cross to \(X\).  Hence every \(D_c\) is a perfect matching between
the two five-sets.  The fourth matching \(R\subset D_0\cup D_1\cup D_2\)
has \(Y=\varnothing\), contradicting (20).

For \((4,6)\), (24) forces \(b=12\).  Again all cubic edges cross to
\(X\).  Each \(D_c\) covers four distinct vertices of \(X\), and the
remaining two vertices are joined by the unique physical pair in the
selected constant matching \(M_c\).  Every perfect matching in
\(M_0\cup M_1\cup M_2\) therefore uses four crossing edges and one
internal \(X\)-edge.  Its fourth mixed matching has \(|Y|=2\), again
contradicting (20).

Finally take \((3,7)\).  Every \(x\in X\) has bad degree at least seven,
while \(b\leq3|C|=9\).  If \(e_X\) is the number of bad pairs internal to
\(X\), then

\[
              2e_X
                 =\sum_{x\in X}\deg_{\rm bad}(x,X)
                 \geq 7|X|-b\geq49-9=40.                    \tag{26}
\]

Thus \(e_X\geq20\).  But a \(4\)-degenerate graph on seven vertices has
at most

\[
                       \binom52+4(7-5)=18                    \tag{27}
\]

edges.  This contradiction closes the last size pair and proves Theorem
1 for all \(N\geq10\).

At \(N=8\), (20) forces \(|X|\geq4\), so \(|C|\leq4\).  Together with
\(X\ne\varnothing\), (13), and \(C\ne\varnothing\), this gives (4).  The
set \(C\) is nonempty because \(|X|\leq7<N\).

## 7. Audit against the prism and Petersen repairs

The conclusion is deliberately a core response, not a false uniqueness
claim.  The Petersen replacement model in
[the selected-triple rewrite](triple-matching-rewrite.md) makes the audit
especially transparent.  Its full support is cubic only at vertices
\(0,5\); the eight endpoints of the added four-edge repair are

\[
                         \{1,2,3,4,6,7,8,9\}.                   \tag{28}
\]

The selected matching and its cancellation mate share the forced edge
\(05\), and their symmetric difference is an eight-cycle entirely on
the displayed set.  This is exactly the localization mechanism of
(18)--(19).  That model is not a globally flat exact source, so it does
not satisfy the additional \(4\)-degenerate bound (13); rather, it shows
why selected-rewrite reasoning alone cannot shrink an eight-site repair.

A triangular-prism repair whose selected matching and mate differ on four
or six vertices likewise does not contradict (19): its cancellation is
retained in the residual core coefficient.  What global flatness adds is
the sharp exceptional-set count and the elimination of every order above
eight.

## 8. Remaining gate

The globally flat branch is now an order-eight boundary problem.  A
continuation can work without large support enumeration:

1. choose a fourth matching in three normalized constant fibres;
2. use (18) to obtain its exact four- or six-site zero response;
3. compare a second fourth matching, or a second pair of open Kempe rails,
   whose forced boundary product uses the same core blocks.

The unresolved step is to show that these overlapping bounded responses
cannot all cancel.  The Petersen audit shows that one response is not
enough; the natural next invariant must couple two rail states or two
fourth-matching fibres on the same exceptional core.
