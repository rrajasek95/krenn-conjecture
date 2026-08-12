# The clean-C5 aggregate separator sees a physical stabilizer kernel

## Exact verdict

The clean (R=0) denominator theorem forces

\[
                   \epsilon(\operatorname{im}\tau)=0,
\]

so the coarse endpoint/Tor module has the explicit separator which gives
value one to every

\[
                 \Omega_v,\qquad q_{v,N},\qquad r_v
\]

and value zero to Eq, (W), target, ordinary residue, and anchor
incidence.  That separator does **not** automatically descend through the
full physical source kernel.  The first failing columns already occur at
first order; no endpoint-tail Hessian or Fitting minor is needed.

Work on the marked direct-cell open

\[
                         t=q_{pq}^{00}\ne0.
\]

For each odd auxiliary site (z\in\{1,\ldots,5\}), take the
colour-diagonal weights

\[
                 \mu_{p,0}=1,\qquad \mu_{z,0}=-1,
\]

with every other weight zero, and normalize the resulting physical vector
field by (t):

\[
                         \eta_z=X_\mu/t.               \tag{1}
\]

The colourwise weight sums vanish.  Hence (1) is a literal tangent to the
complete GHZ source equation:

\[
                         J\eta_z=0.                    \tag{2}
\]

It is the same source-provenant non-Euler stabilizer family pinned in the
marked-polar theorem, not a formal endpoint column.

## Exact separator pairing

Recall

\[
 \Omega_v=(q_{pq}^{22}-q_{pq}^{00})
          -(q_{xv}^{0m_v}-q_{xv}^{00}).                \tag{3}
\]

Put (u_z=q_{xz}^{00}).  Since \((\eta_z)_t=1\), while all selected
nonzero-colour internal cells are fixed, direct substitution in (3) gives

\[
 d\Omega_v(\eta_z)=
 \begin{cases}
 -1,&v\ne z,\\
 -1-u_z/t,&v=z.
 \end{cases}                                          \tag{4}
\]

Every (q_{v,N}) uses only odd sites with the selected colours (1,2).
The weights in (1) are supported in colour zero, so

\[
                         \eta_z(q_{v,N})=0             \tag{5}
\]

for all fifteen companion monomials.  The five normalized C5 cells are
also fixed; thus (1) preserves (R=0) and (h_v=1) coefficientwise.
Equations (2) and (5) give zero physical target and zero ordinary residue.
There is no rootless (r)-component in the currently defined source
correction inventory.

Consequently the aggregate separator evaluates on this physical kernel
column as

\[
                  \boxed{\Lambda(\eta_z)=-5-u_z/t.}   \tag{6}
\]

This is an identity in the localized coefficient ring.  Therefore the
coarse separator is not automatically a functional on the full physical
cokernel.  Killing all five automatic kernel columns would require the
additional relations

\[
                     u_z+5t=0\qquad(z=1,\ldots,5).    \tag{7}
\]

No committed common-(q) or full-nine theorem proves (7).

## Exact missing datum

The first exhaustivity datum is now sharp.  One needs either

1. a source-provenant terminal comparison/correction which assigns to
   (eta_z) a compensating (q)- or rootless-(r) value and preserves
   target and ordinary residue; or
2. a proof from the complete physical source equations that every marked
   clean-C5 source satisfies (7).

The first option is precisely the zero-indeterminacy part of the missing
(Omega\)-to-rootless-ridge comparison.  Merely adjoining the scalar
separator from the denominator module does not supply it.

This also places the endpoint-Jacobian/Fitting program correctly.  Its
tail-normal strata are secondary: (6) is a first-order physical kernel
obstruction already on the exact clean slice.  A later Fitting analysis can
only be promoted after its terminal readout has been made invariant under
(1).

## Scope

This is an exact conditional theorem on the marked (t\ne0) clean-C5
packet.  It does not construct a full rootless source, prove that the five
relations (7) are inconsistent, or disprove a differently corrected
terminal functional.  It proves only—and exactly—that the explicit coarse
separator does not automatically annihilate the complete physical source
kernel.

Run:

```text
python3 computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py
python3 -O computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py
python3 -I -S computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py
```

Frozen ledger SHA-256:

```text
52f9a814e400edec24a7f82b4a19984655631243ea25d18545679c6458d23618
```
