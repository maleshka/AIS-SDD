import sys, re, pathlib, yaml
root = pathlib.Path(sys.argv[1])
out = []
ok = True
# 1) YAML syntax
for p in sorted(root.rglob("*.yaml")):
    try:
        yaml.safe_load(p.read_text(encoding="utf-8"))
        out.append(f"PASS yaml  {p.relative_to(root)}")
    except Exception as e:
        ok = False; out.append(f"FAIL yaml  {p.relative_to(root)}: {e}")
# 2) defined IDs
ctx = yaml.safe_load((root/"spec/architecture/context/architecture-context.yaml").read_text())
defined = {e["id"] for e in ctx["elements"]}
defined |= {m["id"] for m in ctx["model_findings"]}
def collect(path, key, field="id"):
    d = yaml.safe_load((root/path).read_text())
    return {x[field] for x in d[key]}
defined |= collect("spec/requirements/business-rules.yaml", "business_rules")
defined |= collect("spec/requirements/quality-requirements.yaml", "quality_requirements")
defined |= collect("spec/application/interactions.yaml", "interactions")
rc = yaml.safe_load((root/"spec/architecture/continuum/reuse-catalog.yaml").read_text())
for r in rc["reuse_candidates"]:
    defined.add(r["abb"]["id"]); defined.add(r["sbb"]["id"])
feat = (root/"spec/stories/features/US-002.feature").read_text()
defined |= set(re.findall(r"@(SC-\d{3}-\d{2})", feat))
defined |= {"US-002", "BSC-002", "API-Tickets"}
defined |= {p.name[:7] for p in (root/"spec/architecture/decisions").glob("ADR-*.md")}
oq = (root/"spec/drafts/open-questions.md").read_text()
defined |= set(re.findall(r"\b(Q-\d{2}[ab]?)\b", oq.split("## Otvorené")[0])) | set(re.findall(r"### \S+ (Q-\d{2}[ab]?)", oq))
# 3) referenced IDs
pat = re.compile(r"\b((?:SH|DRV|ASM|G|OUT|PRI|R|C|CTR|ACT|ROLE|BE|BP|BS|BI|BO|MEA|REP|PRD|AC|AF|AS|AIF|DO|LOC|NODE|DEV|SSW|TS|ART|NET|PL|GAP|WP|D|IE|BR|QR|SC|US|INT|ADR|Q|MF|ABB|SBB|BSC)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\b")
missing = {}
files = [p for p in root.rglob("*") if p.is_file() and p.suffix in (".yaml",".md",".feature") and p.name != "AGENTS.md" and "reports" not in p.parts]
for p in files:
    for m in pat.findall(p.read_text(encoding="utf-8")):
        if m not in defined and m not in ("AS-IS",) and not m.startswith("R-000") and not re.search(r"(xx|0x)$", m):
            missing.setdefault(m, set()).add(str(p.relative_to(root)))
# ignore Q-04 / Q-10 / Q-14 base ids (a/b variants defined) and SC-xx placeholders
for k in list(missing):
    if re.fullmatch(r"Q-(04|10|14)", k) or k in ("SC-002-xx",): missing.pop(k)
if missing:
    ok = False
    for k, v in sorted(missing.items()):
        out.append(f"FAIL id    {k} – nedefinované, použité v: {', '.join(sorted(v))}")
else:
    out.append(f"PASS ids   všetky použité IDs sú definované ({len(defined)} definovaných)")
# 4) every scenario linked to R-002 in requirements
req = yaml.safe_load((root/"spec/requirements/requirements.yaml").read_text())
r2 = [r for r in req["requirements"] if r["id"]=="R-002"][0]
sc_feat = set(re.findall(r"@(SC-\d{3}-\d{2})", feat))
diff = sc_feat ^ set(r2["acceptance_scenarios"])
out.append(("PASS" if not diff else "FAIL") + f" trace  scenáre vo feature = acceptance_scenarios R-002 {'' if not diff else diff}")
ok = ok and not diff
print("\n".join(out)); print("RESULT:", "PASS" if ok else "FAIL")
