from pathlib import Path
import sys

PROJECT_PATH = Path(__file__).parent.parent.absolute()
assert str(PROJECT_PATH / "src") not in sys.path
sys.path.append(str(PROJECT_PATH / "src"))

sys.dont_write_bytecode = True
