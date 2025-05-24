import multiprocessing

import uvicorn
from uvicorn.config import LOGGING_CONFIG

from app.core.app import init_app
from app.core.settings import Settings

settings = Settings()
app = init_app(settings)

if __name__ == "__main__":
    # Configure logging format
    default_log_fmt = "%(levelname)s %(asctime)s: %(message)s"
    access_log_fmt = (
        "%(levelname)s %(asctime)s %(client_addr)s %(status_code)s: %(request_line)s"
    )
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = default_log_fmt
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = access_log_fmt

    # Calculate the number of workers dynamically
    num_workers=1
    if settings.environment != 'local':
        num_cores = multiprocessing.cpu_count()
        num_workers = 2 * num_cores + 1
    # Serve the app with dynamically calculated workers
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.autoreload,
        ws="none",
        workers=num_workers
    )