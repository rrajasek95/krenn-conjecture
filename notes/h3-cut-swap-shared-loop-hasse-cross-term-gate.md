# Gate I shared-loop Hasse cross-term gate

The concrete product-rule idea is exact, but only at the occurrence level.
It identifies the right missing packet; it does **not** construct the two
physical labelled-residue sections.

The frozen checker is
`computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py`.
It has ledger digest
`8e60905c81012cc720e51e1f7887dde9f2c4e079c3767fcbb399b6d6ac4cbd85`.

## 1. The product-rule calculation

For multi-affine factors in the repeated coordinate,

\[
 f=f_0+t f_1,\qquad g=g_0+t g_1,
\]

the divided-power coefficient is

\[
 \partial_t^{[2]}(fg)=f_1g_1
                       =(\partial_t f)(\partial_t g).       \tag{1}
\]

Equivalently, the ordinary second derivative has two ordered cross terms,
and the Hasse normalization divides their sum by two.  This is precisely the
two-corner normalization in a C4 switch.

The exact first-collapse switch table is

| shared matching | switched partner | two corners | normalized image |
|---|---|---|---|
| `02|13|45` | `13` | `M0,M6` | `B3` |
| `02|13|45` | `45` | `M10,M13` | `B0` |
| `02|14|35` | `14` | `M1,M9` | `B1` |
| `02|14|35` | `35` | `M7,M14` | `B4` |
| `02|15|34` | `15` | `M2,M12` | `B5` |
| `02|15|34` | `34` | `M8,M11` | `B2` |

Both corners in a row collapse to the displayed `B` direction, so (1)
returns one copy of it.  Thus the fixed shared label has choices `B1` and
`B4`, and its rho-even average is

\[
 d_{\rm even}=\frac{B_1+B_4}{2}.                         \tag{2}
\]

The rho-paired labels have exactly the two choices

\[
 \frac{B_0+B_5}{2},\qquad \frac{B_2+B_3}{2}.             \tag{3}
\]

In particular, the favorable selection `B0,B4,B5` is the already audited
decorated face-3 packet

\[
 q_{34}^{11}
 \bigl(q_{3,12|45}+q_{3,14|25}+q_{3,15|24}\bigr).        \tag{4}
\]

So the Hasse cross term explains exactly why the two rho-orbit repair
directions found in the brute-force C4 census have the shape they do.

## 2. Third-Bianchi occurrence carrier

The collision-cofactor model supplies a natural formal carrier.  For the
three shared matchings use respectively

\[
 W_{02}K_{13}q_{45},\qquad
 W_{02}K_{14}q_{35},\qquad
 W_{02}K_{15}q_{34}.                                   \tag{5}
\]

After transporting the exact dormant-connection model, every expression in
(5) is invisible in orders zero, one, and two, and contributes coefficient
one at order three in the marked word `222000`.  This confirms that the
third-Bianchi layer is the first polynomial layer capable of carrying (1).

But the three displayed carriers are not rho-stable.  With
`rho=(1 4)`, the first becomes

\[
  W_{02}K_{34}q_{15}
\]

in word `202020`, rather than the displayed `K15` carrier.  A rho-symmetric
construction therefore necessarily adds a complementary tangent placement
in another word summand.

## 3. Why this is not yet a source cell

There are three independent exact guards.

1. The C4 frame theorem types each switch as a same-word occurrence pair,
   but does not make the pair a binomial source boundary.
2. The committed complete Hasse totalization has formal tail signature

   \[
   (\operatorname{ainc},W,\operatorname{target},\operatorname{ores})
       =(-1,0,0,0),                                    \tag{6}
   \]

   whereas a labelled-residue section needs `(0,0,0,1)`.  The formal cell
   also retains a rank-six endpoint-ridge mismatch, rank-five primitive
   Omega packet, and has no selected physical midpoint-word landing.
3. Treating `02 -> 44` as a simplicial degeneracy cannot help.  In normalized
   chains

   \[
   d(001)=01-01+00=0,                                  \tag{7}
   \]

   so a degenerate cell has zero normalized augmentation.  A nondegenerate
   cell such as `012` retains all three proper faces, which is exactly the
   endpoint/Omega issue in (6).

Consequently (1)--(5) give an exact occurrence-level theorem and a very
specific source target, but not `d_fixed` or `d_pair`.  The smallest missing
object is a **nondegenerate source-labelled product-rule/third-Bianchi cell**
in the canonical repeated `P3+K2` grade whose endpoint/Omega and anchor faces
are capped, leaving protected-zero labelled ordinary residue in the fixed
and paired directions (2)--(3).

Gate I remains open at precisely that source-lifting statement.
