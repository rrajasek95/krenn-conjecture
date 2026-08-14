# N=8 support-18 framed multi-edge persistence

## Verdict

There is no componentwise well-founded potential on the three certificates
from the support-17 theorem alone. A later edge can make each certificate
disappear:

1. its response increment can leave the old contraction ideal \(I_X\);
2. its decorated matching link can cover the last singleton word; and
3. it can add a third residue monomial to a crossed binary face.

Nevertheless their union persists through the next coordinate-anchor layer.
The exact finite theorem is:

> **Support-18 framed persistence theorem.** Fix \(N=8\), the normalized
> three-line GHZ frame, and one of the 502 nonprivate directed support-17 link
> types from commit 4c8d9d5. Add any second live graph edge. If the target
> block has either two-coordinate or full three-coordinate support and every
> other edge is a framed coordinate anchor, then the support-18 chart has at
> least one of: a private cap, a complementary crossed-binary active cap, a
> missing normalized pure row, or a mixed decorated matching word with
> exactly one occurrence.

There is no occurrence-level guard, hence no exact weighted source can evade
these exits. The 5,522 parent-labelled additions collapse to 1,823 directed
support-18 graph types. Both target charts are UNSAT for every type:

    support-two   : 1,823 UNSAT / 0 guards
    support-three : 1,823 UNSAT / 0 guards

The two-coordinate audit retains both inequivalent first-anchor classes.
Since the missing colour is fixed as zero, only \(1\leftrightarrow2\) remains;
the first anchor is therefore allowed to be zero or nonzero. This avoids the
invalid full-\(S_3\) symmetry reduction.

## Exact finite-domain formulation

For a directed support \(E\), introduce a variable

\[
  x_f\in\{0,1,2\}
\]

for every coordinate anchor \(f\ne X\). For each supported perfect matching
and each permitted target colour, expand its literal eight-site decorated
word. If \({\cal O}_w\) is the set of occurrences of \(w\), its multiplicity
is the exact finite-domain expression

\[
  m_w(x)=\sum_{o\in{\cal O}_w}
  \mathbf 1[\text{all anchor colours in }o\text{ agree with }x].
\]

The necessary-guard system imposes simultaneously:

\[
  m_{0^8},m_{1^8},m_{2^8}\ge1,
  \qquad m_w\ne1\quad(w\text{ mixed});
\]

complete framed anchor coverage at every site; and the negation of every
authorized complementary crossed-binary landing. These are finite integer
constraints, not a generic-coefficient approximation. Z3 returns UNSAT in
both charts for all 1,823 directed types.

The theorem is stronger than solving coefficient cancellations: a weighted
source would first need a support chart with all pure words and no singleton,
and none exists.

## Multi-block probe and exact scope

The checker also tests one parent-labelled ancestry for every unmarked
directed type with all three distinguished blocks—the target and both added
edges—given full noncoordinate support. All 1,823 marked probes are again
UNSAT. This shows that simply enlarging all three supports does not repair the
coordinate theorem.

This probe is not promoted to a complete multi-nonanchor theorem: restricted
two-colour supports on one or both added edges, and all inequivalent markings
inside a single unmarked graph orbit, have not been exhausted. Such support
restriction is not monotone for singleton multiplicity: it can change
\(3\mapsto2\) as well as \(2\mapsto1\). The sharp remaining multi-edge task is
therefore the finite set of restricted-support, marked-ancestry charts—not a
search for a potential on the coarse certificate tuple.

## Why this is reusable

The occurrence constraints depend only on the GHZ colour frame, the directed
cap incidence, and the supported perfect matchings. They do not use the local
Phi/mapping-cylinder construction. Thus the theorem can be cited as an
independent support-18 terminal for any route that reaches one of the 502
support-17 directed link types with a coordinate second edge.

No arbitrary-\(\mathrm{GL}_3\) claim is made. The result is equivariant under
source-labelled frame permutations and nonzero line rescalings.

## Reproduction

Run:

    python3 computations/verify_n8_support18_multi_edge_persistence_theorem.py
    python3 -O computations/verify_n8_support18_multi_edge_persistence_theorem.py
    python3 -I -S computations/verify_n8_support18_multi_edge_persistence_theorem.py

The checker pins the support-17 and binary-landing dependencies, reconstructs
the directed quotient, emits every exact finite-domain system to the local
Z3 executable, validates every returned model independently (none survives),
and pins the ledger

    ca0c641fb16ef47aa1cb6a3220556b1e34a95de5f5e413324217f969f2a9eabb
