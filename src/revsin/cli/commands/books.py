"""
Book management commands for the Library Management System CLI
"""

import click
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

from ..utils import (
    handle_errors, get_db_session, print_success, print_error, print_info,
    confirm_action, prompt_for_input, display_table, validate_isbn,
    format_datetime, format_book_status, format_currency, truncate_text
)
from ...crud.book import book_crud
from ...schemas.book import BookCreate, BookUpdate
from ...models.book import BookStatus


@click.group()
def books():
    """Book management commands"""
    pass


@books.command()
@click.option('--isbn', help='ISBN of the book')
@click.option('--title', help='Title of the book')
@click.option('--author', help='Author of the book')
@click.option('--publisher', help='Publisher')
@click.option('--publication-year', type=int, help='Publication year')
@click.option('--edition', help='Edition')
@click.option('--description', help='Description')
@click.option('--category', help='Category')
@click.option('--language', default='English', help='Language')
@click.option('--pages', type=int, help='Number of pages')
@click.option('--location', help='Location in library')
@click.option('--quantity', type=int, default=1, help='Quantity')
@click.option('--price', type=float, help='Price')
@handle_errors
def add(isbn, title, author, publisher, publication_year, edition, description,
        category, language, pages, location, quantity, price):
    """Add a new book"""

    # Collect missing information
    if not isbn:
        isbn = prompt_for_input("ISBN")

    if not validate_isbn(isbn):
        print_error("Invalid ISBN format")
        return

    if not title:
        title = prompt_for_input("Title")

    if not author:
        author = prompt_for_input("Author")

    if not publisher:
        publisher = prompt_for_input("Publisher (optional)", default="")

    if not publication_year:
        year_input = prompt_for_input(
            "Publication year (optional)", default="")
        if year_input:
            try:
                publication_year = int(year_input)
            except ValueError:
                print_error("Invalid publication year")
                return

    if not category:
        category = prompt_for_input("Category (optional)", default="")

    if not location:
        location = prompt_for_input(
            "Location in library (optional)", default="")

    # Create book data
    book_data = BookCreate(
        isbn=isbn,
        title=title,
        author=author,
        publisher=publisher if publisher else None,
        publication_year=publication_year,
        edition=edition,
        description=description,
        category=category if category else None,
        language=language,
        pages=pages,
        location=location if location else None,
        quantity=quantity,
        price=Decimal(str(price)) if price else None
    )

    with get_db_session() as db:
        try:
            book = book_crud.create(db, obj_in=book_data)
            print_success(
                f"Book '{book.title}' added successfully with ID: {book.id}")
        except IntegrityError as e:
            if "isbn" in str(e):
                print_error("ISBN already exists")
            else:
                print_error(f"Failed to add book: {str(e)}")


@books.command()
@click.option('--limit', default=10, help='Number of books to display')
@click.option('--skip', default=0, help='Number of books to skip')
@click.option('--status', type=click.Choice(['available', 'loaned', 'reserved', 'maintenance', 'lost']),
              help='Filter by status')
@click.option('--category', help='Filter by category')
@click.option('--author', help='Filter by author')
@click.option('--available-only', is_flag=True, help='Show only available books')
@handle_errors
def list(limit, skip, status, category, author, available_only):
    """List books"""

    with get_db_session() as db:
        if available_only:
            books = book_crud.get_available_books(db, skip=skip, limit=limit)
        else:
            books = book_crud.search_books(
                db,
                category=category,
                author=author,
                status=BookStatus(status) if status else None,
                skip=skip,
                limit=limit
            )

        if not books:
            print_info("No books found")
            return

        # Prepare data for display
        book_data = []
        for book in books:
            book_data.append({
                'ID': book.id,
                'ISBN': book.isbn,
                'Title': truncate_text(book.title, 30),
                'Author': truncate_text(book.author, 20),
                'Category': book.category or 'N/A',
                'Status': book.status.value,
                'Available': f"{book.available_quantity}/{book.quantity}",
                'Location': book.location or 'N/A'
            })

        headers = ['ID', 'ISBN', 'Title', 'Author',
                   'Category', 'Status', 'Available', 'Location']
        display_table(book_data, headers, "Books")


@books.command()
@click.argument('book_id', type=int)
@handle_errors
def show(book_id):
    """Show book details"""

    with get_db_session() as db:
        book = book_crud.get(db, book_id)

        if not book:
            print_error(f"Book with ID {book_id} not found")
            return

        print_info(f"Book Details - ID: {book.id}")
        print(f"ISBN: {book.isbn}")
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print(f"Publisher: {book.publisher or 'N/A'}")
        print(f"Publication Year: {book.publication_year or 'N/A'}")
        print(f"Edition: {book.edition or 'N/A'}")
        print(f"Category: {book.category or 'N/A'}")
        print(f"Language: {book.language}")
        print(f"Pages: {book.pages or 'N/A'}")
        print(f"Description: {book.description or 'N/A'}")
        print(f"Status: {format_book_status(book.status.value)}")
        print(f"Location: {book.location or 'N/A'}")
        print(f"Quantity: {book.quantity}")
        print(f"Available: {book.available_quantity}")
        print(f"Price: {format_currency(book.price)}")
        print(f"Created: {format_datetime(book.created_at)}")
        print(f"Updated: {format_datetime(book.updated_at)}")

        # Show loan information
        active_loans = sum(
            1 for loan in book.loans if loan.status.value == 'active')
        total_loans = len(book.loans)
        print(f"Active loans: {active_loans}")
        print(f"Total loans: {total_loans}")


@books.command()
@click.argument('book_id', type=int)
@click.option('--isbn', help='New ISBN')
@click.option('--title', help='New title')
@click.option('--author', help='New author')
@click.option('--publisher', help='New publisher')
@click.option('--publication-year', type=int, help='New publication year')
@click.option('--edition', help='New edition')
@click.option('--description', help='New description')
@click.option('--category', help='New category')
@click.option('--language', help='New language')
@click.option('--pages', type=int, help='New number of pages')
@click.option('--location', help='New location')
@click.option('--quantity', type=int, help='New quantity')
@click.option('--price', type=float, help='New price')
@click.option('--status', type=click.Choice(['available', 'loaned', 'reserved', 'maintenance', 'lost']),
              help='New status')
@handle_errors
def update(book_id, isbn, title, author, publisher, publication_year, edition,
           description, category, language, pages, location, quantity, price, status):
    """Update book information"""

    with get_db_session() as db:
        book = book_crud.get(db, book_id)

        if not book:
            print_error(f"Book with ID {book_id} not found")
            return

        # Collect update data
        update_data = {}

        if isbn is not None:
            if not validate_isbn(isbn):
                print_error("Invalid ISBN format")
                return
            update_data['isbn'] = isbn

        if title is not None:
            update_data['title'] = title

        if author is not None:
            update_data['author'] = author

        if publisher is not None:
            update_data['publisher'] = publisher

        if publication_year is not None:
            update_data['publication_year'] = publication_year

        if edition is not None:
            update_data['edition'] = edition

        if description is not None:
            update_data['description'] = description

        if category is not None:
            update_data['category'] = category

        if language is not None:
            update_data['language'] = language

        if pages is not None:
            update_data['pages'] = pages

        if location is not None:
            update_data['location'] = location

        if quantity is not None:
            # Check if new quantity is valid
            if quantity < book.quantity - book.available_quantity:
                print_error(
                    f"Cannot reduce quantity below currently loaned books ({book.quantity - book.available_quantity})")
                return

            # Update available quantity proportionally
            diff = quantity - book.quantity
            update_data['quantity'] = quantity
            update_data['available_quantity'] = book.available_quantity + diff

        if price is not None:
            update_data['price'] = Decimal(str(price))

        if status is not None:
            update_data['status'] = BookStatus(status)

        if not update_data:
            print_info("No changes specified")
            return

        try:
            book_update = BookUpdate(**update_data)
            updated_book = book_crud.update(
                db, db_obj=book, obj_in=book_update)
            print_success(f"Book '{updated_book.title}' updated successfully")
        except IntegrityError as e:
            if "isbn" in str(e):
                print_error("ISBN already exists")
            else:
                print_error(f"Failed to update book: {str(e)}")


@books.command()
@click.argument('book_id', type=int)
@click.option('--force', is_flag=True, help='Force deletion without confirmation')
@handle_errors
def delete(book_id, force):
    """Delete a book"""

    with get_db_session() as db:
        book = book_crud.get(db, book_id)

        if not book:
            print_error(f"Book with ID {book_id} not found")
            return

        # Check for active loans
        active_loans = sum(
            1 for loan in book.loans if loan.status.value == 'active')
        if active_loans > 0:
            print_error(f"Cannot delete book with {active_loans} active loans")
            return

        if not force:
            if not confirm_action(f"Delete book '{book.title}'? This action cannot be undone."):
                return

        try:
            book_crud.remove(db, id=book_id)
            print_success(f"Book '{book.title}' deleted successfully")
        except Exception as e:
            print_error(f"Failed to delete book: {str(e)}")


@books.command()
@click.argument('query')
@click.option('--limit', default=10, help='Number of results to display')
@click.option('--category', help='Filter by category')
@click.option('--author', help='Filter by author')
@click.option('--available-only', is_flag=True, help='Show only available books')
@handle_errors
def search(query, limit, category, author, available_only):
    """Search books by title, author, ISBN, or description"""

    with get_db_session() as db:
        books = book_crud.search_books(
            db,
            query=query,
            category=category,
            author=author,
            available_only=available_only,
            limit=limit
        )

        if not books:
            print_info(f"No books found matching '{query}'")
            return

        # Prepare data for display
        book_data = []
        for book in books:
            book_data.append({
                'ID': book.id,
                'ISBN': book.isbn,
                'Title': truncate_text(book.title, 30),
                'Author': truncate_text(book.author, 20),
                'Category': book.category or 'N/A',
                'Status': book.status.value,
                'Available': f"{book.available_quantity}/{book.quantity}"
            })

        headers = ['ID', 'ISBN', 'Title', 'Author',
                   'Category', 'Status', 'Available']
        display_table(book_data, headers, f"Search Results for '{query}'")


@books.command()
@click.option('--limit', default=10, help='Number of books to display')
@handle_errors
def available(limit):
    """Show available books"""

    with get_db_session() as db:
        books = book_crud.get_available_books(db, limit=limit)

        if not books:
            print_info("No available books found")
            return

        # Prepare data for display
        book_data = []
        for book in books:
            book_data.append({
                'ID': book.id,
                'ISBN': book.isbn,
                'Title': truncate_text(book.title, 30),
                'Author': truncate_text(book.author, 20),
                'Category': book.category or 'N/A',
                'Available': book.available_quantity,
                'Location': book.location or 'N/A'
            })

        headers = ['ID', 'ISBN', 'Title', 'Author',
                   'Category', 'Available', 'Location']
        display_table(book_data, headers, "Available Books")


@books.command()
@handle_errors
def categories():
    """Show book categories"""

    with get_db_session() as db:
        books = book_crud.get_multi(db, limit=1000)  # Get all books

        # Extract unique categories
        categories = set()
        for book in books:
            if book.category:
                categories.add(book.category)

        if not categories:
            print_info("No categories found")
            return

        print_info("Book Categories")
        for category in sorted(categories):
            # Count books in each category
            category_books = [b for b in books if b.category == category]
            print(f"  {category}: {len(category_books)} books")


@books.command()
@click.argument('author')
@click.option('--limit', default=10, help='Number of books to display')
@handle_errors
def by_author(author, limit):
    """Show books by author"""

    with get_db_session() as db:
        books = book_crud.get_books_by_author(db, author=author, limit=limit)

        if not books:
            print_info(f"No books found by author '{author}'")
            return

        # Prepare data for display
        book_data = []
        for book in books:
            book_data.append({
                'ID': book.id,
                'ISBN': book.isbn,
                'Title': truncate_text(book.title, 30),
                'Category': book.category or 'N/A',
                'Status': book.status.value,
                'Available': f"{book.available_quantity}/{book.quantity}"
            })

        headers = ['ID', 'ISBN', 'Title', 'Category', 'Status', 'Available']
        display_table(book_data, headers, f"Books by '{author}'")


@books.command()
@handle_errors
def stats():
    """Display book statistics"""

    with get_db_session() as db:
        total_books = book_crud.count(db)
        available_books = book_crud.count(
            db, filters={'status': BookStatus.AVAILABLE})
        loaned_books = book_crud.count(
            db, filters={'status': BookStatus.LOANED})
        reserved_books = book_crud.count(
            db, filters={'status': BookStatus.RESERVED})
        maintenance_books = book_crud.count(
            db, filters={'status': BookStatus.MAINTENANCE})
        lost_books = book_crud.count(db, filters={'status': BookStatus.LOST})

        print_info("Book Statistics")
        print(f"Total books: {total_books}")
        print(f"Available: {available_books}")
        print(f"Loaned: {loaned_books}")
        print(f"Reserved: {reserved_books}")
        print(f"Maintenance: {maintenance_books}")
        print(f"Lost: {lost_books}")


if __name__ == "__main__":
    books()
