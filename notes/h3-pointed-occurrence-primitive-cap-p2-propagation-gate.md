# The pointed occurrence conormal and primitive cap are two faces, not one existing cell

## Verdict

The pointed occurrence/global generator

\[
 P_f:\qquad dP_f=u_f-u
\]

and the primitive reduced cap

\[
 p_{v,N}:\qquad (Q_{v,N},\operatorname {ores})=(-1,-1)
\]

are not literally the same physical generator.  They are complementary
data which one enriched pointed total comparison could contain:

- `P_f` supplies the missing marked/global conormal `d(u_f-u)`;
- `p` supplies the primitive cap/residue projection in word `01211222`,
  fine/repeated grade `t q_(v,N)` / `P3+K2`.

The universal occurrence graph makes `f-u_f` and `G+u_f` into a
contractible presentation pair.  It does **not** make `u_f-u` a boundary on
the original physical fibre: adjoining that row raises conormal rank
`3 -> 4` and removes an actual old tangent.  Conversely, `p` has target and
protected rows zero and no marked-occurrence conormal.  The marked-tangent
and ordinary-residue covectors separate the two classes.

One literal `p` section cannot generate all eight fixed-packet `P2` private
squares.  Their quotient rank is eight and the marked packet's site/root
stabilizer is the identity.  A single **universal family** natural in the
marked occurrence and ordered root directions could instantiate the eight
sections, but that is a theorem schema, not one fixed source column.

Checker:
[`verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py`](../computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py).

## 1. Exact type separation

In the smallest quotient with rows

```text
(pointed conormal, Q boundary, scalar ordinary residue)
```

the three relevant classes are

\[
             P_f=(1,0,0),\qquad
             p=(0,-1,-1),\qquad
             n=(0,1,0),                              \tag{1}
\]

where `n` is the target-zero invisible cap lift.  Therefore

\[
 \operatorname {rank}(P_f,p)=2,
 \qquad
 \operatorname {rank}(P_f,p,n)=3.                   \tag{2}
\]

The pointed coordinate detects `P_f` and kills `p,n`; ordinary residue
detects `p` and kills `P_f,n`.  Thus the statements

```text
P_f is the primitive p,
the universal graph already constructs p,
the reduced-Eq invisible lift n constructs p
```

are all false.  The correct positive formulation is one enriched comparison
with distinct pointed and cap faces.

The primitive cap theorem further fixes `p`'s complete projected signature:

```text
row order  Omega,Q,ridge,Eq,W,target,ores,ainc,eta,sigma
p          0,-1,0,0,0,0,-1,0,0,0.
```

Its cap augmentation is primitive (`epsilon=-1`).  Its hoped-for centered
source top has scalar face `90 f(x)`.  The coefficient projector proves
where this face must occur; it does not construct the augmented source lift
joining it to (1).

## 2. Why one fixed section does not cover the eight squares

The eight one-root private classes live in eight separate word blocks and
remain independent modulo their complete response rows.  Their fixed-packet
rank is eight.  Although the unmarked word has a `V4` stabilizer, the marked
endpoint/residual occurrence has trivial stabilizer: every nonidentity
element moves the occurrence as well as the word.

Multiplication by `q23` preserves the word block and gives

\[
                    d(q_{23}S)=q_{23}dS+dq_{23}S.    \tag{3}
\]

On the eight block units the map `e_i -> (e_i,e_i)` still has rank eight.
One fixed section still spans rank one.  Therefore root/`q23` functoriality
has two sharply different meanings:

- once a section in one marked grade exists, it supplies that section's
  labelled square and its `dq23` face;
- a theorem natural in every marked occurrence/root pair can be instantiated
  in all eight grades;
- one literal `p` column does not generate those eight instantiations.

This distinction is exactly why a universal pointed-cap family would be a
substantial positive theorem even though its local formula has only one
schema.

## 3. Aggregate, target, cap, and reinsertion faces

At response order three the centered occurrence coefficient has
augmentation zero but scalar zero-face `90 f(x)`.  Its physical cap shadow
would be `p`, with primitive `Q=-1`, `ores=-1`, target zero.

This target-zero shadow cannot by itself lift even the first natural lower
edge.  The centered `(B-4)` preimage has a nonzero eleven-word mixed-target
normal; the primitive coordinate `X_0011^*` reads `2` on it and zero on
`p`.  Hence the first augmented face in a direct edge construction is

> one occurrence-local mixed-target cone section, totalized with its
> one-endpoint Hasse cross face.

The complete labelled two-direction square has zero **commutator** target,
so a full square can cancel those target proper faces.  It still must carry
them; target zero of `p` alone is not that totalization.

After the target square, (3) exposes the independent labelled conormal.  On
the exact representative private preimage `z`,

\[
       \sum_i z_i=0,
 \qquad (e_0+e_3-e_1-e_6)(z)={35\over72}.             \tag{4}
\]

There is a useful strongest-possible conditional calculation.  Suppose an
unconstructed occurrence-to-`Q` map assigns one copy of `p` to every
coefficient `z_i`.  Then

```text
dq23 face       +z
p's Q face      -z       -> cancels coefficientwise
p's ores face   -z       -> remains.
```

The scalar ordinary-residue value of the remainder is zero by (4), but its
labelled detector is `-35/72`.  Thus even the best formal same-label use of
`p` requires an occurrence-labelled `Q/ores` section.  The current `p`
theorem specifies only scalar `ores`; it does not define this labelled map.

## Sharp construction theorem

One theorem schema would close this local program:

> Construct a pointed source-valid total comparison, natural in the marked
> occurrence and ordered root directions, whose degree-zero face is
> `d(u_f-u)`, whose reduced cap face is `p=(-Q,-ores)`, whose root proper
> faces form the labelled Hasse square, and whose `q23` product-rule face
> carries the occurrence-labelled `Q/ores` lift.  Preserve word/fine/repeated
> grade and all target, anchor, physical-`q`, `W`, eta/sigma rows.

This is one universal family, but it has eight literal fixed-grade
instantiations.  Failure gives finite quotient duals at the pointed,
mixed-target, or labelled-residue stage; none is a physical terminal until
extended over the complete augmented map.

## Scope

This gate proves the type and rank separations, the fixed-packet propagation
rank, the direct mixed-target obstruction, and the representative labelled
reinsertion residue.  The coefficientwise cancellation above is explicitly
conditional on the missing occurrence-to-`Q` map.  No physical source lift
or terminal promotion is claimed.

Run:

```text
python3 computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py
python3 -O computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py
python3 -I -S computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py
```

Frozen ledger SHA-256:

```text
5d61c15a520af9790f864e45684029bc75bf5f3437e08fdcf38c21293ea69f81
```
