# Evidence pack: C-2026-014 Blue Harbor Logistics, Inc.

**Workpaper:** REV-AI-2026-01 | **Evidence IDs:** EV-03, EV-04, EV-05, EV-06, EV-16
**Contract:** C-2026-014 | **Customer:** Blue Harbor Logistics, Inc. (fictional) | **TCV:** $1,440,000
**Period:** executed 2026-07-01 | **Sealed:** 2026-10-09 after the journal entry posted
**Status:** Fictional sample. No real agreement, party or person is represented.

## What this pack demonstrates

The pack shows what a reviewer or external auditor would receive for one contract in an AI-assisted revenue workflow: the model output with clause citations and version identifiers, the independent calculation, the reviewer's clause-level annotation, the second-level review memorandum, and a manifest that lets a third party prove nothing changed after close.

The contract and the redaction log are not included. In production the pack also holds the executed agreement (`01_contract`), the intake checklist (`02_intake`) and the redaction log (`03_redaction`). They are omitted here because a real pack would carry confidential customer data. The full structure is in section 9.3 of the workpaper.

## Files

| File | Role | Control | What it shows |
|---|---|---|---|
| `04_ai_output_C-2026-014.json` | Model output | CL-07 | Ten extracted fields with clause citations, spans, confidence, flags and the proposed single-performance-obligation conclusion. The material right field is wrong: the model concluded `false`. |
| `05_calc_C-2026-014.xlsx` | Independent calculation | CL-08 | Relative SSP allocation, monthly and FY2026 revenue, the journal entry and the SSP table version. Ties to the reviewer's correction. |
| `06_review_C-2026-014.md` | Reviewer annotation | CL-09 | Per-field agreement, the override rationale, the material right estimate and the sign-off identity. |
| `07_sl2_C-2026-014.md` | Second-level review | CL-10 | Why the contract was escalated, what the second reviewer tested, sensitivity and concurrence. |
| `manifest.tsv` | Pack manifest | EV-16 | File names, byte counts and SHA-256 hashes. |
| `README.md` | Pack guide | - | This file. |

## How to reproduce the conclusion

1. Open the test input `sample-inputs/C-2026-014_BlueHarbor_MSA_excerpt.md` and read Sections 3.1, 3.2, 5.2, 5.3 and 5.4 (pages 2 and 4).
2. In `04_ai_output_C-2026-014.json`, confirm the renewal terms were extracted correctly but `fields.material_right.value` is `false`.
3. In `06_review_C-2026-014.md`, follow the override calculation: option SSP $20,160, allocation $19,882, monthly $39,448, FY2026 reduction $3,314.
4. In `05_calc_C-2026-014.xlsx`, check the Allocation sheet against the annotation. Both rely on the same inputs and agree.
5. In `07_sl2_C-2026-014.md`, check the second reviewer's sensitivity analysis and concurrence.
6. Run `shasum -a 256 <file>` for each file and compare with `manifest.tsv`. A mismatch means the pack was altered after sealing.

## Pack rules applied

- The pack is sealed at close. Corrections are added as new versions with a reason code, never by overwriting a file.
- Every file carries a hash in the manifest. The manifest is stored separately from the pack in production.
- Retention is seven years from the end of FY2026, with legal hold overriding the schedule.
- The model output is the output the reviewer saw, tied to model, prompt, schema and document versions. It is not regenerated during an audit.
