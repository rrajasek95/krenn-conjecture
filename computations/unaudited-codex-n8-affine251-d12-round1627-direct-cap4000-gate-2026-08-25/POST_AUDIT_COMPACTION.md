# Post-audit compaction at round 1627

Status: PASS

Independent audit `c43b18138cbca585e5256ee5809e94ed16d96eefa3771b695cd93850c53d039b` and manifest `20441719604745ddcdb7c12a75111bb27aa3ee4477d12c4b135c76fc5069530f` sealed PASS first.

Exactly four superseded payloads were removed, retaining every small evidence file and the accepted candidate:

- `control_cap3750/checkpoint.bin` (`40a76f726f40fb022909f219b6ace5d8ee5f04fb5847cb1e37a3cea2829e308e`)
- `control_cap3750/vectors.bin` (`4ae60b262d5bdcea3488ed0bb194e95d338bb962beb172cec33e9ddc76de8eeb`)
- `../unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1614_cap3750_to1626/stage12_cap1626/checkpoint.bin` (`bbee936b4c53882f075c6afb9ec7284ddc36ba29608fa7bdb27062beb54ebdb3`)
- `../unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1614_cap3750_to1626/stage12_cap1626/vectors.bin` (`0dd351df751dc83afecc8b456736b7b45e4c814538b3244a4d9b1f11180a5402`)

Free space increased from133,281,796 KiB to148,389,404 KiB. Candidate revalidation passed at checkpoint `40a76f726f40fb022909f219b6ace5d8ee5f04fb5847cb1e37a3cea2829e308e` and cache `4ae60b262d5bdcea3488ed0bb194e95d338bb962beb172cec33e9ddc76de8eeb`.
