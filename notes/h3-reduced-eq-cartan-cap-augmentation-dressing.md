# The Cartan packet completes exactly the full alpha Koszul face, not one rho pair

## Exact full augmented solve

Work in the canonical six pure-label component and retain literal lower,
Eq, `W`, target, labelled ordinary residue, physical anchor incidence, and
the seven eta/sigma terminal rows.  The old physical columns are

\[
\begin{aligned}
 r_{0,i}&=(B_i,\operatorname{Eq}_i,0,e_i,0,-1,0),\\
 T_i&=(0,0,-e_i,e_i,0,0,0),\\
 \varrho_i&=(0,0,e_i,0,e_i,0,0).
\end{aligned}                                             \tag{1}
\]

The one committed endpoint-odd Cartan packet has

\[
 K_\alpha=(0,0,0,0,\alpha,0,\tau),                       \tag{2}
\]

where

\[
 \alpha=(e_0-e_5)+(e_2-e_3)=(1,0,1,-1,0,-1)
\]

and `tau` is the pinned eta/sigma packet
`(1,1,1,1,1,1,-1)`.

Checker:
[`verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py`](../computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py).

## What the Koszul core must acquire

For each label, the primitive covector

\[
                     \lambda_i=B_i-\operatorname{Eq}_i     \tag{3}
\]

kills every column in (1)--(2) and the physical `M_v` packet.  It detects
the Eq-only normal Koszul cell.  Hence an Eq coefficient `-u` can enter the
physical span only after acquiring the literal lower/private coefficient
`-u` as well.

The independent physical covector

\[
                         \nu=\sum_i B_i+\operatorname{ainc} \tag{4}
\]

then forces anchor incidence `sum(u)`.  These are the first seven exact
augmentation conditions:

```text
lower = -u,   Eq = -u,   ainc = sum(u).
```

Thus `B_i=r0_i-T_i` does contribute the mandatory private/Eq/anchor
dressing, but it does not make that dressing disappear.  In particular,
an augmentation-one `u` cannot simultaneously have zero physical anchor
without a new primitive anchor cell.

## Cartan cancels residue, but forces the terminal

Put

\[
 B_u=\sum_i u_i(r_{0,i}-T_i),\qquad
 O_u=-B_u+\sum_i u_i\varrho_i.                           \tag{5}
\]

Then the complete signature of (5) is

```text
lower = Eq = -u
ainc = sum(u)
W = target = 0
labelled ores = u
terminal = 0.
```

Consequently (2) can cancel the residue in (5) exactly when

\[
                              u\in\mathbb Q\alpha.       \tag{6}
\]

For the full four-corner direction, (6) gives the already physical identity

\[
                         \boxed{O_\alpha-K_\alpha=-M_v}. \tag{7}
\]

This is a positive completion of the **alpha-decorated** Koszul core.  Its
augmentation dressing is not zero: it is the literal lower packet
`-alpha` together with terminal `-tau`.  Equation (7) is precisely the
physical `M_v=-O_alpha+K_alpha` theorem with signs reversed.

For the selected Gate-I odd packet, this closes the **output-side physical
augmentation** at normalized `Y=1`.  It does not yet close Gate I.  The
Koszul cell supplies the unaugmented `-F e_Eq` core, while (7) supplies the
physical augmented output.  One must still construct the source-labelled
comparison from the selected 15-label/Koszul lower input to the literal
lower boundary and terminal in `-M_v`.  The Koszul formula does not identify
those 15 labels or transport their private boundary by itself.

For one rho pair, however,

\[
 u_{05}=e_0-e_5,
 \qquad u_{23}=e_2-e_3,
 \qquad \alpha=u_{05}+u_{23}.                            \tag{8}
\]

Neither pair in (8) lies in the single line `Q alpha`.  Explicit primitive
dual rows annihilate all `r0,T,varrho,K_alpha,M_v` columns and take value one
on the corresponding nearest lift.  For example, with
`w=e0+e3`,

\[
 \lambda_w=-\operatorname{Eq}_w+W_w+operatorname{target}_w
                    -\operatorname{ores}_w               \tag{9}
\]

has `w dot alpha=0` but `w dot u05=1`.  The analogous witness for `u23` is
`w=e2+e5`.  No choice of the Cartan coefficient or its eta/sigma terminal
can change these pairings.

Therefore the residue obstruction identified in `6d63293` is canceled for
the complete alpha packet, but not for an individual rho-paired label orbit.
The true remaining quotient after the mandatory private/anchor dressing is

\[
                         [u]\in\mathbb Q^6/\mathbb Q\alpha, \tag{10}
\]

with the eta/sigma terminal coefficient forced whenever (10) vanishes.

## Scope and next theorem

Only one canonical placed Cartan line is currently source-provenant in this
literal grade.  The 75 abstract alpha placements in the complete private
census do not prove that their Cartan terminals are physical in all those
placements.  A physical equivariant Cartan orbit spanning the entire
zero-sum hyperplane would complete every rho-odd `u`; that orbit is not yet
constructed.

The physical terminal

\[
                         q=\sum_6m_i-\operatorname{ainc}
\]

is also not determined by this row solve.  It retains the exact protected
quotient condition `[q_target Phi-q_source]=0`; a nonzero defect gives the
relative-generator branch once both rows are physically typed.

The selected Gate-I chain uses the full alpha output direction and hence its
output is already completed by (7).  Its remaining theorem is the input-side
15-label comparison just stated.  For any argument which isolates one pair
in (8), a second independent placed Cartan/residue-terminal line is still
needed.  The augmentation-one/even lane additionally needs the independent
primitive anchor cell detected by (4).

## Verification

```text
python3 computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py
python3 -O computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py
python3 -I -S computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py
```

Frozen ledger SHA-256:

```text
9764fecdf999c799e0a4aefb5ed90ce9897e6f6b6b779f200052ad86220ecff2
```
