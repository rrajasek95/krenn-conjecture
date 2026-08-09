# One mixed cell creates the first parity transgression

## 1. Verdict

The colour-diagonal kernel classification does not extend to arbitrary
endpoint-coloured cells by simply taking the target-coordinate part of a
kernel row.  One mixed cell already couples a non-target kernel direction
to a nonzero target component.

The smallest source-faithful family is

```text
q_12(a,a)=1,       q_34(c,c)=1,       q_02(t,a)=lambda,
U(lambda)=-e_a^(1)+lambda e_t^(0).
```

Its literal common-cofactor map satisfies

```text
Phi_{q(lambda)}(U(lambda))=0
```

identically.  At the diagonal special fibre, `-e_a^(1)` is a one-site
kernel, while `e_t^(0)` has nonzero image.  The derivative of the one
mixed cell cancels that target image exactly.

This is a first-filtered-differential counterguard.  It has neither bright
pure images nor the required nonlinear pure kernel product, so it is not a
two-bad packet and not a counterexample to Krenn's conjecture.

## 2. Literal matching identity

On `C={0,1,2,3,4}`, only two four-site cofactors are nonzero:

```text
K_0 = e_a^(1)e_a^(2)e_c^(3)e_c^(4),
K_1 = lambda e_t^(0)e_a^(2)e_c^(3)e_c^(4).
```

The first uses the diagonal matching `(12)(34)`.  The second uses the
mixed matching `(02)(34)`.  After inserting the two row components, both
routes have the same full word

```text
W=e_t^(0)e_a^(1)e_a^(2)e_c^(3)e_c^(4),
```

with coefficients `+lambda` and `-lambda`.  Hence they cancel with common
matching provenance.  There is no abstract cofactor substitution.

Endpoint order is essential and explicit: the mixed cell on physical edge
`02` has colour `t` at site `0` and colour `a` at site `2`.

## 3. Associated-graded equation

Write

```text
q(lambda)=q_0+lambda m,
U(lambda)=U_0+lambda U_1
```

with `U_0=-e_a^(1)` and `U_1=e_t^(0)`.  Expanding the kernel equation gives

```text
degree 0:  Phi_0(U_0)=0,
degree 1:  Phi_0(U_1)+(D_m Phi)(U_0)=0.                (1)
```

The checker reconstructs both degree-one terms:

```text
Phi_0(U_1)=W,          (D_m Phi)(U_0)=-W.              (2)
```

Thus the first off-diagonal differential is nonzero.  In parity language,
an inserted `a` row followed by one `(t,a)` internal cell lands in the same
target parity sector as an inserted `t` row with diagonal internal cells.
The diagonal target-axis component is therefore not itself a kernel.

## 4. Consequence for the mixed-colour attack

The diagonal proof killed a large target-axis kernel by projecting words
with a distinguished target colour.  Equations (1)--(2) identify the exact
first correction to that projection.  A viable mixed-colour theorem must
control the transgression

```text
ker(Phi_0 in a/c sector)
    -- one (t,a) or (t,c) cell -->
target-parity coker/image data.
```

It is not enough to prove again that the diagonal target-axis component has
small support.  One must show that the incoming degree-one class is killed
by the two bright equations, reduces to a diagonal bridge, or cannot carry
the pure kernel-product class.  The displayed three-cell family is the
minimal mutation any such theorem must exclude.

## 5. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_mixed_parity_first_correction_guard.py
python3 -O computations/verify_shared_reciprocal_two_bad_mixed_parity_first_correction_guard.py
```

The checker uses only the Python standard library and exact polynomial
arithmetic in `lambda`.
