"""Build the sample calculation workbook for evidence pack C-2026-014 with GenOffice."""
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
PACK = HERE.parent / "evidence" / "C-2026-014"
GEN = pathlib.Path.home() / ".local" / "bin" / "genoffice"
OUT = PACK / "05_calc_C-2026-014.xlsx"

allocation = [
    ["Step", "Calculation", "Amount"],
    ["Transaction price", "36 months x $40,000", 1440000],
    ["Subscription standalone selling price", "36 months x $40,000, no discount in the initial term", 1440000],
    ["Option standalone selling price", "70% renewal likelihood x 5% x $576,000 annual list", 20160],
    ["Total standalone selling price", "$1,440,000 + $20,160", 1460160],
    ["Allocated to material right", "1,440,000 x 20,160 / 1,460,160", 19882],
    ["Allocated to subscription", "1,440,000 - 19,882", 1420118],
    ["Monthly subscription revenue", "1,420,118 / 36 = 39,447.72", 39448],
    ["Months recognized in FY2026", "July 2026 to December 2026", "6 months"],
    ["FY2026 revenue, model output", "6 x 40,000", 240000],
    ["FY2026 revenue, corrected", "6 x 39,447.72 (unrounded)", 236686],
    ["FY2026 revenue reduction", "240,000 - 236,686", 3314],
]

journal = [
    ["Account", "Debit", "Credit"],
    ["Revenue, subscription", 3314, ""],
    ["Deferred revenue, current", "", 3314],
]

inputs = [
    ["Field", "Value"],
    ["Contract ID", "C-2026-014"],
    ["Customer", "Blue Harbor Logistics, Inc."],
    ["Executed", "2026-07-01"],
    ["Term", "36 months, 2026-07-01 to 2029-06-30"],
    ["Total contract value", "$1,440,000"],
    ["Renewal pricing", "95% of then-current List Price (5% discount)"],
    ["SSP table", "2026.1"],
    ["SSP table effective date", "2026-01-01"],
    ["Rate source", "Approved SSP schedule, hosted platform configuration B"],
    ["Model", "ContractLens 2.4.1 / nlx-4o-2026-05"],
    ["Prompt and schema", "v3.2 / v3.2"],
    ["Document hash", "sha256:8f1c...a7d2"],
    ["Model output hash", "sha256:c41e...9b06"],
    ["Prepared by", "A. Okafor, Senior Revenue Analyst"],
    ["Reviewed by", "R. Tan, Revenue Controller"],
    ["Second-level reviewer", "M. Lindqvist, VP Finance"],
    ["Journal entry", "JE-2026-10-0142"],
    ["Posted", "2026-10-09"],
]

rows = []
rows += [[f"Calculation workbook: C-2026-014"]]
rows += [["Blue Harbor Logistics, Inc. | TCV $1,440,000 | Workpaper REV-AI-2026-01 | Fictional evidence sample"]]
rows += [[]]
rows += allocation
rows += [[]]
rows += [["Journal entry at 2026-12-31"]]
rows += journal
rows += [[]]
rows += [["Prepared by A. Okafor, Senior Revenue Analyst on 2026-10-07; reviewed by R. Tan, Revenue Controller on 2026-10-07; second-level review by M. Lindqvist, VP Finance on 2026-10-08."]]
grid = [r + [""] * (3 - len(r)) for r in rows]

input_rows = [[f"Inputs and version record: C-2026-014"], ["Workpaper REV-AI-2026-01 | Fictional evidence sample"]] + [[]] + inputs
input_grid = [r + [""] * (2 - len(r)) for r in input_rows]

data_path = HERE / "evidence_calc_data.json"
data_path.write_text(json.dumps({"sheets": [
    {"name": "Allocation", "rows": grid},
    {"name": "Inputs", "rows": input_grid},
]}))

# row numbers: title 1, subtitle 2, blank 3, header 4, data 5-15, blank 16, JE title 17,
# JE header 18, JE rows 19-20, blank 21, sign-off 22
ops = [
    {"op": "merge_cells", "sheet": "Allocation", "range": "A1:C1"},
    {"op": "merge_cells", "sheet": "Allocation", "range": "A2:C2"},
    {"op": "merge_cells", "sheet": "Allocation", "range": "A22:C22"},
    {"op": "set_row_height", "sheet": "Allocation", "row": 2, "heightPoints": 18},
    {"op": "set_row_height", "sheet": "Allocation", "row": 22, "heightPoints": 48},
    {"op": "format_range", "sheet": "Allocation", "range": "A1:C1",
     "format": {"fontFamily": "Georgia", "fontSize": 14, "bold": True, "fontColor": "#12324F"}},
    {"op": "format_range", "sheet": "Allocation", "range": "A2:C2",
     "format": {"fontSize": 9, "italic": True, "fontColor": "#55606B"}},
    {"op": "format_range", "sheet": "Allocation", "range": "A4:C4",
     "format": {"bold": True, "fontColor": "#FFFFFF", "fillColor": "#12324F",
                "border": {"type": "all", "color": "#12324F"}}},
    {"op": "format_range", "sheet": "Allocation", "range": "A5:C15",
     "format": {"fontSize": 9, "border": {"type": "all", "color": "#B7C4D1"}, "verticalAlign": "top", "wrapText": True}},
    {"op": "format_range", "sheet": "Allocation", "range": "C5:C15", "format": {"numberFormat": '"$"#,##0'}},
    {"op": "format_range", "sheet": "Allocation", "range": "A17:C17",
     "format": {"fontFamily": "Georgia", "fontSize": 12, "bold": True, "fontColor": "#12324F"}},
    {"op": "format_range", "sheet": "Allocation", "range": "A18:C18",
     "format": {"bold": True, "fontColor": "#FFFFFF", "fillColor": "#12324F",
                "border": {"type": "all", "color": "#12324F"}}},
    {"op": "format_range", "sheet": "Allocation", "range": "A19:C20",
     "format": {"fontSize": 9, "border": {"type": "all", "color": "#B7C4D1"}}},
    {"op": "format_range", "sheet": "Allocation", "range": "B19:C20", "format": {"numberFormat": '"$"#,##0'}},
    {"op": "format_range", "sheet": "Allocation", "range": "A22:C22",
     "format": {"fontSize": 8, "italic": True, "fontColor": "#55606B", "wrapText": True}},
    {"op": "set_col_width", "sheet": "Allocation", "column": "A", "widthPx": 300},
    {"op": "set_col_width", "sheet": "Allocation", "column": "B", "widthPx": 400},
    {"op": "set_col_width", "sheet": "Allocation", "column": "C", "widthPx": 120},
    {"op": "set_row_height", "sheet": "Allocation", "row": 4, "heightPoints": 20},
    {"op": "set_row_height", "sheet": "Allocation", "row": 18, "heightPoints": 20},
    {"op": "set_page_setup", "sheet": "Allocation", "orientation": "portrait", "paperSize": 1,
     "fitToWidth": 1, "fitToHeight": 1, "margins": "normal",
     "footer": {"center": "Fictional evidence sample | REV-AI-2026-01 | C-2026-014"}},
    {"op": "merge_cells", "sheet": "Inputs", "range": "A1:B1"},
    {"op": "merge_cells", "sheet": "Inputs", "range": "A2:B2"},
    {"op": "format_range", "sheet": "Inputs", "range": "A1:B1",
     "format": {"fontFamily": "Georgia", "fontSize": 14, "bold": True, "fontColor": "#12324F"}},
    {"op": "format_range", "sheet": "Inputs", "range": "A2:B2",
     "format": {"fontSize": 9, "italic": True, "fontColor": "#55606B"}},
    {"op": "format_range", "sheet": "Inputs", "range": "A4:B4",
     "format": {"bold": True, "fontColor": "#FFFFFF", "fillColor": "#12324F",
                "border": {"type": "all", "color": "#12324F"}}},
    {"op": "format_range", "sheet": "Inputs", "range": "A5:B23",
     "format": {"fontSize": 9, "border": {"type": "all", "color": "#B7C4D1"}, "verticalAlign": "top", "wrapText": True}},
    {"op": "set_col_width", "sheet": "Inputs", "column": "A", "widthPx": 240},
    {"op": "set_col_width", "sheet": "Inputs", "column": "B", "widthPx": 520},
    {"op": "set_page_setup", "sheet": "Inputs", "orientation": "portrait", "paperSize": 1,
     "fitToWidth": 1, "fitToHeight": 1, "margins": "normal",
     "footer": {"center": "Fictional evidence sample | REV-AI-2026-01 | C-2026-014"}},
]
ops_path = HERE / "evidence_calc_ops.json"
ops_path.write_text(json.dumps(ops))

for cmd in ([GEN, "create", "--type", "xlsx", "--from", data_path, "--out", OUT, "--force"],
            [GEN, "sheet", "apply", OUT, "--ops", ops_path, "--force"]):
    p = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if p.returncode:
        print(p.stdout[-2000:], p.stderr[-2000:])
        raise SystemExit(1)
print("wrote", OUT)
