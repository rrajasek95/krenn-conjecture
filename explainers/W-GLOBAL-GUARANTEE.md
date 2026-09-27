# How close is the known W design to the best possible?

[All explainers](README.md) · [W project](../research/w-state-design/README.md) ·
[Proof and exact checks](../computations/w-universal-factor-two-2026-09-27/README.md)

We now have a global guarantee: **at every even site count, the known
construction achieves more than half the best possible exact W-state rate**.
This allows arbitrary complex weights and colored edges.
We still have not proved that the construction is globally optimal.

**Evidence:** written proof with exact supporting checks; independent
audit pending. This result is separate from the Lean-verified Krenn–Gu theorem.

## The remaining numerical gap

The rate compares output strength with the source strength needed to
produce it. It is unchanged when the whole source is rescaled.
For $n=2m$ sites, write

$$
B_n=\frac{((n-1)!!)^2}{\binom n2^{\,m}}.
$$

The construction achieves $R_*=nB_n/((n-1)^2+1)$.
Every exact W design now satisfies $R\le2B_n/n$.

| Sites | Known construction | No design can exceed | Construction achieves at least this fraction of the optimum |
| --- | ---: | ---: | ---: |
| 4 | $1/10$ | $1/8$ | $80\%$ |
| 6 | $1/65$ | $1/45$ | $9/13\approx69.2\%$ |
| 8 | $9/3136$ | $225/50176$ | $64\%$ |
| 10 | $49/83025$ | $49/50625$ | $25/41\approx61.0\%$ |

The guarantee approaches 50% as the number of sites grows.
The actual construction may be optimal; the table states what the
current unrestricted proof guarantees.

## Why the zero ground output helps

A W state has exactly one excited site. Its all-ground amplitude is
zero. Call the ground-edge matrix $D$.
The all-ground matching sum is the hafnian of $D$, so
$\operatorname{haf}(D)=0$.

Deleting two sites leaves a smaller matching sum, called a cofactor.
This measures how strongly changing their edge affects the ground output.
The same cofactors determine how efficiently single-excitation source
entries can produce each W coefficient.

~~~mermaid
flowchart LR
    A["Exact W output"] --> B["Ground hafnian is zero"]
    B --> C["Sharp bound on total cofactor strength"]
    C --> D["A source cost for each excited site"]
    D --> E["Universal rate bound: 2 B_n / n"]
~~~

Earlier we bounded the cofactors without fully using the zero ground
amplitude. The new argument uses it directly.

## The circle trick

Think first of any homogeneous polynomial $P$ of degree $m$.
Suppose we know a bound on its size in terms of the input length.
At a point $z$ where $P(z)=0$, choose a unit direction $v$ giving
the strongest first response.

Homogeneity implies that $v$ is perpendicular to $z$ in the complex
Euclidean inner product. Now perturb along a circle:

$$
z+t e^{i\theta}v,\qquad 0\le\theta\le2\pi.
$$

Every input on this circle has the same length.
The output is a sum of terms oscillating at different frequencies:

$$
a_1t e^{i\theta}+a_2t^2e^{2i\theta}+\cdots+a_mt^me^{im\theta}.
$$

Average the squared output over the circle. Cross terms between
different frequencies cancel. What remains is

$$
|a_1|^2t^2+|a_2|^2t^4+\cdots+|a_m|^2t^{2m}.
$$

Every term is nonnegative. The known output bound therefore limits
the first response $|a_1|$, even when higher terms are present.
Choosing $t^2=1/(m-1)$ gives the strongest bound from this argument.

~~~mermaid
flowchart TD
    A["Rotate a perturbation through every complex phase"] --> B["Input norm stays fixed"]
    A --> C["Output terms rotate at different frequencies"]
    C --> D["Averaging squared output removes cross terms"]
    B --> E["Known polynomial norm bound"]
    D --> F["First response plus nonnegative higher responses"]
    E --> G["A sharp cap on first-response strength"]
    F --> G
~~~

For the hafnian, the derivative entries are precisely the cofactors.
The bound is sharp: an isolated site next to a complete odd core
attains it. This is also the ground structure of the known W design.

## What a better design would have to change

Large total response is only one requirement. The W state asks for
equal output at every site. Uneven response strengths waste source
strength at the weaker sites.

The known construction maximizes total cofactor strength but has
uneven response rows. Any better design would have to make those
rows more uniform while retaining enough total response.
The proof now quantifies both effects separately.

## Maximum response now forces the known ground structure

A [further theorem](../notes/w-cofactor-rigidity-2026-09-27.md) classifies
the equality case for every even count from six onward.
If the ground source reaches the largest possible total cofactor
strength, it must be a complete equal-magnitude odd core with one
isolated site, up to relabeling, scale, and site phases.

The circle argument explains why. Equality forces every source around
the circle to saturate the scalar hafnian bound. Their edge magnitudes
must all agree. Rotating the phase then shows that a ground edge and
its cofactor cannot both be nonzero.
Every perfect matching must contain exactly one cofactor-supported
edge. In a complete graph on at least six sites, the only edge set
with that property is a full star. Its complement is the odd core.

~~~mermaid
flowchart TD
    A["Maximum total cofactor response"] --> B["Every source on the derivative circle saturates the norm bound"]
    B --> C["Ground and cofactor supports are disjoint"]
    C --> D["Every perfect matching uses exactly one cofactor edge"]
    D --> E["Cofactor edges form a star"]
    E --> F["Ground edges form the known complete odd core"]
~~~

The next step is local stability. The scalar response cost increases
to second order in every direction away from this family, after
removing scaling and phases. This remains true when the ground
perturbation is nonuniform and introduces cancelling perfect matchings.

Together, these results show that **no design with sufficiently
near-maximal cofactor efficiency can beat the known rate**.
Only the ground source needs to be in this regime; all its colored
completions are covered.

The proof does not yet give a numerical meaning to “sufficiently near.”
It therefore leaves the numerical interval in the table unchanged.
A better global design, if one exists, must sacrifice a definite
amount of total response while making the site responses more uniform.
Establishing that this tradeoff can never pay is still the remaining task.
