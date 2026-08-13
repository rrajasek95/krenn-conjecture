# Centered shear: the exact `H0` and target-cylinder alternative

## Result

The ordinary Segre Tate cells and the relative centered cell solve different
problems.

- The ordinary cells `d e_ij=F_ij` resolve the physical toric presentation
  and preserve `H0=A`, but they cannot carry the centered shear because
  `D(F_ij)=-L k_ij` is nonzero in `A`.
- The relative cell `d epsilon=L` makes every such defect exact and permits
  the recursive lift, but changes `H0` to `A/(L)`.
- An `H0`-preserving target cylinder `d epsilon=L-t` exports, rather than
  cancels, the obstruction: `[d,D](e_ij)=t k_ij`.

The third line is not a third honest DGA lift.  It is precisely a curved
comparison/terminal alternative.  Algebraically it retains the source
`H0`; physically it requires a new mixed endpoint-by-matching target module
in the doubled Segre grade.  The current scalar response target does not
supply that module.

Checker:

```text
computations/verify_h3_centered_shear_h0_target_cylinder_alternative.py
```

Frozen ledger digest:

```text
783b96dc336332e84ce8037213e157a04c385705de4f285ce3ffc4440fa0cfa9
```

## 1. Why ordinary Tate resolution cannot help

Let

\[
 S=k[u_{rj}],
 \qquad
 A=S/I,
 \qquad
 I=(F_{01},F_{02},F_{12})
\]

be the local `2 x 3` Segre occurrence algebra.  The ordinary Tate cells

\[
 d e_{ij}=F_{ij}
\]

and their Hilbert--Burch coherence resolve `A`.  In particular their degree
zero homology remains `A`.

Now let `D0(u_rj)=-L`.  Directional differentiation gives

\[
 D_0(F_{ij})=-Lk_{ij}.                               \tag{1}
\]

At the physical point

```text
(e0,e1;q0,q1,q2)=(1,2;1,3,5),
```

the three minors vanish while

```text
(k01,k02,k12)=(2,4,2).
```

Thus (1) is not in `I` when `L` is nonzero.  This is an ideal-membership
witness, not only a tangent-space count.

More generally, let `Q` be any connective semi-free DGA under `S` with
`H0(Q)=A`.  An honest chain derivation on `Q` descends to a derivation on
`H0(Q)`.  Therefore it must send every `r in I` to zero in `A`.  Equation
(1) violates that necessary condition.  Adding more ordinary contractible
Tate cells while preserving `H0=A` cannot change it.

This proves the no-third-option statement for honest DGA lifts:

> A non-tangent degree-zero shear cannot become an honest chain derivation
> on any connective resolution with unchanged degree-zero homology.

## 2. Killing `L` solves the lift and changes `H0`

Adjoin one relative generator

\[
 d\epsilon=L.
\]

Then

\[
 D(e_{ij})=-\epsilon k_{ij}
 \quad\Longrightarrow\quad
 dD(e_{ij})=-Lk_{ij}=D(F_{ij}).                      \tag{2}
\]

The domain property makes `L` regular, so the full recursive Tate lift has
no higher obstruction, including over `k[beta]`.  But the degree-zero
homology is now

\[
 H_0=A/(L),
\]

not `A`.  Calling this a cofibrant lift of the unchanged physical source
would be incorrect.

Any other honest extension making a nonzero `Lk_ij` a boundary has the same
basic issue: its degree-zero class vanishes, so `H0` cannot remain
canonically equal to `A`.

## 3. The target-cylinder model

Introduce a degree-zero output coordinate `t` and use the mapping cylinder

\[
 d\epsilon=L-t.                                      \tag{3}
\]

Because (3) merely identifies `t` with `L`,

\[
 H_0=A[t]/(t-L)\cong A.                              \tag{4}
\]

Keep `D(e_ij)=-epsilon k_ij`.  Equations (1) and (3) give

\[
 \begin{aligned}
 dD(e_{ij})&=-Lk_{ij}+tk_{ij},\\
 Dd(e_{ij})&=-Lk_{ij},\\
 [d,D](e_{ij})&=tk_{ij}.                             \tag{5}
 \end{aligned}
\]

Thus the cylinder retains the physical source homology by exporting the
non-tangency as target curvature.  If `tk_ij` is accepted as a physical
terminal, (5) is the desired nonlift branch.  If one also forces `tk_ij` to
be a boundary, its nonzero `H0` class is killed and the construction again
ceases to preserve `A`.

The exact trichotomy is therefore:

1. `D0(I) subset I`: an honest tangent lift may exist;
2. kill `L`: the relative lift exists with `H0=A/(L)`;
3. retain `H0=A`: the nonzero curvature `t k_ij` must remain as an output
   terminal.

There is no fourth honest DGA option.

## 4. Why the current response target is insufficient

In the coordinate order

```text
(Aq0,Aq1,Aq2,Bq0,Bq1,Bq2),
```

the three local toric characters are

```text
xi01=(-1,+1, 0,+1,-1, 0)
xi02=(-1, 0,+1,+1, 0,-1)
xi12=( 0,-1,+1, 0,+1,-1).
```

They span a two-dimensional module.  Every endpoint row sum and every
matching-column sum annihilates them.  Representation-theoretically this is

\[
 \text{endpoint-odd}\otimes\text{matching-standard}.             \tag{6}
\]

The complete global orbit has rank thirty.  By contrast, the current
response target normal is an aggregate scalar/trivial representation; the
ordinary Segre Tate cells have target and central-Eq value zero, and the
known aggregate anchor/physical-`q` shadows also kill (6).

Consequently the formal output `t k_ij` in (5) is not yet a physically typed
terminal.  To make the cylinder physical one must construct one covariant
mixed target family in the doubled word/fine/repeated Segre grade.  Mapping
the mixed character into the decorated private-site fan is another valid
landing, but it still requires the open incidence square identified in
`55054a0`.

Multiplying the old scalar target symbolically by `k_ij` simply postulates
this missing labelled module; it does not construct it from existing source
rows.

## 5. `beta` and scope

The algebraic trichotomy is unchanged over `k[beta]`.  Multiplication by
`beta` does not alter the endpoint-by-matching character.  Setting the new
target coordinate `t` equal to the base parameter `beta` would impose
`beta=L` on degree-zero homology and is not an `R`-linear preservation of
the physical source.

This result is exact for the canonical `h=3` Segre response block.  It does
not construct the mixed target terminal, its word-changing E14 placement,
the private-site incidence, or the augmented `q`, cap/ridge, eta/sigma
readouts.

## Verification

Run normally, optimized, and isolated/no-site.  Expected headline:

```text
ordinary Segre Tate: H0=A, centered shear lift IMPOSSIBLE
relative d(epsilon)=L: lift EXISTS, H0=A/(L)
target cylinder d(epsilon)=L-t: H0=A, curvature=t*k
current physical scalar output: missing mixed t*k terminal
```
