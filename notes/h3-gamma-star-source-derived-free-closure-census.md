# The source-derived `Gamma_*` closure has eight standard mixed cells and one precise primitive-Hom loophole

## Outcome

The `Gamma_*` census can now be made source-derived up to one explicit
presentation boundary.  The checker does not start from the seventeen prose
records of the old grammar.  It calls the existing physical constructors and
rebuilds their registry:

```text
actual constructor outputs                         128
literal Gamma_* entries                             25
rank in the 27 augmented Gamma_* rows               23
rank in the eight B/Eq rows                          7
nonzero Psi charges                                  0
operation-changing primitive atoms                   0
```

It then adds the canonical relative enlargement supplied by the actual
equations

\[
 F=H_0-u,\qquad Q=\operatorname{Eq},\qquad
 \theta=\epsilon_F\wedge\epsilon_Q,
 \quad d\theta=F\epsilon_Q-Q\epsilon_F.
\]

After relative base change along `Q=0`, `C_K=-theta` has
`dC_K=-F e_Eq`.  This is a genuine source-derived Tate cell, but it is
objectwise on the cap.  It does not create an operation-changing
`response -> cap` map.  The centered response deformation independently
constructs the response-side relative generator `epsilon_s`; it too is
objectwise.  Thus the free cellular/DGA closure of everything currently
constructed still has

\[
             \operatorname{Hom}^1_{\Gamma_*}
             (\mathrm{response},\mathrm{cap})=0.       \tag{1}
\]

Checker:
[`verify_h3_gamma_star_source_derived_free_closure_census.py`](../computations/verify_h3_gamma_star_source_derived_free_closure_census.py).

## Conditional exact eight-class theorem

Adjoin the single missing normalized degree-zero schema

\[
 \Phi_{KS,r_0}:\mathrm{response\ KS}\longrightarrow
               \mathrm{cap\ AugP2}/K_{Eq}.            \tag{2}
\]

The standard cellular closure then has only the following two binary
features at relative degree one:

```text
cross-word  K_Eq mixed     resulting cell
    0           0          local/canonical
    1           0          word-cylinder, Psi-dark
    0           1          objectwise K_Eq, Psi-dark
    1           1          standard kappa interchange
```

The lower parent `0112` has exactly eight one-root neighbours,

```text
0012  0102  0110  0111  0122  0212  1112  2112.
```

Their word idempotents are distinct, so the corresponding standard cells
have quotient rank eight.  Strict multiplicativity gives, separately at
each labelled object,

\[
 d(\epsilon_i\wedge\theta)
   =b_i\theta-\epsilon_iF,
 \qquad
 \Pi_{B/Eq}d(\epsilon_i\wedge\theta)=(v_i,v_i),        \tag{3}
\]

and hence

\[
 \Psi\bigl(d(\epsilon_i\wedge\theta)\bigr)
 =\frac14\delta\cdot(v_i-v_i)=0.                      \tag{4}
\]

Within this source-derived free closure, therefore,

\[
 C^1_{\Gamma_*}/(C^1_{\rm can}+C^1_{\Psi\text{-dark}})
       =\langle\kappa_{0012},\ldots,\kappa_{2112}\rangle, \tag{5}
\]

with no ninth class from the Koszul/Tate enlargement or from ordinary
higher syzygies.  Equation (5) is conditional on the physical construction
of (2) and on identifying the physical relative source with this standard
closure.

## Adversarial exotic search

The search distinguishes a hidden higher face from a genuinely new
operation primitive.  The canonical cone-shifted cell `C_K` is not exotic:
it has type `cap -> cap`, and its interchange with (2) is already one of the
eight cells in (3).  Composition with identities, objectwise PP/Hasse,
Cartan/Weyl, Macaulay, or cap maps cannot cross the disconnected operation
idempotents.  No executable constructor emits an off-diagonal atom.

The smallest still-unexcluded extension is instead an independently
primitive symbol

\[
 \omega_{0102}\in
 \operatorname{Hom}^1_{\Gamma_*}(\mathrm{response},\mathrm{cap}),
 \qquad
 \Pi_{B/Eq}(d\omega_{0102})=(\delta,0),                \tag{6}
\]

with zero canonical coefficient/PP shadow and zero target, `W`, residue,
`M`, anchor, `q`, ridge, eta, and sigma rows.  It has

\[
                    \chi(\omega_{0102})=4
\]

and raises the formal quotient rank `8 -> 9`.  This is a minimal
presentation counterguard, not an asserted GHZ source operation.  Its point
is that all existing callable constructors and the canonical Tate
enlargement are unchanged if (6) is adjoined.

Therefore the first missing presentation datum is exact:

> **Primitive off-diagonal Hom census.**  Construct the physical schema
> (2), and prove that every primitive total-degree-one element of
> `Hom^1_Gamma*(response,cap)` is, modulo canonical and `Psi`-dark cells,
> one of its eight standard `K_Eq` naturality interchanges.  Equivalently,
> prove that there is no independent atom of the form (6).

This is sharper than asking whether an unspecified higher source generator
might exist.  Ordinary higher syzygies cannot enlarge `im(d1)`, and the one
canonical relative Tate shift has been checked explicitly.  Only a new
off-diagonal primitive operation type remains.

## Scope

This is exact for the callable `h=3` constructor registry, the canonical
relative `F/Q` Koszul enlargement, and their free cellular/DGA closure.  It
does not construct (2), prove that the full decorated physical source has no
additional primitive operations, prove pure-target normalization or all
mixed output equations, or promote `Psi` to the final source-terminal
quotient.  The exotic control (6) is a presentation extension, not a finite
GHZ counterexample.

Run all modes:

```text
python3 computations/verify_h3_gamma_star_source_derived_free_closure_census.py
python3 computations/verify_h3_gamma_star_source_derived_free_closure_census.py --mode registry
python3 computations/verify_h3_gamma_star_source_derived_free_closure_census.py --mode closure
python3 computations/verify_h3_gamma_star_source_derived_free_closure_census.py --mode exotic
python3 -O computations/verify_h3_gamma_star_source_derived_free_closure_census.py
python3 -I -S computations/verify_h3_gamma_star_source_derived_free_closure_census.py
```

Frozen ledger SHA-256:

```text
d81dbee5add84bfc72633447b0ada4406b103e7f1f4b6f7dbeeac676ec15b2e4
```
