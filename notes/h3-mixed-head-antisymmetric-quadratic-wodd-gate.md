# The mixed-head antisymmetric selector removes the scalar debt, not the object grade

## Outcome

The proposed coefficient construction is exact.  Retain the two ordered
mixed-head response objects

```text
O+ : (word w,      head 01, operation Q_(0,1) X23),
OT : (word tau(w), head 10, operation Q_(1,0) X23).
```

On the direct-free response packet, let

```text
f     = P0|S1|23|45,
tau f = P1|S0|23|45.
```

Then the two coefficient identities are

\[
 Q_{01}X_{23}R_{01}(w)=e_f,
 \qquad
 Q_{10}X_{23}R_{10}(\tau w)=e_{\tau f},
\]

and therefore

\[
 QX_{23}\bigl(R_{01}(w)-R_{10}(\tau w)\bigr)
              =(e_f,-e_{\tau f}).                    \tag{1}
\]

Both mixed heads have zero GHZ target.  Consequently (1) has target zero
termwise: the earlier scalar defect `f_tau(x)-f(x)` is genuinely absent.

However, (1) is an honest **two-object relative bar**, not a fixed-source
`W_odd` boundary.  Canonical transport from `OT` to `O+` transports the
word, head, operation and endpoint occurrence together, hence

\[
       (\tau w,10,Q_{10},\tau f)
          \longmapsto (w,01,Q_{01},f).
\]

Under that map (1) is zero.  The fold which instead gives

\[
                           e_f-e_{\tau f}              \tag{2}
\]

forgets the object/head/word tag **without** transporting its endpoint
label.  It is not the canonical fixed-source chain map.

Exact checker:
[`verify_h3_mixed_head_antisymmetric_quadratic_wodd_gate.py`](../computations/verify_h3_mixed_head_antisymmetric_quadratic_wodd_gate.py).

## Exact H0 test

There are 90 direct-free occurrences in each head object.  The full
endpoint-transpose groupoid has

```text
C0 dimension       180,
bar rank             90,
H0 dimension         90.
```

The selected vector (1) is exactly one of these bar boundaries, up to
orientation.  Canonical descent sends all 90 bar boundaries to zero.

The nontransported fold has rank 45 over all endpoint-transpose pairs.  If
only the selected relation (2) is adjoined directly to the 90-dimensional
fixed occurrence object, then

```text
fixed-source H0: 90 -> 89.
```

Thus it imposes a new equality rather than resolving the old source.  The
minimal rank-preserving relative repair is still

\[
                       db=(e_f-e_{\tau f})-u^- .       \tag{3}
\]

Adding the private coordinate `u^-` gives 91 coordinates and one new
relation, so H0 remains 90.  Constructing this labelled graph coordinate,
not correcting a scalar target, is the first missing physical datum.

## Quadratic and unselected supports

For either ordered-head object the support sizes are

```text
complete response        90
Q_(ordered endpoints)     3
X23                       12
Q X23 top                  1.
```

The two-object support sizes are therefore `180,6,24,2`.  Away from the
selected top, each object retains two `Q` terms and eleven `X23` terms.
These are not erased by the coefficient equality.  In particular, the
three `Q01` terms are the residual tail matchings

```text
23|45, 24|35, 25|34,
```

and only the first is selected by `X23`.

## All first product-rule flags

Before transport, differentiating the two selected tops gives eight literal
flags:

```text
+ dP0*S1*q23*q45       - dP1*S0*q23*q45
+ P0*dS1*q23*q45       - P1*dS0*q23*q45
+ P0*S1*dq23*q45       - P1*S0*dq23*q45
+ P0*S1*q23*dq45       - P1*S0*q23*dq45.
```

No pair cancels in the retained direct sum: the left column has
`(w,01,Q01)` and the right column has `(tau(w),10,Q10)`.  Canonical
endpoint/head transport pairs the flags crosswise:

```text
dP0*S1       <-> P1*dS0,
P0*dS1       <-> dP1*S0,
P0*S1*dq23   <-> P1*S0*dq23,
P0*S1*dq45   <-> P1*S0*dq45.
```

After that transport all four pairs vanish, just as the top does.  Under
the nontransported fold the two marked tail faces are instead

```text
P0|S1|45 - P1|S0|45,
P0|S1|23 - P1|S0|23,
```

which are precisely the two desired order-two odd faces, but again only
after the same forbidden object-forgetting fold.  A physical repair needs
the carrier (3) on the top and compatible transported carriers on these four
first face families.

## Consequence for the `Phi_KS,r0/P_f` ansatz

This is a useful improvement over selecting one endpoint-even aggregate:
the mixed-head pair supplies the correct odd coefficient and has no scalar
target correction.  It does **not** fill the first missing physical atom in
the finite `Phi` ansatz.  The ansatz needs a literal response-occurrence to
cap section inside the fixed presentation; (1) remains a relative
head-transpose interval whose canonical fixed-source shadow is zero.

The shortest positive datum is now sharper:

> Construct one presentation-safe odd comparison graph with differential
> (3), retaining the word/head/operation transport and its four product-rule
> families.  Its two tail restrictions give the `q23` and `q45` order-two
> selectors.  The mixed-head target requires no additional correction.

## Verification

```text
python3 computations/verify_h3_mixed_head_antisymmetric_quadratic_wodd_gate.py
python3 -O computations/verify_h3_mixed_head_antisymmetric_quadratic_wodd_gate.py
python3 -I -S computations/verify_h3_mixed_head_antisymmetric_quadratic_wodd_gate.py
```

Frozen ledger SHA-256:

```text
148738356fd104ad32ead0ca2d93f4658beac57943acb670225d246d4018fdff
```
