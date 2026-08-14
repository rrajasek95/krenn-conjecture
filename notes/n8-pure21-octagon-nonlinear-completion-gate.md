# The first nonlinear octagon descends to the cost-two anchor sector

## Outcome

The first cost-three circuit does not become a hidden source completion when
all of its cells are adjoined simultaneously.  Its union support consists of
four new (s_1) ports and eight new colour-two (q)-cells.  There are exactly
32 sign assignments in ({\pm1\}^{12}) realizing the eight prescribed
octagon coefficients.

Every such simultaneous packet activates fifteen pure-(21) paths:

\[
              1\text{ old}+8\text{ octagon}+4\text{ cross}
                    +2\text{ lower-cost}.              \tag{1}
\]

The octagon sum is zero.  If (C) is the four-cross sum and (J) is the
two-cofactor lower-cost sum, then the change in the selected row is

\[
                              \Delta_{21}=C-J.           \tag{2}
\]

Across all 32 sign assignments,

\[
 (C,J,C-J)\in\{(0,2,-2),(4,-2,6),(-4,-2,-2)\}.          \tag{3}
\]

The required change is (+1), so no normalized octagon repairs the old
residue (-1): the final selected value is always (-3) or (5).

The eleven-row Fredholm covector from the additive cost-three audit is not
nonlinearly stable: it disagrees with the selected change on 26 of the 32
packets.  Symbolically it has a 20-monomial defect, and the selected
polynomial is not in the radical of the old mixed-row/anchor ideal even
after localizing at all twelve new cells.  The first defect is the DQ face
(-D c g q_{45}) at word/head (121222;01), fine matching
(67\mid02\mid13\mid45).

The failure on the signed octagon is nevertheless controlled.  The same (J) occurs
with the opposite star label in the pure (22) anchor, and the exact anchor
change is (J=\pm2).  Thus the first nonlinear circuit descends to the
already unit-excluded cost-two cofactor/anchor sector rather than creating a
new completion.

The Laurent certificate below excludes every arbitrary nonzero exact
factorization of this signed octagon vector, not merely sign assignments.
Only the separate selected-row unit census uses (pm1) normalization.  The
note does not classify arbitrary points of the entire twelve-cell torus, the
other two octagons, or simultaneous unions of multiple circuits.

## Simultaneous source support

The first octagon has fixed (p_2)-site (2).  Adjoin

\[
 S_{1,2}\setminus\{5\}=\{z_0,z_1,z_3,z_4\}
\]

at physical colour two, and the eight colour-two internal cells

\[
 q_{01},q_{03},q_{05},q_{14},q_{15},q_{34},q_{35},q_{45}. \tag{4}
\]

The prescribed path values are

\[
\begin{array}{c|r@{\qquad}c|r}
z_0q_{14}q_{35}&1&z_0q_{15}q_{34}&-1\\
z_1q_{03}q_{45}&-1&z_1q_{05}q_{34}&1\\
z_3q_{01}q_{45}&1&z_3q_{05}q_{14}&-1\\
z_4q_{01}q_{35}&-1&z_4q_{03}q_{15}&1.
\end{array}                                               \tag{5}

Exactly 32 of the 4096 sign assignments satisfy (5).  One representative is

\[
\begin{gathered}
z_0=z_1=z_3=z_4=1,\\
q_{01}=q_{05}=q_{34}=q_{45}=1,qquad
q_{03}=q_{14}=q_{15}=q_{35}=-1.
\end{gathered}                                             \tag{6}

All twelve cells in (4) are literal shared source entries.  The full row
replay therefore includes every product among them, not only the eight terms
listed in (5).

## Exact cross-product expansion

Besides the eight circuit terms, simultaneous multiplication creates four
new cost-three paths:

\[
 z_0q_{13}q_{45},\quad z_1q_{04}q_{35},\quad
 z_3q_{04}q_{15},\quad z_4q_{05}q_{13}.                 \tag{7}
\]

Their sum is

\[
 C=z_0q_{13}q_{45}+z_1q_{04}q_{35}
      +z_3q_{04}q_{15}+z_4q_{05}q_{13}.                 \tag{8}
\]

More importantly, the new (q)-cells combine with the old
(S_{1,5}=Y=-1) port to reactivate the two cost-two paths

\[
 62\mid75\mid01\mid34,qquad 62\mid75\mid03\mid14.     \tag{9}
\]

Put

\[
                       J=q_{01}q_{34}+q_{03}q_{14}.     \tag{10}
\]

Their head-(21) contribution is (P_2YJ=-J); their head-(22)
contribution is (P_2S_2J=J).  Adding (5), (7), (9), and the old value
(-1) proves

\[
 [222222]F_{21}=-1+C-J,qquad
 \Delta[222222]F_{22}=J.                               \tag{11}
\]

The checker enumerates all fifteen paths separately and independently
replays every one of the 6561 full word/head rows for all 32 sign packets.
Every full difference vector has exactly 32 nonzero labelled rows.

## Polynomial lower-cost certificate

Two signed pairs in (5) give

\[
 E_1=z_1(q_{03}q_{45}+q_{05}q_{34})=0,
 \qquad
 E_2=z_3(q_{01}q_{45}+q_{05}q_{14})=0.                 \tag{12}
\]

There is a literal polynomial identity

\[
\boxed{\begin{aligned}
2z_1z_3q_{05}q_{01}q_{34}
={}&z_1z_3q_{05}J+z_3q_{01}E_1-z_1q_{03}E_2.
\end{aligned}}                                           \tag{13}
\]

Hence, after saturating by the circuit-unit monomial
(z_1z_3q_{05}q_{01}q_{34}), equations (E_1=E_2=0) force

\[
                         J=2q_{01}q_{34}\ne0            \tag{14}
\]

over characteristic zero.  Equation (13) is the exact descent from the
cost-three octagon to the cost-two anchor class.  It does not rely on the
finite sign census.

For completeness, in the finite Boolean quotient defined by
(x^2=1) for the twelve new cells and the eight equations (5), put

\[
                              D=C-J.
\]

The quotient is a product of 32 copies of (mathbb Q), hence radical, and
the exact census gives

\[
                         (D+2)(D-6)=0.                  \tag{15}

Therefore (D-1) is a unit, with explicit inverse

\[
\boxed{
1={D-3\over15}(D-1)-{1\over15}(D+2)(D-6).}             \tag{16}
\]

This is the normalized Nullstellensatz certificate excluding the required
change (D=1).

## Failure of the additive Fredholm dual

Let (Psi) be the eleven-row covector from the cost-three additive audit.
On the 32 nonlinear packets,

\[
 \Psi(\Delta)\in\{-2,0,2\},
\]

and

\[
 \Delta_{21}-\Psi(\Delta)\in\{-4,-2,0,4,6,8\}.         \tag{17}

Equality survives in only six packets.  Thus (Psi) itself does not extend
over the nonlinear octagon fibre.  This is a real boundary, not a failure to
include the cross terms in the checker.

The robust replacement on this fibre is the lower-cost readout in (11):
the nonlinear debt has a nonzero pure-(22) anchor projection (J).  A
future uniform potential must therefore be filtered and triangular—cost
three may descend to cost two—not a single uncorrected linear covector.

### Exact symbolic defect and localized ideal counterguard

Keep the twelve new cells independent.  The selected row changes by the
fourteen-term polynomial

\[
\begin{aligned}
\Delta F_{222222;21}=P_2(&Yq_{01}q_{34}+Yq_{03}q_{14}
 +fq_{15}z_3+fq_{35}z_1+gq_{05}z_4+gq_{45}z_0\\
 &+q_{01}q_{35}z_4+q_{01}q_{45}z_3
 +q_{03}q_{15}z_4+q_{03}q_{45}z_1\\
 &+q_{05}q_{14}z_3+q_{05}q_{34}z_1
 +q_{14}q_{35}z_0+q_{15}q_{34}z_0).
\end{aligned}                                             \tag{18}
\]

Only two of the old eleven dual rows move, and their prescribed weighted
sum is

\[
\Psi(\Delta)=Dc(gq_{45}+q_{14}q_{35}+q_{15}q_{34})
 +P_1c(gz_4+q_{14}z_3+q_{34}z_1).                        \tag{19}
\]

Thus (\Delta F_{222222;21}-\Psi(\Delta)) has exactly twenty
monomials.  Its first monomial is

\[
 \boxed{-D c g q_{45}:\quad
 (121222;01),\quad\mathrm{DQ},\quad67\mid02\mid13\mid45.} \tag{20}
\]

Here (D=a_{01}) is the old direct head, (c=q_{02}) and (g=q_{13})
are old internal cells, and (q_{45}) is new.  This retains word, head,
operation, and fine-matching provenance.

Let (I) be generated by the eleven row changes used by (\Psi) and the
anchor change (\Delta F_{222222;22}=P_2S_2J).  Normalize all inherited
source entries and take the all-nonzero point

\[
\begin{gathered}
z_0=z_1=z_3=1,\quad z_4=-2,\\
q_{01}=q_{05}=q_{14}=q_{15}=q_{34}=q_{35}=1,\quad
q_{03}=-1,\quad q_{45}=-2.
\end{gathered}                                            \tag{21}
\]

Every generator of (I) is zero there, whereas
(\Delta F_{222222;21}=2).  Consequently the selected polynomial is not in
(\sqrt I), even after saturating by the product of all twelve new cells.
The old path dual therefore has no coefficientwise extension over the whole
simultaneous torus without additional rows.

### General torus scope of the lower-cost descent

The identity (13) is stronger than the sign census but must be read with
the right hypotheses.  In any exact nonzero factorization of the signed
octagon vector, the two path monomials in each signed pair have opposite
common value, so (E_1=E_2=0).  If the anchor row also vanished, then
(J=0), and (13) would make the Laurent unit monomial

\[
                 2z_1z_3q_{05}q_{01}q_{34}              \tag{22}
\]

zero.  This is impossible on the octagon torus in characteristic zero.
Hence every arbitrary nonzero complex factorization of the exact signed
octagon has a nonzero lower-cost anchor projection.  This upgrades the
descent theorem from (pm1) to the full Laurent octagon-factorization locus.

Crucially, (E_1) and (E_2) are pair relations imposed by exact signed-vector
factorization; an exhaustive symbolic replay confirms that neither is a
standalone full residual row after cross products are included.  Therefore
(13) does not exclude every arbitrary point of the twelve-cell torus.  The
counter-witness (21) records that sharp boundary.  The finite Boolean unit
(16) remains a separate, sign-specific statement about the selected value.

## Exact remaining scope

This closes the first octagon support under every cross product and every
(pm1) realization.  The next tests are:

1. repeat the simultaneous expansion for the two mixed DQ/PS octagons;
2. determine whether full-row equations force the signed-pair relations
   away from the exact octagon-factorization locus; and
3. adjoin cells from two octagons at once, including their inter-octagon
   products.

Only a packet surviving (13)--(16) without a lower-cost anchor projection
would be a genuinely new nonlinear counterguard.

## Verification

Run

```text
python computations/verify_n8_pure21_octagon_nonlinear_completion_gate.py
python computations/verify_n8_pure21_octagon_nonlinear_completion_gate.py --mode signs
python computations/verify_n8_pure21_octagon_nonlinear_completion_gate.py --mode paths
python computations/verify_n8_pure21_octagon_nonlinear_completion_gate.py --mode rows
python computations/verify_n8_pure21_octagon_nonlinear_completion_gate.py --mode symbolic
python computations/verify_n8_pure21_octagon_nonlinear_completion_gate.py --mode certificate
```

The dependency-free checker enumerates the sign fibre, expands the fifteen
pure paths, performs 32 full 6561-row replays, evaluates the old Fredholm
dual, expands its symbolic polynomial defect, verifies the localized
counter-witness (21), verifies (13) symbolically, distinguishes its
signed-factorization hypotheses from literal full rows, and checks the
Boolean unit inverse (16) on all points.
