# The unspecialized C6 EqSystem has a minimum degree-four parent S-chain

## Outcome

The parent anti-diagonal from the nine-cell guard is not a degree-three
EqSystem row, but it **does** have a source-labelled degree-four Macaulay
lift after one literal endpoint-colour deletion.  Put

\[
 M_0=05|12|34,\qquad M_1=01|25|34
\]

and let (F_w) be the complete fifteen-term six-site coefficient equation
in output word (w), including its affine target term when (w) is pure.
For the two mixed words

\[
 w_0=111001,\qquad w_2=111221,
\]

define (widetilde w_0=001001), (widetilde w_2=001221).  In the full
135-variable source ring the two-row chains

\[
 G_b=a_{01}^{00}F_{w_b}-2a_{01}^{11}F_{\widetilde w_b},
 \qquad b\in\{0,2\},                                      \tag{1}
\]

have total degree four.  Literal deletion of the missing cell gives

\[
 \left.\partial_{a_{01}^{00}}G_b\right|_{a_{01}^{00}=0}
   =\sum_{M\not\ni01}m_M(w_b)-\sum_{M\ni01}m_M(w_b).       \tag{2}
\]

Since (M_0\not\ni01) and (M_1\ni01), the leading parent face of (2) is
exactly (M_0-M_1).  This is the minimum possible total degree and uses the
minimum two coefficient rows.  It does **not** yet give a support-deleting
move: (2) has thirteen surviving outside matching exits, listed below.

The executable proof is
`computations/verify_c6_unspecialized_eqsystem_parent_antidiagonal_spair.py`.

## 1. Sharp degree-three obstruction

Give (a_{uv}^{\alpha\beta}) multidegree
(e_{u,\alpha}+e_{v,\beta}).  Every decorated perfect-matching monomial in
word (w) has the squarefree word grade

\[
                         g(w)=\sum_{v=0}^{5}e_{v,w_v}.      \tag{3}
\]

A decorated matching monomial determines its word, so the only EqSystem row
in grade (g(w_b)) is (F_{w_b}).  Its projection to coordinates
((M_0,M_1)) is ((1,1)).  Therefore

\[
                         \delta(c)=c_{M_0}-c_{M_1}         \tag{4}
\]

kills every degree-three row in the grade and takes value (2) on the
desired face.  The two words have different grades, so combining them at
degree three does not evade (4).  This proves the lower bound `degree >= 4`.

No single degree-four coefficient column has parent projection ((1,-1)),
so the two rows in (1) are also row-minimal.

## 2. Why the degree-four chain works

The first term of (1) differentiates to the complete row (F_{w_b}).  In
the second term, (a_{01}^{00}) occurs exactly in the three matchings that
contain edge `01`.  Multiplication by (a_{01}^{11}) reinserts the original
endpoint colours because sites `0,1` are paired to one another.  Thus the
coefficient `-2` reverses exactly those three matching signs and proves (2)
termwise.

Before deletion, (1) has exactly 27 degree-four monomials:

* twelve (a_{01}^{00}m_M(w_b)) with (M\not\ni01);
* twelve (-2a_{01}^{11}m_M(\widetilde w_b)) with
  (M\not\ni01), all killed by deletion; and
* three common products, one for each (M\ni01), with net coefficient
  (1-2=-1).

After deletion there are fifteen cubic terms.  Removing the two leading
parents leaves precisely these thirteen exits:

| sign | matching | word `111001` monomial | word `111221` monomial |
|---:|:---|:---|:---|
| - | `01|23|45` | (a_{01}^{11}a_{23}^{10}a_{45}^{01}) | (a_{01}^{11}a_{23}^{12}a_{45}^{21}) |
| - | `01|24|35` | (a_{01}^{11}a_{24}^{10}a_{35}^{01}) | (a_{01}^{11}a_{24}^{12}a_{35}^{21}) |
| + | `02|13|45` | (a_{02}^{11}a_{13}^{10}a_{45}^{01}) | (a_{02}^{11}a_{13}^{12}a_{45}^{21}) |
| + | `02|14|35` | (a_{02}^{11}a_{14}^{10}a_{35}^{01}) | (a_{02}^{11}a_{14}^{12}a_{35}^{21}) |
| + | `02|15|34` | (a_{02}^{11}a_{15}^{11}a_{34}^{00}) | (a_{02}^{11}a_{15}^{11}a_{34}^{22}) |
| + | `03|12|45` | (a_{03}^{10}a_{12}^{11}a_{45}^{01}) | (a_{03}^{12}a_{12}^{11}a_{45}^{21}) |
| + | `03|14|25` | (a_{03}^{10}a_{14}^{10}a_{25}^{11}) | (a_{03}^{12}a_{14}^{12}a_{25}^{11}) |
| + | `03|15|24` | (a_{03}^{10}a_{15}^{11}a_{24}^{10}) | (a_{03}^{12}a_{15}^{11}a_{24}^{12}) |
| + | `04|12|35` | (a_{04}^{10}a_{12}^{11}a_{35}^{01}) | (a_{04}^{12}a_{12}^{11}a_{35}^{21}) |
| + | `04|13|25` | (a_{04}^{10}a_{13}^{10}a_{25}^{11}) | (a_{04}^{12}a_{13}^{12}a_{25}^{11}) |
| + | `04|15|23` | (a_{04}^{10}a_{15}^{11}a_{23}^{10}) | (a_{04}^{12}a_{15}^{11}a_{23}^{12}) |
| + | `05|13|24` | (a_{05}^{11}a_{13}^{10}a_{24}^{10}) | (a_{05}^{11}a_{13}^{12}a_{24}^{12}) |
| + | `05|14|23` | (a_{05}^{11}a_{14}^{10}a_{23}^{10}) | (a_{05}^{11}a_{14}^{12}a_{23}^{12}) |

On the nine-cell guard all thirteen are outside the selected word fibre, so
the restriction of (2) there is the desired anti-diagonal.  On an actual
unspecialized/full source they are real terms and must be terminalized,
contracted, or shown to land in an allowed escape block.

## 3. Complete degree-four classification

The checker examines, for each of the two output words, all `135`
one-variable target grades and all `729` possible companion words.  Per word
the number of compatible EqSystem columns is

```text
candidate columns per grade  1:15, 2:60, 4:60,
parent projection rank       1:103, 2:32.                 (5)
```

The `32` rank-two grades are exactly

\[
 e\in M_0\triangle M_1=\{01,05,12,25\},\qquad
 (\alpha,\beta)\ne(w_{b,e^-},w_{b,e^+}).                  \tag{6}
\]

For every such edge and each of its eight alternate ordered colour pairs,
the analogue of (1) gives an oriented two-row chain.  If (e\in M_0-M_1),
multiply the displayed construction by `-1`; this again normalizes the
parent face to (M_0-M_1).  In the other `103` grades the primitive dual
(4), multiplied by the chosen cell, survives.

The exhaustive 270-grade record is hashed in the checker as

```text
b2c809894b672d7af2c94d125bab849377d221f7aef966a203500efd39925ece.
```

## 4. Two-word gluing and the first off-diagonal companion grade

The first common multigrade containing both displayed output words is

\[
 g(111001)+g(a_{34}^{22})
 =g(111221)+g(a_{34}^{00}).                               \tag{7}
\]

Its complete endpoint-colour square consists of

```text
a34^22 F_111001,  a34^20 F_111021,
a34^02 F_111201,  a34^00 F_111221.                        (8)
```

On the common parent coordinates their projections are respectively

```text
(1,1), (0,0), (0,0), (1,1).                              (9)
```

Thus (7) is the first literal cross-word/off-diagonal companion grade, but
ordinary coefficient rows still have rank one there.  The primitive dual is

\[
 \delta_{34}=c_{a_{34}^{22}M_0}-c_{a_{34}^{22}M_1}.       \tag{10}
\]

Any degree-four cross-word constructor that closes the parent orientation
must be an operation-changing cell with nonzero (delta_{34}); merely adding
the two off-diagonal word rows in (8) does not help.

There is nevertheless a presentation-safe common **degree-five** packet:

\[
 G_{\mathrm{sym}}
 =\frac12\left(a_{34}^{22}G_0+a_{34}^{00}G_2\right).       \tag{11}
\]

It uses both output sections, has the same leading parent anti-diagonal after
(a_{01}^{00})-deletion, and has exactly `25` outside degree-four exits.
All twenty-five decorated monomials and their rational coefficients are in
the executable ledger.  Equation (11) synchronizes the two sections; it does
not cancel their outside debt.

## 5. Pure anchors and exact scope

No pure target was discarded.  Across the complete degree-four census the
only pure candidate in the `111001` branch is
(a_{34}^{00}F_{111111}), with lower term (-a_{34}^{00}); in the `111221`
branch it is (a_{34}^{22}F_{111111}), with lower term
(-a_{34}^{22}).  The checker retains both.  The missing pure rows
`000000` and `222222` do not occur in these multigrades and are never turned
into units.

This is an exact theorem in the unspecialized six-site EqSystem.  It sharpens
the earlier toric nonlift: the bare toric binomial is still not a physical
coefficient row, but a literal Macaulay multiplier plus endpoint-colour
deletion realizes it **modulo the thirteen named exits**.  It does not prove
that the nine-cell guard extends to a full GHZ source, that the exits vanish
on every full solution, or that the resulting parent face is a valid active
cap.  The next intrinsic task is precisely the full-source fate of the
thirteen-exit packet (or, for simultaneous word transport, the twenty-five
exits of (11)).

Run:

```text
python3 computations/verify_c6_unspecialized_eqsystem_parent_antidiagonal_spair.py --mode structural
python3 -O computations/verify_c6_unspecialized_eqsystem_parent_antidiagonal_spair.py --mode full
python3 -I -S computations/verify_c6_unspecialized_eqsystem_parent_antidiagonal_spair.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
8ae3440c5925625e521b1801b77a202290f617f226b2b67c54978d7ab9c29283
```
