# The marked derived cap does not yet bypass the physical PAComp map

The fine-marked Beck--Chevalley object

\[
N=\Delta ^5\times\Delta ^1\longrightarrow V_{\rm parent}
\]

is a genuine derived replacement for the response simplex over each of the
90 parent matchings.  For both labelled roots its comparison cone is
acyclic.  Acyclicity is stronger than the constructive branch needs: after
the normalization `t=H0-u=0`, the evident coefficient map
`Response -> N -> B` is already a chain map and sends the selected parent
coefficient to the `B` top.  Its extra Eq cokernel is therefore **not** an
obstruction to this coefficient map.  The actual failure is that the map has
no physical response-to-cap operation/word section, hence does not transport
the selected `P_f` and `q` faces.  Even if that section is granted, the first
proper-face map has the exact word-rank defect `0 -> 2` described below.

The executable certificate is
[`verify_h3_derived_marked_cap_direct_pacomp_schreyer_eq_gate.py`](../computations/verify_h3_derived_marked_cap_direct_pacomp_schreyer_eq_gate.py).

## Exact local complex

For one parent and one root the cone of
`Delta5 -> Delta5 x Delta1` has dimensions

\[
(12,42,70,70,42,14,2)
\]

and boundary ranks

\[
(12,30,40,30,12,2),
\]

so all its homology groups vanish.  Scaling by 90 parents and two distinct
root sections and retaining one global protected Eq coordinate gives

\[
\dim C=(2161,7560,12600,12600,7560,2520,360),
\]

\[
\operatorname{rank}d=(2160,5400,7200,5400,2160,360),
\qquad \dim H=(1,0,0,0,0,0,0).
\]

Thus the marked derived comparison is completely understood.  The lone Eq
coordinate is an undecided protected class, not an assumed absolute cell.

## The normalized selected composite, without a quasi-isomorphism demand

At `t=0`, the one-dimensional top coefficient is literally

```text
selected response --1--> marked N --1--> B.
```

The strict marked bijection retains the `AB/AC` root, parent matching and
missing-site/fine mark.  Thus the composite really does hit the selected
`B` coefficient.  No essential-surjectivity or acyclic-cone hypothesis is
needed for this statement, and the surviving Eq cokernel belongs to the
later terminal-promotion problem.

Embed this coefficient map in the literal root-section coordinates

```text
(id_response, id_cap, Hom(response,cap), response_word, cap_word).
```

Its canonical coefficient-only extension has zero `Hom(response,cap)`
coordinate.  A physical section has coordinates `(0,0,1,-1,1)`.  The
primitive covector `(0,0,1,0,0)` therefore kills the proposed composite and
reads one on the required physical section, independently for the two
roots.  This is the first failure of the map itself.  Equivalently, the
abstract equality “selected coefficient maps to `B`” does not produce an
element of the physical corner `e_C A e_R`, so it proves no chain identity
for `P_f` or the `q` faces.

If this operation/word section is conditionally adjoined, the top image and
the root/parent/fine tags pass.  The next failure is then the P2 rank
`0 -> 2`, followed by the forced `0102/dq` and hidden `(-E,+E)` faces.  This
separates the two remaining questions cleanly:

- constructive filler: operation/word/`P_f`/`q` compatibility, which fails
  before the Eq cokernel is consulted;
- terminal promotion: whether the one protected Eq cokernel is filled or
  supports the exhaustive dual, which matters only after the constructive
  physical map exists.

## End-to-end PAComp chase

The stages separate as follows.

| stage | status on `N` | exact reason |
|---|---|---|
| marked response-to-cap comparison | proved | the fine-marked correspondence is a strict bijection and its cone is acyclic |
| derived target/nonzero | defined after target augmentation | target is constant on the two `Delta1` endpoints and kills simplicial boundaries |
| physical active cap | not supplied | this needs a pointed `R`-linear map `ev_cap:N -> Cap_phys(A;p,q)` which reflects nonvanishing |
| private-site identity | not defined | `N` has parent labels but not the cells, multiplication, cofactors, or evaluation occurring in `p_u G_mixed-q_u G_pure=q_u+sum_s Delta_us C_s` |
| four-good/coloop split | not reached | its input is a nonzero physical determinant/cofactor fan and actual pure supports, not a homology class of a parent resolution |
| `P2 -> 0102 -> dq/Q/ores/ridge` | exact second failure, even after granting a physical realization | the derived cap's universal `q` face stays in the diagonal cap word: image rank 0 versus the two required `q23` and `q45` word summands, rank 2 |
| `N -> N-2` reconstruction | not defined | clean descent contracts an actual covector `K` with `H_B(A)` and outputs actual reduced weights; no such contraction functor is defined on `N` |

This identifies two different senses of “active.”  The statement
`target([n])=1` is well-defined on the derived resolution.  The active cap
used by PAComp is an actual covector satisfying the target-augmented source
identities.  The former does not imply the latter without `ev_cap`.

## Strongest generous grant and the first exact chain defect

Assign every marked vertex its parent augmentation, impose tied `B=Eq`, and
adjoin the target cone.  This closes both target normals and all
coefficient/common-parent columns.  It still supplies no occurrence-local
restriction from the diagonal `01211222` cap face to the two physical P2
objects

\[
0112/q23:21,\qquad 0121/q45:12.
\]

In their three word coordinates the source is `(1,0,0)` and the desired
targets are `(0,1,0)` and `(0,0,1)`.  The two coordinate covectors therefore
annihilate all old `N` columns and detect the two required images.  This is
the literal rank `0 -> 2` obstruction.

If those maps are granted, their first product rule already forces the
12-term `0102` `dq23` vector.  It has augmentation and ordinary residue zero,
but the detector `+e0+e3-e1-e6` reads `35/72`.  At the protected landing,
termwise `N` gives `(delta_plus,delta_plus)` while the physical output is
`(delta_plus,0)`.  With

\[
d_6=(-1,2,-1,-1,2,-1),\qquad \delta_+=d_6/4,
\]

the integral covector `(d6,-d6)` kills tied `N` and reads `3` on the required
`B`-only column.  The accompanying hidden proper faces are precisely
`lower/private=-E` and `word-resolved ores=+E`.

## What would make a derived bypass valid

An absolute underived Eq filler is not the only logically possible route.
A derived PAComp theorem would suffice if it constructed a pointed
`R`-linear realization `ev_cap` of `N` which is natural for:

1. official EqSystem multiplication and the private-site contraction;
2. both P2 restrictions and all `q/dq/ores/ridge` product-rule faces; and
3. clean-cap contraction and `N -> N-2` reconstruction;

and if it reflected target activity/nonvanishing on `H0` while proving that
the protected Eq summand vanishes conservatively on actual solutions.  This
is an exact substitute for the absolute cell, not a consequence of the
present Beck--Chevalley equivalence.

The smallest next datum is therefore one source-derived occurrence-local
restriction from the marked `q` faces of `N` to both P2 word objects, with
the forced `dq23/dq45` jets and the `(-E,+E)` hidden faces.  Its complete
`B/Eq` value decides the remaining fork.

## Why a native Schreyer calculation cannot decide the fork

The official EqSystem has 252 variables, 6561 relations, and 105 matching
terms per relation.  Its selected squarefree coefficient block has 48
divisor/complement slots; the six Boolean resolutions have boundary ranks
`(6,12,6)`.  Higher Schreyer cells resolve kernels but cannot enlarge the
degree-one image.

More importantly, protected `B/Eq` does not descend to the native module.
For `delta=(1,1,-1,-1)`, the lifts `(delta,0)` and `(0,delta)` have the same
native image under `(b,e) -> b+e`, while normalized omega reads `+1` and
`-1`.  Their difference is a native-kernel vector on which omega reads `2`.
Consequently a multigraded Schreyer resolution of the original EqSystem
cannot choose between an Eq boundary and an Eq dual.  The minimum additional
input is a source-derived protected jet/operation enrichment complete on
this forgetful kernel.
