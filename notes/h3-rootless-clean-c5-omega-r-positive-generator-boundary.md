# The clean-C5 comparison needs one new common-companion generator type

## Negative inventory verdict

Grant the reduced-Eq correction, so the five adjacent physical comparison
squares have boundaries

\[
                         C_v-C_{v+1},qquad
                 C_v=t_v\Omega_v-r_v.                 \tag{1}
\]

Their normalized boundary matrix is the oriented incidence matrix of
(C_5).  It has saturated rank four and is killed by the primitive
face-sum covector.  Therefore the aggregate

\[
                            \sum_v C_v                 \tag{2}
\]

is not in the current image.  This remains true after the complete
committed Hasse, PP, collision, full-nine, normal, cap, clean-Tor, and
natural Tate inventories are added: the repeated-inventory audit proves
that every completed target/residue-zero correction cycle has zero
comparison aggregate.

Thus there is no source-labelled chain with (2) and the required
stabilizer readout in the existing inventory.

## The smallest new physical source type

The endpoint bar in one labelled repeated degree is

\[
 B_{v,N}=(-t_v\Omega_v,+Q_{v,N};\operatorname{ores}=1).              \tag{3}
\]

The committed collision calculation has only the factored coarse PP route

\[
                         (-r_v;\operatorname{ores}=1).                \tag{4}
\]

The smallest missing lift is

\[
 \boxed{
 \widetilde P_{v,N}=(-r_v,+Q_{v,N};\operatorname{ores}=1)}.           \tag{5}
\]

It must retain the same matching (N), endpoint word, three cap-shift
slots, chart sector, and repeated (P_3\sqcup K_2) fine degree as (3).
Then the common companion and ordinary residue cancel literally:

\[
 B_{v,N}-\widetilde P_{v,N}
       =-t_v\Omega_v+r_v,                              \tag{6}
\]

with Eq, (W), target, ordinary residue, and anchor incidence all zero.
Equation (5), enhanced by the physical terminal readout below, is the
smallest new generator **type**.  It occurs before any new higher Hasse
order.

## The load-bearing physical readout

The same-labelled companion is necessary but not sufficient.  On the five
target-stabilizer tangents (eta_z), all current (Q_{v,N}) and rootless
readouts vanish, while

\[
 d\Omega_v(\eta_z)=
 \begin{cases}
 -1,&v\ne z,\\
 -1-u_z/t,&v=z.
 \end{cases}                                           \tag{7}
\]

The unique cyclic face-local compensation is (c_v=t-u_v).  Therefore a
physical lift of (5) must induce the rootless terminal values

\[
 r_v(\eta_z)=
 \begin{cases}
 1,&v\ne z,\\
 1+u_z/t,&v=z,
 \end{cases}                                           \tag{8}
\]

and hence

\[
                         \sum_v r_v(\eta_z)=5+u_z/t.  \tag{9}
\]

The strict readouts of the comparison remain

\[
             (W,\operatorname{tgt},\operatorname{ores},
                       \operatorname{ainc})=(0,0,0,0).                \tag{10}
\]

No current PP, normal, cap, full-nine, or Tate column has (8).  This is the
exact positive construction still missing.

## One cyclic homogeneous package

There is a useful distinction between the smallest generator type and a
single cyclic aggregate generator.  Put

\[
 (a,b,c,d,e)=(q_{12},q_{23},q_{34},q_{45},q_{15})
\]

and order the face degrees as

\[
 (g_1,g_3,g_5,g_2,g_4)=(bd,ad,ac,ce,be).              \tag{11}
\]

Their least common multiple is (abcde).  Consequently the first
polynomially homogeneous single cell whose normalized boundary can be (2)
has internal degree five and boundary

\[
 \boxed{
 ace\,C_1+bce\,C_3+bde\,C_5+abd\,C_2+acd\,C_4.}       \tag{12}
\]

After the Laurent C5 normalization, (12) is exactly (sum_vC_v).

The existing degree-five Tor cell is not (12).  Its boundary is

\[
 ceE_0+beE_1+bdE_2+adE_3+acE_4,                       \tag{13}
\]

in the **edge** module, and its next boundary is zero.  It cannot be
relabelled as the vertex aggregate (12).

Over the normalized rational chart, adjoining the all-ones aggregate to a
four-edge spanning tree completes rank five.  Integrally its determinant is
(5), whereas adjoining one vertex has determinant (1).  Thus the
minimal primitive non-equivariant construction is one comparison vertex
(5), followed by the existing edges; (12) is the minimal single cyclic
package requested by the aggregate formulation.

## Exact stopping datum

The current source complex therefore stops at a precise interface:

* earliest new source type: the common-companion (P_3\sqcup K_2) lift
  (5), with the physical readout (8);
* five cyclic copies assemble the aggregate readout (9);
* if packaged as one homogeneous cyclic cell, the first possible degree is
  (abcde), with boundary (12);
* neither the existing degree-five Tor top nor any committed correction
  column supplies it.

This specifies a new physical generator.  It does not construct that
generator or prove an all-resolution impossibility.

Run:

```text
python3 computations/verify_h3_rootless_clean_c5_omega_r_positive_generator_boundary.py
python3 -O computations/verify_h3_rootless_clean_c5_omega_r_positive_generator_boundary.py
python3 -I -S computations/verify_h3_rootless_clean_c5_omega_r_positive_generator_boundary.py
```

Frozen ledger SHA-256:

```text
f8e8b2cb1e6a257158527c8645b169d72864bf6f49c7b4019e83052fa48d090f
```
