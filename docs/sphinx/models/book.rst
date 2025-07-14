Book Model
==========

.. module:: revsin.models.book

The Book model represents books in the RevSin library management system.

Book Class
---------

.. autoclass:: Book
   :members:
   :undoc-members:
   :show-inheritance:

   The ``Book`` class represents a book in the library.

   **Fields**:

   * ``id``: UUID primary key, automatically generated
   * ``title``: Title of the book
   * ``author``: Author of the book
   * ``isbn``: ISBN (International Standard Book Number) of the book
   * ``publication_year``: Year the book was published
   * ``publisher``: Publisher of the book
   * ``category``: Category or genre of the book
   * ``description``: Description or summary of the book
   * ``total_copies``: Total number of copies owned by the library
   * ``available_copies``: Number of copies currently available for loan
   * ``created_at``: Timestamp when the book record was created
   * ``updated_at``: Timestamp when the book record was last updated
   * ``loans``: Relationship to the book's loans

   **Properties**:

   * ``available``: Boolean indicating if the book is available for loan
   * ``current_loans``: Number of active loans for the book

   **Methods**:

   * ``to_dict()``: Convert the book to a dictionary representation
   * ``from_dict()``: Create a book instance from a dictionary
   * ``to_schema()``: Convert the book to a Pydantic schema
   * ``from_schema()``: Create a book instance from a Pydantic schema
   * ``update_availability()``: Update the available_copies count based on active loans

   **Example Usage**:

   .. code-block:: python

      # Create a new book
      book = Book(
          title="The Great Gatsby",
          author="F. Scott Fitzgerald",
          isbn="9780743273565",
          publication_year=1925,
          publisher="Scribner",
          category="Fiction",
          description="The Great Gatsby is a 1925 novel by American writer F. Scott Fitzgerald...",
          total_copies=5
      )
      
      # Check if the book is available
      if book.available:
          # Book is available for loan
          pass
      
      # Get active loans for the book
      active_loans = book.current_loans

ISBN Validation
-------------

The Book model includes validation for ISBN (International Standard Book Number):

* ISBN must be a valid ISBN-10 or ISBN-13 format
* ISBN is stored without hyphens or spaces
* ISBN is unique across all books in the system

Example of ISBN validation:

.. code-block:: python

   # Create a book with a valid ISBN
   book = Book(
       title="1984",
       author="George Orwell",
       isbn="9780451524935"  # Valid ISBN-13
   )
   
   # Invalid ISBN would raise a validation error during creation or update

Availability Management
--------------------

The Book model tracks book availability through the ``total_copies`` and ``available_copies`` fields:

* ``total_copies``: Total number of physical copies owned by the library
* ``available_copies``: Number of copies currently available for loan
* ``available``: Boolean property indicating if at least one copy is available

The ``update_availability()`` method is used to recalculate the ``available_copies`` count based on active loans:

.. code-block:: python

   # Update availability after a loan is created or returned
   book.update_availability()
   db.add(book)
   db.commit()
   
   # Check if the book is available for loan
   if book.available:
       # Book is available
       pass
   else:
       # No copies available
       pass

Search Functionality
-----------------

The Book model supports various search capabilities:

* Search by title (case-insensitive, partial match)
* Search by author (case-insensitive, partial match)
* Search by ISBN (exact match)
* Search by category
* Filter by availability

Example search query:

.. code-block:: python

   # Search for books by title
   books = db.query(Book).filter(Book.title.ilike(f"%{search_term}%")).all()
   
   # Search for available books in a specific category
   books = db.query(Book).filter(
       Book.category == category,
       Book.available_copies > 0
   ).all() 