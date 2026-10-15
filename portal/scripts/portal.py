"""Portable local setup/check/build/serve CLI. No AI provider dependency."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PortalError(RuntimeError):
    pass


def environment_python(root: Path, platform: str | None = None) -> Path:
    kind = platform or sys.platform
    return root / ".venv" / ("Scripts/python.exe" if kind == "win32" else "bin/python")


def run_command(args: list[str], root: Path) -> None:
    result = subprocess.run(args, cwd=root, check=False)
    if result.returncode:
        raise PortalError(f"Command failed with exit code {result.returncode}: {args[0]}")


def require_environment(root: Path) -> Path:
    env = root / ".venv"
    if env.is_symlink() or not env.resolve().is_relative_to(root.resolve()):
        raise PortalError("Refusing a virtual environment outside the portal directory.")
    executable = environment_python(root)
    if not executable.is_file() or not (env / "pyvenv.cfg").is_file():
        raise PortalError("Local environment is missing/incomplete. Run setup; do not install globally.")
    return executable


def setup(root: Path) -> None:
    if sys.version_info < (3, 11):
        raise PortalError("Python 3.11+ required. Ask before installing a global interpreter.")
    env = root / ".venv"
    if env.is_symlink() or not env.resolve().is_relative_to(root.resolve()):
        raise PortalError("Refusing an environment outside the portal directory.")
    if not (root / "requirements-docs.txt").is_file():
        raise PortalError("requirements-docs.txt is missing.")
    if env.exists():
        executable = require_environment(root)
    else:
        run_command([sys.executable, "-m", "venv", str(env)], root)
        executable = require_environment(root)
    run_command([str(executable), "-m", "pip", "install", "--disable-pip-version-check",
                 "-r", str(root / "requirements-docs.txt")], root)
    print("Local setup complete. Next: python scripts/portal.py check")


def port_number(value: str) -> int:
    try:
        port = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Port must be an integer.") from exc
    if not 1024 <= port <= 65535:
        raise argparse.ArgumentTypeError("Use a port from 1024 to 65535.")
    return port


def mkdocs_command(executable: Path, action: str, port: int = 8000, open_browser: bool = False) -> list[str]:
    args = [str(executable), "-m", "mkdocs", action, "--strict"]
    if action == "serve":
        args += ["--dev-addr", f"127.0.0.1:{port}"]
        if open_browser:
            args.append("--open")
    return args


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    for action in ("setup", "check", "build"):
        commands.add_parser(action)
    serve = commands.add_parser("serve")
    serve.add_argument("--port", type=port_number, default=8000)
    serve.add_argument("--open", action="store_true", dest="open_browser")
    options = parser.parse_args(argv)
    try:
        if options.action == "setup":
            setup(ROOT)
        else:
            executable = require_environment(ROOT)
            run_command([str(executable), str(ROOT / "scripts/check_portal.py")], ROOT)
            if options.action in {"build", "serve"}:
                if options.action == "serve":
                    print(f"Portal: http://127.0.0.1:{options.port} (Ctrl+C to stop)", flush=True)
                run_command(mkdocs_command(executable, options.action,
                            getattr(options, "port", 8000), getattr(options, "open_browser", False)), ROOT)
        return 0
    except (PortalError, OSError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
