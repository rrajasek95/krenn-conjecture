# Holonomy orbit versus the carrier-aligned minors

Status: **exact negative attachment theorem.**  The full coned
`S8 x S3` orbit of the selected holonomy identity does not force the 56
maximal minors of the canonical carrier matrix, even after pure normalization
and localization at all three pure cap cofactors.  A literal 16-cell rational
source is an exact counterguard.

## 1. The selected determinant and its orbit

For the selected triangle `012`, columns `01,02,12`, and the three full slice
words

```text
01211222, 01200000, 01211111,
```

let

```text
H = det(C_(01211222), C_(01200000), C_(01211111)),       (1)
```

where each row consists of the three literal residual six-site cofactor
polynomials.  Each entry has source degree three, so `H` has degree nine.
The frozen pure cone is

```text
M=A_01[0,0] A_23[0,0] A_45[0,0] A_67[0,0].             (2)
```

The exact group census is

```text
|S8 x S3|                                      241,920
unconed H orbit                                  20,160
unconed datum stabilizer                             12
coned (M,H) orbit                               120,960
coned-pair stabilizer                                 2
pure cone monomials                                  315
H rows paired with one fixed cone                    384
cones paired with each fixed H                         6.
```

Thus a theorem `M H in I_X5` and all its transports does **not** say that all
20,160 unconed determinants vanish.  On a chart with one live pure cone it
gives only the 384 determinants paired with that cone.  Pure normalization
makes at least one of the 315 cone monomials live; it does not make every cone
paired with a chosen `H` live.

## 2. Exact degree-nine nonmembership

Give a source cell its site-colour torus degree

```text
deg A_uv[a,b] = e_(u,a)+e_(v,b).                         (3)
```

The selected `H` is homogeneous for this fine grading.  Its weight rows by
site are

```text
site 0: (1,0,0)        site 1: (0,1,0)       site 2: (0,0,1)
sites 3,4: (1,2,0)     sites 5,6,7: (1,1,1).             (4)
```

All 20,160 orbit elements have distinct fine weights.  The base polynomial
is nonzero—it evaluates to `1893145593205` at the pinned dense rational
source—so the exact orbit span has rank 20,160 without a coefficient-matrix
solve.

For residual pure colour `c`, the canonical `8 x 3` carrier matrix uses the
eight mixed cap words

```text
ccccccij,   (i,j)!=(c,c),
```

and the same internal-edge columns.  In every one of its maximal minors the
three degree-one triangle ports `0,1,2` all have colour `c`.  In every orbit
element (4), those three degree-one ports have three distinct colours.  Hence
the fine-weight sets are disjoint:

```text
H-orbit polynomials / weights                     20,160 / 20,160
carrier minors, three colours                         168
distinct carrier weights                               123
intersection of weight sets                              0.  (5)
```

All 56 minors in each colour are honest nonzero polynomials.  The dense exact
source `seed=1` evaluates all 168 nontrivially; the determinant-list digest is
`a8fb2c909b15fca08d7cee78752f5ab885a1ad9663676d8aa9c8d94d1a5b42c6`.

It follows immediately that no carrier minor lies in the orbit span.  Since
both the orbit generators and the minors have total degree nine, the degree-
nine piece of the unlocalized homogeneous orbit ideal is exactly that span.
Therefore no carrier minor lies in that ideal either.

## 3. Pure-open literal counterguard to the coned ideal

Every unspecified source cell below is zero.  Put unit diagonal cells on

```text
colour 0: 01,23,45,67
colour 1: 02,13,45,67
colour 2: 03,12,45,67,                                  (6)
```

and add the four unit cells

```text
A_26[0,0], A_16[0,1], A_06[0,2], A_37[0,1].             (7)
```

This source has exactly 16 nonzero cells.  Literal perfect-matching replay
gives

```text
F_(0^8)=F_(1^8)=F_(2^8)=1,
P_0=P_1=P_2=1,                 D=P_0 P_1 P_2=1,          (8)
nonzero pure cone monomials=3.
```

The checker enumerates all 120,960 distinct coned orbit polynomials.  The
119,808 pairs with a zero cone vanish immediately; on the three live cone
charts it evaluates all

```text
                         3 * 384 = 1,152                 (9)
```

literal `H` determinants.  Every one is zero.  Hence every transported
polynomial `M_g H_g` vanishes at (6)--(7).

For residual colour zero, however, the canonical mixed carrier rows include

```text
C_0[01]=(1,0,0),
C_0[11]=(1,1,0),
C_0[21]=(0,0,1).                                       (10)
```

Thus

```text
rank C_0=3,       Delta_(01,11,21)=1.                   (11)
```

Evaluation at this literal source annihilates the coned orbit ideal together
with the three pure-normalization equations, while `D=1` and the carrier
minor (11) equals one.  Consequently

```text
Delta_(01,11,21) notin radical(
  <all transported M_g H_g, F_(c^8)-1> : D^infinity).   (12)
```

Equation (12) is the requested pure-cofactor-open counterguard.  It also
guards the common mistake of replacing the coned orbit by the full unconed
`H` orbit.

## 4. Exact scope and downstream consequence

The source (6)--(7) has 33 nonzero mixed output amplitudes, all equal to one.
It is not a full `X5` point and does not contradict a future theorem using
all 6,558 mixed equations.  It proves the precise negative statement:

> Even if lazy full-X5 CEGAR proves the selected coned holonomy identity, its
> complete transported orbit, pure normalization, and inversion of
> `P_0P_1P_2` do not by themselves imply carrier rank at most two.

Full `X5` equations beyond the coned consequences are load-bearing for any
carrier-alignment theorem.  The artificially stronger saturation problem for
the ideal generated by **all unconed** 20,160 `H` polynomials is separate and
is not justified by the coned theorem.  Fine degree does not settle that
stronger problem after localization: already `D` times each carrier minor
componentwise admits between 240 and 3,600 candidate `H` weights.

## Replay

```sh
python3 computations/unaudited-codex-holonomy-orbit-carrier-alignment-2026-08-23/audit_holonomy_orbit_carrier_alignment.py --write-results
python3 -O computations/unaudited-codex-holonomy-orbit-carrier-alignment-2026-08-23/audit_holonomy_orbit_carrier_alignment.py
python3 -I -S computations/unaudited-codex-holonomy-orbit-carrier-alignment-2026-08-23/audit_holonomy_orbit_carrier_alignment.py
```

The hostile `--mutate-carrier-colour` mode fails.  Logical digest:
`12b95febe56e423108941ccdd0740b1242e9bf940df701f81c9c9debb1968bf2`.
