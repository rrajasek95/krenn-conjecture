# The selected `db01` and `dL01` packets conserve the literal private/Eq charge

## Exact verdict

Let the final augmented private/Eq coordinates be

```text
(B0,B1,B2,B3, Eq0,Eq1,Eq2,Eq3)
```

and set

\[
 \delta=(1,1,-1,-1),\qquad
 \chi(c)=\delta\cdot(B(c)-Eq(c)),\qquad
 \Psi=\chi/4.
\]

For both the selected six-term vertical `db01` face and the next eighteen
endpoint/direction terms of `dL01`, the strict literal answer is

```text
Pi_BEq = 0,       chi = 0,       Psi = 0.
```

This is a proved conservation step, not a chosen cancellation.  Checker:
[`verify_h3_db01_dl01_literal_private_eq_conservation_gate.py`](../computations/verify_h3_db01_dl01_literal_private_eq_conservation_gate.py).

## Why the literal projection is zero

The selected vertical face is the six-term source-labelled packet at

```text
deletion face v=1, residual sites 2,3,4,5,
response word 11:110000:

p0*dq23:00*q45:00*s1       p0*q23:00*dq45:00*s1
p0*dq24:00*q35:00*s1       p0*q24:00*dq35:00*s1
p0*dq25:00*q34:00*s1       p0*q25:00*dq34:00*s1.
```

It is squarefree, but it has vertical principal-parts degree one and its
fine colours and module role are response data.  The canonical `B/Eq` rows
instead live in the `AugP2` cap word

```text
01211222.
```

The words differ at six augmented sites, every one of the six selected cap
fine degrees changes, and the cap word is not in the existing response `D4`
cube.  Thus there are two distinct statements:

- projection from the typed direct sum onto the cap `B/Eq` summand is
  defined by zero-extension, and sends every response column to zero;
- a comparison which regards `db01` as a `B/Eq` column is undefined, because
  no source-labelled word/fine/repeated comparison arrow has been built.

The second statement is exactly the missing physical datum; it cannot be
replaced by forgetting the tags.

## The next eighteen terms

The endpoint/direction packet has primitive six-direction profile

\[
                  v_A=(2,2,-1,-1,-1,-1)
\]

tensored with the invariant three-tail sum, hence has eighteen terms.  It
lives in the same response-side fixed-window category, before the literal
response-to-cap placement.  Consequently all eighteen columns again have
zero strict `B/Eq` image.  If the old rank-seven cap matrix is denoted by
`M_cap`, exact rational row reduction gives

```text
rank(M_cap)                         = 7
rank(M_cap + six db01 zero images) = 7
rank(M_cap + db01 + 18 dL01 images)= 7.
```

There is an important codomain distinction.  The normalized fixed-window
response detector reads `2` on the eighteen-term packet.  The cap detector
`Psi` reads `0`.  These are two different typed covectors, so the former is
not a hidden nonzero `B-Eq` mismatch.

At coefficient level, the conditional endpoint-even `C_+` shadow is

\[
        v_A/4=(1/2,1/2,-1/4,-1/4,-1/4,-1/4).
\]

That identifies the unique response coefficient repair, but it remains
off-grade until its physical restriction/reinsertion and shifted `P2`
placement are constructed.

## Minimal comparison datum and terminal fork

The smallest datum that can decide the comparison is one occurrence-local,
source-labelled response-to-`AugP2` PP mapping cylinder.  It must contain:

1. the `11:110000 -> 01211222` word/fine diagonal;
2. all six selected `P3+K2` faces and the six sibling `3K2` faces;
3. an explicit private/reduced-`Eq` image for the mixed mapping-square
   incidence;
4. the reduced-`Eq`/cap label descent; and
5. the labelled `gamma=-dOmega` and `-d(q_xv^01)` ridge connection.

The four packaging quotient rows remain independent in the sequence

```text
hidden lower/P2 + clean Eq                 rank 2
+ mixed mapping-cylinder incidence         rank 3
+ labelled shifted ridge                   rank 4.
```

Only after the mixed incidence is constructed is its deciding scalar

\[
                  \chi(\mathrm{mixed})
             =\delta\cdot(B(\mathrm{mixed})-Eq(\mathrm{mixed}))
\]

defined.  The normalized controls are exact:

```text
(B,Eq)=(delta,0)       Psi =  1
(B,Eq)=(0,delta)       Psi = -1
(B,Eq)=(delta,delta)   Psi =  0.
```

Therefore the selected `db01` and `dL01` faces do not break the closed-cycle
terminal.  If every completed cross-grade mixed incidence is tied or
otherwise has `chi=0`, `Psi=delta.(B-Eq)/4` survives as the normalized
terminal.  A nonzero `chi` on such a physical mixed column is the first
literal breaker.

## Scope

This is an exact rational projection theorem for the selected six-term
`db01` and eighteen-term fixed-chart `dL01` packets, with word, fine,
repeated, PP-degree and source labels retained.  It does not construct the
missing response-to-`AugP2` mapping cylinder or determine the `B/Eq` image
of its mixed incidence.
