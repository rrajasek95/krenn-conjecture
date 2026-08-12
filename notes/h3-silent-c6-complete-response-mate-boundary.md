# Bright completion forces the silent C6 out of its fixed-port lock

## Outcome

In the chordless branch of `b80b064`, impose the literal physical vanishings

```text
PS = q04 = q13 = 0.
```

The complete perfect-matching expansions of
`G11[110000]` and `G22[000220]` have now been classified with all endpoint
heads and q decorations retained.  Each row starts with 105 matchings.  The
direct edge kills 15 and `q04,q13` kill 22 more, leaving 68 terms.  Relative
to the selected nonzero monomial, the other 67 terms split as follows:

| literal mate type | count per row | exact consequence |
|---|---:|---|
| endpoint port `2` or `5` | 36 | outside-endpoint complete-column route |
| same-word typed C4 | 10 | two identical decorated common factors |
| long or cross-word lock | 16 | no same-word C4 to a selected diagonal base |
| same diagonal cofactor fibre | 5 | no new endpoint carrier |

Thus 46 mates enter already proved source-valid routes.  Before imposing the
missing bright targets, the smallest honest
residual is not the unlabelled C6 of `b80b064`: it is the 16-term
long/cross-word block in each diagonal row, together with its six-term
diagonal cofactor fibre (including the selected monomial).

Twelve of the 16 long terms are physically C4-adjacent to a base in the
**other** diagonal row.  This is not a typed common-tail bridge.  After
decorations are restored, such a graph-only pair has at most one identical
factor; a source-valid C4 comparison needs two.  The other four long terms
are not C4-adjacent to either diagonal family even as physical matchings.
This is the exact label obstruction hidden by the support graph.

## Complete literal terms

For a row of head colour (i) and residual word (w), a matching with
endpoint ports (a,b) is the monomial

\[
 p_i(a,w_a)s_i(b,w_b)
       \prod_{rs\in N}q_{rs}^{w_rw_s}.                 \tag{1}
\]

The checker enumerates all 105 choices of ((a,b,N)).  In the `G11` row,
the own ports are `{0,1}`, the opposite diagonal ports are `{3,4}`, and the
outside ports are `{2,5}`.  For `G22` these roles are exchanged:
`{3,4}`, `{0,1}`, and `{2,5}`.

Any surviving term using port `2` or `5` has a literal nonzero complete
cofactor on an outside endpoint component.  The complete-column dichotomy
of the pinned outside-endpoint theorem applies: a zero column is an exact
joint-kernel deletion, while the nonzero monomial here supplies the active
cofactor and hence the routed outside branch.

For a same-word C4 term, enumeration finds one and only one selected base
at C4 distance.  Because both terms lie in the same literal word, their two
common physical edges have identical endpoint/q decorations.  These ten
terms per row are therefore genuine typed inputs to the common-tail C4
route, rather than physical adjacency alone.

## The diagonal fibre is already a cancellation packet

The six surviving terms whose two endpoint ports remain in the row's own
diagonal pair factor exactly as

\[
\begin{aligned}
G_{11}^{diag}
 &=\left(p_{1,0}^{1}s_{1,1}^{1}
          +p_{1,1}^{1}s_{1,0}^{1}\right)H_{01}^{0000},\\
G_{22}^{diag}
 &=\left(p_{2,3}^{2}s_{2,4}^{2}
          +p_{2,4}^{2}s_{2,3}^{2}\right)H_{34}^{0000}. \tag{2}
\end{aligned}
\]

Each cofactor in (2) has three matching terms.  The selected `O11` and
`O22` monomials are only one term in these sums.  Consequently their
nonvanishing does not, by itself, force a mate with a new endpoint arm.

There is a sharp rational two-row guard.  Set

```text
q04=q13=0,  q34=q12=-2,  every other q00=1,
```

and retain only the selected endpoint orientation.  Then

```text
H01 = 1+1-2 = 0,       H34 = 1+1-2 = 0,
O11 = -2 != 0,         O22 = 1 != 0.
```

Thus both complete displayed zero coefficients vanish while both selected
monomials remain nonzero, entirely through their two same-cofactor mates.
This guard is not a full unary-plus-four-response source; it proves the
logical point that the two zero rows alone do not produce a unit or a new
carrier.

## The two bright targets close all nine fixed-port charts

Now return to the exact rational common-$q$ zero fibre of `69e2417`, retain
its four displayed endpoint ports

```text
p1@0:1,  s1@1:1,  p2@3:2,  s2@4:2,
```

and adjoin one normalized pure-`11` tail in `H01` and one normalized
pure-`22` tail in `H34`.  There are three choices of each:

```text
A1=23|45, A2=24|35, A3=25|34,
B1=01|25, B2=02|15, B3=05|12.
```

The first-bright theorem `853344c` already forces a two-offdiagonal unary
mate.  In this fixed-port chart one can say more: for every one of the nine
pairs `(Ai,Bj)`, a literal private response coefficient forces a
**nonanchor** offdiagonal cell.  The private rows depend only on `Ai`:

```text
A1: G12[101120] contains q15:00*q23:11,
A2: G12[100121] contains q12:00*q35:11,
A3: G11[110110] contains q25:00*q34:11.
```

On the displayed support each coefficient has exactly that one monomial,
with coefficient `1`.  Its two other residual perfect matchings prescribe
the following literal decorated pairs:

```text
A1: q12:01*q35:10   or q13:01*q25:10,
A2: q13:01*q25:01   or q15:01*q23:01,
A3: q23:01*q45:10   or q24:01*q35:10.
```

Select the three pure physical anchors

```text
Q0=03|14|25,    Q1=01|Ai,    Q2=34|Bj.
```

In every displayed alternative at least one offdiagonal physical edge is
outside `Q0 union Q1 union Q2`, for every `j`.  For `A1`, `35` or `13` is
outside; for `A2`, `13` or `23` is outside; for `A3`, both edges of both
alternatives are outside.  This is checked literally for all nine pairs.

Consequently exactness gives the sharp dichotomy:

1. if neither alternate monomial occurs, the private zero coefficient is
   an ordinary localized source unit;
2. if a cancellation monomial occurs, it contains a nonanchor offdiagonal
   cell and enters the certified good active-minor route of `336492c`.

Thus the finite silent-C6 packet with these four endpoint ports is closed as
a lock residual: it exits to a source unit or to the already certified
nonanchor active-carrier interface.  This statement does not reprove the
downstream clean/curved landing from that interface.

## Boundary before and beyond fixed-port bright completion

Without the bright rows, after the proved outside and same-word-C4 routes
are removed, the next source input must do one of two things:

1. use a complete companion coefficient to synchronize one of the 16 long
   terms with a selected diagonal word, producing two identically decorated
   common factors; or
2. produce an exact same-star/affine lock-kernel relation which deletes its
   endpoint component.

Physical C4 adjacency to the other diagonal word is insufficient.  Nor can
one infer a new mate merely from the nonzero `O11,O22`, by the guard above.
The fixed-port bright completion supplies the missing input through the
private rows above.

The endpoint scope remains important.  An additional endpoint component on
an outside strict-shore site `2` or `5` is covered by `7114577`: its complete
column is either zero and jointly deletable, or nonzero and supplies the
active outside arm.  The present calculation does **not** classify an
arbitrary reselection among the four core ports `0,1,3,4`; that requires a
separate endpoint normalization/complete-column argument and is not hidden
in the nine-tail audit.

## Scope and verification

The mate classification is exhaustive for the two displayed complete
response coefficients in the branch `PS=q04=q13=0`.  Its two-row rational
guard is not a full source.  The positive bright conclusion is exhaustive
for all `3 x 3` target-tail choices on the four fixed endpoint ports, using
the full relevant response coefficient and the unary anchor `R`; it does
not assert arbitrary core-port endpoint normalization.

Run

```text
python3 computations/verify_h3_silent_c6_complete_response_mate_boundary.py
python3 -O computations/verify_h3_silent_c6_complete_response_mate_boundary.py
python3 -I -S computations/verify_h3_silent_c6_complete_response_mate_boundary.py
```

The checker pins `b80b064`, the outside-endpoint complete-column theorem,
and the unequal-tail source-validity theorem.  Its frozen ledger digest is

```text
67b4468bf0b7d6c8b69d52fe46abf90516ff6f25cef1b7d949bf3e4b8b105eef
```
