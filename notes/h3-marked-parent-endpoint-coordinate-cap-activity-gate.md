# The marked cap determines one coordinate, not an active covector

## Verdict

There is a literal fixed-word cap operation on the marked parent terms,
but it stops one step earlier than an active cap.  In the canonical chart

```text
physical cap pair       p=6, q=7
cap word                01211222
endpoint colours        22
direct-free pair        36
```

endpoint contraction of every marked term against a general physical
covector $K\in(V_6\otimes V_7)^*$ sees only

\[
                         \operatorname{obs}_{22}(K)=K_{22}.       \tag{1}
\]

The checker verifies (1) on all 90 direct-free parent matchings, including
the 15 direct-$67$ and 75 crossed-$67$ terms.  It also verifies all 195
internal cofactor/reinsertion squares.  In particular the distinguished
`q23` and `q45` families have respectively 15 and 12 direct-free squares.
Thus the literal fixed-word contraction is $R$-linear and commutes with
the already constructed marked deletion/P2 maps.

But (1) has rank one and kernel dimension eight.  The ternary activity
readout needs the three diagonal coordinates

\[
 \kappa_c(K)=K_{cc},\qquad
 s(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0.            \tag{2}
\]

The marked object observes $\kappa_2$ and observes neither $\kappa_0$
nor $\kappa_1$.  Hence it does not determine activity.

This is an obstruction on the original nine-dimensional physical cap, not
on a discretionary operation label.  The exact two-lift guard is

\[
 K^-=E_{22},\qquad K^+=I=E_{00}+E_{11}+E_{22}.          \tag{3}
\]

Both have $K_{22}=1$, so they act identically on every marked parent term,
every endpoint-even copy, and every retained cofactor face.  On the literal
cap block $A_{67}=E_{22}$, both also have the same nonzero direct scalar
$s=1$.  Nevertheless

\[
 (\kappa_0,\kappa_1,\kappa_2)(K^-)=(0,0,1),\qquad
 (\kappa_0,\kappa_1,\kappa_2)(K^+)=(1,1,1),             \tag{4}
\]

so the activity products are respectively zero and one.  The first physical
readout distinguishing the lifts is precisely target contraction,

\[
 K\mathbin{\lrcorner}\Delta_{8,3}
       =\sum_{c=0}^2\kappa_c(K)X_c.                    \tag{5}
\]

The canonical support-preserving lift of (1) is $K_{22}E_{22}$; it is a
genuine cap covector but is always inactive.  Choosing $I$, or another
active completion through the eight-dimensional kernel, is algebraically
possible on a suitable nonzero cap block.  It is not supplied by the marked
parent data and would import the missing endpoint-word sectors.

## What is now constructed

The coefficient and operation sides of the constructive comparison are no
longer the bottleneck:

1. the 90-parent marked augmentation is monic;
2. the six-root product supplies the endpoint-even response-to-cap word
   section;
3. divided-root naturality supplies both `q23/q45` P2 restrictions and the
   first `dq` reinsertion;
4. literal endpoint contraction on that fixed word is $R$-linear and
   cofactor-natural.

What these maps produce is the scalar observation (1), not a section of it.
No combination of the 90 fixed-word parents raises the fibre rank: their
physical cap image remains the line $R E_{22}$ if one insists on the
support-preserving coordinate lift.

## Weakest sufficient constructive datum

The constructive branch does **not** need a quasi-isomorphism from the whole
marked resolution to the underived `r0` packet.  It does not need the full
comparison cone to be acyclic, an absolute `dK_Eq=E` filler, or essential
surjectivity for every primitive cap column.

It needs only a conservative partial evaluation on the selected carrier and
the proper faces actually used:

\[
 j_A:\operatorname{obs}_{22}(K)\longmapsto
       K\in\operatorname{Cap}_{\rm phys}(A;6,7),       \tag{6}
\]

with the following four properties.

1. **Coefficient:** $K_{22}$ is the marked parent coefficient.
2. **Operation/word:** (6) commutes with the two marked P2 restrictions and
   their `q/dq` faces.  This requirement may be imposed only on the selected
   face span; a global $A$-linear comparison is stronger than necessary.
3. **Activity and cleanliness:**
   $s(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0$ and
   ${\cal E}_{6,7}(K)=0$.
4. **Conservativity:** evaluation in the actual source ring sends the marked
   carrier to that same physical $K$, rather than merely to an abstract
   target augmentation.

If $K$ and its clean error are checked directly in the physical cap, the
protected `B/Eq` separation is not an additional hypothesis for the
constructive descent.  It remains necessary only if the existing `r0`
chain ladder is used to *prove* the physical landing, and it remains
load-bearing for a universal/Fredholm terminal.

Thus the shortest positive datum is not another occurrence selector and not
an Eq acyclicity theorem.  It is one source-provenant diagonal completion of
$K_{22}$, supplying the missing $(\kappa_0,\kappa_1)$, together with the two
open scalar assertions $s\ne0$ and ${\cal E}=0$.  The identity-cap choice
is the smallest formal completion, but proving its scalar and clean
conditions is the known full clean-bridge problem, not a consequence of the
marked comparison.

## Scope and verification

This is exact for the canonical $h=3$ physical endpoints, the fixed word,
all 90 direct-free parents, all 195 internal cofactor/reinsertion squares,
the two marked P2 cuts, and the original ternary target.  It does not exclude
a cross-word diagonal completion or prove cleanliness of any completion.

Run:

```text
python3 computations/verify_h3_marked_parent_endpoint_coordinate_cap_activity_gate.py --mode structural
python3 -O computations/verify_h3_marked_parent_endpoint_coordinate_cap_activity_gate.py --mode full
python3 -I -S computations/verify_h3_marked_parent_endpoint_coordinate_cap_activity_gate.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
d447dcef475f55003ce76c8836433a9311f8c3ec372b412aa1595e06e233297a
```
