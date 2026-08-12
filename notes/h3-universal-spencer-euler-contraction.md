# Universal Spencer faces are contractible; only physical descent can obstruct

## The structural theorem

Let `R` be a characteristic-zero polynomial coefficient ring and write a
normally ordered differential operator using commuting symbols
`xi_1,...,xi_m` for its derivative directions.  The commutator identity

\[
              [D,x_i]=\frac{\partial\sigma(D)}{\partial\xi_i}
\]

identifies successive coefficient-prolonging faces with the polynomial de
Rham/Spencer complex

\[
        R[\xi]\otimes\bigwedge^\bullet\langle d\xi_1,\ldots,d\xi_m\rangle.
\]

Let `E=sum_i xi_i partial_(xi_i)` and let `i_E` denote contraction.  On a
homogeneous monomial `xi^alpha dxi_I`, Cartan's formula is

\[
 (d i_E+i_Ed)(\xi^\alpha d\xi_I)
       =(|\alpha|+|I|)\xi^\alpha d\xi_I.                 \tag{1}
\]

Consequently

\[
                 H={i_E\over |\alpha|+|I|}              \tag{2}
\]

contracts every positive-total-degree piece.  The universal Spencer tower
of the order-six residual operator therefore has no positive-degree
homology.  This is a proof, not a bounded rank heuristic.

The checker
`computations/verify_h3_universal_spencer_euler_contraction.py` exhaustively
verifies `d^2=i_E^2=0`, (1), and `dH+Hd=1` for five symbols, polynomial
degree at most six, and every exterior degree.  The formulas themselves are
independent of those bounds.

## Consequence for the order-six frontier

The 126 singleton faces and all higher coefficient faces should not be
eliminated independently.  They are coordinates of one contractible
universal Spencer object.  Likewise, asking one order-six representative to
have zero first and second faces is stronger than the proof needs: a
nonzero pair face has a coherent higher tower.

This explains three exact observations at once:

1. the complete Hasse tower satisfies the divided-incidence identities;
2. an affine representative can remove the first displayed face without
   changing the residual shadow; and
3. a simultaneous second-flat modular diagnostic fails even though the
   universal totalization remains contractible.

The third item is only diagnostic: the modular rank jump does not prove
characteristic-zero nonmembership.  It is also no longer the relevant
target.

## The exact remaining obstruction

Let `S_univ` be the universal Spencer/principal-parts complex and let
`C_phys` be the complete physical labelled source/correction complex.  A
comparison map must preserve

```text
physical fine word and repeated grade,
source boundary, D, W, target, ordinary residue, anchor,
eta and sigma terminal contractions.
```

The universal contraction proves that the missing class cannot originate
inside `S_univ`.  It can only be the obstruction to constructing the
comparison

\[
                         S_{\rm univ}\longrightarrow C_{\rm phys}. \tag{3}
\]

Equivalently, it is a class in the relative mapping cone of (3).  This gives
the proof-relevant alternative:

- if the physical terminal detects the relative class, normalize it to the
  required relative generator;
- if the terminal kills relative homology, the universal contraction
  descends, producing the augmented comparison `M_v`, after which the
  Fredholm alternative applies.

Thus the next theorem is **comparison/physical descent**, not another Hasse
or support census.

## A proof route for physical descent

Filter both complexes by repeated-site degree.  The desired comparison can
be built inductively if the following statement holds on the associated
graded:

> The kernel of the physical labelling map is stable under the two Spencer
> directions, and the induced terminal functional vanishes on its positive
> homology.

The first clause is source exhaustivity: every complete-row face must retain
its labelled companion.  The second is zero indeterminacy.  Algebraic
discrete Morse theory/homological perturbation is the natural construction:
use (2) as the universal contraction, perturb by the physical source rows,
and retain the induced differential on the small relative homology.  A
nonzero induced differential supplies `M_v`; a surviving terminal-visible
class supplies the alternative generator.

This is exactly where the source-labelled matching and terminal data enter.
They are not part of universal Spencer acyclicity and must not be discarded
by passing to an untyped quotient.

## Scope

This theorem removes higher Spencer-face enumeration from the proof
frontier.  It does not construct the physical comparison (3), prove the
kernel-stability/terminal condition, or perform the downstream transverse
rank landing.

Verification:

```text
python3 computations/verify_h3_universal_spencer_euler_contraction.py
python3 -O computations/verify_h3_universal_spencer_euler_contraction.py
python3 -I -S computations/verify_h3_universal_spencer_euler_contraction.py
```

Frozen ledger SHA-256:

```text
c8e88a844687b5f4855a9e160403cb73aa9ffd3398518de8ba60cd1126a74af7
```
