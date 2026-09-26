from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

import course_check


ROOT = Path(__file__).resolve().parents[1]


def test_project_metadata():
    check = course_check.inspect_project()

    assert check.project == "ai-agents-lab"
    assert check.version == "0.1.0"


def test_python_minor_version():
    assert sys.version_info[:2] == (3, 12)


def test_python_comes_from_this_project():
    assert Path(sys.prefix).resolve() == (ROOT / ".venv").resolve()


def test_course_mode_is_visible_to_this_command():
    assert os.environ.get("COURSE_MODE") == "fixture"


def test_signature_is_read_from_toml():
    expected = course_check.read_toml(ROOT / "signature.toml")["student"]["signature"]

    assert course_check.inspect_project().signature == expected


def test_course_check_command_reports_pass():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "course_check.py")],
        cwd=ROOT,
        env=os.environ.copy(),
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "project: ai-agents-lab" in completed.stdout
    assert "RUNTIME_CHECK=PASS" in completed.stdout

