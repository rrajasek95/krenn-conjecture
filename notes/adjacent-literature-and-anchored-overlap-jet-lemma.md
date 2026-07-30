# Adjacent literature and an anchored overlap--jet lemma

## Bottom line

The most coherent candidate framework behind the live attacks is a
**two-chart determinantal-complex analogy on \(\mathbf P^1\)**.  On each
canonical cap line the scalar coordinates of the clean error form a linear
system in \(H^0(\mathbf P^1,{\cal O}(h))\); its common-root question is a
binary resultant/Macaulay question.  After the canonical selector quotient,
the proved order-two vanishing is a principal-parts (first-jet) condition.
The literal identities between overlapping pair caps resemble a
Koszul/Čech differential with a visible curvature coefficient \(AU-BF\),
and the three diagonal rows act as fixed-label boundary anchors.

No cited theorem supplies the missing proof automatically.  The repository
has not constructed an Eagon--Northcott or Buchsbaum--Rim complex whose
grade hypotheses are verified on the source-provenant matching module;
powers of matching quadratics have large annihilators.  The analogy is
useful because it isolates a theorem-shaped target more specific than an
arbitrary vector-polynomial common-root assertion, not because classical
determinantal exactness applies.

Subsequent to the first version of this note, the independently audited
[automatic two-chart extraction theorem](two-chart-joint-hypothesis-extraction.md)
proved that one selected minor already supplies both physical-label
full-nine systems, all four good endpoint maps, the complete all-label
power-free overlap/shared-\((L,M)\) packet, first-chart activity, and
ordinary selectors on every rootless chart.  The conditional ledger below
retains those data for clarity, but they are no longer separate extraction
assumptions.  The live additions are second-chart activity, stronger
fixed-label/own-edge selector compatibility, and branch-specific inactive
routing.

## Dictionary with established results

| Repository structure | Standard mathematical structure | What it explains, and what it does not yet give |
|---|---|---|
| The degree-\(h\) coordinate span \(L_{\cal E}\subset\mathbb C[u,v]_h\), its multiplication map into the \(2h\)-dimensional space \(S_{2h-1}\), and \(Q_f=S_{2h-1}/fS_{h-1}\) | In the rootless branch, a base-point-free linear system on \(\mathbf P^1\), its binary resultant, and restriction to the length-\(h\) divisor \(V(f)\) | The repository proves that gcd one is equivalent to surjectivity of the multiplication map.  It also identifies \(Q_f\) as the \(h\)-dimensional divisor-evaluation module after the nonvanishing block \(fS_{h-1}\) is removed.  Neither assertion constructs the source-derived rank defect. |
| Divisibility by \(\sigma^2\) after quotienting the three selector sites by their combined endpoint-star spans | Order-two vanishing, equivalently a condition on the two-dimensional first-principal-parts quotient at the scalar-zero point | It proves that every full Macaulay minor uses at least two exposed columns.  It does **not** force a determinant defect: \(f(K_*)\ne0\) makes \(\sigma\) a unit on \(Q_f\), exactly as the sharp guard shows. |
| \(P_{pq}t-P_{pr}y=(At-By)z\), its normal-row companion, and the four-site curvature equation | A source-level overlap identity analogous to a Koszul/Čech differential; generalized Koszul and determinantal complexes are models, not identified complexes here | This is the strongest shared structure.  A positive argument would need a new filtered-exactness or injectivity statement after localizing at activity and would use \(AU-BF\ne0\) as a transverse coefficient.  Classical generic acyclicity cannot be quoted on the square-zero matching module. |
| The six formal products \(x_{ij}=p_i s_j\), \(i\ne j\), and \(x_{01}x_{12}x_{20}=x_{02}x_{21}x_{10}\) | The edge subalgebra and toric ideal of the chordless bipartite cycle \(C_6\) | The repository directly proves that the primitive source-label relation is the cubic hexagon and that there is no quadratic product rectangle.  Graph-toric theory supplies context.  The exact guard shows that these off-diagonal data do not by themselves force the desired linear Macaulay defect; a fixed-label diagonal row must enter any such coefficient-cut proof. |
| The full-nine cohafnian identity and the scalar-zero tangent packet | The apolar algebra of the generic hafnian; separately, Lefschetz multiplication in the target GHZ Artinian Gorenstein algebra | Shafiei's quadratic apolar generators organize the generic hafnian identities, but the repository proves that top apolar membership collapses to the original scalar tangent equation and loses support and lift data.  The separate strong-Lefschetz calculation for the target is a no-obstruction result, not a bridge to the source. |
| Short grouped Wick decompositions | Kruskal uniqueness and linear circuits of product tensors/Segre varieties | The repository's rank-gap theorem uses Kruskal only in its visible range and otherwise produces short grouped circuits.  Lovitz--Petrov gives relevant abstract splitting constraints, but no theorem yet makes those circuits stable under matching deletion/exchange.  This remains a backup, not an input to the proposed overlap lemma. |

## Proposed decisive lemma

### Conditional diagonal-anchored two-chart overlap--jet saturation lemma

Let \(|B|=2m\ge8\), put \(h=m-1\), and suppose one entry-minimal physical
source satisfying \(H_B(A)=\Delta_{B,3}\) is equipped with four distinct
sites \(p,q,r,s\) and fixed colours \(a,b,c,d\).  Put

\[
\begin{gathered}
 A=A_{pq}(a,b),\quad B=A_{pr}(a,c),\quad C=A_{qr}(b,c),\\
 E=A_{ps}(a,d),\quad F=A_{qs}(b,d),\quad U=A_{rs}(c,d),
 \qquad AU-BF\ne0.
\end{gathered}
\]

Use the two actual pair charts \(\nu\in\{pq,pr\}\), with canonical lines

\[
 K_{pq}(u,v)=uE_{ab}+vI,
 \qquad K_{pr}(u,v)=uE_{ac}+vI.
\]

Let \({\cal E}_\nu\in V_\nu\otimes S_h\), \(S=\mathbb C[u,v]\), be the
clean-error tensor and let \(L_\nu\subset S_h\) be its scalar coordinate
span.  Write

\[
 I_\nu=(L_\nu)\subset S,
 \qquad
 a_\nu=s_\nu\kappa_{\nu,0}\kappa_{\nu,1}\kappa_{\nu,2}.
\]

The conditional statement uses the following common data.  The status of
each item is recorded explicitly.

1. **Automatic.** Both charts are literal restrictions of the same source
   and carry all nine normalized rows
   \[
          B^\nu_{ij}q_\nu^{[h-1]}=\delta_{ij}X_i
          \quad(0\le i,j\le2),
   \]
   including the three fixed-label diagonal anchors.
2. **Partly automatic.** The four deleted endpoint-star maps for the two good
   pairs are injective and the first activity polynomial is nonzero.  The
   second condition \(a_{pr}\not\equiv0\), equivalently
   \((B,\operatorname{tr}A_{pr})\ne(0,0)\), remains an assumption whenever
   the proof localizes both charts at activity.
3. **Automatic.** Before multiplication by any common divided power, the full
   fixed-label matrix-cap connection, its normal-row companion, and every
   required four-site coefficient cut are retained.  In the displayed
   colours these include
   \[
   P_{pq}t-P_{pr}y=(At-By)z
   \]
   and
   \[
   UP_{pq}+tL_{pq;s}-FP_{pr}-yL_{pr;s}
       =(At-By)v+(AU-BF)z,
   \]
   together with the literal shared \((L,M)\) packet.  The same equations
   are required in all fixed labels used by the diagonal anchors; the two
   charts may not be independently relabelled or obliquely normalized.
4. **Branch dependent.** Each chart is placed in one of two branch ledgers.
   In a rootless ledger,
   \(\gcd L_\nu=1\); the complete rows, endpoint injectivity, and
   scalar-zero nonnilpotence then give the proved three-site selector at
   each endpoint; these ordinary selectors are automatic by the extraction
   theorem.  Any fixed-label, separated, or own-edge compatibility beyond
   them remains an assumption.  In an inactive-root ledger, one additionally
   assumes that the selected cell on that same canonical line is diagonal in
   the common physical labels (renamed \(00\)) and that the line is routed
   to the clean endpoints
   \[
      K_{\nu,\mathrm u}=E_{00},\qquad
      K_{\nu,\mathrm c}=E_{00}-I,
   \]
   where \(s(K_{\nu,\mathrm u})=\sigma_\nu\ne0\),
   \[
   F_\nu^{[h]}=\sigma_\nu^{h-1}X_0,
   \qquad
   R_\nu q_\nu^{[h-1]}=-(X_1+X_2),
   \qquad R_\nu^{[h]}=0,
   \]
   and activity on their joining pencil is exactly \(tu\ne0\).  Thus the
   complementary row here means both its complete physical equation and
   cleanliness of the scalar-zero endpoint, not merely one selected
   coefficient.  A trace-only active chart, with selected coefficient zero
   and nonzero block trace, has the opposite unary/binary scalar orientation
   and requires a separate boundary ledger.

Then

\[
 \boxed{
 (I_{pq}:a_{pq}^\infty)\ne S
 \quad\text{or}\quad
 (I_{pr}:a_{pr}^\infty)\ne S.}
\]

Equivalently, at least one of the two source-provenant lines contains an
active clean point.

This is a proposed lemma, not a proved consequence of the cited
literature.  The automatic extraction theorem supplies items 1 and 3, the
goodness and first-activity parts of item 2, and the ordinary rootless
selectors in item 4.  It does not supply two diagonal unary--complementary
charts, compatible fixed-label selector cuts, or generic activity of the
second overlap line.  No theorem routes every inactive selected line into
the extra packet in item 4.
The label split is also real: the selected line may have \(a=b\) or
\(a\ne b\), and the off-diagonal scalar-zero packet cannot simply be renamed
as the diagonal complementary endpoint.  These are assumptions of this
conditional target, not established extraction results.

The conclusion is intended for all four assignments of the two charts to
the rootless and inactive-root ledgers, including the two mixed assignments.
The following are output formats for a possible proof; they do not exhaust
those assignments by themselves.

* **Rootless output ledger.**  At the scalar-zero point \(K_{\nu,*}\), choose
  an exposed \(f_\nu\in L_\nu\) with \(f_\nu(K_{\nu,*})\ne0\), and write
  \(L_\nu=\mathbb C f_\nu\oplus L_\nu'\).  A successful anchored overlap
  argument could produce, on at least one rootless chart,
  \[
  \operatorname {rank}\!\left(
     L_\nu'\otimes S_{h-1}\longrightarrow
     S_{2h-1}/f_\nu S_{h-1}\right)\le h-1.                 \tag{1}
  \]
  Rootlessness says the same map is surjective onto its \(h\)-dimensional
  target, a contradiction.  At \(h=3\), (1) is precisely the desired
  rank bound \(\le2\).  The residual-gcd theorem also shows that (1) is
  equivalent to a common factor; the new content must be the
  source-provenant construction of its annihilating functional, not the
  rank reformulation itself.
* **Inactive-root output ledger.**  For the additionally routed diagonal
  endpoints in item 4, the uniform interpolation is
  \[
             {\cal E}_\nu(tK_{\nu,\mathrm u}+uK_{\nu,\mathrm c})
                    =tu\,\Omega_\nu(t,u),
        \qquad \deg\Omega_\nu=h-2.                            \tag{2}
  \]
  Only at \(h=3\) does this become
  \(tu(t\Omega_{\nu,0}+u\Omega_{\nu,1})\); there, no active point means
  that the two columns are independent or exactly one is zero.  For
  \(h>3\), no-active behavior is instead the proved bounded certificate
  \[
             (tu)^{h-2}\in I_{\Omega_\nu}.
  \]
  A uniform overlap proof must rule out the simultaneous physical
  certificates, not compare only two endpoint columns.  In a mixed branch
  it must couple this certificate to the rootless residual-Macaulay ledger.

If the remaining activity/compatibility/routing hypotheses above were also
proved for an arbitrary selected source, this lemma and the audited clean-pair theorem
would give the exact \(N\mapsto N-2\) descent, after which the six-site
obstruction closes the induction.  The conditional lemma alone does not
settle the main-line arrow.

## Guards the lemma must genuinely evade

1. **Off-diagonal hexagon guard.**  Six off-diagonal rows, aligned
   selectors, and the \(C_6\) cubic can coexist with coprime clean
   coordinates.  A proof of (1) must retain a nonzero coefficient of at
   least one diagonal target \(X_i\).
2. **Automatically filled selector jet.**  The scalar-zero packet already
   fills the exposed two-dimensional first-jet quotient.  Rank loss must
   occur in \(Q_f\), after the
   \(fS_{h-1}\) block is removed, not in the raw \(J_2\) quotient.
3. **Mixed-word Riccati guard.**  A separating selector can preserve all
   mixed rows by drifting its flags or leaking cofactors.  Both charts must
   synchronize the pure constant-word target flags; independent oblique
   selector normalizations are insufficient.
4. **Deconcentrated response guard.**  Schmidt-rank propagation excludes
   one-pair support but not a spread binary packet.  The proof must use the
   shared physical overlap and curvature, not support spreading alone.
5. **Flat/Bianchi and apolar guards.**  Reindexed top tensors make the
   first Bianchi scalar identity tautological, while top apolar membership
   forgets lifts.  The argument must use the literal overlap equation
   before multiplication by the common power and must be saturated by
   activity.
6. **Label and routing guard.**  Curvature selection does not force the
   selected colour cell to be off-diagonal, and an off-diagonal
   scalar-zero response is not the diagonal unary--complementary endpoint.
   A proof must handle both label cases or prove a separate fixed-label
   routing theorem; independent chart relabellings are not available.

## Primary adjacent sources

* D. A. Buchsbaum and D. S. Rim, [*A generalized Koszul complex. II. Depth and multiplicity*](https://doi.org/10.1090/S0002-9947-1964-0159860-7), *Transactions of the AMS* **111** (1964), 197--224.
* H. Ohsugi and T. Hibi, [*Toric ideals generated by quadratic binomials*](https://doi.org/10.1006/jabr.1999.7918), *Journal of Algebra* **218** (1999), 509--527.  It supplies graph-toric context; the exact primitive \(C_6\) kernel used here is established by the repository's direct lattice calculation.
* H. Maakestad, [*Modules of principal parts on the projective line*](https://doi.org/10.1007/BF02385482), *Arkiv för Matematik* **42** (2004), 307--324.  This is background for the principal-parts language; the selector divisibility theorem is proved in the repository, not imported from this paper.
* S. Shafiei, [*Apolarity for determinants and permanents of generic matrices*](https://doi.org/10.1216/JCA-2015-7-1-89), *Journal of Commutative Algebra* **7** (2015), 89--123; the paper also treats the generic hafnian apolar ideal.
* B. Lovitz and F. Petrov, [*A generalization of Kruskal's theorem on tensor decomposition*](https://doi.org/10.1017/fms.2023.20), *Forum of Mathematics, Sigma* **11** (2023), e27; its abstract splitting theorem is relevant to the backup Segre route, but no matching-compatible specialization is presently proved.

The literature therefore supplies useful analogies, divisor modules, and
abstract circuit constraints.  It does not identify the repository overlap
with an exact standard complex or prove the proposed saturation statement.
The decisive new content would remain physical: diagonal anchoring plus
exact two-chart overlap would have to force a failure of simultaneous
activity-saturated Macaulay exactness.
