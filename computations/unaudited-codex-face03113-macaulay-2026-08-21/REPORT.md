# Face `(0,31,13)`: bounded homogeneous Macaulay audit

Status: the exact characteristic-zero unit remains open.  The complete
degree-9 homogeneous component of the known 12-row affine-unit discovery core
does **not** contain `t^9` modulo 1009.  This is a degree-9 lower bound only;
it is not a nonunit statement over `Q` or over the affine localized chart.

## Literal interface

`export_face03113_macaulay.py` reads the frozen face record from
`results_recursive_face_charts.json`, keeps raw rows

```
7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
```

and appends the combined selected-base/remaining-C Rabinowitsch generator

```
s * (a5*b3*b4) * (1+a0)*(1+a2*d2)*(1+a3*d3) - 1.
```

Each source generator is homogenized to its own degree.  At total degree 9,
the exporter includes every homogeneous multiplier of the complementary
degree and retains every output term, including repeated-term coefficient
merging.  The resulting literal matrix has 135,659 rows, 70,071 columns, and
637,555 nonzeros.

Input SHA-256:

- exporter: `107e216b57910cd5b8c209a1ff9a35f6a49cfc8b4a89bdf172ac6a587fd48c05`
- full degree-9 JSONL: `a916a41bfa53d63815830b9d80359d471182f64ca8d6fa2be9fa0dc19f627b61`

The direct sparse solve of the unpeeled matrix timed out after 300 seconds at
the first prime; no mathematical conclusion is taken from that timeout.

## Sound structural reduction

`peel_target_component.py` repeatedly removes an active column only when it
has a private active row whose target coefficient is zero.  Such a column has
coefficient zero in every representation of the target.  The script aborts
if a target-bearing row would be peeled.  It then retains the unique active
connected component bearing `t^9`; all other components may be assigned zero.

The cascade starts with 40,873 row leaves, removes 47,276 forced-zero columns,
and leaves a target component with 31,847 rows and 22,339 columns.  These
counts independently agree with `core_structure`'s structural census.

- peel script SHA-256: `a39b3ff186e87522ea0775ee105f6ad1ef4ed5ee31476ce90e04b68ecf532167`
- target-core JSONL SHA-256: `d3dc5e0ca91fb0409f417a9a6e5178cc75832212746b66e70cb11711332f536c`

## Modular degree-9 verdict

The no-crate common-echelon solver at `p=1009` completed on the exact target
component:

```
rank                         20,821
dependent columns             1,518
target in image               false
target remainder nonzeros     4,878
partial solution terms       12,945
left-dual terms               7,211
left-dual/target pairing         572  (mod 1009)
elapsed                      218.803 s
```

The modular result SHA-256 is
`4e6d8818e588bde07eb8e3bcf31fdaf5b1d0b5544dfd00cad6fabe04aa19bc73`.
It proves only that this 12-row homogeneous degree-9 component is outside the
target at characteristic 1009.  In particular it does not imply affine
nonmembership, characteristic-zero nonmembership, or failure after restoring
the four omitted literal rows.

The automatically started `p=1013` run was interrupted on the manager's stop
request.  Its partial JSON is not evidence and is intentionally absent from
the manifest.  A finite-field deletion search was likewise stopped after
three 90-second timeouts and yielded no row deletion.

## Remaining exact gate

The original affine two-prime Gröbner lead says this 12-row subsystem is a
unit modulo 1009, so a homogeneous unit exponent exists in that
characteristic but is greater than 9.  The next sound options are a
coordinated degree-10/all-16-row Macaulay run with the same forced-zero peel,
or an exact smaller algebraic row/localizer identity.  Neither was launched
after the manager requested terminal status.
