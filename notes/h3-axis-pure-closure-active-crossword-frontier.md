# The h=3 axis-pure escape is closed; only the active-coloop comparison survives

## Corrected conclusion

The global minimum-support census `22c2e5c` and the coefficient certificate
`b0e1551` completely close the axis-pure support escape left open by
`80732b0` and repeated in `d7765f6`.

The unrestricted `F0`-normalized Boolean formula has exactly six models.
Every model has support `27` and type

```text
F0 + bright K2,2 + bright K2,4.
```

Blocking the six cell supports makes the formula UNSAT.  Each of the six
fails the actual coefficient equations.  Since every finite exact source
has an inclusion-minimal occupied subsupport, there is no larger hidden
minimum-support stratum.  Therefore

\[
               \boxed{\text{the canonical h=3 axis-pure branch is empty}.}
\]

Checker:

```text
computations/verify_h3_axis_pure_closure_active_crossword_frontier.py
```

Frozen ledger SHA-256:

```text
23f56cd2640635a9bf063aa2d9e74cb5ff5b0ea934de1f72803323d32354fd90
```

## What is superseded

Delete these frontier items in the `h=3` packet:

- the “larger axis-purified multi-term cancellation packet” of `80732b0`;
- the parallel “axis-pure support escape” in `d7765f6`; and
- arbitrary pure-colour-coloop normalization as a possible landing for that
  axis-pure branch.

The earlier support-`17`, support-`27`, and inverse-rectangle results remain
valid intermediate structure, but they are no longer live endpoints.

## The surviving active branch

After axis-pure removal, the old full-row alternative becomes

```text
offdiagonal enlargement -> target-augmented private-site active fan.
```

Complete pure target supports then give the exact split:

1. If both fan edges are avoided by a matching in every pure colour, the
   deleted stars have full rank and the fan is four-good.  This branch uses
   the existing landing and needs no new cross-word attachment.
2. Otherwise a fan edge is a literal coloop of some pure-colour support.
   After finite Hall saturation, the only unproved active statement is the
   fan-grade physical comparison

   \[
                   J_0\Phi=A J,
   \]

   with literal `q=M-a` rows on both packets.  Once `Phi` exists, packet
   disagreement, the anchor fork, termination, and the normalized h=3
   coloop closures are already exhaustive.

Thus the only active outcome still needing a comparison is

```text
literal pure-colour coloop trapped in a closed Hall shore.
```

## Relation to the master cross-word attachment

The centered response/cap attachment remains open.  Its required faces are

```text
90df-dR,
selected six-term db01,
Phi_orb((H0-u)eEq)=R_E14,
the cross-word cap and rooted B1+B4 face,
full anchor/q/W/ridge/eta/sigma readouts.
```

A complete multiplicative attachment is a natural candidate to supply the
fan-grade `Phi`.  However, no pinned theorem yet proves that its restriction
to every trapped fan-coloop packet is exactly Gate II's protected comparison.
That factorization must remain explicit.  Excluding axis-pure supports does
not construct it, because it belongs to the unpurified centered/cap grade.

The corrected shortest map is therefore

```text
canonical h3 full-row packet
  +-- axis-pure -> impossible
  `-- offdiagonal -> active fan
        +-- four-good -> landed
        `-- literal coloop -> trapped Hall shore
              `-- OPEN fan-grade Phi/q comparison
                    -> existing q-defect/circuit/normalized-coloop closures.
```

## Scope

This is an exact correction for the canonical `h=3` axis-purified
five-tensor equations over characteristic zero and for an already-entered
`h=3` active fan.  It does not prove an all-order axis theorem, global entry
into the bright/centered packet, or the missing cross-word comparison.
