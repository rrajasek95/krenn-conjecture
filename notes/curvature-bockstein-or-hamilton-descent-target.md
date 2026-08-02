# Curvature Bockstein or Hamilton descent

Research target only.  This note does not prove Krenn's conjecture and does
not change the certified dependency graph.

## 1. The reversal suggested by the exact cells

The primitive alternating-\(C_4\) colon classes in chart 26 need not be
eliminated in order to prove the conjecture.  There are two logically useful
outcomes of a source-labelled path-forest straightening step:

1. the collision class is null-homotopic after physical label identification,
   so the straightening continues to a component-joining forest term; or
2. the class survives diagonal specialization, in which case its connecting
   homomorphism can be paired with the three pure anchors.

The second outcome is potentially an obstruction rather than a failure of the
method.  Chart 25 is the finite exact model: its four-row functional annihilates
every incident mixed-source column but has target pairing \(3\).  After its
common factor is removed, the support consists of three decorations of one
alternating \(C_4\) and the parallel-pair degeneration, with coefficient vector

\[
                             (-2,-1,-1,+1).                 \tag{1}
\]

The first three rows are the genuine matching-exchange circuit.  The last row
is precisely the diagonal collision missing from the ordinary three-row
determinant.  Thus (1) should be read as a local source-relative Bockstein
cochain, not merely as an awkward non-squarefree leading term.

## 2. Candidate local complex

Let \(\widetilde R\) be the ring in which every occurrence of a decorated edge
has its own source-slot label, and let \(L\) be the sequence of differences
which identify labelled copies of the same physical coordinate.  Let
\(\widetilde C_{\mathrm{pf}}\) denote the proposed polarized path-forest
complex.  Its fixed-matching pieces have the already proved Koszul simplices;
alternating-cycle determinants give the base-exchange faces before primitive
division.

The physical total complex is

\[
 {\cal D}=\operatorname {Tot}
       \bigl(\widetilde C_{\mathrm{pf}}\otimes K(L)\bigr).  \tag{2}
\]

For a collision face \(\xi\), the first nonzero label-diagonal differential
defines a connecting class

\[
               \beta_L[\xi]\in H({\cal D}).               \tag{3}
\]

The ordinary Bianchi identities only say that the two-dimensional faces of
(2) close.  They do not force (3) to vanish.  The elementary ideal
\((xy,xz)\) shows that all pairwise diagonal tests can pass while higher Tor
survives.  Consequently the desired construction must use the full Koszul
cube of label identifications, or an equivalent filtered contraction with
proved zero indeterminacy.

## 3. Curvature--Bockstein dichotomy

The useful theorem is weaker than global derived transversality and stronger
than a squarefree degeneration.

> **Target theorem.**  On the synchronized full-nine two-chart packet, every
> primitive critical forest face admits one of the following source-faithful
> resolutions.
>
> 1. **Forest continuation.**  Its class in (2) is a boundary, with a chosen
>    contraction whose leading term is a legal endpoint join and whose lift
>    indeterminacy is zero in the augmented target complex.
> 2. **Curvature obstruction.**  Its first nonzero connecting class has a
>    canonical local representative supported on three alternating-cycle
>    decorations and one parallel-pair degeneration.  Pairing this
>    representative with the pure augmentation equals
>    \(\kappa\) times the appropriate nonzero adjacent-power residue, where
>    \(\kappa\) is the selected physical curvature minor.
> 3. **Geometric split.**  A repeated physical coordinate gives the exact
>    closed/open decomposition \(x=0\) or \(x\ne0\); on both branches a
>    lexicographic defect statistic strictly decreases.

At an exact ternary source the mixed augmentation kills every source boundary.
The synchronized selection gives \(\kappa\ne0\), and activity plus the three
pure anchors must make the residue in alternative 2 nonzero.  Thus alternative
2 is a contradiction.  Alternative 3 terminates by the branch statistic.
Only alternative 1 can persist.

Repeated forest continuation decreases the number of even path components.
It therefore terminates at an alternating Hamilton path.  The two unmatched
endpoints of its join matching are the candidate clean pair.  The terminal
part of the theorem must identify its augmented coefficient with the physical
clean-cap readout and prove activity and zero lift indeterminacy.  The existing
exact clean-pair theorem then descends from \(N\) to \(N-2\).

The [exact terminal chart-26 audit](n8-chart26-terminal-hamilton-readout.md)
shows that none of these three words can be omitted.  The normalized physical
target has 5,596 degree-seven Hamilton rows with unique pure-matching
provenance, 5,388 of which have a support-unit direct endpoint edge.  However,
the 300 path terms in the first mixed-source degree-six cell have 10,173 legal
normalized terminal extensions and none belongs to the physical target.
Moreover, one physical target Hamilton row has an explicit active cap with
zero error on its coordinate face, but adding a single off-path spoke leaves
the terminal monomial and activity unchanged while making four cap-error
coefficients equal to two.  Thus the terminal map must be an augmented
source-chain map with a specified lift; equality of uncoloured Hamilton
skeletons does not define it.

### Exact local model for alternative 3

The two no-simple-path representatives in the weighted chart-26 degree-six
census now satisfy alternative 3 exactly; see
[the exact branch-elimination note](n8-chart26-degree6-branch-elimination.md).
Both select \(x=x_{02}^{00}\).  On \(x=0\), the 8,412-class representative
reduces to zero by the restricted \(H_1,H_{730}\) rows, and the 45,776-class
representative reduces to zero by the restricted \(R_{730,1459}\) row.  On
\(x\ne0\), division by \(x^2\) changes their repeated pivots into the
squarefree Laurent pivots 034bc6f4 and 044ec6f4.

The resulting local defect is

\[
 (\#\text{ undecided decorated coordinates},
   \text{ repeated excess after removing invertible coordinates}). \tag{4a}
\]

Both children decide \(x\), and the open child additionally drops the pivot
excess from one to zero.  This is well-founded if a decided coordinate is
never selected again.  The exact audit proves this descent only for the two
frozen representatives, not uniformly over every member of the two coarse
classes; that propagation remains part of the target theorem.

## 4. Concrete construction by homological perturbation

There is a standard mechanism which can produce the required secondary map
without choosing reductions anew in every cell.  First construct an explicit
contraction

\[
  (\widetilde C_{\mathrm{pf}},d_0)
  \mathrel{\mathop{\rightleftarrows}^{p}_{i}} H,
  \qquad d_0h+hd_0=1-ip,                                  \tag{4}
\]

where \(d_0\) is the direct sum of the fixed-base Boolean/Koszul forest
differentials.  Put every base exchange and label-identification operation in
a filtration-raising perturbation \(\delta\).  The induced differential on
\(H\) is the finite homological-perturbation series

\[
 d_H=p\delta i-p\delta h\delta i
       +p\delta h\delta h\delta i-\cdots .                \tag{5}
\]

The series is finite on each forest because a legal branch has at most
\(h-1\) joins.  Its first term is the ordinary alternating-cycle exchange.
The first possible confluent correction is the second term
\(-p\delta h\delta i\): two distinct labelled exchanges can be identified at
one physical coordinate, producing the parallel-pair degeneration which a
single determinant cannot contain.  Formula (1) is therefore an exact test
for this transferred second differential.

A source-labelled contraction (4) would solve two problems at once.  The
perturbation lemma makes \(d_H^2=0\) automatically, supplying all higher
coherences, and the specified homotopy \(h\) removes the lift ambiguity which
currently prevents the adjacent-power/Bockstein comparison.  The genuinely
new statement is not the abstract perturbation lemma; it is the equivariant
contraction (4), compatible simultaneously with matching-base flips, the
three pure anchors, and physical label identification.  If a denominator
needed by (4) vanishes, that failure should be routed to the geometric split
in alternative 3 rather than silently localized away.

## 5. Why this may be shorter than a complete Groebner theorem

A global squarefree Groebner degeneration would require simultaneous
orientation and reduction of every source-labelled critical pair.  It would
also prove much more radicality than the conjecture needs.  The dichotomy
above only needs:

* one local confluent \(C_4\) connecting formula, including its parallel-pair
  term;
* a proof that its target pairing is the curvature-weighted adjacent-power
  residue with no choice-of-lift ambiguity;
* a decreasing measure for the collision splits; and
* the terminal Hamilton-path target readout.

The degree-six census has already compressed 2,925,805 critical pairs to the
two mechanisms which these clauses address: base-exchange curvature and
collision-only branching.  A proof of the four clauses would avoid completing
the entire normalized ideal.

## 6. Exact tests for the proposed theorem

Any candidate construction must reproduce all of the following without
changing source labels.

1. Before primitive division, the alternating-\(C_4\) three-row determinant
   and its tetrahedral row syzygies.
2. After primitive division, the two nonzero chart-26 degree-six colon
   classes rather than falsely reducing them.
3. On the chart-25 circuit, the exact cochain (1), annihilation of all 56
   actual incident columns, and pure-target pairing \(3\).
4. On the off-diagonal clean boundary, the required grade transport from the
   admitted adjacent-power source relation to the reciprocal clean
   coefficient, retaining the physical target.
5. Independence of every chosen primitive lift modulo the complete anchored
   relative kernel.
6. On the terminal chart-26 row `04237475b8cfea`, the clean coordinate-face
   cap and the one-spoke nonclean lift, together with a chain-level reason the
   latter ambiguity is zero at an exact ternary source.  It must also explain
   how a mixed terminal forest reaches a physical target row despite the zero
   intersection for all 10,173 first-cell terminal extensions.

The third and fourth tests are the same proposed secondary operation in two
different coordinates.  Establishing that identification would connect the
new path-forest computation directly to Components III--IV of the unified
two-chart overlap--jet saturation target.
