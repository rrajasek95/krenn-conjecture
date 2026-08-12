# The ridge and reduced-Eq paths meet only at an unconstructed tail transgression

## Exact verdict

The desired correction to the closest normalized physical candidate
\(r_0-T\) is

\[
                             -r_v-e_{\rm Eq}.           \tag{1}
\]

There is a formally perfect three-piece decomposition of (1), but the
committed source data supply only its first two shapes conditionally.

For a face \(v\), matching \(N\in\operatorname{PM}(F_v)\), and the selected
incident cycle multiplier \(t\), the endpoint bar has exact source-labelled
output

\[
              B_{v,N}=(-\Omega_v,+q_{v,N};
                        \operatorname{ores}=1).         \tag{2}
\]

Multiplying by \(t\) gives \(Q_{v,N}=tq_{v,N}\). Every such product has
site profile \(P_3\sqcup K_2\): one residual site occurs twice and the
other four once. The target-preserving normalization makes \(t=1\) as a
coefficient, but does not erase its fine degree.

If one additionally had a source-valid comparison
\(t\Omega_v\mapsto r_v\), (2) would become

\[
              -r_v+Q_{v,N},\qquad\operatorname{ores}=1. \tag{3}
\]

The completed normal Hasse face has decisive boundary

\[
                              -e_{\rm Eq}.              \tag{4}

\]

It does **not** have boundary \(-e_{\rm Eq}-Q_{v,N}\). Expanding
\(h_v=\sum_Nq_{v,N}\) changes the polynomial coefficient of the Eq row; it
does not create a separate all-derivation companion coordinate. At the
q-zero top, differentiating by \(N\) consumes \(q_{v,N}\) and leaves the
unit rather than a surviving \(-q_{v,N}\) tail.

Thus (3)+(4) leaves exactly \(+Q_{v,N}\). A third cell

\[
 A_{v,N}=(\operatorname{ridge}=0,
          \operatorname{Eq}=0,
          \operatorname{companion}=-Q_{v,N},
          W=\operatorname{tgt}=0,
          \operatorname{ores}=-1)                     \tag{5}

would give the exact composition

\[
                (-r_v+Q_{v,N})+(-e_{\rm Eq})+(-Q_{v,N})
                         =-r_v-e_{\rm Eq}.             \tag{6}

The ordinary-residue values \(1+0-1\) cancel in (6). Equation (6) is
source-valid only if all three pieces live in the same
repeated-site fine degree and the first comparison preserves endpoint and
chart typing. In particular, the formal chart label \(-S_v\) is not being
renamed as physical anchor incidence.

## The missing tail cell is already known—but not constructed

Cell (5) is precisely the reduced companion augmentation isolated by the
Component-IV endpoint and Tor gates. The fifteen literal route columns are

\[
                              (-\Omega_v,+q_{v,N}),
\]

and their cokernel is primitive \(\mathbb Z^5\). The exact source-coordinate
criterion for (5) is a selected denominator kernel vector

\[
 k_v=d_{v,m_v}+\sum_{(u,c)\ne(u,m_u)}z_{u,c}d_{u,c},
                  \qquad b(k_v)=0,                    \tag{7}

\]

whose selected projection is \(e_v\). Equivalently, the denominator Tor
transgression must hit the corresponding face basis vector. This is an
exact characterization, not an existing source cell.

Consequently paths #1 and #2 do expose the same formal tail cancellation,
but they do not yet share one **constructed** physical attachment. Even if
(5) is built, one must still identify the endpoint ridge \(\Omega_v\) with
the rootless repeated-site ridge \(r_v\) in the same mapping cone. The
smallest genuinely shared datum is therefore a multidegree-preserving
mapping-cone cell combining (7), the physical reduced-Eq face, and the
\(\Omega_v\)-to-\(r_v\) comparison.

## Why the `8771755` attachment theorem does not close (5)

Commit `8771755` treats the ten **off-cycle** unmatched monomials occurring
in the residual polynomials \(R_v\). Conditional on a nonzero endpoint
product at \((x,v)\), a complete six-term coefficient routes such a tail to
a unit, same-tail deletion/Fitting carrier, or a different-tail C4
off-anchor/Hall branch.

That theorem is not a chain with boundary \((0,-q_{v,N})\):

1. its output is a routing alternative, not a zero-ridge companion
   nullhomotopy;
2. it requires an active response hole, which normalized internal tail data
   do not force; and
3. on the exact specialization \(R_v=0\), all ten off-cycle inputs vanish,
   while the selected C5 matching is normalized to one and is not in
   `8771755`'s tail domain.

Therefore it cannot supply (5) on the exact clean C5 slice. A future
response-hole accessibility theorem may route the general \(R_v-R_w\)
branch, but it is logically different from the reduced companion
transgression needed in (6).

## Scope and verification

This is an exact conditional composition and a type-level no-go for the
committed endpoint-bar, normal-Hasse, reduced-companion, and unmatched-tail
inventories. It does not exclude a new higher relative generator.

Run:

```text
python3 computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py
python3 -O computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py
python3 -I -S computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py
```

The checker pins all six source theorems, verifies the endpoint/normal/tail
signs, all repeated-site profiles, the conditional sum (6), and the exact
scope exclusion for `8771755`.

Frozen ledger SHA-256:

```text
2cd7a79b24057e3653bb0af9020f183f0544a13dbca0ef4313b53da0c9a189eb
```
