"""Write CHANGES.md: every Text/Translation change and the new cards, from the build inputs."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import OVERRIDES, to_c1  # noqa: E402
from validate import load_all  # noqa: E402

HERE = Path(__file__).parent
CLOZE = re.compile(r"\{\{c\d+::(.*?)(?:::([^}]*))?\}\}")


def short(text: str) -> str:
    return CLOZE.sub(lambda m: f"[{m.group(1)}|{m.group(2) or ''}]", to_c1(text)).replace("<br>", " / ")


def main() -> None:
    cards = json.loads((HERE / "work" / "structure.json").read_text(encoding="utf-8"))
    content = load_all()
    sections = {"dup": [], "hint": [], "tr": [], "text": [], "new": []}
    for c in cards:
        sid, e = c["sort_id"], dict(content[c["sort_id"]])
        ov = OVERRIDES.get(sid, {})
        if c["old_id"] is None:
            text = ov.get("text", e.get("text", c["text"]))
            sections["new"].append(f"- **{sid}**: `{short(text)}` — {e.get('tr', c['tr'])}")
            continue
        text = ov.get("text", e.get("text", c["text"]))
        tr = ov.get("tr", e.get("tr", c["tr"]))
        if to_c1(text) == to_c1(c["text"]) and tr == c["tr"]:
            continue
        flag = ov.get("flag") or e.get("flag", "")
        if "tr" in ov and "tr" not in e:
            flag = flag or "tr: read-through correction"
        kind = flag.split(":", 1)[0] if flag else "text"
        kind = kind if kind in sections else "text"
        why = flag.split(":", 1)[1].strip() if ":" in flag else flag
        lines = [f"- **{sid}** ({c['old_id']}): {why}  "]
        if to_c1(text) != to_c1(c["text"]):
            lines.append(f"  `{short(c['text'])}` → `{short(text)}`  ")
        if tr != c["tr"]:
            lines.append(f"  '{c['tr']}' → '{tr}'")
        sections[kind].append("\n".join(lines).rstrip())
    titles = {"dup": "Near-duplicates replaced", "hint": "Hints fixed", "tr": "Translations fixed",
              "text": "Text fixed (cues and hints)", "new": "New cards"}
    out = ["# Change log: Japanese cloze grammar deck", "",
           "Every Text/Translation change, by new sort ID (old sort ID in brackets). "
           "Cloze text is shown as `[answer|hint]`; c2/c3 are shown as c1, as in the deck.", ""]
    for k, title in titles.items():
        if sections[k]:
            out += [f"## {title} ({len(sections[k])})", ""] + sections[k] + [""]
    (HERE / "CHANGES.md").write_text("\n".join(out), encoding="utf-8")
    print({k: len(v) for k, v in sections.items()})


if __name__ == "__main__":
    main()
