import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
raise SystemExit(subprocess.run([sys.executable,'-m','pytest','tests/conformance','-q'],cwd=ROOT).returncode)
