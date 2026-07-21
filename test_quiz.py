"""Minimal verification that quiz JSONs load correctly."""
import json
import sys
from pathlib import Path

REQUIRED = {"vraag", "opties", "antwoord"}
ALLOWED = REQUIRED | {"toelichting", "domein", "_idx", "agent", "model"}

errors = 0
exam_dir = Path(__file__).resolve().parent / "quizzes"

for fp in sorted(exam_dir.glob("quiz-*.json")):
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ {fp.name}: invalid JSON — {e}")
        errors += 1
        continue

    if not isinstance(data, list):
        print(f"❌ {fp.name}: root is not a list")
        errors += 1
        continue

    for i, q in enumerate(data, 1):
        missing = REQUIRED - q.keys()
        unknown = q.keys() - ALLOWED
        if missing:
            print(f"❌ {fp.name} Q{i}: missing {missing}")
            errors += 1
        if unknown:
            print(f"❌ {fp.name} Q{i}: unknown fields {unknown}")
            errors += 1
        if not isinstance(q["vraag"], str) or not q["vraag"].strip():
            print(f"❌ {fp.name} Q{i}: invalid vraag")
            errors += 1
        if not isinstance(q["opties"], list) or len(q["opties"]) < 2:
            print(f"❌ {fp.name} Q{i}: invalid opties")
            errors += 1
        if not isinstance(q["antwoord"], int) or not (0 <= q["antwoord"] < len(q["opties"])):
            print(f"❌ {fp.name} Q{i}: invalid antwoord index")
            errors += 1
        if "domein" in q and (not isinstance(q["domein"], str) or not q["domein"].strip()):
            print(f"❌ {fp.name} Q{i}: 'domein' must be a non-empty string")
            errors += 1

    print(f"✅ {fp.name}: {len(data)} questions OK")

if errors:
    print(f"\n❌ {errors} error(s) found")
    sys.exit(1)
else:
    print(f"\n✅ All quizzes valid!")
