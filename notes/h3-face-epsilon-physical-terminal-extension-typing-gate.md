# Face epsilon versus the physical Cartan terminal

The actual Cartan terminal packet resolves one algebraic concern but does
not promote the clean face covector to a physical Fredholm separator.

The exact positive identity is

\[
 K_v(\eta_z)=1+\delta_{vz}\frac{u_z}{t},\qquad
 \sum_{v=1}^5 K_v(\eta_z)=5+\frac{u_z}{t}.             \tag{1}
\]

This is exactly opposite to the clean Omega response

\[
 \sum_v d\Omega_v(\eta_z)=-5-\frac{u_z}{t}.            \tag{2}
\]

The sigma response also cancels facewise: physical `K_v` has
`sigma=-q_pq^22`, the `-dOmega_v` value.  Thus the physical Cartan packet is
the correct eta/sigma compensation once a facewise Omega-to-rootless
comparison has been typed.

It is not itself that typing.  Three distinct spaces are involved:

| object | space | variance |
|---|---:|---|
| clean `epsilon=(1,1,1,1,1)` | five denominator face projections | covector |
| shared cut packet | 15 collision labels | input occurrences |
| `K_v`, `M_v=-O_alpha+K_v` | 360 literal lower features, Eq, eta/sigma | source columns |

The committed `271df91` theorem supplies the last row exactly.  It therefore
invalidates the old terminal-only cokernel from the unaudited probe.  But a
source column supplies an additional equation for a physical annihilator;
it does not turn the five-face covector into one.

Formally, promotion requires a covector `epsilon_tilde` on the complete
physical output such that

\[
 i^*\widetilde\epsilon=\epsilon,\qquad
 J_{\rm phys}^*\widetilde\epsilon=0.                    \tag{3}
\]

Equations (1)--(2) show what the terminal part of a solution to (3) must do.
They do not solve the literal lower/Eq equations.  In particular, there is
still no committed map from the 15 collision labels to the 360-feature
`M_v` boundary; comparing those packets directly is the circular step
isolated in `def89a3`.

So the updated verdict is:

* eta/sigma compatibility: **exactly correct**;
* old terminal-only separator: **superseded**;
* physical extension of the face epsilon: **not constructed**;
* Gate-I frontier: still the two labelled sections `d_fixed,d_pair` (or,
  dually, a direct solution of (3) on the complete physical codomain).

Verification is frozen by
`computations/verify_h3_face_epsilon_physical_terminal_extension_typing_gate.py`.
Its ledger digest is
`57b8ee4a80739da5bb9d192d4dde2b2410dbfdea948fd4e26f653ca35fdc0ba4`.
