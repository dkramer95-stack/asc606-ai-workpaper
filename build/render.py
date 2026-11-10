"""Render the ASC 606 AI workpaper (Markdown) and a print-ready HTML file.

Usage:  python3 render.py
The tables are generated from wpdata.py so the Markdown workpaper and the
Excel workbook cannot drift apart.
"""
import html
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from wpdata import *  # noqa: F401,F403


def money(x):
    return f"${x:,.0f}"


def pct(x, digits=1):
    return f"{x * 100:.{digits}f}%"


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        assert len(row) == len(headers), f"row length {len(row)} != {len(headers)}: {row}"
        out.append("| " + " | ".join(cell(c) for c in row) + " |")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Table builders
# ---------------------------------------------------------------------------
def t_doc_control():
    rows = [
        ("Workpaper reference", f"{ENTITY['wp_ref']}"),
        ("Entity", f"{ENTITY['name']} (fictional)"),
        ("Period covered", f"{ENTITY['period']} (FY2026 Q1 to Q3)"),
        ("Population and sample", f"{ENTITY['population']} contracts; 25 tested"),
        ("Tool and versions", f"{ENTITY['tool']}; model {ENTITY['model']}; {ENTITY['prompt']}; {ENTITY['schema']}"),
        ("Overall materiality", money(ENTITY["materiality"])),
        ("Performance materiality", money(ENTITY["performance_materiality"])),
        ("Prepared by", f"{ENTITY['preparer']}, {ENTITY['prepared']}"),
        ("Reviewed by", f"{ENTITY['reviewer']}, {ENTITY['reviewed']}"),
        ("Approved by", f"{ENTITY['approver']}, {ENTITY['approved']}"),
        ("Internal audit observer", f"{ENTITY['internal_audit']}"),
        ("Distribution", "Revenue Controller, CFO, Audit Committee, external auditors"),
        ("Status", "Final (v1.2)"),
        ("Version", "1.2"),
    ]
    return table(["Field", "Detail"], rows)


def t_key_numbers():
    s = SUMMARY
    rows = [
        ("Contracts tested", f"25 of 240 ({25 / 240 * 100:.1f}%)", "6.1"),
        ("Sample contract value", money(s["sample_tcv"]), "6.1"),
        ("Field-level extraction accuracy", f"{pct(s['field_accuracy'])} ({s['field_checks'] - s['field_errors']} of {s['field_checks']} checks)", "7.4"),
        ("Contracts accepted without change", f"{s['contracts_reviewed'] - s['contracts_corrected']} of {s['contracts_reviewed']} ({pct(s['agreement_rate'], 0)})", "7.4"),
        ("Gross effect of corrections", f"{money(s['corrections_total'])} ({pct(s['corrections_pct_tcv'])} of sample TCV; {pct(s['corrections_pct_pm'])} of performance materiality)", "7.2"),
        ("Errors that reached the general ledger", "0", "10.2"),
        ("Average review time", f"{s['review_hours_ai']:.1f} hours (manual baseline {s['review_hours_manual']:.1f} hours; {pct(s['time_reduction'], 0)} reduction)", "7.4"),
        ("Controls rated effective", "12 of 14", "10.1"),
        ("Findings and observations", "4 findings; 3 observations", "8"),
        ("Test cases passed and failed-but-caught", "8 passed; 6 failed at the model level and were caught", "7.4"),
    ]
    return table(["Metric", "Result", "Section"], rows)


def t_systems():
    rows = [
        ("ContractLens application", "Extracts contract terms, proposes ASC 606 conclusions, returns structured JSON", "v2.4.1, production 2026-03-09", "Vendor; Meridian Harbor administrator", "CL-01, CL-02, CL-07"),
        ("Language model", "Generates extraction and draft conclusions", f"{ENTITY['model']}; temperature 0; output capped at 8,000 tokens", "Vendor-hosted, US region", "CL-02, CL-03"),
        ("Prompt template", "Role, output schema, citation format, abstention and injection rules", f"{ENTITY['prompt']}, deployed 2026-08-14", "Revenue Systems", "CL-02, CL-07"),
        ("Extraction schema", "Ten required fields, citation spans, confidence, flags", f"{ENTITY['schema']}", "Revenue Systems", "CL-07"),
        ("Deterministic calculator", "Relative SSP allocation, revenue schedule, effective-dated tables", "Build 2026.4, in-house", "Revenue", "CL-08"),
        ("Redaction service", "Masks personal data before inference; writes redaction log", "v1.9, in-house", "Revenue Systems", "CL-05"),
        ("Contract repository", "Executed agreements, exhibits and amendments; version history", "DocuSign CLM", "Legal; Contract Operations", "CL-04, CL-06"),
        ("Revenue subledger", "Schedules, approvals and journal entry posting", "NetSuite ARM", "Revenue; Accounting", "CL-11"),
    ]
    return table(["Component", "Function", "Version or identifier", "Operated by", "Controls"], rows)


def t_roles():
    rows = [
        ("Contract Operations", "Files executed agreements and exhibits; completes the intake checklist", "Change contract terms; approve revenue"),
        ("Senior Revenue Analyst", "Re-performs calculations; prepares schedules; records differences", "Approve own schedules; change model settings"),
        ("Revenue Controller", "Reviews conclusions; signs off; approves schedules", "Change prompt, model or SSP configuration"),
        ("Revenue Systems Manager", "Owns model, prompt, schema and vendor configuration; controls versions", "Approve revenue or sign conclusions"),
        ("Internal Audit", "Performs monthly QA, independent re-performance and trend reporting", "Post entries; change the workflow"),
        ("CFO", "Approves the use case, data classes, authority limits and risk appetite", "Delegates individual contract approvals to the Controller"),
    ]
    return table(["Role", "Accountable for", "Cannot do"], rows)


def t_decision_points():
    rows = [
        ("Contract existence and collectibility", "ASC 606-10-25-1 through 25-8", "Intake gate; term and payment terms extracted (TC-01)"),
        ("Performance obligations and distinctness", "ASC 606-10-25-21 through 25-22", "TC-02, TC-09"),
        ("Transaction price components", "ASC 606-10-32-1 through 32-4", "TC-03, TC-07"),
        ("Variable consideration and constraint", "ASC 606-10-32-5 through 32-12", "TC-03, TC-07"),
        ("Allocation and standalone selling price", "ASC 606-10-32-28 through 32-38", "TC-02, TC-13"),
        ("Principal versus agent", "ASC 606-10-55-36 through 55-40", "TC-05"),
        ("Material rights and renewal options", "ASC 606-10-55-41 through 55-45", "TC-04"),
        ("Contract modifications", "ASC 606-10-25-10 through 25-13", "TC-06"),
        ("Recognition pattern", "ASC 606-10-25-23 through 25-37", "TC-06, TC-09"),
    ]
    return table(["Decision point", "Codification", "Test evidence"], rows)


def t_risks():
    rows = [(r["id"], f"{r['risk']} (failure mode: {r['mode']})", r["asc"], r["nist"],
             r["inherent"], r["controls"], r["residual"]) for r in RISKS]
    return table(["ID", "Risk and failure mode", "ASC / evidence area", "NIST AI 600-1 risk", "Inherent", "Key controls", "Residual"], rows)


def t_controls():
    rows = [(c["id"], f"**{c['name']}.** {c['description']}", f"{c['type']}; {c['nature']}; {c['freq']}",
             c["owner"], c["evidence"], c["nist"], c["result"]) for c in CONTROLS]
    return table(["ID", "Control and how it operates", "Type; nature; frequency", "Owner", "Key evidence", "NIST function", "Test result"], rows)


DESIGN = {
    "CL-01": ("Effective", "Scope, data classes and authority limits approved before go-live", "Approval package inspected; no exception"),
    "CL-02": ("Effective design, failed in operation", "Change gate exists, but the ticket template lost its test-evidence field", "1 of 3 changes untested (F-01)"),
    "CL-03": ("Effective", "SOC reports, bridge letter, DPA and subprocessor review map to complementary controls", "Annual package complete; two CUECs mapped"),
    "CL-04": ("Effective", "Checklist covers execution, exhibits, amendments and document quality", "25 of 25 files processed; 1 incomplete package returned"),
    "CL-05": ("Effective after remediation", "Redaction happens before inference; logging configuration added after F-04", "F-04 closed 2026-10-02 with deletion certificate"),
    "CL-06": ("Effective", "Role design separates submit, review, approve and configure", "3 access reviews; 2 leaver removals tested"),
    "CL-07": ("Effective", "Schema enforces citation, confidence, abstention and suspicious-content flags", "25 of 25 outputs schema-valid; 2 abstentions"),
    "CL-08": ("Deficient", "No effective-date parameter; the table marked current at run time is used", "Manual re-performance compensates; 2 of 25 allocations corrected (F-02)"),
    "CL-09": ("Partially deficient", "Annotation field is optional, so sign-off is possible without review evidence", "2 of 25 files without annotation (F-03)"),
    "CL-10": ("Effective", "Triggers cover value, non-standard terms, low confidence, new SKUs and modifications", "20 of 20 triggered contracts had second-level review"),
    "CL-11": ("Effective", "Posting requires an approved schedule; the model has no ERP write access", "25 of 25 entries approved before posting"),
    "CL-12": ("Effective", "Independent monthly re-performance with explicit escalation thresholds", "90 contracts tested; 12 exceptions, all logged"),
    "CL-13": ("Effective", "Exception log with owner and due date; quarterly Audit Committee review", "18 exceptions; 17 closed, 1 open"),
    "CL-14": ("Effective", "EOL monitoring, fallback plan and contract exit terms", "1 EOL notice reviewed; transition plan approved"),
}


def t_design():
    rows = [(c["id"], c["name"], DESIGN[c["id"]][0], DESIGN[c["id"]][1], DESIGN[c["id"]][2]) for c in CONTROLS]
    return table(["Control", "Name", "Design conclusion", "Basis", "Effect on operating test"], rows)


def t_tests():
    rows = [(t["id"], t["contract"], t["objective"], t["expected"], t["actual"],
             t["result"] + (f" ({t['defect']})" if t["defect"] not in ("-", "") else ""), t["controls"])
            for t in TESTS]
    return table(["ID", "Contract", "Objective", "Expected behavior", "Actual result", "Conclusion", "Controls"], rows)


def t_corrections():
    by_id = {c["id"]: c for c in CONTRACTS}
    rows = []
    for c in CORRECTIONS:
        con = by_id[c["contract"]]
        rows.append((c["contract"], con["ai"], con["review"], money(c["effect"]), c["kind"], c["control"]))
    rows.append(("**Total**", "", "", f"**{money(SUMMARY['corrections_total'])}**", f"**{pct(SUMMARY['corrections_pct_pm'])} of performance materiality**", ""))
    return table(["Contract", "Model proposed", "Reviewer concluded", "Gross effect", "Error type", "Control"], rows)


def t_findings():
    short_effect = {
        "F-01": "No output change found; change control not demonstrated",
        "F-02": "$25,300 allocation variance; caught by re-performance",
        "F-03": "2 of 25 sign-offs lack review evidence; no financial error",
        "F-04": "Vendor retained raw text for 30 days; deleted, certificate obtained",
    }
    rows = [(f["id"], f["control"], f["severity"], f["condition"], short_effect[f["id"]],
             f"{f['owner']}; {f['due']}") for f in FINDINGS]
    return table(["ID", "Control", "Severity", "Condition", "Effect", "Owner and due date"], rows)


def t_observations():
    return table(["ID", "Contract", "Observation"], [(o["id"], o["contract"], o["text"]) for o in OBSERVATIONS])


def t_remediation():
    actions = {
        "F-01": "Restore the regression gate and ticket field; run retroactive tests for v3.1 and v3.2; require Controller approval for prompt changes",
        "F-02": "Add effective-date parameters and an automated table-version reconciliation; 100% manual check for contracts executed before 2026-02-03",
        "F-03": "Make annotation mandatory in the workflow; retrain reviewers; apply 100% second-level review for 60 days",
        "F-04": "Amend the DPA to require configuration attestation in the annual bridge letter; add logging configuration to CL-05",
    }
    closure = {
        "F-01": "Updated ticket template; two regression reports; approval record",
        "F-02": "Change ticket; regression results; reconciliation report",
        "F-03": "Workflow change ticket; training records; 60-day SL2 sample",
        "F-04": "Signed DPA amendment; vendor attestation; deletion certificate",
    }
    rows = [(f["id"], actions[f["id"]], f["owner"], f["due"], f["status"], closure[f["id"]]) for f in FINDINGS]
    return table(["Finding", "Action", "Owner", "Due", "Status", "Evidence of closure"], rows)


def t_evidence():
    rows = [(e["id"], e["artifact"], e["format"], e["owner"], e["retention"], e["integrity"],
             f"{e['proves']} ({e['controls']})") for e in EVIDENCE]
    return table(["ID", "Evidence artifact", "Format", "Owner", "Retention", "Integrity", "What it proves and controls"], rows)


def t_nist():
    rows = [(n["risk"], n["applicable"], n["treat"], n["link"]) for n in NIST_RISKS]
    return table(["NIST AI 600-1 risk", "Applicability", "Treatment in this workflow", "Related risks"], rows)


def t_field_accuracy():
    rows = [(field, str(checks), str(err), f"{1 - err / checks:.1%}") for field, checks, err in FIELD_ACCURACY]
    total_checks = sum(c for _, c, _ in FIELD_ACCURACY)
    total_errors = sum(e for _, _, e in FIELD_ACCURACY)
    rows.append(("**Total**", f"**{total_checks}**", f"**{total_errors}**", f"**{1 - total_errors / total_checks:.1%}**"))
    return table(["Field checked", "Contracts checked", "Errors", "Accuracy"], rows)


def t_result_summary():
    s = SUMMARY
    rows = [
        ("Test cases passed", "8 of 14", "Tests with no model-level error"),
        ("Test cases failed at the model level", "6 of 14", "All six detected before posting"),
        ("Field-level accuracy", pct(s["field_accuracy"]), "14 errors in 250 field checks, before review"),
        ("Contract-level agreement", pct(s["agreement_rate"], 0), "5 of 25 conclusions changed on review"),
        ("Post-review accuracy", "100%", "25 of 25 final conclusions agreed on re-performance"),
        ("Corrections", money(s["corrections_total"]), "7 corrections across 7 contracts"),
        ("Ledger errors", "0", "No uncaught error reached posting"),
        ("Detection by CL-09 and CL-10", "5 of 7 corrections", "Reviewers reconciling cited clauses"),
        ("Detection by CL-08", "2 of 7 corrections", "Independent recalculation and table check"),
        ("Review time", f"{s['review_hours_ai']:.1f} hours per contract", f"Manual baseline {s['review_hours_manual']:.1f} hours; {pct(s['time_reduction'], 0)} reduction"),
    ]
    return table(["Measure", "Result", "Basis"], rows)


def t_contracts():
    def tick(ref):
        return "Δ" if "C1" in ref else "✓"
    rows = [(c["id"], c["customer"], c["executed"], str(c["months"]), money(c["tcv"]),
             c["feature"], c["ai"], c["review"], c["ref"], tick(c["ref"])) for c in CONTRACTS]
    rows.append(("**Total**", f"**{len(CONTRACTS)} contracts**", "", "",
                 f"**{money(SUMMARY['sample_tcv'])}**", "", "", "", "", ""))
    return table(["ID", "Customer", "Executed", "Term (months)", "TCV", "Non-standard feature", "Model result", "Review result", "Ref", "T"], rows)


def t_control_ratings():
    groups = [
        ("Effective", "10", "CL-01, CL-03, CL-04, CL-06, CL-07, CL-10, CL-11, CL-12, CL-13, CL-14", "Reliance supported for the Q4 close"),
        ("Effective after remediation", "1", "CL-05", "Reliance supported from 2026-09-02"),
        ("Design deficiency, compensating control effective", "1", "CL-08", "Reliance supported only with 100% manual re-performance until the fix"),
        ("Ineffective", "2", "CL-02, CL-09", "Remediate or apply the interim mitigation before the Q4 close"),
    ]
    return table(["Rating", "Count", "Controls", "Consequence"], groups)


def t_signoff():
    rows = [
        ("Prepared by", f"{ENTITY['preparer']}", ENTITY["prepared"]),
        ("Reviewed by", f"{ENTITY['reviewer']}", ENTITY["reviewed"]),
        ("Approved by", f"{ENTITY['approver']}", ENTITY["approved"]),
        ("Internal Audit observer", f"{ENTITY['internal_audit']}", ENTITY["reviewed"]),
    ]
    return table(["Role", "Name and title", "Date"], rows)


def t_version_history():
    rows = [
        ("1.0", "2026-10-20", "Initial draft for the Q4 close readiness assessment"),
        ("1.1", "2026-10-24", "Reviewer comments; corrections tied to the contract register; findings re-rated"),
        ("1.2", "2026-10-27", "Final version; remediation tracker, evidence standard and sign-off added"),
    ]
    return table(["Version", "Date", "Description"], rows)


BUILDERS = {
    "DOC_CONTROL": t_doc_control,
    "KEY_NUMBERS": t_key_numbers,
    "SYSTEMS": t_systems,
    "ROLES": t_roles,
    "DECISION_POINTS": t_decision_points,
    "RISK_REGISTER": t_risks,
    "CONTROL_MATRIX": t_controls,
    "DESIGN_ASSESSMENT": t_design,
    "TEST_CASES": t_tests,
    "CORRECTIONS": t_corrections,
    "FINDINGS": t_findings,
    "OBSERVATIONS": t_observations,
    "REMEDIATION": t_remediation,
    "EVIDENCE": t_evidence,
    "NIST": t_nist,
    "FIELD_ACCURACY": t_field_accuracy,
    "RESULT_SUMMARY": t_result_summary,
    "CONTRACTS": t_contracts,
    "CONTROL_RATINGS": t_control_ratings,
    "SIGNOFF": t_signoff,
    "VERSION_HISTORY": t_version_history,
}


# ---------------------------------------------------------------------------
# Markdown to HTML
# ---------------------------------------------------------------------------
def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def md_to_html(md):
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)
    para = []

    def flush_para():
        nonlocal para
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if stripped == "":
            flush_para()
            i += 1
            continue

        if stripped == "<!-- pagebreak -->":
            flush_para()
            out.append('<div class="pb"></div>')
            i += 1
            continue

        if stripped.startswith("<!--"):
            i += 1
            continue

        if stripped.startswith("```"):
            flush_para()
            lang = stripped[3:].strip()
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            out.append(f'<pre class="code-{lang or "text"}"><code>' + html.escape("\n".join(code)) + "</code></pre>")
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            flush_para()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            flush_para()
            header = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            cls = ' class="wide"' if len(header) >= 9 else (' class="dense"' if len(header) >= 7 else "")
            buf = [f"<table{cls}><thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in header) + "</tr></thead><tbody>"]
            for r in rows:
                if len(r) < len(header):
                    r = r + [""] * (len(header) - len(r))
                buf.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r[: len(header)]) + "</tr>")
            buf.append("</tbody></table>")
            out.append("".join(buf))
            continue

        if stripped.startswith("> "):
            flush_para()
            quote = []
            while i < n and lines[i].strip().startswith("> "):
                quote.append(lines[i].strip()[2:])
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(quote)) + "</p></blockquote>")
            continue

        if re.match(r"^\s*[-*]\s+", line):
            flush_para()
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]).strip())
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            flush_para()
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip())
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ol>")
            continue

        para.append(stripped)
        i += 1

    flush_para()
    return "\n".join(out)


CSS = """
@page { size: Letter; margin: 0.75in 0.7in 0.75in 0.7in; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 9.4pt; line-height: 1.38; color: #111111; margin: 0; }
p { margin: 0 0 6pt 0; text-align: left; }
h1 { font-family: Arial, Helvetica, sans-serif; font-size: 19pt; line-height: 1.15; color: #111111; margin: 28px 0 5pt 0; font-weight: bold; }
h2 { font-family: Arial, Helvetica, sans-serif; font-size: 12pt; color: #111111; margin: 18pt 0 7pt 0; padding-bottom: 2pt; border-bottom: 0.9pt solid #111111; break-after: avoid; }
h1 + h2 { border-bottom: none; font-size: 13pt; font-weight: bold; margin-top: 2pt; color: #111111; }
h3 { font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; color: #111111; margin: 12pt 0 4pt 0; break-after: avoid; }
h4 { font-family: Arial, Helvetica, sans-serif; font-size: 9.4pt; font-weight: bold; margin: 9pt 0 3pt 0; break-after: avoid; }
ul, ol { margin: 0 0 7pt 0; padding-left: 16pt; }
li { margin-bottom: 2.5pt; }
table { width: 100%; border-collapse: collapse; margin: 4pt 0 10pt 0; font-size: 8pt; line-height: 1.28; }
table.dense { font-size: 7.1pt; }
table.wide { font-size: 6.8pt; }
thead { display: table-header-group; }
th { background: #E7E6E6; color: #111111; font-family: Arial, Helvetica, sans-serif; font-size: 7.6pt; font-weight: bold; text-align: left; padding: 3pt 3.5pt; border: 0.5pt solid #7F7F7F; }
table.dense th, table.wide th { font-size: 6.9pt; }
td { padding: 3pt 3.5pt; border: 0.5pt solid #A6A6A6; vertical-align: top; }
table.dense td, table.wide td { padding: 2.6pt 3pt; }
tbody tr:nth-child(even) td { background: #FFFFFF; }
tr { break-inside: avoid; }
code { font-family: "Courier New", monospace; font-size: 8.2pt; background: #F2F2F2; padding: 0 1pt; }
pre { background: #F5F5F5; border-left: 2pt solid #7F7F7F; padding: 6pt 8pt; margin: 5pt 0 9pt 0; break-inside: avoid; }
pre code { background: none; font-size: 7.4pt; line-height: 1.3; }
blockquote { margin: 9pt 0 11pt 0; padding: 7pt 9pt; background: #F2F2F2; border-left: 2pt solid #7F7F7F; color: #222222; font-size: 8.6pt; }
blockquote p { margin: 0; }
a { color: #111111; text-decoration: underline; }
.pb { break-before: page; }
.cover h2 { page-break-after: avoid; }
"""


def build():
    parts = [(HERE / f"template-part{i}.md").read_text() for i in (1, 2, 3)]
    md = "\n\n".join(parts)
    for name, fn in BUILDERS.items():
        token = "{{" + name + "}}"
        if token not in md:
            print(f"warning: placeholder {token} not found", file=sys.stderr)
        md = md.replace(token, fn())

    leftover = re.findall(r"\{\{[A-Z_]+\}\}", md)
    if leftover:
        raise SystemExit(f"unresolved placeholders: {sorted(set(leftover))}")

    out_md = ROOT / "workpaper" / "AI-ASC606-Contract-Review-Workpaper.md"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md)
    print(f"wrote {out_md} ({len(md.splitlines())} lines, {len(md.split())} words)")

    body = md_to_html(md)
    # Wrap the cover (everything before the first page break) in a section.
    marker = '<div class="pb"></div>'
    if marker in body:
        first, rest = body.split(marker, 1)
        body = f'<section class="cover">{first}</section>{marker}{rest}'

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{ENTITY['wp_ref']} AI-Assisted ASC 606 Contract Review</title>
<style>{CSS}</style></head>
<body>{body}</body></html>"""
    out_html = HERE / "workpaper.html"
    out_html.write_text(doc)
    print(f"wrote {out_html}")


if __name__ == "__main__":
    build()
