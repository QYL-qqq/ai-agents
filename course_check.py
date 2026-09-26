"""Show what the current W2 project actually contains and uses."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import sys
import tomllib


ROOT = Path(__file__).resolve().parent
PUBLIC_SIGNATURE = re.compile(r"s[0-9]{2,4}\Z")


@dataclass(frozen=True)
class CourseCheck:
    project: str
    version: str
    python: str
    project_environment: bool
    course_mode: str
    signature: str
    errors: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.errors


def read_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def inspect_project() -> CourseCheck:
    """Collect visible facts without deciding what a student may claim."""

    errors: list[str] = []
    project_data = read_toml(ROOT / "pyproject.toml").get("project", {})
    signature_data = read_toml(ROOT / "signature.toml").get("student", {})

    project = str(project_data.get("name", ""))
    version = str(project_data.get("version", ""))
    python = ".".join(str(part) for part in sys.version_info[:3])
    project_environment = Path(sys.prefix).resolve() == (ROOT / ".venv").resolve()
    course_mode = os.environ.get("COURSE_MODE", "")
    signature = str(signature_data.get("signature", ""))

    if project != "ai-agents-lab":
        errors.append("unexpected project name")
    if version != "0.1.0":
        errors.append("unexpected project version")
    if sys.version_info[:2] != (3, 12):
        errors.append(f"expected Python 3.12.x, got {python}")
    if not project_environment:
        errors.append("Python is not running from this project's .venv")
    if course_mode != "fixture":
        errors.append("COURSE_MODE must be fixture")
    if signature != "teacher" and not PUBLIC_SIGNATURE.fullmatch(signature):
        errors.append("signature must be teacher or a public course ID such as s07")

    return CourseCheck(
        project=project,
        version=version,
        python=python,
        project_environment=project_environment,
        course_mode=course_mode,
        signature=signature,
        errors=tuple(errors),
    )


def render(check: CourseCheck) -> str:
    lines = [
        f"project: {check.project}",
        f"version: {check.version}",
        f"python: {check.python}",
        f"project-env: {'PASS' if check.project_environment else 'FAIL'}",
        f"course-mode: {check.course_mode or '(missing)'}",
        f"signature: {check.signature or '(missing)'}",
    ]
    lines.extend(f"error: {error}" for error in check.errors)
    lines.append(f"RUNTIME_CHECK={'PASS' if check.passed else 'FAIL'}")
    return "\n".join(lines)


def main() -> int:
    check = inspect_project()
    print(render(check))
    return 0 if check.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

