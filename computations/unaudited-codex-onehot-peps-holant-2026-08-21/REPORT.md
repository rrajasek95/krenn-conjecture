# One-hot PEPS/Holant canonical-form audit

Status: **exact bounded negative PASS**.  The fixed one-hot projector has a
large local stabilizer, but its entire `18`-dimensional unipotent radical
leaves the literal Krenn bond family.  Intersecting with the bond family and
the fixed GHZ target recovers only the already-known site-colour torus `T0`
and common colour permutations.  Neither the PEPS fundamental theorem nor
Holant clone theory applies to equality on the single fixed `K8` contraction.

## 1. Source-faithful tensor-network encoding

Let `E=C e0 + V`, `dim V=3`, where `e0` is vacuum.  On the seven labelled
virtual legs at a site define

```text
P(x_1,...,x_7)
  = sum_k (product_(l!=k) phi(x_l)) pi(x_k),
```

where `phi(alpha e0+v)=alpha` and `pi(alpha e0+v)=v`.  Thus `P` accepts
exactly one nonvacuum input and outputs its colour.  It has rank `3` and
kernel dimension

```text
4^7-3 = 16381.
```

On edge `ij`, use

```text
b_A = |00> + sum_(a,b=0)^2 A_ij[a,b]|a+1,b+1>.
```

Contracting the 28 bonds with eight copies of `P` is exactly the Krenn
hafnian tensor: a surviving virtual configuration chooses exactly one live
edge at every site, hence a perfect matching, and its endpoint colours give
the physical word.

## 2. Exact local stabilizer of `P`

Write a general `g_k in GL(E)` in vacuum/nonvacuum blocks.  The full
stabilizer inside `GL4^7 x GL3` is

```text
g_k = a_k [ 1  0 ],       a_k != 0,
            [ w_k C ]

sum_k w_k = 0,            C in GL3 common to all seven legs,
h = ((product_k a_k) C)^(-1).
```

Indeed,

```text
P(g_1x_1,...,g_7x_7)
 = (product_k a_k)[(sum_k w_k) product_l phi(x_l) + C P(x_1,...,x_7)].
```

The sum-zero condition removes the all-vacuum term and `h` removes the
remaining common factor.

For completeness, this is the full group, not just a subgroup.  A slice of
`P` by a vector in the nonvacuum hyperplane `V` is decomposable, whereas a
slice with nonzero vacuum component contains the six-leg one-excitation
tensor and is not decomposable.  Every stabilizer therefore preserves `V`,
so the upper-right block is zero.  Evaluating on zero and one excitation
then forces respectively `sum w_k=0` and a common quotient
`g_k|_V/a_k=C`.

Consequently

```text
Stab(P) = Ga^18 semidirect ((Gm)^7 x GL3),
dim Stab(P) = 18+7+9 = 34.
```

Permuting the seven legs gives an external `S7` normalizer if leg
permutations are admitted; it is not part of `GL4^7 x GL3`.

The checker independently linearizes all excitation-zero, -one, and -two
basis inputs.  There are `121=7*16+9` infinitesimal variables and exact
constraint rank `87`, leaving dimension `34`.  Three or more excitations
cannot contribute to the linearization.  It also evaluates one nontrivial
rational group element on all `4^7=16384` input basis tuples.

## 3. Induced bond action and collapse to `T0`

For half-edge parameters `w_ij,w_ji`, the bond action is

```text
b_A -> a_ij a_ji[
    |00> + |w_ij,0> + |0,w_ji> + |w_ij,w_ji>
    + (C_i tensor C_j)A_ij].
```

The literal bond slice is

```text
S_pair = C|00> + V tensor V.
```

Its one-sided summands `V tensor e0` and `e0 tensor V` are independent, so
the transformed bond lies in `S_pair` iff

```text
w_ij=w_ji=0.
```

Thus none of the unipotent radical acts on the Krenn parameter space.  After
normalizing the vacuum coefficient, the reductive action is only

```text
A_ij -> (C_i tensor C_j) A_ij;
```

the half-edge scalars act trivially on normalized `A` and cancel against the
physical site scalars.

The exact Lie stabilizer of `Delta_(8,3)` inside `GL3^8` has dimension `21`.
The full group consists of sitewise diagonal matrices satisfying the three
colour product-one equations, semidirect a common `S3` colour permutation.
Therefore the target-preserving restricted bond action is exactly

```text
T0 semidirect S3,
```

with no new continuous gauge beyond the frozen `T0` action.

An explicit unipotent control takes `w` on one leg, `-w` on a second, and
zero on the other five.  It fixes `P`, but sends two vacuum bonds to

```text
|00>+|w,0>,        |00>-|w,0>.
```

Their one-sided local outputs cancel.  This is a genuine PEPS gauge motion
and an explicit witness that the full canonical orbit has left finite
one-hot Krenn membership.

## 4. Exact PEPS theorem scope

Acuaviva--Makam--Nieuwboer--Pérez-García--Sittner--Walter--Witteveen,
*The minimal canonical form of a tensor network*, arXiv:2209.14358, proves
for a **uniform** PEPS tensor that common minimal canonical form is
equivalent to intersection of reductive gauge-orbit closures, and in turn to
equality of the induced states on **every allowed contraction graph**.  The
paper explicitly uses all contraction graphs, rather than one periodic
geometry, to obtain its fundamental theorem.

The present problem misses the load-bearing hypotheses:

1. only the one fixed `K8` contraction is known to equal GHZ;
2. the 28 bond tensors are edge-dependent, and absorbing them into sites
   destroys uniformity;
3. `P` is extremely noninjective, so injective/normal PEPS fundamental
   theorems do not apply;
4. the general minimal form uses orbit closure, which retains precisely the
   border/ghost identifications already known to be dangerous;
5. the full local orbit leaves `S_pair` through its unipotent radical.

There is an exact fixed-geometry noninjectivity control even at nonzero
output.  Let

```text
M={01,23,45,67}
```

carry colour-zero unit entries and let every other block vanish.  Add the
extra colour-zero chord `02`.  Among all `105` perfect matchings, both
supports contain only `M`, so both sources output exactly `e_0^tensor8`.
They are not related by the restricted invertible bond gauge: the entire
`02` block is zero before and nonzero after.  A single fixed contraction
therefore cannot support a PEPS fundamental-theorem conclusion.

## 5. Restricted one-hot Holant verdict

The smallest source-faithful invariant is the paired-excitation grading.  If

```text
N=diag(0,1,1,1),
```

then every literal bond obeys the degree-one linear equation

```text
(N tensor I - I tensor N)b_A = 0.                 (* )
```

The kernel of this operator is exactly `C|00> + V tensor V`.  Together with
the excitation-one support of `P`, equation `(*)` is precisely what makes
every live configuration a perfect matching.  It is preserved by the
block-diagonal reductive action and violated by every nonzero stabilizer
unipotent.  This failure is desirable: a full PEPS/Holant-gauge invariant
would already have forgotten literal paired incidence.

Backens--Goldberg, *Holant clones and the approximability of conservative
Holant problems*, arXiv:1811.00817, studies closure under arbitrary tensor
products, contractions/gadgets, permutations, and, in the conservative
classification, arbitrary unary functions.  Its detailed classification is
Boolean, whereas the present virtual domain has size four and an open
three-state physical leg.  More fundamentally, arbitrary gadget closure
allows auxiliary/internal sites and repeated signatures.  Equality on one
fixed open `K8` network is neither clone equality nor Holant
indistinguishability on all signature grids.

If internal gadgets are forbidden and each labelled `P` must occur exactly
once on the prescribed `K8`, the remaining typed “clone” has no substantive
composition beyond disjoint tensoring, relabelling, and edge specialization;
its evaluation is the original hafnian moment map.  Restoring arbitrary
contractions gives the ordinary matching-gadget category and loses the
fixed-geometry finite-membership condition.

## Terminal verdict

No canonical block decomposition or clean cap follows.  The exact local
symmetry explains the failure: the only new part is unipotent and creates
forbidden half-edge monomers; after enforcing the source-faithful paired
grading `(*)`, the action collapses to `T0 semidirect S3`.  PEPS and Holant
canonical/clone theorems require all geometries or gadget closure and cannot
turn the single `K8` GHZ equality into gauge equivalence.

## Replay

```sh
python3 computations/unaudited-codex-onehot-peps-holant-2026-08-21/audit_onehot_peps_holant.py --write-results
python3 -O computations/unaudited-codex-onehot-peps-holant-2026-08-21/audit_onehot_peps_holant.py
python3 -I -S computations/unaudited-codex-onehot-peps-holant-2026-08-21/audit_onehot_peps_holant.py
```

All modes print logical SHA-256

```text
6130619bd6a1c8efdebb17ca47f7db98582e128cc332070dbc340083bf7442b5
```
