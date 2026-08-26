# Round1588 cap3.0m to cap3.25m gate

The gate ran two sequential one-round lanes from distinct fresh clones of the independently audited round1587 endpoint. Every mathematical and resource setting was fixed except the column cap. The frozen v4.1 source, binary, and watchdog hashes matched; both watchdogs passed with atomic outputs below the 36 GiB limit.

Both lanes reached round1588 with 2,940,643 columns and dual support 5,029. Checkpoint SHA `e94a0965eb8d9a7bbb602726635093b9e0ca27a9d9af0ea38703a8bf3498d5b6` and vector-cache SHA `c4ae2b91e86f4b373f078304d0d79416970bd636d97912b25eadc45c86428e05` are byte-identical. After removing timing fields, the only semantic/configuration difference is the declared column cap change from 3,000,000 to 3,250,000.

The cap3.25m candidate is sealed and held for independent audit. No continuation was launched.
