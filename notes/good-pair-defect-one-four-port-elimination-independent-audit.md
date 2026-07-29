# Independent audit of the four-port defect-one elimination

## Verdict

The proof in
[the four-port elimination](good-pair-defect-one-four-port-elimination.md)
is confirmed. It uniformly excludes the residual defect-one chart and
does not use a bounded support census, a capped response table, positivity,
or a summandwise inference from a cancelling coefficient.

## Independent reconstruction

Fix one off-diagonal product with nonzero defect coefficient and let \(U\)
be the union of its two row supports. The defect-one theorem gives
\(|U|\le4\), puts every same-shore or interface block inside \(U\), and
forces \(U\) to meet the nonbipartite remainder.

First, every two-site complement has a nonzero matching power. Otherwise
the nine-dimensional space of variations on the deleted block is Hessian
killed. A gauge vector supported there has block value proportional to
the one fixed block \(q_D\), so the gauge intersection has dimension at
most one. This contradicts gauge rigidity without any condition on
\(q_D\).

For a complement matching, cancel the number of cross-shore edges. If
\(r_A,r_B\) count the two shores' vertices used by same-shore or interface
edges, then

\[
 |A\setminus D|-|B\setminus D|=r_A-r_B,
 \qquad r_A\le|U\cap A|,
 \qquad r_B\le|U\cap B|.
\]

Deleting two vertices from each shore shows that two non-singleton shores
would require at least four shore ports. The live interface requires a
fifth port in the remainder, contradicting \(|U|\le4\).

For a singleton shore \(\{x\}\), deleting \(x\) and each opposite-shore
vertex forces the whole opposite shore into \(U\), leaving only sizes one,
two, or three. The invisible rank-three star equations force \(x\notin U\):
if \(x\) occupied one support, avoiding a single nonzero product on every
star edge would put \(x\) and at least two leaves into one two-site support.
With two leaves, \(x\) has only two possible nonzero-block partners and
violates Lemma R. With three leaves, the supports partition the leaves and
one remainder port; two leaves share one support and have zero mutual block,
and a suitable pair deletion strands them on the one remainder port. The
one-leaf case is exactly the previously proved \(K_2\) sign-collision
kernel.

## Guard audit

1. **Arbitrary invisible blocks.** Cross-shore and remainder-internal
   blocks are unrestricted. They consume equal shore counts or no shore
   vertices and therefore disappear from the balance identity.
2. **Complex cancellation.** The proof uses nonzero divided power only to
   infer existence of some supported matching. It never identifies a
   matching inside a zero coefficient.
3. **Zero blocks.** The block-kernel argument becomes stronger when the
   tested block is zero; its gauge intersection then has dimension zero.
4. **The capped-table countermodel.** No cap or abstract response tensor
   appears. The four-port window is obtained upstream from the physical
   equality \(p_cs_d=\beta_{cd}Z^\zeta\).
5. **Quantifiers.** No bound is placed on \(|W|\), the nonbipartite
   remainder, aggregate multiplicity, or the ranks of invisible blocks.

The companion checker independently enumerates the finite port-count and
singleton-support implications. Those checks audit the local case split;
the uniform statement is supplied by the hand proof.

