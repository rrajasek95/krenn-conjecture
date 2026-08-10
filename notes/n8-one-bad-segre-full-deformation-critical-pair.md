# The Segre chart has a genuine simultaneous Hessian obstruction

## Outcome

The complete one-cell closure of `40d4ca7` does not promote to a global
initial-form theorem by ordering deformation coordinates independently.
The obstruction is exact and source-provenant.

Let (Phi) be the six-row functional from the fixed Segre--K4 diagonal
carrier theorem `a7f8f24`.  Expand it on the **full** decorated residual
quadratic: the fourteen fixed cells of (H), all 45 diagonal `00/11/22`
variables, and all 76 remaining endpoint-colour variables.  Direct matching
expansion gives

\[
                 \boxed{\Phi=L+Q},                       \tag{1}
\]

with

```text
linear deformation terms:     99
quadratic deformation terms:  30
terms of degree >=3:            0
```

Only seventeen of the 76 deformation coordinates occur.  Sixteen are the
first-order directions already found in `e180f0c`.  The seventeenth,

```text
12:02,
```

is completely invisible at first order and enters only through a genuine
common-(q) Hessian pair.

Thus the exact obstruction is not “two cells might interact” in the
abstract.  It is a nine-edge critical-pair graph with a distinguished
tangent-invisible vertex.  Any chart-cover proof must control that graph or
stratify its coefficient permanents; the 76 one-cell units alone cannot.

## 1. The smallest hidden pair

Put

\[
                 x=q_{03}(1,0),\qquad y=q_{12}(0,2).
\]

The two cells are disjoint and complete the literal physical matching

```text
03 | 12 | 45
```

in output word `102000`.  In the full six-row functional their exact joint
coefficient is

\[
 \boxed{
 [xy]\Phi=-d_{45}(d_{02}d_{13}+d_{03}d_{12}).
 }                                                        \tag{2}
\]

Equivalently, the two monomials are

\[
 -xy,d_{45}d_{02}d_{13},\qquad
 -xy,d_{45}d_{03}d_{12}.                               \tag{3}
\]

This is not a formal-cofactor artifact.  For the matching above the genuine
third cofactor is

\[
                         J_{03,12,45}=1.                 \tag{4}
\]

Hence full common-(q) Hessian/third-cofactor provenance certifies the term
in (2); it does not eliminate it.  A leading-form argument that first
discards (y) because its tangent is zero loses an actual source matching as
soon as (x) is present.

## 2. Complete quadratic critical-pair graph

The 30 quadratic terms use exactly nine cell pairs:

```text
02:10 * 14:02    (4 terms)
02:20 * 15:01    (4 terms)
03:10 * 12:02    (2 terms)
03:10 * 14:02    (4 terms)
03:20 * 15:01    (4 terms)
04:10 * 12:02    (2 terms)
04:20 * 15:01    (4 terms)
05:10 * 12:02    (2 terms)
05:10 * 14:02    (4 terms)
```

All are endpoint-star/companion-edge Hessian products.  No third-order
deformation term occurs in this functional.  Of the sixty directions whose
first variation vanishes, 59 are absent to every order here; `12:02` is the
unique hidden quadratic direction.

This full polynomial calculation is different from enumerating two-cell
supports.  It expands the common source once, retains every decorated cell
as an independent variable, and reads its homogeneous transgression.

## 3. Exact obstruction to the proposed initial-form route

The diagonal-carrier theorem starts with (Phi=0).  A coordinatewise initial
order would next process the sixteen nonzero tangent directions and treat
the other sixty as lower or irrelevant.  Equation (2) refutes that
separation: the initial coefficient of (x) depends on the supposedly
invisible coordinate (y).

The coefficient supplies the sharp next two-stratum problem:

\[
                     \Pi=d_{02}d_{13}+d_{03}d_{12}.     \tag{5}

* Off (Pi=0), the hidden Hessian pair has nonzero coefficient after
  localizing (d45xy).  A source-labelled reduction must use that active
  pair together with the response rows.
* On (Pi=0), the two diagonal matchings form a permanent-null exchange.
  One needs a separate matching switch or clean-cap argument.

Neither curvature-free one-cell units nor the cofactor Euler tower decides
this dichotomy.  The tower guarantees (4), while the response equations
constrain products of cofactor carriers and therefore do not impose an
independent order on (x) and (y).

Accordingly there is currently no proof that every projection-degenerate
one-bad packet has initial form in the fixed Segre chart.  The precise
missing global mechanism is a **critical-pair completion theorem** for (2)
and its eight companions, compatible with the four binary response rows.

## 4. Verification and scope

The standard-library checker
[`verify_n8_one_bad_segre_full_deformation_critical_pair.py`](../computations/verify_n8_one_bad_segre_full_deformation_critical_pair.py)
pins the first-variation and complete one-cell theorems, constructs all 135
decorated K6 cells at once, expands the seven coefficients in the integral
six-row identity, and verifies (1)--(5) together with the full nine-pair
ledger.

This is an exact simultaneous-deformation counterguard to an independent
initial-order proof.  It is not a coefficient-feasible one-bad packet, does
not refute a more sophisticated chart-cover theorem, and is not a Krenn
counterexample.
