# The maximal named h3 map preserves the balanced private--Eq law

## Outcome

The complete named `h=3` packet can now be assembled without identifying
unlike operation parents or unlike word/fine/repeated grades.  It contains:

- the complete 90-occurrence response and all fifteen nonempty faces of the
  relative pointed Boolean cube;
- the relative `R01/L01` and selected-fibre carriers;
- the literal selected six-term `db01` graph;
- every tag-preserving root/Weyl word edge, both `C4` matching differences,
  every complete response row, every `H-r` graph and all induced faces in
  the canonical fixed-window packet;
- the eighteen endpoint/direction terms with profile
  `(2,2,-1,-1,-1,-1)`; and
- all named `AugP2` cap, Cartan, pure-target, physical-`q`, anchor, ridge,
  eta and sigma rows.

The resulting blockwise literal matrix has

```text
coordinates   108 + 3 + 48 + 27 = 186
columns        19 + 2 +100 + 25 = 146
rank           19 + 2 + 46 + 23 = 90.
```

The normalized pointed occurrence dual extends through its whole relative
coefficient packet.  On the final augmented packet the normalized balanced
dual is much simpler:

\[
 \boxed{\Psi={1\over4}\delta\mathbin\cdot(B-Eq),\qquad
        \delta=(1,1,-1,-1).}                          \tag{1}
\]

Every named literal family is killed by (1).  The first unmodeled family
which could break it is the physical response-to-`AugP2` principal-parts
mapping cylinder, specifically its mixed private/reduced-`Eq` incidence.

Exact checker:
[`verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py`](../computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py).

## 1. The pointed Boolean block really remains relative

For the direct-free response row `R` with 90 occurrences, the selected
four-edge Euler cube has fifteen nonempty centered faces `C_T`.  Add one
private carrier `u_T` per labelled face and columns

\[
                         C_T-u_T.                     \tag{2}
\]

Together with `R`, these sixteen columns have rank sixteen in 105
coordinates, retaining `H0` dimension 89.  The normalized top dual is

\[
                  \lambda_0={c_f\over90\cdot89},      \tag{3}
\]

extended by `lambda(u_T)=lambda_0(C_T)`.  It kills `R` and every column
(2), and reads `u_f` as one.

The direct-free restrictions of the two local endpoint charts have exact
values

```text
lambda(b01)             =  29/2670
lambda(c10)             =  -1/2670
lambda(R01 restricted)  =  14/1335
lambda(L01 restricted)  = -14/1335.
```

Adding retained `t_R,t_L,t_B` and the three monic graph columns preserves
`H0=89` and forces precisely these values.  It does not supply an absolute
`R01`, `L01`, or selected fibre.  The direct chart `A=Dq01` is absent from
this direct-free block, exactly as in the earlier source-label gate.

## 2. The complete fixed-window response packet

The next literal block has four root words, three operation charts, three
residual matchings and one retained coordinate for every word/chart.  Its
48 coordinates and 100 columns include all known internal families.  Their
rank is 46.  The Gate-II quotient character

\[
                         L=(2,-1,-1)                  \tag{4}
\]

is detected by a covector constant over word and matching labels.  After
normalization it reads one on `L H` and kills all 100 columns.

The eighteen direction terms reinsert to `2L H`, so the detector reads two.
The relative `H-r` graphs transport that value to `2Lr`; they do not cancel
it.  Adding only the `A+B` switch gives ranks `46 -> 47 -> 48` after `L`;
the same holds for only `A+C`.  Adding both gives `46 -> 48 -> 48`.  Thus
both operation-profile-changing families are needed to fill the response
coefficient class.

This response calculation is not yet an augmented terminal calculation.
It lives before the literal response-to-cap word/fine map.

## 3. Why the final dual has only `B` and `Eq`

Here `B_j` denotes the augmented private/lower row at the four chart
corners.  It is not the response chart symbol `B=p0s1`.  In coordinates

```text
(B0,B1,B2,B3, Eq0,Eq1,Eq2,Eq3),
```

the four cap diagonals are `(e_j,e_j)`, and the four signless `K2,2`
companions have one private vertex on each `delta` shore and no `Eq` entry.
Their rank is seven.  The unique primitive left kernel is

\[
                         \delta\cdot(B-Eq).            \tag{5}
\]

All other named cap rows either live outside these eight coordinates or tie
their private and reduced-`Eq` packets.  Hence target, `W`, ordinary
residue, `q`, anchor, ridge, eta and sigma corrections disappear from the
terminal functional.  The full 27-row named cap matrix has 25 columns and
rank 23, while its `B/Eq` projection still has rank seven.  The balanced
face `(B,Eq)=(delta,0)` raises those ranks to 24 and eight respectively.

## 4. Literal grading makes the earlier faces dark

The response packet lies in word

```text
11:110000,
```

whereas the canonical `AugP2` cap packet lies in

```text
01211222.
```

The words differ at six augmented sites; every one of the six selected
`P3+K2` fine degrees changes; and the cap word is not a vertex of the
existing response `D4` cube.  Therefore `R01`, `L01`, selected `db01`, and
the eighteen direction terms have zero *literal* projection to the final
`B_j/Eq_j` rows.  This is forced by their tags, not a declared cancellation.

In particular, the response chart `B=p0s1` must not be conflated with the
augmented private row `B_j`.  A response `L01` face does not break (5) until
a physical word/fine/repeated placement carries it into the `AugP2` block.

Across the three response/intermediate blocks there are 121 named columns,
all with zero `B/Eq` projection.  The remaining 25 cap columns are exactly
the family audited above and are all killed by (5).

## 5. The exact finite exhaustiveness criterion

For any additional literal source column `c` in the selected `AugP2` grade,
retain only its eight private/reduced-`Eq` coefficients and compute

\[
                   \chi(c)=\delta\cdot(B(c)-Eq(c)).    \tag{6}
\]

Then:

```text
chi(c)=0 for every column of the exhaustive map
    -> Psi in (1) annihilates the full map;

some chi(c) != 0
    -> the unique balanced B/Eq quotient is filled projection-wise,
       and that same physical column's other faces must be repaired.
```

This is unconditional linear algebra once the literal column census is
exhaustive.  No target/residue/ridge search is needed.  The primitive
controls are

```text
(B,Eq)=(delta,0)       chi/4 =  1
(B,Eq)=(0,delta)       chi/4 = -1
(B,Eq)=(delta,delta)   chi/4 =  0.
```

Thus one primitive `B`-only or `Eq`-only `delta` column is the exact
smallest missing projected rank-raiser: it changes the projection rank from
seven to eight.

## 6. First truly unmodeled physical family

No currently constructed source object has that bright projection.  The
first missing literal arrow overall is an occurrence-local word-changing
Cartan/Spencer/PP map from `11:110000` to `01211222`.  After granting such a
word arrow, the first independent augmented obstruction is the primitive
mapping-square mixed incidence; the packaging ranks are

```text
hidden lower/P2 + clean Eq       rank 2
+ mixed mapping-square cell      rank 3
+ labelled shifted ridge         rank 4.
```

Hence the first unmodeled family capable of breaking (1) is:

> one source-labelled response-to-`AugP2` PP mapping-cylinder/Tate family
> placing the selected `db01`/eighteen-direction packet and carrying a
> nonzero `delta`-weighted private/reduced-`Eq` mismatch.

It must also carry the six `P3+K2` faces, their six sibling `3K2` faces,
the word/fine diagonal, reduced-`Eq` cap-label descent, and the labelled
`gamma=-dOmega`/`-d(q_xv^01)` ridge connection.  Adjoining another relative
carrier would not answer this test.

## Scope

This is an exact union and projection theorem for all named canonical
`h=3` families.  It constructs the maximal named literal matrix and the
finite scalar exhaustiveness criterion.  It does not prove that the named
families exhaust every full-source column, construct the missing cross-word
family, or promote the blockwise compatibility covector itself to the
source-terminal/Macaulay quotient.

Run:

```text
python3 computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py
python3 -O computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py
python3 -I -S computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py
```

The checker prints its frozen ledger SHA-256.

```text
6e223c587ea94e9544c5ddf711fc16dabc786158da5f9930643e7411dee2afb0
```
