# The Hall-triangle lock forces an active decorated internal cell

## Result

In the non-dark opposite Hall-star branch, the complete crossed coefficient
has the form

\[
                    B_{ab}+A_{Rc}+A_{Pc}=0,
                    \qquad B_{ab}\ne0.                 \tag{1}
\]

Here `B_ab` is the pure-zero cofactor bridge, while `A_Rc,A_Pc` are the
corrections obtained by moving one endpoint star onto the selected anchor
edge through the centre `c`.

Equation (1) has an exact source-level consequence:

> At least one correction contains a nonzero literal matching term.  That
> term contains exactly one internal off-diagonal cell `q_ad^{10}` or
> `q_be^{20}`, multiplied by a nonzero pure-zero matching tail.

Thus the three-term lock cannot remain an abstract scalar cancellation.  It
produces a source-active decorated internal cell.

* If its physical pair lies outside the union of the three selected pure
  target matchings, the nonanchor theorem gives deleted-star ranks `(3,3)`
  and the target-augmented active-minor route.
* If it lies in the anchor union, the residual is exactly the decorated-
  anchor-edge web.  When an avoiding pure matching exists, the alternating-
  exit theorem lands unless every active transition is trapped on the at
  most two other-colour anchor neighbours.  Without an avoiding matching,
  that rank repair is the precise missing source input.

Checker:
`computations/verify_uniform_hall_triangle_three_term_anchor_lock_reduction.py`.

## Why every correction has one mixed cell

For `A_Rc`, delete the sites `b,c`.  The retained word is colour one at
`a` and colour zero everywhere else.  In every perfect matching, `a` must
be paired with one zero-coloured site `d`.  Hence every monomial is

\[
              q_{ad}^{10}\cdot
              (\text{a pure-zero perfect matching on the rest}). \tag{2}
\]

The statement for `A_Pc` is the colour-two dual.  Since the coefficient
domain is integral, `B!=0` in (1) implies that at least one of the two
correction aggregates is nonzero, and a nonzero finite sum has a nonzero
literal term.  This proves (2) without choosing support in advance.

The cofactor in (2) is already the activity witness.  Therefore no extra
genericity hypothesis is needed when applying the pinned nonanchor or
decorated-anchor theorem.

## The signed-holonomy shortcut is not available yet

The two diagonal target normalizations and the silent crossed `12` centre
collision do **not** turn (1) into an odd-character unit.  There is a
literal common-`q` six-site realization.  With residual sites
`c=0,a=1,b=2,3,4,5`, put

```text
pure 0: 04 | 12 | 35,
pure 1: 23, 45,
pure 2: 13, 45,
mixed : 14:10, 24:20.
```

Take

```text
p1(c,1)=s1(a,1)=p2(b,2)=s2(c,2)=1,
s1(c,0)=1,                 p2(c,0)=-2.
```

Literal expansion verifies all of the following simultaneously:

```text
q^[3] = X0                         (the complete unary tensor),
[p1 s1 q^[2]]_111111 = 1,
[p2 s2 q^[2]]_222222 = 1,
p1 s2 q^[2] = 0,
[p2 s1 q^[2]]_012000 = 1 + 1 - 2 = 0.
```

The three lock monomials share the nonzero tail `q35_00`.  This is a
rational point of the proposed unary/anchor/lock row packet, so neither an
ordinary unit nor a signed-character/odd-handcuff unit can follow from
those rows alone.

It is not a one-bad counterexample.  The checker records the remaining
nonzero response coefficients exactly:

```text
11: 111122, 112000,
22: 212000, 222211,
21: 011111, 011122, 022211, 022222.
```

Those off-target diagonal and crossed rows are the next load-bearing input.
Any cancellation mate they force must either expose a nonanchor decorated
cell, supply an avoiding anchor matching, or remain in the finite trapped
anchor web.

## Scope

This is a uniform source-provenance reduction of the three-term lock, not a
closure of the final decorated-anchor web.  It also gives a sharp negative
answer to the proposed signed-holonomy shortcut at the stated row level:
the other complete response grades cannot be omitted.

Run

```text
python3 computations/verify_uniform_hall_triangle_three_term_anchor_lock_reduction.py
python3 -O computations/verify_uniform_hall_triangle_three_term_anchor_lock_reduction.py
python3 -I -S computations/verify_uniform_hall_triangle_three_term_anchor_lock_reduction.py
```

Frozen ledger SHA-256:

```text
5fb50e5271c3425353760f8b78b25857354b1a04c7ae0c163cc51ea54e6c8819
```
