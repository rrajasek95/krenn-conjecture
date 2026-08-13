# Three inputs suffice for the full generic C-plus dressing

This is a conditional assembly theorem. Assume the physical constructions
of:

1. the sigma-covariant shifted `P2` placement, including its literal
   one-endpoint/reinsertion faces and hidden root-private face;
2. the pointed reduced-Eq comparison; and
3. the pure fixed-plane residue section
   `d_even=(B1+B4)/2` isolated in `6c5303c`.

Then no fourth lower/Eq/target/residue cell is needed.

Checker:
[`verify_h3_cplus_conditional_physical_dressing_assembly.py`](../computations/verify_h3_cplus_conditional_physical_dressing_assembly.py).

## The root-word dressing identity

Put

\[
 v={B_1+B_4\over2},\qquad
 E=2D_{\rm root}\otimes v,qquad
 D_{\rm root}=(-1,1,-1,1).
\]

The old physical nearest lift is

\[
 O_{-E}=(\operatorname{lower},\operatorname{Eq},
          \operatorname{ores}_{\rm root})=(E,E,-E).
\]

The placed `P2` comparison supplies the hidden private face `(-E,0,0)`.
Root decoration of the pure section `d_even` supplies `(0,0,+E)`.
Therefore

\[
 \boxed{
 (-E,0,0)+(E,E,-E)+(0,0,E)=(0,E,0).}                \tag{1}
\]

The right side is exactly the clean physical root-decorated `K_Eq` face.
This explains the division of labor:

- `P2` cancels the private lower debt;
- `d_even` cancels the labelled root-residue debt;
- `O_{-E}` carries the desired Eq coefficient.

Commit `3993094` proved that Cartan/Mv bars alone cannot produce (1). The
two added hypotheses supply exactly the two coordinates detected there.

## Substitution into the target/Eq triangle

The already proved order-two triangle is

\[
\begin{array}{c|cc}
 &\operatorname{target}&\operatorname{Eq}_{\rm root}\\ \hline
 B_{\rm endpoint}&+E&0\\
 C_{P_2,+}(J_*)&-E&-E\\
 K_{\rm Eq}&0&+E.
\end{array}
\]

Its sum is zero. Substituting (1) for the last row makes this a fully
physical identity. Separately, the complete-column packet satisfies

\[
 M_{\delta}=(\delta_+,\delta_+),\qquad
 \Phi(K_{\rm Eq})=(0,-\delta_+),
\]

so their sum is `(lower delta+, Eq 0)`. Finally an undecorated copy of
`d_even` supplies the prescribed ordinary residue `v`.

The total core signature is consequently

```text
direct landing                 v
complete lower                 delta+
complete Eq debt               0
root-private debt              0
root-Eq debt                   0
mixed-target debt              0
word-resolved root-ores debt   0
labelled ordinary residue      v
anchor incidence              -1
```

This is the full generic C-plus carrier in the main boundary rows.

## What remains augmented

The construction does not turn every augmented law into a coefficient
identity.

- `W` reduces to the one compatibility equation
  `W(P2 total)+W(Phi_KEq)=0`. Endpoint-evenness does not prove it.
- Physical `q` needs the pointed comparison to be `q`-horizontal. If its
  defect is nonzero, the existing protected relative-generator theorem is
  already the correct exit.
- The anchor is not missing: its desired value is `ainc=-1`. Once `P2` is a
  source-valid placement and the comparison is pointed at the source-algebra
  level, functoriality gives this carrier its physical anchor meaning.
- Eta/sigma reduce to one terminal equation between the `P2` totalization
  and the pointed `K_Eq` image. `O_-E` and `d_even` have zero terminal.

Thus the remaining work is compatibility/naturality on `W`, `q`, and the
rho-even terminal ridge, not another lower, target, Eq, or residue
generator. The theorem is generic. The beta-zero `D0` face follows only if
the pointed comparison is constructed integrally over `k[beta]`; otherwise
it remains the existing Bockstein/Saturation gate.

## Verification

```text
python3 computations/verify_h3_cplus_conditional_physical_dressing_assembly.py
python3 -O computations/verify_h3_cplus_conditional_physical_dressing_assembly.py
python3 -I -S computations/verify_h3_cplus_conditional_physical_dressing_assembly.py
```

Frozen ledger SHA-256:

```text
a101dbfd2d611a242fb2d7da8ef5b56b07f686fd60ffd375497dee782206fafe
```
