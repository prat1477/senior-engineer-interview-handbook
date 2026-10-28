from pathlib import Path

MODULES = {
    4: ("module-04-collections", "module-04-collections-production-playbook.md", ("14-interview-practice.md", "15-interview-assessment-answers.md")),
    5: ("module-05-generics", "module-05-generics-production-playbook.md", ("05-interview-practice.md", "06-interview-assessment-answers.md")),
    6: ("module-06-java-8-streams", "module-06-java-8-streams-production-playbook.md", ("05-interview-practice.md", "06-interview-assessment-answers.md")),
    7: ("module-07-optional", "module-07-optional-production-playbook.md", ("03-interview-practice.md", "04-interview-assessment-answers.md")),
    8: ("module-08-exception-handling", "module-08-exception-handling-production-playbook.md", ("04-interview-practice.md", "05-interview-assessment-answers.md")),
    9: ("module-09-jvm-basics", "module-09-jvm-basics-production-playbook.md", ("10-interview-practice.md", "11-interview-assessment-answers.md")),
}

for _num, (mdir, play, files) in MODULES.items():
    for fn in files:
        p = Path("docs/java") / mdir / fn
        if not p.exists():
            continue
        is_ans = "answers" in fn or "assessment" in fn
        comp = f"../../books/02-interview-companion/core-java/{mdir}/"
        target = comp + ("module-interview-assessment-answers.md" if is_ans else "module-interview-practice.md")
        label = "Assessment answers" if is_ans else "Interview practice"
        p.write_text(
            f"""---
title: "Moved — {fn}"
description: Stub pointer to Interview Companion.
status: stable
audience: all
tags: [stub]
updated: 2026-10-18
---

# Content moved

| Book | Link |
| --- | --- |
| **Interview Companion** | [{label}]({target}) |
| **Production playbook** | [Module playbook](../../books/03-production-playbook/core-java/{play}) |
""",
            encoding="utf-8",
        )

print("stubs ok")
