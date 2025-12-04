#!/usr/bin/env python3
"""Development helper for python-companyatlas.

Company information lookup and enrichment library.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Sequence

# Load .env file if it exists
_env_file = Path(__file__).resolve().parent / ".env"
if _env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_file)
    except ImportError:
        pass


BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
NC = "\033[0m"

if platform.system() == "Windows" and not os.environ.get("ANSICON"):
    BLUE = GREEN = RED = YELLOW = NC = ""


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"


def _resolve_venv_dir() -> Path:
    """Find the virtual env directory, preferring .venv over venv."""
    preferred_names = [".venv", "venv"]
    for name in preferred_names:
        candidate = PROJECT_ROOT / name
        if candidate.exists():
            return candidate
    return PROJECT_ROOT / preferred_names[0]


VENV_DIR = _resolve_venv_dir()
VENV_BIN = VENV_DIR / ("Scripts" if platform.system() == "Windows" else "bin")
PYTHON = VENV_BIN / ("python.exe" if platform.system() == "Windows" else "python")
PIP = VENV_BIN / ("pip.exe" if platform.system() == "Windows" else "pip")


def print_info(message: str) -> None:
    print(f"{BLUE}{message}{NC}")


def print_success(message: str) -> None:
    print(f"{GREEN}{message}{NC}")


def print_error(message: str) -> None:
    print(f"{RED}{message}{NC}", file=sys.stderr)


def print_warning(message: str) -> None:
    print(f"{YELLOW}{message}{NC}")


def run_command(cmd: Sequence[str], check: bool = True, **kwargs) -> bool:
    printable = " ".join(cmd)
    print_info(f"Running: {printable}")
    try:
        subprocess.run(cmd, check=check, cwd=PROJECT_ROOT, **kwargs)
        return True
    except subprocess.CalledProcessError as exc:
        print_error(f"Command exited with code {exc.returncode}")
        return False
    except FileNotFoundError:
        print_error(f"Command not found: {cmd[0]}")
        return False


def venv_exists() -> bool:
    return VENV_DIR.exists() and PYTHON.exists()


def ensure_venv_activation(command: str) -> None:
    """Re-executes this script inside the project virtualenv if present."""
    venv_management_commands = {"venv", "venv-clean"}
    if command in venv_management_commands:
        return

    if not venv_exists():
        return

    current_python = Path(sys.executable).resolve()
    desired_python = PYTHON.resolve()
    if current_python == desired_python:
        return

    print_info(f"Activating virtual environment at {VENV_DIR}...")
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(VENV_DIR)
    env["PATH"] = f"{VENV_BIN}{os.pathsep}{env.get('PATH', '')}"

    args = [str(desired_python), str(Path(__file__).resolve()), *sys.argv[1:]]
    os.execve(str(desired_python), args, env)


def get_code_directories() -> list[str]:
    targets: list[str] = []

    if SRC_DIR.exists():
        for candidate in SRC_DIR.iterdir():
            if candidate.is_dir() and not candidate.name.endswith(".egg-info"):
                targets.append(str(candidate.relative_to(PROJECT_ROOT)))

    if TESTS_DIR.exists():
        targets.append(str(TESTS_DIR.relative_to(PROJECT_ROOT)))

    return targets or ["."]


def install_build_dependencies() -> bool:
    return run_command([str(PIP), "install", "--upgrade", "pip", "setuptools", "wheel"])


def task_help() -> bool:
    print(f"{BLUE}python-companyatlas — available commands{NC}\n")
    
    print(f"{GREEN}Environment:{NC}")
    print("  venv              Create a local virtual environment")
    print("  install           Install the package in production mode")
    print("  install-dev       Install the package in editable mode with dev dependencies")
    print("  venv-clean        Recreate the virtual environment")
    print("")
    
    print(f"{GREEN}Quality & Testing:{NC}")
    print("  test              Run pytest")
    print("  test-verbose      Run pytest with verbose output")
    print("  coverage          Run tests with coverage report")
    print("  lint              Run ruff and mypy")
    print("  format            Format code with ruff")
    print("  check             Run lint/format checks")
    print("")
    
    print(f"{GREEN}Cleaning:{NC}")
    print("  clean             Remove build, bytecode, and test artifacts")
    print("  clean-build       Remove build artifacts")
    print("  clean-pyc         Remove Python bytecode")
    print("  clean-test        Remove test artifacts")
    print("")
    
    print(f"{GREEN}Packaging:{NC}")
    print("  build             Build sdist and wheel")
    print("  upload-test       Upload to TestPyPI")
    print("  upload            Upload to PyPI")
    print("")
    
    print(f"{GREEN}Utilities:{NC}")
    print("  show-version      Print the project version")
    print("  help              Display this help")
    print("")
    
    print(f"Usage: {GREEN}python dev.py <command>{NC}")
    return True


def task_venv() -> bool:
    if venv_exists():
        print_warning("Virtual environment already exists.")
        return True

    python_cmd = "python3" if platform.system() != "Windows" else "python"
    print_info("Creating virtual environment...")
    if not run_command([python_cmd, "-m", "venv", str(VENV_DIR)]):
        return False

    print_success(f"Virtual environment created at {VENV_DIR}")
    activation = (
        f"{VENV_DIR}\\Scripts\\activate"
        if platform.system() == "Windows"
        else f"source {VENV_DIR}/bin/activate"
    )
    print_info(f"Activate it with: {activation}")
    return True


def task_install() -> bool:
    if not venv_exists() and not task_venv():
        return False

    print_info("Installing package (production)...")
    if not install_build_dependencies():
        return False

    if not run_command([str(PIP), "install", "."]):
        return False

    print_success("Installation complete.")
    return True


def task_install_dev() -> bool:
    if not venv_exists() and not task_venv():
        return False

    print_info("Installing package (development)...")
    if not install_build_dependencies():
        return False

    if not run_command([str(PIP), "install", "-e", "."]):
        return False

    requirements_dev = PROJECT_ROOT / "requirements-dev.txt"
    if requirements_dev.exists():
        print_info("Installing development dependencies...")
        if not run_command([str(PIP), "install", "-r", str(requirements_dev)]):
            return False

    print_success("Development installation complete.")
    return True


def task_clean_build() -> bool:
    print_info("Removing build artifacts...")
    for directory in ["build", "dist", ".eggs"]:
        path = PROJECT_ROOT / directory
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
            print(f"  Removed {directory}/")

    for egg_info in PROJECT_ROOT.glob("**/*.egg-info"):
        shutil.rmtree(egg_info, ignore_errors=True)
        print(f"  Removed {egg_info}")

    return True


def task_clean_pyc() -> bool:
    print_info("Removing Python bytecode artifacts...")

    for pycache in PROJECT_ROOT.glob("**/__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
        print(f"  Removed {pycache}")

    for pattern in ["**/*.pyc", "**/*.pyo", "**/*~"]:
        for file in PROJECT_ROOT.glob(pattern):
            file.unlink(missing_ok=True)

    return True


def task_clean_test() -> bool:
    print_info("Removing test artifacts...")
    artifacts = [".pytest_cache", ".coverage", "htmlcov", ".mypy_cache", ".ruff_cache"]

    for artifact in artifacts:
        path = PROJECT_ROOT / artifact
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)
            print(f"  Removed {artifact}")

    print_success("Test artifacts removed.")
    return True


def task_clean() -> bool:
    task_clean_build()
    task_clean_pyc()
    task_clean_test()
    print_success("Workspace clean.")
    return True


def _ensure_venv_for_task(task: str) -> bool:
    if not venv_exists():
        print_error(f"Virtual environment not found. Run `python dev.py install-dev` before `{task}`.")
        return False
    return True


def task_test() -> bool:
    if not _ensure_venv_for_task("test"):
        return False

    pytest = VENV_BIN / ("pytest.exe" if platform.system() == "Windows" else "pytest")
    if run_command([str(pytest)]):
        print_success("Tests complete.")
        return True
    return False


def task_test_verbose() -> bool:
    if not _ensure_venv_for_task("test-verbose"):
        return False

    pytest = VENV_BIN / ("pytest.exe" if platform.system() == "Windows" else "pytest")
    if run_command([str(pytest), "-vv"]):
        print_success("Verbose tests complete.")
        return True
    return False


def task_coverage() -> bool:
    if not _ensure_venv_for_task("coverage"):
        return False

    pytest = VENV_BIN / ("pytest.exe" if platform.system() == "Windows" else "pytest")
    if run_command([str(pytest), "--cov=python_companyatlas", "--cov-report=html", "--cov-report=term"]):
        print_success("Coverage report generated in htmlcov/index.html")
        return True
    return False


def task_lint() -> bool:
    if not _ensure_venv_for_task("lint"):
        return False

    ruff = VENV_BIN / ("ruff.exe" if platform.system() == "Windows" else "ruff")
    mypy = VENV_BIN / ("mypy.exe" if platform.system() == "Windows" else "mypy")
    targets = get_code_directories()

    success = True
    if not run_command([str(ruff), "check", *targets]):
        success = False
    if not run_command([str(mypy), *targets]):
        success = False

    if success:
        print_success("Lint checks passed.")
    return success


def task_format() -> bool:
    if not _ensure_venv_for_task("format"):
        return False

    ruff = VENV_BIN / ("ruff.exe" if platform.system() == "Windows" else "ruff")
    targets = get_code_directories()

    if run_command([str(ruff), "format", *targets]):
        print_success("Code formatted.")
        return True
    return False


def task_check() -> bool:
    if not task_lint():
        return False

    ruff = VENV_BIN / ("ruff.exe" if platform.system() == "Windows" else "ruff")
    targets = get_code_directories()

    if run_command([str(ruff), "format", "--check", *targets]):
        print_success("All checks passed.")
        return True
    return False


def task_build() -> bool:
    if not task_clean():
        return False

    if not venv_exists() and not task_venv():
        return False
    if not install_build_dependencies():
        return False
    if not run_command([str(PIP), "install", "--upgrade", "build"]):
        return False

    python_build = VENV_BIN / ("python.exe" if platform.system() == "Windows" else "python")
    if not run_command([str(python_build), "-m", "build"]):
        return False

    dist_dir = PROJECT_ROOT / "dist"
    if dist_dir.exists():
        for file in dist_dir.iterdir():
            size_kb = file.stat().st_size / 1024
            print(f"  {file.name} ({size_kb:.1f} KB)")

    print_success("Build complete (dist/).")
    return True


def task_upload_test() -> bool:
    if not task_build():
        return False

    if not run_command([str(PIP), "install", "--upgrade", "twine"]):
        return False

    twine = VENV_BIN / ("twine.exe" if platform.system() == "Windows" else "twine")
    if not run_command([str(twine), "upload", "--repository", "testpypi", "dist/*"]):
        return False

    print_success("Upload to TestPyPI complete.")
    return True


def task_upload() -> bool:
    if not task_build():
        return False

    print_warning("WARNING: this will publish to PyPI.")
    input("Press Enter to continue, or Ctrl+C to cancel... ")

    if not run_command([str(PIP), "install", "--upgrade", "twine"]):
        return False

    twine = VENV_BIN / ("twine.exe" if platform.system() == "Windows" else "twine")
    if not run_command([str(twine), "upload", "dist/*"]):
        return False

    print_success("Upload to PyPI complete.")
    return True


def task_show_version() -> bool:
    pyproject = PROJECT_ROOT / "pyproject.toml"
    if not pyproject.exists():
        print_error("pyproject.toml not found")
        return False

    try:
        import tomllib
    except ModuleNotFoundError:
        print_error("tomllib not available (Python 3.11+ required)")
        return False

    with pyproject.open("rb") as f:
        data = tomllib.load(f)
    
    version = data.get("project", {}).get("version")
    if version:
        print_info(f"Current version: {version}")
        return True

    print_error("Version not found in pyproject.toml")
    return False


def task_venv_clean() -> bool:
    if venv_exists():
        print_info("Removing existing virtual environment...")
        shutil.rmtree(VENV_DIR, ignore_errors=True)
        print_success("Virtual environment removed.")
    return task_venv()


COMMANDS = {
    "help": task_help,
    "venv": task_venv,
    "install": task_install,
    "install-dev": task_install_dev,
    "venv-clean": task_venv_clean,
    "clean": task_clean,
    "clean-build": task_clean_build,
    "clean-pyc": task_clean_pyc,
    "clean-test": task_clean_test,
    "test": task_test,
    "test-verbose": task_test_verbose,
    "coverage": task_coverage,
    "lint": task_lint,
    "format": task_format,
    "check": task_check,
    "build": task_build,
    "upload-test": task_upload_test,
    "upload": task_upload,
    "show-version": task_show_version,
}


def main(argv: Sequence[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])

    if not args:
        task_help()
        return 0

    command = args[0]
    if command not in COMMANDS:
        print_error(f"Unknown command: {command}")
        print_info("Run `python dev.py help` to list available commands.")
        return 1

    ensure_venv_activation(command)

    try:
        success = COMMANDS[command]()
        return 0 if success else 1
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user.")
        return 130
    except Exception as exc:
        print_error(f"Unexpected error: {exc}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

