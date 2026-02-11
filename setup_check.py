"""Setup validation and initial configuration script."""
import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check Python version is 3.12+."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        print("❌ Python 3.12+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True


def check_postgres():
    """Check PostgreSQL is installed."""
    try:
        subprocess.run(
            ["psql", "--version"],
            capture_output=True,
            check=True,
        )
        print("✅ PostgreSQL found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  PostgreSQL not found (required for local setup)")
        return False


def check_docker():
    """Check Docker is installed."""
    try:
        subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            check=True,
        )
        print("✅ Docker found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Docker not found (optional)")
        return False


def check_env_file():
    """Check .env file exists."""
    env_path = Path("backend/.env")
    if env_path.exists():
        print("✅ .env file exists")
        return True
    else:
        print("⚠️  .env file missing (copy from .env.example)")
        return False


def check_requirements():
    """Check requirements.txt exists."""
    req_path = Path("backend/requirements.txt")
    if req_path.exists():
        print("✅ requirements.txt found")
        return True
    else:
        print("❌ requirements.txt missing")
        return False


def main():
    """Run all checks."""
    print("\n🔍 Text to SQL - Setup Validation\n")
    print("-" * 50)

    checks = [
        ("Python Version", check_python_version),
        ("PostgreSQL", check_postgres),
        ("Docker", check_docker),
        ("Environment File", check_env_file),
        ("Requirements", check_requirements),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        result = check_func()
        results.append((name, result))

    print("\n" + "-" * 50)
    print("\n📋 Summary:\n")

    required_passed = all(r[1] for r in results[:3])
    print(f"✅ Required checks: {sum(1 for _, r in results[:3] if r)}/3")

    if required_passed or check_docker():
        print("\n🚀 You're ready to start!")
        print("\nNext steps:")
        print("1. Set up .env file: cp backend/.env.example backend/.env")
        print("2. Add GEMINI_API_KEY to .env")
        print("3. Start backend: docker-compose up -d")
        print("4. Visit: http://localhost:8000/docs")
    else:
        print("\n⚠️  Please install missing requirements")

    print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()
