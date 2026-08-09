# P5 all-order newest-bend coefficient

The monic newest-bend part of the P5 Ward/Nakayama recurrence is now an
all-order formal statement, not only an r4 observation.  The remaining gap is
the principal syzygy which makes every other mixed row follow M30.

## Formal shift lemma

After the exact 207-row Schur block, write the selected normal/transverse
equations as

```text
E(tau,z46,u)=0,
```

where `u` consists of the 196 ambient-normal and eleven transverse graph
variables.  Their Jacobian is the identity block together with `b*I_11`, so
it is invertible on the `b != 0` chart.  Along the formal graph `u_*`, put

```text
A(tau) = dE/du (tau,z46,u_*),
B(tau) = dE/dz46 (tau,z46,u_*).
```

Perturb a future coefficient by `delta z46 = eta*tau^k`, with `eta^2=0`.
The linearized graph equation is

```text
A(tau) delta u = -B(tau) eta*tau^k.
```

Since `A(tau)` is invertible, uniqueness gives

```text
delta u = eta*tau^k V(tau),
V = -A^(-1)B,
```

and `V` is independent of `k`.  Every compatibility variation therefore has
the form `eta*tau^k C(tau)` with the same series `C` at every filtered order.
This is simply coefficient translation in a formal implicit system; it does
not assume the desired principal recurrence.

## Exact source audit

The checker constructs the source-faithful Jacobi response using an r4 marker
and audits the hypotheses directly:

- all 196 normal strict rows and all 39 obstruction strict rows have z46
  degree at most one; the eleven transverse rows have degree zero;
- the relative Jacobi response at orders 0,1,2,3 has respectively
  `(variables,terms,max) = (1,1,1),(11,16,3),(11,23,5),(22,41,7)`;
- every linearized normal/transverse residual vanishes;
- no compatibility row responds at relative orders 0,1,2;
- at relative order three only M30 and M33 respond, with

```text
C30[3] = 1/2*z11*z16^2*z41*(z26+b-z44),
C33[3] = 1/2*z11*z16^2*z41*(z26-z44).
```

The M30 coefficient is a unit on the committed chart.  For a genuine future
bend `r_k`, `k>=4`, nonlinear powers cannot contaminate order `k+3`, because
`2k>k+3`.  Hence every newest bend enters M30 at its first compatibility
order with exactly the same localized unit.  The r4 checker is the first
non-dual realization of this general coefficient lemma.

## What remains

This closes the Weierstrass/monicity half of the proposed all-order
connection.  It does **not** prove that the full mixed ideal stays principal.
The exact remaining datum is a uniform source-level, Bianchi, or post-Schur
syzygy which makes the corrected M33 row—and then the other 26 compatibility
rows—follow M30.  Once that is supplied, the exact Ward transgression gives
the corresponding pure membership/constancy statement.

The exact checker is
`computations/verify_n8_p5_newest_bend_uniform_coefficient.py`.
Its frozen ledger has SHA-256
`7419aaf1492fa46d6a2af344333ce34e163c30bbf3824999808245ab47af6cf2`.
