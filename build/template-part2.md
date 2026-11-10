<!-- pagebreak -->

## 4. Risk assessment

### 4.1 Risk factors

Revenue recognition carries a presumed fraud risk under AS 2401. Three factors raise the inherent risk of this process:

- **Contract complexity.** 62 of the 240 contracts in the population carry a non-standard feature: renewal discounts, rebates, reseller arrangements, public-sector clauses, modifications or scanned documents.
- **Plausible wrong answers.** The model returns fluent conclusions with citations whether or not the conclusion is right. A reviewer who trusts the citation reviews faster and misses more.
- **Review capacity.** Manual review runs at 4.2 hours per contract; assisted review at 1.6. The time saving is real, and it removes the natural friction that used to catch errors.

Inherent risk: **High**. Controls must make the reviewer's work visible and independent of the model's presentation.

### 4.2 Risk register

{{RISK_REGISTER}}

Sixteen risks are rated after controls: six low, ten medium, none high. The medium ratings sit on judgment fields, where a plausible model answer can be wrong and where review evidence matters most.

### 4.3 Failure modes seen in the sample

| Failure mode | What it looks like | Seen in the sample | Control |
|---|---|---|---|
| Omitted term | A real clause is not extracted or not priced | Missed material right (C-2026-014); missed rebate exhibit (C-2026-008) | CL-09, CL-10 |
| Wrong classification | A defensible label produces the wrong accounting | Principal instead of agent (C-2026-016); implementation treated as distinct (C-2026-007) | CL-09, CL-10 |
| Unconstrained estimate | A variable amount is treated as fixed | Overage treated as fixed (C-2026-019) | CL-09, CL-10 |
| Instruction from document text | Contract text tries to steer the model | Injection resisted after v3.2 hardening (C-2026-013) | CL-07, CL-09 |
| Silent configuration change | Output changes without a test record | Prompt v3.2 deployed without regression evidence (F-01) | CL-02, CL-14 |
| Reference-data drift | Correct model, stale parameters | SSP table v2025 used for January 2026 contracts (F-02) | CL-08 |

### 4.4 NIST AI 600-1 scoping

Eight of the 12 risks apply: confabulation, data privacy, harmful bias and homogenization, human-AI configuration, information integrity, information security, intellectual property, and value chain and component integration. Four do not apply: CBRN information, dangerous or hateful content, obscene content, and environmental impacts. Environmental impact is assessed rather than dismissed. Annual volume is roughly 240 contracts, the vendor does not meter energy per request, and energy use is not a control objective here. Appendix B records the reason for each decision.

<!-- pagebreak -->

## 5. Control design

### 5.1 Control chain

Five barriers sit between a wrong model output and the general ledger:

1. **Input integrity.** Reviewer and model see the same complete executed agreement (CL-04). Personal data is removed before inference (CL-05).
2. **Output structure.** Every field carries a clause citation. Missing information and suspicious text are flagged. The model must abstain rather than invent (CL-07).
3. **Arithmetic outside the model.** A deterministic calculator recomputes allocation and the schedule from effective-dated tables, and an analyst re-performs it (CL-08).
4. **Human conclusion.** A named reviewer reconciles each judgment field to the cited clause and signs off (CL-09). A second reviewer covers high-value and non-standard contracts (CL-10).
5. **Posting barrier and monitoring.** The Controller approves the schedule before posting (CL-11). Internal Audit re-performs a monthly sample (CL-12), and every error goes to the exception log (CL-13).

### 5.2 Control matrix

{{CONTROL_MATRIX}}

### 5.3 Design notes on the key controls

**CL-07 (citation and abstention).** The schema requires a section, page and character span for every field. A conclusion without a locatable clause is a schema failure, not a review question. The schema also gives the model a legitimate way to say it lacks information. TC-11 tests abstention when Exhibit C is missing; TC-10 tests an instruction embedded in an exhibit.

**CL-08 (arithmetic outside the model).** The calculator applies the approved SSP table. This isolates calculation error from model error. It does not isolate parameter error. F-02 is a table-version failure, not an arithmetic failure, and the manual re-performance caught it.

**CL-09 (reviewer reconciliation).** Every judgment error in the sample was caught at this step. A sign-off without an annotation says a person clicked a button; an annotation tied to a clause says a person read the clause and agreed. F-03 is the gap between those two.

**CL-10 (second-level review).** The triggers direct second-reviewer time to the contracts most likely to carry a wrong conclusion. All five corrected conclusions were above the $250,000 trigger, so all five had second review. The first reviewer identified four. The second reviewer identified the constraint issue on C-2026-019.

**CL-11 (posting barrier).** The model cannot write to the ERP. The only path to the ledger is an approved schedule with preparer and approver identities. This is what keeps the failures in this file out of the financial statements.

### 5.4 Segregation and IT general controls

| Separation | How it is enforced |
|---|---|
| Submit versus approve | The submit role cannot hold revenue approval; tested in CL-06 |
| Review versus model configuration | Reviewers cannot change prompt, schema or model settings; two administrators required for configuration |
| QA versus Revenue | Internal Audit performs CL-12 and reports to the Audit Committee, outside the Revenue line |
| Vendor versus Meridian Harbor | The vendor cannot approve revenue, access the ERP or change the SSP table |

The chain depends on three IT general controls: change management (CL-02), access management (CL-06) and vendor management (CL-03). F-01 is a change management failure. An application control with a broken change process is a temporary control.

### 5.5 Design assessment

{{DESIGN_ASSESSMENT}}

Design is effective for 12 controls. CL-08 has a design gap: the calculator selects the SSP table marked current, not the table effective on the contract date, so a late table load misallocates silently. CL-09 has a partial design gap: the workflow allows sign-off with an empty annotation field, which is how F-03 happened. CL-02 fails in operation, not design.

<!-- pagebreak -->

## 6. Test approach and sample

### 6.1 Population and sample

The population is 240 executed contracts and amendments: 157 new contracts and 83 amendments. The listing reconciled to DocuSign CLM at 09/30/2026 after removing three duplicates and two unexecuted drafts. Sixty-two contracts carry at least one non-standard feature. Eleven were executed before 2026-02-03, when the FY2026 SSP table loaded into the calculator.

| Stratum | Selection basis | Contracts | Purpose |
|---|---|---|---|
| Random | 15 items drawn from the 240 using seed 2026-Q4-07 | 15 | Coverage of contracts not selected by risk |
| Risk-based | All six contracts at or above $1.5 million TCV, plus non-standard features, new SKUs and scanned documents | 10 | Test the judgment fields and routing rules |
| Total | | 25 | $28,536,000 contract value |

Four contracts in the listing had been amended after execution. The latest filed version was used for those four. No other substitutions were made.

The random stratum supports a statement about the contract population. The accuracy and agreement metrics in §7.4 are computed over all 25 contracts, so they describe the test sample, not the 240-contract population.

### 6.2 Tests performed

| Test type | What was done | Coverage |
|---|---|---|
| Design walkthrough | Traced two contracts end to end; inspected prompt, schema, calculator configuration and approval workflow | 2 contracts; 1 walkthrough |
| Operating effectiveness | Re-performed 14 test cases and 14 control tests; recalculated every allocation; reconciled every cited clause | 25 contracts; 250 field checks |
| Change management | Inspected three production changes to prompt, model and schema | 3 of 3 changes |
| Access management | Inspected three quarterly access reviews; tested two leaver removals | 3 reviews |
| Vendor management | Inspected SOC 1 Type II, SOC 2 Type II, bridge letter, DPA and subprocessor list | 1 annual cycle |
| Monitoring | Inspected nine monthly QA reports; re-performed two months of QA | 90 contracts; 900 field checks |

Tested by AO, 10/05 to 10/16/2026. Reviewed by RT, 10/24/2026.

### 6.3 Sample size

Twenty-five items is a readiness sample. A formal conclusion at a 5% tolerable deviation rate and 95% confidence with zero expected deviations requires 60 items. Twenty-five items with zero deviations gives an upper deviation limit of 11.3% (1 minus 0.05^(1/25)). The sample is sufficient to test design and to find the exceptions in §7. It does not support a projectable misstatement estimate, and this workpaper does not make one. The FY2026 audit sample will use 60 items.

### 6.4 Model behavior and reproducibility

ContractLens runs at temperature 0 and caches output by document hash plus prompt, model and schema version. Three repeated runs on C-2026-014 produced byte-identical output. That does not survive a model upgrade. The evidence of record is the captured output with its version identifiers, not an assumption that the same input always produces the same answer. If the vendor retires a model version, the evidence pack still holds what the reviewer saw; CL-14 requires a transition test before the replacement goes live.

### 6.5 Limitations

This workpaper is management-prepared. The sample is partly judgmental. We did not test the vendor's internal model evaluation; we relied on the SOC reports and our own output testing. The tests cover contracts executed through 09/30/2026. Accounting conclusions are management's, and an auditor may reach a different view. A clean test result applies to the tested population, not to the next contract.
