# The W design is locally optimal at every even size

[All explainers](README.md) · [W-state project](../research/w-state-design/README.md) ·
[Proof and replay](../computations/w-all-even-local-optimum-2026-09-27/README.md)

For every even number of sites from four onward, the known one-root
design is a local optimum among all complex colored sources producing
the exact W state. Any sufficiently small change that preserves the
target must either preserve the rate through a known symmetry or make
the rate worse.

**Evidence:** written proof with exact supporting checks; independent
audit pending. A better design far away is still possible. The
unrestricted global optimum remains open.

## What is being optimized?

The W output has exactly one excited site, with the same amplitude
at every possible site. If $H=\lambda W_n$ and $S$ is the sum of
squared source-entry magnitudes, the mathematical rate is

$$
R=\frac{n|\lambda|^2}{S^{n/2}}.
$$

Multiplying all source entries by a common factor changes numerator
and denominator equally. We can therefore fix $\lambda$ and minimize
the source strength $S$.

The known design has one distinguished root and a complete odd core.
Every core edge emits only ground colors. Each root edge can excite
either its core endpoint or the root, in a carefully chosen ratio.
Every matching uses exactly one root edge.

~~~mermaid
flowchart LR
    A["Complete odd core: ground-only edges"] --> C["Each matching uses one root edge"]
    B["Root arms: excite either endpoint"] --> C
    C --> D["Exactly one excitation in every surviving output"]
    D --> E["Equal W amplitudes after choosing the root-arm ratio"]
~~~

For $N=n-1$ core sites, one convenient normalization is

$$
A_{\rm core}=
\begin{pmatrix}\sqrt{N^2+1}&0\\0&0\end{pmatrix},
\qquad
A_{\rm root}=
\begin{pmatrix}0&N\\1&0\end{pmatrix}.
$$

The root matrix's row specifies the root color and its column the
core color. This gives rate $1/10$ at four sites and $1/65$ at six.
The formula for every even size is on the project page.

## “Local” now allows every source entry to change

The previous all-size results covered particular architectural classes.
The earlier unrestricted local proof covered six sites.
The new local theorem allows all of the following at every even size:

- New complex ground couplings at the root.
- Excitations on edges inside the core.
- Entries exciting both ends of an edge.
- Arbitrary phases and additional endpoint colors.

The output must remain exactly W. The theorem gives a neighborhood of
the displayed design, not a numerical radius.

~~~mermaid
flowchart TD
    A["Any sufficiently small complex source change"] --> B{"Output remains exactly W?"}
    B -->|Yes| C{"Only a phase or overall scale symmetry?"}
    C -->|Yes| D["Same rate"]
    C -->|No| E["Strictly smaller rate"]
    B -->|No| F["Outside the exact-W optimization problem"]
~~~

## Why the calculation works at every size

At an optimum, the first change in source strength vanishes along
allowed directions. The next test is the quadratic change.
It is obtained from a Lagrangian: source strength minus weighted
output constraints.

The odd core treats every site in the same way. A perturbation of its
edges can be split into a common change, changes associated with
individual sites, and a remainder whose row sums vanish.
The excitation entries have a similar decomposition.

In these coordinates, the quadratic change becomes a short list of
squared norms with explicit coefficients. For every even $n\ge6$,
all coefficients controlling real changes are positive.
For imaginary changes, the only zero directions are site phases.

Those phases multiply edge $ij$ by $e^{i(\theta_i+\theta_j)}$.
Every matching picks up $e^{i\sum_i\theta_i}$, so choosing
$\sum_i\theta_i=0$ preserves both the output and source strength.
The proof shows that there are no other local equality directions
after the amplitude is fixed.

The coefficient formulas hold for all sizes. The replay separately
enumerates matchings and checks every quadratic coefficient through
twelve sites.

## Four sites expose an additional mathematical idea

At four sites, the straightforward quadratic test has negative
directions. One might interpret them as ways to improve the design.
But the linearized output equations admit directions that the exact
equations do not allow.

The proof follows three mixed-entry row sums, $s_1,s_2,s_3$.
For an actual feasible source at distance $\rho$ from the design,
higher-excitation outputs force

$$
s_1+s_2+s_3=0,\qquad
\sum_i s_i^2=O(\rho^3),\qquad
s_1s_2s_3=O(\rho^4).
$$

Together these imply $s_i=O(\rho^{4/3})$. The potentially negative
quadratic contribution is therefore only $O(\rho^{8/3})$, smaller
than the positive terms of order $\rho^2$.

An exact example illustrates why both extra constraints matter:

~~~mermaid
flowchart LR
    A["A direction with negative quadratic cost"] --> B["Passes the linear output equations"]
    B --> C["Second-order output errors can all be canceled"]
    C --> D["Third-order all-excited output is -3"]
    D --> E["No higher source coefficient can repair that term"]
~~~

This is useful beyond the W problem. When constraints are singular,
a negative direction in their linearized kernel need not correspond
to any feasible improvement. Higher equations can settle a question
that the Hessian alone leaves unresolved.

## What we gain, and what remains

At fixed output, moving away from the local phase orbit costs at least
a constant times squared distance. Thus near-optimal designs within
this neighborhood must be close to the known family.
The constants depend on the site count; the proof does not supply
an explicit experimental tolerance.

This establishes the known design's unrestricted local optimality at
every even size.
To establish global optimality, we still need to exclude a better
exact W design elsewhere in source space, including nonuniform
ground cores with cancelling perfect matchings.
