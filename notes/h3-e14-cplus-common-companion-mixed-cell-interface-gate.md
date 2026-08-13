# The `C+` and common-companion interfaces do not yet form the E14 mixed cell

## Result

There is one positive compatibility and one earlier failure.

The five facewise `Omega/r` companions have aggregate terminal value

\[
                         5+u_z/t
\]

on every `eta_z`.  This is exactly the value required to extend the pure cap
residue `z_cap`.  Thus eta signs do **not** obstruct the proposed mixed cell.

However, no source-valid mixed cell follows from the current interfaces.  The
even `C+` target normal belongs to the two lower source objects

```text
0112 with q23:21 reinsertion,
0121 with q45:12 reinsertion,
```

whereas the exact E14 first-hit covector belongs to the word-`000101`
unary/`G11` presentation.  Before a literal `P2/iota` placement, these target
normals are different direct-sum rows.  The `Omega/r` and cap classes instead
belong to word `01211222` in the repeated `P3+K2` grade.

Checker:
[`verify_h3_e14_cplus_common_companion_mixed_cell_interface_gate.py`](../computations/verify_h3_e14_cplus_common_companion_mixed_cell_interface_gate.py).

## 1. The first failed square is target-normal placement

The formal order-two Cartan/Spencer triangle does close its own target and
reduced-Eq faces.  Its primitive target normal has support 11 on each lower
cut.  But its literal Hasse/source value is undefined until `P2` joins the
diagonal cap object to those two occurrence-labelled objects.

On the E14 side, deleting the visible `v13` companion leaves an exact
`target_unary` remainder of support 9; deleting `v04` as well leaves support
8.  No committed source map identifies either remainder with the two
11-support lower normals.  Hence the first missing square is

```text
iota_target:
  C+ lower target normal
      -> exact word-000101 E14 target_unary normal.
```

This is a typing failure, not a sign to tune.  In particular, the value of
the formal `C+` column under the 22-support E14 covector is presently
undefined.

## 2. The strongest favorable grant still leaves the companion

Grant, only for the quotient calculation, all three favorable steps:

1. identify the `C+` target normal with the exact E14 target-normal row;
2. supply a pure `z_cap` column in the common grade; and
3. supply the five-face `Omega/r` eta mate.

Retain the rows

```text
lambda_E14 companion, identified target normal,
scalar cap ores, C+ labelled ores, eta terminal.
```

The three granted columns have rank 3.  Appending the required mixed column
raises the rank to 4.  The primitive separator is

```text
(1,0,0,0,0),
```

namely `lambda_E14`.  It reads 1 on

```text
u05_01 v13_01 v24_11
```

and zero on the decorated `u05_01 v24_11 v34_10` core.  Thus even the
favorable target placement, cap residue, and eta grants do not replace the
literal unary S-pair column which breaks the old 22-support cancellation.

Without the separate `z_cap` grant there is a second independent failure:
both `C+` and the common companion have zero scalar cap residue.  The
labelled `C+` residue `v=(B1+B4)/2` is not that scalar cap-grade coordinate.

## 3. What does combine positively

For each `eta_z`, four facewise companions read 1 and the distinguished face
reads `1+u_z/t`.  Their sum is exactly

```text
5+u_z/t.
```

The common comparison has strict

```text
(Eq,W,target,ores,ainc)=(0,0,0,0,0),
```

so this eta correction introduces no target or residue debt.  Consequently,
once the same-labelled common-companion vertices exist and are placed in the
cap grade, they are the correct eta dressing for `z_cap`.  They do not supply
either the scalar residue itself or the E14 principal boundary.

## 4. Shortest remaining positive datum

The smallest adequate new source object is one three-object mapping-cone
diagonal joining

```text
word 000101 E14 first hit
  <-> the two lower C+ objects
  <-> word 01211222 cap/common-companion object.
```

After normalization it must simultaneously carry

```text
lambda_E14 on u05*v13*v24       1,
E14 target-normal face          exact 9/8-coordinate remainder,
scalar cap ores                 1,
C+ labelled ores                (B1+B4)/2,
eta_z                           5+u_z/t,
```

together with the already isolated reduced-Eq, hidden lower/residue, and
Hasse proper faces of `C+`.

The centered four-corner private debt is no longer an independent item.  It
is

```text
p=(1,-1,-1,1),       sum(p)=0,
```

and the universal relative graph gives

```text
d Gamma_p=t_p-p.
```

Therefore the same mixed cell must land the retained carrier `t_p`.  Adding
`Gamma_p` then cancels the complete-row private packet automatically and
leaves the desired KS residue correction.  No separate private-pivot theorem
is needed after this AugP2 landing.

Merely summing separately presented `C+`,
`z_cap`, and `Omega/r` classes does not construct this diagonal.

## Scope

This is exact for the pinned canonical E14 module, the sigma-even order-two
`C+` target/Eq cone, the AugP2 cap quotient, and the clean-C5 common-companion
interface.  It does not prove an all-resolution no-go.  It identifies the
first undefined source square and shows that even the strongest favorable
target/cap/eta grants leave the exact E14 companion covector.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
7a75e6715f270d8a88655e81e4fa3785b663db2c0ddcaa6547927c8c7d1e0c8d
```
