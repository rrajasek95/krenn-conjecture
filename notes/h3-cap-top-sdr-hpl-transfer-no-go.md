# The cap top projection is not an SDR; its universal HPL repair is the missing P2 cell

## Exact obstruction

On the canonical cap orbit, write \(N\) for the full translated Hasse chain,
\(B=r_0-T\) for its top coefficient, and \(Y=Yw\).  The derived and physical
local differentials are

\[
 dN=Y,
 \qquad
 dB=Y+(H_0-u)e_{\mathrm{Eq}}.
\]

Thus the fixed top projection has rank-one chain defect

\[
 [d,\pi_{\mathrm{top}}]N=(H_0-u)e_{\mathrm{Eq}}.
\]

It cannot be the projection in a strong deformation retract.  Indeed, for
every homotopy \(h\), \([d,dh+hd]=0\); consequently an identity
\(dh+hd=1-i\pi\) forces \(i\pi\), and hence the projection in an SDR, to be a
chain map.  The nonzero Eq class violates this condition before any transfer
formula can be applied.  In particular, \(pAhAi\) is not a defined physical
HPL operation for the unaugmented top projection.

## Universal one-cell repair

The minimal formal repair is unique.  Adjoin one degree-one cell \(K\) with

\[
 dK=(H_0-u)e_{\mathrm{Eq}}.
\]

Use degree-one basis \((B,K)\), degree-zero basis \((Y,\mathrm{Eq})\), split
differential

\[
 d_0=\begin{pmatrix}1&0\\0&1\end{pmatrix},
 \qquad
 \Delta=\begin{pmatrix}0&0\\1&0\end{pmatrix},
\]

and the standard contraction \(h(\mathrm{Eq})=K\), \(h(Y)=0\).  The checker
verifies both SDR identities exactly.  Homological perturbation gives

\[
 -h\Delta i(N)=-K,
 \qquad
 i'(N)=B-K,
 \qquad
 d(B-K)=Y.
\]

Since \(\Delta K=0\), all higher terms vanish.  With the coefficient of \(B\)
normalized to one, the coefficient \(-1\) of \(K\) is forced modulo adding a
degree-one cycle.

This computation is also the no-go: the retraction kills \(K\).  Hence the
projected higher correction is zero.  Cubical/HPL transfer cancels the Eq
defect only inside the contractible translated-Hasse/Eq fibre; it does not
turn that fibre into a physical response-to-cap arrow.

## Physical grade debt

For source provenance, \(K\) must be realized, not merely adjoined, in the
two sigma-paired operation grades

\[
 0112/q_{23{:}21}/P2,
 \qquad
 0121/q_{45{:}12}/P2.
\]

The current literal source category has no response-to-cap Hom in that local
orbit.  The universal contraction carries no word/fine/repeated/operation
label selecting these objects.  If such a labelled \(K\) is supplied, its
first Hasse/Leibniz face is the already forced \(0102/dq_{23{:}21}\) conormal,
detected by \(+e_0+e_3-e_1-e_6\) with value \(35/72\), together with its
\(dq_{45{:}12}\) sigma mate.

Therefore HPL does not remove the remaining theorem: it identifies it
canonically as the existence of one endpoint-even, sigma-covariant,
occurrence-local P2 cell \(K\) with the protected lower/ores faces.

## Scope

This is an exact rational theorem for the normalized local orbit and the
standard two-by-two SDR/HPL series.  It proves that the proposed
\(\pi_{\mathrm{top}}\)-based transfer is unavailable in the current physical
presentation and that the universal correction is derived/off-operation
grade.  It does not rule out a new source constructor realizing the required
P2-labelled \(K\).

Run:

```bash
python3 computations/verify_h3_cap_top_sdr_hpl_transfer_no_go.py --mode all
python3 computations/verify_h3_cap_top_sdr_hpl_transfer_no_go.py --mode obstruction
python3 computations/verify_h3_cap_top_sdr_hpl_transfer_no_go.py --mode repair
python3 computations/verify_h3_cap_top_sdr_hpl_transfer_no_go.py --mode physical
```

Frozen ledger:

```text
e2316ed92ad68bc9caf7bc52fa052b47e03f2572f508ed26bd3debd8f6783441
```
