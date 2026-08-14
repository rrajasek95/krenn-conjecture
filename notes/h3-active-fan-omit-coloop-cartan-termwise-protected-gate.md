# The active-fan Cartan prism gives the odd U/V row exactly, but not yet its protected ridge

## Result

Put the pure-colour coloop at `01`, the direct-free response edge at `67`,
and let `w` be the signed colour Weyl action at `0,1`.  Let `s` be the
physical endpoint transposition `6 <-> 7`.  On every literal matching `M`
which omits both `01` and `67`, the complete-row pivot has the two weighted
terms

\[
                         \alpha U_M,\qquad dV_M.
\]

The signed Weyl action changes both copies of each root-site colour: the
coefficient cell `alpha=A_01[c,c]` becomes `d=A_01[i,i]`, and the two local
colours in the matching term change from `i,i` to `c,c`.  The two Weyl
signs on `alpha` cancel.  Hence, literally,

\[
                         w(\alpha U_M)=dV_M.           \tag{1}
\]

The endpoint swap fixes `01`, exchanges the two response orientations, and
fixes every decorated edge outside `{0,1,6,7}`.  Therefore on each endpoint
orbit

\[
\begin{aligned}
 (1-s)(w-1)(\alpha U_+)
   &=d(V_+-V_-)-\alpha(U_+-U_-)\\
   &=-D,                                               \tag{2}\\
 D&=\alpha(U_+-U_-)-d(V_+-V_-).
\end{aligned}
\]

Checker:
[`verify_h3_active_fan_omit_coloop_cartan_termwise_protected_gate.py`](../computations/verify_h3_active_fan_omit_coloop_cartan_termwise_protected_gate.py).

## Exact census

There are `105` matchings of eight sites and exactly `78` which omit both
`01` and `67`.  Endpoint transposition partitions them into `39` free
two-element orbits.  Equation (1) is checked on all `78` oriented terms and
equation (2) on all `39` orbits.

Every four-corner term has repeated-site degree

```text
(2,2,1,1,1,1,1,1),
```

the pure/two-site-mixed fine words are exactly the pivot words, and the
remote decorated matching tail is unchanged.  By number of remote tail
edges, the `39` endpoint orbits split as

```text
0 edges: 12 orbits
1 edge : 24 orbits
2 edges:  3 orbits.
```

Thus the proposed construction has no coefficient, matching, orientation,
word, fine, repeated-grade, or ordinary four-corner residue mismatch.  The
old abstract “one private coordinate may remain” guard is too weak at this
coefficient-shadow level: the literal physical prism determines the odd
U/V boundary exactly.

## Why this is not yet the protected Phi

The full protected comparison also has to transport the labelled Kähler
ridge and its eta/sigma readouts.  Its two halves occupy the site degrees

\[
 \deg(\gamma_{67})=e_6+e_7,\qquad
 \deg(\gamma_{01})=e_0+e_1.                           \tag{3}
\]

For every common tail degree `tau`,

\[
                 e_6+e_7+\tau\ne e_0+e_1+\tau.       \tag{4}
\]

This mismatch occurs on all `39` endpoint orbits.  Moreover, on the `27`
orbits with nonconstant remote tail `T`, the literal product rule is

\[
             -d(T\Omega)=T(-d\Omega)-\Omega\,dT.      \tag{5}
\]

The checker finds `30` distinct `Omega*dT` faces: `24` from the one-edge
tails and `6` from the three two-edge tails.  The fixed eta/sigma values are
also multiplied by `T` unless `T=1` in the terminal quotient.

These are not outside-shore matching holes.  They retain the selected Hall
support and differ in Kähler/operation tag.  No existing saturation theorem
turns them into a typed exit.  Consequently (2) constructs the exact
off-diagonal coefficient/residue row, but the implication

```text
literal Cartan boundary D  =>  complete protected Phi/q comparison
```

still fails at the ridge/readout layer.

## Shortest remaining addition

Construct a source-labelled shifted Kähler lift which keeps the `67` and
`01` halves of `-dOmega` as separate relative labels and transports eta and
sigma with the chosen Cartan sites.  After that lift, the existing physical
`q=M-a` quotient theorem applies: a nonzero comparison defect is a typed
witness, while a zero class is removed by protected rows.

So the active-fan shortcut is genuinely positive through the entire
matching/fine/ordinary-residue packet.  Its first exact failure is not a
fine word; it is the augmented ridge/readout.

## Scope and verification

This is exact at `h=3` for the literal `01`-coloop, `67`-direct-free response
packet and all `78` matching occurrences.  It is not an all-`h` theorem and
does not assert a full GHZ source counterexample.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
5061ab738d5bdacf416f8a3453e7cc6557fc3c91e4d3397abd74b144a6cc5a25
```
