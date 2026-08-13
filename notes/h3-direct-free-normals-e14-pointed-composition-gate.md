# The direct-free normal quotient reaches E14 only after the pointed Eq/word comparison

## Outcome

At the direct-free support `x12=a, x14=b`, the five denominator cofactors
have Jacobian rank three.  The normal quotient is exactly

\[
                 \langle h_1,\;a h_2-b h_4\rangle .       \tag{1}
\]

Every leading monomial in (1), after removing its supported coefficient
`a` or `b`, is a two-edge matching.  In particular

\[
                 x_{23}^{21}x_{45}^{12}                 \tag{2}
\]

is the decorated `2K2` core already identified with
`u05_01*v34_10` in the canonical E14 unary row.  This is a real core-level
hit.  It is not yet a source-valid map of the whole normal quotient.

The complete shifted Hasse/chart filler is linear in the deleted-face
coefficient `L`.  It gives, in the indexed derived presentation,

```text
d n_L = L*Y*w,       target(n_L)=ores(n_L)=0,
chart face = the corresponding combination of -S_v.
```

On diagonal projection to the underived physical source its first residual
is instead

\[
             \boxed{L(H_0-u)e_{\rm Eq}}.                \tag{3}
\]

Both choices in (1) give nonzero instances of (3).  Thus the first literal
hidden row is the Eq coordinate, before any E14 unit theorem can be used.
Even if (3) is killed by a pointed reduced-Eq comparison, the physical
source word `01211222` (internal word `12112`) still has to be transported
to the canonical E14 word/grade based at `000101`.  The known E14 theorems
terminalize a two- or three-new-cell support *already placed* in that chart;
they do not construct this placement arrow.

The companion checker is
[verify_h3_direct_free_normals_e14_pointed_composition_gate.py](../computations/verify_h3_direct_free_normals_e14_pointed_composition_gate.py).

## 1. The two exact normal classes

The first class is

\[
h_1=x_{23}x_{45}+x_{24}x_{35}+x_{25}x_{34}.             \tag{4}
\]

With the word decorations from `12112`, its three terms have colour pairs
`(21,12)`, `(21,12)`, and `(22,11)`.  The second class is

\[
 a h_2-bh_4=
 a x_{13}x_{45}+a x_{15}x_{34}
 -b x_{13}x_{25}-b x_{15}x_{23}.                       \tag{5}
\]

The common `x35` tangent cancels in (5).  Every displayed term therefore
begins with two new matching cells.  This explains why the E14 two-cell
census is the right *terminal* theorem once a comparison has placed the
class in a canonical E14 chart.

It does not provide that comparison.  Equation (2) is the one decorated
core for which the existing relabelling is literal.  The full Hasse cell
has its own word, repeated grade, product-rule faces, and chart readout.
Polynomial multiplication by the private E14 multiplier changes polynomial
degree but not the source-row label.

## 2. The order of the obstructions

There are two successive gates.

1. **Underived Eq descent.**  The derived Hasse totalization cancels all
   Boolean product-rule faces.  Forgetting the indexed faces leaves (3).
   Specializing `H0=0,u=1` and one monomial of either (4) or (5) to one
   makes its Eq coefficient `-1`, so it is not a formal zero.
2. **Word/fine/repeated-grade placement.**  After a hypothetical correction
   of (3), the normal row and the E14 unary row are still distinct direct
   summands.  The coordinate covector on word `01211222` kills the E14
   `000101` summand and detects the normal row.  This is a presentation
   separator, not a physical terminal: a new source-valid word/grade arrow
   is precisely allowed to kill it.

The physical `M_v` column solves the odd **output** Eq dressing on the
canonical rootless word, but its input equality

\[
                    J_3(M_v)=A J_{\rm col}(\ell)        \tag{6}
\]

and physical `q` transport are still open.  The universal graph
construction supplies the unaugmented Koszul Eq cone, but its first pointed
row is `d(u_f-u)`.  These are two presentations of the missing pointed
comparison, not two completed routes around it.

## 3. Why composing the derived lift with an old Eq cone does not make the cap

Use normalized rows

```text
(Q-boundary, target, ordinary residue, Eq).
```

Then the invisible shifted lift and primitive cap have

```text
n = (+1,0, 0,0),
p = (-1,0,-1,0),
n+p=(0,0,-1,0).
```

Every currently available reduced-Eq correction relevant here has ordinary
residue zero.  Therefore the ordinary-residue coordinate annihilates the
span of `n` and all those corrections, but reads `-1` on `p`.  In
particular, a reduced-Eq cone may cancel the underived commutator (3), but
it cannot by itself construct

\[
                    p=(-Q,-\operatorname {ores}).       \tag{7}
\]

The smallest missing column is one source-labelled residue section (7) in
the same word/ridge/repeated grade, included in the same pointed comparison
that supplies (6) or `d(u_f-u)`.  Thus the projected primitive cap and the
pointed Eq lift are two domain generators of one enriched comparison
theorem, not two independent conjecture-level theorems.

## 4. Four-cut composition and the first weighted face

The same enriched comparison is a plausible common-carrier construction.
The two ordered curvature factors satisfy

\[
 (q-x)+(q-r+x)=2q-r.                                   \tag{8}
\]

If the pointed endpoint family has two source-valid orientation projections
landing on one augmented carrier `H0`, then either one projection is
nonzero and gives the active-clean exit, or both vanish and (8) gives

\[
                         (r-2q)H_0=0.                  \tag{9}
\]

This remains conditional because the primitive cap presently lives at
intrinsic order three in word `01211222`, repeated grade `P3+K2`, whereas
the four-cut statement requires an all-label restriction--insertion map
for both orientations.  No committed word/grade map supplies those two
projections.

Nor is `c1` automatically the first beta face.  The endpoint projector
remembers the unweighted base augmentation.  The based loop
`phi(t)=2t-1` has

\[
                   \int_0^1\phi(t)dt=0,
 \qquad            \int_0^1t\phi(t)dt={1\over6}.       \tag{10}
\]

Hence unweighted endpoint data do not determine the first weighted moment.
Identifying `c1` with a beta/Hasse face additionally requires a filtered
comparison identifying beta with the affine carrier parameter and a
source-valid horizontal one-form with zero based-loop residue.

### The strongest one-`R`-generator attempt

There is no abstract obstruction to *packaging* the cap and first moment in
one free `R=k[beta]` generator with boundary

\[
                            dG=p+\beta c_1.             \tag{11}
\]

Work to first order over `R/(beta^2)` in the basis

```text
(p, beta*p, c1, beta*c1).
```

The `R`-span of (11) has columns

```text
(1,0,0,1), (0,1,0,0).
```

This is a legitimate formal face/Bockstein package.  However, its image
contains neither `(1,0,0,0)=p` nor
`(0,0,0,1)=beta*c1` separately.  The primitive anti-diagonal covector

\[
                            (1,0,0,-1)                 \tag{12}
\]

annihilates the whole rank-one `R` image and detects their difference.
Before attachment, the two independent face covectors are the cap/residue
readout `epsilon_p=(1,0,0,0)` and the based-loop first-moment readout
`mu_1=(0,0,0,1)`.

Thus one `R` generator can exhibit `c1` as the beta face of a chosen cap
lift, but it only imposes `p=-beta*c1`; it does not make the unweighted cap
and weighted moment individual boundaries.  If the proof needs both
relations separately, a second filtered domain cell is necessary in the
current two-grade quotient.  This
does **not** split the proof into two conjecture-level theorems: both cells
can, and should, be packaged in one enriched pointed comparison family.
The conclusion is conditional on retaining the two readouts in the complete
physical quotient; the existing cap-residue and based-loop calculations
prove their independence in the present candidate module, not yet a global
physical terminal statement.

## Verification

Run the checker normally, with optimization, and in isolated/no-site mode.
It pins the shifted Hasse filler, direct-free two-class quotient, E14 core
hit, the physical odd Eq output scope, universal pointed obstruction,
primitive cap gate, and the oriented four-cut comparison.  Frozen ledger
SHA-256:

```text
e86a1b4cea037a233d80c22f29895fa7ee7f028c79d59bb6ab9b1d69f9f844d1
```
