# The support-15 coordinate repair exhaustion

This note continues the two exceptional edge-`37` strata isolated in
[`n8-support15-edge37-anchor-rank-strata.md`](n8-support15-edge37-anchor-rank-strata.md).
It proves that they cannot extend to an exact source while the forced anchors
remain coordinate anchors.  The proof is independent of the rank and entries
of the sole nonanchor block.

The exact checker is
[`verify_n8_support15_coordinate_repair_exhaustion.py`](../computations/verify_n8_support15_coordinate_repair_exhaustion.py).

## Theorem

Use the unique support-15 graph

```text
01 02 03 04 12 13 16 24 27 35 37 45 46 56 57
```

and the selected edge-`37` one-anchor chart

```text
27=0, 57=1, 37=2, 03=0, 35=1,
```

with `13` the sole nonanchor block.  Suppose every other block is a nonzero
coordinate anchor, every vertex sees all three anchor colours, and all three
pure target fibres are supported.  Then:

1. there are exactly six possible coordinate-anchor colourings;
2. for every colouring, even after all nine cells of `M_13` are declared
   available, there are exactly six mixed words with a unique supporting
   perfect matching not using `13`; and
3. every attempt to add an alternate matching for a selected detector changes
   a protected anchor placement or makes a protected near vector
   noncoordinate.

Consequently neither exceptional local stratum extends to an exact source:

```text
rank(M_13)=3,
rank(M_13)=2 with ker_left(M_13)=<e_direct>.
```

The same contradiction handles both ranks because the detecting matching
does not use `M_13` at all.

This is a theorem for the coordinate-anchor stratum.  It does not silently
assume that an arbitrary noncoordinate anchor can be re-coordinatized.  Such
a deformation is instead routed to the active rank-one zero already proved
in the preceding rank-strata result.

## The requested fibre and the uniform identity

For the guard displayed in the preceding note, the first detector is

```text
word      00000101
matching  03|16|24|57.
```

Write `t_ij` for the nonzero scalar of coordinate anchor `ij`.  The complete
mixed coefficient is the single monomial

\[
 H_{00000101}=t_{03}t_{16}t_{24}t_{57}.              \tag{1}
\]

This remains the complete coefficient after replacing `M_13` by a wildcard
matrix with all nine cells present: none of the other nine support matchings
has the requested coordinate cells.  The exact target row requires the left
side of (1) to vanish.  In the Laurent ring obtained by inverting the live
anchor scalars,

\[
 t_{03}t_{16}t_{24}t_{57}=0
 \quad\Longrightarrow\quad 1=0.                     \tag{2}
\]

Equation (2) is the requested common symbolic certificate.  It never refers
to `det(M_13)` or to its exceptional left kernel, so it handles rank three
and exceptional rank two uniformly.

The six robust detectors for this first colouring are

```text
00000101  03|16|24|57
02201111  03|12|46|57
10120002  02|16|37|45
11011110  01|27|35|46
11020222  01|24|37|56
20012100  04|16|27|35
```

Thus the contradiction is not tied to a lexicographic accident.

## Exhaustion of mates

There are ten perfect matchings in the support graph.  For the word in (1),
the selected matching is the only compatible one.  Each of the other nine
has an incompatible cell on an edge incident to cubic vertex `6` or `7`:

```text
01|24|37|56   bad on 37,56
01|27|35|46   bad on 27,46
02|13|46|57   bad on 46
02|16|37|45   bad on 37
03|12|46|57   bad on 46
03|16|27|45   bad on 27
04|12|37|56   bad on 37,56
04|13|27|56   bad on 27,56
04|16|27|35   bad on 27
```

At a cubic endpoint every incident edge is a forced anchor.  If the new cell
changes the fixed far coordinate, the anchor placement has changed.  If it
keeps the far coordinate and changes the cubic coordinate, its near vector is
noncoordinate; the rank-one factorization

\[
 F=2(u_0\cdot x)(u_1\cdot x)
       (y^TM_0)\otimes(y^TM_1)
\]

then supplies a target-active zero through the corresponding kernel.  Hence
there is no mate that stays inside either exceptional coordinate stratum.

For the other five coordinate completions the same exhaustive statement
holds.  In one completion, the selected detector additionally uses the
protected response anchor `03` as the routing defect.  A changed far colour
again changes the anchor placement; a changed near colour makes the anchored
response vector `w` noncoordinate and invokes the same active rank-one route.

## Scope and consequence

The prior local analysis left two coordinate rank strata and asked the full
mixed system to remove them.  The present theorem does exactly that under the
literal coordinate-anchor normal form, including arbitrary repairs inside
the nonanchor block.  Therefore the unique support-15 terminal has only the
following possible escapes:

* deform a protected anchor, which changes the anchor placement or lands in
  the already positive noncoordinate active-zero stratum; or
* retain the coordinate placement, in which case a mixed Laurent unit gives
  the contradiction (2).

No additional rank split, determinant certificate, or independent-shore
argument is required at this terminal.

## Reproduction

```sh
python3 computations/verify_n8_support15_coordinate_repair_exhaustion.py
python3 -O computations/verify_n8_support15_coordinate_repair_exhaustion.py
python3 -I -S computations/verify_n8_support15_coordinate_repair_exhaustion.py
```

The frozen ledger digest is
`654a90328fa9d3d3b5e742f71eddc6e9b708149cab8be2977eef1af7a90343a6`.
