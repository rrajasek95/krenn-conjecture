# P5 generic-L Ward connection through the next bend

The exceptional M30/M33 derivatives in the four-centre Ward counterguard are
exactly removed by one next filtered bend.  This is the first successful
finite connection step supporting an all-order principal-recurrence theorem.

## The next monic coordinate

Retain

```text
z46(tau) = z46 + tau*s + tau^2*t + tau^3*r3 + tau^4*r4.
```

In the exact 207-row source graph, the order-seven M30 compatibility has

```text
d M30^(7) / d r4
  = 1/2*z11*z16^2*z41*(z26+b-z44).
```

Every factor is a unit on the selected dense chart: `z11,z16,z41,b` were
already inverted and `z26+b-z44=z26+z45` is the committed M30 localizer.
Thus the M30 equation supplies a unique next-bend connection coefficient.

Start with the exact Ward field corrected to preserve `L,F1,F2,G`, and set

```text
theta(r4) = -theta(M30^(7)) /
             (d M30^(7)/d r4).
```

The checker represents the inverse by the existing exact localizer variables;
no numerical division, modular reconstruction, or capped inference is used.

## Exact verdict

In the dual-number saturated quotient

```text
m_i = Q_i^(6) + epsilon*Q_i^(7) mod epsilon^2,
```

characteristic-zero reduction proves:

- `theta(M30)=0` after the r4 correction;
- `theta(M33)=0` with no second correction;
- all 26 nonzero mixed derivative rows reduce to zero;
- all four centre derivatives `L,F1,F2,G` reduce to zero;
- all available pure derivatives reduce to zero: H0 windows
  `(4,5),(5,6),(6,7)` and H1 windows `(5,6),(6,7)`.

The 83- and 61-term survivors from the uncorrected field are therefore one
missing monic-bend effect, not independent obstructions.

## Emerging induction and remaining proof gap

The exact pattern now has the form expected of a filtered connection:

1. M30 is principal and monic in the newest `z46` bend;
2. choose that bend uniquely to make the Ward field tangent to M30;
3. principalization forces M33 and every other mixed row to follow;
4. the pure Ward derivatives vanish in the same quotient.

To promote this to an all-order theorem one still must prove, uniformly in
the filtered order, that the newest-bend coefficient stays the same localized
unit and that the full mixed ideal remains M30-principal after the 207 Schur
graph.  The present result verifies one complete induction step modulo
`epsilon^2`; it is not itself a full-germ membership theorem.

The exact checker is
`computations/verify_n8_p5_generic_L_koszul_ward_r4.py`.
Its frozen ledger has SHA-256
`b9f736bd9a978547b4ffce15ac503bd5cc0b6425eb8756cb904abd95e424a4ca`.
