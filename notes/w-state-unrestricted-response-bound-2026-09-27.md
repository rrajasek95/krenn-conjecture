# An unrestricted W-state bound from scalar ground-core responses

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The global unrestricted optimum is not proved.

[Replay](../computations/balanced-frontier-2026-09-27/README.md) ·
[Guide](../explainers/BALANCED-FRONTIER.md) ·
[Proved two-root optimum](w-state-two-root-optimum-2026-09-26.md)

The [support theorem](w-state-no-ground-matching-optimum-2026-09-27.md)
uses this bound to prove the known optimum at every even order when the
ground support has no perfect matching, including fully colored completions.

## 1. A bound for any colored architecture

Let $n=2m\ge4$, with arbitrary complex edge blocks and exact output
$H=\lambda W_n\ne0$. Define the scalar ground-color core

$$
 D_{ij}=A_{ij}(a,a),\quad a_0=\sum_{i<j}|D_{ij}|^2,\quad
 C_{ij}=\operatorname{haf}(D\setminus\{i,j\}),\quad
 r_i^2=\sum_{j\ne i}|C_{ij}|^2.
$$

The all-ground output forces $\operatorname{haf}(D)=0$. Each $r_i$
must be nonzero. Put $b(D)=\sum_i1/r_i^2$. Then

$$
 \boxed{R\le
 \frac{n(m-1)^{m-1}}{m^m\,a_0^{m-1}b(D)}.}                      \tag{1}
$$

Unlike the one-root and two-root theorems, this upper bound allows a fully
colored core. It is a relaxation: the constraints suppressing multiple
excitations may force additional source strength and a smaller rate.

**Proof.** Let $x_{ij}$ be the entry that emits $b$ at site $i$ and
$a$ at site $j$. The coefficient with its sole excitation at $i$ is

$$
                         \lambda=\sum_{j\ne i}x_{ij}C_{ij}.       \tag{2}
$$

No entry emitting two excitations, or emitting an extra color, occurs in
this word. The entries $x_{ij}$ for different $i$ are distinct source
coordinates. Cauchy--Schwarz, applied independently to each row, gives

$$
 \sum_{j\ne i}|x_{ij}|^2\ge\frac{|\lambda|^2}{r_i^2},\qquad
 S\ge a_0+|\lambda|^2 b(D).                                    \tag{3}
$$

Equality in the first inequality is attained precisely by
$x_{ij}=\lambda\overline{C_{ij}}/r_i^2$. A zero row makes a nonzero
uniform W coefficient impossible. Also $a_0>0$, since a single-excitation
matching term requires $m-1\ge1$ ground edges.

For a fixed core, maximize
$n u/(a_0+b u)^m$ over $u=|\lambda|^2\ge0$. Its maximum is at
$u=a_0/((m-1)b)$ and is the right side of (1). This proves the bound
without assuming that its minimizing source cancels the other outputs. ∎

## 2. An explicit upper bound at every even site count

Write

$$
 B_n=\frac{((n-1)!!)^2}{\binom n2^m},\qquad
 T=\sum_{i<j}|C_{ij}|^2.
$$

The subhafnian inequality in [Roos, Theorem 2.3, equations (38) and
(40)](https://arxiv.org/html/1906.06176), applied with $k=m-1$ partitioned
into ones, gives

$$
 T\le K_n a_0^{m-1},\qquad
 K_n=\frac{((n-3)!!)^2}{\binom n2^{m-2}}=m^2B_n.
$$

Since $\sum_i r_i^2=2T$, Cauchy--Schwarz gives
$b(D)\ge n^2/(2T)$. Inserting these inequalities in (1) yields

$$
 \boxed{R\le B_n\left(\frac{m-1}{m}\right)^{m-1}.}              \tag{4}
$$

This is a global upper bound for arbitrary complex colored sources producing
exact uniform W output. It does not use the zero-hafnian constraint to sharpen
the last scalar inequalities, and is not claimed sharp.

| Sites | Attained rate, proved optimal within two-root designs | Unrestricted upper bound (4) |
|---|---:|---:|
| 4 | $1/10$ | $1/8$ |
| 6 | $1/65$ | $4/135$ |
| 8 | $9/3136$ | $6075/802816$ |
| 10 | $49/83025$ | $12544/6328125$ |

For a weighted target with coefficients $w_i$, replace $b(D)$ by
$\sum_i |w_i|^2/r_i^2$ and the numerator $n$ in (1) by
$\sum_i|w_i|^2$. A required nonzero $w_i$ still needs $r_i>0$.
The same derivation applies; zero target weights contribute zero to the sum.

## 3. A concrete sufficient route to the six-site global optimum

At six sites, (1) reads

$$
                         R\le \frac{8}{9a_0^2 b(D)}.
$$

Consequently the following scalar statement, if proved, would establish
the unrestricted optimum $1/65$:

$$
 \boxed{\operatorname{haf}(D)=0,\quad r_i>0
       \quad\Longrightarrow\quad a_0^2\sum_i\frac1{r_i^2}
                                  \ge\frac{520}{9}.}            \tag{5}
$$

**Equation (5) is open.** It involves only the fifteen complex ground edges,
not the full sixty binary or 135 ternary source entries. It is sufficient,
not established as necessary for the global W theorem: a violating scalar
core might still fail the omitted multi-excitation cancellation constraints.

The known one-root design attains the candidate threshold. Put weight one
on the complete five-site core and zero on all ground edges to the sixth
site. Then

$$
 a_0=10,\quad (r_i^2)=(9,9,9,9,9,45),\quad
 b=26/45,\quad a_0^2b=520/9.
$$

The minimum-norm single-excitation entries are $1/3$ toward the root from
each core site and $1/15$ from the root toward each core site, for target
amplitude one. Their output is exactly W, with no unwanted words. Optimizing
their scale relative to the ground core gives rate $1/65$.

For comparison, two scalar triangles of weight one have $a_0=6,r_i^2=3$,
so (1) gives the stronger core-specific upper bound $1/81$. This holds for
every colored completion of that fixed ground core.

The optional numerical search probes (5) using the real and imaginary parts
of the zero-hafnian equation and unit ground norm as equality constraints.
It is evidence about local optimization only, not a certificate of (5).

## 4. Why the relaxed scalar inequality cannot simply be assumed at all sizes

At four sites put opposite edge pairs at weights $1,\omega,\omega^2$,
where $\omega^2+\omega+1=0$. Then

$$
 \operatorname{haf}(D)=1+\omega^2+\omega=0,\quad
 a_0=6,\quad r_i^2=3,\quad a_0 b=8.
$$

To prove the two-root value $1/10$ by (1) alone would require
$a_0 b\ge10$, which this core disproves. Its relaxed upper bound is $1/8$.
The minimum-norm single-excitation entries do give all four required W
coefficients, but also six nonzero two-excitation coefficients.

This is a counterexample to an all-size *scalar relaxation inequality*,
not a W design beating $1/10$, and not a proof of the unrestricted four-site
optimum. Cancellation constraints cannot be dropped merely because the
single-excitation norm minimization is exact.

Those omitted equations have a useful explicit first layer. Write $y_{ij}$
for the source entry emitting $b$ at both $i,j$. For any pair of distinct
excitation sites,

$$
 0=y_{ij}C_{ij}
   +\sum_{\substack{k,l\notin\{i,j\}\\k\ne l}}
        x_{ik}x_{jl}\operatorname{haf}(D\setminus\{i,j,k,l\}).     \tag{6}
$$

If $C_{ij}\ne0$, this fixes $y_{ij}$ uniquely once $D,x$ are chosen
and adds its squared norm to the source cost. If $C_{ij}=0$, the sum must
vanish independently of $y_{ij}$. Further excitation sectors impose
additional constraints. Equation (6) indicates how to strengthen the
relaxation if (5) fails or proves too difficult.
