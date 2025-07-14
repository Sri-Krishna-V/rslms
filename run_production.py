#!/usr/bin/env python
"""
Production server script for RevSin using Gunicorn with Uvicorn workers.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

# Default settings
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_WORKERS = 4
DEFAULT_WORKER_CLASS = "uvicorn.workers.UvicornWorker"
DEFAULT_LOG_LEVEL = "info"


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run RevSin in production mode")
    parser.add_argument(
        "--host",
        default=os.environ.get("HOST", DEFAULT_HOST),
        help=f"Host to bind to (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", DEFAULT_PORT)),
        help=f"Port to bind to (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=int(os.environ.get("WORKERS", DEFAULT_WORKERS)),
        help=f"Number of worker processes (default: {DEFAULT_WORKERS})",
    )
    parser.add_argument(
        "--worker-class",
        default=os.environ.get("WORKER_CLASS", DEFAULT_WORKER_CLASS),
        help=f"Worker class to use (default: {DEFAULT_WORKER_CLASS})",
    )
    parser.add_argument(
        "--log-level",
        default=os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL),
        choices=["debug", "info", "warning", "error", "critical"],
        help=f"Log level (default: {DEFAULT_LOG_LEVEL})",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload (not recommended for production)",
    )
    parser.add_argument(
        "--access-log",
        action="store_true",
        help="Enable access log",
    )
    parser.add_argument(
        "--log-file",
        default=os.environ.get("LOG_FILE", None),
        help="Log file path (default: stdout)",
    )
    parser.add_argument(
        "--pid-file",
        default=os.environ.get("PID_FILE", None),
        help="PID file path",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run in daemon mode (background)",
    )

    return parser.parse_args()


def build_command(args):
    """Build the Gunicorn command with arguments."""
    cmd = [
        "gunicorn",
        "src.revsin.main:app",
        f"--bind={args.host}:{args.port}",
        f"--workers={args.workers}",
        f"--worker-class={args.worker_class}",
        f"--log-level={args.log_level}",
    ]

    if args.reload:
        cmd.append("--reload")

    if not args.access_log:
        cmd.append("--access-logfile=-")

    if args.log_file:
        cmd.append(f"--log-file={args.log_file}")

    if args.pid_file:
        cmd.append(f"--pid={args.pid_file}")

    if args.daemon:
        cmd.append("--daemon")

    return cmd


def check_gunicorn():
    """Check if Gunicorn is installed."""
    try:
        subprocess.run(["gunicorn", "--version"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def main():
    """Main function to run the production server."""
    # Set environment variable to production
    os.environ["ENVIRONMENT"] = "production"

    # Parse command line arguments
    args = parse_args()

    # Check if Gunicorn is installed
    if not check_gunicorn():
        print("Error: Gunicorn is not installed. Please install it with:")
        print("pip install gunicorn")
        sys.exit(1)

    # Build the command
    cmd = build_command(args)

    # Print the command
    print("Starting RevSin production server with command:")
    print(" ".join(cmd))
    print("\nPress Ctrl+C to stop the server")

    # Run the command
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nServer stopped")


if __name__ == "__main__":
    main()
