# Higher-order constraints near full-support single-color sources

September 27, 2026. **Written proof and exact supporting checks; independent
audit pending.** This does not prove the unrestricted square-root rate law.

[Replay](../computations/full-support-jets-2026-09-27/README.md).

## 1. An identity at every even order

Let $n=2m\ge4$. At a base source $A_0$, every edge has only its $aa$ entry,
denoted $D_{ij}$, and every $D_{ij}$ is nonzero. Consider a formal path

$$
A(t)=A_0+tA_1+t^2A_2+\cdots,\qquad H(A(t))=\sum_k t^k H_k.
$$

Choose any output word $w$ all of whose colors differ from $a$. For an edge
$ij$, let $w^{ij}$ replace its two endpoint colors by $a$. Then

$$
\boxed{
m(H_m)_w=\sum_{i<j}\frac{(A_1)_{ij}(w_i,w_j)}{D_{ij}}
                      (H_{m-1})_{w^{ij}},
}
\tag{1}
$$

$$
\boxed{
(H_{m+1})_w=\sum_{i<j}\frac{(A_2)_{ij}(w_i,w_j)}{D_{ij}}
                      (H_{m-1})_{w^{ij}}.
}
\tag{2}
$$

All complex entries of every source jet are free. Zero base output is not
required for the identities, although it is needed for the near-GHZ
application below.

**Proof.** Project the edge blocks of $A_1$ onto the non-ground colors and
call the resulting source $T$; call the corresponding projection of $A_2$
$U$. To obtain $n-2$ non-ground output colors at order $m-1$, a matching
must use exactly one base edge, joining the two ground-color sites, and
$m-1$ first-jet edges. Therefore

$$
(H_{m-1})_{w^{ij}}
 =D_{ij}\bigl(H_{n-2}(T[V\setminus\{i,j\}])\bigr)_{w|_{V\setminus\{i,j\}}}.
\tag{3}
$$

For an entirely non-ground word, the output at order $m$ is $H_n(T)$.
At order $m+1$ it is $DH_n(T)[U]$: one edge uses the second jet and the
other $m-1$ edges use the first jet. Higher jets cannot occur at these
orders. Expanding the derivative by its chosen edge proves (2).
Euler's identity for the degree-$m$ matching polynomial, or counting each
matching once for each of its $m$ edges, proves (1). ∎

## 2. What this says about a GHZ approach

Suppose $H(A_0)=0$ and the leading nonzero output of an analytic path is
proportional to the GHZ tensor with at least one non-ground target color.
That leading output cannot occur before order $m$, because an entirely
non-ground word requires $m$ perturbed edges. All coefficients before the
leading order must vanish, including $H_{m-1}$. Equations (1)--(2) then
rule out leading order $m$ and $m+1$ as well.

Thus **the first possible leading GHZ output has parameter order at least
$m+2$**. At six sites it is at least fifth order. This applies to the whole
full-support single-color class, including the balanced rank-25 example,
and permits perturbations in all 135 ternary source entries.

At six sites, vanishing of the relevant $H_2$ outputs has a further structural
consequence: every four-site matching tensor of $T$ vanishes. The
[four-site norm theorem](balanced-four-site-response-bound-2026-09-26.md)
then implies that the support graph of $T$ has matching number at most two.
The first non-ground direction therefore lies in a specific critical
locus, not in an arbitrary 60-dimensional colored-edge space.

Parameter order must not be confused with a uniform power of source
distance. An analytic path can start with $t^2A_2$ rather than $tA_1$,
and fractional orders can appear when distance is used as its parameter.
We do not claim a uniform fifth-power distance bound.

## 3. A uniform fourth-power distance bound at six sites

For clarity, there is also a direct bound for arbitrary nearby sources.
Let $d=\min_{i<j}|D_{ij}|>0$ and $\delta=\|A-A_0\|\le d/2$.
Write $H=\lambda\Delta+E$ and $\varepsilon=\|E\|$ for the ternary GHZ
projection. Choose a non-ground target color $b$. Write
$Y_{ij}=A_{ij}(b,b)$ and let $X$ denote the entries with one ground and
one $b$ endpoint. For each pair $ij$,

$$
H_{a_i a_j b^4}
 =A_{ij}(a,a)\operatorname{haf}(Y[V\setminus\{i,j\}])+Q_{ij},
$$

where $Q_{ij}$ is the sum of the twelve matching terms with two mixed
edges and one $bb$ edge. Hence $|Q_{ij}|\le12\delta^3$.
Euler's identity and $|A_{ij}(a,a)|\ge d/2$ give

$$
3|H_{b^6}|
\le \frac{2\delta}{d}\varepsilon+\frac{360}{d}\delta^4.
$$

For the first term use Cauchy--Schwarz on the fifteen distinct mixed output
words, and $\sum_{ij}|Y_{ij}|^2\le\delta^2$.
For the second, bound the fifteen remaining summands separately.
Since $|H_{b^6}-\lambda|\le\varepsilon$,

$$
\boxed{
|\lambda|\le
\left(1+\frac{2\delta}{3d}\right)\varepsilon
\frac{120}{d}\delta^4.
}
\tag{4}
$$

The constants are deliberately coarse. This is an onset bound, not the
needed lower bound $\varepsilon\ge c|\lambda|^3$.

The replay checks (1)--(2) coefficient by coefficient for all 64 non-ground
words at six sites, using all four jets as available variables, on two
different complex bases. It also rejects a missing denominator edge and
checks that the Euler factor three cannot be omitted. The universal
all-even statement follows from the matching-count proof above.
