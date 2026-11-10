# Redactions and staging changes — asc606-ai-workpaper

Prepared 2026-11-10 10:36 WIB.

- Source directory (read-only): `asc606-ai-workpaper`
- Staged at: `agents/portfolio/staging/asc606-ai-workpaper`
- Privacy rules: v1 from `scripts/privacy.py`

## Privacy gate on the source

Strict scan result: **CLEAN** — 0 hard finding(s), 0 review finding(s), 0 risky unscanned file(s).

## Content redactions

None required.

No file content was altered to remove personal data. If the gate above had produced a hard finding, the run would have refused to stage unless `--force-redacted` was passed, and this section would list every manual edit with the reason.

## Staging changes (not redactions)

| Change | Path | Why |
|---|---|---|
| Replaced | `README.md` | The source README is written as a delivery note for the private workspace. The staged README is written for a public reader in Problem / Method / Result / Limitations / Sources form. Every claim is traceable to a source file; nothing was added that the artifact does not demonstrate. The source copy is untouched at `asc606-ai-workpaper`.
| Excluded | `build/__pycache__/wpdata.cpython-312.pyc` | build cache directory (`__pycache__`) — not publishable content |

## Files copied unchanged

53 file(s) copied byte-for-byte (SHA-256 verified at copy time).

- `AI-ASC606-Test-Workbook.xlsx`
- `build/build_evidence_calc.py`
- `build/cover.png`
- `build/crop-findings.png`
- `build/crop-remediation.png`
- `build/evidence-calc-png/05_calc_C-2026-014-01.png`
- `build/evidence_calc_data.json`
- `build/evidence_calc_ops.json`
- `build/genoffice_build.py`
- `build/make_manifest.py`
- `build/proof_render.py`
- `build/render.py`
- `build/sheet-proofs/contract-register/data.json`
- `build/sheet-proofs/contract-register/ops.json`
- `build/sheet-proofs/contract-register/png/proof-01.png`
- `build/sheet-proofs/contract-register/proof.xlsx`
- `build/sheet-proofs/control-matrix/data.json`
- `build/sheet-proofs/control-matrix/ops.json`
- `build/sheet-proofs/control-matrix/png/proof-01.png`
- `build/sheet-proofs/control-matrix/proof.xlsx`
- `build/sheet-proofs/cover/data.json`
- `build/sheet-proofs/cover/ops.json`
- `build/sheet-proofs/cover/png/proof-01.png`
- `build/sheet-proofs/cover/proof.xlsx`
- `build/sheet-proofs/metrics/data.json`
- `build/sheet-proofs/metrics/ops.json`
- `build/sheet-proofs/metrics/png/proof-01.png`
- `build/sheet-proofs/metrics/proof.xlsx`
- `build/template-part1.md`
- `build/template-part2.md`
- `build/template-part3.md`
- `build/workbook-check.pdf`
- `build/workbook_data.json`
- `build/workbook_ops.json`
- `build/workpaper.html`
- `build/wpdata.py`
- `build/xlsx-pages/AI-ASC606-Test-Workbook-01.png`
- `build/xlsx-pages/AI-ASC606-Test-Workbook-grid.png`
- `evidence/C-2026-014/04_ai_output_C-2026-014.json`
- `evidence/C-2026-014/05_calc_C-2026-014.xlsx`
- `evidence/C-2026-014/06_review_C-2026-014.md`
- `evidence/C-2026-014/07_sl2_C-2026-014.md`
- `evidence/C-2026-014/README.md`
- `evidence/C-2026-014/manifest.tsv`
- `sample-inputs/C-2026-007_GranitePeak_SOW_excerpt.md`
- `sample-inputs/C-2026-008_Harborview_rebate_exhibit.md`
- `sample-inputs/C-2026-011_Kestrel_order_form_excerpt.md`
- `sample-inputs/C-2026-013_Tidewater_Exhibit_D.md`
- `sample-inputs/C-2026-014_BlueHarbor_MSA_excerpt.md`
- `sample-inputs/C-2026-016_Pinewood_master_agreement_excerpt.md`
- `sample-inputs/README.md`
- `workpaper/AI-ASC606-Contract-Review-Workpaper.md`
- `workpaper/AI-ASC606-Contract-Review-Workpaper.pdf`

## Not text-scanned

The scanner reads text files and xlsx cell text. These copied files are binary and need a human eyeball before publishing:

- `build/cover.png`
- `build/crop-findings.png`
- `build/crop-remediation.png`
- `build/evidence-calc-png/05_calc_C-2026-014-01.png`
- `build/sheet-proofs/contract-register/png/proof-01.png`
- `build/sheet-proofs/control-matrix/png/proof-01.png`
- `build/sheet-proofs/cover/png/proof-01.png`
- `build/sheet-proofs/metrics/png/proof-01.png`
- `build/workbook-check.pdf`
- `build/xlsx-pages/AI-ASC606-Test-Workbook-01.png`
- `build/xlsx-pages/AI-ASC606-Test-Workbook-grid.png`
- `workpaper/AI-ASC606-Contract-Review-Workpaper.pdf`

For this artifact the PDF is a print render of the Markdown workpaper (the build chain in `build/render.py` writes Markdown to HTML to PDF) and the PNGs are rendered sheet proofs. The text they render is scanned as Markdown, not as PDF. Confirm that by eye once; do not assume it.

## Staged copy re-scan

The staged copy was scanned again with the strict gate after the README and runbook were written:

```text
privacy scan — rules v1 (56 hard, 8 review) — agents/portfolio/staging/asc606-ai-workpaper
scanned: 43 files, 7041 text units (37 text file(s), 6 workbook(s)); not scannable: 12
not scannable by type: .pdf=2, .png=10 — manual review before publishing

findings: none

by category: medical=0, credit=0, address=0, contact=0, immigration=0, third_party=0, confidential=0, identity=0, travel_window=0

RESULT: CLEAN (strict) — no blocking findings. Exit 0.
```

The staged copy passes. Packaging did not modify the source directory; every diff between source and staging is listed in this file.
