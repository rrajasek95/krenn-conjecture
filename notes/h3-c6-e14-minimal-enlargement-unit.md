# The minimal response-silent `E14` tail still has a two-row unit

## Exact theorem

Continue from the complete minimal core-port envelope of `7320475`.  Its
common `q` consists of the rational silent-`C6` `q00` fibre, one selected
pure-`11` tail, and one selected pure-`22` tail.  Allow every endpoint
component on the core sites `0,1,3,4`, and adjoin the complete minimal
decorated cell family used by the response-silent pair

```text
E14 = Q3+Q6,
Q3 = 02:02 | 14:11 | 35:11,
Q6 = 05:01 | 14:11 | 23:21.                          (1)
```

Give arbitrary formal coefficients to every cell in (1) not already fixed
by the chosen bright tail.  In each of all nine bright-tail charts, one
complete `G11` target row and one complete mixed zero row have **identical**
endpoint polynomials.  The row pairs are

```text
X1 tail 23|45:  111111 versus 111100,
X1 tail 24|35:  111111 versus 111010,
X1 tail 25|34:  111111 versus 110110.                 (2)
```

If their common polynomial is `P`, the physical source generators are

```text
F_target=P-1,       F_zero=P,
```

and therefore

\[
                         F_{zero}-F_{target}=1.        \tag{3}
\]

The checker is
`computations/verify_h3_c6_e14_minimal_enlargement_unit.py`.

## Why `q14:11` does not create hole `14`

For the first two `X1` tails, the new cell `q14:11` occurs in neither
polynomial in (2).  For the third tail it occurs in both, with exactly the
same additional terms:

\[
 q_{14}^{11}\bigl(p_{1,0}^{1}s_{1,3}^{1}
                  +p_{1,3}^{1}s_{1,0}^{1}\bigr).      \tag{4}
\]

Thus the internal spoke `q14:11` produces a parallel hole-`03` tail.  It
does **not** force either physical hole-`14` endpoint product

```text
p1_1:1*s1_4:1,      p1_4:1*s1_1:1.                   (5)
```

This is the exact answer to the first spoke-to-hole test: `E14` alone is
not a missing response attachment.  More strongly, it cannot occur as the
only enlargement of the minimal full response packet, because (3) is an
ordinary source unit independent of its coefficients.

## Forced next exit

A full source containing the canonical `E14` pair must therefore introduce
one of two genuinely new inputs.

1. An endpoint component on one of the outside sites `2,5`.  The pinned
   complete-column theorem applies: a zero complete column is exactly
   deletable, while a nonzero column has a literal cofactor and is a free
   active arm.
2. A second internal decorated `q` tail which enters the target and zero
   rows in (2) asymmetrically.  By the corrected contamination identity

   \[
   (a/b)F_z-F_t=1+(a/b)\Delta_z-\Delta_t,
   \]

   a source zero forces a nonzero literal monomial in that asymmetric
   difference.  This is a source-typed new edge, but it need not yet have
   deleted-star rank three.

The second alternative is the smallest remaining source-exhaustivity
guard.  It is strictly sharper than the response-silent `E14` guard of
`ebd1ba1`: the minimal pair itself is now excluded, and the next proof must
route a *second asymmetric tail*.  Rank completion remains separate.

## Scope

This is a coefficientwise polynomial identity on the exact rational fibre
of `7320475`, with all core `p1/s1` components and the full minimal `E14`
cell family.  It is not a support-only inference and does not specialize
the new `E14` parameters to a numerical cancellation.  It does not cover a
second asymmetric internal cell or assert that every such cell is already
off-anchor or four-good.

## Verification

```text
python3 computations/verify_h3_c6_e14_minimal_enlargement_unit.py
python3 -O computations/verify_h3_c6_e14_minimal_enlargement_unit.py
python3 -I -S computations/verify_h3_c6_e14_minimal_enlargement_unit.py
```

Frozen ledger SHA-256:

```text
a2d72f4ceadab5e0327c39f0f222c498fc8b54b3832eb7066d1caf796fd67f4a
```
