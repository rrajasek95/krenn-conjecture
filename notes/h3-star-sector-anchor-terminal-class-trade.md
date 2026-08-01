# The diagonal anchor and the terminal class annihilate each other

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.  This is a guard in the
sense of [`terminal-bianchi-handoff-guide.md`](terminal-bianchi-handoff-guide.md),
and it executes that guide's stated next concrete step.

## 1. Outcome

The guide asked for a **star-sector repair** of the audited seven-row guard:
keep the colour-2 slice that pins \(\chi=-2\), add colour-0 and colour-1
material to the endpoint stars and to the internal quadratic, impose all
\(9\times729\) rows, and find out whether \(\chi\) can stay nonzero.  It also
asked that failure be pinned as an explicit residual formula rather than a
heuristic.

Call the six off-diagonal rows together with the complete \(22\) row, on all
\(729\) words, **the seven rows**.  The guard itself satisfies them, so that
system is consistent and everything below is an identity on a non-empty
variety.  On it,

\[
 \boxed{\;q_c(2,3)\cdot\chi=0\qquad(c=0,1),\;}
\]

where \(q_c(2,3)\) is the sole carrier of the colour-\(c\) diagonal anchor and
\(\chi\) is the terminal class of the selected \((0,1)\) cap **on the frozen
colour-2 slice**, that is the cap at the pure word \(2^6\).  The identity is
literally \(-2\) times a single row equation at a single word.  The same holds
for the \((0,2)\) cap with factor \(\tfrac12\), and those two are the only
caps on this slice with a nonzero class.

So the anchor and the class cannot both be live.  The guard sits at
\(q_c(2,3)=0\), \(\chi=-2\); at the other end, restoring an anchor forces
\(\chi=0\).  That end is attainable: there is an explicit packet with the
seven rows and \(\operatorname{Row}(0,0,0^6)=1\), and it has \(\chi=0\) exactly
as the identity predicts — see
[the witness note](h3-star-sector-pure-word-anchor-witness-and-colour-asymmetry.md),
which also shows the colour-1 anchor is impossible even at its pure word.

Two infeasibility corollaries, by exhaustive branching over the monochromatic
ansatz of section 2: the seven rows plus the **complete** colour-\(c\) anchor
row have no solution, for \(c=0\) and for \(c=1\); hence neither does the full
nine-row system.  Within that ansatz the star-sector repair therefore fails
outright, not merely in the class-preserving direction.  The cross-colour
completion of the same repair is untouched by this and remains open; see
section 9.2.

Every identity below is formal, over all monomials in all \(111\) repair
unknowns; the infeasibility statements of section 7 are exhaustive case
analyses rather than identities.  Nothing is verified on random samples.

## 2. The ansatz

Six residual sites \(W=\{0,\dots,5\}\), two endpoints, three colours.  A
packet has internal quadratic \(q\), endpoint stars \(p_i(x,c)\), \(s_j(y,c)\),
and direct block \(d_{ij}\), with row coefficients

\[
 \operatorname{Row}(i,j,w)=d_{ij}\operatorname{haf}_w(q)
  +\sum_{x<y}\bigl[p_i(x,w_x)s_j(y,w_y)+p_i(y,w_y)s_j(x,w_x)\bigr]
   \operatorname{haf}_w\bigl(q|_{W\setminus\{x,y\}}\bigr),
\]

and the nine-row system is
\(\operatorname{Row}(i,j,w)=\mathbf 1_{i=j,\,w=i^6}\) on all \(729\) words.

**Frozen** — copied verbatim from the audited guard checker — the whole
colour-2 slice: \(q_2=z_0z_1+z_4z_5\) and

\[
\begin{aligned}
 p_0&=z_0+z_1,&p_1&=z_4,&p_2&=z_2+z_3,\\
 s_0&=z_5,&s_1&=z_2-z_3,&s_2&=\tfrac12(z_2+z_3).
\end{aligned}
\]

**Free** — all nine direct scalars; every colour-0 and colour-1 star entry;
and the colour-0 and colour-1 internal quadratics, taken **monochromatic**.
That restriction is the ansatz's one real hypothesis, and section 9 shows it
is not cosmetic.

Freezing the colour-2 slice is what keeps the class alive: \(\chi\) is
computed from \(d_{ab}\), the colour-2 star vectors and \(q_2\) alone, so no
colour-0/1 addition can disturb it.

## 3. The seven rows collapse the repair sector

The guard's **own** seven rows force \(32\) of the \(111\) unknowns to zero.
Neither restored anchor row is used.

\[
 p_0(2,c)=p_0(3,c)=p_1(2,c)=p_1(3,c)=s_0(2,c)=s_0(3,c)=0\qquad(c=0,1),
\]
\[
 \operatorname{supp}q_c\subseteq\bigl\{\{0,4\},\{0,5\},\{1,4\},\{1,5\},\{2,3\}\bigr\}
 \qquad(c=0,1).
\]

Both families come from the same degeneracy.  Since \(q_2\) is the two
disjoint edges \(01\) and \(45\), the four-site colour-2 hafnian
\(\operatorname{haf}(q_2|_T)\) is nonzero for exactly one four-set,
\(T=\{0,1,4,5\}\).  A word carrying colour \(c\) on a pair \(\{x,y\}\) and
colour 2 elsewhere therefore reduces to

\[
 \operatorname{Row}(i,j,w)=q_c(x,y)\,\rho_2\bigl(i,j,W\setminus\{x,y\}\bigr)
  +\operatorname{haf}(q_2|_{W\setminus\{x,y\}})\,
   \bigl[p_i(x,c)s_j(y,c)+p_i(y,c)s_j(x,c)\bigr],
\]

and for the fourteen pairs other than \(\{2,3\}\) the second term drops while
the frozen four-site row \(\rho_2\) is nonzero for ten of them, killing those
\(q_c(x,y)\).  The single-site words give the star entries: at
\(w=(2,2,c,2,2,2)\) the \((0,1)\) row is
\(p_0(2,c)s_1(3,2)+p_0(3,2)s_1(2,c)=-p_0(2,c)\).

What survives is the bipartite graph \(\{0,1\}\times\{4,5\}\) together with the
isolated edge \(\{2,3\}\).

## 4. The anchor peels onto one edge

Sites \(2\) and \(3\) now carry no colour-\(c\) internal edge except the one
joining them.  Every colour-\(c\) matching on six sites, and every one on a
four-site complement other than \(\{0,1,4,5\}\), must use \(\{2,3\}\); and the
one term that could avoid it — the star pair \(\{2,3\}\) — is annihilated by
\(p_c(2,c)=p_c(3,c)=0\) from section 3.  Hence

\[
 \boxed{\operatorname{Row}(c,c,c^6)=q_c(2,3)\,\rho_c\bigl(c,c,\{0,1,4,5\}\bigr),}
\]
\[
\begin{aligned}
 \rho_c\bigl(c,c,\{0,1,4,5\}\bigr)
 ={}&d_{cc}\bigl(q_c(0,4)q_c(1,5)+q_c(0,5)q_c(1,4)\bigr)\\
 &+q_c(0,4)\bigl[p_c(1,c)s_c(5,c)+p_c(5,c)s_c(1,c)\bigr]\\
 &+q_c(0,5)\bigl[p_c(1,c)s_c(4,c)+p_c(4,c)s_c(1,c)\bigr]\\
 &+q_c(1,4)\bigl[p_c(0,c)s_c(5,c)+p_c(5,c)s_c(0,c)\bigr]\\
 &+q_c(1,5)\bigl[p_c(0,c)s_c(4,c)+p_c(4,c)s_c(0,c)\bigr].
\end{aligned}
\]

All ten monomials carry \(q_c(2,3)\), so a live anchor forces
\(q_c(2,3)\neq0\).

There is a structural reason for the shape.  For every word and every label
pair,
\(\operatorname{Row}(i,j,w)=\langle\tfrac{d_{ij}}3q^w+R^w_{ij},H(q^w)\rangle\)
with \(H(A)_e=\operatorname{haf}(A[W\setminus e])\) — the pure-word rows are
grade-zero four-hole pairings, and the frozen slice has
\(|\operatorname{supp}H_0(q_2)|=1\), that one element being \(\{2,3\}\).  See
[the weight-grading note](terminal-class-weight-invisibility-and-fourhole-grade-ladder.md).

## 5. The trade

At the witness word \(w_c\) — colour \(c\) on \(\{2,3\}\), colour 2 elsewhere —
we have \(\operatorname{haf}(q_2|_{W\setminus\{2,3\}})=1\) and
\(\rho_2(i,j,\{0,1,4,5\})=d_{ij}+\mathbf 1_{(i,j)=(1,0)}\).  Seven of the nine
label pairs have their star bracket killed by section 3, giving

\[
 d_{ij}\,q_c(2,3)=0\quad\text{for }(i,j)\in\{00,01,02,11,12,20\},
 \qquad
 (1+d_{10})\,q_c(2,3)=0,
\]

with only \((2,1)\) and \((2,2)\) retaining a star correction.  So a live
anchor pins seven of the nine direct scalars: \(d_{10}=-1\) and the six
members of \(\{00,01,02,11,12,20\}\) vanish, while \((2,1)\) and \((2,2)\) are
pinned only modulo their star correction and are genuinely free — there are
seven-row solutions with a live anchor and \(d_{22}\) any rational.  In
particular \(d_{cc}=0\): **the
restored anchor cannot be carried by its own direct scalar.**  Unlike L3 of
[`three-anchor-internal-quadratic-leak.md`](three-anchor-internal-quadratic-leak.md)
this needs no hypothesis on the stars and no non-negativity; it does use the
seven rows, \(q_c(2,3)\neq0\), and the \((c,c)\) row at \(w_c\), and section 7
shows the last of those cannot be met together with the complete \((c,c)\)
row.

Four of these come from the seven rows alone: \((0,1)\), \((0,2)\), \((1,2)\),
\((2,0)\), plus the shifted \((1,0)\).  The \((0,0)\) and \((1,1)\) members
need the restored anchor rows.

## 6. The product identity

On the frozen slice the graded cap layers of \(d_{ab}q_2+R_{ab}\) vanish for
every label pair except

* \((0,1)\): \((0,0,-2d_{01},0)\), so \(\chi=-2d_{01}\);
* \((0,2)\): \((0,0,\tfrac12d_{02},0)\), so \(\chi=\tfrac12d_{02}\);
* \((2,2)\): \((0,d_{22}^{2},0,0)\).  Its unscaled layers are
  \((Q_0,Q_1,Q_2,Q_3)=(0,1,0,0)\), so \(\alpha Q_0+Q_1=1\neq0\) for every
  \(\alpha\) and the row is not an admissible selected row.

Combining with section 5, on the seven-row variety

\[
 q_c(2,3)\cdot\chi=-2\,\bigl[\text{the }(0,1)\text{ row equation at }w_c\bigr]=0,
\]

and likewise \(q_c(2,3)\cdot\chi_{(0,2)}=\tfrac12[\,(0,2)\text{ row at }w_c\,]=0\).
This is the residual formula the guide asked for.  The coupling is exact and
localized at one edge: the anchor's carrier is precisely what the
off-diagonal rows use to annihilate the direct scalars carrying the class.

It sharpens **L0** of the leak note, which says an anchor needs two disjoint
colour-\(c\) edges *somewhere* — the surviving support has them, so L0 alone
does not close this route.  What closes it is the localization onto the
specific edge \(\{2,3\}\).

## 7. Infeasibility

Each claim is decided by splitting single-monomial equations into their
factors, valid over a field, and propagating forced single-variable
equations; all branches close.

* Seven rows \(+\) the complete colour-0 anchor row: infeasible.  Branch A,
  \(q_0(2,3)=0\), makes the anchor equation the constant \(-1\); branch B,
  \(q_0(2,3)\neq0\), licenses the trade substitutions and closes over \(486\)
  nodes.
* The same for colour 1, over \(2636\) nodes.
* The full nine-row system: infeasible, over \(533\) nodes.

Node counts depend on the branch ordering of the implementation and are
regression tripwires, not invariants; the mathematical content is that no
leaf survives.

## 8. Is the hypothesis attainable?

Yes for colour 0, no for colour 1 — see
[the witness note](h3-star-sector-pure-word-anchor-witness-and-colour-asymmetry.md).
The witness is the guard plus \(q_0=z_1z_5+z_2z_3\), \(p_0(0,0)=1\),
\(s_0(4,0)=1\) and \(d_{10}=-1\) in place of \(d_{01}\); it satisfies all
\(5103\) seven-row coefficients and \(\operatorname{Row}(0,0,0^6)=1\), has
rank-three stars and every literal Segre rectangle, and has \(\chi=0\) on
every admissible cap.  For colour 1, \(\operatorname{Row}(1,1,1^6)\) lies in
the ideal generated by the seven rows, so it can never equal \(1\).

Section 6's conditional therefore has a model, and is not vacuous.

## 9. What this does not prove

1. **It is not the nine-row landing at \(h=3\).**  It closes one repair route
   for one packet.  The open target of the handoff guide, section 4, is
   untouched.
2. **Monochromatic internal edges only**, and that is a real restriction.
   With the \(90\) cross-colour internal edges freed, the anchor rows do not
   peel — \(90\) monomials of each avoid \(q_c(2,3)\) — and the unconditional
   case is **open**.  Three things are known there, from
   [the cross-colour note](h3-cross-colour-repair-internal-edge-localization.md).
   The propagation used in section 3 forces only \(8\) of those edges, but
   that is a property of the rule, not of the system: full elimination of the
   degree-one equations forces \(20\), leaving the two relations
   \(q(2@2,4@c)+q(3@2,4@c)=0\).  The trade survives as two fifteen-word
   families, so a completion keeping the edge \(\{2,3\}\) live in both
   orientations still has \(\chi=0\).  And killing the twenty internal edges
   that carry a non-\(2\) colour at site \(2\) or \(3\) against a colour-\(2\)
   partner closes the whole system, so any cross-colour completion must have
   at least one of those twenty edges nonzero.  This is the same boundary as gap 1 of
   the leak note.
3. **The peel and the trade do not generalize.**  On two further packets with
   the same ledger, the same cap position and the class carrier free, the
   anchor does not peel and the trade never touches the class carrier.  What
   controls this is the geometry of the collapsed support, not the number of
   live four-sets: that count is neither necessary nor sufficient, and the
   endpoint stars are what decide how far the collapse reaches.  See
   [the transport note](h3-star-sector-transport-collapse-general-peel-degenerate.md),
   which also gives a hand criterion for when the peel does occur.  The
   collapse and the infeasibility, by contrast, do recur.
4. **The colour-0 and colour-1 anchors are not interchangeable**, which
   sections 4–6 treat symmetrically and section 8 corrects.
5. **\(\chi\) is invisible to the matching tensor anyway.**  A rescaling fixes
   every row coefficient while scaling \(\chi\) by \(\tau^6\), so no landing
   theorem can be a formula or a bound — only a vanishing statement.  This
   result is a vanishing statement, which is the admissible shape.
6. **\(\chi\) means the colour-2 cap throughout.**  A repaired packet also
   carries colour-0 and colour-1 caps, and those are not analysed here.  The
   witness of section 8 happens to have \(\chi=0\) on every admissible cap in
   all three colours, but that is a fact about it, not a general claim.

## 10. Audit

The dependency-free checker
[`verify_h3_star_sector_anchor_terminal_trade.py`](../computations/verify_h3_star_sector_anchor_terminal_trade.py)
verifies: all-ones hafnian normalization; that the symbolic system evaluated
at the guard point reproduces the committed two-entry ledger and that the
guard satisfies the seven rows; the cap-layer table, including linearity of
\(\chi\) in the direct scalar at three values and the failure of the source
relation at \((2,2)\); the frozen-slice geometry, including the unique live
four-set and the ten detecting pairs; each of the \(32\) forcings against its
named row and word, with an explicit assertion that no restored anchor row is
used, and closure against the whole seven-row subsystem; the four-hole form of the
rows on all \(729\) words and all nine label pairs, and
\(|\operatorname{supp}H_0(q_2)|=1\) on the frozen slice; the peel identity,
both against the four-site restriction of the row functional and against a
literal rebuild of the ten monomials displayed in section 4; the full nine-member trade family; the product
identity as an exact multiple of one row equation; the three infeasibility
searches — the two anchor-row ones through the two-branch case split, the
nine-row one directly; the leaf census of the
pure-word-only system, recorded as *not decided by that search*; and the
cross-colour scope guard, which checks both that the section-3 propagation
forces eight cross edges and that full elimination of the twenty-two
degree-one equations forces twenty and leaves the two displayed relations,
with the anchor still not peeling under either.

Standard library only, exact `Fraction` arithmetic, about nine seconds,
passing normal, `-O` and `-I -S`, and deterministic across hash seeds.
