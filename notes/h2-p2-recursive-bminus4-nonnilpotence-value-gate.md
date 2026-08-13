# Recursive unlabelled `B-4` repair is not nilpotent; the labelled Hasse square is the finite object

## Outcome

Applying the same coefficientwise even `B-4` repair to every successive
one-root private face does not produce a decreasing filtration. The exact
recursive operator on the full four-site ternary word module is not
nilpotent:

\[
                         \operatorname {tr}(R^2)=109/3. \tag{1}
\]

Starting from the `0102` private face, one repair returns nontrivially to
the original word `0112`, and the next returns nontrivially to `0102`.
After four iterations every one of the 81 four-site ternary words is
present. Thus repeating the same unlabelled Cartan/`B-4` cone would create
an infinite repair problem rather than close `P2`.

This does not contradict finite Hasse totalization. The recursive operator
forgets which of the two root directions has already been used and resets
the Hasse degree after every lift. Retaining those labels gives one
two-direction Boolean/cobar square, whose differential squares to zero.
The remaining positive theorem is therefore one physical realization of
that labelled square, not an unbounded sequence of new cells.

The first private class is also a value-level response obstruction. The
single complete equation `H_0102=0` does not imply its vanishing: an explicit
two-occurrence evaluation has `H_0102=0` and private value `-13/12`.

Checker:
[verify_h2_p2_recursive_bminus4_nonnilpotence_value_gate.py](../computations/verify_h2_p2_recursive_bminus4_nonnilpotence_value_gate.py).

## 1. The strongest natural recursive operator

For each word `w` in `{0,1,2}^4`, let `V_w` be its twelve-dimensional
ordered occurrence module. Let

\[
 P_{\rm priv}={1+S\over2}-{1\over12}J              \tag{2}
\]

project onto the five-dimensional endpoint-even, augmentation-zero
quotient. On this quotient, `B` has eigenvalues `0,-2`; hence

\[
 L=-{1\over4}P_0-{1\over6}P_{-2},
 \qquad (B-4I)L=P_{\rm priv}.                         \tag{3}
\]

For every one-root Hasse transition `w -> w'`, let `D_(w',w)` be the
diagonal matrix counting the root face at each retained occurrence. The
strongest coefficientwise recursive repair is

\[
 R_{w',w}=P_{\rm priv}D_{w',w}L.                      \tag{4}
\]

It acts on

\[
                 \bigoplus_{w\in\{0,1,2\}^4}
                    P_{\rm priv}V_w,
\]

which has dimension `81*5=405`.

Every one-root face changes the word, so `tr(R)=0`. Nilpotence would force
all positive-power traces to vanish. Exact summation over the 288 oriented
two-step word round trips instead gives (1), proving that (4) is not
nilpotent.

## 2. The selected private face returns immediately

Starting with the exact `0102` private vector from the preceding gate gives
the following first iterations:

| iteration | nonzero words | min/max distance from `0112` | selected return |
|---:|---:|---:|---|
| 1 | 8 | 0/2 | detector on `0112` is `35/72` |
| 2 | 32 | 0/3 | detector on `0102` is `-857/3888` |
| 3 | 64 | 0/4 | nonzero |
| 4 | 81 | 0/4 | all words reached |

In particular, neither root-count nor word distance decreases. The first
step already reaches distance zero from the original word. The second has a
nonzero round trip to the starting intermediate word.

These are statements about the natural recursive operator (4), not a no-go
for every filtered enlargement. A different filtration could work only if
it retains additional Hasse-direction or cone-degree data that (4) forgets.

## 3. Why the labelled Hasse square remains finite

Let the two root directions be labelled `0,1`. In the Boolean Hasse
coalgebra, the reduced coproduct of the two-direction top is

\[
             \Delta'\{0,1\}={0\}|\{1\}+\{1\}|\{0\}. \tag{5}
\]

The cobar differential of the right side vanishes by the two opposite
parenthesizations, so

\[
                              d_{\rm cobar}^2=0.       \tag{6}
\]

Thus the source-side product rule already has a finite totalization. The
apparent infinite recursion arises only after discarding the direction
labels and applying `(B-4)^-1` as though every face were a fresh top.

The shortest positive theorem is consequently:

> Realize the one labelled two-root Hasse square in the physical
> occurrence complex, with the `0102` one-endpoint section and its
> `dq23:21` reinsertion face.

No separate cell is required for every word reached by (4), provided this
single comparison respects the labelled cobar boundary.

## 4. The private class is not killed by the complete response value

Write the twelve literal occurrence monomials in word `0102` as
`m_0,...,m_11`. The complete source equation is

\[
                         H_{0102}=\sum_i m_i.          \tag{7}
\]

The private vector is not constant, so it is not in the degree-preserving
span of (7). More concretely, set

```text
m0=1, m1=-1, all other mi=0.
```

Then

\[
             H_{0102}=0,
 \qquad r_{\rm priv}=-13/12\ne0.                      \tag{8}
\]

This is an exact coordinate-pivot witness in the literal response block.
It proves that the private face is not merely a chain-level artifact erased
by evaluating the complete response row.

Equation (8) is deliberately scoped: the displayed occurrence evaluation
is not claimed to satisfy all other word, target, anchor, or physical-`q`
equations simultaneously. Hence it does not yet give a full physical source
point or a Fredholm terminal. It establishes the first value-level
membership obstruction and explains why a source-minimality pivot would
have to use additional global equations.

## Frontier

The raw recursive `B-4` strategy is eliminated. The finite route is the
existing labelled Hasse/cobar square plus one missing physical
occurrence-local comparison. Its boundary must contain the even private
one-endpoint face and the independent reinsertion conormal, while carrying
the protected augmented readouts. Failure can be terminalized only after
the private covector is extended over that complete augmented map.

Run:

```text
python3 computations/verify_h2_p2_recursive_bminus4_nonnilpotence_value_gate.py
python3 -O computations/verify_h2_p2_recursive_bminus4_nonnilpotence_value_gate.py
python3 -I -S computations/verify_h2_p2_recursive_bminus4_nonnilpotence_value_gate.py
```

Frozen ledger SHA-256:

```text
efdb245d2055178250441190d82b5fb7f5488ecb368d8c9877cda49a890e23db
```
