# A complete graph test for diagonal matching-cover exclusions

September 26, 2026. **Written proof with exact supporting replay; awaiting
independent audit.** This is a diagonal-source theorem. General off-diagonal
perturbations are outside its neighborhood conclusion.

[Guide](../explainers/BOUNDARY-STRUCTURE.md) ·
[Replay](../computations/boundary-structure-2026-09-26/README.md)

## 1. Recover a pure amplitude from mixed outputs

Take an even number \(n\ge4\) of sites and a diagonal complex source.
Write \(A_e^h=A_e(h,h)\), and \(\tau_h=\operatorname{haf}(A^h)\).
Fix color \(a\) and a set of edges \(D\) on which \(A_e^a\ne0\).
Suppose there are scalar edge weights \(\rho_e\), supported on \(D\), with

\[
                   \sum_{e\in M}\rho_e=1
             \quad\text{for every perfect matching }M.       \tag{1}
\]

For another color \(b\), the output word with \(a\) on the two endpoints
of \(e\) and \(b\) everywhere else has coefficient

\[
               H_{w(e,b)}=A_e^a\operatorname{haf}(A^b[V\setminus e]).
\]

Every perfect matching monomial appears with total weight one in (1), so

\[
 \boxed{\tau_b=\sum_{e\in D}\rho_e
                  \frac{A_e^b}{A_e^a}H_{w(e,b)}.}             \tag{2}
\]

This is an exact complex identity, with no restriction on cancellation.
Its denominator stays harmless in a neighborhood where the chosen
\(A_e^a\)'s remain bounded away from zero.

For six sites and three colors, the receiving word sets for \(b,c\) are
disjoint from one another and from the pure outputs. Put

\[
 s_h=\sum_{e\in D}\left|\rho_e A_e^h/A_e^a\right|^2
                  \quad(h=b,c).
\]

Equation (2) puts the output in a linear subspace in which each pure
amplitude is a specified linear functional of its corresponding mixed
outputs. Projecting the normalized GHZ target onto that subspace gives

\[
 \boxed{F\le\frac13\left(1+\frac{s_b}{1+s_b}
                              +\frac{s_c}{1+s_c}\right)<1.}   \tag{3}
\]

For one block, the subspace is \(\{(d x,x):x\in\mathbb C^k\}\); the
squared projection of the pure coordinate onto it is
\(\|d\|^2/(1+\|d\|^2)\). The three target coordinates lie in orthogonal
blocks, proving (3). Enlarging to this subspace gives a valid upper bound;
it need not be attainable by source weights.

## 2. Exactly when such a matching cover exists

Let \(G\) contain the edges outside \(D\). Then (1) has a solution
if and only if \(G\) has a bipartite connected component whose two parts
have different sizes. An isolated vertex counts as parts of sizes one and zero.

**Proof.** A constant matching-sum weight on \(K_n\) must have the form
\(\rho_{ij}=p_i+p_j\). Compare matchings differing only on four sites to
obtain
\(\rho_{ij}+\rho_{kl}=\rho_{ik}+\rho_{jl}=\rho_{il}+\rho_{jk}\).
These relations give vertex potentials, for example starting with
\(p_1=(\rho_{12}+\rho_{13}-\rho_{23})/2\).
Their sum must be one. Conversely, any vertex potentials with sum one give
matching sum one, because every vertex is used once.

Support on \(D\) means \(p_i+p_j=0\) on \(G\). Along a connected
bipartite component, the potentials alternate between a scalar and its
negative. Their contribution to the sum is that scalar times the difference
of the part sizes. An odd cycle forces the scalar to zero. Hence a nonzero
total sum exists exactly when some bipartite component is unbalanced.
Scaling its alternating potentials gives sum one. \(\square\)

Therefore a necessary condition for a normalized *diagonal* source limit
to admit \(F\to1\) is:

> For each target color, every bipartite component of the graph of its zero
> edges must have equally sized parts.

This is complete for certificates of the form (1), not a complete
classification of high-fidelity limits. The exact six-site census considers
all \(2^{15}=32768\) supports: 6510 admit this certificate and 26258 do not.
It verifies the cover against all 15 perfect matchings whenever one exists.
This count concerns support patterns, not a percentage of continuous sources.

## 3. Excluding a limit whose entire first derivative is zero

Let \(\omega^2+\omega+1=0\), \(|\omega|=1\). On sites \(0,1,2,3\),
give opposite pairs of color-\(a\) edges weights

\[
 A_{01}=A_{23}=1,\quad A_{02}=A_{13}=\omega,\quad
 A_{03}=A_{12}=\omega^2.
\]

Give all four color-\(a\) edges to site 4 weight one. Site 5 is isolated;
all other colors and endpoint pairs are zero. Call the resulting source
\(A_0\). It has squared norm ten.

Every four-site hafnian within the five-site core vanishes. For the first
four vertices it is \(1+\omega^2+\omega=0\); for a four-set containing
site 4 it is the sum of three triangle weights, again zero. Four-sets
containing site 5 also have zero output.

Thus \(H(A_0)=0\) and **all 135 columns of \(DH(A_0)\) vanish**.
All six old single-root response maps are zero, and all six augmented ranks
are only three. The earlier rank gates pass this limit.

However, the complement of its ten color-\(a\) edges is \(K_{1,5}\),
an unbalanced bipartite graph. Choose potential \(1/4\) at each core
vertex and \(-1/4\) at site 5. This gives \(\rho_e=1/2\) on all ten
core edges and zero on the others.

For a diagonal source with \(\|A-A_0\|\le\eta<1\), the selected
denominators have modulus at least \(1-\eta\), while the total squared
norm in colors \(b,c\) is at most \(\eta^2\). Hence

\[
 s_b+s_c\le\frac{\eta^2}{4(1-\eta)^2},\qquad
 F\le\frac13\left(1+\frac{\eta^2}{4(1-\eta)^2}\right).
\]

At \(\eta=1/100\), this gives

\[
                         F\le39205/117612<0.334.
\]

The package verifies the cancellations in the exact field \(\mathbb Q(\omega)\).
The neighborhood estimate is proved above and does not rely on numerical
sampling. Arbitrary complex *off-diagonal* perturbations of this same base
remain an unresolved case for the unrestricted rate problem.

## 4. Where this enters the universal rate proof

Equation (3) removes entire diagonal neighborhoods even when the first
derivative has no useful rank. The graph test is fast and produces explicit
identities, so it can precede expensive searches for high-order cancellation.
The missing step is to control the additional terms in (2) when the source
has off-diagonal endpoint colors; two cross-color edges can contribute to
the same receiving word. They cannot be silently discarded or bounded by
the diagonal argument.
