# Output-preserving W shears need not isolate a ground site efficiently

September 27, 2026. **Written proof and exact checks; independent audit pending.**

[Replay](../computations/full-support-jets-2026-09-27/README.md) ·
[Ground-support optimum](w-state-no-ground-matching-optimum-2026-09-27.md).

## 1. The proposed normalization

At each site apply $a\mapsto a$, $b\mapsto b+s_i a$. The output $W_n$ changes
to $W_n+(\sum_i s_i)a^n$, so any complex parameters with $\sum_i s_i=0$
preserve W exactly. These invertible local maps are called shears.

If the source has no $bb$ entries, shears leave all one-excitation entries
unchanged and change only the ground entries:

$$
D'_{ij}=D_{ij}+s_iX_{ij}+s_jX_{ji},
$$

where $X_{ij}$ excites $i$ and leaves $j$ in the ground color.
Thus minimizing source strength over these shears is an ordinary complex
least-squares problem. This suggested reducing a general W source to one
with an isolated ground site and applying the all-even support theorem.

The following exact example shows that isolation by shears alone can have
a strictly positive source cost.

## 2. A source already minimal over its entire shear orbit

Use roots $0,1$ and core sites $2,3,4,5$. Set ground weight one on the four
edges between $\{2,3\}$ and $\{4,5\}$. Put $\sigma_2=\sigma_3=1$ and
$\sigma_4=\sigma_5=-1$, and set

$$
D_{0i}=-\sigma_i/2,\quad D_{1i}=1/2,\quad
X_{i0}=1/2,\quad X_{i1}=\sigma_i/2,\quad
X_{01}=X_{10}=1/2.
$$

All other entries are zero. Direct matching expansion gives $H=W_6$,
source strength $S=17/2$, and rate $48/4913$.
For arbitrary complex shear parameters, direct expansion of the norm gives

$$
\boxed{
S'= \frac{17}{2}
   +\frac14|s_0+s_1|^2
   +\frac12\sum_{i=2}^5|s_i|^2.
}
\tag{1}
$$

The original ground vector is orthogonal to every linear shear direction,
which eliminates the linear terms. Formula (1) proves global minimality
over the entire complex shear orbit, including the W-preserving subgroup.

To isolate ground site 0, its four core edges force $s_i=\sigma_i$.
The edge $01$ and the W constraint both then require $s_0+s_1=0$.
To isolate site 1, the four core edges instead force $s_i=-\sigma_i$,
again with $s_0+s_1=0$. Both possibilities have $S'=21/2$.

No core site can be isolated by any shear: its unit ground edges to the
opposite core pair have no mixed entries and remain unchanged.
Therefore every available ground-isolating shear has rate
$6/(21/2)^3=16/3087$, strictly below the original rate.

This is not a counterexample to the optimal W rate. It is already within
the proved two-root architecture and has rate below $1/65$. It disproves
the proposed claim that ground isolation can always be obtained by these
shears without increasing source strength. Additional transformations or
the cancellation equations remain necessary.

The exact checker verifies all output coefficients, the complete Hermitian
quadratic form (1), both isolation costs, and the invariant edges preventing
the other four isolations. The quadratic-form certificate covers every
complex shear parameter, not just sampled transformations.
