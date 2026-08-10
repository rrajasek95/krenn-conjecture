# Dependency audit for the uniform square-zero one-bad cap

## Verdict

Commit `ca6362b` proves a complete **landing lemma**: once an exact
square-zero one-bad physical pair exists, an explicit active clean cap and
the exact `N -> N-2` descent follow at every even order.  It does not prove
the **extraction lemma** which would produce that pair from the certified
selected full-nine packet.

More sharply, the one-bad pair cannot be either selected good chart in the
unified overlap theorem.  A selected `pq` or `pr` chart has injective
deleted endpoint-star maps.  In the one-bad normal form the selected colour
row is zero at both endpoints, so both maps have rank at most two.  Under
the additional square-zero hypothesis, each of their two remaining colour
rows is supported at at most one residual site, so each whole endpoint star
is supported on at most two sites.  Rank and support are unchanged by a
colour normalization, and tilting a cap covector does not alter either
source star.

Thus the square-zero cap is not the generic/rootless `SP-CLEAN-BRIDGE`
landing in disguise.  Reaching it requires a new exact source modification
or a reselection to a different, singular physical pair.  That is itself a
theorem-strength step.

The exact audit is
`computations/verify_uniform_one_bad_clean_cap_dependency_audit.py`.

## 1. Exact map of the two packets

For a physical pair `xy`, the automatic full-nine theorem gives

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2.                                  \tag{1}
\]

The square-zero one-bad packet is the specialization, after one physical
colour permutation and scalar normalization,

\[
 A_{xy}=\lambda E_{aa},\qquad p_a=s_a=0,\qquad\lambda\ne0, \tag{2}
\]

together with, for the two complementary colours `b,c`,

\[
 \lambda q^{[h]}=X_a,\qquad
 p_i s_jq^{[h-1]}=\delta_{ij}X_i\quad(i,j\in\{b,c\}). \tag{3}
\]

Equation (3) is automatic from the full nine rows **after** (2) is known.
The full-nine theorem does not force (2).

Use the cap whose `(a,a)` entry is `lambda^-1` and whose complementary
binary block is

\[
 \begin{pmatrix}1&1\\-1&1\end{pmatrix}.                \tag{4}
\]

Its direct scalar and target coefficients are all nonzero.  Its effective
binary response is

\[
 R=p_bs_b+p_bs_c-p_cs_b+p_cs_c.                         \tag{5}
\]

The logically minimal extra condition is

\[
                              R^{[2]}=0.                 \tag{6}
\]

In characteristic zero, (6) kills every higher power of `R`, and (1)--(5)
give

\[
                         (q+R)^{[h]}=X_a+X_b+X_c.       \tag{7}
\]

The concrete hypothesis proved sufficient in `ca6362b` is stronger but
especially source-transparent:

\[
 p_b^{[2]}=p_c^{[2]}=s_b^{[2]}=s_c^{[2]}=0.            \tag{8}
\]

It implies (6) coefficientwise in the site-square-zero algebra.  For a
literal star row, each identity in (8) is equivalent to support at at most
one physical residual site.

## 2. Why this is not a selected unified chart

The curvature and automatic extraction theorems select two **good** pairs.
For each selected pair, both deleted endpoint-star maps

\[
 P:\mathbb C^3\longrightarrow\bigoplus_{z\ne x,y}V_z,
 \qquad
 S:\mathbb C^3\longrightarrow\bigoplus_{z\ne x,y}V_z             \tag{9}
\]

are injective.  Conditions (2) give `P(e_a)=S(e_a)=0`.  Hence

\[
                 \operatorname{rank}P,\operatorname{rank}S\le2. \tag{10}
\]

No invertible endpoint basis change can turn (10) into injectivity.  The
tilted second-chart theorem changes the contracted matrix direction from
`I` to `I+E_ij`; it leaves `A_xy`, `P`, and `S` fixed.  Its intrinsic
zero-block branch has `A_pr=0` and is nowhere active, not the nonzero
scalar-unit block (2).

There is a second independent consistency check.  On an intrinsic
scalar-unit **good** pair, anchor--curvature synchronization gives

\[
                             (U_a,\Theta_a)\ne(0,0).    \tag{11}
\]

In (2)--(3), however, `G_a=lambda*q`, and direct substitution gives
`U_a=Theta_a=0`.  There is no contradiction: (11) assumes a good pair,
while the one-bad pair violates that assumption.  It does rule out silently
identifying the one-bad packet with the intrinsic good scalar-unit branch.

## 3. Rootless, shore, and inactive branches

The branch separation is exact.

| Unified branch | Proved information | Relation to the one-bad cap |
|---|---|---|
| Rootless selected chart | Complete full-nine rows, injective endpoint stars, scalar-zero response nonnilpotence | Cannot be the same pair: (10) already fails |
| Rootless sparse/type-3 subbranch | The uniform type-3 theorem gives off-site rank at least two; nonnilpotence then forces a three-site selector at each endpoint | The square-zero one-bad endpoint is supported on at most two sites, so this route is explicitly closed |
| Rootless no-disjoint-bases branch | The maximal-shore theorem classifies aggregate common-coloop, line-plus-plane, and endpoint-dark shores | It does not force a zero colour row or the four individual self-squares (8) |
| Rootless disjoint-bases branch | Ordinary three-site selectors | It requires the still-open source-provenant Macaulay annihilator, not sparse one-bad concentration |
| All-inactive selected chart | Roots lie on the activity divisor, with the existing boundary ledgers | The physical pair remains good and injective; inactivity of a cap point is not singularity of an endpoint star |
| Tilted `pr` chart | Generic activity if `A_pr != 0` | Changes only the cap direction; cannot produce (2) or (8) |
| Direct-free `pr` auxiliary | `A_pr=0`, full-nine triangular overlap, no activity | Not the scalar-unit one-bad pair and gives no clean cap by itself |

The full-nine exceptional-shore theorem is particularly important here.  It
does not merely fail to prove concentration; on the rootless good chart it
eliminates the two-site endpoint-support alternative which (8) would create.
Therefore any proof using `ca6362b` must leave the rootless selected chart,
not reinterpret its sparse subbranch.

## 4. The separate reciprocal route

The shared-reciprocal Lemma-E and anchor-safe retraction results can produce
the unary-top/binary-response equations (2)--(3) on a
projection-degenerate **singular-arm** route.  This route is not one of the
selected good charts in the unified theorem.  It also stops before (6) or
(8): the arbitrary-multisite defect has eight quadratic repeated-label
sectors, and the current theorem explicitly leaves their concentration
open.

Thus the existing reciprocal reduction proves that the one-bad row packet
is a natural boundary object.  It does not supply the square-zero clean cap
on every source, or even on every one-bad packet.

## 5. Minimal sufficient missing lemma

The exact new statement needed to consume `ca6362b` is the following.

> **Source-faithful one-bad clean-cap extraction lemma (open).**  Let
> `N=2h+2>=8`, and let `A` be the synchronized exact ternary source selected
> by the certified spine.  If `A` has no active clean cap already, then an
> exact source-preserving modification or a physical-pair reselection
> produces a pair `xy` satisfying (2) and (3), for which the effective
> response (5) satisfies (6).

The square-zero version may replace (6) by the stronger four identities
(8).  If extremality is used to force the modification, the proof must also
show the appropriate maximum-anchor/support monotonicity; that monotonicity
is a proof mechanism, not an extra hypothesis needed by the cap itself.

This is minimal in the following sense.

1. Once (2) is known, the complete nine rows give (3).
2. Once (6) is known, `ca6362b` gives the explicit active clean cap.
3. The certified clean-pair theorem then gives an exact source on `N-2`
   sites.
4. Minimum-order induction and the certified six-site theorem give the
   contradiction.

No overlap, shore, Macaulay, or inactive-boundary hypothesis is needed
after the extraction lemma has produced (2) and (6).

## 6. Complete dependency ledger

| Input | Status | What it proves here |
|---|---|---|
| `SP-CURVATURE` | Certified | A generically active physical line on a good pair |
| `ROOT-EXTRACTION` | Certified | Both full-nine packets and the tilted/direct-free alternative, with good endpoint maps |
| `SP-CLEAN-BRIDGE` | **Open; no accepted supersession** | The selected-line-to-active-clean implication under audit |
| Anchor--curvature synchronization | Proved current theorem | Places curvature and extremality on the same source; does not make the pair one-bad |
| Uniform full-nine type-3 closure | Proved and consumed by the rootless audit | Excludes sparse/two-site endpoint stars in the rootless good branch |
| Uniform maximal-shore classification | Proved/audited classification | Routes failure of disjoint selectors; does not force (2), (6), or (8) |
| Tilted/direct-free theorem | Included in certified extraction | Supplies activity or a triangular auxiliary; does not change source support |
| Shared-reciprocal anchor-safe retraction | Proved current theorem on a separate singular-arm route | Supplies one-bad rows there; not square-zero concentration |
| Uniform square-zero cap (`ca6362b`) | Proved current local lemma, not a spine supersession | `(2)+(3)+(8)` gives an active clean cap and exact descent |
| `SP-DESCENT` | Certified | Active clean cap gives a finite exact `N-2` source |
| `SP-K6` | Certified | Terminal arbitrary-complex six-site contradiction |

The first two certified items do not imply the ninth.  The missing bridge is
exactly the new extraction lemma in Section 5 (or some different direct
active-clean argument).

## 7. No hidden `N=8` shortcut

At `N=8`, `h=3`, the full-nine system is the open eight-vertex coefficient
system itself.  The calibrated theorem says that `SP-CLEAN-BRIDGE` at this
order is equivalent to emptiness of that system.  Therefore an unconditional
proof of the extraction lemma at `h=3` would already prove the open `N=8`
case; it cannot be treated as a routine consequence of finite degree.

Top degree only removes response powers above the six-site matching degree.
It does not force `R^[2]=0`.  The arbitrary-multisite one-bad calculation
exhibits the eight surviving repeated-label sectors after permanent
cancellation.  The fixed-star `N=8` theorem closes the special case only
because its four literal ports already satisfy (8); there is no proved
reduction from arbitrary endpoint stars to those ports.

Finally, `ca6362b` is itself uniform for every `h>=3`.  Its useful content is
not an `N=8` coincidence: it finishes the cap algebra at all orders once
concentration is extracted.  The extraction, not the cap calculation, is
the entire remaining theorem-level cost.

## Reproduction

```bash
.venv/bin/python computations/verify_uniform_one_bad_clean_cap_dependency_audit.py
.venv/bin/python -O computations/verify_uniform_one_bad_clean_cap_dependency_audit.py
python3.14 computations/verify_uniform_one_bad_clean_cap_dependency_audit.py
```
