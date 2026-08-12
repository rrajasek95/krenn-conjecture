# The order-six class and the five non-Euler polars require a covariance bridge

## Exact separation

The canonical endpoint-recoloured order-six class has common total
site-colour character

\[
 \gamma=(e_{x,0}-e_{x,1})
       +(e_{p,2}-e_{p,1})+(e_{q,2}-e_{q,1}).           \tag{1}
\]

For the odd word `12112`, the marked non-Euler polar on face (v) has
diagonal GHZ-stabilizer character

\[
 \chi_v=\sum_{i\in\{1,\ldots,5\}\setminus\{v\}}
                 (e_{i,0}-e_{i,m_i}).                 \tag{2}
\]

Modulo either the diagonal (GL_3) GHZ constraints or their sitewise
(SL_3) restriction, the five characters (2) have rank five and adjoining
(1) raises the rank to six.  In particular,

\[
                         \gamma\ne\chi_v
\]

for every face, and (gamma) is not in their span.  Thus the order-six
secondary class and the physical non-Euler polar are not two literal
presentations of one equivariant class.  A direct identification would lose
a genuine stabilizer weight.

Checker:
`computations/verify_h3_order6_to_polar_stabilizer_covariance_bridge.py`.

## The missing weights are seven-site covariance roots

The separation is completely structured.  Put

\[
                         \beta_v=\chi_v-\gamma .       \tag{3}
\]

Then (3) is the sum of exactly seven local colour roots, one at every site
except (v):

\[
\begin{aligned}
 \beta_v={}&(e_{x,1}-e_{x,0})
 +\sum_{i\in F_v}(e_{i,0}-e_{i,m_i})\\
 &+(e_{p,1}-e_{p,2})+(e_{q,1}-e_{q,2}).               \tag{4}
\end{aligned}
\]

Each root in (4) is an ordinary sitewise (GL_3) covariance direction on
the complete matching tensor.  Tensoring their seven comparison intervals
therefore gives a canonical covariance cube whose endpoints have weights
(gamma) and (chi_v).

The input colours of (4) are mixed: they contain colour zero at (x), the
two colours occurring in `12112` on (F_v), and colour two at (p,q).
Consequently the all-output endpoint kills the ternary GHZ target.  Every
other cube vertex contains a source derivation and is target-zero as well.
The complete covariance prism is therefore target-safe without a separate
target correction.

The seven-cube has 128 vertices, 448 edges, incidence rank 127, and one
normalized (H_0) class.  Hence it transports one endpoint to the other but
does not make either endpoint vanish by itself.  This is precisely the
scope guard found in the earlier normalized-bar calculation.

## Revised physical-comparison theorem

The first structural proof should no longer try to identify the order-six
class with each non-Euler polar.  It should prove the following composition:

1. start with the one canonical order-six endpoint-odd class of weight
   (gamma);
2. attach the target-zero covariance prism (4) for each face (v);
3. identify its all-source endpoint with the corresponding face of the
   canonical order-six Hasse totalization; and
4. read its all-output endpoint as the marked non-Euler polar of weight
   (chi_v), with the commuting ridge providing eta/sigma.

Only step 3 remains a source-chain assertion.  All weight shifts, target
rows, and prism signs are now forced.  If the two endpoints fail to glue in
the physical relative complex, their difference is the single relative
class to which the physical terminal generator/separator alternative must
be applied.

This replaces an opaque comparison by five copies of one explicit
seven-site covariance prism.  It also explains why bare sitewise covariance
was insufficient before the order-six theorem: covariance supplied the
prism but no source-provenant class at its all-derivation endpoint.  The
canonical order-six totalization is now the only possible endpoint filler.

## Scope

This is an exact stabilizer-character and covariance-cube theorem.  It does
not yet prove that the all-source endpoint equals the order-six physical
correction, kill the normalized (H_0) class, define the physical terminal,
or perform transverse-rank landing.

Verification:

```text
python3 computations/verify_h3_order6_to_polar_stabilizer_covariance_bridge.py
python3 -O computations/verify_h3_order6_to_polar_stabilizer_covariance_bridge.py
python3 -I -S computations/verify_h3_order6_to_polar_stabilizer_covariance_bridge.py
```

Frozen ledger SHA-256:

```text
6fb940267987ecbcdbf4a80c4be70bc2b300feb5fe1b728c233f475ea27b3a18
```
