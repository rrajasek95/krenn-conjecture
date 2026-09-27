# A star can prevent arbitrarily high GHZ fidelity

[All explainers](README.md) · [GHZ project](../research/ghz-rates/README.md) ·
[Proof](../notes/ghz-star-fidelity-gap-2026-09-27.md) ·
[Exact replay](../computations/ghz-star-fidelity-gap-2026-09-27/README.md)

A useful consequence of the earlier proof identities is stronger than
our recent onset estimate: **every full-support single-color zero has
a neighborhood whose GHZ fidelity stays below one**.

The result works at every even site count of at least four. Its status is
**written proof with exact supporting checks; independent audit pending**.
The unrestricted square-root rate law remains open.

## The obstruction is a star, not a matrix rank

Choose a site and one target color, say red. Look at its red–red
connection to every other site:

~~~mermaid
flowchart TD
    P["Root"] ---|"red–red"| A["1"]
    P ---|"red–red"| B["2"]
    P ---|"red–red"| C["3"]
    P ---|"red–red"| D["4"]
    P ---|"red–red"| E["5"]
~~~

If all these entries are nonzero, multiply them:

$$
z=A_{p1}(\mathrm{red},\mathrm{red})\cdots
  A_{p5}(\mathrm{red},\mathrm{red}).
$$

This product is an auxiliary response coefficient. The five edges
are not a physical perfect matching: they share a root. The proof
identities let us examine this auxiliary coefficient anyway.

Write the actual output as $H=\lambda\Delta+E$, where $\Delta$ is the
three-color GHZ sum. The new estimate, with source strength normalized
to one, is

$$
\|E\|\ge \kappa_n |z|^2|\lambda|.
$$

The positive constant depends only on the number of sites. If $z$
stays bounded away from zero, the error cannot become arbitrarily small
relative to the signal. Thus the fidelity has a fixed ceiling:

$$
F=\frac{3|\lambda|^2}{3|\lambda|^2+\|E\|^2}<1.
$$

The available constants are very conservative. The useful conclusion
is the exclusion of a whole type of limiting source.

## Why the last coefficient settles it

An earlier proof step encodes the auxiliary responses in an even
polynomial $g$. At six sites it has degree at most four. Approximate
GHZ output forces a small residual in

$$
g(s/\sqrt2)^2-g(s).
$$

Suppose the coefficient of $s^4$ is $w$. The coefficient of $s^8$ in
this residual is exactly $w^2/16$. No lower term can cancel it:

~~~mermaid
flowchart LR
    A["g has degree at most 4"] --> B["Its square has a degree-8 term"]
    B --> C["Subtracting g cannot remove that term"]
    C --> D["Small residual bounds the highest coefficient"]
    D --> E["A nonzero star forces signal-relative error"]
~~~

Here $w=z/\lambda$. Keeping the powers of $\lambda$ in the earlier
residual bound gives the displayed error estimate. Complex phases
do not evade this step: the absolute value of $z^2$ is $|z|^2$.

The earlier rate proof extracted a low-degree coefficient to control
general sources. Extracting the highest coefficient instead gives
this useful local exclusion.

## A broader test uses whole columns of an edge block

The argument also constrains limits with off-color entries. At a
possible limit of fidelity approaching one:

> For every root and every pair of receiving colors, some neighbor must
> have both corresponding columns of its edge block equal to zero.

For the receiving pair red and blue, such a block has the form

$$
\begin{pmatrix}
0&0&*\\
0&0&*\\
0&0&*
\end{pmatrix}.
$$

Rows are root colors; columns are neighbor colors. The stars are
unrestricted entries. The qualifying neighbor can differ for another
root or another color pair.

Why whole columns? The highest response is a product of one linear
factor per neighbor. Its coefficients must all vanish on that
two-color palette. A product of ordinary complex polynomials is zero
only if some factor is zero, which here means both columns vanish.

This is a necessary support test, not a recipe for attaining high fidelity.

## What changes in the proof program

At a full-support single-color zero, every root has the nonzero star
described above. All such zeros are therefore excluded, including the
example with derivative rank 25.

~~~mermaid
flowchart TD
    A["Candidate high-fidelity limit"] --> B{"Required two-column zeros present?"}
    B -->|"No"| C["Excluded: a local fidelity ceiling"]
    B -->|"Yes"| D["Still a candidate; examine error versus signal"]
    E["Full-support single-color zero"] --> C
    D --> F["Unrestricted square-root problem remains open"]
~~~

The [earlier fifth-power onset proof](FULL-SUPPORT-ONSET.md) bounded
the signal using both error and distance from the ground source.
The new result removes the distance term for this boundary class.
Its previous response identities and exact examples remain useful,
but this class no longer needs a separate square-root argument.

Sparse limits, including singular two-triangle configurations and
other cancelling sources that pass the support test, still require work.
No universal rate exponent has been improved by this exclusion alone.
