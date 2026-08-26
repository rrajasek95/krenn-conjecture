# Supersession: shell-private is not full-D12 private

`results_d12_private_ownership.json` uses the field name
`global_private_new_row`.  Its quantified universe is only the accepted repair
packet (or the round-13 pending packet) relative to the preceding selected row
interface.  It does **not** assert uniqueness among every homogeneous D12
mixed-generator column.

Full incidence falsifies that stronger reading.  The lex-first shell owner
`(code=4,multiplier=0a52b8ee)` has coefficient `+1` on target-zero row
`0a12515291c1e5eb`, but that row is incident to 91 column orbits.  The lex-first
outside owner is `(code=4,multiplier=0a12515291c1e5eb)`, also with coefficient
`+1`; it is neither selected nor in the round-13 pending packet.

Authority: `results_d12_first_external_owner.json`.  The complete bounded
counterowner census is `results_d12_shell_counterowners.json` (logical
`d04715ede95aa4194acf0f2ee9dd829e568a1b09186c6cc6dfdf685375ed7444`): all
1,186 shell columns have an unselected, outside-shell external owner.
No full-D12 nonmembership follows from shell ownership alone.
