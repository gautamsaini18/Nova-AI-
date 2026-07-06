"""Nova AI — Vercel Serverless Entry Point"""

import sys
from pathlib import Path

# Add repo root to sys.path so that 'from backend.main import app' works.
# Vercel project root must be set to 'backend/' directory in project settings.
_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from backend.main import app

# Vercel ASGI handler — Vercel auto-detects the 'app' variable
handler = app
