# The collision dual extends, while unsigned roots move the debt to second order

## Verdict

There are two exact conclusions.

First, the parent-labelled collision functional `Xi_01/30` extends through
the strongest currently justified relative packet: all 90 top parent
graphs, all 120 labelled first-PP graphs, the complete physical response
block, and the known cap/Cartan columns.  Before a cross-grade placement is
supplied, the forced augmented values are

```text
target = Eq = q = anchor = ores = W = ridge = 0.
```

The first cross-grade rank raiser is the missing forward-`DSQ`
`P3+K2` PP-to-cap comparison.  A presentation-safe relative copy does not
kill the dual: it transports it to the cap block, where the known
cap/Cartan formula extends it exactly.

Second, complete **unsigned** vertex roots are a real shortcut through the
first collision face.  After the shore gauge they return exactly `A+B` and
`A+C`, not the pre-gauge differences.  But on the complete response their
second order is a 90-term aggregate, not the required six-term fixed-window
switch.  The first missing datum moves from a collision-standard splitter
to a squarefree occurrence/window projector.

Exact checker:
[`verify_h3_collision_xi_augmented_dual_unsigned_root_shortcut_gate.py`](../computations/verify_h3_collision_xi_augmented_dual_unsigned_root_shortcut_gate.py).

## 1. Relative extension of `Xi_01/30`

Resolve the 45-term missing-`0`/doubled-`S` sector into its 90
operation-parent occurrences.  The signed root packet has values

```text
15 occurrences +1,  15 occurrences -1,  60 occurrences 0.
```

Let `c_i` be the collision occurrence and `t_i` its retained carrier.  The
presentation-safe top graph is

\[
                          d\beta_i=c_i-t_i.             \tag{1}
\]

Consequently the normalized dual is forced to take the same value
`Xi_i/30` on `c_i` and `t_i`.  For every active occurrence and every one of
its four labelled PP faces, write `f_(i,e)` for the face and `s_(i,e)` for
its retained carrier.  Naturality gives

\[
                    d(PP_e\beta_i)=f_{i,e}-s_{i,e},    \tag{2}
\]

so the dual is again forced to take `Xi_i/30` on both sides.  Thus it kills
all 90 columns (1) and all 120 columns (2), while reading one on both the
top signed packet and its retained anti-carrier.

The parent-even collision row is one on all 90 occurrences, hence is killed
because the root weights sum to zero.  Every ordinary response term remains
in squarefree operation degree and is killed by grade.  This is the exact
relative extension; setting the retained values to zero would change `H0`
and is not presentation-safe.

## 2. Exact augmented values

The response collision word is `11:110000`.  The known cap corners live in
the separate physical cap word/fine/repeated block.  No committed column
connects them.  Therefore the only extension before a cross-grade bridge is

```text
B_j = Eq_j = target_j = W_j = ores_j = 0,
q = anchor/ainc = ridge = 0.
```

This zero extension kills all old cap/Cartan columns

\[
\begin{aligned}
 r0_j&=B_j+Eq_j+target_j-ainc,\\
 T_j&=-W_j+target_j,\\
 \rho_j&=W_j+ores_j,\\
 K&=\sum_j\alpha_jores_j+ridge,
 \qquad \alpha=(-1,1,1,-1).
\end{aligned}                                                   \tag{3}
\]

Now take the smallest literal positive PP carrier, of dual value `1/30`,
and formally bridge it to cap corner `B0`:

\[
                            s_{+,e}-B_0.               \tag{4}
\]

The zero-cap dual reads `1/30` on (4), and the boundary rank rises
`224 -> 225`.  Killing (4) forces `mu_0=1/30`.  The unique known
cap/Cartan extension is

```text
mu                = ( 1/30, 0, 0, 0)
target             = (-1/30, 0, 0, 0)
Eq                 = (     0, 0, 0, 0)
q, anchor/ainc     = 0, 0
ores               = ( 1/30, 0, 0, 0)
W                  = (-1/30, 0, 0, 0)
ridge              = 1/30.
```

For arbitrary cap values `mu_j`, the exact formula is

\[
 \boxed{
 target_j=W_j=-\mu_j,\quad ores_j=\mu_j,\quad
 ridge=-\sum_j\alpha_j\mu_j,\quad Eq=q=ainc=0.}       \tag{5}
\]

Substitution in (3) makes every pairing zero.  Thus a relative
PP-to-cap bridge is the first augmented rank raiser, but it is not the
class-killing column.  An **absolute** occurrence-labelled landing of the
whole retained Xi anti-carrier has dual value one and is the actual
filler/terminal fork.

The physical typing of (4) is the still-missing forward-`DSQ` `P3+K2`
response-to-AugP2 family, with word, fine degree, repeated edge, operation
parent, removed edge and reinsertion edge all retained.  The reverse root
has the analogous `PQQ` word-placement issue.

## 3. Unsigned roots in the shore-gauged basis

Let `X_0` replace every edge incident with vertex `0` by the corresponding
edge incident with `S`, with all signs positive, and let `Y_0` be the
opposite root.  On the complete 105-matching response `H`, direct
enumeration gives

\[
 X_0H=2C_{0\to S},                                    \tag{6}
\]

where `C_(0->S)` is the symmetric 45-term missing-`0`/doubled-`S`
collision row.  Therefore the signed standard dual `Xi_01/30` kills (6).
If the symmetric collision cell and its faces are granted, the first-order
signed 24-term obstruction is genuinely bypassed.

The local second-order return is also correct.  On

\[
 A=Dq_{01}H_{2345},\quad B=p_0s_1H_{2345},\quad
 C=p_1s_0H_{2345},
\]

one has

\[
                         Y_0X_0(A)=A+B.                \tag{7}
\]

The analogous unsigned `1 <-> S` square gives

\[
                         Y_1X_1(A)=A+C.                \tag{8}
\]

Equations (7)--(8) are exactly the required physical families after the
shore gauge `diag(1,-1,-1)`.  Comparing them to pre-gauge `A-B,A-C` would
produce a spurious sign defect.

## 4. The exact second-order aggregate

The shortcut does not yet isolate the fixed window.  On all of `H`, every
matching containing the edge `0S` is killed by `X_0`; every other matching
returns once to itself and once to its `0/S`-swapped mate.  Hence

\[
 \boxed{Y_0X_0(H)=2\bigl(H-H_{0S}\bigr),}              \tag{9}
\]

where `H_(0S)` is the complete 15-term block of matchings containing edge
`0S`.  The right side has 90 terms, all of coefficient two.  Similarly,

\[
             Y_1X_1(H)=2\bigl(H-H_{1S}\bigr).         \tag{10}
\]

Each desired fixed-window packet `(A+B)H_2345` or `(A+C)H_2345` contains
only six terms: three root-swap orbits out of the 45 orbits in (9) or (10).

On the 105 matching coordinates the ranks are exactly

```text
H plus the two unsigned aggregates                 rank 3
plus one fixed-window switch                       rank 4
plus both fixed-window switches                    rank 5
plus (2A+B+C)H = (A+B)H+(A+C)H                    rank 5.
```

So both selected switches are independent occurrence raisers.  The checker
gives normalized exact detectors.  For `(A+B)H`, one may use

```text
selected A and B                         1/6
other matchings containing neither S0/S1 -1/144
other matchings containing S1            -1/24
matchings containing S0                    0.
```

It kills `H` and both unsigned aggregates and reads one on the selected
switch.  After that switch is granted, the detector for `(A+C)H` is `1/3`
on the three selected `C` matchings, `-1/12` on the other twelve matchings
containing `S0`, and zero elsewhere.

A symmetric detector for the shore-gauged Gate-II packet
`(2A+B+C)H_2345` is

```text
selected A, B, C                         1/12
other matchings containing neither S0/S1 -1/288
other matchings containing S0 or S1      -1/48.
```

It kills all three aggregate columns and reads one on `2A+B+C`.

## 5. Revised shortest path

There are now two valid lanes.

1. **Signed-root lane.**  Construct an absolute Xi anti-carrier landing.
   The first relative augmented interface is the forward-`DSQ` PP-to-cap
   bridge, with forced values (5).
2. **Unsigned-root lane.**  Grant the symmetric collision cell and its full
   face packet.  The collision-standard dual disappears, and the first new
   obstruction is a squarefree occurrence/window projector splitting the
   three selected `A/B` or `A/C` tail orbits from the 45-orbit aggregate
   (9)--(10).  That projector must carry the same word/fine/repeated,
   restriction/reinsertion, `q`/anchor, target, residue, `W`, and ridge
   readouts as the desired chart-switch family.

The unsigned lane is shorter only if the fixed-window projector follows
from an existing physical restriction/occurrence theorem.  Ordinary
response normalization cannot isolate it: the displayed rank and dual
prove exact independence.

## Scope

This is an exact canonical `h=3` rational theorem.  The signed calculation
extends through the known relative and cap/Cartan blocks, not through
unknown full-source columns.  The unsigned calculation exhausts the
complete 105-matching response and corrects the shore-gauge sign, but does
not construct either selected occurrence projector or its augmented
physical landing.

## Verification

Run

```text
python3 computations/verify_h3_collision_xi_augmented_dual_unsigned_root_shortcut_gate.py
python3 -O computations/verify_h3_collision_xi_augmented_dual_unsigned_root_shortcut_gate.py
python3 -I -S computations/verify_h3_collision_xi_augmented_dual_unsigned_root_shortcut_gate.py
```

Frozen ledger SHA-256:

```text
2aebec770a0d1b394e56977b7097e2152dd34b3a1060a0b35ef13ce68ed79328
```
