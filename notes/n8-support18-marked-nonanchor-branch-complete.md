# N=8 support-18 marked nonanchor branch completion

## Result

The framed support-18 persistence theorem is branch-complete. There is no
restricted-support or ancestry-marking guard.

Start with any of the 502 nonprivate directed support-17 link types from
commit 4c8d9d5, retain its first added edge as a marked operation role, and
add any second graph edge. Give the target block support \(12\) or \(012\),
and independently give each added block support

\[
  01,\quad 02,\quad 12,\quad\text{or}\quad012.
\]

Then every source-labelled chart has at least one of:

1. a private contraction cap;
2. a complementary crossed-binary active cap;
3. a missing normalized pure target row; or
4. a mixed decorated matching word with one literal occurrence.

Equivalently, the simultaneous avoidance system is UNSAT in every branch.
No occurrence guard survives, so there is no coefficient/pure-anchor fibre
to solve and no exact weighted source guard.

## True marked quotient

The quotient fixes the directed target incidence. The two added edges are
operation marks:

- if their colour-support subsets differ, they remain ordered marks;
- if their colour-support subsets agree, their interchange is allowed.

Thus the quotient is taken by the actual stabilizer of the marked
source-labelled data, rather than by the unmarked graph automorphism group.
The exact counts are

    parent-labelled second-edge additions : 5,522
    ordered marked directed types          : 5,496
    equal-support unordered marked types   : 4,367

The target/support data have 15 GHZ-frame orbits. For target support \(012\),
the full \(S_3\) action leaves five ordered added-support patterns:

\[
\begin{aligned}
 &(012,012),\quad(012,12),\quad(12,012),\\
 &(12,12),\quad(12,02),
\end{aligned}
\]

where the two entries are the supports of the first and second added edges.
For target support \(12\), the stabilizer \(1\leftrightarrow2\) leaves ten
patterns. Five of the total 15 patterns have equal added supports and use the
4,367-type unordered quotient; the other ten use the 5,496-type ordered
quotient. Hence the exact census size is

\[
  5(4367)+10(5496)=76795.
\]

Every one of these 76,795 systems is UNSAT.

## Exact occurrence system

For a marked graph and one of the 15 support patterns, all remaining edges
are coordinate anchors with variables in \(\{0,1,2\}\). Every supported
perfect matching is expanded through every permitted colour of each marked
nonanchor block. For each eight-site decorated word \(w\), the checker forms
its exact occurrence count

\[
  m_w=\sum_o {\bf1}[\text{the coordinate anchors realize occurrence }o].
\]

A necessary guard must satisfy:

\[
  m_{0^8},m_{1^8},m_{2^8}\ge1,\qquad
  m_w\ne1\quad\text{for every mixed }w,
\]

complete framed anchor coverage at each site, and the negation of every
source-authorized crossed-binary landing whose five displayed roles remain
coordinate. If one of those roles is itself a nonanchor mark, the binary
landing is not asserted; this makes the avoidance system weaker and the
UNSAT conclusion stronger.

The target support \(12\) chart excludes direct-colour-zero binary landings,
as required by the exact rank-two construction. No invalid arbitrary
\(S_3\) gauge fixing is used in the marked systems.

## Relation to the coarse persistence potential

There is still no componentwise monotone on

\[
  (I_X,\ S_G,\ \operatorname{supp}L_e)
\]

alone: a new edge may leave \(I_X\), cover the last old singleton, and enlarge
a binary residue. The branch-complete result is instead a finite union
theorem: although the individual witnesses can disappear, they cannot all
disappear simultaneously on any support-18 marked chart.

This result is occurrence-level and independent of the local Phi or mapping
cylinder route. It can therefore be used as a terminal wherever a proof
reaches the 502 support-17 framed link types.

## Reproduction

Run:

    python3 computations/verify_n8_support18_marked_nonanchor_branch_complete.py
    python3 -O computations/verify_n8_support18_marked_nonanchor_branch_complete.py
    python3 -I -S computations/verify_n8_support18_marked_nonanchor_branch_complete.py

The checker reconstructs both true marked quotients, verifies the 15
colour-support orbits, runs the 76,795 exact systems in deterministic fork
shards, retains every SAT model for coefficient solving (the returned set is
empty), and pins ledger

    a6ae147b913999ae4cf4f12f70d57139b5ee7342fdf7f8f4049a313084e9cb73
