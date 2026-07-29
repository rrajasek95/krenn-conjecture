# Independent audit of the ten-site pair-slice exchange

## 1. Frozen claim and verdict

This clean-room audit checks the frozen primary artifacts

* [`ten-site-overlapping-pair-exchange-redundancy.md`](ten-site-overlapping-pair-exchange-redundancy.md),
  SHA-256
  `f482941b671deead2a9e410d2f2e46fd1dc7fbd31e3da7d74a89eeb187b2527b`;
* [`verify_ten_site_overlapping_pair_exchange_redundancy.py`](../computations/verify_ten_site_overlapping_pair_exchange_redundancy.py),
  SHA-256
  `1828193d419455704025b693a6eb9d0dc406d9fcc0abff1949d50c1f518d61c5`.

The verdict is **PASS**, with the scope qualification in Section 6 below.
For arbitrary aggregated endpoint-ordered edge cells, a complete nine-row
tensor system for one deleted pair and a complete nine-row tensor system for
another pair have exactly the same \(3^{10}=59{,}049\) scalar residual
polynomials, merely regrouped by row and boundary coordinates.  This is true
for an overlapping pair and, by the same argument, for a disjoint pair.

The independent checker is
[`audit_ten_site_overlapping_pair_exchange_redundancy_independent.py`](../computations/audit_ten_site_overlapping_pair_exchange_redundancy_independent.py),
SHA-256
`f1f7c59c19f469dff603def19a6ab7a2d5f4b49afa3b9546bcc1bdbee98f030a`.
It imports no code from the primary checker.

## 2. Independent matching reconstruction

Label the sites \(r,t,z,1,\ldots,7\), where \(z\) is the site called \(0\)
in the primary note.  I generated all perfect matchings by a bit-mask
recursion unrelated to the primary checker's tuple recursion.  It gives

\[
                              9!!=945
\]

matchings, each once.

For a generic ordered deleted pair \((u,v)\), I then generated the pair slice
directly from its two cases:

* the matching contains \(uv\), leaving one of \(7!!=105\) matchings on the
  eight boundary sites;
* \(u\) and \(v\) have ordered distinct boundary neighbors, giving
  \(8\cdot7\cdot5!!=840\) terms.

For both \((r,t)\) and \((r,z)\), the resulting \(105+840\) terms are disjoint,
have multiplicity one, and equal the independently generated set of all
\(945\) matchings.  Thus each pair row expansion is a partition of the same
top hafnian; it is not an additional family of top-degree monomials.

## 3. Endpoint-order redecomposition

The audit represents a literal colored cell as

\[
                  (u,\alpha;v,\beta),\qquad u<v,
\]

with each color attached to its named endpoint.  A generic chart encoder
classifies the cell as cap, left star, right star, or internal, and a
separately written decoder reconstructs the literal cell.  Both
\((r,t)\)- and \((r,z)\)-encodings decode exactly on all

\[
                         \binom{10}{2}3^2=405
\]

cells.  Every chart-role key occurs once.  The old/new transition census is

\[
\begin{array}{c|c|r}
\text{old role}&\text{new role}&\text{cells}\\ \hline
\text{cap}&\text{left star}&9\\
\text{left star}&\text{cap}&9\\
\text{left star}&\text{left star}&63\\
\text{right star}&\text{right star}&9\\
\text{right star}&\text{internal}&63\\
\text{internal}&\text{right star}&63\\
\text{internal}&\text{internal}&189.
\end{array}
\]

The numerical site order in the independent checker deliberately puts \(t\)
before \(z\).  Hence the old \(tz\) cell is stored in the reverse order from
the new chart's named right endpoint \(z\); successful decode tests the
endpoint reversal that is easy to mishandle in the formula for
\(\widetilde s_\alpha\).

The role totals in either chart are

\[
             9\ \text{cap},\quad72\ \text{left star},\quad
             72\ \text{right star},\quad252\ \text{internal}.
\]

They sum to \(405\), so no cell is omitted or duplicated by the
redecomposition.

## 4. Universal exchange and all residual coordinates

Give every site an algebraically distinct formal endpoint tag.  For every
matching in each chart expansion, encode every edge through that chart and
decode it back to its literal endpoint-ordered cell.  The two resulting
formal matching polynomials agree as counters: they contain the same
\(945\) distinct monomials, all with coefficient one.  Because the reversible
cell audit was performed for all \(405\) ternary cells, this formal matching
comparison specializes to every ternary coloring.  It reconstructs

\[
 \iota_{z,\alpha}\iota_{t,j}\iota_{r,i}H
 =
 \iota_{t,j}\iota_{z,\alpha}\iota_{r,i}H
\]

without using the primary checker.

I also enumerated every tuple

\[
                       (i,j,\alpha,\omega)
        \in\{0,1,2\}^3\times\{0,1,2\}^7.
\]

In the first chart it is row \((i,j)\) and boundary word
\((\alpha,\omega)\).  In the second it is row \((i,\alpha)\) and boundary
word \((j,\omega)\).  Both reconstruct the identical ten-site color word.
The two maps are bijections on all \(59{,}049\) coordinates.

The target indicator was checked independently in both charts.  It is
nonzero precisely for the three monochromatic words, so the target
contractions agree coordinate by coordinate.  Combining this target audit
with the universal source-polynomial comparison proves exact equality of
all \(59{,}049\) residual polynomials, not merely equality after a numerical
specialization.  Consequently the two complete scalar generator lists, and
hence their ideals, are equal.

## 5. Polarized/raw normalization

For a direct-cap term, the independent checker decorates each internal
four-edge boundary matching by a distinguished internal edge and then
forgets the decoration.  There are exactly four decorations.  This is the
literal matching verification of

\[
                         q q^{[3]}=4q^{[4]}.
\]

Every raw direct term therefore has polarized multiplicity \(4\).  Every
two-star term has raw multiplicity \(1\), while the polarized expression has
the explicit coefficient \(4\).  For each of both deleted pairs, the entire
\(945\)-term polarized counter is exactly four times the raw counter.  Thus
the factors are

\[
              4\delta_{i\alpha}X_i\quad\text{and}\quad
                \delta_{i\alpha}X_i
\]

in the polarized and raw equations, respectively.  No pair-dependent or
orientation-dependent factor appears.

## 6. Exact scope: redundant equations, useful chart

The primary conclusion is sound when “the full nine equations” means nine
**tensor** equations, including every boundary coefficient.  Those nine
rows already contain every coefficient of \(H-\mathrm{GHZ}_{10}\).  A second
complete pair slice therefore adds no scalar ideal generators, and a
dimension count must not count it as independent information.

This does **not** make the overlapping chart mathematically useless.  It is
a different factorization and grouping of the same residual polynomials.
That presentation can expose source-variable eliminations, convenient
leading terms, localizations, saturations, or lower cap identities which are
hard to see in the first chart.  Such consequences remain consequences of
the original full ideal; the chart helps derive them rather than supplying
new hypotheses.

Likewise, a second chart can genuinely strengthen a computation which kept
only selected rows, projections, aggregated coefficients, or other weakened
data from the first chart.  One must compare the actually retained scalar
ideals in that setting.  The exchange theorem alone neither constructs a
clean internal cap nor closes the all-even descent.

## 7. Reproduction

Running

```text
uv run python computations/audit_ten_site_overlapping_pair_exchange_redundancy_independent.py
```

returns `PASS` and reports

* \(945\) perfect matchings and both \(105+840\) partitions;
* \(405\) reversible endpoint-ordered cells and the seven transition counts;
* \(945\) universal exchange monomials;
* polarized/raw factors \((4,1)\) for both pairs;
* \(59{,}049\) residual coordinates, with exactly three nonzero GHZ targets.
