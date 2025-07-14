"""
Main CLI entry point for the Library Management System
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .commands.system import system
from .commands.users import users
from .commands.books import books
from .commands.loans import loans
from .utils import print_info, print_error
from ..config import settings

console = Console()

# ASCII Art Banner
BANNER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ██████╗ ███████╗██╗   ██╗███████╗██╗███╗   ██╗                         ║
║    ██╔══██╗██╔════╝██║   ██║██╔════╝██║████╗  ██║                         ║
║    ██████╔╝█████╗  ██║   ██║███████╗██║██╔██╗ ██║                         ║
║    ██╔══██╗██╔══╝  ╚██╗ ██╔╝╚════██║██║██║╚██╗██║                         ║
║    ██║  ██║███████╗ ╚████╔╝ ███████║██║██║ ╚████║                         ║
║    ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝╚═╝  ╚═══╝                         ║
║                                                                              ║
║                    Library Management System CLI                             ║
║                           Version 1.0.0                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


def print_banner():
    """Print the CLI banner"""
    console.print(BANNER, style="cyan")


def print_welcome():
    """Print welcome message"""
    welcome_text = Text()
    welcome_text.append("Welcome to the ", style="white")
    welcome_text.append("Library Management System CLI", style="bold cyan")
    welcome_text.append("!\n\n", style="white")
    welcome_text.append(
        "This CLI provides comprehensive management tools for:\n", style="white")
    welcome_text.append("  • ", style="yellow")
    welcome_text.append("Users", style="bold green")
    welcome_text.append(
        " - Create, manage, and search library users\n", style="white")
    welcome_text.append("  • ", style="yellow")
    welcome_text.append("Books", style="bold green")
    welcome_text.append(
        " - Add, update, and organize book inventory\n", style="white")
    welcome_text.append("  • ", style="yellow")
    welcome_text.append("Loans", style="bold green")
    welcome_text.append(
        " - Handle book borrowing, returns, and renewals\n", style="white")
    welcome_text.append("  • ", style="yellow")
    welcome_text.append("System", style="bold green")
    welcome_text.append(
        " - Database management and health monitoring\n\n", style="white")
    welcome_text.append("Use ", style="white")
    welcome_text.append("revsin --help", style="bold yellow")
    welcome_text.append(" or ", style="white")
    welcome_text.append("revsin <command> --help", style="bold yellow")
    welcome_text.append(" for detailed usage information.", style="white")

    panel = Panel(welcome_text, title="Getting Started", border_style="blue")
    console.print(panel)


@click.group()
@click.version_option(version="1.0.0", prog_name="RevSin CLI")
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--quiet', '-q', is_flag=True, help='Suppress non-error output')
@click.pass_context
def cli(ctx, verbose, quiet):
    """
    Library Management System CLI

    A comprehensive command-line interface for managing library operations
    including users, books, loans, and system administration.

    \b
    Examples:
        revsin users list                    # List all users
        revsin books search "python"         # Search for books containing "python"
        revsin loans create --user-id 1 --book-id 2   # Create a new loan
        revsin system health                 # Check system health

    \b
    Environment:
        The CLI respects the following environment variables:
        - DATABASE_URL: PostgreSQL connection string
        - REDIS_URL: Redis connection string
        - SECRET_KEY: JWT secret key
        - ENVIRONMENT: Application environment (development/production)
    """
    # Store context for subcommands
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet

    # Set up logging based on options
    if verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    elif quiet:
        import logging
        logging.basicConfig(level=logging.ERROR)


@cli.command()
@click.pass_context
def version(ctx):
    """Show version information"""
    print_info("Library Management System CLI")
    console.print(f"Version: 1.0.0")
    console.print(f"Environment: {settings.environment}")
    console.print(f"Debug mode: {settings.debug}")


@cli.command()
@click.pass_context
def welcome(ctx):
    """Show welcome message and getting started guide"""
    if not ctx.obj.get('quiet'):
        print_banner()
        print_welcome()


@cli.command()
@click.pass_context
def examples(ctx):
    """Show usage examples"""
    examples_text = Text()
    examples_text.append("Common CLI Usage Examples:\n\n", style="bold white")

    # System commands
    examples_text.append("System Management:\n", style="bold cyan")
    examples_text.append("  revsin system health", style="green")
    examples_text.append(
        "                    # Check system health\n", style="dim")
    examples_text.append("  revsin system init-db", style="green")
    examples_text.append(
        "                  # Initialize database\n", style="dim")
    examples_text.append("  revsin system info", style="green")
    examples_text.append(
        "                     # Show system information\n\n", style="dim")

    # User commands
    examples_text.append("User Management:\n", style="bold cyan")
    examples_text.append("  revsin users create", style="green")
    examples_text.append(
        "                      # Create a new user (interactive)\n", style="dim")
    examples_text.append("  revsin users list --role member", style="green")
    examples_text.append("         # List all members\n", style="dim")
    examples_text.append("  revsin users search 'john'", style="green")
    examples_text.append(
        "            # Search for users named 'john'\n", style="dim")
    examples_text.append("  revsin users show 1", style="green")
    examples_text.append(
        "                     # Show user details\n\n", style="dim")

    # Book commands
    examples_text.append("Book Management:\n", style="bold cyan")
    examples_text.append("  revsin books add", style="green")
    examples_text.append(
        "                        # Add a new book (interactive)\n", style="dim")
    examples_text.append("  revsin books list --available-only", style="green")
    examples_text.append("     # List available books\n", style="dim")
    examples_text.append(
        "  revsin books search 'python programming'", style="green")
    examples_text.append(" # Search books\n", style="dim")
    examples_text.append(
        "  revsin books by-author 'Robert Martin'", style="green")
    examples_text.append("   # Books by author\n\n", style="dim")

    # Loan commands
    examples_text.append("Loan Management:\n", style="bold cyan")
    examples_text.append(
        "  revsin loans create --user-id 1 --book-id 2", style="green")
    examples_text.append(" # Create loan\n", style="dim")
    examples_text.append("  revsin loans active", style="green")
    examples_text.append(
        "                     # Show active loans\n", style="dim")
    examples_text.append("  revsin loans overdue", style="green")
    examples_text.append(
        "                    # Show overdue loans\n", style="dim")
    examples_text.append("  revsin loans return-book 1", style="green")
    examples_text.append("             # Return a book\n", style="dim")
    examples_text.append("  revsin loans renew 1", style="green")
    examples_text.append("                   # Renew a loan\n\n", style="dim")

    # Advanced examples
    examples_text.append("Advanced Usage:\n", style="bold cyan")
    examples_text.append(
        "  revsin books add --isbn '978-0134685991' --title 'Effective Java'", style="green")
    examples_text.append("\n", style="dim")
    examples_text.append(
        "  revsin users update 1 --role librarian --active", style="green")
    examples_text.append("\n", style="dim")
    examples_text.append("  revsin loans by-user 1 --limit 20", style="green")
    examples_text.append("\n", style="dim")
    examples_text.append("  revsin system clear-cache", style="green")
    examples_text.append("\n\n", style="dim")

    examples_text.append(
        "For detailed help on any command, use:", style="white")
    examples_text.append("\n  revsin <command> --help", style="bold yellow")

    panel = Panel(examples_text, title="Usage Examples", border_style="green")
    console.print(panel)


@cli.command()
@click.pass_context
def quick_start(ctx):
    """Quick start guide for new users"""
    quick_start_text = Text()
    quick_start_text.append("Quick Start Guide:\n\n", style="bold white")

    quick_start_text.append("1. ", style="bold yellow")
    quick_start_text.append("Check System Health", style="bold white")
    quick_start_text.append("\n   ", style="white")
    quick_start_text.append("revsin system health", style="green")
    quick_start_text.append(
        "\n   Verify database and Redis connections are working.\n\n", style="dim")

    quick_start_text.append("2. ", style="bold yellow")
    quick_start_text.append(
        "Initialize Database (if needed)", style="bold white")
    quick_start_text.append("\n   ", style="white")
    quick_start_text.append("revsin system init-db", style="green")
    quick_start_text.append(
        "\n   Set up database tables and initial structure.\n\n", style="dim")

    quick_start_text.append("3. ", style="bold yellow")
    quick_start_text.append("Create Your First User", style="bold white")
    quick_start_text.append("\n   ", style="white")
    quick_start_text.append("revsin users create --role admin", style="green")
    quick_start_text.append(
        "\n   Create an admin user to manage the system.\n\n", style="dim")

    quick_start_text.append("4. ", style="bold yellow")
    quick_start_text.append("Add Some Books", style="bold white")
    quick_start_text.append("\n   ", style="white")
    quick_start_text.append("revsin books add", style="green")
    quick_start_text.append(
        "\n   Add books to your library inventory.\n\n", style="dim")

    quick_start_text.append("5. ", style="bold yellow")
    quick_start_text.append("Create a Loan", style="bold white")
    quick_start_text.append("\n   ", style="white")
    quick_start_text.append("revsin loans create", style="green")
    quick_start_text.append(
        "\n   Start lending books to users.\n\n", style="dim")

    quick_start_text.append("6. ", style="bold yellow")
    quick_start_text.append("Monitor Operations", style="bold white")
    quick_start_text.append("\n   ", style="white")
    quick_start_text.append("revsin loans active", style="green")
    quick_start_text.append(" / ")
    quick_start_text.append("revsin loans overdue", style="green")
    quick_start_text.append(
        "\n   Keep track of active and overdue loans.\n\n", style="dim")

    quick_start_text.append("Pro Tips:", style="bold cyan")
    quick_start_text.append("\n• Use ", style="white")
    quick_start_text.append("--help", style="yellow")
    quick_start_text.append(
        " with any command for detailed options\n", style="white")
    quick_start_text.append("• Most commands support ", style="white")
    quick_start_text.append("--limit", style="yellow")
    quick_start_text.append(" and ", style="white")
    quick_start_text.append("--skip", style="yellow")
    quick_start_text.append(" for pagination\n", style="white")
    quick_start_text.append(
        "• Search commands use fuzzy matching\n", style="white")
    quick_start_text.append("• Use ", style="white")
    quick_start_text.append("stats", style="yellow")
    quick_start_text.append(" subcommands for quick overviews", style="white")

    panel = Panel(quick_start_text, title="Quick Start",
                  border_style="magenta")
    console.print(panel)


# Add command groups
cli.add_command(system)
cli.add_command(users)
cli.add_command(books)
cli.add_command(loans)

# Custom help formatting


@cli.command()
@click.pass_context
def help(ctx):
    """Show comprehensive help information"""
    console.print(cli.get_help(ctx))


if __name__ == "__main__":
    cli()
