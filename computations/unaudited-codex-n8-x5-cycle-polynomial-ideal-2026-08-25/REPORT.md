# The six cycle residuals generate the unit ideal

Status: **the arbitrary 24-cell colour-saturated cycle family has no
zero-residual member.**  More generally, after allowing arbitrary entries in
all four cycle blocks, pure normalization makes every one of the six residual
amplitudes a unit.  This is an exact source-labelled polynomial identity, not
a sampled or modular inference.

## Four-term factorization

Retain the physical blocks

```text
A03=A16=A27=A45=I3
```

and write the four arbitrary cycle blocks as

```text
X=A04,  Y=A35,  U=A12,  V=A67.
```

For the base-sector word

```text
w(a,b,c,d)=(a,b,c,a,d,d,b,c),
```

exactly four perfect matchings are supported:

```text
03|12|45|67,  03|16|27|45,
04|12|35|67,  04|16|27|35.
```

Their source-labelled sum factors for every `a,b,c,d`:

```text
Phi(w) = 1 + Xad Yad + Ubc Vbc + Xad Yad Ubc Vbc
       = (1 + Xad Yad)(1 + Ubc Vbc).                 (1)
```

The audit constructs both sides as sparse integral polynomials and verifies
all 81 colour choices.  Thus (1) holds over every commutative coefficient
ring.

## Pure rows force all six residuals to be units

Put

```text
P_t=1+Xtt Ytt,   Q_t=1+Utt Vtt.
```

The three pure-normalization hypotheses are exactly

```text
P_0 Q_0=P_1 Q_1=P_2 Q_2=1.                          (2)
```

For ordered colours `a!=b`, the residual word
`(a,b,b,a,a,a,b,b)` has amplitude

```text
R_ab=P_a Q_b=(1+Xaa Yaa)(1+Ubb Vbb).                (3)
```

In the quotient by (2), its explicit inverse is `Q_a P_b`.  The exact
two-generator certificate is

```text
R_ab(Q_a P_b)-1
 = (P_a Q_a-1)(P_b Q_b)+(P_b Q_b-1).                (4)
```

The six instances of (4) were replayed as literal integral-polynomial
equalities.  Consequently each `R_ab` is a unit modulo the pure ideal.  In
particular the six residuals cannot have a common zero over any nonzero
unital commutative ring; no active-clean-cap alternative is needed inside
this support family.

## The requested arbitrary 24-cell family

The fully colour-saturated guard family lets all 24 ordered off-diagonal
entries of `X,Y,U,V` vary independently and fixes

```text
Xtt=Ytt=Utt=0,  Vtt=1.
```

Therefore `P_t=Q_t=1`: all pure amplitudes are one and each of the six
polynomials (3) specializes identically to the constant one.  The result is
independent of the 24 coefficients, including zeros and non-unit values.
The triangle-response guard is structural here: among the supported blocks,
the only possible response pair for sites `(6,7)` is `{1,2}`, which lies
inside the distinguished triangle.

As independent guards, the literal source evaluator replayed 257 exact
rational assignments of all 24 off-diagonal variables, and 257 exact rational
extensions with arbitrary diagonal data solved subject to (2).  The latter
checked all 81 amplitudes per sample and every inverse identity.

## Scope

This closes the arbitrary-coefficient version of the complete 24-cell
saturated cycle and the larger four-cycle-block family subject to pure
normalization.  It does **not** classify source cells outside `A04,A35,A12,A67`
or prove that every point of the full formal X5 guard reduces to this family.
Accordingly it is a nontrivial symbolic closure of the current boundary case,
not a full-conjecture proof.

Parent manifest:
`a8de425bbe54221874b4c75cb45b8dd4a465f628c881536d2e4d785a9afe4ab1`.
