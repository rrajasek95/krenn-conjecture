# Local $C_4$ coherence--curvature is a conditional relative square

This note isolates the exact theorem supplied by the local E2/E3
matching-exchange identities. The result is useful, but conditional: the
determinantal cells give a flat-homotopy/curved-carrier dichotomy only in the
literal localized source complex. They do not prove primitive source
saturation or zero indeterminacy.

## 1. The relative square

For matching bases $M,N$, put

$$
 a_c=\mu_M(c),\qquad b_c=\mu_N(c),\qquad
 P^M_{cd}=a_cH_d-a_dH_c,\qquad
 \Delta_{cd}=a_cb_d-a_db_c .
$$

The first endpoint form of E2 is

$$
 b_cP^M_{cd}-a_cP^N_{cd}=\Delta_{cd}H_c.       \tag{1}
$$

On the one-sided chart $D(a_cb_c)$, this is the cellular-square boundary

$$
 \frac{P^M_{cd}}{a_c}-\frac{P^N_{cd}}{b_c}
 =\frac{\Delta_{cd}}{a_cb_c}H_c.               \tag{2}
$$

Thus there is a precise dichotomy.

* On the flat fibre $\Delta_{cd}=0$, the two normalized transports are
  chain homotopic by the E2 square. This is genuinely **one-sided**: only
  $a_c,b_c$, not the opposite endpoint pivots, are inverted.
* Before any localization, the curved boundary contains the literal source
  term $\Delta_{cd}H_c$. On $D(\Delta_{cd})$, it exposes $H_c$ as the
  carrier.

For $M\mathbin\triangle N=C_4$, all terms in (1) have the alternating-cycle
factor times the common matching core. Consequently (1) is a literal
source-labelled relation before that core is cancelled.

## 2. Coherence is exact

For a third state $e$, E3 says

$$
\begin{aligned}
 C^{MN}_{cde}
 &=b_cP^M_{de}-b_dP^M_{ce}+b_eP^M_{cd}\\
 &=-a_cP^N_{de}+a_dP^N_{ce}-a_eP^N_{cd}\\
 &=-\bigl(\Delta_{de}H_c-\Delta_{ce}H_d
                  +\Delta_{cd}H_e\bigr).       \tag{3}
\end{aligned}
$$

This is the Bianchi face comparing the three relative squares. The two
row-Laplace E4 identities are its tetrahedral boundary, so the literal
undivided cells satisfy $\partial^2=0$. In particular, the curved carrier
in (2) is not an arbitrary remainder: its endpoint changes obey (3).

The exact chart-26 audit verifies the twelve ordered endpoint pairs, all four
E3 determinants, and both E4 boundaries. No matching-support census is used
in this formulation.

## 3. The two source gates

There are two separate operations which must not be hidden inside the word
"coherence."

First, let $g$ be the common $C_4$ matching core. Dividing the undivided cell
by $g$ is automatically legal over $R[g^{-1}]$. To promote the result to an
unlocalized primitive source relation, however, the relevant source-chain
and boundary modules must be $g$-saturated. Equivalently, the required colon
classes must vanish. A proof on the nonzero chart may use localization; a
proof in the global source ideal may not silently cancel $g$.

Second, restriction to the flat fibre should be treated as derived base
change unless the relevant $\Delta$-Tor vanishes. The square (2) still gives
a homotopy in the ordinary quotient, but new flat-fibre cycles can change a
chosen homotopy. If $K_{\rm flat}$ is the localized primitive relative
complex and $\varepsilon$ is the terminal physical readout, then the exact
zero-indeterminacy condition is

$$
          \varepsilon\bigl(H_1(K_{\rm flat})\bigr)=0.    \tag{4}
$$

A source-labelled contraction is a sufficient way to prove (4): the
corrected HPL augmentation
$\varepsilon(1+h\delta)^{-1}i$ kills transferred boundaries. Merely checking
$\partial^2=0$, or choosing one convenient lift, is not.

## 4. Sharp scope guard

The primitive chart-26 colon audit is an exact counterguard to the
unconditional master pattern. Its E3 and E4 cells remain coherent after
primitive normalization, yet both path-bearing degree-six classes remain
nonzero. Multiplication by every decorated coordinate of the alternating
$C_4$ still leaves the tested remainders irreducible by the complete lower
basis. One E2 family is lower-exact and the other merely transports the
remainder to $c_6g$ or $c_ag$.

Therefore the local master theorem is exactly:

> **Conditional $C_4$ coherence--curvature square.** After localizing the
> common matching core and the one-sided endpoint pivots, E2 gives flat
> source homotopy or curved literal carrier, and E3/E4 give its Bianchi
> coherence. This descends to a primitive, zero-indeterminate physical
> operation precisely after the source-saturation/base-change condition and
> (4) are supplied.

The missing theorem is not another $C_4$ identity. It is the global
source-saturation or contraction statement which kills the primitive
relative homology. Without it, the flat and curved formulas are correct but
do not close the clean-cap bridge.

## Verification

Run

```text
python3 computations/verify_local_c4_relative_coherence_curvature_square.py
```

The checker verifies E2, both presentations of E3, both E4 boundaries, the
linear zero-indeterminacy criterion, and pins the exact undivided/primitive
physical audits on which the scope statement depends. Its frozen ledger
digest is
`471c4106a4576bbd552e8ab51f1bbd08cda045c6a8b9aa3ad59b9949d6458426`.
