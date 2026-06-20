#!/usr/bin/env python3
"""
Podar LMS — Local Development Setup Script
Run: python setup_local.py

This script:
1. Creates a Python virtual environment
2. Installs backend dependencies
3. Sets up SQLite database (no PostgreSQL needed)
4. Creates sample data
5. Installs frontend dependencies
6. Starts both servers

Requirements: Python 3.10+ and Node.js 18+
"""
import subprocess
import sys
import os
import platform
import shutil

# Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def log(msg, color=GREEN):
    print(f"\n{color}{BOLD}{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}{RESET}\n")

def run(cmd, cwd=None, check=True):
    print(f"  {CYAN}→ {cmd}{RESET}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=False)
    if check and result.returncode != 0:
        print(f"  {RED}✗ Command failed!{RESET}")
        return False
    return True

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    backend = os.path.join(root, "backend")
    frontend = os.path.join(root, "frontend")
    is_windows = platform.system() == "Windows"

    print(f"""
{CYAN}{BOLD}
  ╔══════════════════════════════════════════╗
  ║         PODAR LMS — LOCAL SETUP         ║
  ║     No Docker · No PostgreSQL needed    ║
  ╚══════════════════════════════════════════╝
{RESET}""")

    # ── Check Python ──
    log("Step 1/6: Checking Python...", YELLOW)
    py_version = sys.version_info
    print(f"  Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version < (3, 10):
        print(f"  {RED}✗ Python 3.10+ required. Please upgrade.{RESET}")
        sys.exit(1)
    print(f"  {GREEN}✓ Python OK{RESET}")

    # ── Check Node.js ──
    log("Step 2/6: Checking Node.js...", YELLOW)
    if shutil.which("node") is None:
        print(f"  {RED}✗ Node.js not found!")
        print(f"  Download from: https://nodejs.org/ (LTS version){RESET}")
        sys.exit(1)
    run("node --version")
    print(f"  {GREEN}✓ Node.js OK{RESET}")

    # ── Create venv ──
    log("Step 3/6: Setting up Python virtual environment...", YELLOW)
    venv_path = os.path.join(backend, "venv")
    if not os.path.exists(venv_path):
        run(f"{sys.executable} -m venv venv", cwd=backend)
    
    if is_windows:
        pip = os.path.join(venv_path, "Scripts", "pip.exe")
        python = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        pip = os.path.join(venv_path, "bin", "pip")
        python = os.path.join(venv_path, "bin", "python")

    # ── Install backend dependencies ──
    log("Step 4/6: Installing backend dependencies...", YELLOW)
    run(f'"{pip}" install --upgrade pip', cwd=backend)
    
    # Install a lighter requirements set (skip postgres, redis, channels for local dev)
    light_reqs = os.path.join(backend, "requirements_local.txt")
    if not os.path.exists(light_reqs):
        with open(light_reqs, "w") as f:
            f.write("""Django==4.2.11
djangorestframework==3.15.1
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
django-filter==24.2
django-environ==0.11.2
django-extensions==3.2.3
drf-spectacular==0.27.2
Pillow==10.3.0
reportlab==4.2.0
qrcode==7.4.2
""")
    
    run(f'"{pip}" install -r requirements_local.txt', cwd=backend)

    # ── Create local .env ──
    env_file = os.path.join(backend, ".env")
    with open(env_file, "w") as f:
        f.write("""SECRET_KEY=local-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
FRONTEND_URL=http://localhost:5173
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
""")
    print(f"  {GREEN}✓ Created .env for local development{RESET}")

    # ── Run migrations & seed ──
    log("Step 5/6: Setting up database...", YELLOW)
    run(f'"{python}" manage.py migrate', cwd=backend)
    run(f'"{python}" manage.py seed', cwd=backend)

    # ── Install frontend ──
    log("Step 6/6: Installing frontend dependencies...", YELLOW)
    
    # Create frontend .env
    fe_env = os.path.join(frontend, ".env")
    with open(fe_env, "w") as f:
        f.write("VITE_API_URL=http://localhost:8000/api/v1\n")
    
    run("npm install", cwd=frontend)

    # ── Done! ──
    print(f"""
{GREEN}{BOLD}
  ╔══════════════════════════════════════════╗
  ║          ✓ SETUP COMPLETE!              ║
  ╚══════════════════════════════════════════╝
{RESET}
  {BOLD}To start the app, open TWO terminals:{RESET}

  {CYAN}Terminal 1 — Backend:{RESET}
    cd backend
    {"venv\\Scripts\\python" if is_windows else "venv/bin/python"} manage.py runserver

  {CYAN}Terminal 2 — Frontend:{RESET}
    cd frontend
    npm run dev

  {BOLD}Then open:{RESET}
    🌐  http://localhost:5173

  {BOLD}Login credentials:{RESET}
    👤  Student:   student1@podar-lms.io / student123
    👨‍🏫  Lecturer:  lecturer1@podar-lms.io / lecturer123
    🔑  Admin:     admin@podar-lms.io / admin123

  {BOLD}API Docs:{RESET}
    📄  http://localhost:8000/api/docs/
""")

if __name__ == "__main__":
    main()
