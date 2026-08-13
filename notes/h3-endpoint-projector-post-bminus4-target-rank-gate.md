# One target cone serves all endpoint factors, but their PP faces are independent

## Exact sequential calculation

For the marked `h=3` occurrence put

\[
 c_f=90e_f-\mathbf1,
 \qquad v_0=(A+I)c_f,
 \qquad v_1=(B-4I)v_0,
 \qquad v_2=(B-2I)v_1.                               \tag{1}
\]

The last factor closes the coefficient polynomial:

\[
                  (B+2I)v_2=0.                       \tag{2}
\]

For a coefficient packet `v`, let `N(v)` be the target normal of the
literal endpoint site-transposition/two-root-Cartan paths weighted by `v`.
The three endpoint stages have

\[
 N_4=N(v_0),\qquad N_2=N(v_1),\qquad N_{-2}=N(v_2).  \tag{3}
\]

Each normal has support eighteen, and exact arithmetic gives

\[
                 \boxed{N_2=-{32\over7}N_4,
                        \qquad N_{-2}={108\over7}N_4.} \tag{4}
\]

Thus their sequential target ranks are

```text
N4                    rank 1
N4,N2                 rank 1
N4,N2,N-2             rank 1
```

and adjoining the GHZ target line gives rank two at every stage.  For
example, the `X_000000` coordinate on the three normals is

```text
(-1008, 4608, -15552),
```

which displays the same ratios.  The normal is not on the GHZ line; the
previously pinned mixed-word detector witnesses that distinction.

Checker:
[`verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py`](../computations/verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py).

## Consequence for `C2+`

Once one physical `B-4` / `C2+` target-bearing cone realizes `N4`, no new
target direction is needed for the other two endpoint factors.  The same
cone, rescaled by `-32/7` and `108/7`, cancels `N2` and `N-2` respectively.
This is a real compression of the target part of the cubic endpoint
projector.

It does **not** reduce the entire source lift to the `B-4` section.

## The product-rule packets do not collapse

A physical endpoint path has the product rule

\[
 d(vH)=v(g-1)+(dv)H.                                 \tag{5}
\]

The first term of (5) carries the target normal above.  The second terms
are weighted by `v0,v1,v2`.  In the complete ninety-occurrence module their
sequential ranks are

```text
v0                    rank 1
v0,v1                 rank 2
v0,v1,v2              rank 3.
```

This remains a rank-three obstruction after forgetting the endpoint-path
labels; retaining the distinct Hasse stages and source paths cannot lower
the rank.  Hence ordinary endpoint bar covariance and the single `B-4`
section do not manufacture the `B-2` and `B+2` product-rule packets.

All three endpoint stages stay in the response/bar source summand and have
central Eq input incidence zero.  The matching factor has its own first
face

\[
\begin{aligned}
 db_{01}=p_0s_1(&dq_{23}q_{45}+q_{23}dq_{45}
               +dq_{24}q_{35}+q_{24}dq_{35}\\
               &+dq_{25}q_{34}+q_{25}dq_{34}),       \tag{6}
\end{aligned}
\]

which is target zero and lives in the fixed-endpoint matching-PP summand,
not in any endpoint-path packet.  After granting the complete physical
`B-4` section, the smallest protected quotient therefore still has three
independent face types:

1. the `B-2` one-endpoint product-rule packet;
2. the `B+2` one-endpoint product-rule packet;
3. the `(A+I)` selected six-term matching packet.

None supplies the central Eq incidence; that enters only in the mixed
selected-fibre / `K_Eq` square.

## Shortest positive theorem

Extend the physical `B-4/AugP2` section to one source-natural cubic
endpoint/matching principal-parts totalization.  Its target correction may
reuse the single `C2+` cone with the ratios (4), but it must explicitly
carry the two new endpoint product-rule packets and (6).  A higher
bar/Bianchi cell could package these three faces coherently; ordinary
coefficient covariance alone does not prove that cell exists.

This is an exact rational `h=3` coefficient, target, source-stage-rank, and
central-Eq-incidence audit.  It does not construct the higher totalization
or promote a remaining local dual to a physical terminal.

## Verification

```text
python3 computations/verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py
python3 -O computations/verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py
python3 -I -S computations/verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py
```

Frozen ledger SHA-256:

```text
645ffbc09b92fd5a087c69d35b834143d2195d48ea7d26bcf4d2e0d2b6afbb1a
```
