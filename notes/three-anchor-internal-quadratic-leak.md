# The diagonal anchors cannot be carried by the internal quadratic

Research evidence only.  Krenn's conjecture remains open; no certified
dependency is changed and `SP-CLEAN-BRIDGE` is untouched.  This is a
negative structural result — a guard — in the sense of
[`terminal-bianchi-handoff-guide.md`](terminal-bianchi-handoff-guide.md).

## 1. Why the question arises

The [blindness guard](fourhole-cap-polarization-terminal-blindness.md)
showed that the terminal class \(\chi\) is invisible to the response
contraction and left one concrete next step: find out whether the diagonal
anchor sector can supply the \(J_2\) component that the response rows
cannot.

There is an obvious and tempting route.  In the audited seven-row guard of
[`h3-diagonal-segre-second-transgression-seven-row-guard.md`](h3-diagonal-segre-second-transgression-seven-row-guard.md)
exactly two rows fail, \((0,0)\) at \(0^6\) and \((1,1)\) at \(1^6\), each
by \(-1\); and \(\chi=-2\) is determined entirely by the **colour-2** data.
So if the two missing anchors could be repaired using only colour-0 and
colour-1 material, the repaired packet would satisfy all nine rows while
keeping \(\chi=-2\), refuting the nine-row landing at \(h=3\).

This note closes that route.  The repair is impossible in the natural
non-negative regime, for a reason that has nothing to do with the guard's
particular numbers.

## 2. Setting

Six residual sites, three colours.  Let \(q\) be a colour-decorated
internal quadratic whose edges are **monochromatic** with **non-negative**
weights, and let \(E_c\) be the **positive-weight support** in colour \(c\)
(not merely the nominal colour class: a colour-\(c\) edge of weight zero
contributes nothing).  For a
colour word \(w\),

\[
 \operatorname{haf}_w(q)=\sum_{M}\ \prod_{(x,y)\in M}q(x,y,w_x,w_y),
\]

the sum over the fifteen perfect matchings.  A matching edge is usable only
when both endpoints carry the same colour, so \(\operatorname{haf}_w\)
factors over the colour classes of \(w\), and only words whose three colour
classes all have **even** size can contribute.  There are exactly \(180\)
such words other than the three pure ones.

## 3. The leak

**L1 (exhaustive).**  For every triple \((M_0,M_1,M_2)\) of perfect
matchings of \(K_6\) there is a non-pure even-class word \(w\) whose class
\(S_c\) is perfectly matched inside \(M_c\) for each \(c\).  Checked over
all \(15^3=3375\) triples: **zero** are leak-free.

**L2 (monotonicity).**  "\(S\) is perfectly matched inside \(E\)" is
monotone in \(E\).  Hence L1 lifts from matchings to arbitrary edge sets:
if each \(E_c\) contains a perfect matching \(M_c\), the word supplied by
L1 for \((M_0,M_1,M_2)\) still works for \((E_0,E_1,E_2)\).  No search over
edge sets is needed.

**L3 (consequence).**  Suppose the response/star sector vanishes
identically.  Satisfying the diagonal anchor at colour \(c\) then reads
\(d_{cc}\operatorname{haf}_{c^6}(q)=1\), forcing \(d_{cc}\ne0\) and
\(\operatorname{haf}_{c^6}(q)\ne0\); with non-negative weights the latter
forces a perfect matching inside \(E_c\).  By L1 and L2 there is then a
non-pure word \(w\) with \(\operatorname{haf}_w(q)\ne0\) — no cancellation
is available, every term being non-negative — so the diagonal row
\((c,c)\) takes the nonzero value \(d_{cc}\operatorname{haf}_w(q)\) at
\(w\), where its target is zero.  The three anchors are therefore
**unsatisfiable through the internal quadratic alone**.

\[
 \boxed{\begin{gathered}
 \text{For monochromatic, non-negative }q\text{ with a vanishing star
 sector:}\\
 \text{three diagonal anchors}\ \Longrightarrow\ \text{contradiction;}\\
 \text{so the star/response sector must participate.}
 \end{gathered}}
\]

**L0 (star-independent).**  One necessary condition survives without any
hypothesis on the stars.  The anchor row at the pure word \(c^6\) is

\[
 d_{cc}\operatorname{haf}_{c^6}(q)
 +\sum_{x<y}R_{xy}\operatorname{haf}_{c^6}\bigl(q\ \text{on the four sites
 off }\{x,y\}\bigr),
\]

so every term is a colour-\(c\) hafnian on six or on four sites, needing
three or two disjoint colour-\(c\) edges respectively.  Hence

\[
 \boxed{E_c\ \text{without two disjoint edges}
 \ \Longrightarrow\ \text{anchor }c\text{ is unreachable,}}
\]

whatever the star sector contains.  This is exactly the guard's anatomy:
colours 0 and 1 have no internal edges at all, so their anchors fail, while
colour 2 has \(\{01,45\}\) — two disjoint edges but no six-site matching —
so its anchor is necessarily carried by the **response** term, and is.

## 4. What this rules out, and what it does not

Three statements of different strength are in play, and it is worth
keeping them apart.

* **L3** closes the **star-free** regime only.  Its hypothesis is that the
  response sector vanishes identically, so it does *not* by itself apply to
  the section 1 repair, which keeps the guard's nonzero stars.  At a leak
  word that repair's row value is
  \(d_{cc}\operatorname{haf}_w(q)+R_{cc}\!\cdot\!\operatorname{haf}(\text{complement})\),
  and L3 excludes no cancellation between those two terms.
* **The section 5 instance** is what actually closes the section 1 repair:
  computed in the audited physical model, no cancellation occurs there, and
  the repair breaks 66 equations.
* **L0** needs no hypothesis on the stars at all, and is the durable part:
  the anchors constrain \(q\) itself.

Together these narrow the route of section 1 rather than closing it in
general.  A repair may still add colour-0 and colour-1 entries to the
**star** vectors, and neither L0 nor L3 excludes that.  What they do
establish is that such a repair is forced — by L0 the internal quadratic
must in any case acquire two disjoint edges in each anchor colour, and by
L3 it cannot carry the anchors by itself.  That matters because the star vectors are shared across
colours — the same \(p_i,s_j\) whose colour-2 entries build the response
\(R_{ij}=p_is_j\) that determines \(\chi\) — so an anchor repair cannot be
performed in a sector disjoint from the one carrying the terminal class.
This is a coupling statement, and it is weaker than an impossibility
statement: it does not show that a star-sector repair must disturb
\(\chi\), only that it cannot be made in ignorance of it.  That is the
precise, and limited, sense in which "the diagonal sector must enter before
the pairing".

It does **not** prove the nine-row landing, and it is not a proof that no
nine-row packet with \(\chi\ne0\) exists.  Two explicit gaps:

1. **Cross-colour quadratics are not covered, and signed ones only
   partly.**  L3 uses non-negativity to conclude
   \(\operatorname{haf}_w(q)\ne0\) from the existence of one matching.  With
   edges joining sites of *different* colours the whole class-factorization
   fails and the argument gives nothing.

   For **signed** monochromatic weights the situation is better than a flat
   exclusion.  On a \((2,2,2)\) word each colour class is a single pair, so
   its hafnian is one edge weight and a product of three nonzero weights
   cannot cancel.  Hence L3 holds *verbatim* for signed \(q\) whenever the
   three supports admit a \((2,2,2)\) leak word, which happens for
   \(1845\) of the \(3375\) matching triples (\(54.7\%\)), rising to about
   \(86.6\%\) for supports of the form matching-plus-one-edge.  The
   remaining signed cases are genuinely open: cancellation there is not
   excluded, though a 20 000-trial random search for a signed \(q\) with
   three live anchors and all 180 non-pure words vanishing found none.
2. **A vanishing star sector is a hypothesis, not a reduction.**  Real
   packets have responses; L3 says only that they must be used, not what
   using them costs.  In particular a nine-row packet with \(\chi\ne0\) is
   *not* excluded — it is only excluded from being built by adding
   internal-quadratic material alone.

## 5. Instance check

The route of section 1 was also tried literally against the audited guard
before being ruled out.  Adding, for each of colours 0 and 1, the perfect
matching \(\{01,23,45\}\) to \(q\) together with a unit diagonal direct
scalar repairs both failing anchors and leaves \(\chi=-2\) untouched, but
breaks **66** of the nine-row equations, distributed as
\((0,1)\!:\!18\), \((0,0)\!:\!17\), \((1,1)\!:\!17\), \((2,2)\!:\!8\),
\((1,0)\!:\!6\).

The 66 break into three mechanisms, and only the first is the L1 leak:

* \(48\) at the \(16\) non-pure words where
  \(\operatorname{haf}_w(q)\ne0\), in the three rows with \(d_{ij}\ne0\) —
  namely \((0,0)\), \((1,1)\), \((0,1)\) — with **no** response
  cancellation at any of them.  A representative word is \(001122\), where
  all three colours contribute one matched pair.
* \(14\) response-only breaks in rows \((1,0)\) and \((2,2)\), where
  \(d_{ij}=0\); these are not L1 leaks.
* \(4\) breaks at the **pure** words \(0^6\) and \(1^6\), in rows
  \((0,1)\) and \((1,1)\), and \((0,0)\) and \((0,1)\) respectively, caused
  by the new direct scalars meeting the now-nonzero pure hafnians.

So it is not the case that every broken word is non-pure; \(62\) of the
\(66\) are.  The baseline ledger reproduced in the same run is the audited
one: two failures, \((0,0)\) at \(0^6\) and \((1,1)\) at \(1^6\), each
\(-1\), with source jet \(J_0=0\) and \(\chi=-2\).

## 6. Audit

The dependency-free checker
[`verify_three_anchor_internal_quadratic_leak.py`](../computations/verify_three_anchor_internal_quadratic_leak.py)
proves L1 by exhaustion over all \(3375\) triples and verifies the
monotonicity of L2 on every even subset against every perfect matching and
a deterministic spread of supersets.  L0 is checked over **all \(2^{15}\)
edge sets**: no set lacking two disjoint edges admits a four- or six-site
matching.  A weighted section then does what the combinatorial ones do not
— it computes actual hafnians, verifying the class factorization
\(\operatorname{haf}_w(q)=\prod_c\operatorname{haf}_{S_c}(E_c)\) on which
the whole argument rests, and running L3 end to end on explicit integer
quadratics.  The signed \((2,2,2)\) count \(1845/3375\) is verified
exhaustively.  Standard library only, exact integer arithmetic, under half
a second, passing normal, `-O` and `-I -S`.

Two scope notes on the checker itself.  Its `audit_L3_consequence` is
deliberately a re-run of L1 on the same family plus the guard-consistency
check; the substance of L3 is carried by the weighted section, not by that
function.  And the checker is dependency-free by design, so it models the
row equations only through their hafnian terms.  It also verifies that the
seven-row guard sits outside L3's hypothesis — its colour-2 quadratic is
the two disjoint edges \(01,45\) and carries no perfect matching — so the
lemma and the guard are consistent rather than in tension.

The section 5 numbers were produced against the audited guard checker
`verify_h3_diagonal_segre_second_transgression_seven_row_guard.py` by
modifying its `BLOCKS` table and re-evaluating all \(9\times729\) row
equations; that instance run is not part of the standalone checker, which
is deliberately dependency-free.

An independent audit of the first version returned PASS with two
substantive corrections, both applied.  It found that the claim "every
broken word is non-pure" was false for four of the sixty-six (section 5 now
gives the full three-mechanism decomposition), and that section 4 asserted
more than L3's hypothesis supports (sections 3--4 now separate L0, L3 and
the instance computation, and L0 was added as the star-independent
statement).  The audit also reclaimed the signed \((2,2,2)\) case, which the
first version dismissed, and observed that the original checker computed no
hafnian at all — hence the weighted section.  Its independent
reconstructions of the \(180\), \(3375\), \(0\), \(66\) and per-row figures
all agreed, and it found L1 tight: some triples leak at exactly one word.
