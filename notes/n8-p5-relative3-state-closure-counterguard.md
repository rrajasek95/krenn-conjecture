# P5 relative-order-three state closure counterguard

The full literal Schur-coordinate support visible at relative order three
does not carry a time-homogeneous state evolution.  The next exact response
leaves that 22-coordinate support in 26 new coordinate directions.

## Exact support calculation

Differentiate the exact 207-row localized Schur graph with respect to
`r4=z46^(4)`.  The numbers of nonzero literal coordinates at relative
orders zero through four are

```text
1, 11, 11, 22, 48.
```

The selected raw `2+1` cascade uses eight of the 22 relative-order-three
coordinates.  Its complement has fourteen coordinates: three already occur
at earlier order and eleven first occur at relative order three.  No member
of the 22-coordinate support disappears at the next order, but these 26
new coordinates appear:

```text
n12 n13 n18 n19
y56 y83 y86 y126 y127 y129 y130 y162
y198 y199 y200 y201 y202 y203 y207 y209 y210 y212 y214 y224 y225 y226
```

Thus the exact graph response cannot be represented by a fixed endomorphism
`A` of the proposed 22 literal coordinates: that coordinate subspace is not
invariant under the next coefficient shift.  Consequently a Krylov/Hankel
test on only this state set is not a valid all-order transfer certificate.

## Scope and next finite object

This does not rule out pole cancellation in a larger
reachable--observable quotient, nor does it contradict the checked `W4/W5`
output recurrence.  It says that expanding the state order by order has not
yet produced a finite invariant state space.  The bounded alternative is
the finite rational full-Rees substitution

```text
R(T)=N_{<=3}(T)/((1+z0*T)(1+z30*T)(1+z52*T)),
```

followed by clearing the fourth power of the denominator (the matching
source has degree at most four) and reducing the resulting finite
numerators by the 207 Schur rows and localized center equations.  A zero
numerator certificate would prove the transfer identity without assuming a
literal finite state closure; a nonzero numerator would be the next exact
obstruction.

The exact checker is
`computations/verify_n8_p5_relative3_state_closure_counterguard.py`.
Its frozen ledger SHA-256 is
`a1ad238cb8894402d4d8ed7e1673e4ef3226ab6b204d57e163031ba406cdf002`.
