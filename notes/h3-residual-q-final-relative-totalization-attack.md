# Final local attack: one augmented Spencer square

## The target theorem

The shortest local theorem now has a precise chain-level form.

> In the labelled repeated `P3+K2` grade and word `1211222`, the complete
> order-six Hasse tower `Theta_6` and the shifted relative ridge jet
> `gamma_v=-dOmega_v` are faces of one physical augmented Spencer cycle
> `M_v`.

The required image is

```text
literal source boundary = 0,
ordinary residual       = -delta,
D, W, target, anchor    = 0,
eta_z                   = 1+delta_(vz)u_z/t,
sigma                   = -q_pq:22.
```

No entry in this target is now guessed:

- `Theta_6` supplies the zero source and `-delta` rows;
- its complete unsigned Hasse tower is coherent through all six layers;
- `gamma_v=-dOmega_v` supplies exactly the eta/sigma rows and no ordinary
  boundary; and
- both constructions meet at the primitive endpoint/cofactor face
  `07:11 wedge 24:11`.

## Why one square should exist

The residual symbol already factors as an endpoint/tail commutator

\[
              (E_- - E_+)(T_0-T_1).
\]

The tail change is a literal covariance operation on complete source rows.
The endpoint change is the relative ridge differential `-dOmega_v`.  The
order-five and order-six corrections are precisely the lower Hasse faces
needed to make their mixed square source-closed.  Thus the desired object is
not a new matching identity: it is the interchange homotopy between
endpoint principal parts and tail covariance.

In a universal Spencer/principal-parts resolution this interchange square
is formal.  The proof burden is to show that its four sides descend to the
physical labelled repeated component with all augmented readouts—not to
prove another support census.

The universal assertion is now an exact theorem: the
[Euler contraction of the differential-symbol Spencer complex](h3-universal-spencer-euler-contraction.md)
contracts every positive-total-degree face.  Hence neither the 126 first
faces nor any higher Hasse layer is an independent obstruction.  All local
failure is relative: it lies in the mapping cone of the universal-to-
physical labelled comparison, where a terminal-visible class is itself the
alternative relative generator.

## A concrete proof order

1. **Choose the physical grading.**  Retain the `pq` and `xv` halves of
   `-dOmega_v` as distinct shifted labels.  Do not replace them by the
   determinant `tb-ua`; that changes the eta/sigma law.
2. **Insert the source side.**  Place every term of the exact 188-term
   `Theta_6` in the corresponding four corner grades.  Use its complete
   Hasse incidence tower, not a truncation at pairs.
3. **Use strict interchange.**  This coefficient-ring identity is now
   proved (`10ab27f`): all 8,580 eligible order-six operators are disjoint
   from every ridge coordinate, so `[Theta_6,-dOmega_v]=0`.  No additional
   mixed correction is required; only its physical labelled realization
   remains.
4. **Check augmented rows.**  The ordinary source/residue rows are fixed by
   `Theta_6`; eta/sigma are fixed by `-dOmega_v`.  The endpoint-odd Cartan
   identity `K=(1-s)H_w` now proves that `D`, `W`, target, anchor, and the
   pure-Eq aggregate vanish for every intermediate tail form.  They are no
   longer independent checks.  The remaining assertion is that `H_w`
   descends through the complete physical labelled source resolution and
   that its residue face is the pinned order-six tower.
5. **Use the primitive face.**  If `07:11 wedge 24:11` survives with its
   internal endpoint target-full and its colour quotient-visible, it gives
   the one-sided `(2,3)->(3,3)` rank landing.  If every such face is dark,
   use the complete-row dependence/terminal alternative.

## Evidence for and against

Evidence for the theorem:

- the source commutator is literal on both complete rows;
- the order-five generator defect is exactly repaired;
- the order-six source cycle and all its unsigned Hasse faces are exact;
- the terminal packet is one canonical Kähler class;
- the Hasse tower and Kähler class commute on the entire eligible block;
- the same primitive face has the needed overlap topology.
- endpoint oddness kills every protected augmentation without requiring the
  local Weyl action itself to stabilize the GHZ target.

The remaining guards are real:

- ordinary fine-grade homogenization changes the terminal law;
- `pq-pr` chart copies cancel every physical terminal as well as every
  private boundary;
- formal derived principal-parts cells do not automatically descend to the
  physical repeated-site module; and
- endpoint-rank repair still requires compatible site/colour labels.

## How this closes the global proof

Once `M_v` exists, the conditional five-lock theorem closes the E14 and
unequal-tail holonomy and lowers the unresolved-component potential.  Its
primitive arm supplies the first one-sided rank repair.  The remaining
Theorem-A work is then the already isolated Hall/rank landing and global
termination theorem.

The same `M_v` is the missing physical comparison for Theorems B and C.
After it defines the five columns `P(e_v)`, the Fredholm alternative gives
either the normalized relative generator or the annihilator.  Component C
then needs only the horizontal rootless/inactive compatibility and the
separate diagonal inactive routing.

So the present comparison is the shared end-game construction, while the
post-comparison Hall/termination theorem is the remaining specifically
combinatorial piece.
