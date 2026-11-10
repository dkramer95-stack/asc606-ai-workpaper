"""Build the companion test workbook with the GenOffice CLI.

1. Emit workbook data as JSON ({sheets: [{name, rows}]}).
2. `genoffice create --type xlsx` builds the workbook.
3. Emit a GenOffice workbook-DSL ops batch and apply it with `genoffice sheet apply`.
4. `genoffice render` writes one PNG per printed page so the result can be checked.

Run:  python3 genoffice_build.py
Output: ../AI-ASC606-Test-Workbook.xlsx
"""
import json
import math
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "AI-ASC606-Test-Workbook.xlsx"
GENOFFICE = pathlib.Path.home() / ".local" / "bin" / "genoffice"

sys.path.insert(0, str(HERE))
from wpdata import *  # noqa: F401,F403

HEADER = "#D9D9D9"
INK = "#000000"
RULE = "#7F7F7F"
STEEL = "#333333"
LIGHT = "#EAF0F6"
GREEN = "#E2EFDA"
AMBER = "#FFF2CC"
RED = "#FCE4E4"
GREY = "#F2F2F2"
ALT = "#F2F2F2"
BORDER = "#A6A6A6"


def col_letter(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def px(width):
    return min(390, int(width * 7.2) + 6)


def money(x):
    return f"${x:,.0f}"


def rows_to_grid(rows, ncols):
    out = []
    for row in rows:
        row = list(row)
        out.append(row + [""] * (ncols - len(row)))
    return out


def base_ops(sheet, ncols, widths, last_row, title_size=15, header_row=5, freeze=True,
             landscape=True, filter_range=None):
    """Shared ops for a table sheet with title rows 1-3 and header on row 5."""
    ops = [
        {"op": "merge_cells", "sheet": sheet, "range": f"A1:{col_letter(ncols)}1"},
        {"op": "format_range", "sheet": sheet, "range": f"A1:{col_letter(ncols)}1",
         "format": {"fontFamily": "Arial", "fontSize": title_size, "bold": True,
                    "fontColor": INK, "verticalAlign": "center"}},
        {"op": "set_row_height", "sheet": sheet, "row": 1, "heightPoints": 26},
        {"op": "format_range", "sheet": sheet, "range": f"A2:{col_letter(ncols)}2",
         "format": {"fontFamily": "Calibri", "fontSize": 9, "italic": True, "fontColor": "#55606B"}},
        {"op": "format_range", "sheet": sheet, "range": f"A3:{col_letter(ncols)}3",
         "format": {"fontFamily": "Calibri", "fontSize": 8, "fontColor": "#7A8794"}},
        {"op": "format_range", "sheet": sheet, "range": f"A{header_row}:{col_letter(ncols)}{header_row}",
         "format": {"bold": True, "fontColor": "#FFFFFF", "fillColor": HEADER,
                    "horizontalAlign": "center", "verticalAlign": "center",
                    "wrapText": True, "border": {"type": "all", "color": RULE}}},
        {"op": "set_row_height", "sheet": sheet, "row": header_row, "heightPoints": 30},
    ]
    for j, w in enumerate(widths, start=1):
        ops.append({"op": "set_col_width", "sheet": sheet, "column": col_letter(j), "widthPx": px(w)})
    if freeze:
        ops.append({"op": "set_freeze", "sheet": sheet, "rows": header_row, "columns": 0})
    if filter_range:
        ops.append({"op": "set_filter", "sheet": sheet, "range": filter_range})
    ops.append({"op": "set_page_setup", "sheet": sheet,
                "orientation": "landscape" if landscape else "portrait", "paperSize": 1,
                "fitToWidth": 1, "fitToHeight": 0, "margins": "normal",
                "header": {"right": "REV-AI-2026-01"},
                "footer": {"center": "Fictional sample | Meridian Harbor Software, Inc. | REV-AI-2026-01"}})
    return ops


def style_body(ops, sheet, ncols, first_row, last_row, widths, number_formats=None, fills=None):
    lastcol = col_letter(ncols)
    ops.append({"op": "format_range", "sheet": sheet, "range": f"A{first_row}:{lastcol}{last_row}",
                "format": {"fontFamily": "Calibri", "fontSize": 9, "verticalAlign": "top",
                           "wrapText": True, "border": {"type": "all", "color": BORDER}}})
    for r in range(first_row, last_row + 1):
        if (r - first_row) % 2 == 1:
            ops.append({"op": "format_range", "sheet": sheet, "range": f"A{r}:{lastcol}{r}",
                        "format": {"fillColor": ALT}})
        lines = 1
        for j, w in enumerate(widths, start=1):
            val = None
            lines = max(lines, 1)
        # row heights estimated from the grid outside this helper
    if number_formats:
        for rng, fmt in number_formats:
            ops.append({"op": "format_range", "sheet": sheet, "range": rng, "format": {"numberFormat": fmt}})
    if fills:
        for cell, color in fills:
            ops.append({"op": "format_range", "sheet": sheet, "range": cell, "format": {"fillColor": color}})


def add_result_rules(ops, sheet, range_):
    ops.append({"op": "add_conditional_format", "sheet": sheet, "range": range_,
                "rule": {"kind": "text", "operator": "contains", "text": "Deficiency",
                         "format": {"fillColor": AMBER}}})
    ops.append({"op": "add_conditional_format", "sheet": sheet, "range": range_,
                "rule": {"kind": "text", "operator": "contains", "text": "Ineffective",
                         "format": {"fillColor": RED}}})
    ops.append({"op": "add_conditional_format", "sheet": sheet, "range": range_,
                "rule": {"kind": "text", "operator": "contains", "text": "Fail",
                         "format": {"fillColor": RED}}})
    ops.append({"op": "add_conditional_format", "sheet": sheet, "range": range_,
                "rule": {"kind": "text", "operator": "contains", "text": "Effective",
                         "format": {"fillColor": GREEN}}})
    ops.append({"op": "add_conditional_format", "sheet": sheet, "range": range_,
                "rule": {"kind": "text", "operator": "contains", "text": "Pass",
                         "format": {"fillColor": GREEN}}})
    ops.append({"op": "add_conditional_format", "sheet": sheet, "range": range_,
                "rule": {"kind": "text", "operator": "contains", "text": "Closed",
                         "format": {"fillColor": GREEN}}})


def row_heights(grid, widths, first_row):
    heights = []
    for i, row in enumerate(grid):
        lines = 1
        for j, val in enumerate(row):
            if val in (None, ""):
                continue
            cpl = max(8, widths[j] * 1.05)
            lines = max(lines, math.ceil(len(str(val)) / cpl))
        heights.append((first_row + i, min(150, max(20, lines * 12.5 + 4))))
    return heights


def table_sheet(name, title, subtitle, headers, data, widths, center_cols=(),
                number_formats=None, conditional_range=None):
    ncols = len(headers)
    grid = [[title], [subtitle], ["REV-AI-2026-01 | Meridian Harbor Software, Inc. (fictional) | FY2026 Q4 close readiness | Fictional data"],
            [""], headers] + data
    rows = rows_to_grid(grid, ncols)
    first_data = 6
    last_row = first_data + len(data) - 1
    ops = base_ops(name, ncols, widths, last_row, filter_range=f"A5:{col_letter(ncols)}{last_row}")
    ops.append({"op": "format_range", "sheet": name, "range": f"A{first_data}:{col_letter(ncols)}{last_row}",
                "format": {"fontFamily": "Calibri", "fontSize": 9, "verticalAlign": "top",
                           "wrapText": True, "border": {"type": "all", "color": BORDER}}})
    for r in range(first_data, last_row + 1):
        if (r - first_data) % 2 == 1:
            ops.append({"op": "format_range", "sheet": name, "range": f"A{r}:{col_letter(ncols)}{r}",
                        "format": {"fillColor": ALT}})
    for (r, h) in row_heights(rows[first_data - 1:last_row], widths, first_data):
        ops.append({"op": "set_row_height", "sheet": name, "row": r, "heightPoints": h})
    for col in center_cols:
        ops.append({"op": "format_range", "sheet": name,
                    "range": f"{col_letter(col)}{first_data}:{col_letter(col)}{last_row}",
                    "format": {"horizontalAlign": "center"}})
    if number_formats:
        for rng, fmt in number_formats:
            ops.append({"op": "format_range", "sheet": name, "range": rng, "format": {"numberFormat": fmt}})
    if conditional_range:
        add_result_rules(ops, name, conditional_range)
    return rows, ops, last_row


def extra_block(ops, name, title, headers, data, start_row, widths, ncols, center_cols=(), merge_tail_from=None):
    rows = [[title], headers] + [list(r) for r in data]
    lastcol = col_letter(ncols)
    ops.append({"op": "format_range", "sheet": name, "range": f"A{start_row}:{lastcol}{start_row}",
                "format": {"fontFamily": "Arial", "fontSize": 12, "bold": True, "fontColor": INK}})
    hdr = start_row + 1
    if merge_tail_from:
        mfrom = col_letter(merge_tail_from)
        ops.append({"op": "merge_cells", "sheet": name, "range": f"{mfrom}{hdr}:{lastcol}{hdr}"})
    ops.append({"op": "format_range", "sheet": name, "range": f"A{hdr}:{lastcol}{hdr}",
                "format": {"bold": True, "fontColor": "#FFFFFF", "fillColor": HEADER,
                           "horizontalAlign": "center", "verticalAlign": "center", "wrapText": True,
                           "border": {"type": "all", "color": RULE}}})
    first = hdr + 1
    last = first + len(data) - 1
    if merge_tail_from:
        for r in range(first, last + 1):
            ops.append({"op": "merge_cells", "sheet": name,
                        "range": f"{col_letter(merge_tail_from)}{r}:{lastcol}{r}"})
    ops.append({"op": "format_range", "sheet": name, "range": f"A{first}:{lastcol}{last}",
                "format": {"fontFamily": "Calibri", "fontSize": 9, "verticalAlign": "top",
                           "wrapText": True, "border": {"type": "all", "color": BORDER}}})
    for r in range(first, last + 1):
        if (r - first) % 2 == 1:
            ops.append({"op": "format_range", "sheet": name, "range": f"A{r}:{lastcol}{r}",
                        "format": {"fillColor": ALT}})
    for col in center_cols:
        ops.append({"op": "format_range", "sheet": name,
                    "range": f"{col_letter(col)}{first}:{col_letter(col)}{last}",
                    "format": {"horizontalAlign": "center"}})
    # Height for the title row, header row and data rows.
    ops.append({"op": "set_row_height", "sheet": name, "row": start_row, "heightPoints": 20})
    ops.append({"op": "set_row_height", "sheet": name, "row": hdr, "heightPoints": 24})
    for i, r in enumerate(range(first, last + 1)):
        lines = 1
        for j, val in enumerate(data[i]):
            if val:
                w = sum(widths[j:]) if (merge_tail_from and j == merge_tail_from - 1) else widths[j]
                lines = max(lines, math.ceil(len(str(val)) / max(8, w * 1.05)))
        ops.append({"op": "set_row_height", "sheet": name, "row": r, "heightPoints": min(150, max(20, lines * 12.5 + 4))})
    return rows


def cover_sheet():
    rows = [
        [""],
        ["", "Revenue Workpaper REV-AI-2026-01", ""],
        ["", "AI-Assisted Contract Review Under ASC 606 | companion test workbook", ""],
        [""],
        ["", "Meridian Harbor Software, Inc. (fictional) | FY2026 Q4 close readiness | Fictional data", ""],
        [""],
        ["", "This is a training and portfolio sample. The entity, vendor, customers, people, contracts, amounts, "
             "test results and findings are fictional. The workbook supports the Markdown and PDF workpaper but does "
             "not replace it. Values are static: they were computed from the same data module that renders the "
             "workpaper, not by spreadsheet formulas.", ""],
        [""],
        [""],
        [""],
        ["", "Sheet", "Contents"],
    ]
    index = [
        ("Contract Register", "25-contract test sample with model and reviewer results"),
        ("Risk Register", "16 risks, inherent and residual ratings, mapped to NIST AI 600-1"),
        ("Control Matrix", "14 controls with objective, operation, owner, evidence and test result"),
        ("Control Tests", "Test method, sample size, exceptions and conclusion for each control"),
        ("Test Cases", "14 test cases: objective, expected behavior, actual result and conclusion"),
        ("Findings", "4 findings with condition, criteria, cause, effect and owner"),
        ("Observations", "3 observations that do not rise to a control finding"),
        ("Remediation", "Remediation actions with owners, dates and closure evidence"),
        ("Next Steps", "6 actions to close the gaps before the Q4 close"),
        ("Evidence Log", "16 evidence artifacts with format, retention, integrity and control linkage"),
        ("NIST Mapping", "Applicability decision and treatment for the 12 NIST AI 600-1 GenAI risks"),
        ("Metrics", "Accuracy, agreement, correction and timing metrics"),
        ("Change Log", "Version history of this workbook"),
    ]
    rows += [["", name, desc] for name, desc in index]
    rows += [[""], [""], ["", "Key metrics", ""]]
    s = SUMMARY
    metrics = [
        ("Contracts tested", "25 of 240"),
        ("Sample contract value", money(s["sample_tcv"])),
        ("Field-level extraction accuracy", "94.4% (236 of 250 checks)"),
        ("Contracts accepted without change", "20 of 25 (80%)"),
        ("Gross effect of corrections", f"{money(s['corrections_total'])} ({s['corrections_pct_pm']:.1%} of performance materiality)"),
        ("Errors that reached the ledger", "0"),
        ("Controls rated effective", "12 of 14"),
        ("Findings and observations", "4 findings, 3 observations"),
    ]
    rows += [["", k, v] for k, v in metrics]
    grid = rows_to_grid(rows, 3)
    ops = [
        {"op": "set_col_width", "sheet": "Cover", "column": "A", "widthPx": 28},
        {"op": "set_col_width", "sheet": "Cover", "column": "B", "widthPx": 250},
        {"op": "set_col_width", "sheet": "Cover", "column": "C", "widthPx": 690},
        {"op": "merge_cells", "sheet": "Cover", "range": "B2:C2"},
        {"op": "format_range", "sheet": "Cover", "range": "B2:C2",
         "format": {"fontFamily": "Arial", "fontSize": 16, "bold": True, "fontColor": INK, "verticalAlign": "center"}},
        {"op": "set_row_height", "sheet": "Cover", "row": 2, "heightPoints": 34},
        {"op": "merge_cells", "sheet": "Cover", "range": "B3:C3"},
        {"op": "format_range", "sheet": "Cover", "range": "B3:C3",
         "format": {"fontFamily": "Arial", "fontSize": 10.5, "italic": True, "fontColor": STEEL}},
        {"op": "merge_cells", "sheet": "Cover", "range": "B5:C5"},
        {"op": "format_range", "sheet": "Cover", "range": "B5:C5",
         "format": {"fontFamily": "Calibri", "fontSize": 10, "bold": True, "fontColor": STEEL}},
        {"op": "merge_cells", "sheet": "Cover", "range": "B7:C9"},
        {"op": "format_range", "sheet": "Cover", "range": "B7:C9",
         "format": {"fontFamily": "Calibri", "fontSize": 9, "fontColor": "#4D3F2A",
                    "fillColor": "#F2F2F2", "wrapText": True, "verticalAlign": "top",
                    "border": {"type": "all", "color": "#7F7F7F"}}},
        {"op": "set_row_height", "sheet": "Cover", "row": 7, "heightPoints": 18},
        {"op": "set_row_height", "sheet": "Cover", "row": 8, "heightPoints": 18},
        {"op": "set_row_height", "sheet": "Cover", "row": 9, "heightPoints": 18},
        {"op": "format_range", "sheet": "Cover", "range": "B11:C11",
         "format": {"bold": True, "fontColor": "#FFFFFF", "fillColor": HEADER,
                    "border": {"type": "all", "color": RULE}}},
    ]
    for r in range(12, 12 + len(index)):
        ops.append({"op": "format_range", "sheet": "Cover", "range": f"B{r}:C{r}",
                    "format": {"fontFamily": "Calibri", "fontSize": 9,
                               "border": {"type": "all", "color": BORDER},
                               "fillColor": ALT if (r - 12) % 2 else "#FFFFFF"}})
        ops.append({"op": "set_row_height", "sheet": "Cover", "row": r, "heightPoints": 17})
    metric_title_row = 11 + len(index) + 3
    ops.append({"op": "format_range", "sheet": "Cover", "range": f"B{metric_title_row}:C{metric_title_row}",
                "format": {"fontFamily": "Arial", "fontSize": 12, "bold": True, "fontColor": INK}})
    for r in range(metric_title_row + 1, metric_title_row + 1 + len(metrics)):
        ops.append({"op": "format_range", "sheet": "Cover", "range": f"B{r}:C{r}",
                    "format": {"fontFamily": "Calibri", "fontSize": 9,
                               "border": {"type": "all", "color": BORDER},
                               "fillColor": GREY if (r - metric_title_row) % 2 else "#FFFFFF"}})
        ops.append({"op": "set_row_height", "sheet": "Cover", "row": r, "heightPoints": 16})
        ops.append({"op": "format_range", "sheet": "Cover", "range": f"B{r}",
                    "format": {"bold": True, "fontColor": "#2A3B4C"}})
    ops.append({"op": "set_page_setup", "sheet": "Cover", "orientation": "portrait", "paperSize": 1,
                "fitToWidth": 1, "fitToHeight": 1, "margins": "normal",
                "footer": {"center": "Fictional sample | Meridian Harbor Software, Inc. | REV-AI-2026-01"}})
    return grid, ops


def build():
    sheets = []
    ops = []

    cover_grid, cover_ops = cover_sheet()
    sheets.append({"name": "Cover", "rows": cover_grid})
    ops += cover_ops

    # Contract register
    headers = ["ID", "Customer", "Industry", "Executed", "Start", "Term (months)", "TCV",
               "Non-standard feature", "Model result", "Review result", "Exception / ref"]
    data = [[c["id"], c["customer"], c["industry"], c["executed"], c["start"], c["months"], c["tcv"],
             c["feature"], c["ai"], c["review"], c["ref"]] for c in CONTRACTS]
    data.append(["Total", f"{len(CONTRACTS)} contracts", "", "", "", "", SUMMARY["sample_tcv"], "", "", "", ""])
    widths = [13, 27, 17, 11, 11, 9, 13, 38, 40, 42, 10]
    rows, sheet_ops, last = table_sheet("Contract Register", "A. Contract register",
        "The 25 contracts in the test sample, model and reviewer results", headers, data, widths,
        center_cols=(4, 5, 6, 7))
    sheets.append({"name": "Contract Register", "rows": rows})
    ops += sheet_ops
    ops.append({"op": "format_range", "sheet": "Contract Register", "range": f"G6:G{last}",
                "format": {"numberFormat": '"$"#,##0'}})
    ops.append({"op": "format_range", "sheet": "Contract Register", "range": f"A{last}:K{last}",
                "format": {"bold": True, "fillColor": LIGHT}})

    # Risk register
    headers = ["ID", "Risk", "Failure mode", "ASC / evidence area", "NIST AI 600-1 risk",
               "Inherent (L / I)", "Key controls", "Residual", "Why this residual rating"]
    data = [[r["id"], r["risk"], r["mode"], r["asc"], r["nist"], r["inherent"], r["controls"], r["residual"], r["why"]] for r in RISKS]
    widths = [7, 46, 24, 30, 34, 12, 18, 10, 44]
    rows, sheet_ops, last = table_sheet("Risk Register", "B. Risk register",
        "16 risks after controls, mapped to NIST AI 600-1 GenAI risks", headers, data, widths,
        center_cols=(1, 6, 8))
    sheets.append({"name": "Risk Register", "rows": rows})
    ops += sheet_ops
    for r in range(6, last + 1):
        val = data[r - 6][7]
        color = AMBER if val == "Medium" else GREEN if val == "Low" else None
        if color:
            ops.append({"op": "format_range", "sheet": "Risk Register", "range": f"H{r}",
                        "format": {"fillColor": color}})

    # Control matrix
    headers = ["ID", "Control", "Objective", "How it operates", "Type", "Nature", "Frequency",
               "Owner", "Key evidence", "COSO", "NIST function", "Result", "Finding"]
    data = [[c["id"], c["name"], c["objective"], c["description"], c["type"], c["nature"], c["freq"],
             c["owner"], c["evidence"], c["coso"], c["nist"], c["result"], c["finding"]] for c in CONTROLS]
    widths = [7, 27, 40, 55, 10, 15, 14, 24, 13, 14, 20, 22, 7]
    rows, sheet_ops, last = table_sheet("Control Matrix", "C. Control matrix",
        "14 controls across input, output, human, posting and monitoring layers", headers, data, widths,
        center_cols=(1, 5, 6, 7, 10, 13), conditional_range=f"L6:L{last}")
    sheets.append({"name": "Control Matrix", "rows": rows})
    ops += sheet_ops

    # Control tests
    headers = ["Control", "Name", "How the control was tested", "Sample tested", "Exceptions", "Result", "Finding"]
    data = [[c["id"], c["name"], TEST_METHOD[c["id"]], c["sample"], c["exceptions"], c["result"], c["finding"]] for c in CONTROLS]
    widths = [9, 32, 55, 18, 11, 26, 8]
    rows, sheet_ops, last = table_sheet("Control Tests", "D. Control test results",
        "Test method, sample size, exceptions and conclusion for each control", headers, data, widths,
        center_cols=(1, 5, 6, 7), conditional_range=f"F6:F{last}")
    sheets.append({"name": "Control Tests", "rows": rows})
    ops += sheet_ops

    # Test cases
    headers = ["ID", "Contract", "Controls", "Objective", "Expected behavior", "Actual result", "Conclusion", "Ref"]
    data = [[t["id"], t["contract"], t["controls"], t["objective"], t["expected"], t["actual"], t["result"], t["defect"]] for t in TESTS]
    widths = [8, 15, 15, 38, 38, 48, 20, 9]
    rows, sheet_ops, last = table_sheet("Test Cases", "E. Test cases",
        "14 tests across extraction, judgment, adversarial and routing scenarios", headers, data, widths,
        center_cols=(1, 7, 8), conditional_range=f"G6:G{last}")
    sheets.append({"name": "Test Cases", "rows": rows})
    ops += sheet_ops

    # Findings
    headers = ["ID", "Control", "Severity", "Condition", "Criteria", "Cause", "Effect", "Remediation",
               "Owner", "Due", "Status"]
    data = [[f["id"], f["control"], f["severity"], f["condition"], f["criteria"], f["cause"], f["effect"],
             f["remediation"], f["owner"], f["due"], f["status"]] for f in FINDINGS]
    widths = [17, 8, 15, 44, 38, 40, 44, 48, 24, 10, 14]
    rows, sheet_ops, last = table_sheet("Findings", "F. Findings and observations",
        "Condition, criteria, cause and effect for each finding", headers, data, widths,
        center_cols=(2, 10), conditional_range=f"C6:C{last}")
    sheets.append({"name": "Findings", "rows": rows_to_grid(rows, 11)})
    ops += sheet_ops

    # Remediation
    headers = ["Finding", "Action", "Owner", "Due", "Status", "Closure evidence"]
    data = [[f["id"], f["remediation"], f["owner"], f["due"], f["status"], ""] for f in FINDINGS]
    widths = [9, 70, 26, 11, 16, 44]
    rows, sheet_ops, last = table_sheet("Remediation", "G. Remediation",
        "Owners, dates and closure evidence", headers, data, widths,
        center_cols=(1, 4, 5), conditional_range=f"E6:E{last}")
    sheets.append({"name": "Remediation", "rows": rows_to_grid(rows, 6)})
    ops += sheet_ops

    # Observations
    headers = ["ID", "Contract", "Observation"]
    data = [[o["id"], o["contract"], o["text"]] for o in OBSERVATIONS]
    widths = [9, 16, 115]
    rows, sheet_ops, last = table_sheet("Observations", "H. Observations",
        "Matters noted in testing that do not rise to a control finding", headers, data, widths,
        center_cols=(1,))
    sheets.append({"name": "Observations", "rows": rows_to_grid(rows, 3)})
    ops += sheet_ops

    # Next steps
    headers = ["ID", "Action", "Owner", "Due", "Evidence it will create"]
    data = [list(r) for r in NEXT_STEPS]
    widths = [9, 62, 26, 11, 50]
    rows, sheet_ops, last = table_sheet("Next Steps", "I. Next steps",
        "Actions to close the gaps before the Q4 close", headers, data, widths,
        center_cols=(1, 4))
    sheets.append({"name": "Next Steps", "rows": rows_to_grid(rows, 5)})
    ops += sheet_ops

    # Evidence log
    headers = ["ID", "Evidence artifact", "Format", "Owner", "Retention", "Integrity", "What it proves", "Controls"]
    data = [[e["id"], e["artifact"], e["format"], e["owner"], e["retention"], e["integrity"], e["proves"], e["controls"]] for e in EVIDENCE]
    widths = [8, 42, 34, 24, 18, 34, 46, 12]
    rows, sheet_ops, last = table_sheet("Evidence Log", "J. Evidence log",
        "What is retained, where it lives, and what it proves", headers, data, widths, center_cols=(1, 8))
    sheets.append({"name": "Evidence Log", "rows": rows})
    ops += sheet_ops

    # NIST mapping
    headers = ["NIST AI 600-1 risk", "Applicability", "Treatment in this workflow", "Related risks"]
    data = [[n["risk"], n["applicable"], n["treat"], n["link"]] for n in NIST_RISKS]
    widths = [38, 14, 95, 22]
    rows, sheet_ops, last = table_sheet("NIST Mapping", "K. NIST AI 600-1 mapping",
        "Applicability and treatment for the 12 named GenAI risks", headers, data, widths, center_cols=(2,))
    sheets.append({"name": "NIST Mapping", "rows": rows})
    ops += sheet_ops
    for r in range(6, last + 1):
        val = data[r - 6][1]
        color = LIGHT if val == "In scope" else GREY if str(val).startswith("Out") else None
        if color:
            ops.append({"op": "format_range", "sheet": "NIST Mapping", "range": f"B{r}",
                        "format": {"fillColor": color}})

    # Metrics
    s = SUMMARY
    metrics = [
        ("Contracts in population", ENTITY["population"]),
        ("Contracts tested", s["contracts_reviewed"]),
        ("Sample contract value", money(s["sample_tcv"])),
        ("Field checks", s["field_checks"]),
        ("Field errors before review", s["field_errors"]),
        ("Field accuracy before review", f"{s['field_accuracy']:.1%}"),
        ("Contracts with a conclusion change", s["contracts_corrected"]),
        ("Corrections identified", 7),
        ("Contract-level agreement", f"{s['agreement_rate']:.0%}"),
        ("Gross effect of corrections", money(s["corrections_total"])),
        ("Corrections as a percentage of sample TCV", f"{s['corrections_pct_tcv']:.1%}"),
        ("Corrections as a percentage of performance materiality", f"{s['corrections_pct_pm']:.1%}"),
        ("Review time with the tool (hours per contract)", s["review_hours_ai"]),
        ("Manual baseline (hours per contract)", s["review_hours_manual"]),
        ("Review time reduction", f"{s['time_reduction']:.0%}"),
        ("Errors reaching the general ledger", 0),
    ]
    grid = [["L. Metrics"], ["Accuracy, agreement, correction and timing metrics"],
            ["REV-AI-2026-01 | Meridian Harbor Software, Inc. (fictional) | FY2026 Q4 close readiness | Fictional data"],
            [""], ["Summary metrics"], [""]]
    grid += [[""] if False else [k, v] for k, v in metrics]
    grid += [[""], [""], ["Field-level accuracy before review"], ["Field checked", "Contracts checked", "Errors", "Accuracy"]]
    grid += [[f, c, e, f"{1 - e / c:.1%}"] for f, c, e in FIELD_ACCURACY]
    grid += [["Total", s["field_checks"], s["field_errors"], f"{s['field_accuracy']:.1%}"]]
    rows = rows_to_grid(grid, 4)
    sheets.append({"name": "Metrics", "rows": rows})
    metrics_ops = [
        {"op": "merge_cells", "sheet": "Metrics", "range": "A1:D1"},
        {"op": "merge_cells", "sheet": "Metrics", "range": "A2:D2"},
        {"op": "merge_cells", "sheet": "Metrics", "range": "A3:D3"},
        {"op": "format_range", "sheet": "Metrics", "range": "A1:D1",
         "format": {"fontFamily": "Arial", "fontSize": 15, "bold": True, "fontColor": INK}},
        {"op": "set_row_height", "sheet": "Metrics", "row": 1, "heightPoints": 26},
        {"op": "format_range", "sheet": "Metrics", "range": "A2:D2",
         "format": {"fontSize": 9, "italic": True, "fontColor": "#55606B"}},
        {"op": "format_range", "sheet": "Metrics", "range": "A3:D3",
         "format": {"fontSize": 8, "fontColor": "#7A8794"}},
        {"op": "format_range", "sheet": "Metrics", "range": "A5:D5",
         "format": {"fontFamily": "Arial", "fontSize": 12, "bold": True, "fontColor": INK}},
        {"op": "set_col_width", "sheet": "Metrics", "column": "A", "widthPx": 420},
        {"op": "set_col_width", "sheet": "Metrics", "column": "B", "widthPx": 150},
        {"op": "set_col_width", "sheet": "Metrics", "column": "C", "widthPx": 80},
        {"op": "set_col_width", "sheet": "Metrics", "column": "D", "widthPx": 90},
        {"op": "set_page_setup", "sheet": "Metrics", "orientation": "portrait", "paperSize": 1,
         "fitToWidth": 1, "fitToHeight": 1, "margins": "normal",
         "footer": {"center": "Fictional sample | Meridian Harbor Software, Inc. | REV-AI-2026-01"}},
    ]
    for r in range(7, 7 + len(metrics)):
        metrics_ops.append({"op": "format_range", "sheet": "Metrics", "range": f"A{r}:B{r}",
                            "format": {"fontSize": 9, "border": {"type": "all", "color": BORDER},
                                       "fillColor": GREY if (r - 7) % 2 else "#FFFFFF"}})
        metrics_ops.append({"op": "format_range", "sheet": "Metrics", "range": f"A{r}",
                            "format": {"bold": True, "fontColor": "#2A3B4C"}})
        metrics_ops.append({"op": "set_row_height", "sheet": "Metrics", "row": r, "heightPoints": 16})
    fld_title = 7 + len(metrics) + 2
    metrics_ops.append({"op": "format_range", "sheet": "Metrics", "range": f"A{fld_title}:D{fld_title}",
                        "format": {"fontFamily": "Arial", "fontSize": 12, "bold": True, "fontColor": INK}})
    hdr = fld_title + 1
    metrics_ops.append({"op": "format_range", "sheet": "Metrics", "range": f"A{hdr}:D{hdr}",
                        "format": {"bold": True, "fontColor": "#FFFFFF", "fillColor": HEADER,
                                   "horizontalAlign": "center", "border": {"type": "all", "color": RULE},
                                   "wrapText": True}})
    first = hdr + 1
    last = first + len(FIELD_ACCURACY)
    metrics_ops.append({"op": "format_range", "sheet": "Metrics", "range": f"A{first}:D{last}",
                        "format": {"fontSize": 9, "border": {"type": "all", "color": BORDER},
                                   "wrapText": True, "verticalAlign": "top"}})
    for r in range(first, last + 1):
        metrics_ops.append({"op": "format_range", "sheet": "Metrics", "range": f"B{r}:D{r}",
                            "format": {"horizontalAlign": "center"}})
        if (r - first) % 2 == 1:
            metrics_ops.append({"op": "format_range", "sheet": "Metrics", "range": f"A{r}:D{r}",
                                "format": {"fillColor": ALT}})
        metrics_ops.append({"op": "set_row_height", "sheet": "Metrics", "row": r, "heightPoints": 16})
    metrics_ops.append({"op": "format_range", "sheet": "Metrics", "range": f"A{last}:D{last}",
                        "format": {"bold": True, "fillColor": LIGHT}})
    ops += metrics_ops

    # Change log
    headers = ["Version", "Date", "Description", "Author"]
    data = [
        ("1.0", "2026-10-20", "Initial workbook generated with the draft workpaper", "A. Okafor"),
        ("1.1", "2026-10-24", "Reviewer comments; control tests and findings added", "R. Tan"),
        ("1.2", "2026-10-27", "Final version; remediation, evidence log and metrics added", "A. Okafor"),
    ]
    widths = [10, 12, 75, 16]
    rows, sheet_ops, last = table_sheet("Change Log", "M. Change log",
        "Version history of this workbook", headers, data, widths, center_cols=(1, 2, 4))
    rows = rows_to_grid(rows, 4)
    sheets.append({"name": "Change Log", "rows": rows})
    ops += sheet_ops

    data_path = HERE / "workbook_data.json"
    ops_path = HERE / "workbook_ops.json"
    data_path.write_text(json.dumps({"sheets": sheets}, ensure_ascii=False))
    ops_path.write_text(json.dumps(ops, ensure_ascii=False))
    print(f"sheets: {len(sheets)}  ops: {len(ops)}")

    def run(cmd):
        print("+", " ".join(str(c) for c in cmd))
        p = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
        if p.returncode != 0:
            print("STDOUT:", p.stdout[-3000:])
            print("STDERR:", p.stderr[-3000:])
            raise SystemExit(f"genoffice failed: {p.returncode}")
        return p.stdout

    run([GENOFFICE, "create", "--type", "xlsx", "--from", data_path, "--out", OUT, "--force"])
    out = run([GENOFFICE, "sheet", "apply", OUT, "--ops", ops_path, "--force"])
    try:
        result = json.loads(out)
        print("apply status:", result.get("status"), "ops applied:", (result.get("detail") or {}).get("batch", result.get("detail")))
        failures = (result.get("detail") or {}).get("failures")
        if failures:
            print("FAILURES:", json.dumps(failures, indent=1)[:4000])
    except json.JSONDecodeError:
        print(out[:2000])
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()
