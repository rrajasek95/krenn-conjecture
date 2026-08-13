# The odd input needs one pointed excess-to-occurrence comparison

## Exact verdict

Neither of the two categorical shortcuts constructs the missing physical
Gate-I input by itself.

1. The derived self-intersection of the noninjective `0,2 -> 4` collapse
   retains the excess conormal as a degree-one Tor **cycle**.  It does not
   supply a cell whose differential is the occurrence class `Xi^-`.
2. The endpoint-odd Weyl bar is a genuine chain over the tail-root orbit,
   but the root action is not an automorphism of the fixed GHZ fibre.
   Canonical transport back to that fibre identifies the Weyl-shifted
   occurrences and kills the private four-corner packet.

The shortest positive theorem is therefore one pointed, augmented
excess-to-occurrence comparison.  Its first unavoidable datum is a
degree-preserving map from the oriented excess line to the already certified
rank-one occurrence quotient `Q_xi`, with the literal word/fine/repeated
labels.  This is strictly smaller than a comparison on all fifteen collision
labels, but it is not supplied by ordinary derived base change or by passing
to a homotopy quotient.

Checker:
[`verify_h3_selected_lower_excess_orbit_pointed_comparison_gate.py`](../computations/verify_h3_selected_lower_excess_orbit_pointed_comparison_gate.py).

## 1. Why excess intersection retains rather than kills the class

The minimal model is

\[
 A=\mathbb Q[x],\qquad B=A/(x).
\]

The derived self-intersection is represented by

\[
 B\otimes_A^{\mathbf L}B=\bigl[B e\mathrel{\mathop{\longrightarrow}^{0}}B\bigr].
\]

Thus the excess generator `e` survives in `H_1`.  Endpoint oddization of two
copies leaves `e-rho e` as another cycle.  By contrast, a physical filler of
the selected occurrence quotient would have

\[
                         d\sigma_\xi=\Xi^- .             \tag{1}
\]

The unit differential in (1) kills the degree-zero and degree-one pair; it
is not the zero differential produced by derived base change.  A Gysin or
connecting map can identify the excess line with `Q_xi`, but specifying that
map is extra structure.  Calling `Xi^-` “the excess conormal” without this
map merely renames the open comparison.

The exact Hasse cross term does constrain this extra structure.  For
multi-affine factors,

\[
       \partial_4^{[2]}(fg)=(\partial_4f)(\partial_4g)       \tag{2}
\]

with coefficient one.  The pinned shared-loop audit sends (2) to precisely

```text
fixed shared label:  B1 or B4,
rho-paired labels:   (B0+B5)/2 or (B2+B3)/2.
```

So (2) fixes the normalization and the correct C4 occurrence tails.  It
does not yet give (1).  Its available third-Bianchi carrier has marked word
`222000`, its rho mate has word `202020`, and its formal augmented tail is

```text
(ainc,W,target,ores)=(-1,0,0,0).
```

The selected class instead occupies four fine degrees with repeated profile

```text
(1,1,1,2,1,1,1,2).
```

Consequently the diagonal Gysin proposal reaches the right one-dimensional
occurrence direction, but still lacks the physical word/fine lift and the
protected cap that would turn it into `-Xi^-` with output `+/-M_v`.

## 2. Why the orbit quotient does not remove the comparison

The four tail-root directions at sites `2,5` move the GHZ tensor to four
independent mixed target words.  Hence the local Weyl path is not an action
on the exact fixed source fibre.  Only the endpoint swap used for oddization
fixes that fibre.

Over the target orbit, the endpoint boundary of the odd bar is

\[
                         -v+sv+wv-swv.                  \tag{3}
\]

Its base projection is zero because the two source paths cover the same
target path.  But canonical `w^{-1}` transport to the initial fibre sends
`wv` to `v` and `swv` to `sv`, so (3) becomes zero.  There are exactly two
choices:

- use canonical equivariant transport and lose the private packet;
- retain the fixed occurrence labels through a nontrivial local system,
  which is the missing comparison/connection.

Passing to the homotopy quotient of the exact fixed fibre is therefore not
available: the required root element is not in its stabilizer.  Passing to
the quotient of the whole orbit family makes the bar genuine, but a class
there need not give a physical kernel vector at the chosen GHZ fibre;
basepoint evaluation kills exactly (3).  A labelled basepoint section or
connection is again required.

The terminal alternative cannot yet be moved upstairs for free.  It needs a
horizontal family of the physical cocycle

\[
                         q=\sum_{i=1}^6m_i-\mathrm{ainc}. \tag{4}
\]

Unaugmented orbit transport does not force `q` horizontality.  Moreover, a
group-homology class detected by an equivariant `q` would still need a
conservative basepoint comparison before it becomes the physical relative
generator required by the fixed-fibre theorem.

## 3. What the order-six cofibrant resolution does solve

The source-closed, tail-antisymmetric order-six representative has 372
terms and 126 singleton Spencer faces.  Those faces are one coherent
universal Spencer differential, not 126 unrelated physical obligations.
The universal Euler contraction makes every positive Spencer degree
contractible.

There is an even sharper finite result: inside the same 8,580-column bounded
operator block, an exact 343-term representative has

```text
literal source = 0,
D1 singleton face = 0,
D2 = -delta.
```

Augmented HPL proves that `D2` is canonical on `D1` homology.  Thus the proof
does **not** need to place each of the 126 old faces in the old physical row
ideal.  The complete cofibrant/Spencer model already packages the higher
operation.

This does not construct Gate I.  The 343-term class lives in the bounded
coefficient-operator complex.  The missing map is still the comparison from
that complex—and specifically its one oriented occurrence/excess line—to
the literal 360-feature repeated-`P3+K2` physical correction complex.  The
physical output `M_v` is constructed; the input occurrence map and physical
`q` on its domain are not.

## 4. Pointed comparison theorem sufficient for closure

It is enough to prove the following single theorem.

> **Pointed odd excess comparison.**  There is a pointed morphism of source
> presentations, together with its filtered PP/Spencer chain map, from the
> orbit-relative excess model to the canonical physical `h=3` correction
> complex such that:
>
> 1. on the selected oriented excess generator, the associated-graded
>    boundary is the normalized `-Xi^-` packet in its four literal fine
>    degrees;
> 2. the augmented image is the already fixed `+/-M_v`, preserving the
>    word, repeated grade, protected rows, and eta/sigma terminal;
> 3. on degree-zero source functions,
>    `f-Phi^*(a_Eq)` lies in the complete response ideal—equivalently the
>    private/global diagonal has conormal `d(u_f-u)=0`; and
> 4. the complete source domain carries the physical cocycle (4).

Clause 3 makes anchor faithfulness automatic by differentiated conormal
functoriality.  Clause 4 does not require exact terminal equality across the
comparison: once both sides are physically typed, a nonzero `q` defect is
already the protected-kernel relative-generator branch, while zero defect
transports `q` and enables the Fredholm branch.

The dimension-one excess line, the dimension-one `Q_xi`, and the unit Hasse
coefficient make this theorem plausible and minimal.  The first unproved
statement is their **physically graded identification**, not the existence
of either abstract line.  Until it is supplied, the primitive occurrence
dual is a separator only for the tested old inventory, not a physical
terminal/Fredholm functional.

## Scope and verification

This is a sharp construction gate, not a no-go against an enriched pointed
PP comparison.  It proves that ordinary excess pullback, ordinary
fixed-fibre transport, and an unaugmented orbit quotient do not provide that
comparison.  It also removes the 126 separate Spencer-face searches from
the frontier.

Run:

```text
python3 computations/verify_h3_selected_lower_excess_orbit_pointed_comparison_gate.py
python3 -O computations/verify_h3_selected_lower_excess_orbit_pointed_comparison_gate.py
python3 -I -S computations/verify_h3_selected_lower_excess_orbit_pointed_comparison_gate.py
```

Frozen ledger SHA-256:

```text
208553758ea514371e2647aa65cb33520a834feaadf4f9a48e6db7bb7da8f431
```
