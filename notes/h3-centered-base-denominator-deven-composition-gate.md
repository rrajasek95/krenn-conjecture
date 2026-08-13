# The centered base meets the `d_even` route exactly at the primitive cap

The face-3/face-5 denominator packet and the centered occurrence program do
fit into one exact conditional composition.  The currently proved centered
restriction formulas do **not** themselves remove the clean reset
obstruction: the promoted base cell would remove it through the same
primitive cap face which is still unconstructed.

Checker:
[`verify_h3_centered_base_denominator_deven_composition_gate.py`](../computations/verify_h3_centered_base_denominator_deven_composition_gate.py).

## 1. The two augmentations are different rows

On the clean normalized `C5` slice, the standard denominator/Cartan face
image is

\[
 \ker(\epsilon:\mathbf Q^5\to\mathbf Q),
 \qquad \epsilon(y)=\sum_{v=1}^5y_v.                 \tag{1}
\]

The selected projection needed by the even packet is

\[
                         y={e_3+e_5\over2},
 \qquad \epsilon(y)=1.                                \tag{2}
\]

For either marked centered restriction, the proved lower occurrence vector
is

\[
 R={15\over2}c_{\rm lower}+{13\over2}H_0,             \tag{3}
\]

with twelve occurrence coordinates.  Its ordinary coordinate sum is `78`.
This number is not (1): (3) lies in the separately labelled lower
occurrence module, while (1) reads the five denominator face coordinates.
In their direct sum, the extension of `epsilon` kills (3) and both common
`H0` lines.

Therefore the `13/2 H0` term cannot be reinterpreted as an aggregate-one
denominator kernel.  A comparison between those rows would be a new
physical source theorem.

## 2. Where a full centered base would close the clean obstruction

The proposed promoted base cell `G_f` explicitly requires the cap face

\[
                  p_{v,N}=(-Q_{v,N},-\operatorname{ores}),
 \qquad \epsilon(p_{v,N})=-1.                         \tag{4}
\]

Take its face-3 and face-5 translates.  On the five face coordinates,

\[
 p_3=-e_3,\qquad p_5=-e_5,
 \qquad {p_3+p_5\over2}=-y.                           \tag{5}
\]

Thus a fully physical `G_f` orbit would indeed cancel (2).  But this is not
new evidence for (4): the centered-projector theorem lists (4) as a
required face and explicitly does not construct it.  Using `G_f` as the
aggregate-one denominator cell before proving its cap face is circular.

Equivalently, the new centered restriction formulas advance the lower
occurrence faces of `G_f`, while the clean denominator obstruction remains
its first cap face.

## 3. Exact conditional composition to the two fixed tails

Assume temporarily that (4) exists on faces 3 and 5.  Both selected
companions land on `B0`.  The matching-Bianchi differences give

\[
\begin{aligned}
 A_4&=A_3-(B_4-B_0)=(-B_4,-1_{\rm ores}),\\
 A_1&=A_5-(B_1-B_0)=(-B_1,-1_{\rm ores}).
\end{aligned}                                          \tag{6}
\]

Consequently

\[
 -{A_4+A_1\over2}
   =(\operatorname{tail}=v,
     \operatorname{ores}_{\rm scalar}=1),
 \qquad v={B_1+B_4\over2}.                            \tag{7}
\]

This is the exact conditional tail found in `73ee225`.  It is not the pure
labelled residue section `d_even`: it still has tail `v` and only the scalar
ordinary-residue coordinate.

## 4. The full `p+n+label` formula

The invisible cap lift requested by the degree-four reset has

\[
                         n_i=(+Q_i,0_{\rm ores}).       \tag{8}
\]

Thus

\[
                         p_i+n_i=(0,-1_{\rm ores}).    \tag{9}
\]

If the physical occurrence-to-label comparison assigns the face-3
off-cycle occurrence to `B4` and the face-5 occurrence to `B1`, then

\[
 \boxed{
 d_{\rm even}=-{1\over2}igl[(p_3+n_3)_{B_4}
                              +(p_5+n_5)_{B_1}\bigr]
 ={B_1+B_4\over2}.}                                  \tag{10}
\]

Every sign and coefficient in (10) is fixed.  Its three physical inputs
remain open:

1. `p_i`: the primitive cap faces of the promoted centered base;
2. `n_i`: the target-zero invisible cap lifts, equivalently the relevant
   physical `K_Eq` descent; and
3. the occurrence-to-`B4/B1` label map in the actual word/fine/repeated
   grade.

The lower K4 quotient already assigns the two labels coefficientwise, but
its checker explicitly withholds a physical source chain map.  Before that
map exists, the labelled-residue covector

\[
                    \chi=(0,1,-1,0,1,-1)              \tag{11}
\]

kills the scalar/tail composition and reads one on `d_even`.

The first missing face of that physical label map is now explicit.  In the
`0112/q23:21` representative, the complete two-root Hasse square leaves
eight nonconstant one-root occurrence vectors in eight intermediate words.
The complete response rows have rank eight; adjoining these private faces
raises the rank to sixteen.  The target/Spencer triangle has zero projection
to those occurrence blocks.  Hence the label-map item above can be replaced
by the sharper requirement: an endpoint-even one-endpoint principal-parts
section cancelling those word-labelled private vectors, followed by the
reinsertion product-rule face.  The second cut is its sigma transport.

## Frontier

The strongest unified construction target is one sigma-covariant pointed
augmented comparison whose two object restrictions simultaneously supply
`p_i`, `n_i`, and the physical `B4/B1` residue labelling.  Constructing that
one orbit proves (10); constructing `d_even` directly is equivalent for the
current root-even residue gate.

The two exact projected obstructions are:

- face `epsilon`, detecting the missing primitive cap; and
- labelled `chi`, detecting the missing fixed-plane residue after the
  scalar/tail composition; and
- the occurrence-private one-root covector from the P2 placement audit.

Neither is yet a final physical terminal: each must extend across the full
word, ridge, physical-`q`, anchor, eta/sigma, `W`, and target comparison.
