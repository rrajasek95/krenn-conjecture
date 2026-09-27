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

## A balanced competitor is another local minimum

At six sites we have found and proved a second local minimum of the
scalar response cost. It has no isolated site: all fifteen ground edges
are present, and their matching contributions cancel.

~~~mermaid
flowchart LR
    A["Triple A: all three internal weights are +√(2/3)"]
    B["Triple B: all three internal weights are −√(2/3)"]
    A ---|"All nine cross edges have weight 1"| B
~~~

The ground matching sum is $9abc+6c^3$, where $a,b$ are the
within-triple weights and $c$ is the cross weight. Here $ab=-2/3$
and $c=1$, so the sum is zero.
Unlike the one-root ground, this source has equal response strength
at every site. That perfect balance costs some total response.

The scalar cost measures the ground strength together with the
minimum excitation strength needed for the six desired coefficients.
Lower cost gives a better upper bound on rate.

| Ground source | Scalar cost | Consequence for exact W rate |
| --- | ---: | --- |
| Known one-root family | $520/9\approx57.778$ | $1/65$ is attained |
| Balanced cancellation family | $117/2=58.5$ | Strictly below $(80/81)(1/65)$ |

The difference in scalar cost is only **1.25%**.
Nevertheless, the balanced source cannot improve the known design.
The [new proof](../notes/w-state-balanced-three-plus-three-2026-09-27.md)
establishes this throughout the symmetric three-weight family.
It also checks every complex perturbation of the balanced source,
including changes that break all its visible symmetry.
After removing scaling and phases, all 21 remaining directions
increase the scalar cost to second order.

This explains a concrete hurdle for the global proof. Local descent
in the scalar problem can settle near this second minimum instead
of the lower one-root minimum. A proof that every local minimum is
the known construction would therefore be false.
We now exclude a neighborhood of this competitor as well.

The scalar relaxation only enforces the desired single-excitation
coefficients. At its minimum-row completion, the unwanted
two-excitation coefficients have nonzero sum. The balanced scalar
minimum is therefore **not a proved local optimum of exact W design**,
and its scalar rate bound cannot be attained by an exact W source.
The unrestricted global optimum remains open.

## The same competitor can now be excluded at every even size

The six-site calculation extends to two groups of $m$ sites each,
with one weight inside each group and a third weight between them.
The other colored source entries can be chosen freely.
A [new all-even argument](../notes/w-state-equal-split-legendre-2026-09-27.md)
proves that every exact W design with this ground structure has

$$
R<\frac{80}{81}R_*,\qquad n=2m\ge6.
$$

This settles the whole three-weight family, including unequal weight
magnitudes, every way its ground matchings can cancel, and the cases
where the two groups are disconnected.

~~~mermaid
flowchart TD
    A["Two groups of m sites; three ground weights"] --> B["Count matchings by how many pairs stay inside each group"]
    B --> C["The cancellation equation is a Legendre polynomial"]
    C --> D["Its roots list every cancellation branch"]
    D --> E["Unequal magnitudes increase the scalar cost"]
    E --> F["At balance, a classical polynomial bound controls the cost"]
    F --> G["Every colored completion has rate below 80/81 of the known design"]
~~~

Legendre polynomials are familiar from approximation and integration.
Here they arise because the coefficients count the possible matchings.
Their roots turn a complex cancellation problem into a finite list
of real cases at each size.

There is a second useful connection. Once the two groups have equal
weight magnitudes, the scalar response cost can be written using
the weights from **Gauss–Legendre quadrature**, a method for integrating
polynomials exactly using finitely many sample points. A standard
bound on these polynomials controls every sufficiently large size
at once. Exact rational identities handle the five smaller cases.

The penalty also grows with size. From 16 sites onward, a proved
upper bound on this family's rate, relative to the known design,
shrinks by a factor of $2/3$ for every extra pair of sites.
This describes the bound, not the exact optimal rate of the family.

The useful lesson is that complete ground support and perfectly
balanced response rows do not by themselves improve W production.
This whole symmetric alternative pays too much in total response
cost. The unrestricted problem still allows independently varying
ground edges and remains open.

## Unequal groups give a small algebraic optimization problem

The two groups need not have the same size. The matching count then
becomes a **Gegenbauer polynomial**, a family that includes Legendre
polynomials as a special case. Its roots again list every cancellation
branch.

Once a branch is fixed, scaling and phases leave just one positive
real parameter. The scalar response cost is an explicit rational
function of that parameter. Its derivative vanishes at roots of a
polynomial of degree **six**, regardless of the number of sites.
The lowest scalar cost must occur at one of those finitely many
positive roots.

This is useful because the source problem originally has many complex
entries and exact cancellation constraints. Within the two-group
ground family, we can work with one real variable and prove bounds
for all its possible values. The other colored entries remain free.

The [new results](../notes/w-state-two-group-reduction-2026-09-27.md) are:

| Ground structure | What is proved |
| --- | --- |
| One site and a uniform odd core | The known rate is attained and optimal at every even size |
| Two sites and the remaining sites | Rate is strictly below $5/6$ of the known rate at every even size from six onward |
| Two equal groups | Rate is strictly below $80/81$ of the known rate at every even size from six onward |
| Any two-group split, from six through forty sites | The known rate is optimal; every split with at least two sites in each group has a strict gap |

~~~mermaid
flowchart TD
    A["Choose the two group sizes"] --> B["Polynomial roots list all ground cancellations"]
    B --> C["One positive parameter remains on each branch"]
    C --> D["A degree-six equation lists possible scalar minima"]
    C --> E["Exact interval arithmetic proves a bound for the whole branch"]
    E --> F["615 certified branches cover every unequal split through forty sites"]
    F --> G["Together with the equal-split proof: the known rate is optimal in this ground family"]
~~~

The finite certificates cover every parameter value on every listed
branch. They are stronger than checking many numerical examples.
They use rational root intervals and positive polynomial coefficients
on subdivisions of a fixed interval.

Forty sites is the endpoint of the verified catalog, not a claim
about all larger unequal splits. The general reduction remains valid
there, but a uniform proof is still needed. These results also leave
ground sources without two-group symmetry outside their scope.
