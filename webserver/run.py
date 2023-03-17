from pathlib import Path
import sys

import uvicorn

if __name__ == "__main__":
    current = Path(__file__)
    sys.path.insert(0, str(current.parent.parent.absolute()))
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info",
        workers=16
    )
