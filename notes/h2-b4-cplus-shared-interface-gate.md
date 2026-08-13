# The lower `B-4` and root-even `C_+` gates have one coefficient shadow, not yet one physical cell

This note pins

- `7206f28` (the lower endpoint-parity and `B-4` reduction),
- `142606d` (the literal `0112/0121` lower-word placement),
- `bdf7a42` (the promoted orientation cell and direct-Cartan no-go),
- `3b8bcfc` and `c6e08c6` (the signless/root-even adjacent-power gate), and
- `a872264` (the full `tau_+` interface).

The accompanying checker is

```text
computations/verify_h2_b4_cplus_shared_interface_gate.py
```

Its conclusion has two deliberately separate parts.  The coefficient
projections agree exactly.  A source-labelled restriction/insertion chain
map realizing that agreement is still open.

## 1. The exact common coefficient

Write the six unordered holes of a four-endpoint packet as

```text
B0=02, B1=01, B2=03, B3=13, B4=23, B5=12.
```

The site involution `(0 1)` acts by

```text
(B0 B5)(B2 B3), with B1 and B4 fixed.
```

Let `H0=B0+...+B5` and let

\[
 c_i^+=6B_i-H_0.
\]

The integral `tau_+` debt from the full six-output interface is

\[
 D_6=(-1,2,-1,-1,2,-1)
     ={c_1^++c_4^+\over2}.
\]

Consequently its normalized lower landing is exactly

\[
 \boxed{\delta_+={D_6\over4}={c_1^++c_4^+\over8}}. \tag{1}
\]

This is not merely a rank comparison.  It is equality in the ordered
`(B0,...,B5)` output basis.  If `B_ep` denotes endpoint adjacency on the
six-hole octahedron, then

\[
 B_{\rm ep}D_6=-2D_6,
 \qquad
 (B_{\rm ep}-4I)\left(-{\delta_+\over6}\right)=\delta_+. \tag{2}
\]

Thus the missing even `B-4` cell and the missing root-even `C_+` cell demand
the same augmentation-zero coefficient at their common lower projection.

The letter `B` in the two statements must not be conflated.  `B_ep` is an
operator on lower occurrence holes.  The symbols `B0,...,B5` are the six
complete `P3+K2` output columns.

## 2. A diagonal target-normal row cannot repair the signless prism

Use target coordinates

```text
pure0, pure1, pure2, mixed0, mixed2.
```

Literal diagonal target-normal Hasse rows span the first three coordinates.
Their rank is three.  The target of the two-root Weyl defect
`2(w-1)Delta` has nonzero mixed coordinates and raises the rank to four.
The covector selecting `mixed0` vanishes on every diagonal row and is
nonzero on this defect.  Therefore no combination of diagonal target-normal
rows cancels the defect.

There is also no noncollapsing repair within the two Cartan orbit columns.
In the basis `(H_w,rho H_w)`, target cancellation imposes `a+b=0`.
Starting from the signless vector `(1,1)`, the internal correction
`(-2,0)` produces `(-1,1)`: precisely the odd prism.  Retaining the
occurrence-local input does not alter this target quotient calculation.

Hence the smallest even repair is an independent, target-bearing,
`rho`-even relative cell `C_+`; it is not a diagonal normalization of the
old Cartan prism.

## 3. The minimum common full interface

Let

\[
 D_{\rm root}=(-1,1,-1,1),
 \qquad
 v={B_1+B_4\over2}.
\]

Any physical common cell must carry all of the following data together:

\[
\begin{array}{c|c}
\text{interface} & \text{required value}\\ \hline
\text{parity} & \rho\text{-even}\\
\text{upper target} & -2D_{\rm root}\otimes v\\
\text{complete lower landing} & \delta_+\\
\text{reduced-Eq face} &
  +2D_{\rm root}(H_0-u){\rm Eq}\otimes v\\
\text{ordinary labelled residue} & v.
\end{array} \tag{3}
\]

Its next literal Cartan/Hasse boundary is

\[
 R_+={1\over9\alpha\beta}(1+\rho)H_wd(P(J_*)), \tag{4}
\]

together with the one-endpoint product-rule cross term.  This is
load-bearing: the old formal fourth-Hasse filler projects to
`(Eq,w)=(1,1)`, while the required correction is `(1,0)`.  The covector
`(1,-1)` separates them.  Thus a bare coefficient filler does not supply
the source-valid reduced-Eq face.

## 4. Exact theorem and exact open map

**Shared-interface theorem (conditional physical form).**  Suppose there
is a source-valid, `rho`-equivariant restriction/reinsertion map from the
two lower occurrence packets to the six complete output columns, preserving
word, fine grade, repeated grade, target, reduced-Eq, labelled residue, and
the Hasse faces in (3)--(4).  If it sends the endpoint-even `B_ep-4I`
family to its complete lower projection, then that projection is the
`C_+` landing `delta_+` in (1).  Conversely, a physical `C_+` orbit whose
two marked order-two restrictions are the `B_ep-4I` endpoint family closes
the odd-dark lower centered branch.

What is proved unconditionally is the coefficient identity (1), the short
preimage (2), and the target no-go.  What is **not** proved is the physical
map in the hypothesis.  The lower theorem has two twelve-coordinate source
packets, in words `0112` and `0121`; the `C_+` theorem has a six-coordinate
complete-output quotient.  Equality of their common coefficient shadow
does not manufacture a chain map between those presentations.

The remaining construction is therefore one precise object: a full
`rho`-even product-rule/Bianchi orbit `C_+` whose two order-two restrictions
realize the lower `B_ep-4I` occurrence family and whose next boundary is
(4) with the required reduced-Eq correction.  Producing that one cell would
merge the two gates; until then they share an exact interface but remain
distinct physical obligations.

## Reproduction

```bash
python3 computations/verify_h2_b4_cplus_shared_interface_gate.py
python3 -O computations/verify_h2_b4_cplus_shared_interface_gate.py
python3 -I -S computations/verify_h2_b4_cplus_shared_interface_gate.py
```

Pinned ledger digest:
`0173b3e8fbb5fc377b71d6f024f28cd6bccfe5a732e8eeac7272804b49a20d7e`.
