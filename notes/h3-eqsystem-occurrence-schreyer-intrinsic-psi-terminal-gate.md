# `Psi` does not descend to the actual occurrence-labelled EqSystem resolution

This is the requested alternative (B), not a physical Fredholm
contradiction.  Even after retaining every literal equation-word,
matching-monomial occurrence, divided-operator history, repeated-pair shape,
and word/fine shift in the original EqSystem resolution, the protected
functional

\[
\Psi=\delta\cdot(B-Eq),\qquad \delta=(1,1,-1,-1),
\]

is not defined.  The first missing datum is exactly the auxiliary choice of
two protected copies `B` and `Eq` of one intrinsic occurrence.  Higher
Taylor/Schreyer cells do not repair a missing degree-zero readout.

The executable certificate is
`computations/verify_h3_eqsystem_occurrence_schreyer_intrinsic_psi_terminal_gate.py`.

## 1. The source presentation used

The checker starts with the official polynomial presentation, not the
declared `Gamma_*` operation grammar:

```text
252 oriented colour-edge variables,
6561 equation words,
105 perfect-matching monomial occurrences in each equation.
```

At the Gamma word `01211222`, the 105 decorated matching monomials are
distinct occurrence generators and all have the same honest `N^24`
site-colour degree.  A four-generator Taylor packet, specialized on the
coefficient torus, has chain dimensions `(6,4,1)` and boundary ranks
`(3,3,1)`.  Thus its higher cells resolve lower kernels; they do not enlarge
the degree-zero occurrence/readout space.

The audit then retains the complete current order-six operator presentation:

```text
8580 literal columns,
159 coarsened site-repeating pair coordinates,
271 pair/word/fine occurrences before coarsening.
```

Consequently the no-descent result is not caused by discarding the known
operator or fine labels.

## 2. Exact no-descent theorem

Let `U=Q^4` be the four intrinsic protected occurrence coordinates.  The
enriched terminal presentation replaces it by

\[
\widetilde U=U_B\oplus U_{Eq}
\]

and forgets the copy label by

\[
\pi(b,e)=b+e.
\]

Every covector defined on the original occurrence module pulls back as

\[
\pi^*(\lambda)=(\lambda,\lambda).
\]

These tied pullbacks have rank four.  The desired detector is

\[
\Psi=(\delta,-\delta),
\]

and adjoining it raises the rank to five.  More explicitly,
`(delta,-delta)` lies in `ker(pi)`, while

\[
\Psi(\delta,-\delta)=8.
\]

Already on the first protected occurrence label, an intrinsic functional
would have to assign the same label both `+1` (when called `B`) and `-1`
(when called `Eq`).  Equation, monomial, operator, repeated, and fine labels
do not distinguish these two later presentation copies.  This is the first
exact undefined datum.

The argument is stable under adding ordinary Taylor/Schreyer resolution
cells: those cells change syzygies above the occurrence module, whereas the
failure is that `Psi` is absent from the dual of the degree-zero intrinsic
target.  No new decorated generator is added in the checker.

## 3. Consequence for the finite alternative

Once a literal matrix `J:C1->Y` and a right-hand side `b in Y` are defined,
finite-dimensional linear algebra gives the desired automatic alternative:

```text
b lies in im(J), giving a physical filler;
or some lambda in ker(J^T) has lambda(b) != 0, giving a separator.
```

Here that calculation cannot yet start with `Psi`: the original EqSystem has
no target map to the anti-diagonal `B-Eq` coordinate.  Coarsening to the
intrinsic sum `B+Eq` is well defined, but kills the detector.  Therefore the
current result is a missing-enrichment criterion, not a Macaulay/Fredholm
contradiction for physical solutions.

The weakest sufficient replacement does not require a response-to-cap source
generator.  It is a solution-level theorem defining a scalar
`Psi_actual` directly from literal EqSystem/Macaulay coefficients and proving

\[
\Psi_{actual}=0
\]

for every exact solution.  Since the required terminal right-hand side has
nonzero detector value, that intrinsic scalar identity would itself be the
left-kernel Fredholm certificate.  Alternatively, if the resulting explicit
right-hand side lies in the actual matrix image, its preimage is the physical
filler.

## 4. The derived-cap `N` does not evade the same datum

The marked collision species supplies a derived cap resolution `N` of the
same 90-parent module.  On an actual normalized solution `t=H0-u=0`, the
evident composite

```text
response -> N -> B
```

is genuinely a chain map.  It is monic on the selected parent carrier,
realizes the common-parent `B` augmentation, and can carry the top target via
the existing cone.  This statement does not use or require the comparison
cone to be acyclic.

It nevertheless does not realize the full protected `Phi_KS,r0`.  In the
first protected quotient the composite has boundary

\[
dN=(1,0).
\]

The physical `r0` boundary is `(0,1)`.  The two vectors have rank two, and the
first failed chain-map/readout equation is the absolute decorated Eq equation

\[
\Phi_0(c_f)=-E:
\]

the solution-wise composite has Eq projection zero while physical `r0` has Eq
projection one.  Thus the extra Eq class is not being invoked merely as an
objection to quasi-isomorphism; it is a literal missing protected value of the
constructive selected-carrier map.

Declaring the same parent augmentation to be both `B` and `Eq` changes this to

\[
dN_{tied}=(1,1).
\]

The correction is exactly

\[
(1,1)-(1,0)=(0,1)=e_{Eq}.
\]

Thus a tied augmentation on `N` is a legitimate possible theorem, but it
supplies the missing absolute decorated Eq preimage; it does not derive that
preimage from the common parent augmentation.  This agrees with the Tor
guard: after `H0-u=0`, a relative `dK=(H0-u)e_Eq` filler leaves homology
`(H0,H1)=(1,1)`, while an absolute `dK=e_Eq` filler gives `(0,0)`.

Conditional on granting the tied augmented map, the parent, target, marked
deletion, `0102/dq/Q`, and other linear readouts can in principle be
reformulated as natural transformations on `N`; none logically needs a
chosen underived representative merely as homological data.  The first later
pointed requirement is `P_f`/anchor and active-cap extraction.  In the exact
selected quotient,

```text
P_f                 = (1, 0, 0),
primitive cap p     = (0,-1,-1),
invisible q lift n  = (0, 1, 0).
```

The first two have rank two and all three have rank three.  Hence the common
`B` augmentation and derived primitive/q class do not determine `P_f`.  An
active cap is a pointed property of an actual degree-zero physical cap
representative, not of the common-parent homology class alone.  The terminal
branch can avoid this underived extraction only via the intrinsic
`Psi_actual` solution theorem above.

## 5. Non-flat normalization and the `Tor_1` loophole

A universal boundary census is not automatically exhaustive after the
specialization `t=H0-u=0`.  Once an Eq quotient has been chosen, the
labelwise relative normal form is

\[
R\{K_i\}\xrightarrow{\ t\ }R\{E_i\},\qquad R=\mathbb Q[t].
\]

Tensoring with `R/(t)` makes this differential zero.  For the four protected
labels it creates a four-dimensional `Tor_1` space generated by the `K_i`
and leaves a four-dimensional Eq `H0` generated by the `E_i`.  The exact
Bockstein/transgression is the identity matrix

\[
\tau([K_i])=[E_i],
\]

so it has rank four and sends `delta` to `delta`.  The relative cell becomes
an invisible cycle, not an Eq filler.  This is why `dK=tE` cannot substitute
for an absolute `dK=E` cell.

There is a second, distinct specialization loophole.  A universal column

\[
dL=E+tY
\]

does not make `E` a universal boundary, but it does make `E` a boundary after
`t=0`.  For an actual labelled matrix `J`, the two finite tests are

```text
universal boundary:          E in im(J),
post-specialization filler:  E in im(J)+t*C0
                             (equivalently E mod t in im(J mod t)).
```

Thus terminal promotion must check the `t`-saturated/specialized image, not
only the universal primitive list.  This does not rescue the current
intrinsic `Psi` construction: the original EqSystem still has no canonical Eq
quotient selecting the `E_i`, so neither the transgression nor the saturation
test can be attached to `B-Eq` without the same missing readout datum.  The
calculation characterizes exactly what must be run once that quotient is
defined.

## 6. Scope and reproduction

The theorem is an exact no-descent statement for the official EqSystem and
the full current order-six occurrence/operator labels.  It does not assert
that no intrinsic scalar observable can exist; it identifies the exact
additional datum required to define one.  It grants no operation idempotent,
no no-orphan axiom, and no physical response-to-cap generator.

```text
python3 computations/verify_h3_eqsystem_occurrence_schreyer_intrinsic_psi_terminal_gate.py --mode all
python3 computations/verify_h3_eqsystem_occurrence_schreyer_intrinsic_psi_terminal_gate.py --mode presentation
python3 computations/verify_h3_eqsystem_occurrence_schreyer_intrinsic_psi_terminal_gate.py --mode descent
python3 computations/verify_h3_eqsystem_occurrence_schreyer_intrinsic_psi_terminal_gate.py --mode derived
```

All modes have ledger digest
`9f36375ce004f03773a65b1f981cdf446f2e3b8f94d6af6b50eb5d1c43466307`.
