# Independent audit: the nine-cell fixed quadratic has no one-pair cap

## 1. Scope and verdict

This is a clean-room audit of the fixed-quadratic statement in
[`polarized-eight-site-fixed-q-pair-cap-obstruction.md`](polarized-eight-site-fixed-q-pair-cap-obstruction.md).
It confirms the following sharply delimited result over
characteristic zero (in particular over \(\mathbb C\)).

Let
\[
\begin{aligned}
q={}&e_{2,0}e_{3,0}+e_{4,0}e_{5,0}+e_{6,0}e_{7,0}
    +e_{0,1}e_{1,1}+e_{3,1}e_{6,1}+e_{5,1}e_{7,1}\\
   &+e_{0,2}e_{2,2}+e_{1,2}e_{4,2}+e_{5,2}e_{6,2}.
\end{aligned}
\]
In the eight-site square-zero algebra, there are no scalar \(a\) and
linear forms \(p,s\) satisfying
\[
        (a q+4ps)q^{[3]}=\Delta_{8,3}.
\]

The audit does **not** prove the corresponding claim for an arbitrary
quadratic \(q\).  It therefore does not by itself prove a uniform one-pair
cap theorem, handle several rows sharing the same quadratic, perform the
all-even descent, or settle the Krenn conjecture.

The independent checker is
[`verify_polarized_eight_site_fixed_q_pair_cap_obstruction_independent.py`](../computations/verify_polarized_eight_site_fixed_q_pair_cap_obstruction_independent.py).
It imports no code from the discovery checker and uses repeated algebra
multiplication rather than enumerating compatible cell subsets.

## 2. Independent divided-power reconstruction

Represent a monomial by an eight-letter word in \(\{0,1,2,\mathord.\}\),
where a dot is an unoccupied site.  Multiplication is zero when two factors
occupy the same site and otherwise merges their words.  Repeated
multiplication of the nine literal cells above gives
\[
q^3=3!\sum_{w\in\mathcal F}e_w,
\]
where the complete nineteen-word set \(\mathcal F\) is
\[
\begin{array}{llll}
\texttt{..000000}&\texttt{110000..}&\texttt{1100..00}&\texttt{.2002.00}\\
\texttt{1100.1.1}&\texttt{1100.22.}&\texttt{.20021.1}&\texttt{.200222.}\\
\texttt{11..0000}&\texttt{2.2.0000}&\texttt{11.1001.}&\texttt{2.21001.}\\
\texttt{222.2.00}&\texttt{11.1.111}&\texttt{2.21.111}&\texttt{.2.12111}\\
\texttt{22212.1.}&\texttt{222.21.1}&\texttt{222.222.}&&
\end{array}
\]
and every displayed coefficient in \(q^{[3]}=q^3/3!\) is exactly one.
The same independent multiplication gives
\[
 q^4=4!\bigl(e_{11000000}+e_{22212111}\bigr),\qquad
 Q:=q^{[4]}=e_{11000000}+e_{22212111}.
\]

Put \(F=q^{[3]}\).  Direct multiplication also verifies
\[
             qF=\frac{q^4}{3!}=4\frac{q^4}{4!}=4Q.
\]
Thus the proposed identity has the exact rescaling
\[
 (aq+4ps)F=4(aQ+psF)=\Delta_{8,3},
 \qquad
 aQ+psF=\frac14\Delta_{8,3}.                 \tag{1}
\]
This factor of four is essential: the pure target coordinates below force
\(1/4\), not \(1\).

## 3. Full coordinate-incidence check

For modes \(X=(i,c)\) and \(Y=(j,d)\) at distinct sites, write
\[
 R_{XY}=p_Xs_Y+s_Xp_Y.
\]
The checker constructs all \(\binom82\cdot3^2=252\) possible abstract
entries \(R_{XY}\), multiplies each corresponding pair monomial by all
nineteen terms of \(F\), and collects top-degree words.  The independently
reconstructed incidence data are:

* 171 total nonzero pair--\(F\) incidences;
* 165 distinct top-degree words;
* 163 words having exactly one incidence;
* two words having four incidences;
* coefficient one on every incidence.

No rank-one parametrization is used in this count.  It is first an exact
linear audit in abstract Gram entries \(R_{XY}\).

## 4. The seven decisive singleton coordinates

Set
\[
A=(0,0),\quad B=(1,0),\quad C=(2,1),\quad D=(4,1),
\quad E=(3,2),\quad F_0=(7,2).
\]
(``\(F_0\)'' here is a mode and should not be confused with the divided
power \(F=q^{[3]}\).)  The following table was recovered from the full
incidence map, not inserted as an assumed support pattern.

| top word | sole coefficient from \(psF\) | coefficient in \(Q\) | coefficient in \(\Delta/4\) |
|---|---:|---:|---:|
| \(00000000\) | \(R_{AB}\) | \(0\) | \(1/4\) |
| \(11111111\) | \(R_{CD}\) | \(0\) | \(1/4\) |
| \(22222222\) | \(R_{EF_0}\) | \(0\) | \(1/4\) |
| \(02002222\) | \(R_{AF_0}\) | \(0\) | \(0\) |
| \(20210012\) | \(R_{BF_0}\) | \(0\) | \(0\) |
| \(02112111\) | \(R_{AC}\) | \(0\) | \(0\) |
| \(11110012\) | \(R_{CF_0}\) | \(0\) | \(0\) |

The third column is checked against the complete two-word support of \(Q\),
so the scalar \(a\) is absent on every one of these coordinates.  Equation
(1) consequently forces
\[
 R_{AB}=R_{CD}=R_{EF_0}=\frac14,
 \qquad
 R_{AF_0}=R_{BF_0}=R_{AC}=R_{CF_0}=0.        \tag{2}
\]

## 5. Independent two-dimensional Gram contradiction

Associate to every mode \(X\) the vector \(x_X=(p_X,s_X)\in\mathbb C^2\)
and use the nondegenerate symmetric bilinear form
\[
 \beta((r,t),(r',t'))=rt'+tr'.
\]
Then \(R_{XY}=\beta(x_X,x_Y)\).

The relation \(R_{EF_0}=1/4\) implies \(x_{F_0}\ne0\), so
\(x_{F_0}^{\perp}\) is a one-dimensional line.  The three zero relations
\(R_{AF_0}=R_{BF_0}=R_{CF_0}=0\) place \(x_A,x_B,x_C\) on this line.
Since \(R_{AB}=1/4\), the restriction of \(\beta\) to the line is nonzero
and \(x_A\ne0\).  On a one-dimensional nonisotropic line,
\(R_{AC}=0\) therefore forces \(x_C=0\).  This contradicts
\(R_{CD}=1/4\).

As a second exact check, the audit forms the seven polynomial equations
(2) in the twelve coordinates of \(x_A,\ldots,x_{F_0}\).  SymPy's exact
Groebner-basis engine over \(\mathbb Q\), with graded reverse lexicographic
order, returns the unit basis \([1]\).  This is independent of the source
checker's Singular elimination and agrees with the geometric proof.

## 6. Reproduction

From the repository root, run

```sh
uv run python computations/verify_polarized_eight_site_fixed_q_pair_cap_obstruction_independent.py
```

The checker verifies the literal nine cells, all nineteen terms of
\(q^{[3]}\), both terms of \(q^{[4]}\), the factor-four normalization, the
complete incidence histogram, the seven singleton equations, the absence
of \(aQ\) on them, and the exact characteristic-zero inconsistency.
