# The active coloop solves `db01` only after forgetting its operation and repeated-site labels

## Outcome

On the normalized pure-colour coloop chart

\[
                        q_{01}H_{2345}=1
\]

the coefficient calculation is exact:

\[
 H_{2345}\,dq_{01}+q_{01}\,dH_{2345}=0,
 \qquad
 db_{01}=p_0s_1dH_{2345}
          =-p_0s_1H_{2345}^{,2}dq_{01}.             \tag{1}
\]

Equation (1) does **not** construct the selected six-term physical
`db01` column.  There are only two ways to read its Laurent factors, and
both expose the same missing comparison.

1. If `q01`, `H2345`, `p0`, and `s1` are used only as evaluated scalar
   units, scalar multiplication does not change the pure-coloop target
   operation idempotent into the selected response first-PP idempotent.
2. If `p0*s1` is used as a physical endpoint insertion, the common top is
   `p0*s1*q01*H2345`.  It has two repeated sites and graph type
   `P4+2K2`, not the squarefree `4K2` response top underlying `b01`.

Even after granting all endpoint `dp0/ds1` faces as fan exits, the inserted
coloop row leaves six `P4+K2` tail faces and three `4K2` `dq01` faces.  The
committed complete collision fan has only `3K2` and `P3+K2` first-PP
cofactors.  Thus the localization has not routed its own mandatory
companions.

Exact checker:
[`verify_h3_selected_db01_active_coloop_reinsertion_gate.py`](../computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py).

## 1. The desired squarefree packet

Write

\[
 H_{2345}=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.
\]

The selected response fibre is

\[
 b_{01}=p_0s_1H_{2345}
\]

in word/head `11:110000`.  Its internal first-PP face is

\[
\begin{aligned}
 db_{01}=p_0s_1(&dq_{23}q_{45}+q_{23}dq_{45}
                 +dq_{24}q_{35}+q_{24}dq_{35}\\
                &+dq_{25}q_{34}+q_{25}dq_{34}).       \tag{2}
\end{aligned}
\]

The three tops in (2) are squarefree perfect matchings on all eight sites.
Each of the six flags removes one tail edge and has a squarefree `3K2`
cofactor.  These are precisely the fine and removed-edge labels frozen by
the selected-`db01` ledger.

The coloop target has three squarefree residual terms `q01*H2345`.  Its
first PP row has six tail-deletion flags and three `dq01` flags.  As an
unlabelled Kahler relation this is enough for (1).  It is still a pure
six-site target row, not the response operation in (2).

## 2. Physical endpoint insertion creates a new double collision

To acquire the `p0*s1` response label physically, insert those two endpoint
edges before using the coloop PP row.  For each of the three tails the top
is

\[
                      p_0s_1q_{01}q_{ab}q_{cd}.       \tag{3}
\]

The component through `P,0,1,S` is the path

```text
P -- 0 -- 1 -- S,
```

and the two tail edges are disjoint.  Hence (3) is `P4+2K2`, with repeated
site profile

```text
(P,S,0,1,2,3,4,5) = (1,1,2,2,1,1,1,1).
```

Its complete product-rule faces are:

| removed factor | count | cofactor type | role |
|---|---:|---|---|
| `p0` or `s1` | 6 | `P3+2K2` | endpoint insertion companions |
| one tail `q` | 6 | `P4+K2` | `q01*db01` before Laurent cancellation |
| `q01` | 3 | `4K2` | `p0*s1*H2345*dq01` companion |

The `ds1` component contains the already known selected reverse-root top
`p0*q01*H2345`.  To make the negative statement stronger, the checker
grants **all six** endpoint insertion companions an exit, whether or not
their finer root label has already been constructed.

That grant does not touch the other nine faces.  The exhaustive complete
collision packet pinned in the hyperbolic-root audit has 720 first-PP
flags, with cofactor census

```text
360 of type 3K2,
360 of type P3+K2.
```

Its selected subpacket has the same two types.  Neither `P4+K2` nor `4K2`
occurs.  Therefore dividing the coefficient of the six `P4+K2` faces by
the nonzero number `q01` is not a physical cancellation: it would have to
change the repeated-site/operation block and discard the three linked
`4K2` faces.

## 3. Complete rows and termwise reinsertion still retain the centered class

There are thirty ordered endpoint fibres.  Each has three residual `K4`
matchings and two tail deletions, hence six internal tail flags and 180
flags in the complete response tail row.

The checker gives the proposed route its strongest presentation-safe
version:

* a target/carrier copy of every one of the 180 flags;
* all 180 monic termwise reinsertion graphs `target_flag-response_flag`;
* the complete response PP row; and
* the complete target PP row.

On the resulting 360-coordinate module these rows have rank `181`.
Adjoining the selected six-term packet raises the rank to `182`.  An exact
integral detector is:

```text
weight  29 on the selected six flags in both blocks,
weight  -1 on every other flag in both blocks.
```

It kills every termwise graph and both complete rows and reads `174` on
`db01`.  Common Laurent-unit rescaling leaves both ranks unchanged.  Thus
termwise reinsertion transports the centered class to its retained carrier;
it does not make that carrier absolute.  Rows in the orthogonal
`P4+2K2` double-collision block are also killed by this detector, unless a
new column explicitly descends that block to the selected squarefree
fibre.

This is the full-labelled version of the simple warning that a complete
row does not select one endpoint fibre.  It remains true after granting
the relative graphs term by term rather than only in aggregate.

## Shortest positive datum

The earliest missing object is now smaller than any cap or `K_Eq` cell:

> Construct one source-labelled localized `PS`-over-`q01`
> restriction/insertion column whose absolute squarefree endpoint is the
> six-term packet (2), and whose six `P4+K2` plus three `4K2`
> double-collision faces land in physical fan rows without imposing a new
> relation on the classical fibre.

Such a column would make (1) a physical computation.  Without it, (1) is
only the correct coefficient shadow, and selected `db01` remains the first
unconstructed face before the cap.

## Verification

Run all three theorem views in each interpreter mode:

```text
python3 computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py --mode shadow
python3 computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py --mode fan
python3 computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py --mode counterguard
python3 -O computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py --mode shadow
python3 -O computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py --mode fan
python3 -O computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py --mode counterguard
python3 -I -S computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py --mode shadow
python3 -I -S computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py --mode fan
python3 -I -S computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py --mode counterguard
```

Frozen ledger SHA-256:

```text
39ddf6b23e9ffd12e0f4084d3c23f9684bd635263ed88e19291fea1fe27576a3
```
