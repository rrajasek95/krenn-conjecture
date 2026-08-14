# Three pure target normalizations do not break a centered `K2,2` family

## Verdict

The hoped-for global signed-sum theorem is false at the complete-row
interface.  A finite family of centered balanced `K2,2` components is
exactly compatible with all three pure target normalizations

\[
                            P_0=P_1=P_2=1.              \tag{1}
\]

The decisive invariant is a Fredholm pairing, but centeredness makes that
pairing vanish.  Thus normalization supplies no contradiction and cannot,
by itself, force an uncentered component, odd holonomy, a unit, or an active
outside fan.

There is a smallest exact occurrence-typed guard with two `K2,2` blocks.
If one imposes the stronger recurrent-core convention that every block has
one monochromatic common core, the smallest guard has three blocks, one per
target colour.

Exact checker:
[`verify_uniform_global_centered_k22_normalization_counterguard.py`](../computations/verify_uniform_global_centered_k22_normalization_counterguard.py).

## 1. The exact global invariant

For one component, order the complete rows by

```text
A0, A1 | B0, B1
```

and write them together as

\[
                    F=T^{\mathsf t}p+B^{\mathsf t}z.   \tag{2}
\]

Here `p=(P0,P1,P2)`, the columns of `T` record which pure-target
occurrence is carried by each row, and `B` is the four-edge unsigned
incidence matrix of `K2,2`.  The unique transported companion charge is

\[
                         \lambda=(1,1,-1,-1),           \tag{3}
\]

so `ker B` is spanned by `lambda`.  The affine zero-row equations (2) are
soluble precisely when

\[
       \lambda^{\mathsf t}T^{\mathsf t}p
                    =(T\lambda)\mathbin{\cdot}p=0.     \tag{4}
\]

This is the complete signed-sum/holonomy invariant.  For a disjoint family,
there is one condition (4) per component; taking signed sums between
components only takes linear combinations of these conditions.

Call a component **coordinatewise centered** when

\[
                              T\lambda=0.               \tag{5}
\]

Then (4) holds for every value of `p`, in particular for (1).  Moreover,
every global companion syzygy is a combination of the component charges,
and its pure-target image is zero.  Therefore no global signed sum of the
complete zero rows projects any nonzero combination of `P0,P1,P2`.

Notice the direction of the result: the same centeredness which obstructs
the local common-core projector also guarantees compatibility with the
three normalized target values.

## 2. Smallest occurrence-typed normalized guard

Assume every complete row carries exactly one pure-target occurrence.  Use
two disjoint internal `K2,2` blocks with shorewise colour words

```text
block I  :  A0 A1 | B0 B1 = 0 1 | 0 1
block II :  A0 A1 | B0 B1 = 2 0 | 2 0.
```

In each block introduce four internal companion coordinates
`z00,z01,z10,z11` and use the usual complete rows

\[
\begin{aligned}
F_{A0}&=P_{\kappa(A0)}+z_{00}+z_{01},&
F_{A1}&=P_{\kappa(A1)}+z_{10}+z_{11},\\
F_{B0}&=P_{\kappa(B0)}+z_{00}+z_{10},&
F_{B1}&=P_{\kappa(B1)}+z_{01}+z_{11}.                 \tag{6}
\end{aligned}
\]

The two colour multisets on the shores of each block agree, so (5) holds
in every target coordinate.  The exact rational point

\[
             P_0=P_1=P_2=1,
             \qquad z_e=-\tfrac12\quad\hbox{for all eight edges}           \tag{7}
\]

kills all eight complete rows.  Every row has two companions, every
companion occurs in two rows, both components have even holonomy, and all
companions are internal to their declared block.  Hence there is no
singleton, no odd unit, and no outside-fan term in this abstract module.

This guard is minimal under the stated typing.  In a coordinatewise
centered block, the two colour multisets on its two-vertex shores must be
equal.  One block can therefore involve at most two colours.  Covering all
three normalized target rows needs at least two blocks, and (6) attains the
bound.  The checker exhausts all one- and two-block colour assignments.

## 3. Monochromatic common-core variant

If every recurrent component is required to have one common pure core in
all four rows, use the three blocks

```text
0000, 1111, 2222.
```

Again set all three pure cores to one and all twelve internal companions to
`-1/2`.  All twelve complete rows vanish.  The global companion kernel is
three-dimensional, spanned by the centered charge (3) on each block, and
the three charges all map to zero in the pure-target space.

Three blocks are plainly minimal in this stronger convention: a
monochromatic block participates in only one of the three target rows.
Thus even the literal “one recurrent common core per target colour” model
does not acquire a global normalization obstruction.

## 4. What extra hypothesis would suffice

Equation (4) gives the sharp alternatives.  The argument can advance only
if the physical source labels prove at least one of the following:

1. some completed component has transported target charge `T lambda` whose
   pairing with `(1,1,1)` is nonzero;
2. odd multiplicative holonomy destroys the nonzero transported charge;
3. a companion coordinate is private/deletable; or
4. mandatory boundary completion links an internal block to a genuinely
   active outside-fan occurrence.

Pure normalization proves none of these.  If all companion coordinates
remain internal, the global incidence matrix is block diagonal and its
kernel is exactly the direct sum of the centered component charges.  A
cross-component boundary theorem, with physical port/site typing retained,
is therefore the shortest positive attack; another unsigned global sum is
not.

## Scope

This is an exact rational complete-row counterguard.  It tests the proposed
implication from balanced component algebra plus the three target
normalizations.  It is not claimed to be a full ternary decorated-hafnian
source, so a stronger physical realization/exclusion theorem remains
available.

Run

```text
python3 computations/verify_uniform_global_centered_k22_normalization_counterguard.py
python3 -O computations/verify_uniform_global_centered_k22_normalization_counterguard.py
python3 -I -S computations/verify_uniform_global_centered_k22_normalization_counterguard.py
```

The checker uses exact rational arithmetic, pins the local projection and
balanced-square audits, verifies (4), exhausts the minimality claim, and
checks both guards in all three interpreter modes.
