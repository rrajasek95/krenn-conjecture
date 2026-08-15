# The six-root product constructs the derived response-to-cap word section

## Result

There is a source-derived coefficient/derived operation-word map which was
absent from the previous constructor registry.  This statement is not yet an
underived `AugP2` comparison.  Let

```text
r = 11110000,
c = 01211222.
```

They differ at sites `0,2,4,5,6,7`.  Apply at those sites the six commuting
endpoint matrix units

```text
1->0, 1->2, 0->1, 0->2, 0->2, 0->2.
```

On every perfect-matching monomial in the coefficient `H_r`, each site
operator has exactly one matching factor on which to act.  Their product
therefore sends that monomial, with coefficient one, to the monomial with
the same matching index in `H_c`.  The checker verifies all `105` matchings,
including all `90` parents avoiding the direct edge `36`.

For the selected matching `01|23|45|67`, the literal map is

```text
01:11 23:11 45:00 67:00
        ->
01:01 23:21 45:12 67:22.
```

Both coefficient words are mixed GHZ-zero rows.  More intrinsically, the
input letters required on the six changed sites contain both `0` and `1`,
so the operator kills every constant target word.  Hence this word map is
target-safe.

Tensor the word map with the endpoint-even section of the marked collision
correspondence,

```text
Delta5 -> Delta5 x Delta1,
x      -> x tensor (endpoint_0+endpoint_1)/2.
```

The missing-site/fine mark makes the collision square strictly Cartesian.
The checker verifies in every degree that the displayed section commutes
with the simplex/product differential and has parent augmentation one.
Consequently the composite is an explicit derived chain map from the
response word/operation object to the marked cap word/operation object.  It
retains the root, parent matching, missing-site/fine and repeated cap labels.

This removes the degree-zero operation/word edge as an independent axiom at
the marked derived level.  It is constructed by the source root action plus
the already proved marked Beck--Chevalley correspondence.

## Exact remaining boundary

The construction is a map to the marked derived cap totalization `N`, not an
underived `AugP2/P2` descent.  The first remaining map is exactly

```text
diagonal 01211222 cap q-face
    -> 0112/q23:21 P2 and 0121/q45:12 P2.
```

The current derived object has rank zero on those two word/operation rows;
the physical packet requires rank two.  If that restriction is constructed,
Leibniz immediately exports the `0102/dq23` conormal with detector `35/72`,
its sigma mate, and the hidden `(lower,word-ores)=(-E,+E)` pair.  No claim is
made here that those underived faces or the absolute reduced-Eq filler are
already present.

Thus the local construction frontier moves from

```text
missing response-to-cap word section
```

to the sharper single requirement

```text
occurrence-local marked-cap q-face -> P2 restriction with its Eq/ores faces.
```

## Verification

Run

```text
python3 computations/verify_h3_six_root_marked_collision_word_section.py
python3 -O computations/verify_h3_six_root_marked_collision_word_section.py
python3 -I -S computations/verify_h3_six_root_marked_collision_word_section.py
```

The checker uses exact rational arithmetic, replays the 105-term word map,
and verifies the complete marked chain section.

Frozen ledger SHA-256:

```text
1c12231daa14798ede88268372b26cb03deafd9ae08dc492ea2e28cd92472d9f
```
