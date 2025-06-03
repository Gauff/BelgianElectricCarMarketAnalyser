#!/usr/bin/env python3
"""
Unified Development Tools for Electric Car Market Analyzer

This script provides a comprehensive development environment management tool that combines:
- Environment setup and dependency installation
- Code formatting with Black
- Linting with Ruff
- Type checking with MyPy
- VS Code integration

Usage:
    python development.py setup           # Set up development environment
    python development.py format          # Format code with Black
    python development.py lint            # Lint code with Ruff
    python development.py type-check      # Type check with MyPy
    python development.py fix             # Auto-fix formatting and linting issues
    python development.py all             # Run all development tools
    python development.py --help          # Show detailed help

Features:
- Automatic UV/pip detection and fallback
- Support for both pre-installed and on-demand package execution
- Comprehensive error handling and user guidance
- VS Code settings generation
- Installation validation
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


class DevTools:
    """Unified development tools manager."""

    def __init__(self):
        self.use_uv = self._check_command_exists("uv")
        self.use_pip = self._check_command_exists("pip")
        self.project_root = Path.cwd()

    def _check_command_exists(self, command: str) -> bool:
        """Check if a command exists in the system."""
        try:
            subprocess.run([command, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _check_uv_package_exists(self, package: str) -> bool:
        """Check if a package is installed via UV."""
        if not self.use_uv:
            return False
        try:
            subprocess.run(
                ["uv", "run", "python", "-c", f"import {package}"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _run_command(
        self, command: list[str], description: str, check: bool = True
    ) -> bool:
        """Run a command and handle errors."""
        print(f"\n🔧 {description}")
        print(f"Running: {' '.join(command)}")
        print("-" * 50)

        try:
            result = subprocess.run(command, check=check, capture_output=False)
            if result.returncode == 0:
                print(f"✅ {description} completed successfully")
                return True
            else:
                print(f"⚠️  {description} completed with warnings")
                return False
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed with exit code {e.returncode}")
            return False
        except FileNotFoundError:
            print(f"❌ Command not found: {command[0]}")
            if command[0] in ["uv", "pip"]:
                print("Make sure you have a Python package manager installed.")
            else:
                print("Make sure you have installed the development dependencies:")
                print("python development.py setup")
            return False

    def _get_target_paths(self) -> list[str]:
        """Get target paths for development tools."""
        paths = ["src/"]
        # Include root Python files if they exist
        root_py_files = list(self.project_root.glob("*.py"))
        if root_py_files:
            paths.extend([str(f) for f in root_py_files])
        return paths

    def _validate_project_structure(self) -> bool:
        """Validate that we're in the correct project directory."""
        if not (self.project_root / "src").exists():
            print("❌ Error: 'src' directory not found.")
            print("Please run this script from the project root directory.")
            return False
        return True

    def setup(self) -> bool:
        """Set up the development environment."""
        print("🚀 Setting up development environment...")
        print("=" * 60)

        if not self._validate_project_structure():
            return False

        # Install dependencies
        if not self._install_dependencies():
            print("\n❌ Failed to install dependencies. Please check the errors above.")
            return False

        # Validate installation
        if not self._validate_installation():
            print("\n❌ Some development tools are not properly installed.")
            print("Please check the installation and try again.")
            return False

        # Create VS Code settings (optional)
        self._create_vscode_settings()

        print("\n🎉 Development environment setup completed successfully!")
        print("\nNext steps:")
        print("1. Run all development tools:")
        print("   python development.py all")
        print("\n2. Format your code:")
        print("   python development.py format")
        print("\n3. Check for issues:")
        print("   python development.py lint")
        print("\n4. Type check:")
        print("   python development.py type-check")
        print("\n5. Auto-fix issues:")
        print("   python development.py fix")

        return True

    def _install_dependencies(self) -> bool:
        """Install development dependencies using UV or pip."""
        if self.use_uv:
            print("✅ UV detected - using UV for fast package installation")

            # Install production dependencies
            success = self._run_command(
                ["uv", "pip", "install", "-r", "src/requirements.txt"],
                "Installing production dependencies with UV",
            )

            if success:
                # Install development dependencies
                success = self._run_command(
                    ["uv", "pip", "install", "-r", "requirements-dev.txt"],
                    "Installing development dependencies with UV",
                )

            return success

        elif self.use_pip:
            print("⚠️  UV not found - falling back to pip (slower)")
            print(
                "Consider installing UV for faster package management: https://github.com/astral-sh/uv"
            )

            # Install production dependencies
            success = self._run_command(
                ["pip", "install", "-r", "src/requirements.txt"],
                "Installing production dependencies with pip",
            )

            if success:
                # Install development dependencies
                success = self._run_command(
                    ["pip", "install", "-r", "requirements-dev.txt"],
                    "Installing development dependencies with pip",
                )

            return success

        else:
            print("❌ Neither UV nor pip found. Please install Python package manager.")
            return False

    def _validate_installation(self) -> bool:
        """Validate that all development tools are properly installed."""
        print("\n🔍 Validating development tool installation...")

        tools = [
            ("black", "Black code formatter"),
            ("ruff", "Ruff linter"),
            ("mypy", "MyPy type checker"),
        ]

        all_good = True
        for tool, description in tools:
            if self._check_uv_package_exists(tool):
                print(f"✅ {description} is installed")
            else:
                print(f"❌ {description} is NOT installed")
                all_good = False

        return all_good

    def _create_vscode_settings(self) -> bool:
        """Create VS Code settings for the development tools."""
        vscode_dir = self.project_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)

        settings = {
            "python.formatting.provider": "black",
            "python.linting.enabled": True,
            "python.linting.ruffEnabled": True,
            "python.linting.mypyEnabled": True,
            "python.linting.pylintEnabled": False,
            "python.linting.flake8Enabled": False,
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {"source.organizeImports": True},
            "python.defaultInterpreterPath": "./venv/bin/python",
            "[python]": {
                "editor.defaultFormatter": "ms-python.black-formatter",
                "editor.formatOnSave": True,
                "editor.codeActionsOnSave": {"source.organizeImports": True},
            },
        }

        settings_file = vscode_dir / "settings.json"

        try:
            with open(settings_file, "w") as f:
                json.dump(settings, f, indent=2)
            print(f"✅ Created VS Code settings: {settings_file}")
            return True
        except Exception as e:
            print(f"⚠️  Could not create VS Code settings: {e}")
            return False

    def format_code(self) -> bool:
        """Format code with Black."""
        if not self._validate_project_structure():
            return False

        target_paths = self._get_target_paths()

        # Try pre-installed packages first, then fall back to on-demand
        if self.use_uv and self._check_uv_package_exists("black"):
            command = ["uv", "run", "black"] + target_paths
        elif self.use_uv:
            command = ["uv", "run", "--with", "black", "black"] + target_paths
        else:
            command = ["black"] + target_paths

        return self._run_command(command, "Formatting code with Black")

    def lint_code(self) -> bool:
        """Lint code with Ruff."""
        if not self._validate_project_structure():
            return False

        target_paths = self._get_target_paths()
        success = True

        # Run Ruff linting
        if self.use_uv and self._check_uv_package_exists("ruff"):
            command = ["uv", "run", "ruff", "check"] + target_paths
        elif self.use_uv:
            command = ["uv", "run", "--with", "ruff", "ruff", "check"] + target_paths
        else:
            command = ["ruff", "check"] + target_paths

        success &= self._run_command(command, "Linting code with Ruff")

        # Run Ruff formatting check (additional to Black)
        if self.use_uv and self._check_uv_package_exists("ruff"):
            command = ["uv", "run", "ruff", "format", "--check"] + target_paths
        elif self.use_uv:
            command = [
                "uv",
                "run",
                "--with",
                "ruff",
                "ruff",
                "format",
                "--check",
            ] + target_paths
        else:
            command = ["ruff", "format", "--check"] + target_paths

        success &= self._run_command(command, "Checking Ruff formatting")

        return success

    def type_check(self) -> bool:
        """Type check with MyPy."""
        if not self._validate_project_structure():
            return False

        # MyPy typically only checks the src directory
        target_path = "src/"

        if self.use_uv and self._check_uv_package_exists("mypy"):
            command = ["uv", "run", "mypy", target_path]
        elif self.use_uv:
            # Include type stubs for better type checking
            command = [
                "uv",
                "run",
                "--with",
                "mypy",
                "--with",
                "types-requests",
                "--with",
                "types-beautifulsoup4",
                "mypy",
                target_path,
            ]
        else:
            command = ["mypy", target_path]

        return self._run_command(command, "Type checking with MyPy")

    def fix_code(self) -> bool:
        """Auto-fix code issues where possible."""
        if not self._validate_project_structure():
            return False

        target_paths = self._get_target_paths()
        success = True

        # Format with Black
        if self.use_uv and self._check_uv_package_exists("black"):
            command = ["uv", "run", "black"] + target_paths
        elif self.use_uv:
            command = ["uv", "run", "--with", "black", "black"] + target_paths
        else:
            command = ["black"] + target_paths

        success &= self._run_command(command, "Auto-formatting with Black")

        # Auto-fix with Ruff
        if self.use_uv and self._check_uv_package_exists("ruff"):
            command = ["uv", "run", "ruff", "check", "--fix"] + target_paths
        elif self.use_uv:
            command = [
                "uv",
                "run",
                "--with",
                "ruff",
                "ruff",
                "check",
                "--fix",
            ] + target_paths
        else:
            command = ["ruff", "check", "--fix"] + target_paths

        success &= self._run_command(command, "Auto-fixing issues with Ruff")

        return success

    def run_all(self) -> bool:
        """Run all development tools."""
        print("🚀 Running all development tools...")

        success = True
        success &= self.format_code()
        success &= self.lint_code()
        success &= self.type_check()

        if success:
            print("\n🎉 All development tools completed successfully!")
        else:
            print("\n⚠️  Some tools reported issues. Please review the output above.")

        return success


def main():
    """Main entry point for the development tools."""
    parser = argparse.ArgumentParser(
        description="Unified Development Tools for Electric Car Market Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python development.py setup         # Set up development environment
  python development.py format        # Format code with Black
  python development.py lint          # Lint code with Ruff
  python development.py type-check    # Type check with MyPy
  python development.py fix           # Auto-fix formatting and linting issues
  python development.py all           # Run all development tools

Features:
  - Automatic UV/pip detection and fallback
  - Support for both pre-installed and on-demand package execution
  - Comprehensive error handling and user guidance
  - VS Code settings generation
  - Installation validation

Backward Compatibility:
  This script replaces and consolidates the functionality of:
  - setup-dev.py (use: python development.py setup)
  - dev-tools.py (use: python development.py <command>)
  - run-dev-tools.py (use: python development.py <command>)
        """,
    )

    parser.add_argument(
        "command",
        choices=["setup", "format", "lint", "type-check", "fix", "all"],
        help="Development operation to perform",
    )

    parser.add_argument(
        "--version", action="version", version="Development Tools v2.0.0 (Consolidated)"
    )

    args = parser.parse_args()

    # Initialize the development tools manager
    dev_tools = DevTools()

    # Map commands to methods
    command_map = {
        "setup": dev_tools.setup,
        "format": dev_tools.format_code,
        "lint": dev_tools.lint_code,
        "type-check": dev_tools.type_check,
        "fix": dev_tools.fix_code,
        "all": dev_tools.run_all,
    }

    # Execute the requested command
    try:
        success = command_map[args.command]()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue if it persists.")
        sys.exit(1)


if __name__ == "__main__":
    main()
