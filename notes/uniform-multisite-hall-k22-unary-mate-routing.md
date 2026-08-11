# The strict `K2,2` unary mate has three anchor-web routes

## Result

The strict opposite-shore packet contains a forced pure-colour unary
matching.  For colour 1, the two diagonal core terms use

```text
holes 01 with cofactor 23|45,
holes 23 with cofactor 01|45.
```

Their nonvanishing forces

\[
             q_{01}^{11}q_{23}^{11}q_{45}^{11}\ne0.   \tag{1}
\]

But `q^[3]=X0`, so the pure-`1` unary coefficient is zero.  One of the
other fourteen physical perfect matchings must cancel (1).

There are exactly three nonfree matching types:

1. an exact physical copy of the selected pure-zero matching `Q0`;
2. the other core matching `02|13|45`; or
3. the third core matching `03|12|45`.

The remaining eleven alternatives are bridge matchings with a physical
edge outside the selected pure-anchor web.  They enter the existing free
active-carrier route.  The three anchor-web alternatives are not an odd
signed circuit: the `Q0` copy lands on the affine line-hitting gate, while
the other two enter literal diagonal/crossed response coefficients and
force a bridge product or an off-axis mate.

Checker:
`computations/verify_uniform_multisite_hall_k22_unary_mate_routing.py`.

## 1. Exact fifteen-matching classification

On six residual sites let

```text
M1=01|23|45,  M2=02|13|45,  M3=03|12|45.
```

These are the three perfect matchings containing `45`.  The other twelve
matchings pair sites `4,5` separately into the K4 core.  Fix the normalized
bridge unary anchor

```text
Q0=01|24|35.
```

Among the twelve bridges, exactly one is `Q0`; every other bridge changes
at least one core-to-`{4,5}` edge.  The selected diagonal matchings use
only K4 edges and `45` in their residual cofactors, so that changed bridge
edge lies outside all three selected pure matchings.  The exact arithmetic
is therefore

```text
14 alternatives to M1
 = 11 free noncopy bridges + Q0 + M2 + M3.             (2)
```

This corrects the informal count “twelve other free matchings”: there are
eleven after the three anchor-web alternatives are removed.

## 2. `M3` enters the crossed row

If the `M3` alternative is nonzero, then `q12:11*q45:11` and
`q03:11*q45:11` are nonzero.  The selected-axis crossed coefficient with
shore holes `03` contains the complete cofactor

\[
 q_{12}^{11}q_{45}^{11}
 +q_{14}^{11}q_{25}^{11}
 +q_{15}^{11}q_{24}^{11}.                              \tag{3}
\]

The endpoint-star pivot is a unit on the strict chart.  Hence the crossed
zero row forces one of the two bridge products in (3), unless a same-word
off-axis endpoint-star mate occurs.  Either alternative leaves the isolated
anchor web and enters the already named carrier/lock routing.

## 3. `M2` enters the other diagonal row

The `M2` alternative is a colour-1 copy of the physical matching used by
the colour-2 core.  In the colour-2 diagonal response with selected holes
`02`, take the word which is colour 2 on those holes and colour 1 on the
remaining sites.  Its selected-axis coefficient is

\[
 p_{2,2}s_{2,0}
 \left(q_{13}^{11}q_{45}^{11}
      +q_{14}^{11}q_{35}^{11}
      +q_{15}^{11}q_{34}^{11}\right).                 \tag{4}
\]

The first term is nonzero for `M2`, while the target tensor has no such
mixed word.  Therefore (4) forces a bridge product or an off-axis
endpoint-star cancellation mate.  This consumes the second K4 alternative
using a literal full response coefficient, not an abstract recolouring.

## 4. The `Q0` copy is exactly the affine gate

Suppose the colour-1 cancellation matching is the physical unary anchor
`Q0=01|24|35`.  Recolour edge `01` and retain pure zero on the other four
sites.  The unary mixed coefficient is

\[
 q_{01}^{11}H_{01}^{00},qquad
 H_{01}^{00}=q_{23}^{00}q_{45}^{00}
             +q_{24}^{00}q_{35}^{00}
             +q_{25}^{00}q_{34}^{00}.                 \tag{5}
\]

The same complete cofactor occurs in the colour-1 diagonal response with
holes `01`, multiplied by the selected endpoint-star factor.  Thus the
copy is an additional contribution in the same target affine fibre.  It
does not yield an independent scalar unit or odd holonomy.  It lands
precisely on the previously isolated line-hitting/joint-kernel gate: either
the complete fibre has a target-coordinate representative, a kernel switch
deletes a blocker, or further cancellation terms expose a free carrier.

## 5. Why `H03=H12=0` does not itself kill `q45`

The scalar pure-zero support

```text
01,24,35,45
```

has top hafnian one, both shore cofactors zero, and `q45!=0`.  Consequently
the implications

```text
q^[3]=1, H03=H12=0  =>  q45=0
```

and “no alternative cofactor product implies `q45=0`” are false without
the pure-colour unary zero rows and the response routing above.  The extra
`45` cell is top-invisible in this guard.  The guard is not a full one-bad
source; it only pins the logical dependency.

## Scope

This is a uniform matching-family and complete-cofactor argument, not a
support census.  It consumes the two K4 alternatives into literal response
rows and routes the exact `Q0` copy to the established affine gate.  It does
not solve that affine joint-kernel problem and does not claim a full-packet
contradiction from the selected matching data alone.

## Verification

Run

```text
python3 computations/verify_uniform_multisite_hall_k22_unary_mate_routing.py
python3 -O computations/verify_uniform_multisite_hall_k22_unary_mate_routing.py
python3 -I -S computations/verify_uniform_multisite_hall_k22_unary_mate_routing.py
```

Frozen ledger SHA-256:

```text
1619d4e8916463a4119f6f15ae2f6adb5e229ab4e4cb599040fd67fd5b8c1199
```
