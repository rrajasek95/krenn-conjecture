# Optimal W-state design

[All subprojects](../README.md) · [Illustrated methods guide](../../explainers/METHOD-UTILITY.md)

The W state has one excited site, equally distributed over all sites. This
project asks which complex weighted source produces it exactly with the
largest scale-invariant rate.

**Status:** written proofs with exact supporting checks; independent audit
pending. The global unrestricted optimum is open, including at six sites.

## The attained rate and its proved scope

For $n=2m\ge4$, define

$$
B_n=\frac{((n-1)!!)^2}{\binom n2^{\,m}},
\qquad
R_*=\frac{nB_n}{(n-1)^2+1}.
$$

A one-root source with a complete odd core attains $R_*$. This is the
optimum within the one-root and scalar-core two-root families. The broader
theorem permits arbitrary complex colored entries and assumes only that
the support of the ground-color entries has **no perfect matching**.
Within this class, $R_*$ is the exact optimum at every even site count.

| Sites | Attained rate $R_*$ |
| --- | --- |
| 4 | $1/10$ |
| 6 | $1/65$ |
| 8 | $9/3136$ |
| 10 | $49/83025$ |

These are proved optima in the stated classes, not claims of unrestricted
global optimality.

## Results and proof packages

| Result | Why it helps | Read and reproduce |
| --- | --- | --- |
| One-root optimum at every even count | Gives the explicit construction and its sharp rate. | [Proof](../../notes/w-state-optimal-design-2026-09-26.md), [replay](../../computations/method-utility-2026-09-26/README.md) |
| Two-root optimum at every even count | Covers scalar cores with connected or disconnected cofactor graphs. | [Guide](../../explainers/BOUNDARY-STRUCTURE.md), [proof](../../notes/w-state-two-root-optimum-2026-09-26.md), [replay](../../computations/w-state-two-root-2026-09-26/README.md) |
| Unrestricted local optimality at six sites | The construction is a local optimum under complex colored-edge perturbations, modulo phase symmetries. | [Proof](../../notes/w-state-unrestricted-local-optimum-2026-09-26.md), [replay](../../computations/w-state-local-optimum-2026-09-26/README.md) |
| All-even optimum without ground perfect matchings | Fully colored completions cannot improve $R_*$ in this larger class. | [Frontier guide](../../explainers/BALANCED-FRONTIER.md), [proof](../../notes/w-state-no-ground-matching-optimum-2026-09-27.md), [replay](../../computations/balanced-frontier-2026-09-27/README.md) |
| Optimum with a uniform odd ground core and cancelling root couplings | At every even $n\ge6$, arbitrary complex root ground couplings cannot improve $R_*$; nonzero root strength gives a strict loss. Other colored entries remain unrestricted. | [Illustrated guide](../../explainers/W-GROUND-CANCELLATION.md), [proof](../../notes/w-state-coherent-odd-core-2026-09-27.md), [replay](../../computations/w-ground-cancellation-2026-09-27/README.md) |
| Six-site octahedral ground-core gap | Arbitrary complex cycle and root weights, with every colored completion, give $R<2/135<1/65$. | [Proof](../../notes/w-state-octahedral-ground-gap-2026-09-27.md), [replay](../../computations/w-ground-cancellation-2026-09-27/README.md) |
| Unrestricted response bound | Gives a bound for every colored architecture and isolates a possible six-site scalar proof target. | [Proof](../../notes/w-state-unrestricted-response-bound-2026-09-27.md), [replay](../../computations/balanced-frontier-2026-09-27/README.md) |
| Obstruction to normalization by local shears | An exact example shows that ground-site isolation by W-preserving shears can increase source strength. This proposed shortcut needs more than shears alone. | [Proof](../../notes/w-state-shear-normalization-obstruction-2026-09-27.md), [replay](../../computations/full-support-jets-2026-09-27/README.md) |

## The remaining case

~~~mermaid
flowchart TD
    A["Exact W output: ground amplitude is zero"] --> B{"Ground support has a perfect matching?"}
    B -->|No| C["Exactly two odd components"]
    C --> D["Known optimum proved for all even counts"]
    B -->|Yes| E["Ground matching terms cancel"]
    E --> F{"Ground-core structure"}
    F --> G["Uniform odd core: settled for n ≥ 6"]
    F --> H["Six-site octahedral family: strict gap"]
    F --> I["Other nonuniform cores: open"]
~~~

Every design exceeding $R_*$ must therefore use cancellation among
supported ground-color perfect matchings outside the newly settled core
families. Merely allowing more colored entries does not bypass these
theorems.

At six sites the unrestricted response bound gives $R\le4/135$, while
the construction attains $1/65$. One sufficient way to close this gap is
the following **open** scalar inequality. Let $D$ be the ground-color
matrix, $a_0=\sum_{i<j}|D_{ij}|^2$, and
$r_i^2=\sum_{j\ne i}|\operatorname{haf}(D\setminus\{i,j\})|^2$. For
$\operatorname{haf}(D)=0$ and all $r_i>0$, the desired inequality is

$$
a_0^2\sum_i r_i^{-2}\ \ge\ \frac{520}{9}.
$$

Numerical searches support this candidate but do not prove it. At four
sites the analogous response-only route is insufficient: the equations
removing multiple excitations must also be used. The
[shear obstruction](../../notes/w-state-shear-normalization-obstruction-2026-09-27.md)
likewise rules out one simple normalization argument, not the unrestricted
optimality conjecture.

All exact packages are included in the
[project-wide replay](../README.md#reproduce-the-follow-up-checks).
