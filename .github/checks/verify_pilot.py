"""Trusted pilot acceptance checks; control-gate blocks PR edits to this file."""

import importlib.util
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "salon_booking.py"


def check() -> None:
    """Check the fixed booking contract and required pilot documents."""
    if not MODULE.exists():
        base = os.environ.get("BASE_SHA")
        if base:
            existed = subprocess.run(
                ["git", "cat-file", "-e", f"{base}:salon_booking.py"],
                cwd=ROOT,
                check=False,
                capture_output=True,
            ).returncode == 0
            changed = subprocess.check_output(
                ["git", "diff", "--name-only", base, "HEAD"],
                cwd=ROOT,
                text=True,
            ).splitlines()
            application_changes = [
                path for path in changed
                if not path.startswith((".github/", "docs/"))
                and path not in ("README.md", ".coderabbit.yaml")
            ]
            if existed or application_changes:
                raise AssertionError("application changes require salon_booking.py")
        return

    required = [
        ROOT / "docs" / name
        for name in (
            "requirements.md",
            "implementation-plan.md",
            "setup.md",
            "operations.md",
            "change-log.md",
        )
    ]
    for path in required:
        if not path.is_file() or len(path.read_text(encoding="utf-8").strip()) < 40:
            raise AssertionError(f"missing or empty document: {path.relative_to(ROOT)}")

    spec = importlib.util.spec_from_file_location("salon_booking", MODULE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    can_book = module.can_book
    assert can_book([], 10, 20) is True
    assert can_book([(10, 20)], 20, 30) is True
    assert can_book([(10, 20)], 5, 10) is True
    assert can_book([(10, 20)], 15, 25) is False
    assert can_book([(10, 20), (30, 40)], 35, 45) is False
    assert can_book([(10, 20)], 10, 20) is False
    assert can_book([], 20, 20) is False
    assert can_book([], 30, 20) is False
    assert can_book([(10, 20)], 20, 20) is False
    assert can_book([(10, 20)], 30, 20) is False


if __name__ == "__main__":
    check()
    print("pilot acceptance passed")
