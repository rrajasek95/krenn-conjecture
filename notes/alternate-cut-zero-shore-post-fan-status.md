# Post-fan status of the induced-zero four-cut / growing-shore identity

Status audit for Priority 3 of
[the current audit](current-proof-audit-and-next-steps.md), Section 6:

> In the alternate cut route, exploit the induced-zero four-cut/growing-shore
> identity from the regular fan, using its full common matching power and
> coupled mixed coefficients.

The identity is equation (2) of
[the induced-zero four-cut reduction](good-pair-fan-induced-zero-four-cut-reduction.md).
The new input is
[the fan six-port simultaneous exclusion](good-pair-fan-six-port-simultaneous-exclusion.md)
(with its
[independent audit](good-pair-fan-six-port-simultaneous-exclusion-independent-audit.md)),
whose Theorem A proves that no good pair is regular nonbipartite, and whose
Corollary D already states that the shore alternative is unreachable along
the regular fan route.

## 1. Verdict

**Priority 3 is (d): transformed into a new concrete target.**  As
literally worded it is dead — "(c)" — because the phrase "from the regular
fan" names a provably empty branch: the four-cut theorem produces its shore
only under \(|F|\ge7k\ge7\) regular nonbipartite fan pairs, and
\(F=\varnothing\) for every even \(N\ge8\) (Corollaries B and D of the
exclusion note).  But the identity itself is not touched, because it never
depended on the chart.  The exact split is:

* **Dead** — the shore *construction* (sparse rows, bounded aggregate
  degree, greedy independent set).  Its one chart input is the sparse-row
  bound, which is derivable only on the regular nonbipartite chart, and
  every chart class on which that mechanism fires is a chart class on which
  Theorem A's collapse also fires, so it contains no good pairs
  (Section 5: there is no corrected-hypothesis rescue).
* **Alive but idle** — the shore *identity*: for an induced-zero set \(S\),
  \(|S|=h\ge2\), in any hypothetical exact source, the \(3^h\)
  common-power system (2) holds verbatim, with no Hessian, gauge, or graph
  hypothesis.  Verified exactly at \(N=8\) for \(h=2,3,4\) on a
  deliberately mixed internal chart (Section 6).  It is a conditional tool
  with no theorem currently supplying its hypothesis: nothing now forces
  even one literal zero aggregate block in a hypothetical source.

**The transformed target (exact statement).**  Prove a zero-block forcing
theorem on the three escape charts: for a hypothetical exact ternary
source, upgrade the forced structure of a good pair — the localized
missing row \(p_{c,i}=0\) on the gauge-rigid connected-spanning-bipartite
chart, the extra kernel direction, or the disconnected/nonspanning
component structure — to a literal zero aggregate block \(A_{xy}=0\), or
directly to an induced-zero set \(S\) with \(|S|\ge2\), uniformly in
\(N\).  Any such theorem re-arms the chart-free shore expansion (2) at
full strength (all \(3^h\) rows, one common matching power
\(q^{[m-h]}\), coupled mixed coefficients, arbitrary complex
cancellation), with injectivity of the \(h\) row triples still supplied
free by goodness and mode flattening.  Until such a theorem exists, the
alternate-cut route has no forced source factorization of four-cut type,
and Priority 3's slot is inherited by the escape-chart programme already
named in Section 8 of the exclusion note.

## 2. The two layers of the four-cut theorem

The four-cut note proves a dichotomy: either at least \(N-7k-6\) fan pairs
escape, or a \((k{+}1)\)-vertex induced-zero shore exists and satisfies
(2).  Its proof has two logically independent layers.

**Layer C (construction, Sections 2–3 there).**  For each regular
nonbipartite fan pair \(\{r,x\}\), the sparse-row consequence

\[
 |S_c(r)\setminus\{x\}|\le2 \qquad(c=0,1,2)             \tag{C1}
\]

is imported from Theorem 5.1 of
[the source-Hessian dichotomy](source-derivative-hessian-dichotomy.md).
Four-deletion then gives \(|S_c(r)|\le2\), the same bound at the other
endpoints gives aggregate degree at most six on
\(Z=F\setminus C\), and greedy seven-colouring extracts the shore.  This
layer consumes the chart hypotheses **gauge-rigid + \(G_3\) connected,
spanning, nonbipartite** — nothing else in the whole note does.

**Layer I (identity, Section 4 there).**  Given any set \(S\) of \(h\)
named vertices with every internal aggregate block literally zero,
decomposing the source quadratic as
\(a=q+\sum_j\sum_ce_c^{(x_j)}p_c^{(j)}\) has no named-to-named term, so
every perfect matching sends the named vertices to distinct complement
sites, and slot extraction gives

\[
 \Bigl(\prod_{j=0}^{h-1}p_{c_j}^{(j)}\Bigr)q^{[m-h]}
    =\delta_{c_0=\cdots=c_{h-1}}X_{c_0}^D.               \tag{2}
\]

This is a pure matching partition.  It uses no Hessian, no gauge
rigidity, no rank-three graph, and no regularity of any kind.  The
injectivity of the \(h\) row triples and the coordinate anchors in
alternative 2 also come from chart-free inputs (mode flattening and the
two-hole coordinate-anchor lemma) plus the zero blocks themselves.  Only
the two-site support statement of alternative 2 is Layer-C material.

## 3. Question 1: does the derivation need the nonbipartite chart?

**Layer I does not; Layer C does, irreparably.**

The exclusion theorem's hypothesis is exactly "regular nonbipartite":
source Hessian with only the vertex-gauge kernel, and \(G_3(q)\)
connected on all of \(W\) and nonbipartite.  Regular **bipartite** charts
are indeed not excluded — they are the third escape chart, and they are
nonvacuous (the \(K_{2,2}\) certificate of
[the bipartite rank-drop note](source-hessian-bipartite-rankdrop.md), and
the new exact \(|W|=6\) certificate below).  So the question whether the
fan construction could be re-run on regular bipartite pairs is
substantive.  The answer is no, at proof level:

1. **Where nonbipartiteness enters.**  The proof of (C1) turns the mixed
   kernel membership \(p_cs_d+\frac{a_{cd}}tq\in\ker\mathcal H_q\) into
   the blockwise equation
   \((p_cs_d)_{ij}=(\alpha_i+\alpha_j-\frac{a_{cd}}t)q_{ij}\) via gauge
   rigidity, kills the scalar on rank-three edges, and then needs the
   affine system \(\{\alpha_i+\alpha_j=\gamma\hbox{ on }E,\ \sum\alpha=0\}\)
   to have only the zero solution.  That is exactly where the odd cycle
   is consumed.  On bipartite graphs the system has the one-parameter
   antipodal solution \(\alpha=\beta\sigma\) (exact dimensions in
   Section 6, CHECK 3), so \(p_cs_d=0\) is not forced and no support
   bound follows.

2. **On regular bipartite charts the sparse-row inference is false, not
   merely unproven.**  CHECK 2 constructs, at the \(N=8\) pair-chart size
   \(|W|=6\), an exact integer chart with rank-three blocks exactly on
   \(K_{3,3}\) (connected, spanning, bipartite, balanced), rank-one
   blocks \(z_iz_j^{\mathsf T}\) inside the shores, and an exactly
   gauge-rigid Hessian (two-sided certificate, Section 6).  On it the
   **full-support** rows \(p=z=\sum_iz_i\) and
   \(s=z^\sigma=\sum_i\sigma_iz_i\) satisfy the mixed pair-contraction
   kernel equation

   \[
    a\,q^{[3]}+(ps)\,q^{[2]}=0,\qquad a=0,
   \]

   because \(ps\) equals the bipartition gauge element \(Z^\sigma\)
   blockwise.  By bilinearity, \(p_c=t_cz\), \(s_d=u_dz^\sigma\)
   satisfies all six mixed cells at once with every row supported on all
   six sites.  So the conclusion "support at most two" cannot be a
   consequence of the mixed equations on the regular bipartite chart.

3. **What a good pair does force there.**  The witness rows are
   colour-proportional, hence not injective — consistently with
   [the bipartite rank-drop theorem](source-hessian-bipartite-rankdrop.md):
   if all six rows were sitewise nonzero everywhere, the antipodal
   synchronization would make the nine responses rank at most two against
   the rank-three target.  For a good pair on a regular bipartite chart
   the surviving forced consequence is therefore exactly **one localized
   missing row** — some local vector \(p_{c,i}=0\) or \(s_{d,i}=0\), a
   single \(1\times3\) row of a single block — never a two-site support
   bound and never a zero block.  That is Proposition 3.1(1) of
   [the bridge frontier](injective-star-hessian-bridge-frontier.md)
   combined with Corollary 5.2(3) of the rank-drop note.

4. **A small surviving fragment (observation, with proof).**  On a
   regular bipartite chart whose \(G_3\)-bipartition is *balanced*
   (\(|P|=|Q|\), as for any \(K_{3,3}\) chart at \(N=8\)), the
   \(a_{cd}=0\) half of the degree-two collapse still holds for
   \(c\ne d\): gauge rigidity gives zero-sum \(\alpha\) with
   \(\alpha_i+\alpha_j=a_{cd}/t\) on every edge; connected bipartite
   \(G_3\) gives \(\alpha_i=a_{cd}/(2t)+\beta\sigma_i\); summing over
   \(|W|=2t\) sites gives \(0=a_{cd}+\beta(|P|-|Q|)=a_{cd}\).  The
   \(\beta\)-parameter survives, so \(p_cs_d=0\) does not follow.  On
   unbalanced charts (e.g. \(K_{2,4}\)) even \(a_{cd}\) escapes, with
   \(\beta=-a_{cd}/(|P|-|Q|)\).  CHECK 3 verifies both regimes exactly
   (\(\gamma=0\) forced on \(K_{3,3}\) and \(C_6\); \(\gamma\) free on
   \(K_{2,4}\)).  This fragment bounds direct blocks, not star supports;
   it does not feed the shore construction.

## 4. Question 2: re-derivation on the three escape charts

The only chart input of the four-cut theorem is (C1).  Per chart:

| Escape chart | First failing step | What survives |
|---|---|---|
| **Extra kernel** | Gauge rigidity itself: kernel membership has no \(Z^\alpha\) representation, so even the blockwise equation is unavailable. | Only the chart-free pair identity and Layer I.  Guard: [the common-origin countermodel](common-origin-factorization-rank-countermodel.md) satisfies all nine cells \(p_is_jq^{[2]}=\delta_{ij}z_0\cdots z_5\) at \(|W|=6\) with support-six rows; its \(q^{[3]}=0\) makes \(q\) an extra non-gauge kernel vector.  No support bound is derivable. |
| **Disconnected or nonspanning \(G_3\)** | The affine graph step: nonzero solutions exist whenever some component is bipartite, isolated vertices included (CHECK 3: nonspanning dimension 2). | Blockwise zero products on each rank-three edge (if gauge-rigid).  Guard: the fourteen-site family of [the bridge frontier](injective-star-hessian-bridge-frontier.md) has all 91 pairs both-injective with every pair chart failing connected-spanning.  Caveat: if the graph is spanning with *every* component nonbipartite, the mechanism does fire (CHECK 3: two disjoint triangles give dimension 0, the audit's sufficiency remark) — but then Theorem A's collapse fires equally, so that sub-stratum contains no good pair and belongs to the empty class. |
| **Connected spanning bipartite** | The odd cycle: the antipodal solution \(\alpha=\beta\sigma\) survives; sparse rows are refuted by the exact full-support witness of CHECK 2 on a gauge-rigid \(K_{3,3}\) chart. | Blockwise zero products on cross edges; \(a_{cd}=0\) \((c\ne d)\) on balanced charts (Section 3.4); for good pairs, exactly one localized missing row.  Guard: [the all-pair missing-row countermodel](all-pair-missing-row-countermodel.md) occupies this response branch coherently. |

On every chart, Layer I survives unchanged (CHECK 1 plants a zero block
and a rank-one block inside \(D\) precisely to exhibit this
insensitivity), and Layer C fails at the stated step.  The re-derivation
of the *construction* is possible on none of the three charts; the
re-derivation of the *identity* is possible on all of them but is empty
of force, because no theorem supplies a shore.

## 5. No corrected hypothesis exists (the mechanism identity)

The first stage of the sparse-row proof — gauge rigidity plus the odd
cycle forcing \(a_{cd}=0\) and \(p_cs_d=0\) for \(c\ne d\) — is
**the same first stage** as Lemma 4.1 of
[the exclusion note](good-pair-fan-six-port-simultaneous-exclusion.md).
Theorem A's remaining steps (annihilator trichotomy, one-site collapse,
diagonal contradiction) consume only those degree-two identities, one
independent star triple, and the diagonal cells.  Consequently, on
*every* chart class where the sparse-row input (C1) can be established by
this mechanism — the maximal such class being gauge-rigid, spanning, with
every \(G_3\)-component nonbipartite, by the audit's sufficiency remark —
Theorem A's collapse also runs, and the class contains no good pairs at
all.  So

\[
 \{\hbox{good pairs}\}\cap
 \{\hbox{charts where (C1) is derivable by the known mechanism}\}
 =\varnothing
\]

identically, not accidentally.  A corrected-hypothesis rescue of
Priority 3 — option (b), re-running the fan construction on an enlarged
chart class — is therefore impossible: enlarging the class where the
mechanism fires enlarges the exclusion by exactly the same amount.  A
genuine rescue would need a support-bounding mechanism that does not pass
through the degree-two identities; no such mechanism exists in the
workspace, and the three guards of Section 4 show the pair equations
alone do not force sparsity on any escape chart.

For the same reason, alternative 1 of the four-cut dichotomy now holds
threshold-free and maximally (all \(\ge N-7\) fan pairs escape for every
even \(N\ge8\)) — but that is verbatim Corollary B of the exclusion note,
so the four-cut theorem adds nothing on that side either.  Its entire
residual value is Layer I.

## 6. Exact audit

The standalone checker
[zero_shore_post_fan_status_check.py](../computations/zero_shore_post_fan_status_check.py)
verifies, exactly:

* **CHECK 1 (Layer I is chart-free), \(N=8\), \(h=2,3,4\).**  Random
  asymmetric integer aggregate blocks on eight sites; scattered shore
  labels \(\{1,4\}\), \(\{1,4,6\}\), \(\{1,4,6,3\}\) so both storage
  orientations of named blocks occur; all shore-internal blocks zero; one
  zero block and one rank-one block planted inside \(D\).  All \(3^h\)
  slot extractions of the full 105-matching power equal
  \(\bigl(\prod_jp^{(j)}_{c_j}\bigr)q^{[m-h]}\), computed independently
  in the \(D\)-site square-zero algebra.  The contributing matching
  supports are \(90,60,24\), matching \((N-h)_h(N-2h-1)!!\) —
  equation (12) of the four-cut note.  No Hessian, gauge, or graph data
  appears anywhere in this check.
* **CHECK 2 (the bipartite witness), \(|W|=6\).**  Seed 1 already gives
  the chart: cross blocks of nonzero determinant, shore blocks
  \(z_iz_j^{\mathsf T}\), so \(G_3=K_{3,3}\) exactly.  Gauge rigidity by
  the established two-sided certificate: the five vertex gauges are
  exactly annihilated over \(\mathbb Z\) and exactly independent
  (rank 5), and the \(135\times729\) Hessian has rank \(130\) modulo
  \(1{,}000{,}003\), used only as an exact lower bound for the rational
  rank; hence the rational kernel is exactly the vertex-gauge space.
  Also \(q^{[3]}\ne0\).  The witness \(p=z\), \(s=z^\sigma\) has both
  supports equal to six, satisfies \(ps=Z^\sigma\) blockwise, and all 729
  top coefficients of \((ps)q^{[2]}\) vanish exactly over \(\mathbb Z\).
* **CHECK 3 (the graph step), exact rational dimensions** of
  \(\{\alpha_i+\alpha_j=\gamma\hbox{ on }E,\ \sum\alpha=0\}\) on seven
  six-vertex graphs: \(K_6\to0\); \(C_5\)+pendant \(\to0\); two disjoint
  triangles \(\to0\); \(K_{3,3}\to1\) with \(\gamma=0\) forced;
  \(K_{2,4}\to1\) with \(\gamma\) free; \(C_6\to1\) with \(\gamma=0\)
  forced; triangle+edge+isolated \(\to2\).

Run from the repository root:

    uv run python computations/zero_shore_post_fan_status_check.py

All 26 checks print PASS.  The frozen artifact has SHA-256

    d96ad4c3e6ce0f14359ab357d456e55ca79783327d1851d8db926e0f6831f498  computations/zero_shore_post_fan_status_check.py

Evidence discipline: every identity is checked over \(\mathbb Z\) or
\(\mathbb Q\); the single modular rank is an exact lower bound combined
with exact integer gauge certificates, the same two-sided pattern as the
audited exclusion note; no anchor, value, or finite field carries a
closure step.

## 7. Scope

This is a status note.  It modifies no existing note, computation, or
registry entry, and it closes nothing: it records that Priority 3's
stated route is dead, that the shore expansion (2) survives as an exact
chart-free conditional tool awaiting a zero-block forcing theorem, and
that the balanced-bipartite \(a_{cd}=0\) fragment (Section 3.4, an
observation with inline proof, not a registered theorem) is the only new
degree-two information currently visible on the surviving regular chart.
The uniform descent must come from the extra-kernel,
disconnected-or-nonspanning, and bipartite-with-missing-row charts, as
the exclusion note already directs.
