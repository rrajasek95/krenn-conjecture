# Parallel proof attack board after unconditional curvature selection

Audit date: 2026-07-29.

Supersession note: this board records the portfolio immediately after
unconditional curvature selection.  Later full-nine shore, residual
Macaulay, selector-incidence, and two-anchor guards have merged or retired
several entries.  For current task allocation use
[the consolidated proof frontier](consolidated-proof-frontier.md).

## 1. Current trunk

The conjecture is still open, but it no longer has a curved/flat global
split.  Given any hypothetical exact ternary aggregate source on even
\(N\geq8\), choose a representative having minimum entry support.  The
audited flat reductions prove that not all canonical good-fan transitions
can vanish.  Hence that representative contains a literal nonzero physical
minor

\[
             AU-BF\ne0,                                          \tag{1}
\]

and therefore a canonical cap line

\[
             K_z=E_{ab}+zI                                      \tag{2}
\]

which is active away from a finite divisor.  If the clean-error polynomial

\[
             {\cal E}_{p,q}(K_z)                                \tag{3}
\]

has a common active zero, the exact clean-pair theorem gives the
\(N\mapsto N-2\) descent and the six-site obstruction closes the induction.
The single missing main-line arrow is therefore

\[
 \boxed{\text{generically active physical line}
        \Longrightarrow\text{active clean point}.}             \tag{4}
\]

Parallel work should attack (4) through different consequences of the
same physical minor, not reopen the now-empty flat branch.  A useful result
must either prove (4), bypass it with an exact selector descent, or produce
a source-level contradiction satisfying all transverse target rows.

## 2. Highest-value parallel attacks

### A. Exclude the no-common-root branch on one line

The [uniform response-resultant theorem](curved-rootless-line-uniform-response-resultant.md)
gives the no-root branch an exact all-order form.  Eliminating the physical
target row gives

\[
 {\cal E}(K)=\sum_{j=2}^{h}s(K)^{h-j}q^{[h-j]}r(K)^{[j]}.       \tag{5}
\]

If its scalar coordinates have gcd one, their Macaulay multiplication map
has rank \(2h\), equivalently two physical coordinate combinations have
nonzero degree-\(h\) resultant.  At the unique scalar-zero point of an
off-diagonal canonical line, rootlessness also forces

\[
 r_*q^{[h-1]}=-\alpha\Delta_{2h,3},\qquad
 r_*^{[h]}\ne0,                                                \tag{6}
\]

where \(r_*\) is an invertibly paired response of the two injective
endpoint stars.

At \(N=8\), the independently audited
[cubic Macaulay packet theorem](curved-no-root-macaulay-and-scalar-zero-packet.md)
turns the resultant into one rank-six minor on six shifted columns from
literal four-cut rows.  Each good endpoint has either a three-site selector
or a sharp one-/two-site concentration.

Three independently audited refinements make this packet substantially less
open-ended.  First, the
[scalar-zero tangent alternative](curved-scalar-zero-tangent-apolar-hall-alternative.md)
scalarizes all nine physical rows as

\[
 P_\omega^TH(Q_\omega)S_\omega
   =D_\omega-\operatorname {haf}(Q_\omega)a.                    \tag{7}
\]

Either \(r_*^{[h]}\) has only pure coordinates—in which case the ternary
subcase is the desired descent—or one mixed word has nonzero response
hafnian, zero hafnian derivative, and a balanced simultaneous-star matrix
with nonzero permanent.  Second, the
[sparse-star propagation theorem](rootless-sparse-star-propagation-and-rank-one-shore-guard.md)
closes the support-on-at-most-two-sites alternative immediately, since it
would force \(r_*^{[3]}=0\).  Third, the
[uniform full-nine exceptional-shore theorem](full-nine-type3-annihilator-plane-closure.md),
with its
[independent audit](full-nine-type3-annihilator-plane-closure-independent-audit.md),
uses the literal nine pair rows to prove

\[
 \operatorname {rank}P_{\bar x},\operatorname {rank}S_{\bar x}\ge2
 \qquad(x\in W).                                               \tag{8}
\]

This holds at every even residual size.  For \(h\ge3\), rootlessness
removes the two-site alternative as well, so both endpoint stars have
three-site selectors and no sparse-shore case remains.

Thus the two direct deliverables are now exact: force the full-nine
cohafnian identity (7) to contradict the Hall-certified mixed permanent or
to retain all three pure colours; prove that the selector coordinates meet
every possible rank-six Macaulay minor and then its degree-\(h\) uniform
analogue.  Generic
vector cubics, arbitrary apolar hafnian pairs, and one contracted response
row all have exact guards, so none of those relaxations can close the line.

### B. Couple the two charts selected by the minor

The nonzero square \(AU-BF\) supplies two overlapping coordinate cap
charts, not just one abstract line.  Two known roots on one chart can be
removed in one formula; at \(8\to6\) the residual is
\(uv(uR_0+vR_1)\).  The charts share literal \((L,M)\) coefficient data,
and their new clean equations are coupled by the same nonzero square.

An independently audited
[two-chart unary-root guard](curved-n8-two-chart-unary-root-guard.md)
shows that two unary coordinate roots can satisfy their complete
contracted target tensors, all four good-star injectivity conditions, the
shared \((L,M)\) equations, and \(AU-BF\ne0\) simultaneously.  The
padding colours are invisible at both roots.  Thus comparing only those
two root tensors cannot close the branch.

The independently audited
[complementary-row theorem](curved-complementary-row-coupling-frontier.md)
now inserts exactly that missing covector.  Joining a clean unary point to
a clean scalar-zero binary point gives

\[
 {\cal E}(tK_0+uK_1)=tu(t\Omega_0+u\Omega_1).                    \tag{9}
\]

An active clean point is automatic unless \(\Omega_0,\Omega_1\) are
independent or exactly one vanishes.  A shore-flattening lemma proves that
a binary scalar-zero response cannot remain supported on the one residual
pair used by the old padding guard, so the complementary row genuinely
forces propagation.  A sharp deconcentrated packet shows that propagation
alone is still consistent.

The concrete two-chart deliverable is therefore no longer “add another
row.”  It is to prove that the two source-provenant charts sharing
\((L,M)\) and \(AU-BF\ne0\) cannot both realize the independent or
endpoint-degenerate alternatives for their pairs
\((\Omega_0,\Omega_1)\).  That statement would give an active clean point
from (9) with no support census.

### C. Recover channel sparsity; direct minor inversion is blocked

The independently audited
[symmetric-square selector obstruction](curvature-minor-symmetric-square-selector-obstruction.md)
shows that the determinant in (1) is exterior-square data, while a
two-star matching response transforms in the symmetric square.  After
normalizing the two selected flags, the physical response has the exact
form

\[
 \xi\eta=AF\,X^2+(AU+BF)XY+BU\,Y^2.                           \tag{10}
\]

The desired curvature \(AU-BF\) is not the \(XY\) coefficient, and the
two same-channel terms cannot be supplied or subtracted by physical
same-endpoint rows.  A literal good-pair guard satisfies the complete
selected mixed target slice with both \(X^2,Y^2\ne0\).  Moreover
\(X^2=0\) is equivalent to \(X\) being supported at at most one residual
site.

Thus direct inversion is not an independent descent route.  It becomes
useful only after a **physical channel-sparsification lemma** derived from
other exposed-colour rows.  The rootless analysis now supplies a first
real instance: two-site support is impossible, while rank one away from an
exceptional site has the rigid factorization (8).  Work here should use the
ternary diagonal, the omitted eight rows, or an overlapping chart to force
\(E_x(LM)^{[2]}=0\) or a literal one-site channel.  Another manipulation of
the \(2\times2\) inverse without that input cannot advance the proof.

### D. Close the faithful cubic Hessian packet as a backup

For two nonneighbours of a cubic centre, the audited exact dichotomy is:

1. two faithful nullity-at-least-two spaces are visible on the same common
   exterior star and all their cross-Hessian responses land in one tensor
   line; or
2. one colour has the pure \(3\times3\) two-crossing packet: eight Hessian
   responses vanish and the ninth is a nonzero decomposable target.

The nonfaithful alternative is now confined to at most six typed pure ports
and hence to order at most eighteen.  Thus every cubic-centred source at
even order at least twenty has a faithful residual pair.  The useful target
is a theorem for the faithful one-line cross-image—shared kernel, selector,
or sparse star—together with exact treatment of the finitely bounded small
cores.  This route is independent of global flatness and should not become
another unbounded local-star census.

### E. Finish the E2 plane-packet boundary

On the dense defect-three chart, a diagonally live rank-two block is now
one of:

1. a glued physical two-plane packet;
2. a complement-sum block;
3. an endpoint-hole collapse.

The complement-sum locus is empty when all three defect components are
imbalanced and equals the constrained universal inactive core when all
three are balanced.  The remaining targets are therefore exact: propagate
an endpoint hole to a sparse row, glue differently labelled plane packets
across their rank-one intersection, or eliminate the one-/two-imbalance
component signatures.  Rank-zero/rank-one blocks and zero diagonals must be
handled separately rather than silently absorbed.

## 3. More independent backup routes

### F. Zero-shore apolar ladder

A growing aggregate-zero shore forces linearly many full internal stars on
its complement and an \(O(h)\)-sparse cross-interface unless curvature
returns.  More strongly, three coordinate monomials lie in one hafnian
ideal with all mixed permanent syzygies, and the common matching power
obeys an exact multiaffine apolar ladder.  A useful next theorem would turn
those syzygies into a multigraded degree or Betti-number contradiction, or
show that one full internal star supplies an active clean cap.  This route
is independent of the cubic classification and becomes stronger with
\(N\).

### G. Filtered acyclicity of pair-cap overlaps

Physical annihilator corrections on overlapping pair charts satisfy a
literal Koszul-type lift equation before multiplication by the common
power.  Prove that the kernel of this overlap complex is gauge, or else
forces one of the registered sparse/low-rank alternatives.  This would
turn chartwise E1/E2 data into one global cap family.  Mere Bianchi flatness
is not enough; the target is filtered injectivity on the actual Hessian
annihilator module.

### H. Matching-compatible Segre circuits

Kruskal uniqueness already excludes every decorated Wick expansion in its
visible range.  Outside that range, every tripartition forces a short exact
linear circuit among grouped Segre products.  The missing theorem is to
show that a circuit whose terms come from decorated perfect matchings has a
shared physical edge, a tight cut, or a selector cap.  A classification of
arbitrary Segre circuits would be excessive; only circuits stable under the
matching deletion/exchange operations are relevant.

### I. Multi-pair cap incidence

For one pair, cap-space dimension and intersection theory are guarded by
exact dirty root-cover models.  A viable algebraic-geometric version must
use two or more overlapping physical pair-cap spaces and the transverse
target equations on their intersection.  The exact deliverable is a
proper saturated common-zero statement for the joint clean-error ideal,
not a dimension count on one projective cap space.

## 4. Work to deprioritize

The following may still falsify a proposed lemma, but they are not natural
main-line proof work:

* another fixed-order collision census;
* a larger support enumeration around one polarized seed;
* bare curvature/Bianchi identities without transverse target rows;
* raw kernel-dimension or graph-density counts without physical response
  provenance;
* isolated generic-rank computations whose exceptional strata are not
  closed exactly.

The dependency order is therefore A/B first, C only through its new
sparsification hypothesis, D as the strongest structurally independent
backstop, and E/F/G/H/I only when capacity permits.
