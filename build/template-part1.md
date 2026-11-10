<!-- COVER -->
# Revenue Workpaper REV-AI-2026-01

## AI-Assisted Contract Review Under ASC 606

**Meridian Harbor Software, Inc. (fictional)**

> Fictional sample prepared for training and portfolio use. Meridian Harbor, ContractLens, Northstar Cognition, all customers, people, amounts, results and findings are invented. This is not an audit opinion or legal advice. NIST AI 600-1 is cited as a voluntary framework, not as an endorsement.

## Document control

{{DOC_CONTROL}}

### Index

| Tab | Content | Section |
|---|---|---|
| 1 | Purpose, scope, conclusion, tickmarks and sources | 1 |
| 2 | Process, system inventory, roles and limits | 2 |
| 3 | Accounting criteria, control framework, NIST scoping | 3 |
| 4 | Risk assessment and failure modes | 4 |
| 5 | Control design and key control notes | 5 |
| 6 | Test approach, sample and limitations | 6 |
| 7 | Test cases, corrections and results | 7 |
| 8 | Findings, observations and remediation | 8 |
| 9 | Evidence requirements and auditor questions | 9 |
| 10 | Conclusion, sign-off, review notes and open items | 10 |
| A-F | Contract register, NIST mapping, worked example, evidence pack, glossary, references | A-F |

## 1. Purpose, scope and conclusion

### 1.1 Purpose

Document the design and operating effectiveness of the contract review controls for the FY2026 Q4 close. The controls cover the AI extraction tool (ContractLens), the deterministic calculator, reviewer sign-off and the posting barrier. The workpaper also records the evidence pack retained for each contract and the results of the 25-contract test sample.

### 1.2 Scope

| In scope | Out of scope |
|---|---|
| Customer contracts and amendments executed 2026-01-01 through 2026-09-30 | Contracts executed before 2026-01-01 |
| 240-contract population; 25-contract sample (Appendix A) | Negotiation history and side letters not filed in the repository |
| ASC 606 conclusions: performance obligations, transaction price, allocation, recognition, material rights, principal versus agent, modifications | Billing accuracy, credit memos, commission accounting (ASC 340-40), income tax |
| 14 controls (CL-01 to CL-14), including vendor, access and change controls | The vendor's model training and evaluation, relied on through SOC reports only |
| Evidence retention and the per-contract evidence pack | System implementation, data migration and historical restatement |

Contracts executed before 2026-02-03 were processed while the FY2026 SSP table was still loading. They are in scope for the sample and flagged in §7.2 and §10.2.

### 1.3 Conclusion

**Twelve of 14 controls operated effectively. CL-02 (change management) and CL-09 (reviewer sign-off) did not operate as designed. CL-08 has a design gap; the manual recalculation compensates. Four findings and three observations are recorded in §8.**

Twenty of 25 contracts (80%) were accepted without change. Field accuracy before review was 94.4% (236 of 250 fields). Seven corrections were made before posting, totalling $757,347. That is 2.7% of sample contract value and 91.8% of performance materiality. No error reached the general ledger.

Q4 reliance is conditional on three items:

1. CL-09 annotation enforcement ships, or 100% second-level review applies until it does.
2. The 11 contracts executed before 2026-02-03 receive a 100% SSP table check.
3. No prompt, model or schema change deploys without regression evidence and Controller approval.

An auditor would test the same controls independently and would likely extend the CL-09 sample to 60 items.

### 1.4 Tickmarks

| Mark | Meaning |
|---|---|
| ✓ | Agreed to the source document or system record |
| T | Traced to a system-generated report or extract |
| R | Re-performed the calculation |
| Δ | Difference noted and cleared |
| N/A | Not applicable to this contract or test |

### 1.5 Source records

| Source | Extract or report | Date | Used for |
|---|---|---|---|
| DocuSign CLM | Executed contract files, exhibits and amendments | Extracted 10/06/2026 | Contract register, intake test |
| ContractLens | Model output JSON with version identifiers | Run dates 01/2026 to 09/2026 | Extraction, citation and flag tests |
| Revenue calculator | Allocation workbook with SSP table version | Re-performed 10/06 to 10/16/2026 | Calculation tests |
| NetSuite ARM | Approved schedules and journal entries | 10/15/2026 | Posting barrier, approval test |
| Internal Audit | Monthly QA reports, January to September 2026 | 10/02/2026 | Monitoring control test |
| Vendor package | SOC 1 Type II, SOC 2 Type II, bridge letter, DPA | Received 09/30/2026 | Vendor control test |

### 1.6 Summary metrics

{{KEY_NUMBERS}}

<!-- pagebreak -->

## 2. Process and system description

### 2.1 Workflow

1. Legal executes the agreement. Contract Operations files the executed PDF and all exhibits, completes the intake checklist and returns incomplete packages (CL-04).
2. The redaction service masks personal data and writes a redaction log with entity counts and timestamps (CL-05).
3. ContractLens receives the masked document and the active prompt template (v3.2).
4. The model returns structured JSON: ten fields, each with a clause citation (section, page and character span), a confidence score and flags. It also proposes a conclusion for each ASC 606 decision point.
5. Schema validation rejects malformed output. Missing-information and suspicious-content flags route the file to review (CL-07).
6. The deterministic calculator computes relative SSP allocation and the revenue schedule from the model's proposed inputs and the SSP table effective on the contract date (CL-08).
7. The senior analyst re-performs the calculator output, checks the table version and records differences (CL-08).
8. The Revenue Controller or delegate opens each cited clause, agrees the term, records an annotation and signs off under SSO identity (CL-09).
9. Second-level review fires on the CL-10 triggers.
10. The Controller approves the schedule. The entry posts through the standard workflow; the model has no write access to the ERP (CL-11).
11. Internal Audit re-performs ten closed contracts each month and reports accuracy and exception trends (CL-12). Exceptions go to the log (CL-13).

### 2.2 System inventory

{{SYSTEMS}}

The vendor hosts the model in a single US region. The contract with the vendor prohibits training on customer content, restricts subprocessors to the published list reviewed under CL-03, and sets deletion at 30 days after termination of the vendor agreement.

### 2.3 Roles and authority

{{ROLES}}

The model has no authority. Its output is a proposal with citations. A named reviewer signs each conclusion, a second reviewer signs the high-risk ones, and the Controller approves each schedule. Section 7 tests whether that happened.

### 2.4 Limits on the model

- No write access to the general ledger, billing or approvals.
- No access to the SSP table; the calculator holds it.
- Masked input only. No external calls or internet access.
- No memory between contracts. Each run starts from the filed document and the prompt template.

<!-- pagebreak -->

## 3. Criteria

### 3.1 Accounting criteria

The tests use the decision points below. A clause citation or codification reference is the criteria; a confidence score is not.

{{DECISION_POINTS}}

Two judgments sit outside the model's authority. Material rights require expected renewal behavior and future pricing. The variable consideration constraint requires an assessment of the probability of a significant revenue reversal. The model may propose an answer; the reviewer concludes it.

### 3.2 Control framework

The control matrix maps to COSO 2013. The company is private and not yet an SEC issuer. We apply PCAOB AS 2201, AS 1105, AS 1215 and AS 2401 as readiness criteria for the planned IPO: internal control assessment, evidence, documentation and the fraud risk presumption in revenue.

| COSO principle | Where it appears |
|---|---|
| P1 Integrity and ethical values | CL-01 use-case approval; reviewer competency standards |
| P3 Structures, authority and responsibility | CL-01, CL-03; roles in §2.3 |
| P7 Identifies and analyzes risk | Section 4 risk register; NIST mapping in Appendix B |
| P10 Selects and develops control activities | CL-04, CL-06, CL-08, CL-09, CL-10, CL-11 |
| P11 Technology general controls | CL-02 change, CL-06 access, CL-05 data handling |
| P12 Policies and procedures | Revenue AI policy REV-AI-07; SSP policy REV-SSP-04 |
| P13 Relevant information | CL-09 citations; EV-03 output record |
| P15 External communication | Audit Committee and auditor reporting |
| P16 Performance evaluation | CL-12 monthly QA; CL-13 trend review |
| P17 Evaluates and remediates deficiencies | Section 8 findings and remediation |

### 3.3 Generative AI criteria

NIST published AI RMF 1.0 in January 2023 and the Generative AI Profile, NIST AI 600-1, in July 2024 (doi.org/10.6028/NIST.AI.600-1). The profile is free and voluntary. It names 12 generative AI risks and organizes suggested actions under GOVERN, MAP, MEASURE and MANAGE.

We used AI 600-1 to identify risks and to check that each control addresses one. We did not treat the profile as a certification, and we did not adopt suggested actions that do not fit a contract review process. Eight of the 12 risks apply; Appendix B records the four exclusions and the reasons. NIST states that AI RMF 1.0 is being revised; AI 600-1 remains the current generative AI profile as of 10/28/2026.

### 3.4 Evidence standard

Evidence must be relevant, reliable, complete and timely. For system output, reliability depends on version identification and the controls over the system. A model output is accepted as evidence only when it ties to a document hash and to the model, prompt and schema versions. A reviewer note without a clause reference does not evidence review.
