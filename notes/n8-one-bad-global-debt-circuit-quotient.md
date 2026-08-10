# The K6 global-debt quotient has forty-five sign-even circuits

## Verdict

For the six-site residual of the reduced `N=8` one-bad packet, augment a
mixed-word debt label by the endpoint-incidence vector of its matching
monomial.  This finite quotient has no strictly positive linear functional
on all primitive exchanges.  Its first exact Farkas counterguards are
fifteen four-move squarefree and thirty six-move multiplicity-two,
sign-even balanced circulations.

The complete minimal integer-circuit census of the `15x15`
edge-versus-perfect-matching incidence matrix is

| matching terms | signs | circuits | consequence |
|---:|---:|---:|---|
| 6 | `3+ / 3-` | 10 | odd three-binomial holonomy, hence a unit |
| 8 | `4+ / 4-` | 15 | even four-binomial holonomy, no sign unit |
| 11 | primitive `6+ / 6-` | 30 | even six-move balance; one column has multiplicity two |

The matrix has rank ten and these 55 are all its minimal circuits.  The
first 25 are precisely the **unit-coefficient** circuits; omitting the thirty
support-eleven circuits would make the theorem false.  In every eight-term
circuit, orient four moves from the negative side to the positive side.  All
terms have the same row-word label, so the label changes sum to zero; the
four endpoint-exponent differences also sum to zero.  Their coefficients
are positive and their sign product is `(-1)^4=1`.  This is the smallest
nonnegative balanced combination.

Each support-eleven circuit has one primitive coefficient of absolute value
two and ten of absolute value one.  Expanding multiplicity gives six moves
on either side.  These exponent differences also telescope with even sign.
They form a second family of Farkas counterguards rather than odd units.

The exact checker is
`computations/verify_n8_one_bad_global_debt_circuit_quotient.py`.

## Octahedral classification of the even circuits

Each even circuit is indexed by a perfect matching `F` of `K6`.  Its eight
terms are exactly all perfect matchings avoiding `F`; their physical support
is the octahedral graph `K6-F`.  Conversely every one of the fifteen perfect
matchings gives one circuit.  Thus the even circuits form one abstract
`S6` orbit.

This does **not** mean that all fifteen embeddings are equivalent after the
one-bad response stars have been fixed.  In the canonical first sharp chart,
the distinguished matching is

\[
                         F_0=01\mid24\mid35,             \tag{1}
\]

where `01` is the left pair and `24,35` are the two diagonal response-hole
pairs.  Relative to `F0`, the fifteen omitted matchings split as

```text
F=F0:                 1
F shares one edge:    6
F is disjoint:        8
```

So the abstract single orbit becomes three relative strata `1+6+8`.

## The aligned circuit is exactly the two-zero-fan rectangle

For `F=F0`, the eight circuit terms partition into four pairs according to
the cross edge

\[
                         23,\quad25,\quad34,\quad45.     \tag{2}
\]

For each cross edge `rs`, the other four vertices are matched in the two
possible ways.  These are exactly the two summands of

\[
                    T_{rs}=u_r\otimes v_s+u_s\otimes v_r. \tag{3}

The two terms have opposite incidence-circuit signs.  The four tensors in
(3) form a `K2,2` rectangle; its four adjacent pairs are the four shared
two-zero fans.  The pinned exact theorem proves that, together with

\[
                         T_{24}=E_{bb},\qquad T_{35}=E_{cc}, \tag{4}

each shared zero fan generates the unit ideal over `Q`.  Hence the single
aligned even circuit is coefficient-impossible despite its sign-even
incidence balance.

## The multiplicity-two orbit

The thirty support-eleven circuits form one further abstract `S6` orbit.
Every circuit has a unique doubled matching, and each of the fifteen K6
perfect matchings is doubled in exactly two circuits.  Relative to `F0`, the
doubled matching splits as

```text
doubled matching = F0:              2
doubled matching shares one edge:  12
doubled matching is disjoint:      16
```

Even the two aligned doubled circuits are not instances of the existing
squarefree shared-zero-fan theorem: their six-move relation uses one matching
twice.  A translated-target or repeated-provenance identity would be needed
to turn them into a coefficient unit.  The checker records this as a scope
guard rather than guessing such an identity.

## The exact remaining guard

The other fourteen circuits do not have omitted matching `F0`.  Six share
one edge with it and eight are disjoint.  The existing fan theorem does not
identify their four circuit pairs with the two fixed diagonal target tensors
in (4).  Killing them requires a transport between different top/response
words or another common-provenance identity.

Therefore the finite theorem is deliberately two-sided:

- the positive-functional route on label plus endpoint incidence is retired
  by fifteen squarefree and thirty multiplicity-two even circuits;
- the coefficient equations close the unique aligned relative class; and
- `6+8=14` unaligned squarefree classes, together with the multiplicity-two
  orbit, are the precise cross-word/translated-target coupling gap.

This is not a support-depth enumeration and not a Krenn counterexample.  It
is the complete circuit classification of the K6 matching-incidence quotient
and an exact identification of what the current rectangle theorem does and
does not cover.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_global_debt_circuit_quotient.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_global_debt_circuit_quotient.py
```

Both modes freeze the ledger hash printed by the checker.
