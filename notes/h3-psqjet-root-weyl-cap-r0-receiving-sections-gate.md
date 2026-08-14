# Root/Weyl plus tied `r0` does not construct either receiving section

## Outcome

The relative source is now settled: the full Boolean/Kähler presentation
contains

\[
 d(q_{01}b^-)=dq_{01}b^-+q_{01}db^-
\]

with carrier boundary `d(q01*u^-)` and all fifteen signed product-rule face
pairs.  The strongest source-provenant attempt to receive this carrier in
the balanced cap is to use the two target-safe root/Weyl transports and the
physical tied `r0` packet.

That attempt does not construct a section.  Root/Weyl lies in the response
corner `e_R A e_R`; `r0` and its cap normalizers lie in the cap corner
`e_C A e_C`.  Since `e_C e_R=e_R e_C=0`, compositions of these operations
remain diagonal.  The missing map lies in the independent corner

\[
                      e_C A e_R.
\]

Thus a formal tensor product of a response Weyl homotopy and `r0` is not a
physical operation-changing composition.

Exact checker:
[`verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py`](../computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py).

## Literal two-root quotient

There are two required naturality instances:

| root label | local repair | domain | cap target |
|---|---|---|---|
| `AB` | `A/B`, root `0<->1` | `11110000=11:110000`, ordered response heads `01/10` | `01211222`, `AugP2/K_Eq r0` |
| `AC` | `A/C`, root `0<->2` | same relative carrier, separately root-labelled | same tied cap, separately root-labelled |

The source fine packet has six signed `P4+K2` tail pairs and three signed
`4K2` `dq01` pairs, with repeated sites `0,1`.  The cap has the six
`t*q_(v,N)` occurrence degrees in repeated `P3+K2`.  Signed Weyl transport
may recolour the response word, but it preserves the underlying matching,
repeated-edge label, Hasse direction tag, and response operation parent.  It
therefore cannot turn the transported carrier into the cap object.

The checker makes the no-go stronger by granting every diagonal
word/head/fine/repeated/operation repair independently.  Per root it retains

```text
id_response, id_cap, Hom(response,cap),
word_response, word_cap,
head_response, head_cap,
fine_response, fine_cap,
repeated_response, repeated_cap,
operation_response, operation_cap.
```

Only `Hom(response,cap)` is withheld.  The exact ranks are

```text
strong diagonal base                             24
+ AB section                                     25
+ AC section alone                               25
+ one root-forgetting sum AB+AC                  25
+ both separately labelled sections              26.
```

Hence the section quotient is two-dimensional.  Its primitive covectors are
the two root-labelled Hom characters

\[
                 \omega^{\rm Hom}_{AB},\qquad
                 \omega^{\rm Hom}_{AC}.
\]

One labelled section leaves the other character.  One unlabelled aggregate
leaves the anti-diagonal character

\[
       (\omega^{\rm Hom}_{AB}-\omega^{\rm Hom}_{AC})/2.
\]

This is the precise sense in which one section is rank-insufficient.  The
shortest positive datum is one physical `Phi_KS,r0` constructor natural in
the root label and instantiated on both `A/B` and `A/C`; it must carry the
displayed word, head, fine, repeated, and operation incidences.

## It is not the terminal bright `omega_0102`

The first Hom covectors and the terminal control occupy different degrees
and have different augmented signatures.

| datum | degree and shadow | `B/Eq` signature | `Psi` |
|---|---|---|---:|
| two receiving sections | degree-zero; visible `d(q01*u^-)`/selected-`db01` carrier | land in tied `r0`: `(delta,delta)` | `0` |
| `omega_0102` | primitive degree-one; canonical shadow `0` | untied boundary `(delta,0)` | `4` |

The section schema is the missing degree-zero parent of the eight standard
`K_Eq` naturality interchanges.  Those interchanges remain tied and
`Psi`-dark.  The formal `omega_0102` is instead the possible independent
ninth degree-one primitive used by the terminal census as its bright
counterguard.  Constructing the two sections neither fills nor excludes it.

The two objects share only the broad operation orientation
`response -> cap`; they are not the same class.

## Scope and verification

This is exact for the canonical `h=3` relative `PSQJet_01` domain, the two
signed-Weyl root transports, balanced protected `r0`, and the fully labelled
two-root quotient.  It is not a global no-go for an unregistered physical
operation-changing primitive.

Run:

```text
python3 computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py --mode all
python3 computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py --mode candidate
python3 computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py --mode sections
python3 computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py --mode terminal
python3 -O computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py --mode all
python3 -I -S computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py --mode all
```

Frozen ledger SHA-256:

```text
d65cf3b7c2e7528badc87c6e7c36cd1d17e1be11f2cbc6e812225cbf590ee229
```
