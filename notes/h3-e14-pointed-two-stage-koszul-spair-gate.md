# A pointed E14 higher cell must carry the full twelve-tail unary S-pair

## Result

The private return cannot be installed by the degree-zero source-algebra
map: pointedness kills it.  Keeping the degree-zero map pointed and moving
the return to a higher PP/Koszul homotopy is formally viable, but its first
literal physical proper face is forced and is not closed by the present
inventory.

On the only silent localization branch, `v04_00=0`, put

```text
g=(p1_0_1*s1_1_1)u35_11*v24_11.
```

The complete mixed unary row splits as `U=pA+B`, with

```text
p=u35_11,
A=-1+v04_00,
B=12 nonpivot monomials.
```

After multiplying by `v24_11`, the exact source row is

\[
 v_{24}^{11}U_{000101}=-R_{E14}+T_{12},               \tag{1}
\]

where `R_E14=g-v04_00*g` and `T_12` is the packet of twelve nonprivate
tails.  At `v04=0`, (1) becomes `-g+T_12`.

Therefore a higher cell with principal face `g` cannot omit `T_12`.  The
total boundary has thirteen face blocks—one factorized private face and
twelve proper tails—and fourteen literal monomials before specializing
`v04=0`, because the private face has two monomials.

Checker:
[`verify_h3_e14_pointed_two_stage_koszul_spair_gate.py`](../computations/verify_h3_e14_pointed_two_stage_koszul_spair_gate.py).

## The centered-occurrence shortcut is coefficient-only

For a marked occurrence `g` among the ninety pure-target occurrences,

\[
 c_g=90e_g-\mathbf1_{90},\qquad
 c_g+\mathbf1_{90}=90e_g.                             \tag{2}
\]

This is an exact and useful compression.  Retaining the target coordinate
of the complete pure-target response row changes the bare identity to

\[
 c_g+(\mathbf1_{90}-u)=90e_g-u.                       \tag{3}

Give the construction every benefit and suppose the centered `c_g` cell
also carries the primitive cap face `(-Q,-ores)`.  Integrally, (3) then has
signature

```text
(principal g, target, Q, ores)=(90,-1,-1,-1).
```

Isolating coefficient one on `g` divides every augmented face by 90.  After
the central `K_Eq` correction cancels `Q`, the normalized signature is

```text
(1,-1/90,0,-1/90),
```

whereas the required E14/primitive-cap signature is `(1,-1,0,-1)`.  The
residual is `(target,Q,ores)=(-89/90,0,-89/90)`.

This residual is **not** a new class in the reduced old cap quotient.  At
the normalized cap parameter, the old columns have

```text
           Yw  target  Q  ores
T          -1     +1   0    0
rho        +1      0   0   +1
T+rho       0     +1   0   +1.
```

Consequently `desired-current=(-89/90)(T+rho)` in the convention above.
Equivalently, if the residual is recorded as a debt, the opposite multiple
cancels it.  Thus `T+rho` removes the factor-90 discrepancy *coarsely*.

The correction is not yet physical in the required summand.  The committed
primitive cap is in word `01211222`, fine degree `t*q_(v,N)`, repeated grade
`P3+K2`; `g` is tagged in pure target `G11[111111]`, and its unary E14
comparison is word `000101`.  The old two-generator cap calculation defines
only `(Yw,target,ores)`: it does not construct a source-labelled copy in the
pure-target word or certify the anchor, physical-`q`, ridge, eta, and sigma
rows there.  Therefore the normalization is conditionally merged with
`z_cap`, while the word/grade transport remains open.

There is also an exact word obstruction.  The committed centered occurrence
calculation is for the marked mixed response block

```text
11:110000,
```

whereas `g` is literally a marked occurrence of the pure target row
`G11[111111]`, and its actual E14 cycle-breaker is the mixed unary word
`000101`.  A centered family natural in word and occurrence tag would give a
promising *input*, but the transport between these word/fine/repeated
summands is precisely the missing four-root comparison.  A site/global
colour relabel cannot turn `110000` (multiplicities `4,2,0`) into `111111`
(`0,6,0`), so the known `c_f` cannot simply be reused as `c_g`.

## Why the first proper face does not reduce away

The twelve tails in (1) consist of ten cubic and two quartic monomials.  The
complete target-augmented first-hit module contains 269 independent physical
columns that hit them.  Exact reduction gives

```text
T_12 -> R_E14,
```

not zero.  A rational dual of support 22 kills all 269 columns and pairs
`-1` with the tail packet; its primitive integral pairing is `-30`.

This is the concrete first `d^2`/chain-map proper face.  The reduced-Eq term
`(H0-u)e_Eq` is only a projection of the face.  A valid higher comparison
must retain all twelve word-resolved tails, their target readouts, and their
subsequent companion homotopy.

## Shortest positive construction target

The minimal pointed totalization now has the following form.

1. Its degree-zero source-algebra map remains pointed.
2. It has the separate conormal face `P_f`, with `dP_f=u_f-u`.
3. A higher endpoint-word-change cell sends the central product to
   `R_E14` and carries the complete `T_12` proper-face packet from (1).
4. A next companion homotopy kills the first-hit class of `T_12` while
   retaining word, fine, repeated, target, residue, `q`, ridge, `W`, eta,
   and sigma typing.

`P_f` may be another homogeneous face of the same augmented totalization,
but it is not the E14 higher cell.  The primitive-cap normalization need not
be an independent direction if a fully typed pure-word copy of `T+rho` is
constructed.  Constructing the word/grade transport and the final companion
homotopy are the genuine positive obligations; the present theorem identifies
the first literal proper face without collapsing the full S-pair to its Eq
shadow.

## Scope

This is exact for the canonical `h=3`, chart-`(1,1)`, silent `v04=0`
branch.  It does not rule out a new mapping-cone/Tate attachment and does
not promote the first-hit dual to a physical terminal.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
bdaab7de4af63d8d043f19fcfd0e81234f0ceec1f7e671cd13ca987dd4d8455e
```
