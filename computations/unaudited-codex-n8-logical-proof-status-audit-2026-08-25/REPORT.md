# Logical proof-status audit: finite certificates versus induction

## Verdict

The Krenn–Gu conjecture remains open, including the general bicoloured
`n=8,d=3` case.  The exact D6--D11 evidence closes several *bounded
nonmembership* statements, but it supplies neither a finite induction in
certificate degree nor the uniform site-induction package.  Two distinct
gradings must not be conflated: `D` is homogeneous Nullstellensatz degree at
fixed `n=8`, whereas `h=n/2` is the site-order parameter in `PAComp(h)`.

This audit used only small reports, ledgers, and manifests.  It did not read a
provider, selected-column file, checkpoint, cache, or matrix and ran no solve.

## Ranked implication map

### 1. Certified clean-pair descent: complete conditional spine

The certified implication

```text
active clean pair at n -> exact source at n-2
                       -> minimality, or the certified six-site contradiction
```

is complete.  The missing lemma is not another bounded ideal calculation: it
is the branch-complete physical package `PAComp(h)` for every `h>=3`, producing
either an active clean pair or an accepted physical terminal contradiction.
The proof sketch expressly lists the open physical comparison, augmented
readouts, rootless/inactive/face-zero routing, and terminal promotion.

### 2. Fixed-`n=8` X5 triangle reduction: closest working-exact route

Working-exact source replays give

```text
hypothetical normalized X5 point
  -> a live cross cell
  -> under the all-560-triangles-blocked hypothesis, one canonical flag
  -> one of four literal blocker ideals.
```

An active triangle instead gives the clean cap and certified descent.  Thus an
exact unit certificate for *each* of the four blocker ideals, possibly in
different degrees, would close this `n=8` arrow.  The reduction is still in
`unaudited-*`, so promotion is separately required before citing it as a
certified-spine theorem.

The D6--D11 results point in the other algebraic direction.  D6--D10 have
exact characteristic-zero separating duals for all four branches.  At D11
only the direct branch is globally certified; the triangle branch is a
nonterminal one-prime checkpoint with 1,250,001 selected columns and support
1,378,456, while the other two coloured branches are unresolved.  A dual
showing `t^D` is *not* in an ideal rules out a degree-`D` unit certificate; it
does not show that the branch is empty.

Minimal missing lemma: literal rational unit membership for all four branches
at some degrees, or a same-source cancellation-clean cap theorem.  Merely
completing the three coloured D11 lanes as nonmembers would extend only the
certificate-degree lower bound.

### 3. Affine live-cell cover: decisive only with membership or regularity

The 251-variable cover is the full normalized fixed-live-cell affine system.
The exact ledger proves characteristic-zero nonmembership of `t^D` for every
`D=4,...,11`.  The inherited seven-row dual works at D9--D11 but has a literal
first failure at D12.  The latest independently audited D12 state is exact and
resumable at round 1587 (2,927,014 exposed columns, support 5,598), but is not a
closed global dual or a membership result.

Minimal missing lemma: either produce `t^D in I^h` at some degree, which is a
finite unit certificate, or prove an explicit structure-specific
saturation/regularity bound `B` with

```text
1 in I_aff  <=>  t^B in I^h,
```

and then obtain a terminal degree-`B` verdict.  No retained theorem gives
`B<=12`.  With such a valid bound, a degree-`B` *nonmember* would imply a point
on the exact cover, not emptiness; reversing this implication is a
Nullstellensatz sign/direction error.

### 4. Degree stabilization: the natural recurrences are refuted

The X5 extension audit gives the exact finite contraction criterion.  It fails
for every sealed D6--D8 certificate except the one-step direct D8-to-D9 lift:
the coloured D8 certificates already violate `C_1`, and the direct D8
certificate violates `C_2` and `C_4`.  D10-to-D11 transport has 76, 76, and 70
literal violations on the coloured branches.  Independently, the affine
D8-derived seven-row functional fails at D12.  These are explicit
counterexamples to the proposed shift recurrence, not merely missing tests.

A real induction would need a finite-dimensional, source-labelled
inverse-system module closed under every relevant contraction, together with a
degree-raising right inverse preserving all generator annihilations and the
target pairing; or an explicit regularity/saturation theorem for the exact
ideal.  No such object or theorem is retained.  Invoking Noetherianity without
proving the numerical bound and compatibility is circular.

### 5. Representation stability: coefficient layer only

The proof spine proves polynomial/stable coefficient data in `h`, but also
states that spectator suspension raises the isotypic level and uniformity must
be proved per composed step.  The independent stress report agrees: it does
not supply the physical Cartan/Hasse lift.  Therefore “representation
stability, so one `h` (or `n=8`) suffices” is a false extrapolation.  The
minimal missing lemma remains the source-provenant physical `PAComp(h)` with
all routing and terminal-promotion hypotheses.

## Fail-closed guards

- Finite nonmembership is compatible with both a higher-degree unit
  certificate and a genuine point; it decides neither.
- A selected-subsystem CEGAR vector is not global while any violating/frontier
  column remains.
- A single-prime partial vector is not a characteristic-zero theorem.  The
  accepted D6--D10 and affine D4--D11 statements avoid this problem by exact
  integer/rational replay; the current coloured D11 checkpoint does not.
- A live cross cell alone does not select the canonical triangle.  The
  symmetry reduction uses the universal all-triangles-blocked hypothesis.
- `D=10,11` is certificate degree, not site order `n=10,11`.

The machine-readable ranking, exact bounded coverage, evidence paths, and
invalid-inference ledger are in `results_logical_proof_status_audit.json`.
