# Binary residual targets pay a sharp near-perfect-matching charge

## 1. Outcome

Work in the site-square-zero algebra on \(W\), where \(|W|=2h\) and
\(h\geq3\).  At an intrinsic scalar-unit pair retain the complete nine
rows

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
      +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,
 \qquad \alpha\ne0.                                      \tag{1}
\]

Put

\[
 Q=q^{[h]}=v_0X_0+v_1X_1+v_2X_2,
 \qquad S=\{i:v_i\ne0\}.                                \tag{2}
\]

The zero-coordinate branch has an exact combinatorial cost which is not
visible in the top tensor alone.

> **Theorem 1.1 (zero-coordinate near-perfect charge).**  For every
> \(\ell\notin S\), the residual quadratic \(q\) contains a nonzero
> monochromatic \(\ell\)-coloured near-perfect matching: there are two
> holes \(u\ne v\) and \(h-1\) nonzero \(\ell\ell\)-cells of \(q\)
> forming a perfect matching of \(W\setminus\{u,v\}\).  Moreover one of
> the two oriented products
> \[
>       (p_\ell)_{u,\ell}(s_\ell)_{v,\ell},\qquad
>       (p_\ell)_{v,\ell}(s_\ell)_{u,\ell}               \tag{3}
> \]
> occurs nontrivially in the same expanded response term.

Let \(q_S\) be the principal colour restriction obtained by retaining only
cells whose two endpoint colours lie in \(S\).  Projection is an algebra
map, so

\[
                         q_S^{[h]}=\sum_{i\in S}v_iX_i.   \tag{4}
\]

Consequently, when \(Q\ne0\),

\[
 \boxed{
 |S|=2\Longrightarrow |\operatorname {supp}q|\ge3h-1,
 \qquad
 |S|=1\Longrightarrow |\operatorname {supp}q|\ge3h-2.} \tag{5}
\]

In the binary case, equality in (5) forces the following support normal
form:

* the \(2h\) cells of \(q_S\) are the two weighted monochromatic factors
  of one alternating Hamilton cycle; and
* the remaining \(h-1\) cells are a monochromatic near-perfect matching in
  the missing colour.

In the unary case, equality consists of one \(h\)-cell monochromatic
perfect matching in the active colour and one \((h-1)\)-cell
near-perfect matching in each missing colour.  These are support
statements.  They do not say that a displayed off-target cell is
termwise inactive in every response or that mixed top matching terms
vanish separately.

The Hamilton-minimal binary subcase therefore has a precise answer.  If
one incorrectly requires the *whole* \(q\) to have only the \(2h\)
Hamilton cells, (1) is immediately contradictory: the row belonging to
the missing colour has no required near-perfect cofactor.  In the most
important normalization

\[
             S=\{b,c\},\qquad a\notin S,                 \tag{6}
\]

it is the exceptional row

\[
                 R_{aa}q^{[h-1]}=X_a-\alpha Q            \tag{7}
\]

whose \(X_a\)-coefficient gives the contradiction.  But if only the
active binary *face* is Hamilton-minimal, (7) instead forces the extra
\(h-1\) cells in (5).  It does not eliminate them.

There is a second exact Hamilton ledger.  Assume (6), let
\(H=q_{\{b,c\}}\), and suppose its \(2h\) cells are Hamilton-minimal.  If
the scalar-unit cap is clean,

\[
             (\alpha q+R_{aa})^{[h]}=\alpha^{h-1}X_a,    \tag{8}
\]

then, with \(r=(R_{aa})_{\{b,c\}}\), projection of (7)--(8) gives

\[
 \boxed{rH^{[h-1]}=-\alpha H^{[h]},\qquad
        (\alpha H+r)^{[h]}=0.}                           \tag{9}
\]

These equations are not contradictory.  A uniform adjacent-edge
rank-one switch below realizes (9) with arbitrary nonzero Hamilton
weights.  Thus the clean equation does not turn the charge in (5) into a
binary contradiction.

Finally, anchor-first lexicographic extremality does not promote \(q\) to
a least-cell representative of its top fibre.  If the global exact source
is chosen first with maximum mutual-anchor count and then with minimum
aggregate support in that stratum, it makes \(q\) minimal only in the
**anchor-preserving nine-row fibre**.  To state the scope precisely, put

\[
 \Delta_h=z^{[h]}-q^{[h]},\qquad
 \Delta_{h-1}=z^{[h-1]}-q^{[h-1]}.
\]

With the selected direct block and stars fixed, a general replacement is
exact if and only if

\[
 \boxed{
 R_{ij}\Delta_{h-1}=0\quad((i,j)\ne(a,a)),\qquad
 \alpha\Delta_h+R_{aa}\Delta_{h-1}=0.}                  \tag{10a}
\]

Thus the \(aa\)-row can in general cancel a change of top against a change
of adjacent power.  For the stronger comparison relevant to a binary
top-normal-form argument, one insists that \(z\) remain in the same top
fibre.  A lower-support top-preserving candidate is a legal lexicographic
comparison precisely when

\[
 \boxed{
 \begin{aligned}
 z^{[h]}&=q^{[h]},\\
 R_{ij}\bigl(z^{[h-1]}-q^{[h-1]}\bigr)&=0
                       &&(0\le i,j\le2),\\
 \nu(A[z])&\ge\nu(A[q]).
 \end{aligned}}                                         \tag{10}
\]

Indeed, the first line of (10) reduces (10a) to the second line, while the
third line keeps the replacement in the maximum-anchor stratum.  No binary
top normal-form theorem supplies either of those two additional conditions.
If one also wants to remain on the same clean cap, one must add

\[
                 (\alpha z+R_{aa})^{[h]}
                         =\alpha^{h-1}X_a.               \tag{11}
\]

The exact missing condition for this top-preserving route is therefore an
**anchor-preserving nine-row Hamiltonization**, not another top-only binary
classification.  A top-changing replacement satisfying (10a) is a distinct
possible descent mechanism and is not excluded here.

A six-site rational guard in Section 6 shows at the first admissible
residual order that the \(h-1\) charged cells can be invisible in
\(q^{[h]}\) and nevertheless detected by \(R_{aa}q^{[h-1]}\).  Deleting
them preserves the binary top but violates the second line of (10).

This gives a quantitative boundary theorem and a sharp no-go for the
minimality inference.  It is not a recurrence theorem, a full-source
guard, or a proof of Krenn's conjecture.

## 2. Proof of the near-perfect charge

Let \([X_i]\) denote literal coefficient restriction to the all-\(i\)
word.  The diagonal rows of (1) are

\[
 R_{ii}q^{[h-1]}=X_i\quad(i\ne a),\qquad
 R_{aa}q^{[h-1]}=X_a-\alpha Q.                           \tag{12}
\]

If \(v_\ell=0\), both cases give

\[
                  [X_\ell]\,R_{\ell\ell}q^{[h-1]}=1.   \tag{13}
\]

Expand the left side using \(R_{\ell\ell}=p_\ell s_\ell\), and then
expand the divided power over unordered decorated cells.  It is a finite
sum.  Since its value is nonzero, at least one summand is nonzero.  Such a
summand consists of

1. one \(\ell\)-coordinate of \(p_\ell\) at a hole \(u\);
2. one \(\ell\)-coordinate of \(s_\ell\) at a different hole \(v\), with
   the opposite endpoint assignment also allowed; and
3. a perfect matching of \(W\setminus\{u,v\}\) made from \(h-1\)
   nonzero \(\ell\ell\)-cells of \(q\).

Same-site products are zero, so the holes are distinct.  This proves
Theorem 1.1 without declaring any other summand zero and without
cancelling a matching power.

For the support bound, set every colour outside \(S\) to zero.  This is an
algebra homomorphism and proves (4).  If \(|S|=2\), the two nonzero constant
coefficients require \(h+h=2h\) distinct scalar cells in \(q_S\): one
nonzero perfect-matching monomial for each colour.  The theorem in
[`binary-entry-minimal-normal-form.md`](binary-entry-minimal-normal-form.md)
shows that equality is exactly the alternating Hamilton form.  The
argument is unchanged for nonzero coefficients \(v_i\): the two selected
factor products are \(v_i\), or equivalently one selected cell in each
colour may be rescaled to normalize the target first.  The
missing-colour witness supplies another \(h-1\) cells, all outside
\(q_S\).  This proves the first bound in (5) and its equality statement.

If \(|S|=1\), its nonzero constant coefficient requires \(h\) active-colour
cells.  At equality those cells are one perfect matching.  Each of the two
missing labels contributes \(h-1\) further same-colour cells.  Cells with
different endpoint colours are distinct even when their underlying
physical pair agrees, proving the second bound and equality statement.
For completeness, \(Q=0\) gives the weaker but sometimes useful bound

\[
                         |\operatorname {supp}q|\ge3(h-1). \tag{14}
\]

In the complementary binary normalization (6), every pure coefficient of
(7) is nonzero:

\[
 [X_a]R_{aa}q^{[h-1]}=1,\qquad
 [X_b]R_{aa}q^{[h-1]}=-\alpha v_b,\qquad
 [X_c]R_{aa}q^{[h-1]}=-\alpha v_c.                       \tag{15}
\]

The same finite-sum argument now shows that each of \(p_a,s_a\) has at
least one scalar coordinate of each of the three colours.  Hence

\[
                  |\operatorname {supp}p_a|\ge3,qquad
                  |\operatorname {supp}s_a|\ge3.         \tag{16}
\]

This three-port lower bound is independent of goodness.  Goodness gives
injectivity of the complete triples, but does not reduce the support cost.

## 3. The exact Hamilton response equations

Continue with (6) and suppose \(H=q_{\{b,c\}}\) has the Hamilton normal
form.  Write its alternating factors as \(P_b,P_c\), and let \(w_e\ne0\)
be the scalar on the \(ii\)-cell of \(e\in P_i\).  Thus

\[
              \prod_{e\in P_i}w_e=v_i\qquad(i=b,c).     \tag{17}
\]

Projection of (7) to the active colour plane gives the first equation in
(9), while projection of (8) gives the second.  The pure coordinates of
the first equation are especially concrete.  If \(r_e^{ii}\) denotes the
\(ii\)-cell of \(r\) on \(e\in P_i\), then

\[
 \boxed{\sum_{e\in P_i}{r_e^{ii}\over w_e}=-\alpha
                   \qquad(i=b,c).}                      \tag{18}
\]

Indeed, after one \(ii\)-cell is supplied by \(r\), the only all-\(i\)
Hamilton cofactor is \(P_i\setminus\{e\}\), of weight \(v_i/w_e\).
Equation (18) is cancellation-aware: it constrains the sum of all such
response placements rather than choosing one.

The remainder of \(r\) is constrained by the mixed coordinates in the
first equation of (9), and the second equation is nonlinear.  Neither
condition forces \(r=0\).  The following construction is the smallest
local reason.

Number the Hamilton cycle \(0,1,\ldots,2h-1\), with

\[
 P_b=01|23|\cdots|(2h-2,2h-1),\qquad
 P_c=12|34|\cdots|(2h-1,0).                              \tag{19}
\]

Let the weights of \(01\in P_b\) and \(12\in P_c\) be \(B,C\ne0\), and
put

\[
 u=e_b^{(0)}+e_c^{(1)},\qquad
 v=-\alpha B e_b^{(1)}-\alpha C e_c^{(2)},\qquad r=uv.  \tag{20}
\]

The same-site product at site \(1\) vanishes, so

\[
 r=-\alpha B\,e_b^{(0)}e_b^{(1)}
   -\alpha C\,e_c^{(1)}e_c^{(2)}
   -\alpha C\,e_b^{(0)}e_c^{(2)}.                       \tag{21}
\]

The first two cells replace one edge of \(P_b,P_c\) and give
\(-\alpha v_bX_b,-\alpha v_cX_c\).  The last cell joins sites \(0,2\),
which lie on the same Hamilton shore; its Hamilton cofactor is zero.
This proves the first equation of (9).

In \(\alpha H+r\), the \(01\) and \(12\) cells cancel, while the new
\(02\) cell remains.  Site \(1\) is isolated in the resulting physical
support: its only two Hamilton edges were \(01,12\), and the chord \(02\)
does not meet it.  Hence there is no perfect matching and

\[
                         (\alpha H+r)^{[h]}=0.            \tag{22}
\]

This proves (9) uniformly, with a literal rank-one response and arbitrary
nonzero Hamilton weights.  It is a projected guard, not a completion of
the missing-colour row.

## 4. What anchor-first extremality actually says

Suppose the full source is chosen with maximum mutual-coordinate-anchor
count \(\nu\), and then with minimum aggregate scalar-cell support among
those sources.  Keep the selected direct block and stars fixed, and replace
only the internal quadratic \(q\) by \(z\).  Expanding the full matching
tensor by the partners of the two selected sites shows that the replacement
is exact if and only if its nine rows are exact.  Relative to the old rows,
the general difference system is (10a).  Within the top-preserving subclass
\(\Delta_h=0\), it reduces precisely to the first two lines of (10).

If in addition \(\nu(A[z])\ge\nu(A[q])\), global maximality makes the two
anchor counts equal.  A strict decrease in \(|\operatorname {supp}z|\)
would then contradict the secondary support minimum.  Conversely, a
top-only Hamilton representative supplies only \(z^{[h]}=Q\).  It need not
annihilate any of the nine adjacent-power differences, and deleting its
cells may destroy internal mutual anchors.  Thus this top-preserving
Hamilton comparison gives no descent unless all of (10) has first been
constructed.  A top-changing comparison would instead have to satisfy
(10a), preserve the anchor stratum, and lower support.

The clean scalar-unit hypotheses do give the already known survival fork,
but not Hamiltonization.  For this paragraph assume additionally that the
selected pair is good and that its unary cap is clean, equivalently (8).
Put

\[
 G=\alpha q+R_{aa},\qquad
 \Theta_a=G^{[h-1]}-\alpha^{h-1}q^{[h-1]}.              \tag{23}
\]

At the anchor-first lexicographic representative, goodness, cleanliness,
and the anchor-preserving support-decreasing row-deletion argument give

\[
                              \Theta_a\ne0.              \tag{24}
\]

If all four complementary products

\[
                    R_{ij}\Theta_a=0\qquad(i,j\ne a)    \tag{25}
\]

also vanished, the complementary scalar-unit pivot would be an exact
same-order source and would create a new mutual anchor while preserving
all old ones.  This contradicts maximum \(\nu\).  Therefore

\[
                    (R_{ij}\Theta_a)_{i,j\ne a}\ne0.    \tag{26}
\]

These extra global, good-pair, and clean-cap hypotheses are essential to
(24)--(26); those conclusions do not follow from the local nine rows and a
binary top alone.  Equations (24)--(26) force a surviving normal comparison.
They do not make a top-inactive cell response-inactive, bound the binary
excess from above, or produce a recurrence move.  In fact (16) places the
complementary binary branch at the \(3\)-by-\(3\)-or-larger star-support
boundary, where the elementary pivot support ledger permits an internal
increase.

## 5. The exact missing replacement theorem

It is useful to name the absent statement without hiding it under the word
"minimality."

> **Anchor-preserving nine-row Hamiltonization (missing).**  Given a
> binary-top residual \(q\) in the lexicographically selected full source,
> construct a lower-support \(z\) satisfying (10).

The top binary normal form does not prove this statement.  Nor does the
fact that a cell is absent from every full matching of \(q\): the cell may
occur after two sites have been occupied by a response.  The second line
of (10) is exactly the requirement that all such response activity be
preserved.  A coordinated change of the stars could be allowed, but then
all nine new rows, total support change, and anchor persistence would have
to be checked together; that is a stronger replacement theorem, not a
consequence of the current extremal choice.

The quantitative theorem therefore leaves three honest possibilities:

1. the binary face has Hamilton support and the missing colour pays the
   \(h-1\) near-perfect charge;
2. the binary face itself has excess support, possibly needed by the same
   nine response cofactors; or
3. a future anchor-preserving nine-row replacement removes one of these
   excesses and gives a genuine source descent.

No counting argument presently excludes the first two.

## 6. A smallest rational top/cofactor guard

The following guard lives at \(h=3\), the first residual order allowed in
the scalar-unit branch.  It is exact in the literal site algebra and uses
only coefficients \(0,\pm1\).  Write \(a=0,b=1,c=2\) on sites
\(0,\ldots,5\), and put

\[
\begin{aligned}
q={}&e_b^{(0)}e_b^{(1)}+e_b^{(2)}e_b^{(3)}
       +e_b^{(4)}e_b^{(5)}\\
 &+e_c^{(1)}e_c^{(2)}+e_c^{(3)}e_c^{(4)}
       +e_c^{(5)}e_c^{(0)}\\
 &+e_a^{(1)}e_a^{(5)}+e_a^{(2)}e_a^{(4)}.               \tag{27}
\end{aligned}
\]

The underlying graph is the six-cycle plus the chords \(15,24\).  A
perfect matching using \(15\) strands site \(0\), and one using \(24\)
strands site \(3\).  Hence its only perfect matchings are the two cycle
factors, and

\[
                              q^{[3]}=X_b+X_c.            \tag{28}
\]

The last two cells in (27) occur in no full matching at all.  Nevertheless
they form an all-\(a\) near-perfect matching on the complement of
\(\{0,3\}\).  Thus, for \(d=e_a^{(0)}e_a^{(3)}\),

\[
                         [X_a]\,d q^{[2]}=1.              \tag{29}
\]

This attains the \(3h-1=8\) support ledger exactly and proves that deleting
top-inactive cells need not preserve an exceptional response.

There is a combined three-port version.  Set

\[
 p_a=e_a^{(0)}+e_b^{(0)}+e_c^{(1)},\qquad
 s_a=e_a^{(3)}-e_b^{(1)}-e_c^{(2)},\qquad R=p_as_a.      \tag{30}
\]

For a word \(\omega=(\omega_0,\ldots,\omega_5)\), write \(X_\omega\)
for its coordinate monomial.  Direct multiplication gives

\[
\begin{aligned}
Rq^{[2]}={}&X_a-X_b-X_c+{\cal R}_1,\\
(q+R)^{[3]}={}&X_a+{\cal R}_2,                            \tag{31}
\end{aligned}
\]

where

\[
\begin{aligned}
{\cal R}_1={}&-X_{002220}-X_{011111}+X_{022011}+X_{100000}\\
              &-X_{102220}+X_{122011}+X_{220002},\\
{\cal R}_2={}&-X_{002220}-X_{011111}-X_{022011}+X_{100000}\\
              &-X_{102220}-X_{122011}+X_{220002}.         \tag{32}
\end{aligned}
\]

Thus this one packet simultaneously has

* the Hamilton-minimal active binary face;
* the sharp \(h-1\) missing-colour charge;
* one coordinate of every colour in each selected star row;
* the exact active-face projection (9) with \(\alpha=1\); and
* the correct three pure coefficients of both the exceptional row and the
  clean unary equation.

It fails exactly at the displayed mixed fibres (and no companion eight
rows are asserted).  This is why it is a **lower-level guard**, not an
exact ternary source.  It identifies the additional information a closing
argument must use: simultaneous vanishing/cancellation of all mixed
coefficients in (7)--(8), the other eight full-source rows, and the
anchor-preserving replacement condition (10).  Pure targets, Hamilton
support, and top inactivity alone do not supply any of them.

## 7. Exact audit and scope

The dependency-free checker
[`verify_scalar_unit_binary_residual_target_branch.py`](../computations/verify_scalar_unit_binary_residual_target_branch.py)
implements the literal site-square-zero algebra over
`fractions.Fraction`.  It verifies the weighted adjacent-edge switch for
several orders, reconstructs every coefficient of (27)--(32), enumerates
the six-site supported perfect matchings, checks the sharp support and
near-perfect charges, and includes sign/deletion mutations.  It uses
explicit exceptions rather than Python `assert`, so all tests remain live
under `python -O`.

The uniform statements are proved above; the finite runs audit signs,
divided-power normalization, endpoint order, and the sharp rational guard.
Nothing here proves that the mixed residues in (32) can occur in a full
exact source, or that they cannot be cancelled in one.  The conjecture
remains open.
