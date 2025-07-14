"""
System commands for the Library Management System CLI

This module provides CLI commands for system administration tasks including:
- Database initialization and management
- System health checks
- Cache management
- System information display
- Backup guidance

These commands are intended for system administrators and developers
to manage and monitor the Library Management System.
"""

import click
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

from ..utils import (
    handle_errors, get_db_session, print_success, print_error, print_info,
    print_warning, print_celebration, confirm_action, with_progress,
    console, display_stats_panel, print_ascii_art, create_interactive_menu
)
from ...database.connection import init_db, engine
from ...database.redis_client import cache
from ...config import settings


@click.group()
def system():
    """
    System management commands

    This group contains commands for managing system-level operations
    such as database initialization, health checks, and cache management.

    Examples:
        revsin system health          # Check system health
        revsin system init-db         # Initialize the database
        revsin system clear-cache     # Clear the Redis cache
    """
    pass


@system.command()
@handle_errors
def init_db():
    """
    Initialize the database

    This command creates all database tables defined in the models.
    It should be run when setting up the system for the first time
    or after a database reset.

    The command will ask for confirmation before proceeding.

    Example:
        revsin system init-db
    """
    if not confirm_action("This will initialize the database. Continue?"):
        return

    with with_progress("Initializing database tables..."):
        try:
            init_db()
            print_celebration("Database initialized successfully!")
            print_ascii_art("success")
        except Exception as e:
            print_error(f"Failed to initialize database: {str(e)}")
            raise


@system.command()
@handle_errors
def health():
    """
    Check system health

    This command performs a comprehensive health check of the system:
    - Tests database connectivity
    - Tests Redis cache connectivity
    - Displays current configuration settings

    Use this command to verify that all system components are working correctly.

    Example:
        revsin system health
    """
    print_info("Performing comprehensive system health check...")

    health_status = {}
    overall_healthy = True

    # Check database connection
    try:
        with get_db_session() as db:
            result = db.execute(text("SELECT 1")).scalar()
            if result == 1:
                print_success("Database connection: Healthy")
                health_status["Database"] = "✅ Connected"
            else:
                raise Exception("Unexpected result from database")
    except SQLAlchemyError as e:
        print_error(f"Database connection: Failed - {str(e)}")
        health_status["Database"] = "❌ Failed"
        overall_healthy = False

    # Check Redis connection
    try:
        cache.ping()
        print_success("Redis connection: Healthy")
        health_status["Redis Cache"] = "✅ Connected"
    except Exception as e:
        print_error(f"Redis connection: Failed - {str(e)}")
        health_status["Redis Cache"] = "❌ Failed"
        overall_healthy = False

    # Display system info
    system_info = {
        "Environment": settings.environment,
        "Debug Mode": "✅ Enabled" if settings.debug else "❌ Disabled",
        "Database": "PostgreSQL",
        "Cache": "Redis",
        "Host": settings.host,
        "Port": str(settings.port)
    }

    # Get database statistics if healthy
    if health_status.get("Database") == "✅ Connected":
        try:
            with get_db_session() as db:
                users_count = db.execute(
                    text("SELECT COUNT(*) FROM users")).scalar()
                books_count = db.execute(
                    text("SELECT COUNT(*) FROM books")).scalar()
                loans_count = db.execute(
                    text("SELECT COUNT(*) FROM loans")).scalar()

                db_stats = {
                    "Total Users": users_count,
                    "Total Books": books_count,
                    "Total Loans": loans_count
                }
                display_stats_panel("Database Statistics", db_stats)
        except SQLAlchemyError:
            print_warning("Could not retrieve database statistics")

    # Display overall health status
    display_stats_panel("System Health", health_status)
    display_stats_panel("System Configuration", system_info)

    if overall_healthy:
        print_celebration("All systems are healthy and operational!")
        print_ascii_art("success")
    else:
        print_error(
            "Some systems are experiencing issues. Please check the details above.")


@system.command()
@handle_errors
def clear_cache():
    """
    Clear Redis cache

    This command flushes all data from the Redis cache.
    Use this when you want to force the system to reload data from the database,
    or if you suspect the cache contains stale or corrupted data.

    The command will ask for confirmation before proceeding.

    Example:
        revsin system clear-cache
    """
    if not confirm_action("This will clear all cached data. Continue?"):
        return

    with with_progress("Clearing Redis cache..."):
        try:
            cache.flushall()
            print_success("Cache cleared successfully!")
        except Exception as e:
            print_error(f"Failed to clear cache: {str(e)}")
            raise


@system.command()
@handle_errors
def info():
    """
    Display system information

    This command displays comprehensive information about the system:
    - Version information
    - Environment settings
    - Database statistics (user count, book count, loan count)

    Use this command to get a quick overview of the system status.

    Example:
        revsin system info
    """
    print_info("Library Management System - RevSin CLI")

    # System Information
    system_info = {
        "Version": "1.0.0",
        "Environment": settings.environment,
        "Debug Mode": "Enabled" if settings.debug else "Disabled",
        "Database Type": "PostgreSQL",
        "Cache Type": "Redis",
        "Host": settings.host,
        "Port": settings.port,
        "Workers": settings.workers
    }

    display_stats_panel("System Information", system_info)

    # Database stats
    try:
        with get_db_session() as db:
            # Get table counts
            users_count = db.execute(
                text("SELECT COUNT(*) FROM users")).scalar()
            books_count = db.execute(
                text("SELECT COUNT(*) FROM books")).scalar()
            loans_count = db.execute(
                text("SELECT COUNT(*) FROM loans")).scalar()

            # Get more detailed stats
            active_loans = db.execute(
                text("SELECT COUNT(*) FROM loans WHERE status = 'active'")
            ).scalar()
            overdue_loans = db.execute(
                text("SELECT COUNT(*) FROM loans WHERE status = 'overdue'")
            ).scalar()

            db_stats = {
                "Total Users": users_count,
                "Total Books": books_count,
                "Total Loans": loans_count,
                "Active Loans": active_loans,
                "Overdue Loans": overdue_loans
            }

            display_stats_panel("Database Statistics", db_stats)
    except SQLAlchemyError:
        print_warning("Could not retrieve database statistics")


@system.command()
@handle_errors
def reset_db():
    """
    Reset database (WARNING: This will delete all data!)

    This command completely resets the database by:
    1. Dropping all existing tables
    2. Recreating the tables from the models
    3. Clearing the Redis cache

    WARNING: This will permanently delete all data in the database!
    The command requires double confirmation to proceed.

    Use this command only in development or when you need to start
    with a clean database.

    Example:
        revsin system reset-db
    """
    console.print(
        "[red]⚠️  WARNING: This will delete ALL data in the database! ⚠️[/red]")

    if not confirm_action("Are you absolutely sure you want to reset the database?"):
        return

    # Double confirmation
    if not confirm_action("This action cannot be undone. Continue?"):
        return

    with with_progress("Resetting database (dropping tables)..."):
        try:
            # Drop all tables
            from ...models.base import Base
            Base.metadata.drop_all(bind=engine)
            print_info("Tables dropped")
        except Exception as e:
            print_error(f"Failed to drop tables: {str(e)}")
            raise

    with with_progress("Recreating database tables..."):
        try:
            # Recreate tables
            init_db()
            print_info("Tables recreated")
        except Exception as e:
            print_error(f"Failed to recreate tables: {str(e)}")
            raise

    with with_progress("Clearing cache..."):
        try:
            # Clear cache
            cache.flushall()
            print_info("Cache cleared")
        except Exception as e:
            print_error(f"Failed to clear cache: {str(e)}")
            raise

    print_celebration("Database reset completed successfully!")
    print_ascii_art("complete")


@system.command()
@click.option('--table', help='Specific table to check (e.g., users, books, loans)')
@handle_errors
def check_tables(table):
    """
    Check database tables

    This command checks the existence and record count of database tables.
    It can check either a specific table (if specified) or all main tables.

    Use this command to verify that tables exist and contain the expected
    number of records.

    Options:
        --table TEXT  Specific table to check (e.g., users, books, loans)

    Examples:
        revsin system check-tables           # Check all tables
        revsin system check-tables --table users  # Check only the users table
    """
    with get_db_session() as db:
        if table:
            # Check specific table
            try:
                result = db.execute(
                    text(f"SELECT COUNT(*) FROM {table}")).scalar()
                table_stats = {f"Table '{table}'": f"{result} records"}
                display_stats_panel("Table Check", table_stats)
            except SQLAlchemyError as e:
                print_error(f"Table '{table}' check failed: {str(e)}")
        else:
            # Check all tables
            tables = ['users', 'books', 'loans']
            table_stats = {}

            for table_name in tables:
                try:
                    result = db.execute(
                        text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
                    table_stats[f"Table '{table_name}'"] = f"{result} records"
                except SQLAlchemyError as e:
                    table_stats[f"Table '{table_name}'"] = f"❌ Error: {str(e)}"

            display_stats_panel("Database Tables", table_stats)


@system.command()
@handle_errors
def backup_info():
    """
    Display backup information and recommendations

    This command provides information about how to back up and restore
    the PostgreSQL database used by the system.

    It includes:
    - Recommended backup tools
    - Example backup commands
    - Example restore commands

    Note: This command does not perform backups; it only provides guidance.

    Example:
        revsin system backup-info
    """
    backup_info = {
        "Database Type": "PostgreSQL",
        "Recommended Tool": "pg_dump",
        "Alternative Tool": "pg_dumpall (for all databases)"
    }

    display_stats_panel("Backup Information", backup_info)

    console.print("\n📋 Example Commands:", style="bold cyan")
    console.print("─" * 20)
    console.print("Backup:")
    console.print(
        "  pg_dump -h hostname -U username -d database_name > backup.sql", style="green")
    console.print("\nRestore:")
    console.print(
        "  psql -h hostname -U username -d database_name < backup.sql", style="green")
    console.print(
        "\n⚠️ Note: Replace hostname, username, and database_name with your actual values", style="yellow")


@system.command()
@click.option('--days', default=30, help='Number of days of logs to keep')
@handle_errors
def rotate_logs(days):
    """
    Rotate and clean up log files

    This command rotates log files and removes logs older than the specified
    number of days. It helps manage disk space by removing old log files.

    Options:
        --days INTEGER  Number of days of logs to keep (default: 30)

    Example:
        revsin system rotate-logs          # Keep 30 days of logs
        revsin system rotate-logs --days 7  # Keep only 7 days of logs
    """
    import os
    import time

    print_info(f"Rotating logs and removing logs older than {days} days")

    log_dir = "logs"
    if not os.path.exists(log_dir):
        print_warning("No logs directory found")
        return

    with with_progress("Processing log files..."):
        try:
            # Calculate cutoff time
            cutoff = time.time() - (days * 86400)  # days in seconds

            # Check all files in logs directory
            count = 0
            for filename in os.listdir(log_dir):
                filepath = os.path.join(log_dir, filename)

                # Check if it's a file and older than cutoff
                if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff:
                    os.remove(filepath)
                    count += 1

            result_stats = {
                "Log Directory": log_dir,
                "Retention Period": f"{days} days",
                "Files Removed": count
            }

            display_stats_panel("Log Rotation Results", result_stats)

            if count > 0:
                print_success(
                    f"Removed {count} log files older than {days} days")
            else:
                print_info("No old log files found to remove")

        except Exception as e:
            print_error(f"Failed to rotate logs: {str(e)}")
            raise


@system.command()
@handle_errors
def interactive():
    """
    Interactive system management menu

    Provides a user-friendly menu interface for common system operations.
    """
    print_ascii_art("welcome")

    while True:
        options = [
            "🔍 Check System Health",
            "🗃️  Initialize Database",
            "🧹 Clear Cache",
            "📊 Show System Info",
            "🔄 Reset Database (Danger)",
            "🚪 Exit"
        ]

        choice = create_interactive_menu("System Management", options)

        if choice == 0:  # Health check
            health.callback()
        elif choice == 1:  # Init DB
            init_db.callback()
        elif choice == 2:  # Clear cache
            clear_cache.callback()
        elif choice == 3:  # System info
            info.callback()
        elif choice == 4:  # Reset DB
            reset_db.callback()
        elif choice == 5:  # Exit
            print_info("Goodbye! 👋")
            break

        console.print("\n" + "─" * 50)


if __name__ == "__main__":
    system()
