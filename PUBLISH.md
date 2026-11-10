# Publish runbook — AI-Assisted ASC 606 Contract Review: sample workpaper

Prepared 2026-11-10 10:36 WIB for the staged copy at `agents/portfolio/staging/asc606-ai-workpaper/` (56 files, 3.3 MB).

**The agent that wrote this file does not publish, push, post or create repositories.** Every command below is for the owner to run, in order. Nothing here contacts a network until the final step, and that step is yours to run or skip.

## 0. Pre-flight (do not skip)

```bash
cd agents/portfolio/staging/asc606-ai-workpaper
# read the three generated files first:
#   README.md      what the artifact claims
#   REDACTIONS.md  every change and every excluded file
#   PUBLISH.md     this file

# re-run the strict privacy gate on what is about to be published:
python3 ../../../.agents/skills/portfolio-agent/scripts/privacy.py . --strict
# expected: RESULT: CLEAN (strict) ... Exit 0

# no secrets or key material in the tree:
grep -rIlE 'api[_-]?key|secret|BEGIN [A-Z ]*PRIVATE KEY|\.env' . || echo 'none found'

# size sanity check:
du -sh .
```

Three judgment calls the agent cannot make for you:

1. **Venue prior-publication policy.** If this workpaper is going to a blind-review venue, confirm that publishing a public edition does not break the venue's prior-distribution rule first. This is the one item that can cost a submission.
2. **Author line.** Open `README.md` and replace the `Author: TODO` line with your name and, if you want it public, a contact line you are happy to have indexed.
3. **Licence.** Without one, nobody may reuse the artifact. Choose below.

## 1. Final read

Read `README.md` top to bottom. If any claim is not backed by a file in the tree, delete the claim rather than softening it. Do not add a capability the artifact does not demonstrate.

## 2. Add a licence

For this artifact the sensible choices are **CC-BY-4.0** (docs-first: others may reuse the text with attribution) or **MIT** (permissive, the usual choice for a repo that is mostly a document plus build scripts). Do not mix them without a reason.

```bash
# CC-BY-4.0: paste the official text from
# https://creativecommons.org/licenses/by/4.0/legalcode.txt
# (or MIT, below), then:
python3 - <<'PY'
from pathlib import Path
Path('LICENSE').write_text('''CC-BY-4.0 or MIT text here''', encoding='utf-8')
PY
```

MIT template, if you pick MIT:

```text
MIT License

Copyright (c) 2026 <your name>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 3. Local commit

```bash
cd agents/portfolio/staging/asc606-ai-workpaper
git init -b main
git add -A
git commit -m "Add asc606-ai-workpaper"
git log --oneline
```

If `git` complains about identity, set it once: `git config user.name "Your Name"` and `git config user.email "you@example.com"`.

## 4. Create the repository and push (the only outbound step)

The agent never creates a repository, adds a remote or pushes. If you want this public, run these yourself:

```bash
gh repo create <your-github-user>/asc606-ai-workpaper --public --source . --remote origin --push \
  --description "Fictional ASC 606 generative-AI contract-review workpaper: risk register, controls, test cases, 25-contract sample and evidence pack."

gh repo edit --add-topic asc606 --add-topic revenue-recognition --add-topic ai-governance --add-topic audit --add-topic nist-ai-600-1
```

Do not force-push, do not rewrite history after people have linked it, and do not push anything from the private source directory. The private copy stays where it is.

## 5. Post-publish steps

1. Add one line to your profile README: `- [asc606-ai-workpaper](https://github.com/<your-github-user>/asc606-ai-workpaper) — Fictional ASC 606 generative-AI contract-review workpaper: risk register, controls, test cases, 25-contract sample and evidence pack.`
2. Share the URL once, where the intended audience actually is. Distribution, not another edit, is the remaining gap.
3. Draft post (edit before posting; the agent does not post):

```text
I wrote a fictional ASC 606 workpaper for one of the least-discussed problems in applied AI: what the control evidence looks like when a model sits between a contract and a revenue conclusion.

The setting is a made-up SaaS company running 240 contracts through a made-up extraction tool. A named reviewer reconciles every judgment field to the cited clause; a second reviewer covers the risky items. I tested 25 contracts.

Field-level extraction accuracy was 94.4%, but that is the easy number. Five of 25 conclusions changed under review, an independent recalculation corrected two more, and the corrections totalled $757,347, or 91.8% of performance materiality. Zero errors reached the ledger. Three controls failed or had design gaps; the remediation plan is in the paper.

Everything is invented, including the company, the tool and the people. The method is not.
```

## 6. Rollback

```bash
# before the repo exists: just delete the staging copy
rm -rf agents/portfolio/staging/asc606-ai-workpaper
# after publishing: delete the repository yourself (irreversible)
# gh repo delete <your-github-user>/asc606-ai-workpaper --yes
```

## Gate output at packaging time

```text
source gate (scripts/privacy.py, strict, rules v1): CLEAN — 0 hard, 0 review
staged-copy gate: recorded in REDACTIONS.md; re-run step 0 yourself before any push
```

## Files in this staged copy

- `AI-ASC606-Test-Workbook.xlsx`
- `PUBLISH.md`
- `README.md`
- `REDACTIONS.md`
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

`PUBLISH.md` and `REDACTIONS.md` are build records. Leave them in the repository or delete them before the commit; they contain no private data either way.
