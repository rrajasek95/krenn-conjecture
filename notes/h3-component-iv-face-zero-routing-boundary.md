# Curvature does not open a deleted face, and the five-face zero locus is not an inactive-root branch

Research boundary only.  This audit identifies the exact landing left after
the selected-denominator separator.  It does not prove that the full-source
five-face zero locus is nonempty or empty, and it does not prove the unified
overlap theorem.

## Exact routing verdict

For the five required Component-IV memberships, the selected-word separator
gives

\[
 b(d_{v,m_v})\in\operatorname {im}(b_{\rm oth})
       \Longrightarrow h_v=0.                            \tag{1}
\]

There are two sharply different uses of (1).

1. On the open union \(\bigcup_vD(h_v)\), all five memberships are
   incompatible with a nonzero full-source quotient.  If the source-routing
   theorem forced this open union, (1) would be the desired contradiction.
2. On the closed locus \(V(h_1,\ldots,h_5)\), the separator is silent.  The
   old rational packets show that scalar vanishing is not sufficient for
   whole-column membership, but the converse calculation is not the next
   routing task.

The first alternative is **not** currently forced by curvature.  The exact
direct-free and tilted guards have respectively

\[
 \kappa=-\tfrac14,-\tfrac52,
 \qquad h_1=\cdots=h_5=0.                               \tag{2}
\]

They are not full-source points, so (2) is a counterguard only to the
implication “\(\kappa\ne0\) forces some \(h_v\ne0\).”  It neither constructs
nor excludes a physical source on the closed locus.

## What the rootless five-cycle calculation does prove

On the five-cycle specialization used in the rootless module audit,

\[
 (h_1,h_3,h_5,h_2,h_4)=(bd,ad,ac,ce,be).               \tag{3}
\]

Thus after localizing \(abcde\), every \(h_v\) is a unit.  Equation (1)
immediately proves that none of the five selected memberships can hold in a
nonzero quotient on that Laurent test chart.  At the diagonal point
\(a=b=c=d=e=1\), all five separators read one.

This is an exact negative membership result, but it is **not** a physical
chart cover.  The five-cycle was introduced as a dominant specialization
proving algebraic independence and exposing the minimal pentagon resolution.
The committed positive-interface note explicitly warns that its Laurent
normalization makes no assertion about physical sources on the boundary.
Consequently (3) cannot be promoted into “every rootless source has a
nonzero \(h_v\).”

## No existing rootless-to-inactive landing

The automatic two-chart theorem splits a selected cap line according to the
gcd of its clean-error coordinate polynomials:

* **rootless:** gcd one, hence no clean point;
* **all-inactive:** clean roots exist, but lie on the activity divisor.

The five \(h_v\), by contrast, are deleted-four-site hafnian coefficients of
one fixed internal word.  None of the proved automatic packet, goodness,
activity, full-nine, overlap, or Hall--Rado selector statements identifies
simultaneous vanishing of those five coefficients with either side of the
cap-line gcd split.  In particular, \(h_1=\cdots=h_5=0\) is not an already
proved landing in the all-inactive ledger.

The remaining theorem-strength statement is therefore exactly one of:

\[
 \text{physical rootless source}\Longrightarrow
       \bigvee_v h_v\ne0,                               \tag{4}
\]

or a source-labelled proof that the simultaneous zero stratum routes to an
already closed inactive/source-unit branch.  Neither implication is present
in the committed dependency graph.  Until one is proved, the zero stratum
stays inside the rootless Component-III/IV interface and the converse Tor
membership calculation should not be pursued speculatively.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_component_iv_face_zero_routing_boundary.py
.venv/bin/python -O computations/verify_h3_component_iv_face_zero_routing_boundary.py
```

The checker pins the selected-word separator, the exact curvature packets,
the rootless five-cycle resolution, and the automatic two-chart theorem.  It
recomputes (2), the five monomials (3), and the Laurent membership verdict.
The distinction between the internal face-zero stratum and the cap-line gcd
split is a dependency audit, not an inferred algebraic equivalence.
