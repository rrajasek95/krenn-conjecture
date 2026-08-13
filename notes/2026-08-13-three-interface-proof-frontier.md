# Proof frontier: three physical interfaces

Audit date: 2026-08-13.

This is the shortest honest proof sketch after the selected-lower,
trapped-carrier, and inactive-Rees reductions.  It is a programme, not a
claim that the conjecture is proved.  The point of the sketch is that the
remaining work is no longer a large support classification.  The universal
matching, Hasse, Weyl, Cartan, and Fredholm algebra is already in place.  The
open work is descent through three physically labelled interfaces.

## 1. Global skeleton

Start with a minimal counterexample, normalized by maximum protected mutual
anchors and then minimum occupied scalar support.  The established clean-line
gcd split gives the exhaustive fork

```text
minimal counterexample
        |
        +-- active carrier ----------------> endpoint accessibility
        |
        +-- rootless collision ------------> odd Spencer comparison
        |
        `-- all roots inactive ------------> even/Rees comparison
```

Every successful branch ends in one of four already accepted terminal
outputs:

```text
ordinary source unit,
anchor-safe support deletion,
four-good active pair followed by clean-cap descent,
physical relative generator or Fredholm separator.
```

The remaining proofs must therefore construct the arrows in this diagram;
they do not need new terminal mechanisms.

### The common comparison theorem behind the three arrows

The three arrows should not be proved as unrelated coefficient chases.
They are three symmetry sectors of one augmented descent problem.  Let
`C_sym` be the source-valid principal-parts/Cartan/product-rule complex
before the fixed word, collision label, and physical readouts are imposed,
and let `C_phys` be the complete labelled physical source complex augmented
by target, ordinary residue, anchor incidence, and `W`.  The desired master
statement is:

> **Augmented physical comparison.**  On the two-root/one-collision sector,
> the comparison cone from `C_sym` to `C_phys` has no terminal-dark first
> homology.  Equivalently, every protected comparison defect is either a
> physical boundary or is detected by one of the already terminal physical
> readouts.

Its three isotypic pieces are precisely:

```text
odd Weyl/sign sector       -> Interface I,
occurrence/anchor sector   -> Interface II,
even divided-power sector  -> Interface III.
```

This formulation gives the shortest plausible proof.  First construct the
symbol-level maps from the Weyl/Cartan and Hasse product rules.  Then descend
them through the fixed fibre using a relative connection/mapping cone,
retaining every physical augmentation row.  Finally compute the small
isotypic cone.  Exactness gives the required physical cell; nonexactness is
paired with the six-term, anchor, residue, or `W` readout and enters the
already proved generator/Fredholm alternative.  This last pairing is
load-bearing: a nonzero occurrence or chart covector is not a physical
terminal merely because it detects the symbol-level cone.

Proving the master statement at once would close all three interfaces.  The
three interface lemmas below are a weaker modular route: each proves exactly
one isotypic piece and is therefore safe to attack independently.

## 2. Interface I: odd labelled Spencer descent

For the selected determinant-dark cut cycle, the complete lower vector is

\[
                    \ell=u_{024}-u_{012}.
\]

It has eighteen direction-labelled terms, fifteen physical collision
labels, twelve nonzero labels, and coefficient zero on the three shared
repeated-`02` labels.  Consequently this selected branch does not require a
map on all fifteen basis vectors.  It requires one complete protected row
identity

\[
                    J_3(M_v)=A J_{\rm col}(\ell).       \tag{I}
\]

The universal source-side picture is exact.  The two 341-term fine
components satisfy `tau Z0=-Z1`; hence their group-bar boundary cancels the
Weyl-paired singleton faces.  Endpoint oddization produces the interference
pattern

\[
 {4\over3}(\xi-\bar\xi-s\xi+s\bar\xi),                 \tag{1}
\]

with signs `+,-,-,+`, and kills the GHZ target defect.  This is the precise
sense in which the remaining cancellation is structural rather than a list
of unrelated monomials.

This source-side cancellation is naturally **orbit-relative**, not a chain
on the fixed GHZ fibre.  The four tail-root directions have independent
nonzero normal values, so the fixed fibre is not root-equivariant.  In the
orbit-relative principal-parts/bar model there is nevertheless a canonical
one-cell `b_xi=(1-s)[tau|Z0]` and a rank-one section of its private face.
Ordinary transport back to the fixed fibre kills the four-corner boundary;
therefore the remaining theorem is an enriched comparison (equivalently a
connection or relative mapping-cone lift), not a stronger ordinary
equivariance statement.

That enriched physical descent is still open.  In the first private degree,

\[
 \xi=q_{01}^{01}q_{27}^{21}q_{34}^{11}q_{35}^{12}q_{67}^{22}
\]

has no `37` edge, while both compatible old complete-row columns have a
forced `q_37` multiplier.  The normalized coordinate covector detects this
failure.  Complete-row Weyl bars do not repair it: the endpoint/bar image
has rank eight and adjoining (1) raises the rank to nine.  The missing
object is therefore the physical comparison image of the canonical
orbit-relative principal-parts/Weyl-bar cell, with its physical
`D/W/anchor/eta/sigma` rows, not another complete-row covariance identity
or an ordinary fixed-fibre quasi-isomorphism.

There are two possible proof styles.

1. Construct that relative cell and verify (I) literally.
2. Put the cell in the exhaustive physical relative complex and use the
   physical six-term readout.  If the obstruction is terminal-visible it
   normalizes to the relative generator; if the readout kills the whole
   relative homology, it descends and the Fredholm separator applies.

The second style is shorter only after the protected complex and physical
readout are defined on the same labelled repeated grade.  A chart or
occurrence covector is not a substitute.

## 3. Interface II: complete endpoint accessibility

Every evaluated determinant-bright zero mixed row supplies an offdiagonal
private-site fan.  Complete pure-target supports make it four-good unless
one fan edge is a literal pure-colour coloop.  The uniform coloop pivot then
produces a pure-target or fine-typed mixed matching omitting the coloop and
lands in one of the six finite Hall closures.

The trapped-carrier question has now reduced to one complete endpoint map.
At fixed common `q` and fixed right endpoint, the physical part is no
longer hypothetical.  The unary derivative in the 36 left-endpoint
coordinates is zero, while the four response blocks form a
`2916 x 36` matrix.  Its generic nonzero entries are the explicit
five-partner/three-matching cofactor sums, so there are 17,496 generic
entries and fifteen common-`q` monomials in each.  Selected anchors are
coordinate-selector borders on this physical response matrix; they are
protection constraints, not automatically extra source equations.

On a support-minimal fibre of the bordered map there are only the following
outcomes:

```text
coordinate access,
an extra response-transverse column (typed rank exit),
an in-span extra column (fundamental anchor-safe dependence),
a selector in the physical response-row span,
or a selector using the protection border only.
```

The first four alternatives are terminal by the existing target-line,
Fitting, deletion, and physical-dual theorems.  Only the last one remains.
Its sharp proof obligation is to append the simultaneous `q`-deformation
columns and compare with the physical six-term readout.  This extension is
now explicit: the domain has 36 endpoint plus 135 decorated-`q` columns;
the unary block has 10,935 generic entries, and the four response blocks
have 43,740.  The anchor border must also be differentiated: a marked
`p*s*q*q` occurrence has one endpoint and two `q` product-rule entries.

Let `A` be this physical map, `H` the full anchor differential, `e` the
support selector, and `Lambda` the physical six-term row.  Exact row-space
duality closes every branch except

\[
             \Lambda\in\operatorname{row}(A),
             \qquad H\notin\operatorname{row}(A).      \tag{II}
\]

Indeed, visibility of `e` on `ker[A;H]` is an anchor-safe exchange;
`e in row(A)` is a physical dual; visibility of `Lambda` on the protected
kernel is the relative generator; and a nonzero `H` coefficient in the
factorization of `Lambda` transports `e` to the physical six-term row.
Thus (II), equivalently the nonzero-anchor-coefficient theorem or a direct
physical realization of `H`, is the sole Interface-II statement left.  A
small rational packet shows that linear algebra alone cannot exclude it.
This is the precise point where Interface II meets Interface I; it is not a
new Hall-incidence case.

No new Hall termination argument is needed: the six-site saturation has
only 446 closed concepts in six symmetry types, and every new typed hole
strictly enlarges closure.

## 4. Interface III: even/Rees descent

The inactive branch is not another copy of Interface I.  Its comparison is
root-even and target-bearing.  On the generic diagonal stratum the unique
input is

\[
 J_*=(\beta-2\alpha)J_1+(\beta+\alpha)J_2,
 \qquad J_*=-h\alpha\beta I.
\]

After normalization, the universal lower source is the parameter-free trace
jet

\[
              -{1\over h}(1+\rho)H_w\,dP(I).           \tag{2}
\]

The physical theorem must do three things simultaneously:

1. carry (2) into the literal diagonal Rees packet;
2. supply the adjacent-power mixed target direction (rank two in the two
   diagonal jet targets); and
3. cancel the reduced-Eq and labelled ordinary-residue debt.

It must be stated as an **augmented** comparison, retaining the physical
`W` row.  This does not introduce a fourth source-generator theorem.  The
existing cap chain

\[
 r_0-T=(\operatorname{Eq}=1,Yw=1,W=1,
        \operatorname{ainc}=-1,\operatorname{tgt}=
        \operatorname{ores}=0)
\]

already supplies the cap and anchor values.  If Interface III constructs
the same-grade repair

\[
 A_v=(-r_v,-\operatorname{Eq},Yw=0,W=0,
       \operatorname{ainc}=\operatorname{tgt}=
       \operatorname{ores}=0),
\]

then `P_v=(r_0-T)+A_v` is the exact physical base with `Yw=W=1`.
Projected equations cannot infer `W(A_v)=0`: replacing `A_v` by `A_v-W`
leaves every other displayed row unchanged but destroys the cap.  Thus
`Yw -> W` is one load-bearing output row of Interface III, not a separate
cell construction.  Rees-linearity propagates this factorization through
normal orders one, two, and three.

Equivariant collapse constructs thirteen of the fifteen labels.  The unique
missing even repair is the fixed direction
`v=(B1+B4)/2`.  The two omitted labels form one `rho`-orbit, so the missing
generic source representation is exactly one-dimensional.  The divided
product rule has coefficient one on it.  Its complete physical column is
nevertheless coupled: in the omitted repeated-`25` grade it must carry

```text
full-nine tail       delta+ = (-1,2,-1,-1,2,-1)/4,
mixed target         -2 D tensor v,
reduced Eq           +2 D (H0-u) Eq tensor v,
labelled residue     v,
plus the forced ridge and word faces,
```

where `D=(-1,1,-1,1)`.  Independent primitive covectors rule out a
tail-only, residue-only, or Eq-only shortcut.  Local C4/Hasse resolution
reaches the correct formal diagonal cross term, but old literal Hasse rows
are site-squarefree and the physical source loop labels collapse to the
same target diagonal.  Thus the remaining generic datum is exactly one
full label-decorated relative product-rule/Bianchi orbit, not several
unrelated cells and not a bare `(B1+B4)/2` section.

The connected local `SL_3`/Weyl action does not construct this orbit.  It
changes root colours but preserves the uncoloured matching multiplier and
repeated-edge labels.  Even after adjoining `rho`, the actual omitted-`25`
packet stays in `<B0,B2,B3,B5>`, while `v` lies in the complementary fixed
plane `<B1,B4>`.  Conversely the formal `B1/B4` product-rule seed stays in
the wrong shared-`02` grade.  Thus Cartan homotopy supplies the word/root
decoration only after the placement exists; it cannot replace the one
relative placement/product-rule orbit.

At `beta=0`, the selected target first appears at order `h`; the branch is
the separate one-dimensional protected membership `1 in theta(Z)`, or its
physical dual.  It should not be folded into the generic argument by calling
the nondegenerate Hasse top a normalized degeneracy.

Once the seed even comparison is source-labelled and Rees-linear, base
change propagates its three coherence equations through every diagonal jet.
No new matching census is required.

## 5. Assembly

The shortest exhaustive proof is:

1. use the clean-line gcd split;
2. close the normalized rootless packet with Interface I and the physical
   generator/Fredholm alternative;
3. route every residual active carrier through Interface II, and compare
   its sole protection-only outcome with the physical readout before using
   the exhaustive relative generator/separator alternative of Interface I;
4. extend the augmented Interface III comparison over the all-inactive
   normal jets; the existing cap chain and its mandatory `W` row then give
   the physical `Yw -> W` base without another generator;
5. apply clean-cap descent and induction to the six-site contradiction.

The independent constructive route replaces steps 2 and 4 by a uniform
entry theorem into the six-site active-fan/collision fork.  At present that
route is not shorter because its global source-connectivity theorem is still
unproved.  The rootless/inactive route is exhaustive already, so it remains
the primary spine; Interface II is the high-value parallel shortcut and
supplies the rank landing needed by either assembly.

## 6. Fastest attacks

The next calculations should be limited to the following.

1. **Odd descent:** construct or separate the enriched comparison carrying
   the canonical orbit-relative bar (1) into the fixed physical augmented
   complex, beginning with the private `xi`/mate pair and typing all
   augmented rows and the physical six-term readout.
2. **Accessibility:** exclude (II)—prove the physical six-term
   factorization has nonzero anchor coefficient, or realize the marked
   anchor differential as a physical row; do not re-enumerate Hall shores.
3. **Even descent:** construct the single root-even product-rule/Bianchi
   cell landing `(B1+B4)/2`, with mixed target, reduced-Eq, and labelled
   residue retained, and keep its physical `W=0` row.
4. **Adversarial check:** in each lane, test the complete protected map, not
   an occurrence shadow, bare tail module, or coarse terminal signature.

Further support enumeration is useful only when it tests one of these three
physical interfaces.
