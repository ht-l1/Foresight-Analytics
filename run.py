import sys
from pathlib import Path

root_dir = Path(__file__).parent
sys.path.append(str(root_dir))

from app.main import main

if __name__ == "__main__":
    main()