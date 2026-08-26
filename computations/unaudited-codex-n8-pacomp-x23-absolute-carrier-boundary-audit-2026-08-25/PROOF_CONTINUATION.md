# The absolute carrier equation is new, not an identity of the existing chains

Status: **REFUTED AS A DERIVATION FROM THE PINNED PHYSICAL DEFINITIONS.**

Parent manifest: `92bbb2983c79ad15921ad95d3528b51e7f9e0812f39819cdcbaef47d2adb78be`.
Scope: canonical `h=3` only.

## Provenance comes first

The names `E_B,E_C` do not occur as generator definitions in the pinned
physical registry.  Their only pre-existing occurrence is the explicitly
conditional sentence

```text
If one physical augmented chain (E_B+E_C) has boundary (t_B+t_C), then ...
```

Therefore `d(E_B+E_C)=t_B+t_C` cannot be expanded from the original
definitions.  It is the hypothesis whose construction was requested, not a
previously defined identity.

## Exact expansion of the genuine nearest chains

The source-provenant fixed-source chains are the monic relative
endpoint-choice graphs

\[
 d\Gamma_B=t_B-(B-A),\qquad
 d\Gamma_C=t_C-(C-A),                                \tag{1}
\]

where

\[
 A=Dq_{01}H,\quad B=p_0s_1H,\quad C=p_1s_0H,
 \quad H=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.     \tag{2}
\]

Consequently

\[
\boxed{d(\Gamma_B+\Gamma_C)=t_B+t_C+L_{01}},
\qquad L_{01}=2A-B-C.                                \tag{3}
\]

There is no sign freedom in (3).  On each of the three fixed `C4` tails its
terms are

```text
+t_B +t_C +2 D*q01*tail -p0*s1*tail -p1*s0*tail.
```

Thus the first mismatch against `t_B+t_C` is `A-B` in the B channel and
`A-C` in the C channel.  Their sum is exactly the primitive balanced packet
`L01`.  The direct-chart covector kills the endpoint plane and reads `2` on
`L01`, so it cannot be discarded as a complete-response combination.

## Proper faces

Differentiating `L01` gives 36 terms:

- 18 residual-tail derivatives, six in each of the `DQ`, `PS01`, `PS10`
  charts, with coefficients `2,-1,-1`; and
- 18 endpoint/direction-factor derivatives with the same chartwise support
  and coefficients.

The relative `C4` totalization is honest: the two mixed `x'y'U` faces cancel
termwise.  Its boundary nevertheless exports

\[
\begin{aligned}
&-2((dD)q_{01}+D(dq_{01}))r_{DQ},\\
&+((dp_0)s_1+p_0(ds_1))r_{PS01},\\
&+((dp_1)s_0+p_1(ds_0))r_{PS10}.
\end{aligned}                                        \tag{4}
\]

These are retained-carrier faces, not zero.  The switch--Weyl product is
also not an absolute carrier: its strict boundary is

\[
D(T H_W)=(d_{PP}T)H_W+T(W-1),                       \tag{5}
\]

so it has both PP and `W-1` proper faces rather than boundary `T` alone.

## Restriction and covariance

The site-covariance bar is source-valid between two endpoint-choice
objects.  It fixes response word `11110000` and the physical tail `2345`.
There are exactly two folds to one fixed object:

1. canonical transport relabels `B` back to `A`, so the boundary is zero;
2. raw forgetting gives `B-A` (and similarly `C-A`) but kills the old
   two-dimensional chart `H0`.

Hence neither fold constructs (1) without the retained `t` coordinate.

At coefficient level the two total mate involutions `tau_a,tau_b` reverse
the balanced charge, and the cut involution `(2 5)(3 4)` permutes the three
terms of `H` and hence fixes their sum.  Those checks establish the forced
signs only.  Physical tau/sigma naturality of `E_B,E_C` is untypable because
the chains do not exist.  Assigning it would assume the conclusion.

## Minimal corrected statement

The exact theorem supplied by the original chains is (3), equivalently

\[
 d(\Gamma_B+\Gamma_C)-(t_B+t_C)=L_{01}.              \tag{6}
\]

The smallest new positive hypothesis is one source-valid absolute carrier
`E_T` with

\[
                         dE_T=t_B+t_C.                \tag{7}
\]

Splitting `E_T` into `E_B+E_C` is unnecessary for the coefficient filler and
is strictly stronger: it additionally requires endpoint naturality.  No
placement `J`, filler, `Q23`, `PAComp(3)`, or uniform conclusion is promoted.
