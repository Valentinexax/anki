"""Read and write the text-based deck format stored under decks/<slug>/.

Layout of one deck directory:
    deck.yaml   deck names/ids and note type definitions (fields, templates, CSS)
    notes.yaml  one entry per note: guid, notetype, optional subdeck, tags, fields
    media/      images and audio referenced by notes
"""

from __future__ import annotations

from pathlib import Path

import yaml


class _Dumper(yaml.SafeDumper):
    pass


def _str_presenter(dumper: yaml.SafeDumper, data: str) -> yaml.ScalarNode:
    # Multi-line HTML/CSS reads and diffs far better as a literal block.
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_Dumper.add_representer(str, _str_presenter)


def dump(data, path: Path) -> None:
    path.write_text(
        yaml.dump(data, Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class Deck:
    def __init__(self, root: Path):
        self.root = root
        self.slug = root.name
        meta = load(root / "deck.yaml")
        self.name: str = meta["name"]
        self.decks: dict[str, int] = meta["decks"]
        self.notetypes: list[dict] = meta["notetypes"]
        self.notes: list[dict] = load(root / "notes.yaml") or []

    @property
    def media_dir(self) -> Path:
        return self.root / "media"

    def notetype(self, name: str) -> dict | None:
        return next((nt for nt in self.notetypes if nt["name"] == name), None)


def all_decks(decks_dir: Path, only: list[str] | None = None) -> list[Deck]:
    dirs = sorted(p for p in decks_dir.iterdir() if (p / "deck.yaml").exists())
    if only:
        dirs = [p for p in dirs if p.name in only]
    return [Deck(p) for p in dirs]
