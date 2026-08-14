# The normalized coloop submatching contracts only before the chart operation

## Result

There is a genuine positive coefficient fact in the proposed shortcut.  On
an evaluated normalized pure word with active coloop `q01`, the three pure
matching occurrences through `q01` have sum

\[
 a=q_{01}H_{2345}=1,
 \qquad
 H_{2345}=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.       \tag{1}
\]

Thus their submatching Koszul vector is a normalized contraction.  This does
not make the contraction chart-specific or source-valid under the `pq/pr`
restriction operations.  Every currently source-provenant matching identity,
including the selected submatching sum, is global and therefore appears with
the diagonal operation tag.

The exact conditional positive theorem is the following.  Let `U` be the
absolute global contraction and suppose a new physical chain `X` has the
`pq`-specific boundary

\[
 dU=e_{pq}+e_{pr},\qquad dX=Ae_{pq}.                    \tag{2}
\]

Then

\[
 \boxed{d(2X-AU)=A(e_{pq}-e_{pr})=A t.}                \tag{3}
\]

Consequently, if `A` is a same-grade source unit and all proper faces of `X`
have been totalized,

\[
 \boxed{\Eta=2A^{-1}X-U,\qquad d\Eta=t.}               \tag{4}
\]

Without the unit, (3) leaves exactly one cyclic class `(R/(A))*t`; proving
that it vanishes is the previously isolated full-core saturation/colon
theorem.  More importantly, neither a unit nor saturation constructs the
`pq` operation tag in (2).  If the sector chain is diagonal, subtracting it
from `U` has no chart-odd component even after localization.

For the direct response sector in Gate II,

\[
 A=Dq_{01}H_{2345}=D                                  \tag{5}
\]

on the coloop locus (1).  The coloop equation does not make `D` a unit.  The
lower normalization therefore removes the pure cofactor but not the capped
direction factor, the restriction/insertion faces, or the occurrence-block
projector.  The proposed shortcut does not presently give `dEta=t`; after a
genuine chart lift it either gives (4), or merely restates full-core
saturation.

Exact checker:
[`verify_h3_trapped_coloop_chart_submatching_contraction_gate.py`](../computations/verify_h3_trapped_coloop_chart_submatching_contraction_gate.py).

## 1. The exact coloop unit and its scope

There are fifteen perfect matchings on the six pure sites `0,...,5`.
Exactly three contain `q01`; their residual tails are the three terms of
`H2345`.  Split the normalized pure row as

\[
 H_c=a+b=1,                                            \tag{6}
\]

where `a` is the `q01` sector and `b` contains the other twelve matchings.
For a literal active coloop every nonzero pure matching contains `q01`, so
`b=0` at the source and (1) follows.

If `e_M` are the matching Koszul generators, put

\[
 u_{\rm all}=\sum_Me_M,
 \qquad
 u_{01}=\sum_{M\ni01}e_M.                             \tag{7}
\]

At the evaluated coloop,

\[
 \iota(u_{\rm all})=1,
 \qquad
 \iota(u_{01})=a=1.                                   \tag{8}
\]

The checker realizes this non-symmetrically with sector weights
`(1/5,2/5,2/5)` and zero complement.  Hence the assertion is not a rank-one
symmetry artifact.

Two scope guards are essential.

First, pure normalization without the coloop gives only `a+b=1`; a proper
sector need not be a unit.  The universal counterguard is

```text
sector sum = A, complement sum = 1-A.
```

Second, (8) is a matching-coefficient/Koszul statement.  Even under the
favourable grant that all individual matching Koszul generators are physical,
their sum remains a global pure-word chain.  Selecting the summands which
contain `q01` does not say that restriction to the `pq` chart was applied
before the contraction.  Thus it does not assign a chart operation tag.

If only the single absolute global homotopy `u_all` is granted, rather than
all individual matching generators, the inference to `u01` is weaker still:
the submatching vector has not even been supplied as a source chain.

## 2. Operation tag is independent of normalization

Let

\[
 V_{\rm op}=Re_{pq}\oplus Re_{pr},
 \qquad e_+=e_{pq}+e_{pr},
 \qquad t=e_-=e_{pq}-e_{pr}.                          \tag{9}
\]

A global matching identity is displayed in both charts with the same
coefficient, hence with tag `e+`.  A selected global submatching identity is
still global.  Its boundary has the form

\[
                         A e_+.                       \tag{10}
\]

The two columns `e+` and `A e+` have rank one for every value of `A`.
Inverting `A` changes no operation tag, so (10) cannot reach `t`.

By contrast, granting the genuinely chart-labelled `X` of (2) gives the
boundary matrix

\[
 \begin{pmatrix}1&A\\1&0\end{pmatrix},                \tag{11}
\]

whose determinant is `-A`.  Equation (3) is the explicit Smith relation.
On `D(A)` the matrix has full rank and (4) follows.  On the fibre `A=0`, the
second column vanishes and the sign line survives.  Thus before localization
the exact remaining quotient is

\[
                         (R/(A))t.                     \tag{12}
\]

Equivalently, if a complete physical image is known to be `A`-saturated,
then (3) implies `t` is a boundary.  Asking saturation to perform this last
cancellation is precisely the common-core colon problem; it is not a new
consequence of the pure matching normalization.

Characteristic zero matters only in using the coefficient `2` in (3).  Two
separately constructed `pq` and `pr` sector chains would give `t` by their
difference without that normalization, but constructing those two chains is
the same missing operation-labelled lift.

## 3. Why the direct `Dq01` chart is not the lower pure sector

The direct Gate-II response block is

\[
 Dq_{01}H_{2345},                                     \tag{13}
\]

not merely the pure cofactor in (1).  Substituting the exact coloop equation
reduces (13) to `D`; it does not reduce it to one.  The elementary assignment

```text
q01=2, H2345=1/2, D=0
```

satisfies the normalized coloop equation and kills (13).  This is a guard on
the stated hypotheses, not a claim that this assignment is a complete GHZ
source.  It proves that the active-coloop equation alone cannot authorize
division by the full direct core.

There is also a typed distinction.  The known lower candidate is

```text
U_C4[D,Q01;2345] -> H2345.
```

Capping it by `D*q01` has the principal-parts boundary

\[
 \delta((Dq_{01})U)
 =Dq_{01}\delta U
  +(\delta D)q_{01}U
  +D(\delta q_{01})U.                                 \tag{14}
\]

The last two terms are independent direction/reinsertion faces.  Dividing
the coefficient in the first term does not cancel them.  Moreover the direct
nine-term block is only part of the complete 105-term response.  The exact
identity

\[
 L_{01}=3Dq_{01}H_{2345}-R_{01}                       \tag{15}

\]
still needs a source-valid projector isolating `R01`, or one combined pointed
cell whose boundary is `L01`.  The pure coloop contraction supplies neither.

Thus there are two separate scalar stages:

1. `q01*H2345=1` removes the lower pure matching coefficient;
2. a same-grade inverse or saturation for the *full capped core* removes the
   remaining `D` factor after a physical chart-labelled cap exists.

Conflating these stages silently discards both the operation tag and (14).

## 4. Exact shortest positive theorem

The shortcut becomes a proof if and only if the following source data are
added in the literal decorated grade.

1. Construct one restriction-before-contraction chain `X` with boundary
   `A*e_pq`, rather than a global identity expanded in both charts.
2. Totalize its `delta-D`, `delta-q01`, tail, word/fine/repeated, response-head,
   and occurrence-block faces.
3. Retain target, anchor/ainc, physical `q`, `W`, labelled residue/ridge,
   eta, and sigma rows.
4. Prove the full coefficient `A` is a same-grade unit, or prove the complete
   physical image is `A`-saturated.

Then (3)--(4) give `dEta=t` with no further matching algebra.  At the lower
pure coloop level `a=1`, so item 4 is automatic there; items 1--3 are still
not.  At the capped direct-response level `A=D`, so all four items remain.

This cleanly separates the two possible readings of the shortcut:

```text
global or selected matching contraction, diagonal tag
    -> no chart-odd boundary, even after localization;

new source-valid pq-tagged contraction X
    -> A*t is a boundary;
    -> t is a boundary exactly after full-core unit/saturation.
```

## 5. Scope

This is exact for the canonical `h=3` coloop coefficient packet, the
matching Koszul differential, the two chart-operation rows, and the literal
capped principal-parts faces.  The evaluated three-term coloop sector is a
physical pure-word coefficient packet.  The note does not construct a new
finite tensor satisfying every GHZ equation, does not claim the formal
matching Koszul basis is already the full decorated source complex, and does
not exhibit an accepted augmented terminal.

The conclusion is therefore a sharp conditional theorem/counterguard:
normalization genuinely contracts the lower sector, but source-valid chart
oddness is an independent lift; once that lift exists, any remaining scalar
cancellation is exactly the full-core saturation problem already on the
frontier.

## Verification

Run

```text
python3 computations/verify_h3_trapped_coloop_chart_submatching_contraction_gate.py
python3 -O computations/verify_h3_trapped_coloop_chart_submatching_contraction_gate.py
python3 -I -S computations/verify_h3_trapped_coloop_chart_submatching_contraction_gate.py
```

The checker pins the global operation-tag theorem, the active-coloop tail
partition, the generic C4 core-saturation theorem, the capped-C4 response
decomposition, and the Gate-II relative landing.  It verifies the 15/3/12
matching census, an exact normalized nonuniform coloop sector, the diagonal
versus chart-specific ranks, (3)--(4), the `(R/(A))*t` fibre, the `D=0`
capped-core guard, and independence of the two proper reinsertion faces.

Frozen ledger SHA-256:

```text
62a758fc868a853ecb33f88d6f7cfc4303e05119658ce8eb90fcc4af876b5232
```
