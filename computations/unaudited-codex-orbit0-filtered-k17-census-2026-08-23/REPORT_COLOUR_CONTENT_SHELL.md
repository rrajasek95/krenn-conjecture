# K17 colour-content quotient and literal first shell

## Verdict

The exact reduced K17 target exports to a 6,800-coordinate global-S3
cycle-colour-content vector.  Its target support has 6,529 nonzero coordinates.

The source-faithful literal first-shell scan hit the prescribed 100,000-vector
cap after only 139,818 of 55,191,349 target rows.  Those profiles already use
16,412 coordinates, including 9,612 outside the target coordinate set.  Thus
the quotient does not produce a small complete block: the shell grows beyond
the target by `2.41x` in coordinates before even `0.26%` of target rows are
processed.  Per scope, no rank calculation or full-shell inference is made.

## Exact target vector and controls

The target TSV has schema

```text
colour_content_type    numerator    denominator
```

where a type is an unordered list of per-cycle triples `c0:c1:c2`, canonical
under one global colour permutation.  Exact controls are:

- coordinate dimension: `6,800`;
- nonzero target entries: `6,529`;
- total signed mass: `-12,732,235,776/7`;
- forgetting cycle colour content gives 183 nonzero cycle partitions;
- the forgotten vector pairs with the frozen 77-cycle functional as
  `-9,747,200,926,208/6,545`.

Target TSV SHA-256:
`09e9dbe55e6c877cdbcd7cee198e2adb129a34fd61c8c898fc142c65d686a06b`.

## Literal source profile definition

For each streamed K17 target row, the scanner enumerates every physical perfect
matching monomial dividing that row.  Pure endpoint-colour words are rejected.
For a surviving mixed word and multiplier, it forms the literal 105-term
source column, retains exactly those completions whose anchor K-degree equals
the selected term's K-degree, and projects the retained rows to global-S3
cycle-colour-content types.  Identical projected integer vectors are deduplicated.

The anchor cells are loaded/guarded against the frozen structure and equal

```text
[0,4,8,117,121,125,198,202,206,243,247,251].
```

This guard caught and rejected an earlier provisional hardcoded-anchor packet;
the provisional files were overwritten before any rank consumer used them.

## Bounded first-shell result

- target rows processed: `139,818`;
- literal mixed source columns visited: `4,690,558`;
- pure-word divisors skipped: `215,292`;
- distinct projected vectors: `100,000` (hard terminal cap);
- coordinate union: `16,412`;
- new coordinates outside the target 6,800: `9,612`;
- vector nonzero support: minimum `2`, maximum `15`, total `1,019,457`;
- selected-term K-degree histogram:
  `K2=787,781`, `K3=1,409,722`, `K4=2,493,055`;
- elapsed: `89.565` seconds.

The vector TSV schema is

```text
vector_id    coordinate_id:integer_coefficient,...
```

and the coordinate dictionary includes exact rational target coefficients.
All vectors are literal same-filtration source-column projections, not abstract
completion supersets.

## Scope and artifacts

This is a target-rooted prefix, terminalized by the explicit 100,000-vector
guard.  It is not an exhaustive first shell, a span/rank result, or a separator.

- coordinate dictionary SHA-256:
  `10ebfdcf622f0fd04ca7bf05f83f977c7cec81af8921fefb3fbf57b075d2114c`;
- vector packet SHA-256:
  `f642f9b0ab22180919bcde2144bc66e59905cf75f72897af669485a41a68993d`;
- result byte SHA-256:
  `c84949cf56e929c95174d090299b8e3c0d3113c9b2084701eb325a6129d5286b`;
- result logical SHA-256:
  `3ee8fc021e9237d3541eb255398efd41895137c9393277604045a22220ad0010`;
- scanner source SHA-256:
  `27a9731da0c96b422e3556cf909c6718e2c31c28a49cd627f61b56440df2aa17`.
