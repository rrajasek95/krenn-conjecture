# The two lower target normals have a minimal sigma-covariant Cartan–Spencer cone

The (h=2) diagonal identity

\[
 J_*=(\beta-\alpha)J_1+(\beta+\alpha)J_2
     =-2\alpha\beta I                                  \tag{1}
\]

does construct the target-bearing part of the missing even orbit on
`alpha*beta != 0`.  Together with the canonical reduced-Eq Koszul cell, it
closes the target and root-Eq faces of both lower cuts in the derived
target/Eq cone.  The remaining physical descent is smaller and agrees with
the interface isolated in `b6ee603`.

Checker:

```text
computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py
```

## 1. Minimal target/Eq cone

Let (N_{23}) and (N_{45}) be the primitive mixed-target normals of the
exact `B-4` preimages in

```text
0112 with q23:21 reinsertion,
0121 with q45:12 reinsertion.
```

They are exchanged by the physical word stabilizer

\[
                       \sigma=(2\ 5)(3\ 4).             \tag{2}
\]

For either cut (c), retain the two rows

```text
target, reduced Eq=(H0-u)Eq.
```

The lower endpoint path, normalized even (J_*)-Cartan cone, and
root-decorated Koszul/Spencer face have columns

\[
 \begin{array}{c|cc}
                  &\mathrm{target}&\mathrm{Eq}\\ \hline
 B_c              & N_c&0\\
 C_{2,+}(J_*)     &-N_c&-N_c\\
 K_{\rm Eq,c}     &0&+N_c.
 \end{array}                                             \tag{3}
\]

Their sum is zero.  The three columns have rank two and every proper pair
also has rank two.  Hence (3) is the minimal target/Eq totalization: the
target-bearing (J_*) term and the Spencer term are both necessary.

Across the two cuts, the six columns have rank four and a two-dimensional
relation space, one relation per object.  Equation (2) exchanges those two
relations.  Thus they form one sigma-covariant two-object orbit rather than
two unrelated constructions.

The normalization is uniform.  At order (h=2,3),

\[
 J_*^{(h)}=-h\alpha\beta I,
 \qquad
 {J_*^{(h)}\over h^2\alpha\beta}=-{I\over h}.          \tag{4}
\]

The intrinsic (P_h) factor (h) and evenization factor two make the
target coefficient (-2) at both orders.  Thus the (h=2) cone is exactly
the lower restriction of the generic (C_+) target/Spencer architecture.

## 2. Actual residual after the cone

The construction (3) kills

```text
mixed target        0,
root reduced Eq     0.
```

It does not remove three distinct source-labelled remainders.

First, in the complete six-output module, the known literal realization is
tied:

\[
       (\mathrm{lower},\mathrm{Eq})=(\delta_+,\delta_+),
\]

whereas the required bridge is ((\delta_+,0)).  Therefore the exact
complete-Eq remainder is

\[
                         \boxed{(0,-\delta_+)}.          \tag{5}
\]

For (D_6=4\delta_+=(-1,2,-1,-1,2,-1)), the private-minus-Eq covector
reads `12` on the integral form of (5).

Second, the full physical interface prescribes the labelled
ordinary-residue class

\[
                         \boxed{v={B_1+B_4\over2}}.      \tag{6}
\]

The primitive covector

\[
                  (0,1,-1,0,1,-1)
\]

kills the committed diagonal scalar residue and old Cartan residue lines
and reads one on (v).  This is a sharp quotient guard, not yet the computed
residue of the new even cone: the termwise ordinary residue of the even
(J_*)-Cartan cell is undefined before (P_2) places it in the lower source
object.  The Spencer face has zero ordinary residue.

Third, the formal cone is based at the diagonal identity-cap object.  Its
two physical restrictions must instead land in the two displayed lower
words.  Those objectwise word coordinates have rank two modulo the
diagonal word.  Sigma exchanges them, so their invariant sum is one orbit
line, but a physical two-object comparison must still contain both
restrictions.  The pinned old formal totalization hits neither midpoint
word.

There is a further augmentation visible only before forgetting the four
root words.  Put

\[
             E=2D_{\rm root}\otimes v.
\]

The clean derived Spencer cell has only `Eq=+E`.  Its nearest checked
physical cap/response dressing is instead

```text
(lower/private, Eq, W, target, word-resolved ores, anchor)
       =(+E,          +E, 0, 0,      -E,                0).
```

Thus physical dressing leaves the exact debt

\[
             (\operatorname{lower/private},\operatorname{ores}_{word})
                         =(+E,-E),                       \tag{7a}
\]

and the raw target-bearing `C+` cell must contain hidden faces `(-E,+E)`
to cancel it.  Both components vanish after summing the four root words, so
the six-label quotient alone cannot see (7a).  Also, the actual local source
grades span `B0,B2,B3,B5`, while (v) lies in the fixed plane `B1,B4`;
root decoration preserves matching/repeated-edge labels and cannot repair
that placement.

Thus the exact/forced coarse residual interface is

\[
 \boxed{
 (\mathrm{complete\ Eq},\operatorname{ores},\mathrm{word})
 =(-\delta_+,v,\{0112/q23,0121/q45\}).}                 \tag{7}
\]

At full root-word resolution, (7a) must be appended.

## 3. The remaining Hasse face

For each object the exact formal Cartan remainder is

\[
 R_{2,+}=-{1\over2}(1+S)H_wd(P_2(I)),                  \tag{8}
\]

together with the occurrence-local one-endpoint product-rule face of the
lower `B` path.  Formula (8) is exact, but its literal word/fine/repeated
value remains undefined before (P_2) is constructed.  Cartan naturality
cannot define a comparison between source objects that are not already
joined.

Consequently this result constructs the derived output-side target/Eq mapping cone,
not the full physical `iota`.  The remaining object is one source-labelled
sigma-covariant (P_2/K_{\rm Eq}) descent carrying (5), (6), the two word
faces, the hidden `(-E,+E)` dressing faces, their Hasse cross terms, and the
already prescribed protected/ridge rows.

## 4. Comparison with `b6ee603`

Commit `b6ee603` computed

\[
 v={B_1+B_4\over2},\qquad
 \ell={B_0+B_2+B_3+B_5\over4},\qquad
 \delta_+=v-\ell.                                      \tag{9}
\]

The cone calculation sharpens rather than changes that result:

- its mixed target and root Spencer faces are supplied by (3);
- its complete Eq correction is exactly (5);
- its required labelled residue is exactly (6), while its value on the
  unplaced even cone is not yet defined; and
- its missing physical descent is precisely the two-object word/Hasse map
  (P_2).

The word-resolved dressing gate adds information which `b6ee603` necessarily
forgets: the coarse-dark private/residue pair (7a).  Hence `b6ee603` is
correct on the six-output quotient but is not by itself a complete physical
augmentation theorem.

So no additional target generator is needed.  What remains is one augmented
source comparison orbit.  Until it is constructed, the literal Hasse value
cannot be inferred from the closed target/Eq triangle.

Run:

```text
python3 computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py
python3 -O computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py
python3 -I -S computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py
```

Pinned ledger SHA-256: `db0ba608a436c18c0b7fd9a14acfe37aa6d48aafe1171346dec3377c30da940e`.
