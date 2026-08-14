# An executable Gamma-star registry stops at one missing operation arrow

## Verdict

The smallest source registry assembled from the actual callable h=3
constructors has now been built.  It contains the implemented response KS,
cap `r0`/AugP2, PP/Hasse, Cartan/Weyl, `K_Eq`, and strict relative
bar-times-`K_Eq` primitives.  It does not use the 17 prose census records as
generators.

The exact result is

```text
implemented primitive entries                 128
literal Gamma* entries                          25
off-Gamma* entries                             103
rank of the 27-row Gamma* image                 23
rank of the eight-row B/Eq image                 7
Psi charge of every registered entry             0
literal kappa entries                             0.
```

The registry comparison is the literal direct-sum projection

\[
 \Pi_{\Gamma_*}:\operatorname{Gen}_{\rm impl}longrightarrow
 Y_{\Gamma_*}^{27}.
\]

It retains the actual 27-entry vectors returned by the cap constructors and
sends implemented primitives with orthogonal word/fine/repeated/operation
idempotents to zero.  This is an executable comparison on the named
implemented source APIs; it is not claimed to be a census of an unwritten
full physical complex.

The first absent constructor is precise:

\[
 \Phi_{KS,r0}:\epsilon_s\;\hbox{in the response object}
       \longrightarrow r_0\;\hbox{in the cap object}.                 \tag{1}
\]

Calling the registry mapping-cylinder operation on this pair raises

```text
MissingPhysicalArrow:
no registered degree-zero physical arrow response:epsilon_s -> cap:r0_0
```

Exact checker:
[`verify_h3_gamma_star_executable_gen_phys_registry.py`](../computations/verify_h3_gamma_star_executable_gen_phys_registry.py).

## 1. Entries emitted by actual constructors

The registry stores, for every primitive,

```text
name, family, homological degree, literal grade,
producer API, native boundary vector, Gamma* boundary vector.
```

Its entries split as follows.

| Implemented family | Count | Native output | `Gamma*` image |
|---|---:|---:|---:|
| cap `r0` | 4 | 27 rows | retained |
| cap normalizers `T,rho` | 8 | 27 rows | retained |
| cap Cartan/Weyl | 5 | 27 rows | retained |
| target, `q`, `P_f`, ridge, eta, sigma, complete cap | 8 | 27 rows | retained |
| fixed-window PP/Hasse word faces | 36 | 48 rows | zero |
| fixed-window `C4` matching flips | 24 | 48 rows | zero |
| fixed-window response/relative/retained faces | 40 | 48 rows | zero |
| selected response KS `epsilon_s` | 1 | 90 rows | zero |
| strict covariance-bar times `K_Eq` cell | 1 | 3 symbolic rows | zero |
| Macaulay `b01*r0` product | 1 | 2 Leibniz rows | zero |

The cap `r0` provenance is checked by executing the translated physical
totalization: its private full-nine boundary and internal reduced-`Eq`
differential are genuinely tied.  The fixed-window constructor directly
returns its 100 labelled 48-entry columns.  The response constructor supplies

\[
 d\epsilon_s=-c_f,\qquad c_f=90e_f-\mathbf1_{90}.      \tag{2}
\]

Finally, the covariance bar and central cone form the genuine strict cell

\[
 \kappa_{bar}=E\theta,qquad
 d\kappa_{bar}=(L-D)\theta-EF,qquad d^2=0.             \tag{3}

Equation (3) is not discarded.  Its implemented grade is squarefree `2K2`
with local-GL3 covariance/output-bar operation parent.  Tensoring with
`K_Eq` preserves those idempotents, so its literal projection to the selected
`t*q_(v,N)`, `P3+K2`, response-to-AugP2 summand is zero.

## 2. Why the standard cylinder cannot yet make kappa

Forgetting the labels, the response and cap two-term complexes admit a unique
normalized chain-map shape:

\[
 d\epsilon_s=-c_f,quad dr_0=E,qquad
 \Phi_1(\epsilon_s)=r_0,quad \Phi_0(c_f)=-E.           \tag{4}

There is no scalar or sign obstruction.  The obstruction is the operation
matrix unit.  In the current fixed source,

```text
response identity       response -> response
cap identity            cap -> cap
required Phi            response -> cap.
```

Only the first two are implemented.  A standard mapping cylinder is a
constructor on an already supplied chain map; it cannot create the third
matrix unit.  The registry therefore makes cylinder formation a partial API
and throws `MissingPhysicalArrow` on (1).

The mismatching literal tags are all five retained coordinates:

```text
word, fine degree, repeated shape, operation parent, window/occurrence.
```

This is stronger than saying that the map has not been named.  The current
operation algebra has degree-zero `Hom(response,cap)=0`, while the unique
ungraded shape (4) lives in the missing off-diagonal coordinate.

## 3. The `b01*r0` Macaulay shortcut is cap-internal

The physical polynomial product is a genuine new registry entry.  Executing
the selected first-PP constructor gives the six literal terms of `db01`, and
Leibniz gives

\[
             d(b_{01}r_0)=db_{01}r_0+b_{01}E.          \tag{5}

Its next boundary cancels exactly:

\[
 d(db_{01}r_0)=-db_{01}E,qquad
 d(b_{01}E)=+db_{01}E.                                 \tag{6}

Thus the shortcut is not rejected for algebraic or `d^2` reasons.  It fails
by literal object typing.  There are two possible readings:

```text
response copy b01 : response -> response
cap r0             : cap -> cap
product             undefined/zero (orthogonal idempotents);

cap copy b01       : cap -> cap
cap r0             : cap -> cap
product             cap -> cap.
```

The required map (1) has type `response -> cap`.  Consequently the valid cap
copy of (5) is a cap-parent PP/Macaulay column.  Its `db01*r0` is not the
response-selected `db01`, and its `b01*E` is not the cross-summand incidence

\[
                 \Phi((H_0-u)e_{Eq})=R_{E14}.          \tag{7}

The checker retains (5), verifies (6), and computes its literal mixed
`Gamma*` projection to be zero.  Macaulay multiplication therefore does not
supply the missing matrix unit.

## 4. Smallest positive API addition

One normalized constructor schema would suffice:

```text
Phi_KS,r0(
    response epsilon_s,
    cap r0,
    selected db01 and endpoint/root-labelled mates,
    central Eq incidence (7),
    six P3+K2 and six sibling 3K2 faces,
    q/W/residue/ridge/eta/sigma faces
) -> physical degree-zero response-to-cap arrow.
```

Once this arrow exists, the already implemented standard cone product gives
eight literal instances, one for each lower word

```text
0012, 0102, 0110, 0111, 0122, 0212, 1112, 2112.
```

Strict normalized multiplicativity then gives

\[
 \Pi_{B/Eq}(d\kappa_i)=(v_i,v_i),\qquad
 \lambda_i=\frac14\delta\cdot(v_i-v_i)=0              \tag{8}

for all eight.  Equation (8) is currently conditional: those eight columns
are not entries of the implemented registry.

## Scope

This closes the API audit requested after `754c64c`: among the named actual
primitive constructors, the obstruction is not an unknown charge but the
absence of the degree-zero arrow on which the kappa mapping cylinder depends.
It does not prove that the 128 registered primitives exhaust every possible
physical source operation.

Run all modes:

```bash
python3 computations/verify_h3_gamma_star_executable_gen_phys_registry.py --mode all
python3 computations/verify_h3_gamma_star_executable_gen_phys_registry.py --mode registry
python3 computations/verify_h3_gamma_star_executable_gen_phys_registry.py --mode missing-arrow
python3 -O computations/verify_h3_gamma_star_executable_gen_phys_registry.py --mode all
python3 -I -S computations/verify_h3_gamma_star_executable_gen_phys_registry.py --mode all
```

Frozen ledger:

```text
195d8fe444c0efc0d3cfd3c81ff8347fcccafd75a0535110cd3716b5a6001096
```
