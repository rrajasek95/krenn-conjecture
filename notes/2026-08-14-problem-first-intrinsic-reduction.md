# Problem-first intrinsic reduction

## Outcome

The conjecture should be attacked through the actual perfect-matching
coefficient equations, not by treating any particular enriched
`B/Eq/AugP2` presentation as intrinsic.

The exact global target is the following minimal-source trichotomy.

> Let `A` be an exact ternary source chosen first with minimum even order,
> then with the committed maximum-anchor/minimum-support normalization.
> Produce one of:
>
> 1. a literal source-ideal unit or accepted physical Fredholm separator;
> 2. a pair `p,q` and a physical cap covector `K` with
>    `s*kappa_0*kappa_1*kappa_2 != 0` and `E_pq(K)=0`;
> 3. a source-valid deformation or contraction preserving every coefficient
>    equation and strictly reducing the chosen normalization.

The first outcome contradicts exactness.  The second invokes the proved
clean-pair descent and contradicts minimum order (with the six-site theorem
as the endpoint).  The third contradicts the choice of representative.
Thus this one trichotomy closes the conjecture.

`PAComp(h)` is a sufficient implementation of this trichotomy.  It is not
logically the only implementation, and failure to construct one of its
auxiliary operation arrows is not evidence for a polynomial solution.

## Intrinsic data and auxiliary data

The following are intrinsic:

* the endpoint-ordered blocks `A_uv` and all `3^N` coefficient equations;
* pure target normalizations and literal mixed zero rows;
* occupied decorated cells and their word/matching multigrades;
* source-derived multiplication, deletion, reinsertion, polarization and
  Macaulay relations;
* the physical cap quantities `s`, `r`, `kappa_c` and the homogeneous error
  `E_pq(K)`;
* a unit or left-kernel identity evaluated on an actual occurrence-labelled
  source resolution.

The duplicated private-`B` and reduced-`Eq` coordinates, `r0`, `Gamma_*`
operation atoms, mapping cylinders, and chosen HPL splittings are auxiliary
until a literal source map carries them into the coefficient system.  Their
balanced dual can diagnose a missing constructor, but cannot by itself be a
terminal for the original conjecture.

## The first literal packet

The smallest currently exposed intrinsic obstruction is no longer an
abstract chart square.  In the six-site residual window put

```text
M0 = 05|12|34,
M1 = 01|25|34.
```

For either mixed output section `111001` or `111221`, commit `9ab9b48`
constructs the minimum two-row, degree-four Macaulay chain whose selected
face is `M0-M1`.  After the source-valid endpoint-colour deletion, its
boundary is the signed complete 15-matching row:

```text
M0 - M1 + 13 explicitly labelled exits.
```

This is the first object on which the desired parent orientation and the
actual source equations coexist.  Degree three cannot contain the
orientation, and the first common two-word grade still has rank one.  The
next theorem must therefore classify the thirteen exits rather than erase
them by an untyped fold.

The exits have useful physical structure.  Relative to `M0,M1`, nine are a
single `C4` flip from at least one parent and four are primitive `C6`
changes.  With respect to the physical cap at `34`, `M0`, `M1`, and the
third matching `02|15|34` are the three direct terms; the other twelve exits
are its crossed response.  Across the two words the cap colours are `00`
and `22`, while the retained residual word is the same pure `1111`.  Hence
this packet is exactly where a three-colour cap, a pure unit, or a
parent-resolving reduction could first appear.

## A counterguard that is now gone

Commit `00a1d52` gave an abstract three-channel dirty signature which was
compatible with the top GHZ contraction but had no active clean cap.  It
showed that first-derivative and support information alone were
insufficient.

Commit `1412e4d` proves that this signature cannot come from one physical
common edge.  A genuine two-site cap has only boundary degrees zero and two.
For every residual decorated cell its second-response slice is

```text
u*v^T + x*y^T,
```

so its determinant is zero.  The dirty signature requires a nonzero scalar
multiple of a rank-three direct block at three disjoint cells.  The exact
rank classification also rules out ranks two and one; rank zero makes the
cap inactive.  On the guard's fixed internal matching, the physical cap
formula misses all three pure residual rows and yields literal `0=1` units.

This is important evidence for the problem-first route: the first apparent
structural counterexample disappears as soon as the shared-star identities
of actual edge matrices are imposed.

## The next lemma to prove

The highest-value local statement is now:

> **Thirteen-exit lemma.**  In a maximum-anchor/minimum-support exact source,
> every literal realization of the signed degree-four `M0-M1` packet has one
> of the following source-labelled outcomes:
>
> * a mixed singleton or polynomial unit;
> * a complementary, active clean `C4` cap;
> * a source-valid occupied-cell deletion/contraction;
> * a strictly smaller packet of the same kind.

The statement must retain the output word, fine matching, endpoint order,
operation grade, and common tail.  A coefficient-only `C4`, a cross-word
identification, or a raw parent fold is insufficient.

If the fourth outcome strictly decreases a well-founded quantity, such as
the number of live exits followed by alternating-cycle length and support,
the lemma terminates in one of the first three outcomes.  At `N=8` this
would close the present trapped branch without constructing a global
response-to-cap comparison.  An all-order terminal-ear version would give
the full intrinsic trichotomy directly.

There is a small finite hard core after common-tail branches are removed.
Any two six-site perfect matchings either share one edge, giving a `C4` with
a literal spectator tail, or are edge-disjoint.  A family with no common-tail
pair is therefore a family of pairwise edge-disjoint perfect matchings and
has size at most five.  Exact `S_6` enumeration gives only four geometries:

```text
channels   labelled families   S6 orbits   PM-closure sizes
3          80                  2           4, 6
4          30                  1           8
5           6                  1           15
```

Thus the nonminimum transverse branch does not require an unrestricted
matching search: after grouping a fixed colour slice by fine matching, its
tail-free part has only these four uncoloured channel geometries.  Every one
has additional perfect matchings in its edge-union closure.  The remaining
question is genuinely endpoint-coloured: whether source equations force at
least one of those extra fines to be live, or instead supply an intrinsic
rank/deletion relation.  Uncoloured closure alone is not enough.

## The first uniformity boundary

The support-minimum singleton certificate is uniform whenever the larger
occurrence fibre is a Cartesian product of the local singleton with one
labelled spectator-tail family of nonzero total coefficient.  The tail may
itself contain several matchings; rank one here means common factorization
of the full occurrence family, not one tail monomial.

The first failure is at eight sites and has exactly two window/tail crossing
channels.  In word `00000122` the coefficient is

```text
a01^00*a23^00 *
  (a45^01*a67^22 + a46^02*a57^12).
```

This is not an amorphous higher-order obstruction.  After removing the
literal common tail `01|23`, it is the two-matchings part of one physical
`K2,2` on sites `4,5,6,7`:

```text
45|67, 46|57, with 47|56 the third perfect matching.
```

Thus the problem-first route returns to a balanced four-site packet, but
now inside the original coefficient equations and with the exact common
tail exposed.  The next intrinsic test is its full three-colour completion:
either the missing third matching and the other colour rows form a
tail-stable permanent unit/active cap, or crossing-tail contamination gives
the next explicit guard.  This is the earliest all-order issue; no auxiliary
`B/Eq` interpretation is needed to state it.

## Ranked attacks

1. **Literal exit closure.**  Enumerate the thirteen exits and every
   source-valid minimum mate, retaining all labels.  Seek a decreasing
   repair DAG or freeze the smallest recurrent packet.  This is the
   shortest and most falsifiable attack.
2. **Shared-star integrability.**  On every recurrent packet, impose the
   identities
   `A_pq*A_ab + A_pa*A_qb + A_pb*A_qa = 0` and their first product-rule
   faces.  The determinant/rank theorem already kills the minimal dirty
   signature; the aim is to show that every next guard similarly becomes a
   unit, clean cap, or lower-rank deletion.
3. **Intrinsic Macaulay terminal.**  If a repair packet does not close
   constructively, extend its literal dual through the actual multigraded
   EqSystem/Macaulay rows.  Only a separator defined on that source module
   is an accepted Fredholm outcome.
4. **Uniform terminal-ear recurrence.**  After the six-site packet is
   understood, prove that a terminal ear/tight cut either has a row-common
   rank-one tail, exposes the same thirteen-exit packet, or contracts while
   preserving every output row.  This is the all-order replacement for the
   full `PAComp(h)` package.

The enriched comparison route remains available, but work on it should be
judged by whether it proves one of these intrinsic outcomes.  Constructing
more auxiliary homology without a source-labelled evaluation does not move
the conjecture.

## Scope

No theorem above asserts that the thirteen-exit lemma is proved.  The
clean-pair descent and six-site endpoint are proved; the parent Macaulay
packet and common-edge no-go are proved.  The exit classification and its
all-order promotion are the open mathematical work.

The scope and the exact matching counts are audited by
`computations/verify_problem_first_intrinsic_reduction.py`.  Run it under
the three standard interpreters:

```text
python3 computations/verify_problem_first_intrinsic_reduction.py --mode structural
python3 -O computations/verify_problem_first_intrinsic_reduction.py --mode full
python3 -I -S computations/verify_problem_first_intrinsic_reduction.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
129fb9b62e1fa94e344bae1fb31726308c4ab95850957138d525735d7a16d63c
```
