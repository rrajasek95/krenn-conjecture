# Zero holonomy has only two interference amplitudes

## Result

Let `M` be a minimal square critical block of matching classes in a mixed
source component.  On the zero-holonomy branch,

\[
                  \operatorname {rank}M=n-1.
\]

Write `c` and `ell` for full-support right and left kernel generators.  The
adjugate has rank one:

\[
                  \operatorname {adj}(M)=\kappa c\ell^T,
                  \qquad \kappa\ne0.                    \tag{1}
\]

Adjoin a pure/target reduction row `h^T` and a physically typed Cartan
connector `g`.  On the zero-Fitting locus, the complete Schur determinant is

\[
 \boxed{
 \det\begin{pmatrix}M&g\\h^T&\alpha\end{pmatrix}
       =-\kappa(h^Tc)(\ell^Tg).
 }                                                        \tag{2}
\]

Thus an even critical SCC is controlled by exactly two amplitudes:

1. the **anchor amplitude** `h^T c`; and
2. the **Cartan amplitude** `ell^T g`.

There is no further `C4/C6/C8` topology in the determinant.  The checker is
[`verify_oo_zero_holonomy_schur_interference_reduction.py`](../computations/verify_oo_zero_holonomy_schur_interference_reduction.py).

## Why this advances the global proof

The earlier pure-anchor block had `g=0`, so (2) vanished identically.  The
physical endpoint-odd Cartan theorem now constructs precisely the missing
kind of grade-changing connector in the canonical selected packet.  Formula
(2) identifies what must be checked when that connector is inserted into an
arbitrary higher critical SCC.

If `M` is a minimal circuit, both kernel vectors have full support.  Hence a
literal coordinate row selecting the marked matching class has
`h^T c != 0`, and a literal coordinate Cartan attachment has `ell^T g != 0`.
Every such even component then acquires a nonzero maximal minor, giving the
localized source unit.  The checker verifies this for compatible weighted
cycles of lengths four, six, and eight, with arbitrary nonconstant rational
transition weights.

This explains the recent selected-two-cycle theorem.  Its long decoration
census established that the marked off-diagonal class really does enter a
literal Cartan/fan coordinate.  Once that source typing is present, the
two-cycle cannot be a terminal even interference pattern.  Equation (2)
shows that the same conclusion is independent of the length of the critical
cycle.

## The zero-amplitude branch is exact transport, not another terminal

Because the left cokernel of `M` is spanned by `ell`,

\[
                         \ell^Tg=0
             \quad\Longleftrightarrow\quad
                         g\in\operatorname {im}M.       \tag{3}
\]

Thus a dark Cartan amplitude is not unexplained cancellation.  There is a
potential `y` with `My=g`.  Column operations absorb the connector into the
old mixed component.  The component remains rank deficient, but the physical
comparison has become an explicit internal transport potential.

Consequently the remaining higher-SCC theorem can be stated sharply:

> In the minimal critical component containing the selected off-diagonal
> class, the physical pure/Cartan comparison either has both nonzero charge
> pairings, or its component potential lifts to a complete-column dependence
> touching occupied support, or to a literal exchange leaving that component.

The first branch is the Fitting unit by (2).  The dependence branch performs
the proved anchor-safe support deletion.  The escaping exchange enlarges the
typed component and restarts the same test.  No classification of longer
even cycles is needed.

## Relation to interference

Odd holonomy makes the mixed block itself invertible.  Zero holonomy leaves
one coherent mode `c`.  The pure anchor measures that mode from the right,
while physical Cartan measures it from the left.  Their product is the Schur
minor (2).  In physical language:

```text
odd phase around the component       -> direct unit
coherent even phase + two visible amplitudes -> Schur unit
one invisible amplitude              -> exact internal transport potential
```

This is the structural interference pattern behind the finite cases.

## Scope

The rank-one adjugate and image criterion are unconditional linear algebra
over characteristic zero.  The weighted cycle audits verify all signs and
normalizations.  What is not yet proved is that the complete physical
Cartan/pure comparison lands as a coordinate connector in every higher
source component, or that every component-exact potential gives the required
support deletion/escape.  That source-typing statement, rather than even
cycle topology, is now the remaining global gate.

Run:

```text
python3 computations/verify_oo_zero_holonomy_schur_interference_reduction.py
python3 -O computations/verify_oo_zero_holonomy_schur_interference_reduction.py
python3 -I -S computations/verify_oo_zero_holonomy_schur_interference_reduction.py
```

Frozen ledger SHA-256:

```text
26166fd7252b7cb6a000a62ef2fc40d0b38697ad53b9aa84dd22233d0fe482b1
```
