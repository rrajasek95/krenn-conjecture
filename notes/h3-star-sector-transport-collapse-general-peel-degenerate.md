# How far the star-sector collapse transports

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.

## 1. Outcome

The [star-sector trade](h3-star-sector-anchor-terminal-class-trade.md) proves,
on the audited seven-row guard's frozen colour-2 slice, that the diagonal
anchor peels onto one internal edge and that the same edge annihilates the
direct scalars carrying the terminal class.  This note asks how much of that
survives on other packets, and answers it with three further packets.

The answer splits cleanly:

* **the collapse and the outright infeasibility are general** — they recur on
  every packet tested, with a proved sufficient condition for the peel;
* **the peel and the class-killing trade are not** — they fail on packets B
  and C, which carry the audited ledger and a live class.

What controls them is the geometry of the collapsed support, the criterion of
section 4 — **not** the number of live four-sets.  That count is neither
necessary nor sufficient: on packet B's own slice \(q_2=01+23+45\), which has
three live four-sets, \(324\) of \(400\) sampled rank-three star pairs with
the audited ledger and a live class do peel, \(36\) of them with a
class-killing trade; while on the audited guard's own slice \(q_2=01+45\),
with one live four-set, \(6\) of \(120\) do not peel.

So scope item 3 of the trade note is not a formality.  The anchor/terminal
trade must not be pushed toward a general lemma without the section 4
collapse criterion as an explicit hypothesis.

## 2. The complementary guard has no terminal class to trade

The committed all-word \(8/9\) packet — section 3, equations (G1)–(G5) of
[`tagged-incidence-cokernel-hamming-one-boundary.md`](tagged-incidence-cokernel-hamming-one-boundary.md),
audited by `verify_tagged_incidence_cokernel_eight_row_guard.py` — is the
mirror of the seven-row guard: it supplies \(X_0,X_1\) and misses \(X_2\).
Its data is

\[
 q=(23)_0+(45)_0+(12)_1+(34)_1,\quad
 (p_0,p_1,p_2)=(z_0^0,z_5^1,z_2^2),\quad
 (s_0,s_1,s_2)=(z_1^0,z_0^1,z_4^0),
\]

with \(d=E_{02}\) and the single missing-target entry \((22,2^6,-1)\).

Freezing its colour-0/1 slice and freeing the whole colour-2 sector, the
mirror analysis runs and every part recurs:

* the eight supplied rows force \(36\) of \(60\) unknowns to zero, collapsing
  \(\operatorname{supp}q_2\) to the bare matching \(\{05,13,24\}\) and both
  stars to the sites \(\{2,4\}\);
* the anchor peels, now onto **two** edges:
  \(\operatorname{Row}(2,2,2^6)=q_2(0,5)\,q_2(1,3)\,\rho_2(2,2,\{2,4\})\);
* the trade equations \(d_{ij}q_2(0,5)=0\) hold for all nine label pairs, so a
  live anchor kills the entire direct block and the anchor **residual** becomes
  the constant \(-1\), that is, the anchor row is identically \(0\) against its
  target \(1\);
* the system is infeasible outright, over \(15\) branch nodes.

But the trade is **vacuous for the class** here.  Every \(p_i,s_j\) is a
single cell, so every response is one edge and \(R^{[2]}=R^{[3]}=0\); this
packet has \(\chi=0\) on all nine caps and all three pure colours, before the
anchor question is even asked.  So this packet cannot test the trade at all.

(The other committed \(8/9\) packet,
`one-unused-anchor-hessian-all-cycle-eight-row-guard.md`, has stars
\(p=(x_{0a},x_{3b},0)\), \(s=(x_{1a},x_{5b},0)\) and \(d=0\), so every response
is at most one edge, \(R^{[2]}=R^{[3]}=0\) and \(\chi\equiv0\) for the same
reason.  Checked during audit; it is not in this note's checker.)

## 3. Two seven-row guards that do carry a class

To test it properly one needs packets with the audited guard's ledger *and* a
live class, differing only in the frozen slice.  Two were built.

**Packet B.**  \(q_2=01+23+45\), a perfect matching, so
\(\operatorname{haf}(q_2)=1\) with three live four-sets.  Stars
\(p=\bigl((1,0,0,0,1,0),(0,0,1,0,0,0),(0,1,0,0,0,1)\bigr)\),
\(s=\bigl((0,-1,0,0,0,1),(-1,0,0,0,-1,0),(0,0,0,0,1,0)\bigr)\).  The pure word
pins the direct block, so \(\chi=2d_{21}=4\) is forced.  Its \((0,0)\) cap
also has \(Q_2=-2\), neutralized not by vanishing but by the source relation
\(\alpha Q_0+Q_1=0\) forcing \(d_{00}=0\).

**Packet C**, the controlled comparison.  \(q_2=01+23+04+25\), so
\(\operatorname{haf}(q_2)=0\) as in the audited guard, with **four** live
four-sets.  Stars
\(p=\bigl((-1,0,-1,-1,0,-1),(0,0,0,-1,0,-1),(0,1,0,0,0,0)\bigr)\),
\(s=\bigl((-1,0,0,0,0,0),(0,-1,0,0,1,0),(0,0,0,0,0,1)\bigr)\), direct point
\(d_{01}=1\).  Its class sits on the same cap \((0,1)\) as the audited
guard's, at \(\chi=-4d_{01}\) with \(d_{01}\) free.

Both satisfy all six off-diagonal rows and the complete \(22\) row on all
\(729\) words, both have the audited missing-target ledger
\((00,0^6,-1)\), \((11,1^6,-1)\), and both have rank-three stars.

| packet | \(q_2\) | live 4-sets | \(\chi\) | collapse | peel | trade |
|---|---|---|---|---|---|---|
| audited guard | \(01+45\) | 1 | \(-2d_{01}\) | 32 zeros | yes, one edge | kills \(d_{01},d_{02},d_{12},d_{20}\), shifts \(d_{10}\) |
| complementary \(8/9\) | frozen 0/1 slice | — | \(\equiv0\) | 36 zeros | yes, two edges | kills all \(d_{ij}\) |
| B | \(01+23+45\) | 3 | \(4\) forced | 44 zeros | **no** | **none** |
| C | \(01+23+04+25\) | 4 | \(-4d_{01}\) | 40 zeros | **no** | only \(d_{10},d_{20},d_{21}\) |

Packet C matches the audited guard on everything the trade argument appeared
to use — same ledger, same cap position, same vanishing
\(\operatorname{haf}(q_2)\), class carrier free.  Its anchor does not peel,
and although trade equations do appear, they annihilate
\(d_{10},d_{20},d_{21}\) and **never** the class carrier \(d_{01}\).  It is
**not** a controlled comparison in the number of live four-sets alone,
however: its endpoint stars differ from the guard's as well, and the stars are
what decide how far the collapse goes.  All four packets are nevertheless
infeasible outright.  The node counts here depend on the branch ordering and
are regression tripwires, not invariants.

## 4. When does the anchor peel?

There is a sufficient condition, and it is a theorem rather than a heuristic;
both peeling instances are also verified by monomial exhaustion.  Suppose that
after the collapse a set \(D\) of sites satisfies

1. no surviving colour-\(c\) internal edge leaves \(D\);
2. \(|D|\) is even;
3. the in-\(D\) star pair is killed for the label \((c,c)\); and
4. the colour-\(c\) edges inside \(D\) admit a **unique** perfect matching
   \(M\).

Then the anchor peels off \(M\):

\[
 \operatorname{Row}(c,c,c^6)
 =\Bigl(\prod_{e\in M}q_c(e)\Bigr)\,
  \rho_c\bigl(c,c,\,W\setminus V(M)\bigr).
\]

Conditions (1)–(3) already give
\(\operatorname{Row}(c,c,c^6)=\operatorname{haf}(q_c[D])\,
\rho_c(c,c,W\setminus D)\), in four lines: by (1) and (2) every matching
splits across \(D\) and its complement; pairs inside \(D\) die by (3); mixed
pairs die because \(D\setminus\{x\}\) is odd and isolated; and pairs inside
the complement contribute the displayed product.  Condition (4) only makes the
first factor a monomial.  Condition (3) is not necessary either: it weakens to
(3′), *for every pair inside \(D\), either the \((c,c)\) star pair is dead or
\(\operatorname{haf}(q_c[W\setminus\{x,y\}])=0\)*, and there are packets that
peel with live in-\(D\) star pairs, killed instead through their complementary
hafnian.

The audited guard is the case \(D=\{2,3\}\), \(|M|=1\), complement four sites;
the complementary \(8/9\) guard is \(D=\{0,1,3,5\}\), \(|M|=2\), complement two
sites.  Packets B and C isolate no proper even set at all: for every proper even
\(D\) some surviving colour-\(c\) edge leaves \(D\), and \(D=W\) fails both
(3), with fifteen and nine live star pairs, and (4), with two induced
matchings.  Correspondingly they show no peel.

This is a sufficient condition, not a characterization.  It says the peel is a
property of what the collapse happens to isolate, and it is the hypothesis
under which a peel may be assumed.

## 5. What was not determined

* Everything here is the **monochromatic** internal-edge ansatz.  The
  cross-colour version was not run on any of these packets; the trade note
  records that branch as unterminated.
* Whether B and C also admit a literal adjacent \(27\)-row decomposition.
  Ledger, star ranks and literal Segre rectangles were verified; the adjacent
  decomposition was not.
* Whether a peel-and-trade with a nonzero class exists on any
  non-degenerate slice.  The search found none but was not exhaustive.
* Freezing only one of the complementary guard's two anchor colours.

## 6. Audit

The dependency-free checker
[`verify_h3_complementary_guard_star_sector_transport.py`](../computations/verify_h3_complementary_guard_star_sector_transport.py)
verifies all-ones normalization; the committed \(8/9\) ledger reproduced
symbolically; \(\chi\equiv0\) on all nine caps and three colours there, with
the two supplied anchor caps at layers \((0,1,0,0)\); each of the \(36\)
forcings against a named supplied row and word, plus closure; the two-edge
peel identity; the nine trade equations; the reduction of the anchor row to
\(-1\); the \(15\)-node branch search; and for packets B and C the ledger,
four-set support, star ranks, cap tables, collapse counts, the **absence** of
any peel, the exact set of traded scalars, and their branch searches.
Standard library only, exact arithmetic, about three seconds, passing normal,
`-O` and `-I -S`, byte-identical across hash seeds.

Packets B and C were independently reconstructed against the committed guard
checker's own model: both satisfy the seven rows on all \(729\) words, both
reproduce the audited two-entry ledger, both have rank-three stars, and their
nonzero caps are exactly \((2,1)\) at \(\chi=4\) for B and \((0,1)\) at
\(\chi=-4\) for C, with three and four live four-sets respectively.
