"""The release workflow's script, run against the repository on every change."""

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _script() -> ModuleType:
    path = ROOT / ".github" / "scripts" / "release_notes.py"
    spec = importlib.util.spec_from_file_location("release_notes", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_current_version_has_release_notes(tmp_path: Path) -> None:
    notes = tmp_path / "notes.md"
    assert _script().main(["--root", str(ROOT), "--notes-file", str(notes)]) == 0
    assert notes.read_text(encoding="utf-8").strip()


def test_a_version_without_a_section_fails() -> None:
    script = _script()
    with pytest.raises(script.ReleaseError):
        script.changelog_section("# Changelog\n\n## [0.1.0] - 2026-01-01\n\n- x\n", "0.2.0")


def test_versions_below_one_are_prereleases() -> None:
    script = _script()
    assert script.is_prerelease("0.9.0")
    assert not script.is_prerelease("1.0.0")
