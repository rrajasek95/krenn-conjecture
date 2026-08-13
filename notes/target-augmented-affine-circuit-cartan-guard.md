# A target-augmented affine circuit gives an exchange or a target-dark separator

## Result

Let

\[
 C:k^S\longrightarrow Y,\qquad t\in Y,
\]

and choose an inclusion-minimal-support point `x` of the affine fibre

\[
                         Cx=t.                         \tag{1}
\]

Put

\[
 A=(C\mid-t),\qquad c=(x,1)\in\ker A.                \tag{2}
\]

Then the support of `c` is a circuit of the column matroid of `A`.  If a
proper dependence contains the target column, normalizing its target
coefficient gives a solution of (1) with smaller support.  If it avoids the
target column, translating `x` along it can kill one occupied coordinate
without adding support.  Both contradict minimality.

Consequently, if (1) misses every literal target-coordinate line, the
circuit (2) contains the target column and at least two old columns.  This is
the exact full-support circuit promised by the affine-accessibility
boundary; no response census is needed.

Checker:
[`verify_target_augmented_affine_circuit_cartan_guard.py`](../computations/verify_target_augmented_affine_circuit_cartan_guard.py).

## Append the complete Cartan column

Let `g in Y` be the placed complete physical Cartan/word-change column and
append it to `A`.  There is an exact rectangular alternative.

### Internal Cartan column

If `g in im A`, choose `Ay=g`.  Then

\[
                         (-y,1)\in\ker(A\mid g)        \tag{3}
\]

has unit Cartan coordinate.  Because every coordinate of `c` is nonzero,
for each old circuit coordinate `i` there is a unique scalar `mu` for which

\[
                        y'=y+\mu c,qquad y'_i=0.       \tag{4}
\]

The unit-Cartan relation from `y'` has two possible meanings.

* If its target coefficient `y'_tau` is nonzero, divide by it.  Equation
  `Ay'=g` becomes a new normalized affine presentation of `t` using `g` and
  omitting old coordinate `i`.  This is the literal matroid augmenting
  step.
* If `y'_tau=0`, it is a homogeneous connector expressing `g` through old
  response columns, again with unit new coordinate and with `i` omitted.

This is a genuine exchange theorem, but its proof-theoretic output depends
on types.  It is an anchor-safe support deletion only if the participating
old/new columns are literal endpoint coordinates in the same physical
affine problem.  For a Cartan source-chain column it is instead a relative
unit-coordinate kernel; the physical terminal decides whether it is the
generator or can be absorbed.

### External Cartan column

If `g` is external to `im A`, there is a covector `lambda` with

\[
             \lambda A=0,\qquad \lambda g=1.           \tag{5}
\]

Because `-t` is already a column of `A`, (5) forces

\[
                         \lambda t=0.                  \tag{6}
\]

Thus the external branch is sharper than a generic Fredholm alternative:
it is a **target-annihilating** Fitting separator.  It cannot become a
source unit merely by invoking the normalized target coefficient.  It
closes only after `lambda` is identified with a literal old optical/source
row, a physical relative terminal, or the complete-row covector of a typed
star/triangle/`K2,2` Hall tight set.  Without that identification it is only
the separator detecting the newly inserted Cartan column.

## The normalized target coefficient is not the physical anchor row

Let `e_tau^*` select the coefficient of the target column in (2).  It obeys

\[
                         e_\tau^*(c)=1.                \tag{7}
\]

Therefore the abstract rectangular theorem applies to the bordered matrix

\[
 \begin{pmatrix}A&g\\ e_\tau^*&\alpha\end{pmatrix}.   \tag{8}
\]

For external `g`, (8) gains two ranks over `A`.  This does **not** yet give
the physical two-rank source unit: `e_tau^*` is the domain coordinate of the
homogenizing target column, not a row of the physical source presentation.

On the restricted circuit block `A_D`, the kernel is one-dimensional.  A
literal physical anchor/normalization row `h_phys` promotes (8) precisely
when

\[
                         h_{phys}(c)\ne0.              \tag{9}
\]

Equivalently, after scaling `h_phys`,

\[
               h_{phys}-e_\tau^*\in\operatorname{row}(A_D). \tag{10}

\]

Equation (10) is the exact coloop-normalization transport criterion: the
physical row and target selector define the same nonzero functional on the
circuit kernel.  In a larger reachable block the stronger equality of their
restrictions to the entire kernel is likewise equivalent to their classes
agreeing in `X^*/row(A)`; mere nonvanishing on one circuit is enough for the
rank-two theorem on that circuit.

The distinction is real.  Take

\[
 C_1=e_1,\quad C_2=e_2,\quad C_3=e_3,\quad
 t=e_1+e_2+e_3,\quad g=e_4.                            \tag{11}

\]

The affine fibre has the unique minimum solution `(1,1,1)` and meets no
coordinate line.  Its augmented circuit is `(1,1,1,1)`.  The formal
`e_tau^*` border has rank `rank(A)+2=5`.  But the abstract target-bearing row

\[
                         h=(1,0,0,-1)                 \tag{12}

\]

is already the first row of `A`, kills the circuit, and gives only rank
`rank(A)+1=4` after `g` is appended.  Adding `e_tau^*` to (12) produces a
row satisfying (10), and the two-rank gain returns.  This is a logical
rank guard, not a claim that (11)--(12) form a Krenn source.  The pinned
physical pure-target triangular block exhibits the same one-rank failure in
the source presentation.  Hence a coefficient normalized to one is not
itself the missing physical unit row.

## Exact proof interface

Starting from a saturated reachable family of complete columns, the
structural fork is now:

```text
minimum affine support
  -> target-containing circuit
  -> internal placed Cartan
       -> normalized circuit exchange or homogeneous unit-Cartan kernel
  -> external placed Cartan
       -> target-dark complete-row separator
```

The internal branch yields support deletion only after literal endpoint and
anchor-safe typing; otherwise it feeds the established relative
kernel/terminal alternative.  The external branch yields a source unit or
Hall exit only after its covector is physically typed.  If neither typing is
available, the exact remaining datum is one complete-row lift of the
target-dark separator, not another affine-support enumeration.

This isolates the global accessibility theorem's first missing physical
statement: on every saturated target circuit, either a literal physical row
satisfies (9), or the target-dark separator (5) is the covector of a typed
Hall/Fitting exit.

## Scope versus global source entry

This theorem begins **after** a complete endpoint response fibre and its
target `t` have been identified.  It therefore sharpens the normalization
of an already constructed active-fan coloop.  In particular, it closes no
more than the determinant-bright branch unless another argument first
constructs such a fan.

An arbitrary maximum-anchor/minimum-support source initially supplies only
a protected-relative frame circuit for the unsigned port-incidence map.
That circuit may be a long even cycle or an odd handcuff.  The existing
trichotomy says:

```text
squarefree + common tail -> candidate in one complete matching word;
squarefree - common tail -> general Tutte accessibility barrier;
repeated site/path       -> Cartan-Spencer collision grade.
```

Even on the first branch, the other matchings in the complete row produce a
defect, so the optical circuit is not yet a kernel of the complete labelled
source map.  The exact global entry still missing is a source-provenant
chain lift which either nullhomotopes that defect while retaining a marked
physical anchor coordinate, or turns the dual separator into a literal
source/Hall exit.  For no-common-tail long circuits it must additionally
lift the general Tutte barrier to an anchor-preserving complete-row
augmenting path; star, triangle, and `K2,2` are only its smallest shadows.

Thus arbitrary coloop normalization does not replace global source
connectivity.  It supplies the terminal matroid fork once the long optical
circuit has reached a physically typed affine response component.

## Scope and verification

This note proves the affine/matroid and rectangular linear-algebra
alternative.  It uses the committed uniform physical Cartan provenance but
does not prove that every circuit exchange has the required endpoint word
and fine-label placement, nor that every target-dark separator is a
physical Hall row.

Run

```text
python3 computations/verify_target_augmented_affine_circuit_cartan_guard.py
python3 -O computations/verify_target_augmented_affine_circuit_cartan_guard.py
python3 -I -S computations/verify_target_augmented_affine_circuit_cartan_guard.py
```

Frozen ledger SHA-256:

```text
4a9b28e031310e40adbd8dc09e58f83975575375e873406b3182095aaec8457d
```
