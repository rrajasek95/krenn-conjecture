# Useful consequences: architecture exclusion and fidelity–rate benchmarks

Date: 2026-09-26. **Status: new written deductions and exact computational
checks; no separate independent audit or admission to the certified spine.**
The all-order exclusion below uses admitted inputs. The benchmark is an
explicit achievable construction, not a universal rate upper bound. No
historical-priority claim is made.

Read the [illustrated explanation](../explainers/USEFUL-CONSEQUENCES.md) or run
the [replay package](../computations/useful-consequences-2026-09-26/README.md).

## 1. Definitions and dependencies

At each of n=2r sites use an orthonormal basis a,b,c. An ordinary source A
assigns arbitrary complex endpoint-color coefficients to pairs of distinct
sites. Its whole matching tensor is H(A)=A^[r]=A^r/r!, in the commutative
algebra where using any site twice gives zero. Tensor norms below are the
Euclidean coefficient norms in this fixed basis.

A **bipartite output-pair graph** has a single partition U,T of the physical
output sites such that every nonzero edge block crosses U,T. This is different
from the source–output incidence graph, which is bipartite by construction.

The admitted inputs are:

* [GD §§1–6](../certification/stronger-results-2026-09-26/sources/GD.md): an exact
  full ternary GHZ source on even n>=4 has diagonal original edge blocks.
* [BC §§1–3 and the balanced-source corollary in §4](../certification/stronger-results-2026-09-26/sources/BC.md):
  in an actual balanced bipartite source with exactly two nonzero pure target
  terms, every opposite-shore deletion cofactor has nonzero whole binary
  projection. Individual pure coefficients need not be nonzero.
* The [six-site exclusion](../proofs/six-site-arbitrary-complex-obstruction.md)
  and admitted [eight- and ten-site exclusions](../certification/stronger-results-2026-09-26/THEOREMS.md)
  are used only for the compactness statement in §4.

The [admission record](../certification/SUPERSESSIONS.md#supersession-2026-09-26-01)
defines the scope of the September inputs. Their historical file headers are
preserved and may describe a pre-admission status.

## 2. Bipartite exclusion at every even order

**Theorem A.** For every even n>=4, no ordinary source supported on a bipartite
output-pair graph satisfies

    H(A) = tau_a a^V + tau_b b^V + tau_c c^V,
    tau_a tau_b tau_c != 0.

**Proof.** A nonzero matching tensor requires equal shores: |U|=|T|=r.
GD makes every edge block diagonal in the original a,b,c basis. Project each
site onto b,c and call the resulting actual source B. Its whole tensor is
tau_b b^V+tau_c c^V. For every p in U and t in T, BC gives

    K_pt = H(B restricted off {p,t}) != 0.                 (A1)

Now take the slice of H(A) with a at p,t and only b,c at the other n-2 sites.
The target slice is zero because n>=4. Diagonality forces the two a sites to
pair together, so this WHOLE slice is exactly

    A_pt(a,a) K_pt = 0.                                   (A2)

Equation (A1) makes A_pt(a,a)=0 for every opposite-shore pair. There are no
same-shore edges, so the all-a amplitude is zero, a contradiction. QED.

The same exclusion holds for three or more nonzero pure target terms by
projecting onto any three. It permits arbitrary complex cancellation and
parallel sources aggregated into edge blocks. It excludes common bipartite
support for all colors, not merely one bipartite color component.

**Boundaries.** At n=2 the remaining tensor is the empty unit and the selected
slice is pure; a single edge can carry all three colors. At n=4 the usual
three colored matchings of K4 work, but K4 is not bipartite. Binary GHZ states
on alternating even cycles remain possible. The general n>=12 problem is
not settled by restricting its graph to a bipartite architecture.

## 3. A computable lower bound on mixed-output leakage

This statement applies to any **diagonal** bipartite source, whether or not
it is close to GHZ. Exact GD does not justify assuming diagonality for an
arbitrary approximate source.

Write H(A)=tau_a a^V+tau_b b^V+tau_c c^V+E, where E contains all mixed words.
Fix p in U and choose a as the tested color. For t in T define

    k_pt^2 = ||H(B restricted off {p,t})||^2,
    q_pt   = haf(M_a restricted off {p,t}),
    D_p    = sum_(t in T) |q_pt|^2 / k_pt^2.              (B1)

Here B is the b,c projection and M_a is the a-color matrix. Suppose all
k_pt>0 and tau_a!=0. Then D_p>0 and

    ||E||^2 >= |tau_a|^2 / D_p.                           (B2)

**Proof.** The slices with a exactly at p,t and b,c elsewhere have mutually
disjoint word supports as t varies. By the same matching expansion as (A2),

    ||E||^2 >= sum_t |A_pt(a,a)|^2 k_pt^2.                (B3)

Expanding the pure hafnian at p and applying weighted Cauchy–Schwarz gives

    |tau_a|^2 = |sum_t A_pt(a,a) q_pt|^2
       <= (sum_t |A_pt(a,a)|^2 k_pt^2) D_p.               (B4)

Combining (B3) and (B4) proves (B2). If D_p were zero, all q_pt would vanish,
forcing tau_a=0. QED.

For equal, phase-aligned pure amplitudes tau_a=tau_b=tau_c=tau!=0, fidelity
to g=(a^V+b^V+c^V)/sqrt(3) therefore obeys the explicit bound

    F = 3|tau|^2 / (3|tau|^2+||E||^2)
      <= 3D_p / (3D_p+1).                                (B5)

One can use the smallest valid D_p over roots and color choices. If a
denominator vanishes, this version gives no bound for that root; it does
not license division or imply impossibility. Cofactor tensors use only two
colors, so this witness can be evaluated without constructing every
three-color output. D_p depends on the proposed source: (B5) is a design
diagnostic, not a uniform architecture-independent fidelity ceiling.

## 4. Nonzero generation strength forces a fidelity gap

Let ||A||_edge^2 be the sum of squared absolute values of all aggregate
endpoint-color coefficients, counting each unordered physical pair once.
Fix ||A||_edge=1, a normalized three-color GHZ target g with all three
amplitudes nonzero, and R(A)=||H(A)||^2. For R(A)>0 set

    F(A) = |<g,H(A)>|^2 / R(A).

**Theorem C.** At n=6,8,10, for every rho>0 such that the set below is
nonempty, there exists delta(rho,g)>0 with

    R(A)>=rho  =>  F(A)<=1-delta(rho,g).                  (C1)

The same statement holds at any fixed even n>=4 when support is restricted
to a fixed bipartition.

**Proof.** The coefficient sphere is compact in finite-dimensional real
coordinates. Its closed subset R>=rho is compact, and F is continuous
there. Hence F attains its maximum. Equality F=1 would make H(A) a nonzero
multiple of g, contradicting the appropriate exact exclusion. QED.

Equivalently, along a sequence of norm-one sources with F approaching one,
R must approach zero. Otherwise a subsequence would have R>=rho>0. This
proof gives no numerical delta. R is generation strength under a fixed
coefficient budget; it is not by itself a normalized physical probability.

## 5. An exactly solvable six-site benchmark

Use the following properly edge-colored triangular prism. Vertices are
0,1,2 on one triangle and 3,4,5 on the other. All edges are monochromatic.

| Color | Triangle edges, amplitude t | Vertical edge, amplitude t omega |
|---|---|---|
| a | 01, 34 | 25 |
| b | 12, 45 | 03 |
| c | 02, 35 | 14 |

Its four perfect matchings are the three rows and the set {03,14,25}.
Therefore, for real t>0, omega>0,

    H = t^3 omega (a^6+b^6+c^6) + t^3 omega^3 (bcabca).
                                                               (D1)

The fourth word lists site colors in order 0,...,5. Put x=omega^2. Direct
normalization gives

    F = 3/(3+x^2),
    R_shape = x(3+x^2) / [27(2+x)^3].                    (D2)

R_shape is ||H||^2 after rescaling ||A||_edge to one; before rescaling,
||A||_edge^2=t^2(6+3x). Thus R_shape tends to zero as F tends to one, exactly
as Theorem C requires.

Near-perfect six-photon constructions and the scalings 1-F=O(omega^4),
counts=O(omega^2) already appear in
[THESEUS, Figure 3](https://arxiv.org/html/2005.06443). The construction here
is an explicit benchmark and calibration; it is not a claim to have first
discovered that asymptotic phenomenon.

### Exact physical probability in a specified source model

Realize each edge in its own two optical modes as a phase-coherent two-mode
squeezed vacuum

    sqrt(1-|lambda_e|^2) sum_(k>=0) lambda_e^k |k,k>.

This convention is given in [NIST IR 8486, §2.8.4, equation (12)](https://nvlpubs.nist.gov/nistpubs/ir/2023/NIST.IR.8486.pdf).
Because each site–color mode belongs to exactly one edge, the nine pair
sources act on disjoint modes. Group the three color modes at each output
site, and condition on **exactly one photon per site**, preserving color
coherence. Assume ideal mode matching, stable phases, and no losses.

Any edge emitting two or more pairs fails this selection. All surviving
occupancies are exactly the four perfect matchings, but the full vacuum
normalization must still be included. For s=t^2, 0<s<min(1,1/x), the exact
selection probability per trial is

    P(s,x) = s^3 x(3+x^2) (1-s)^6 (1-sx)^3.              (D3)

This is an ideal postselection probability, not a heralded usable-state
rate or a prediction for threshold detectors with loss. In particular, no
claim is made that a large-pump low-order truncation describes those devices.

## 6. Optimal probability for balanced sources on this prism

Allow arbitrary complex amplitudes on the same nine colored edges, each of
magnitude less than one. Require the three pure matching amplitudes to equal
one common nonzero complex number mu. Their common phase can be removed.
Let nu be the mixed matching amplitude and x=|nu|/|mu|>0. Fidelity remains
3/(3+x^2).

**Theorem D.** Among all such balanced prism sources with this fixed x,
the maximum ideal selection probability is P(s_*(x),x), where

    s_*(x) = 2 / [3+2x+sqrt(9-4x+4x^2)].                (E1)

This optimum is attainable with all six triangle amplitudes t=sqrt(s_*)
and all three vertical amplitudes t omega=sqrt(s_* x), with aligned phases.

**Proof of symmetry at the optimum.** Fix |mu| and x. The product of the
three vertical squared magnitudes is |mu|^2 x^2; the product of the six
triangle squared magnitudes is |mu|^4/x^2. The probability is
|mu|^2(3+x^2) times the product of the nine vacuum factors (1-|lambda_e|^2).
The function z -> log(1-exp(z)) is strictly concave for z<0. At fixed
product, Jensen's inequality maximizes each group of vacuum factors by
making its squared magnitudes equal. These two equalizations are feasible
simultaneously: triangle squared magnitude s=|mu|^(2/3)/x^(1/3), vertical
squared magnitude sx. Their pure amplitudes still have magnitude |mu|,
and their phases can be aligned. Thus optimization reduces exactly to (D3).

**Proof of the pump optimum.** For fixed x>0,

    d/ds log P = 3/s - 6/(1-s) - 3x/(1-sx),
    d^2/ds^2 log P = -3/s^2 - 6/(1-s)^2 - 3x^2/(1-sx)^2 < 0.

The first derivative goes from positive infinity to negative infinity
across the feasible interval, so its unique zero is the global maximum.
Clearing positive denominators gives

    1-(3+2x)s+4xs^2=0.                                  (E2)

The smaller root, rationalized to avoid cancellation, is (E1). QED.

The balance assumption is part of the theorem. We have not optimized
unbalanced prism sources at fixed GHZ fidelity, other graph architectures,
lossy detection, or a fixed laboratory pump-power budget.

For a desired F<1, set x=sqrt(3(1-F)/F). As F approaches one,

    s_* -> 1/3,
    P_* ~ (64/6561)x
        ~ (64 sqrt(3)/6561) sqrt(1-F).                  (E3)

The coefficient is about 0.01690. This is an exact optimum within the
stated balanced prism class, and an achievable benchmark for the wider
design space. It is not an upper bound for every source.

## 7. What is still open in this application

The [universal-rate feasibility follow-up](universal-rate-bound-feasibility-2026-09-26.md)
now proves power-law existence for the full complex model, supplies an explicit
square-root bound for nonnegative six-site sources, and rules out one tempting
polynomial shortcut. A useful explicit bound for arbitrary complex weights
remains open.

The main practical next step is a source-independent quantitative bound
at a specified generation budget, or an upper bound on physical success
probability at fixed fidelity in a specified hardware model. Theorem C
establishes a positive gap without calculating it; Theorem B computes an
instance-specific gap under diagonality; Theorem D solves a restricted
optimization exactly. None implies that the prism has the optimal global
scaling or constant.

Fidelity and success probability are jointly optimized in current research,
including [Ruiz-Gonzalez, Krenn and Gu (2026)](https://arxiv.org/abs/2605.02721).
Their broader physical models must be matched before comparing numerical
rates. These results also leave unrestricted exact sources at n>=12 open.

The replay checks the finite matching expansions, leakage identities on
exact controls, symbolic derivatives, and benchmark calibration. The
all-order arguments and the Jensen proof remain written proofs requiring
a separate independent audit before repository certification.
