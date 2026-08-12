# The order-six lift reduces the fiber problem to a terminal-only class

## Outcome

The earlier residual-q fiber criterion asked one relative cell to carry two
pieces simultaneously:

```text
ordinary residual:  -delta,
terminal packet:    eta_z=1+delta_(vz)u_z/t, sigma=-q_pq:22.
```

The order-six theorem now constructs the first piece with zero literal
pair-generator boundary.  Therefore, conditional only on typing that
explicit chain in the physical repeated grade, the remaining comparison is
a **terminal-only relative class**:

```text
source boundary = residue = D = W = target = anchor = 0,
eta_z = 1+delta_(vz)u_z/t,
sigma = -q_pq:22.
```

This is a genuine reduction.  The missing physical object no longer needs
to cancel 360 private matching terms or manufacture the four-corner residue.
It only needs to transport the known affine eta primitive and its sigma
correction through the shifted relative grade.

Checker:
`computations/verify_h3_residual_q_order6_terminal_only_fiber_reduction.py`.

## Why the reduction is exact

Let `theta_6` denote the 188-term order-six chain.  Its audited projections
are

\[
 d_{\rm src}\theta_6=0,
 \qquad \operatorname{res}(\theta_6)=-\delta.
\]

Let `gamma_v` have only the terminal entries displayed above.  In the
augmented row module,

\[
 ( -\delta,\eta,\sigma)
       =( -\delta,0,0)+(0,\eta,\sigma)
       =\theta_6+\gamma_v.
\]

Every protected row vanishes on the second summand.  Conversely, subtracting
the physically typed `theta_6` from any solution of the old fiber target
produces precisely `gamma_v`.  Hence the two image-membership formulations
are equivalent once the order-six direction is placed in the physical
complex.

There is no hidden adjustment inside the ordinary order-six block: none of
its 8,580 eligible coefficient monomials contains a colour-zero cell or a
marked `p/x` colour-two cell.  Its entire kernel is eta/sigma-dark.  The
terminal class must therefore come from the shifted comparison, not from a
different solution of the same ordinary linear system.

## Fastest remaining construction

The natural candidate is now a relative Cartan/Spencer transport of the
already known affine primitive `t-u_v`, with a single additional
`-q_pq:22` sigma face.  It should be built in three checks:

1. assign the terminal primitive to the same labelled repeated grade as
   `theta_6` using the common face `07:11 wedge 24:11`;
2. prove its physical source, residue, `W`, target, and anchor faces vanish;
3. verify the eta and sigma laws on the complete stabilizer kernel.

If such a class exists, adding it to `theta_6` supplies the full residual-q
comparison and activates the conditional endpoint-holonomy theorem.  If it
does not, non-membership is useful only after the complete physical relative
map is assembled: then the kernel/readout dichotomy produces either the
physical separator or the relative generator.

## Scope

This note does not claim the order-six differential operator is already a
physical repeated-grade cell, nor does it construct the terminal-only class.
It is an exact algebraic reduction of the remaining image target and a guide
to the next physical comparison.

Verification:

```text
python3 computations/verify_h3_residual_q_order6_terminal_only_fiber_reduction.py
python3 -O computations/verify_h3_residual_q_order6_terminal_only_fiber_reduction.py
python3 -I -S computations/verify_h3_residual_q_order6_terminal_only_fiber_reduction.py
```

Frozen ledger SHA-256:

```text
f804422d5924462820a3ac95c4813c19c3d0c90c51df4ee79be6d8e38b609ebc
```
