"""
Loan management commands for the Library Management System CLI
"""

import click
from datetime import datetime, timedelta
from decimal import Decimal

from ..utils import (
    handle_errors, get_db_session, print_success, print_error, print_info,
    confirm_action, prompt_for_input, display_table, format_datetime,
    format_loan_status, format_currency, format_bool, truncate_text
)
from ...crud.loan import loan_crud
from ...crud.user import user_crud
from ...crud.book import book_crud
from ...schemas.loan import LoanCreate, LoanUpdate, LoanReturn
from ...models.loan import LoanStatus


@click.group()
def loans():
    """Loan management commands"""
    pass


@loans.command()
@click.option('--user-id', type=int, help='User ID')
@click.option('--book-id', type=int, help='Book ID')
@click.option('--days', type=int, default=14, help='Loan duration in days')
@handle_errors
def create(user_id, book_id, days):
    """Create a new loan"""

    with get_db_session() as db:
        # Get user ID if not provided
        if not user_id:
            user_id_input = prompt_for_input("User ID")
            try:
                user_id = int(user_id_input)
            except ValueError:
                print_error("Invalid user ID")
                return

        # Get book ID if not provided
        if not book_id:
            book_id_input = prompt_for_input("Book ID")
            try:
                book_id = int(book_id_input)
            except ValueError:
                print_error("Invalid book ID")
                return

        # Validate user exists
        user = user_crud.get(db, user_id)
        if not user:
            print_error(f"User with ID {user_id} not found")
            return

        # Validate book exists
        book = book_crud.get(db, book_id)
        if not book:
            print_error(f"Book with ID {book_id} not found")
            return

        # Check if book is available
        if not book.is_available:
            print_error(f"Book '{book.title}' is not available for loan")
            return

        # Calculate due date
        due_date = datetime.utcnow() + timedelta(days=days)

        # Create loan data
        loan_data = LoanCreate(
            user_id=user_id,
            book_id=book_id,
            due_date=due_date
        )

        try:
            loan = loan_crud.create_loan(db, obj_in=loan_data)
            if loan:
                print_success(f"Loan created successfully with ID: {loan.id}")
                print(f"User: {user.full_name}")
                print(f"Book: {book.title}")
                print(f"Due date: {format_datetime(loan.due_date)}")
            else:
                print_error(
                    "Failed to create loan - book may not be available")
        except Exception as e:
            print_error(f"Failed to create loan: {str(e)}")


@loans.command()
@click.option('--limit', default=10, help='Number of loans to display')
@click.option('--skip', default=0, help='Number of loans to skip')
@click.option('--status', type=click.Choice(['active', 'returned', 'overdue', 'renewed', 'lost']),
              help='Filter by status')
@click.option('--user-id', type=int, help='Filter by user ID')
@click.option('--book-id', type=int, help='Filter by book ID')
@handle_errors
def list(limit, skip, status, user_id, book_id):
    """List loans"""

    with get_db_session() as db:
        filters = {}
        if status:
            filters['status'] = LoanStatus(status)
        if user_id:
            filters['user_id'] = user_id
        if book_id:
            filters['book_id'] = book_id

        loans = loan_crud.get_multi(
            db, skip=skip, limit=limit, filters=filters)

        if not loans:
            print_info("No loans found")
            return

        # Prepare data for display
        loan_data = []
        for loan in loans:
            loan_data.append({
                'ID': loan.id,
                'User': truncate_text(loan.user.full_name, 20),
                'Book': truncate_text(loan.book.title, 25),
                'Status': loan.status.value,
                'Loan Date': format_datetime(loan.loan_date),
                'Due Date': format_datetime(loan.due_date),
                'Return Date': format_datetime(loan.return_date) if loan.return_date else 'N/A',
                'Renewals': loan.renewal_count,
                'Fine': format_currency(loan.fine_amount)
            })

        headers = ['ID', 'User', 'Book', 'Status', 'Loan Date',
                   'Due Date', 'Return Date', 'Renewals', 'Fine']
        display_table(loan_data, headers, "Loans")


@loans.command()
@click.argument('loan_id', type=int)
@handle_errors
def show(loan_id):
    """Show loan details"""

    with get_db_session() as db:
        loan = loan_crud.get(db, loan_id)

        if not loan:
            print_error(f"Loan with ID {loan_id} not found")
            return

        print_info(f"Loan Details - ID: {loan.id}")
        print(f"User: {loan.user.full_name} (ID: {loan.user_id})")
        print(f"Book: {loan.book.title} (ID: {loan.book_id})")
        print(f"ISBN: {loan.book.isbn}")
        print(f"Status: {format_loan_status(loan.status.value)}")
        print(f"Loan Date: {format_datetime(loan.loan_date)}")
        print(f"Due Date: {format_datetime(loan.due_date)}")
        print(
            f"Return Date: {format_datetime(loan.return_date) if loan.return_date else 'Not returned'}")
        print(f"Renewal Count: {loan.renewal_count}/{loan.max_renewals}")
        print(f"Fine Amount: {format_currency(loan.fine_amount)}")
        print(f"Fine Paid: {format_bool(loan.fine_paid)}")
        print(f"Notes: {loan.notes or 'None'}")

        # Show status information
        if loan.is_overdue:
            print(f"[red]Overdue by {loan.days_overdue} days[/red]")

        if loan.can_renew:
            print("[green]Can be renewed[/green]")
        else:
            print("[red]Cannot be renewed[/red]")


@loans.command()
@click.argument('loan_id', type=int)
@click.option('--notes', help='Return notes')
@handle_errors
def return_book(loan_id, notes):
    """Return a book"""

    with get_db_session() as db:
        loan = loan_crud.get(db, loan_id)

        if not loan:
            print_error(f"Loan with ID {loan_id} not found")
            return

        if loan.status != LoanStatus.ACTIVE:
            print_error(f"Loan is not active (status: {loan.status.value})")
            return

        # Calculate fine if overdue
        fine_amount = Decimal('0.0')
        if loan.is_overdue:
            fine_amount = Decimal(str(loan.calculate_fine()))
            print_warning(f"Book is overdue by {loan.days_overdue} days")
            print_warning(f"Fine amount: {format_currency(fine_amount)}")

        try:
            loan_return = LoanReturn(
                return_date=datetime.utcnow(),
                notes=notes,
                fine_amount=fine_amount
            )

            returned_loan = loan_crud.return_book(
                db, loan_id=loan_id, return_data=loan_return)
            if returned_loan:
                print_success(
                    f"Book '{loan.book.title}' returned successfully")
                if fine_amount > 0:
                    print_warning(
                        f"Fine of {format_currency(fine_amount)} has been applied")
            else:
                print_error("Failed to return book")
        except Exception as e:
            print_error(f"Failed to return book: {str(e)}")


@loans.command()
@click.argument('loan_id', type=int)
@handle_errors
def renew(loan_id):
    """Renew a loan"""

    with get_db_session() as db:
        loan = loan_crud.get(db, loan_id)

        if not loan:
            print_error(f"Loan with ID {loan_id} not found")
            return

        if not loan.can_renew:
            if loan.status != LoanStatus.ACTIVE:
                print_error(
                    f"Loan is not active (status: {loan.status.value})")
            elif loan.renewal_count >= loan.max_renewals:
                print_error(f"Maximum renewals ({loan.max_renewals}) reached")
            elif loan.is_overdue:
                print_error("Cannot renew overdue loan")
            else:
                print_error("Loan cannot be renewed")
            return

        try:
            renewed_loan = loan_crud.renew_loan(db, loan_id=loan_id)
            if renewed_loan:
                print_success(f"Loan renewed successfully")
                print(
                    f"New due date: {format_datetime(renewed_loan.due_date)}")
                print(
                    f"Renewals: {renewed_loan.renewal_count}/{renewed_loan.max_renewals}")
            else:
                print_error("Failed to renew loan")
        except Exception as e:
            print_error(f"Failed to renew loan: {str(e)}")


@loans.command()
@click.option('--limit', default=10, help='Number of loans to display')
@handle_errors
def overdue(limit):
    """Show overdue loans"""

    with get_db_session() as db:
        loans = loan_crud.get_overdue_loans(db, limit=limit)

        if not loans:
            print_info("No overdue loans found")
            return

        # Prepare data for display
        loan_data = []
        for loan in loans:
            loan_data.append({
                'ID': loan.id,
                'User': truncate_text(loan.user.full_name, 20),
                'Book': truncate_text(loan.book.title, 25),
                'Due Date': format_datetime(loan.due_date),
                'Days Overdue': loan.days_overdue,
                'Fine': format_currency(loan.calculate_fine()),
                'Contact': loan.user.phone or loan.user.email
            })

        headers = ['ID', 'User', 'Book', 'Due Date',
                   'Days Overdue', 'Fine', 'Contact']
        display_table(loan_data, headers, "Overdue Loans")


@loans.command()
@click.argument('user_id', type=int)
@click.option('--limit', default=10, help='Number of loans to display')
@handle_errors
def by_user(user_id, limit):
    """Show loans for a specific user"""

    with get_db_session() as db:
        user = user_crud.get(db, user_id)
        if not user:
            print_error(f"User with ID {user_id} not found")
            return

        loans = loan_crud.get_loans_by_user(db, user_id=user_id, limit=limit)

        if not loans:
            print_info(f"No loans found for user '{user.full_name}'")
            return

        # Prepare data for display
        loan_data = []
        for loan in loans:
            loan_data.append({
                'ID': loan.id,
                'Book': truncate_text(loan.book.title, 30),
                'ISBN': loan.book.isbn,
                'Status': loan.status.value,
                'Loan Date': format_datetime(loan.loan_date),
                'Due Date': format_datetime(loan.due_date),
                'Return Date': format_datetime(loan.return_date) if loan.return_date else 'N/A',
                'Renewals': loan.renewal_count,
                'Fine': format_currency(loan.fine_amount)
            })

        headers = ['ID', 'Book', 'ISBN', 'Status', 'Loan Date',
                   'Due Date', 'Return Date', 'Renewals', 'Fine']
        display_table(loan_data, headers, f"Loans for {user.full_name}")


@loans.command()
@click.argument('book_id', type=int)
@click.option('--limit', default=10, help='Number of loans to display')
@handle_errors
def by_book(book_id, limit):
    """Show loan history for a specific book"""

    with get_db_session() as db:
        book = book_crud.get(db, book_id)
        if not book:
            print_error(f"Book with ID {book_id} not found")
            return

        loans = loan_crud.get_loans_by_book(db, book_id=book_id, limit=limit)

        if not loans:
            print_info(f"No loans found for book '{book.title}'")
            return

        # Prepare data for display
        loan_data = []
        for loan in loans:
            loan_data.append({
                'ID': loan.id,
                'User': truncate_text(loan.user.full_name, 20),
                'Status': loan.status.value,
                'Loan Date': format_datetime(loan.loan_date),
                'Due Date': format_datetime(loan.due_date),
                'Return Date': format_datetime(loan.return_date) if loan.return_date else 'N/A',
                'Renewals': loan.renewal_count,
                'Fine': format_currency(loan.fine_amount)
            })

        headers = ['ID', 'User', 'Status', 'Loan Date',
                   'Due Date', 'Return Date', 'Renewals', 'Fine']
        display_table(loan_data, headers, f"Loan History for '{book.title}'")


@loans.command()
@click.argument('loan_id', type=int)
@click.option('--amount', type=float, help='Fine amount to pay')
@handle_errors
def pay_fine(loan_id, amount):
    """Pay fine for a loan"""

    with get_db_session() as db:
        loan = loan_crud.get(db, loan_id)

        if not loan:
            print_error(f"Loan with ID {loan_id} not found")
            return

        if loan.fine_amount == 0:
            print_info("No fine to pay for this loan")
            return

        if loan.fine_paid:
            print_info("Fine has already been paid")
            return

        if not amount:
            amount_input = prompt_for_input(
                f"Fine amount to pay (${float(loan.fine_amount):.2f})")
            try:
                amount = float(amount_input)
            except ValueError:
                print_error("Invalid amount")
                return

        if amount < float(loan.fine_amount):
            print_error(
                f"Amount must be at least ${float(loan.fine_amount):.2f}")
            return

        try:
            loan_crud.update(db, db_obj=loan, obj_in={'fine_paid': True})
            print_success(f"Fine of ${amount:.2f} paid successfully")
        except Exception as e:
            print_error(f"Failed to record fine payment: {str(e)}")


@loans.command()
@handle_errors
def stats():
    """Display loan statistics"""

    with get_db_session() as db:
        total_loans = loan_crud.count(db)
        active_loans = loan_crud.count(
            db, filters={'status': LoanStatus.ACTIVE})
        returned_loans = loan_crud.count(
            db, filters={'status': LoanStatus.RETURNED})
        overdue_loans = loan_crud.count(
            db, filters={'status': LoanStatus.OVERDUE})
        renewed_loans = loan_crud.count(
            db, filters={'status': LoanStatus.RENEWED})
        lost_loans = loan_crud.count(db, filters={'status': LoanStatus.LOST})

        print_info("Loan Statistics")
        print(f"Total loans: {total_loans}")
        print(f"Active loans: {active_loans}")
        print(f"Returned loans: {returned_loans}")
        print(f"Overdue loans: {overdue_loans}")
        print(f"Renewed loans: {renewed_loans}")
        print(f"Lost loans: {lost_loans}")

        # Calculate fine statistics
        all_loans = loan_crud.get_multi(db, limit=10000)
        total_fines = sum(float(loan.fine_amount) for loan in all_loans)
        unpaid_fines = sum(float(loan.fine_amount)
                           for loan in all_loans if not loan.fine_paid)

        print(f"Total fines: ${total_fines:.2f}")
        print(f"Unpaid fines: ${unpaid_fines:.2f}")


@loans.command()
@click.option('--limit', default=10, help='Number of loans to display')
@handle_errors
def active():
    """Show active loans"""

    with get_db_session() as db:
        loans = loan_crud.get_active_loans(db, limit=limit)

        if not loans:
            print_info("No active loans found")
            return

        # Prepare data for display
        loan_data = []
        for loan in loans:
            loan_data.append({
                'ID': loan.id,
                'User': truncate_text(loan.user.full_name, 20),
                'Book': truncate_text(loan.book.title, 25),
                'Due Date': format_datetime(loan.due_date),
                'Days Left': (loan.due_date - datetime.utcnow()).days,
                'Renewals': f"{loan.renewal_count}/{loan.max_renewals}",
                'Can Renew': format_bool(loan.can_renew)
            })

        headers = ['ID', 'User', 'Book', 'Due Date',
                   'Days Left', 'Renewals', 'Can Renew']
        display_table(loan_data, headers, "Active Loans")


if __name__ == "__main__":
    loans()
