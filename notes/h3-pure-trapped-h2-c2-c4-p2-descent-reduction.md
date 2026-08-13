# The pure trapped second face leaves one pointed carrier or one four-site cell

## Finite descent theorem

The literal classification in `1480f7d` leaves exactly three all-pure,
fully trapped response faces:

```text
C2+   d*q_uv + p_u*s_v + p_v*s_u,
C4    q_ab*q_cd + q_ac*q_bd + q_ad*q_bc,
P2    s_a*q_bc + s_b*q_ac + s_c*q_ab
      (or the p-reverse).
```

Composing each type with the strongest committed placement theorem gives
the following exhaustive finite alternative.

1. A literal centered occurrence row is nonzero.  This is the required
   occurrence-asymmetric pointed `P_f` source type.
2. A one-matching `C4` support has literal restricted coloops.
3. A `C4` already in the normalized target-coloop packet routes by the
   punctured-cube alternate-target theorem.
4. The only remaining object is one tail-covariant, same-grade relative
   `C4` placement on four residual sites.

There is no further six-site Hasse topology and no independent `C2+` target
generator.

Checker:
[`verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py`](../computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py).

## The centered occurrence identity

For `N` literal occurrences put

\[
                         C_N=NI-J.
\]

Over characteristic zero,

\[
 C_N^2=NC_N,qquad \operatorname {rank}C_N=N-1,
 \qquad
 u={\sum_i u_i\over N}\mathbf1+{1\over N}C_Nu.      \tag{1}
\]

The `i`th pointed contrast

\[
                 P_i=e_i^*-{1\over N}\mathbf1^*      \tag{2}
\]

satisfies

\[
                         P_i(u)={(C_Nu)_i\over N}.    \tag{3}

Thus every nonconstant lower coefficient packet canonically exhibits an
occurrence-asymmetric pointed row.  This is stronger than saying that an
abstract quotient is nonzero: (2) names the literal occurrence and its
complete-row correction.

## `P2`: the source-side construction is already finite

For the twelve ordered endpoint occurrences, the committed relative graph
resolution adjoins `z,t` and generators `theta,phi` with

\[
 d\theta_i=z_i-u_i,qquad
 d\phi_i=t_i-(C_{12}z)_i.
\]

The universal section

\[
 \Gamma_i=\phi_i+\sum_j(C_{12})_{ij}\theta_j
\]

has

\[
                         d\Gamma_i=t_i-(C_{12}u)_i.   \tag{4}

This is a presentation-safe resolution of the old physical coefficient
algebra when `t=C_12u` is retained.  It already supplies the labelled
two-root square and the full reinsertion product rule, including the `dq`
face.

For the exact private `B-4` preimage, eight explicit `Gamma_i` combine to

\[
                   d\Gamma_{z_{\rm priv}}
                     =t_{z_{\rm priv}}-z_{\rm priv}(u). \tag{5}

The selected vector has sum zero, so
`C_12 z_priv=12 z_priv != 0`.  Therefore the entire fixed `P2` debt reduces
to one selected carrier line `t_zpriv`.  The ambient endpoint-even carrier
has rank five, but no five independent construction theorems are needed for
this chosen face.

The still-open step is physical rather than combinatorial:

> Land `t_zpriv` in the complete augmented cap complex with its target,
> Eq, labelled `Q/ores`, anchor, physical-`q`, `W`, eta/sigma, word/fine,
> and repeated-grade readouts.

Setting `t=0` is not allowed; it imposes the occurrence equations on the
old classical fibre.

## `C2+`: no independent target problem remains

The order-two diagonal trace jet and root-decorated Koszul cell already form
the minimal sigma-covariant cone which cancels the mixed target and root
reduced-Eq values of both lower cuts.  Its exact residual data are fixed:

```text
complete Eq       -delta_plus,
labelled residue   v=(B1+B4)/2,
word objects       0112/q23 and 0121/q45,
root-word dressing lower +E / ores -E.
```

The literal Hasse value is undefined only because the source-labelled `P2`
placement has not been supplied.  Consequently `C2+` introduces no new
target-bearing theorem: it composes with (5) and leaves the same physical
`t_zpriv` landing, with the fixed decorations above.

## `C4`: exact support/value split

A four-site hafnian has three literal matching values `u=(u0,u1,u2)`.
Apply (1) with `N=3`.

- If only one `u_i` is nonzero, its two `q` edges occur in every supported
  restricted matching.  They are literal four-site coloops.
- If two values are nonzero, or three values are not all equal, then
  `C_3u != 0`; equation (3) gives an explicit three-occurrence pointed row.
- If all three values are equal and nonzero, `C_3u=0`.  The packet is the
  symmetric flat `K4` face and has no occurrence-asymmetric debt.

For the normalized target-coloop chart, the committed punctured-cube
identity closes the last flat rectangles by alternate pure-target
reselection or an offanchor active exit.  This uses its selected endpoint
and common-tail hypotheses and is not a generic `C4` theorem.

Outside that normalized chart, the strongest general result isolates one
strictly smaller cell:

```text
tail-covariant protected relative-C4 restriction/insertion primitive,
domain: four residual sites / three matching occurrences,
grade: the actual word, fine, and repeated-edge label of the H2 face.
```

Coefficient translations and canonical symmetries do not supply its tail;
in particular they cannot identify it with `P2`, whose operation and
repeated-edge grade differ.

## Updated frontier

The pure trapped second-order branch is therefore no longer “construct
three lower theories.”  It is:

```text
P2 or C2+ asymmetric face
        -> explicit centered line t_zpriv
        -> one physical augmented P_f-type landing

C4 face
        +-- singleton support -> restricted coloop
        +-- asymmetric values -> explicit P_i row
        +-- normalized flat   -> punctured-cube closure
        `-- generic flat      -> one four-site relative-C4 placement
```

This theorem does not declare the final two physical placements constructed.
It isolates them literally and shows that every other coefficient, target,
root, symmetry, and Hasse-coherence issue is already resolved.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
recorded by the checker.
