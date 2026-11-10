"""Write the evidence pack manifest (bytes + SHA-256) for C-2026-014."""
import hashlib
import pathlib

PACK = pathlib.Path(__file__).resolve().parent.parent / "evidence" / "C-2026-014"
ROLES = {
    "04_ai_output_C-2026-014.json": ("Model output", "EV-03"),
    "05_calc_C-2026-014.xlsx": ("Independent calculation", "EV-04"),
    "06_review_C-2026-014.md": ("Reviewer annotation and sign-off", "EV-05"),
    "07_sl2_C-2026-014.md": ("Second-level review memorandum", "EV-06"),
    "README.md": ("Pack guide", "-"),
}
lines = ["file\trole\tevidence_id\tbytes\tsha256\tretention"]
for path in sorted(PACK.iterdir()):
    if path.name in ("manifest.tsv",) or not path.is_file():
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    role, ev = ROLES.get(path.name, ("Unclassified", "-"))
    lines.append(f"{path.name}\t{role}\t{ev}\t{path.stat().st_size}\t{digest}\t7 years from FY2026 close")
manifest = "\n".join(lines) + "\n"
(PACK / "manifest.tsv").write_text(manifest)
print(manifest)
