# Both colour copies route the strict `K2,2` physical-copy residual

## Result

The exact physical-`Q0` copy left by the strict Hall `K2,2` unary audit does
not remain an independent affine gate once **both** non-target colour copies
and the complete response rows are used.

Normalize

```text
Q0=01|24|35,
M1=01|23|45,   M2=02|13|45,   M3=03|12|45.
```

The K4 core edge `01` of `Q0` belongs to the colour-1 matching `M1`.  Use
the colour-2 copy of `Q0` in the colour-1 diagonal response word which is
colour 1 at holes `01` and colour 2 elsewhere.  Its selected-axis row is

\[
 p_{1,0}s_{1,1}H_{01}^{22}=0.                         \tag{1}
\]

If no endpoint-star mate occurs, (1) gives `H01^22=0`.  The pure-colour-2
unary row factors as

\[
 [222222]q^{[3]}
 =q_{01}^{22}H_{01}^{22}
  +\sum_{R\not\ni01}T_R=0.                            \tag{2}

The selected `M2` term in the sum is nonzero.  Hence another matching
avoiding `01` must occur.  It is either `M3`, which enters the already
identified crossed row, or one of ten bridge matchings, each exposing a
physical pair outside the selected anchor web.

If (1) has an endpoint-star mate, its word type is equally rigid: the only
other pure-axis orientation is the reverse `01` orientation, which makes
the complete hole-`01` star factor vanish and permits target-witness
reselection; every other mate
contains an off-diagonal endpoint cell and enters the active/lock route.

Thus the physical-copy residual routes to already named proof interfaces.
There is no additional `Q0`-specific support packet, but this statement is
a reduction, not by itself a proof that the full affine gate is empty.

Precisely, the ten avoiding bridges always leave the selected anchor web and
enter the certified free/active route.  The other two outcomes retain named
obligations:

1. `M3` enters a crossed complete coefficient.  That coefficient forces a
   free bridge or an off-axis endpoint mate; the latter may still be the
   trapped-lock residual of the five-lock interface.
2. The reverse-axis mate kills the complete contribution at holes `01` and
   permits source-preserving **witness reselection**.  It does not alone prove
   that an affine response fibre meets a target-coordinate line.

Consequently the exact implication needed for full closure is:

```text
all M3/off-axis mates exit to a proved unit/free/curved branch,
and every reverse-axis reselection either gives an anchor-safe
joint-kernel target-coordinate point or strictly decreases a
well-founded selected-support measure.
```

Neither additional implication is asserted by this checker.

Checker:
`computations/verify_uniform_multisite_hall_k22_q0_copy_affine_closure.py`.

## 1. The common complete cofactor

The colour-2 Q0 copy makes

\[
 q_{24}^{22}q_{35}^{22}\ne0.                          \tag{3}

For the output word `112222`, the selected colour-1 endpoint cells occupy
holes `01`.  The remaining coefficient is the complete four-site hafnian

\[
 H_{01}^{22}
 =q_{23}^{22}q_{45}^{22}
  +q_{24}^{22}q_{35}^{22}
  +q_{25}^{22}q_{34}^{22}.                            \tag{4}

The middle term is (3).  Since the diagonal response target has no mixed
word, its full coefficient is zero.  Terms with the same selected endpoint
holes give exactly (1); different endpoint holes are handled in Section 3.

Equation (2) is not a formal recurrence.  The three matchings containing
`01` are precisely the three terms of `q01^22 H01^22`.  The other twelve
physical matchings avoid `01`.

## 2. What remains after `H01^22=0`

Among the twelve matchings avoiding `01`:

```text
M2=02|13|45         selected and nonzero,
M3=03|12|45         crossed-row route,
ten bridge matchings.
```

Each of the ten bridges differs from `Q0` and contains an edge outside

```text
Q0 union M1 union M2 union M3.
```

The selected diagonal matchings use only K4 edges and `45` in their
residual cofactors.  Therefore such an outside bridge edge is absent from
all three selected pure matchings and enters the pinned free active-carrier
reselection theorem.  Since `M2` is already nonzero, (2) forces `M3` or one
of these ten bridges.  This is the load-bearing use of the other pure-colour
unary equation.

## 3. Complete endpoint-star mates

The word `112222` has colour 1 only at sites `0,1`.  A pure diagonal
`p1,s1` pair can therefore occur only in orientations `(0,1)` and `(1,0)`.

The first is the selected pivot.  With the reverse orientation and no
off-axis terms, the mixed row factors as

\[
 (p_{1,0}s_{1,1}+p_{1,1}s_{1,0})H_{01}^{22}=0.        \tag{5}
\]

If `H01^22` is nonzero, the parenthesized star factor vanishes.  The same
factor multiplies `H01^11` in the pure colour-1 response, so the complete
hole-`01` contribution is zero.  Since the total diagonal target
coefficient is one, another hole has a nonzero complete contribution and
can be selected without changing the source.  This is the target-witness
form of the existing affine gate, not a new support case.

Every other ordered hole pair uses a site of output colour 2.  At least one
endpoint cell then has outer colour 1 and residual colour 2.  It is an
off-diagonal endpoint cell.  The private-site and five-lock theorems route
such a mate to a free active companion, an anchor-safe lock kernel, or the
already isolated trapped-lock branch.

## 4. The other K4 core edges

Every bridge matching has exactly one K4 core edge.  The six K4 edges split
as the three perfect matchings `M1,M2,M3`.

- If the Q0 core edge lies in `M1`, use the colour-2 copy as above.
- If it lies in `M2`, exchange colours and use the colour-1 copy in the
  colour-2 diagonal row.
- If it lies in `M3`, either non-target copy enters a crossed shore row
  directly.

Hence the argument is uniform across the strict rectangle and does not
depend on the displayed labelling.

## Scope

This is complete-cofactor and endpoint-word algebra, not another matching
support census.  It removes the physical-copy packet as a new combinatorial
obstruction by routing every branch to a previously isolated theorem
interface.  It proves that all ten avoiding bridges are free relative to
the anchor web.  It does not turn reverse-axis witness reselection into an
affine target-line point, and it does not close the trapped-lock alternative
that can follow `M3` or another off-axis mate.

## Verification

Run

```text
python3 computations/verify_uniform_multisite_hall_k22_q0_copy_affine_closure.py
python3 -O computations/verify_uniform_multisite_hall_k22_q0_copy_affine_closure.py
python3 -I -S computations/verify_uniform_multisite_hall_k22_q0_copy_affine_closure.py
```

Frozen ledger SHA-256:

```text
586a44e9293e903aa4c025a08c0fb5869f127bd4450910bb262da099e2294027
```
