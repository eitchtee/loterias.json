"""
Orchestrator for Loterias data collection services.
Iterates over all service modules in the services folder and calls their main() function.
"""

import importlib.util
import logging
import os
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_and_run_service(service_path: Path) -> bool:
    """
    Dynamically load a service module and execute its main() function.

    Args:
        service_path: Path to the service Python file.

    Returns:
        True if the service ran successfully, False otherwise.
    """
    service_name = service_path.stem
    logger.info(f"Running service: {service_name}")

    try:
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(service_name, service_path)
        if spec is None or spec.loader is None:
            logger.error(f"Failed to load spec for {service_name}")
            return False

        module = importlib.util.module_from_spec(spec)
        sys.modules[service_name] = module
        spec.loader.exec_module(module)

        # Check if main() exists
        if not hasattr(module, "main"):
            logger.warning(f"Service {service_name} has no main() function, skipping")
            return False

        # Execute main()
        module.main()
        logger.info(f"Service {service_name} completed successfully")
        return True

    except Exception as e:
        logger.error(f"Service {service_name} failed with error: {e}", exc_info=True)
        # Check if running in GitHub Actions to show a workflow warning
        if os.getenv("GITHUB_ACTIONS") == "true":
            print(
                f"::warning title=Service Failure::Service {service_name} failed: {e}"
            )
        return False


def run_all_services():
    """
    Discover and run all service modules in the services folder.
    """
    services_dir = Path(__file__).parent / "services"

    if not services_dir.exists():
        logger.error(f"Services directory not found: {services_dir}")
        return

    # Add services directory to path for imports
    if str(services_dir) not in sys.path:
        sys.path.insert(0, str(services_dir))

    # Find all Python files in services (excluding __init__.py, base.py, and __pycache__)
    service_files = sorted(
        [
            f
            for f in services_dir.glob("*.py")
            if f.stem not in ("__init__", "base") and not f.stem.startswith("_")
        ]
    )

    if not service_files:
        logger.warning("No service files found in services directory")
        return

    logger.info(f"Found {len(service_files)} service(s) to run")

    results = {"success": 0, "failed": 0}

    for service_path in service_files:
        if load_and_run_service(service_path):
            results["success"] += 1
        else:
            results["failed"] += 1

    logger.info(
        f"Execution complete. Success: {results['success']}, Failed: {results['failed']}"
    )


if __name__ == "__main__":
    run_all_services()
