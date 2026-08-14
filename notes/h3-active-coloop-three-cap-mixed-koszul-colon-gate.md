# The active-coloop chart does not create the mixed three-cap cell

## Verdict

On the active-coloop chart

```text
q01*H2345 = 1
```

the factors `q01` and `H2345` are units, but the chart factors `D`,
`D*q01`, `p*s`, and the three-cap equation `R01` are not.  In the normalized
source ring the literal three chart monomials are

\[
 A=DqH=D,\qquad B=psH=q^{-1}ps,\qquad
 C=rtH=q^{-1}rt,
\]

and hence

\[
 R_{01}=A+B+C=D+q^{-1}(ps+rt).                 \tag{1}
\]

The canonical resolution of the one hypersurface equation (1) has one odd
generator and no pairwise DQ/PS two-cell.  A formal mixed Koszul cell exists
only after replacing the one equation by the split ideal `(A,B,C)`; that
replacement changes `H0`.  Before localization the common factor `H` does
produce a Tor class, but it is supported on `H=0` and vanishes when `qH=1`.
Thus it cannot be reused on the active chart without silently restating a
saturation hypothesis.

The formal split cell also does not determine the required cap landing.
Its canonical reduced-`Eq` projection is dark, while the same square
boundary is compatible with every value

\[
 \delta\mathbin{\cdot}(B-Eq)=4\lambda,
 \qquad \lambda\in\mathbb Q.                   \tag{2}
\]

Consequently the active-coloop localization constructs no source-valid
chi-bright `kappa_mix`.

Exact checker:
[`verify_h3_active_coloop_three_cap_mixed_koszul_colon_gate.py`](../computations/verify_h3_active_coloop_three_cap_mixed_koszul_colon_gate.py).

## 1. What the active coloop actually inverts

Work in

\[
 S=\mathbb Q[q^{\pm1},D,p,s,r,t],\qquad H=q^{-1}.
\]

The relation `qH=1` makes both `q` and `H` units.  It does not make a
coefficient carrying `D`, `p`, or `r` a unit.  The literal point

```text
q=2, H=1/2, D=0, p=0, r=0, s=t=1
```

satisfies the active-coloop relation but has

```text
A=B=C=R01=0.
```

This is the smallest zero-denominator counterguard.  A contraction using
`1/D`, `1/(D*q)`, `1/(p*s)`, or `1/R01` discards a branch that is still
present in the literal trapped chart.

Moreover, (1) is monic and irreducible as a polynomial in `D` over the
Laurent coefficient UFD.  It is coprime to both `D*q` and `p*s`.  Therefore

\[
 (R_{01}):H^\infty=(R_{01}):q^\infty
 =(R_{01}):(Dq)^\infty=(R_{01}):(ps)^\infty=(R_{01}). \tag{3}
\]

There is no hidden chart-specific class in any of these colons.  For the
pair ideal itself,

\[
 (A,B)=(D,ps),\qquad
 \operatorname{Syz}(D,ps)=S\,(ps,-D),             \tag{4}
\]

with `(D):ps=(D)` and `(ps):D=(ps)`.  In particular `1` is not in the pair
ideal.

## 2. One hypersurface versus three split equations

The presentation-safe resolution of the source hypersurface is simply

\[
 0\longrightarrow S e_f
 \mathop{\longrightarrow}^{R_{01}} S
 \longrightarrow S/(R_{01})\longrightarrow0.       \tag{5}
\]

Equivalently, the Koszul DGA has one odd generator `e_f` with
`d(e_f)=R01`; over characteristic zero, `e_f^2=0`.  There is no canonical
degree-two generator whose boundary distinguishes the DQ summand `A` from
the PS summand `B`.

If instead one declares three degree-one generators with boundaries
`A,B,C`, the split Koszul complex has the familiar pairwise cells

\[
 \begin{aligned}
 d\kappa_{AB}&=B e_A-Ae_B,\\
 d\kappa_{AC}&=C e_A-Ae_C,\\
 d\kappa_{BC}&=C e_B-Be_C.
 \end{aligned}                                      \tag{6}
\]

Their boundaries are exact syzygies, but this complex resolves

\[
 S/(A,B,C)=S/(D,ps,rt),                              \tag{7}
\]

not `S/(A+B+C)`.  The distinction is physical rather than cosmetic.  At

```text
q=H=1, D=1, p=1, s=-1, r=0
```

one has `R01=0` while `A=1` and `B=-1`.  Thus the point belongs to the
original hypersurface and is removed by the split presentation.  Calling
`kappa_AB` in (6) a canonical cell of (5) changes `H0`.

## 3. The common-H Tor line vanishes on the active chart

Before imposing `qH=1`, set

\[
 A_0=HDq,\qquad B_0=Hps
\]

in the polynomial ring `S0=Q[H,q,D,p,s,r,t]`.  The monomial identities are

\[
 (A_0)\cap(B_0)=(HDqps),\qquad
 (A_0)(B_0)=(H^2Dqps).                              \tag{8}
\]

Hence

\[
 \operatorname{Tor}_1^{S_0}(S_0/(A_0),S_0/(B_0))
 \cong (S_0/(H))[HDqps].                            \tag{9}
\]

The same support appears in the common-factor colon quotient

\[
 ((Hg):H)=(g),\qquad (g)/(Hg)\cong(S_0/(H))g.       \tag{10}
\]

Equations (9) and (10) are killed when `H` becomes a unit.  Therefore the
active chart does not turn the Tor carrier into an absolute mixed cell; it
annihilates it.  Retaining it after localization is precisely the extra
relative/saturation datum that the construction was meant to derive.

## 4. First proper faces of the formal split cell

Even if the H0-changing split cell `kappa_AB` is retained as a relative
carrier, its first product-rule boundary is

\[
 dB\,e_A+B\,d e_A-dA\,e_B-A\,d e_B.                \tag{11}
\]

Before using `qH=1`, the coefficient faces are

```text
dA = (dD)qH + D(dq)H + Dq(dH),
dB = (dp)sH + p(ds)H + ps(dH).
```

The literal fixed-window occurrence census is:

| family | number of terms |
|---|---:|
| each `dD,dq,dp,ds` factor times the three `H2345` matchings | 3 |
| each `Dq*dH` or `ps*dH` tail packet | 6 |
| total A-side coefficient faces | 12 |
| total B-side coefficient faces | 12 |
| coefficient PP faces altogether | 24 |
| carrier reinsertion families | 2 |

The differentiated active relation gives `H*dq+q*dH=0`, so the algebraic
forms reduce to

\[
 dA=dD,\qquad
 dB=sH\,dp+pH\,ds-psH^2\,dq.                       \tag{12}
\]

This cancellation is coefficientwise.  It does not erase the operation,
occurrence, removed-edge, word, or fine labels of the physical PP rows.

The physical opposite-root squares begin instead with

```text
-D*s1*H, +p0*q*H, -D*s0*H, +p1*q*H.
```

Restoring the complete response produces four independent signed 24-term
collision splitters.  Their selected PP boundaries contain 48 flags.  The
shared unary return `qH` becomes the scalar one on the active chart, but it
is still the selected three-of-fifteen occurrence vector, not the complete
unary row.  The first forward lower cofactor is operation type `DSQ`, whose
`DS` lower idempotent is absent; the reverse `PQQ` cofactor has `P2`
topology but remains in the response word/fine degree rather than the cap
degree.  Thus (11) does not totalize the physical labelled square.

## 5. Private/reduced-Eq augmentation remains independent

For the signless formal private tops, use

```text
u_AB=(1,0,1,0),  u_AC=(1,0,0,1),
delta=(1,1,-1,-1).
```

With `chi=delta.(B-Eq)`, both formal tops have `chi=0` when the Eq projection
is zero, and also when Eq is tied to the private top.  An independently
adjoined balanced Eq face changes the value, but neither (5), (6), nor
`qH=1` selects it.

The exact square-augmentation quotient already has one free coordinate:

\[
 \Pi_{B/Eq}(\kappa)\equiv\lambda(\delta,0)
 \pmod{\text{old cap rows}},
 \qquad \chi=4\lambda.                              \tag{13}
\]

A dark filler (`lambda=0`) and a bright filler (`lambda=1`) have the same
source square boundary and both satisfy `d^2=0`.  The active-coloop identity
is an equality in the coefficient ring and gives no chain map from the
formal Koszul carrier to the corner-resolved cap Eq rows.  It therefore
does not choose `lambda`.

## Shortest remaining positive datum

The shortest positive hypothesis is not another scalar localization.  It
is one source-labelled pointed DQ/PS mapping-cylinder two-cell for the
single-equation source (5), together with:

1. the four signed 24-term complete-response collision splitters;
2. the selected-unary occurrence return and its complete-row comparison;
3. the forward `DSQ` and reverse `PQQ` lower faces, including the response-
   to-cap word/fine descent; and
4. a physical private/reduced-`Eq` law fixing a nonzero value of `lambda`
   in (13).

Without that datum the construction is exactly a relative carrier plus an
unfixed augmentation, not an absolute chi-bright column.

## Verification

Run

```text
python3 computations/verify_h3_active_coloop_three_cap_mixed_koszul_colon_gate.py
python3 -O computations/verify_h3_active_coloop_three_cap_mixed_koszul_colon_gate.py
python3 -I -S computations/verify_h3_active_coloop_three_cap_mixed_koszul_colon_gate.py
```

Frozen ledger digest:

```text
d1e697f5a173c5056c6460c2ae5e71139f8c3413fe61f9aed60d24099908b216
```
