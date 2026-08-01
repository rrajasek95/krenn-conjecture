# The terminal class is invisible to the matching tensor

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.  This note records a
grading on decorated block arrays, its immediate consequence for what a
landing theorem can possibly say, and the four-hole grade ladder that comes
with it.

## 1. Outcome

Give the block array a grading: internal quadratic edges weight \(-1\),
endpoint star edges weight \(+1\), the direct scalar weight \(+3\).  Then
**every coefficient of the eight-site matching tensor has weight zero**,
while the terminal class \(\chi\) has weight six.  Concretely, for every
\(\tau\neq0\) the substitution

\[
 \boxed{\;q\mapsto q/\tau,\qquad p\mapsto\tau p,\qquad s\mapsto\tau s,
 \qquad d\mapsto\tau^3d\;}
\]

fixes every one of the \(9\times729\) row coefficients, in every chart, for
every packet, while

\[
 \chi\longmapsto\tau^6\chi .
\]

The proof is a two-line count and is given in section 2.

The consequence is a restriction on every future attack on the landing:

> \(\chi\) is **not a function of the matching tensor**.  If it were, say
> \(\chi=F(\text{rows})\), then \(\chi=\tau^6\chi\) for all \(\tau\), hence
> \(\chi\equiv0\) — false, because the audited seven-row guard has
> \(\chi=-2\).

So a landing theorem can only ever be a **vanishing** statement
("all nine rows \(\Longrightarrow\chi=0\)").  There is no formula for
\(\chi\) in terms of row values, and no quantitative bound
\(|\chi|\leq\Phi(\text{row residuals})\) of any shape.  The same applies to
every quantity of nonzero weight, including \(Q_2\), \(Q_3\), the response
contraction \(\langle R,H_1\rangle\), and the twenty committed cut values.
Only weight-zero data can be read off the tensor.  Two things this does not
exclude: a relation normalizing \(\chi\) by another weight-six quantity of the
packet — section 4's own formula for \(\chi\) is of that kind — and a
nonzero-weight quantity being a function of the tensor on a locus where it
vanishes identically, which is exactly what a landing theorem asserts.

This also strengthens the committed
[seven-row guard](h3-diagonal-segre-second-transgression-seven-row-guard.md).
That packet is not a point but a one-parameter family.  Identical across the
family: the eight-site matching tensor \(X_2\), the missing-target ledger
\((00,0^6,-1)\), \((11,1^6,-1)\), and the full \(27\times243\) adjacent
decomposition.  Preserved but not fixed: star entries scale by \(\tau\) and
responses by \(\tau^2\), so it is the endpoint-star *ranks* and the Segre
*identities* that survive, not the entries.  Meanwhile \(\chi=-2\tau^6\) is
unbounded.  The guard therefore rules out not
merely "a packet with \(\chi=-2\)" but any bound on \(\chi\) in terms of the
retained data.

## 2. The grading

The eight vertices are the six residual sites and the two endpoints.  A
perfect matching of the block array is one of exactly two shapes.

* It uses the direct edge, and then three internal edges: weight
  \(3+3(-1)=0\).  There are \(15\) of these.
* It uses one star edge at each endpoint, and then two internal edges:
  weight \(1+1+2(-1)=0\).  There are \(6\cdot5\cdot3=90\) of these.

That is all \(15+90=105=7!!\) perfect matchings, each of weight zero, so
every matching-tensor coefficient is weight zero and the displayed
substitution fixes it.  For the terminal class, \(R=ps\) has weight \(2\)
and \(\alpha=d_{ab}\) has weight \(3\), so with \(Q_j=R^{[j]}q^{[3-j]}\),

\[
 \operatorname{wt}Q_j=3j-3,\qquad
 \operatorname{wt}\chi=\operatorname{wt}(\alpha Q_2)
 =\operatorname{wt}Q_3=6 .
\]

The jet basis of the
[blindness guard](fourhole-cap-polarization-terminal-blindness.md) is
homogeneous for this grading, with \(J_0,J_1,J_2,J_3\) at weights \(0,3,6,9\)
and \(\operatorname{wt}H_k=3k-2\).  That note assigns no weights itself; the
grading is put on it here.

The group action itself is **not** new.  It is a one-parameter subgroup of
the repository's target-stabilizing torus (`combinatorial-route.md`, section 4,
equations (7)–(8); `finite-obstruction.md`, equation (14)), equivalently the
universal scalar vertex gauge \(A_{uv}\mapsto\lambda_u\lambda_vA_{uv}\) of
`minimal-norm-gauge.md`, equation (29), taken at \(\lambda_v=\mu\) on the six
sites and \(\mu^{-3}\) at the two endpoints with \(\tau=\mu^{-2}\), so that
\(\prod_v\lambda_v=1\).  That such a gauge fixes the matching tensor term by
term is already stated there, and the eight-vertex form with endpoints
\(6,7\) is used routinely, for instance in equation (12) of
`three-cut-internal-23-two-cell-fourth-cut-obstruction.md`.

What is new is the **weight ledger** it induces on the response data —
\(\operatorname{wt}Q_k=3k-3\), \(H_k=3k-2\), \(J_k=3k\), \(\chi=6\),
\(C_k=3k-4\) — and the consequence for landing theorems.  No prior occurrence
of those was found.  (This is also distinct from the uniform colour torus of
[`h3-nonclean-twojet-middle-core.md`](h3-nonclean-twojet-middle-core.md),
which is a response translation \(\hat q(t)=q+2tR+2\alpha t^2R\), not a group
action on the array.)

## 3. The all-word four-hole identity

Write \(q^w(x,y)=q(x,y,w_x,w_y)\) for the internal quadratic read at the
word \(w\), \(R^w_{ij}(x,y)=p_i(x,w_x)s_j(y,w_y)+p_i(y,w_y)s_j(x,w_x)\), and
\(H(A)_e=\operatorname{haf}(A[W\setminus e])\).  Then for **every** word and
every label pair,

\[
 \boxed{\operatorname{Row}(i,j,w)
 =\bigl\langle\tfrac{d_{ij}}3q^w+R^w_{ij},\;H(q^w)\bigr\rangle .}
\]

The proof is one line: the direct term is \(d_{ij}\operatorname{haf}(q^w)\),
and \(\langle q^w,H(q^w)\rangle=3\operatorname{haf}(q^w)\) because each
perfect matching is recovered once from each of its three edges.  Nothing
about colour enters, so the identity holds for arbitrary decorated \(q\),
cross-colour edges included.

Two consequences worth stating separately.

* The \(27\) pure-word equations of a full-nine packet are exactly nine caps
  paired against three grade-zero four-hole vectors.  **The diagonal anchor
  sector and the four-hole interface are the same object.**  This is the kind of
  entry point the blindness guard was missing when it concluded, on the
  seven-row guard specifically, that the diagonal sector must enter before the
  pairing; that note's statement is packet-local, and this one is not.
* At the pure word, \(\operatorname{Row}(i,j,c^6)=d_{ij}Q_0+Q_1=J_0\).  The
  "selected source relation \(\alpha Q_0+Q_1=0\)" is therefore not an extra
  hypothesis; it is the physical pure-word row of any label pair whose
  target is zero.

With a monochromatic \(q\) the identity refines by colour class.  Every word
has zero or two odd colour classes — three is impossible, since the class
sizes sum to six.  On the \(183\) all-even words the row is a sum over
colours of a class-restricted four-hole pairing times the hafnians of the
other classes; on the \(546\) two-odd words the direct term dies entirely
and the row becomes a star product straddling the two odd classes.  Freeing
the cross-colour edges destroys this refinement rather than perturbing it:
the direct term revives at two-odd words.

## 4. The grade ladder, and where the rows stop

Every monomial of every row polynomial has \(p\)-degree and \(s\)-degree
exactly equal and at most one.  So each row is a grade-zero four-hole
pairing and nothing more, whereas
\(\chi=\tfrac\alpha2\langle R,H_1\rangle+\tfrac13\langle R,H_2\rangle\) is
response-quadratic and response-cubic.  Reading the contractions off against
the weight:

* \(\langle R,H_0\rangle=Q_1\), weight \(0\) — the entire row content;
* \(\langle q,H_1\rangle=2Q_1=2\langle R,H_0\rangle\), weight \(0\), and so
  grade-zero data in disguise rather than anything new;
* \(\langle R,H_1\rangle=2Q_2\), weight \(3\) — **the first datum the rows do
  not control**;
* \(\langle q,H_2\rangle=Q_2\) and \(\langle R,H_2\rangle=3Q_3\), weights
  \(3\) and \(6\) — grade two is entirely out of reach.

The double-polar covariant is no better: its response grades
\(C_k=[t^k]\bigl(H(H(A))-2\mathcal B(A)\bigr)=Q_kq+Q_{k-1}R\) have weight
\(3k-4\), and \(3k-4=0\) has no integer solution, so no grade of that
identity is weight zero either.

Finally, the only row datum entering \(\chi\) at all is the source jet:

\[
 \operatorname{haf}(A_{\rm cap})=\alpha^2\operatorname{Row}(i,j,c^6)+\chi,
 \qquad\text{so}\qquad
 \chi=\operatorname{haf}(d_{ij}q_c+R^c_{ij})-d_{ij}^2\operatorname{Row}(i,j,c^6).
\]

For an off-diagonal selected row the row term vanishes and \(\chi\) is
exactly the cap hafnian.  The residual is the pure grade-\(\{1,2\}\) part,
which by the weight count no row controls.

## 5. What this does not say

1. **It does not refute the landing.**  \(\chi\equiv0\) on the row variety is
   precisely the \(\tau\)-invariant case, and is entirely consistent with
   everything here.  What is ruled out is a class of *proof attempts*:
   computing \(\chi\) from row data, or bounding it by row residuals.
2. **It does not make the guards weaker or stronger as statements** — it
   explains them.  Every audited guard so far exhibits \(\chi\) uncontrolled
   by row data; the weight count says that had to happen.
3. **It says nothing about which vanishing arguments succeed.**  The
   admissible shape is a vanishing argument on the row ideal, of the kind the
   [star-sector trade](h3-star-sector-anchor-terminal-class-trade.md) carries
   out inside its ansatz.  Whether one exists in general is the open target.
4. The \(\tau\)-family lives among rational decorated block arrays, which is
   the class the audited guard already inhabits — it uses entries \(1/2\) and
   \(-1\).  A model restricting entries to a subring realizes fewer \(\tau\),
   but the weight count itself is unaffected.

## 6. Audit

The dependency-free checker
[`verify_fourhole_allword_row_identity_grade_ladder.py`](../computations/verify_fourhole_allword_row_identity_grade_ladder.py)
verifies the all-word identity as a formal polynomial identity over all
monomials, on all \(729\) words and all nine label pairs, in both the
monochromatic and the cross-colour model; the two monochromatic class forms
on the \(183\) even and \(546\) two-odd words, and the exact cross-colour
break; response-affineness and weight-zero-ness of every row monomial; the
weights of \(Q_k,H_k,J_k,\chi\); the grade-ladder contractions; the cap
split \(\operatorname{haf}(A_{\rm cap})=\alpha^2J_0+\chi\); that all \(105\)
perfect matchings are weight zero in both audited charts, re-derived from
each chart's own code; that the rank-two clean packet stays clean with its
twenty committed cut values at weight six; and the seven-row guard
\(\tau\)-family with identical tensor, ledger, star ranks, Segre rectangles
and adjacent \(27\)-rows at \(\chi=-2\tau^6\).

Standard library only, exact `Fraction` arithmetic, about seven seconds,
passing normal, `-O` and `-I -S`, and deterministic across hash seeds.

The \(\tau\)-invariance was independently re-derived against the committed
guard checker's own packet at \(\tau=2,-3,\tfrac12,5,-\tfrac27\): all
\(6561\) row coefficients identical, \(\chi/\chi_0=\tau^6\) exactly in every
case.
