"""
CLI utility functions for the Library Management System
"""

import sys
from typing import Optional, Any, Dict, List
from contextlib import contextmanager
from functools import wraps
import time

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from tabulate import tabulate
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..config import settings

console = Console()


def handle_errors(func):
    """Decorator to handle common CLI errors"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            console.print("\n[yellow]🚫 Operation cancelled by user[/yellow]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]💥 Error: {str(e)}[/red]")
            if settings.debug:
                raise
            sys.exit(1)
    return wrapper


@contextmanager
def get_db_session():
    """Context manager to get database session"""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def print_success(message: str):
    """Print success message with animation"""
    console.print(f"[green]🎉 {message}[/green]")


def print_error(message: str):
    """Print error message"""
    console.print(f"[red]❌ {message}[/red]")


def print_warning(message: str):
    """Print warning message"""
    console.print(f"[yellow]⚠️  {message}[/yellow]")


def print_info(message: str):
    """Print info message"""
    console.print(f"[blue]📋 {message}[/blue]")


def print_celebration(message: str):
    """Print celebration message with extra flair"""
    console.print(f"[magenta]🎊 {message} 🎊[/magenta]")


def confirm_action(message: str, default: bool = False) -> bool:
    """Confirm action with user"""
    return Confirm.ask(f"🤔 {message}", default=default)


def prompt_for_input(
    message: str,
    default: Optional[str] = None,
    password: bool = False,
    choices: Optional[List[str]] = None
) -> str:
    """Prompt user for input with emoji"""
    prompt_text = f"💭 {message}"
    if choices:
        return Prompt.ask(prompt_text, choices=choices, default=default)
    return Prompt.ask(prompt_text, default=default, password=password)


def display_table(data: List[Dict[str, Any]], headers: List[str], title: str = ""):
    """Display data in a rich table with enhanced styling"""
    if not data:
        print_info("No data found")
        return

    # Add emoji to title based on content
    if "user" in title.lower():
        title = f"👥 {title}"
    elif "book" in title.lower():
        title = f"📚 {title}"
    elif "loan" in title.lower():
        title = f"📋 {title}"
    elif "search" in title.lower():
        title = f"🔍 {title}"
    else:
        title = f"📊 {title}"

    table = Table(title=title, show_header=True, header_style="bold magenta")

    # Add columns with alternating styles
    for i, header in enumerate(headers):
        style = "cyan" if i % 2 == 0 else "green"
        table.add_column(header, style=style)

    # Add rows with zebra striping
    for i, row in enumerate(data):
        row_style = "dim" if i % 2 == 0 else None
        values = [str(row.get(header, "")) for header in headers]
        table.add_row(*values, style=row_style)

    console.print(table)


def display_simple_table(data: List[Dict[str, Any]], headers: List[str]):
    """Display a simple table using tabulate"""
    if not data:
        print_info("No data found")
        return

    table_data = []
    for row in data:
        table_data.append([row.get(header, "") for header in headers])

    console.print(tabulate(table_data, headers=headers, tablefmt="grid"))


def format_datetime(dt) -> str:
    """Format datetime for display"""
    if dt is None:
        return "N/A"
    return dt.strftime("%Y-%m-%d %H:%M")


def format_currency(amount) -> str:
    """Format currency for display"""
    if amount is None:
        return "N/A"
    return f"${float(amount):.2f}"


def format_bool(value: bool) -> str:
    """Format boolean for display with emojis"""
    return "✅ Yes" if value else "❌ No"


def paginate_results(
    results: List[Any],
    page: int = 1,
    per_page: int = 10
) -> tuple[List[Any], Dict[str, Any]]:
    """Paginate results and return pagination info"""
    total = len(results)
    total_pages = (total + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    paginated_results = results[start_idx:end_idx]

    pagination_info = {
        "current_page": page,
        "total_pages": total_pages,
        "total_items": total,
        "items_per_page": per_page,
        "start_index": start_idx + 1,
        "end_index": min(end_idx, total),
        "has_previous": page > 1,
        "has_next": page < total_pages
    }

    return paginated_results, pagination_info


def print_pagination_info(pagination_info: Dict[str, Any]):
    """Print pagination information"""
    info = pagination_info
    console.print(
        f"📄 Page {info['current_page']} of {info['total_pages']} "
        f"(Items {info['start_index']}-{info['end_index']} of {info['total_items']})"
    )


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_isbn(isbn: str) -> bool:
    """Validate ISBN format"""
    import re
    # Remove hyphens and spaces
    isbn = re.sub(r'[-\s]', '', isbn)
    # Check if it's 10 or 13 digits
    return re.match(r'^\d{10}$', isbn) or re.match(r'^\d{13}$', isbn)


def with_progress(description: str = "Processing..."):
    """Enhanced context manager for progress display"""
    @contextmanager
    def progress_context():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task(description=f"⚡ {description}")
            yield progress
            # Add a small delay to see the completion
            time.sleep(0.5)

    return progress_context()


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if text is None:
        return "N/A"
    return text if len(text) <= max_length else text[:max_length-3] + "..."


def format_user_role(role: str) -> str:
    """Format user role for display with emojis"""
    role_info = {
        "admin": ("👑", "red"),
        "librarian": ("📚", "yellow"),
        "member": ("👤", "green")
    }
    emoji, color = role_info.get(role, ("👤", "white"))
    return f"{emoji} [{color}]{role.upper()}[/{color}]"


def format_book_status(status: str) -> str:
    """Format book status for display with emojis"""
    status_info = {
        "available": ("✅", "green"),
        "loaned": ("📤", "yellow"),
        "reserved": ("🔒", "blue"),
        "maintenance": ("🔧", "orange"),
        "lost": ("❌", "red")
    }
    emoji, color = status_info.get(status, ("❓", "white"))
    return f"{emoji} [{color}]{status.upper()}[/{color}]"


def format_loan_status(status: str) -> str:
    """Format loan status for display with emojis"""
    status_info = {
        "active": ("🟢", "green"),
        "returned": ("✅", "blue"),
        "overdue": ("🚨", "red"),
        "renewed": ("🔄", "yellow"),
        "lost": ("❌", "red")
    }
    emoji, color = status_info.get(status, ("❓", "white"))
    return f"{emoji} [{color}]{status.upper()}[/{color}]"


def display_stats_panel(title: str, stats: Dict[str, Any]):
    """Display statistics in a beautiful panel"""
    stats_text = Text()

    for key, value in stats.items():
        # Add appropriate emoji based on key
        if "total" in key.lower():
            emoji = "📊"
        elif "active" in key.lower():
            emoji = "🟢"
        elif "overdue" in key.lower():
            emoji = "🚨"
        elif "available" in key.lower():
            emoji = "✅"
        elif "admin" in key.lower():
            emoji = "👑"
        elif "librarian" in key.lower():
            emoji = "📚"
        elif "member" in key.lower():
            emoji = "👤"
        else:
            emoji = "📈"

        stats_text.append(f"{emoji} {key}: ", style="bold cyan")
        stats_text.append(f"{value}\n", style="white")

    panel = Panel(
        Align.center(stats_text),
        title=f"📊 {title}",
        border_style="bright_blue",
        padding=(1, 2)
    )
    console.print(panel)


def print_ascii_art(text: str):
    """Print ASCII art for special occasions"""
    arts = {
        "success": """
    🎉 SUCCESS! 🎉
    ╔══════════════╗
    ║   AWESOME!   ║
    ╚══════════════╝
        """,
        "welcome": """
    ✨ WELCOME! ✨
    ╔═══════════════╗
    ║   LET'S GO!   ║
    ╚═══════════════╝
        """,
        "complete": """
    🚀 COMPLETE! 🚀
    ╔═══════════════╗
    ║   ALL DONE!   ║
    ╚═══════════════╝
        """
    }

    if text in arts:
        console.print(arts[text], style="green")


def create_interactive_menu(title: str, options: List[str]) -> int:
    """Create an interactive menu for selection"""
    console.print(f"\n🎯 {title}", style="bold cyan")
    console.print("─" * (len(title) + 4))

    for i, option in enumerate(options, 1):
        console.print(f"{i}. {option}")

    while True:
        try:
            choice = int(prompt_for_input("Select an option", default="1"))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print_warning(
                    f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print_warning("Please enter a valid number")
