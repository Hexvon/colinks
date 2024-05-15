import logging
import sys

import uvicorn

from colinks_backend.config import CONFIG

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if CONFIG.debug_logs else logging.INFO)

if __name__ == "__main__":
    uvicorn.run("colinks_backend.app:app", host="0.0.0.0", reload=True, log_level="debug", port=8000)
