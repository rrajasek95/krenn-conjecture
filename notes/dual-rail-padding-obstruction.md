# Why Bell-pair dual-rail padding does not directly give a counterexample

The Bell-pair observation in `notes/planar-kasteleyn-route.md`, Section 7,
puts the whole Krenn model very close to an elementary tensor-network
construction.  A doubled Bell path has a local quotient to `GHZ_3`: encode
the three states by `00,01,10`, and at an internal block retain only equal
left and right codewords.  This note isolates exactly why padding those
three words to one-hot incidence words does not give a perfect-matching
counterexample.

## 1. Product Bell pairs and one-hot blocks

Take a disjoint union of weighted Bell edges.  Group their endpoints into
blocks indexed by a set `V`.  A bit `0` means that the endpoint is retained.
The signature of a Bell edge of weight `w` is

\[
                           w|00\rangle+|11\rangle.          \tag{1}
\]

Restrict every block to words with exactly one retained endpoint.  A
nonzero global word then retains both or neither endpoint of every Bell
edge and exactly one endpoint in every block.  Consequently its retained
Bell edges form a perfect matching of the blocks.  This is precisely the
perfect-matching incidence construction, not an approximation to it.

Suppose a one-hot padding assigns one distinguished incidence
`p_v(r)` at block `v` to each colour `r=0,1,2`, for example by replacing

\[
                 00,01,10\quad\text{with}\quad100,010,001. \tag{2}
\]

All other one-hot words are killed.  Each distinguished incidence is an
endpoint of one fixed Bell edge.

## 2. Unique-rail padding is impossible uniformly

**Theorem 2.1 (unique-rail padding obstruction).**  Let `|V|` be even and
at least six.  No product of Bell pairs followed by the unique one-hot
decoder above has image `Delta_(V,3)`.  Edge weights may be arbitrary
nonzero complex numbers, and auxiliary blocks do not help if they obey the
same unique-rail rule.

**Proof.**  The constant colour-`r` coefficient can be nonzero only if the
incidences `p_v(r)`, over all `v`, are paired among themselves by the Bell
edges.  They therefore form a perfect matching `P_r`.  The three
one-factors are edge-disjoint as decorated Bell occurrences, even when two
of them join the same pair of blocks by parallel rails.

The three-one-factors lemma gives a fourth perfect matching `M` in

\[
                             P_0\cup P_1\cup P_2.           \tag{3}
\]

*Attribution.*  The three-one-factors lemma is **Bogdanov's observation**
(Bogdanov 2017); the occurrence-multigraph form used here is Thm 1.7 of
Chandran-Gajjala-Illickan, arXiv:2407.00303 (the simple-graph form is
Thm 1 of Chandran-Gajjala, arXiv:2202.05562).  See
[`references/REFERENCES.md`](../references/REFERENCES.md).  No priority is
claimed for it here.

It is mixed.  Colour `v` by the rail used by `M` there.  At the port
`(v,r)` there is exactly one selected Bell edge, the edge of `P_r`.
Therefore `M` is the unique compatible perfect matching in (3).  Its
weight is a product of nonzero selected weights, so its mixed output
coefficient is nonzero and cannot cancel.  This contradicts the target.
`QED`

This is the selected-factor cancellation-cycle theorem in
`proofs/selected-one-factor-cancellation-cycle.md`, specialized to an
injective local code.  Adding dummy **vertices** merely enlarges `V`: all
of them are output parties in Krenn's problem, so the same three selected
one-factors and the same fourth-matching argument apply.

## 3. Signed parallel rails have no extra power

A natural attempted repair replaces one Bell rail by several signed copies.
If all copies of the colour-`r` rail at `v` go to the same partner
`p_r(v)`, this does not change the argument.

**Lemma 3.1 (parallel aggregation).**  Replace every selected edge
`uv in P_r` by any finite family of parallel Bell occurrences, all decoded
as colour `r` at both endpoints.  Let their total aggregate weight be

\[
                              a_{uv}^{(r)}=\sum_k w_{uv,k}.  \tag{4}
\]

The complete output tensor is unchanged if the family is replaced by one
rail of weight `a_uv^(r)`.  If the constant colour-`r` coefficient is
nonzero, every aggregate weight on `P_r` is nonzero.  Hence the fourth
matching in (3) still gives one nonzero mixed monomial.

**Proof.**  Once an underlying perfect matching chooses the pair `uv`, the
choice of its parallel occurrence is independent of all other pairs.
Summing those choices replaces `w_uv,k` by (4), and doing this on every
pair gives the asserted product of sums.  The all-`r` coefficient has only
the underlying matching `P_r`, so it is

\[
                              \prod_{uv\in P_r}a_{uv}^{(r)}.
\]

Its nonvanishing forces every factor to be nonzero. `QED`

Thus copies of opposite sign either leave one nonzero aggregate rail or
delete that cell everywhere.  They cannot cancel only the unwanted hybrid
while preserving a desired constant matching which uses the same cell.
Dummy incidences mapped to zero can simply be removed; dummy incidences
mapped to a colour and paired to the same selected partner are covered by
Lemma 3.1.

## 4. The exact boundary: a different-neighbour cycle

To cancel the forced matching `M`, a genuine repair must supply a distinct
matching `M'` with exactly the same named-vertex colouring.  After
aggregation, `M triangle M'` has no doubled two-cycle: a parallel occurrence
with the same endpoints and endpoint colours is the same aggregate cell.
Therefore the symmetric difference contains an alternating cycle of length
at least four.  Every `M'` edge on that cycle is outside the three selected
one-factors.  In particular:

* at least two new rails are required;
* they go to different selected partners (or use genuinely new endpoint
  colour cells); and
* at some vertex-colour port there are now two possible incident rails.

This is exactly the conclusion of the selected-factor cancellation-cycle
theorem.  It marks a sharp boundary: once different-neighbour rails are
allowed, the construction is no longer padding of the Bell code (2); it is
the full Krenn cancellation problem.

If `M triangle M'` is one cycle, choosing the new weight product to be the
negative of the old one cancels that one fibre.  It does **not** certify the
whole tensor.  The new rails combine with `P_0,P_1,P_2` to create further
perfect matchings, and each of their mixed fibres needs its own mate.

## 5. Why independent signed cycle repairs can be inconsistent

There is an exact torus test when every mixed fibre has two terms.  Give
the nonzero aggregate cells variables `z_e`.  For a binomial fibre `f`, let

\[
                         d_f=\mathbf1_{M_f}-\mathbf1_{N_f}\in\mathbb Z^E
                                                                    \tag{5}
\]

be the exponent difference of its two matching monomials.  Cancellation is

\[
                                  z^{d_f}=-1.               \tag{6}
\]

The system (6) has a solution in `(C^*)^E` exactly if every integer
relation

\[
                              \sum_f m_fd_f=0               \tag{7}
\]

has even coefficient sum `sum_f m_f`.  Necessity follows by multiplying
(6) to the powers `m_f`.  Sufficiency is the standard character-lattice
criterion for the image of a complex algebraic torus (equivalently, use
Smith normal form and divisibility of `C^*`).

So assigning an opposite sign to each duplicate cycle locally is sound
only when the global circulation lattice passes this parity test.  The
eight-vertex no-singleton labeling in
`computations/verify_monomial_n8_counterexample.py` fails it with the exact
relation

\[
                              -d_1+d_6+d_{10}=0,             \tag{8}
\]

whose coefficient sum is odd.  All 38 mixed fibres have mates, yet no
nonzero complex weighting cancels them simultaneously.

## 6. Consequence for the proposed construction

The padding audit gives a clean trichotomy.

1. One rail per colour is impossible by Theorem 2.1.
2. Any number of signed copies to the same partner reduces to case 1 by
   Lemma 3.1.
3. A surviving construction must introduce different-neighbour rails on
   alternating cycles and then solve all induced fibre equations, including
   the lattice-parity constraints (7).

The doubled Bell path succeeds because an internal block simultaneously
retains code information from its left and right bonds.  Exactly-one
incidence forbids that operation.  Neither local dummy padding nor parallel
signed duplication restores it; only the nonlocal cancellation cycles of
the original conjecture can do so.
