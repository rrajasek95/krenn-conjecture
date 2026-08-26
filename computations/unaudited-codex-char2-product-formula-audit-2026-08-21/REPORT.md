# Characteristic two, product formula, and tropical-cover audit

Status: **the degree-nine lift globalizes exactly to arithmetic instability,
not to a product-formula contradiction; generator-level tropical casework is
also insufficient**.

## 1. The exact global algebraic consequence

Let

```text
B = Z[z]/(F_mixed, F_000000-1, F_111111-1, F_222222-1)
```

be the normalized six-site ternary fibre ring.  The audited integral identity

```text
P-C=2R
```

has `P=1` and `C=0` in `B`, hence

```text
1=2R in B.                                                (1)
```

This is the precise globalization of the characteristic-two certificate:
`2` is a unit in `B`, with inverse `R`.  Thus every component of `Spec B`
lies over `Spec Z[1/2]`, and the characteristic-two special fibre is empty.
At any number-field point, equation (1) says

```text
R(A)=1/2,       N_K/Q(R)=2^{-[K:Q]}.
```

That fixed norm is compatible with the product formula.  Its negative orders
above two are compensated at the remaining finite/archimedean places.  The
minimal model `Spec Z[1/2]` already exhibits exactly this phenomenon.  A
variety being forced away from the prime two is not a contradiction to its
having characteristic-zero points.

The identity fixes the balanced **sum** `R`, not an individual monomial
`z^Gamma`.  Even the equation `x+y=1/2` allows both summands to have
arbitrarily negative order:

```text
x=2^{-N},       y=1/2-2^{-N},       v_2(x)=v_2(y)=-N
```

for every `N>=2`.  Therefore (1) supplies neither a lower bound on witness
valuations nor a height bound on source coordinates.

Nor does multiplying a finite witness list help.  Knowing one factor has
negative order at a place gives no sign for the product: other witness
monomials may have arbitrary positive orders there.  Since the selected
`Gamma` may vary with the place, no fixed product inherits the local
minimum-witness inequality.

## 2. Exact source-faithful product-formula countermodel

There is a uniform exact binary GHZ family in the same six-site, three-colour
source coordinate space.  The third target summand is absent, so this is
**not** a ternary Krenn counterexample; it tests the proposed arithmetic
inference itself.

For `N>=1`, let

```text
K_N=Q(sqrt(4^N-1)),
a=2^{-N},
b=sqrt(4^N-1)*2^{-N},
a^2+b^2=1.
```

Use colour zero on

```text
01=a, 23=a, 02=b, 13=b, 45=1,
```

and colour one on the perfect matching `12,34,05`, all with coefficient one.
Exact enumeration of all 729 word amplitudes gives only

```text
F_000000=1,       F_111111=1.
```

The balanced source monomial supported once on the switched `C4` and twice
on the tail is

```text
(ab)^2=(4^N-1)/2^{4N},       v_2((ab)^2)=-4N.             (2)
```

Its port degree is two at every colour-zero site and zero at every other
port.  Thus normalized exact matching equations, torus polystability, the
global product formula, and an arbitrarily negative balanced monomial are
mutually compatible.  The checker replays `N=1,...,6`, reaching orders
`-4,...,-24`.  Any contradiction using only those properties is false.

The ternary degree-nine identity adds the stronger fixed equation (1), but
that equation itself is also product-formula compatible.  A successful
ternary arithmetic proof therefore needs new information forcing an
individual witness to be an algebraic-integer unit or giving an independent
global height bound; neither follows from the coefficient identity.

## 3. Why source-cycle invariants do not supply the unit

At six sites the one-hot source-cycle invariants also have degree nine and
the same balanced multidegree.  But

```text
I_M=H_m Q_M
```

contains a mixed target coefficient.  Hence every `I_M` is zero on an exact
ternary GHZ fibre.  It equals one on the known Laurent boundary orbit and is
excellent for separating border from exact source quotients, but it cannot
turn a residual `Gamma` monomial into a nonzero unit on the exact fibre.

## 4. Tropical initial-ideal cover

The dependence of the witness on `Gamma` is not an infinitude obstruction.
The residual has finite Newton support—395,542 nonzero row orbits—and a
finite normal-fan refinement can select minimum witnesses in principle.

However the 729 original coefficient generators are not a tropical basis.
The exact two-edge-star valuation assigns weight `-1` to every coloured cell
on physical edges `01` and `02`, and zero elsewhere.  Every coefficient
fibre has exactly six minimum matchings.  At the all-ones residue point its
initial value is

```text
6=0 in F_2,
```

so all 729 generator initial forms vanish simultaneously in the source
torus.

The saved integral residual nevertheless has row 1589 with coefficient
`-1`, balanced incidence one at all eighteen stubs, and valuation `-3`:

```text
02_02 02_11 01_22 12_00 15_11 35_02 34_12 34_21 45_00.
```

Thus this cone already contains the mandatory negative `Gamma` and a common
zero of every generator initial form.  No finite cover using only those
initial forms and the selected witness can close the problem.  The known
failure occurs at the next 2-adic digit (the rank-45/46 four-row first-jet
obstruction), not at order zero.

A finite higher-jet/valued initial-ideal cover remains possible in principle,
but it is genuinely new machinery: it must retain multi-term leading fibres
and subsequent 2-adic digits rather than repeat the minimum-monomial Farkas
argument.

## Terminal verdict

1. **Product formula/height:** terminally negative without a new integrality
   or global height theorem.
2. **Finite generator-level tropical cover:** terminally negative; the exact
   star cone is a common torus-zero countercone.
3. **Higher 2-adic initial ideals:** still logically open, but this is a
   filtered multi-jet computation, not a globalization of the degree-nine
   monomial witness.

## Replay

```sh
python3 computations/unaudited-codex-char2-product-formula-audit-2026-08-21/audit_char2_product_formula.py --write-results
python3 -O computations/unaudited-codex-char2-product-formula-audit-2026-08-21/audit_char2_product_formula.py
python3 -I -S computations/unaudited-codex-char2-product-formula-audit-2026-08-21/audit_char2_product_formula.py
```

All modes return logical SHA-256
`d29defb42e72ecb70a8e44704f40d8a230110cc2de977553d66f96230e55b1b6`.
