Loan Model
==========

.. module:: revsin.models.loan

The Loan model represents book loans in the RevSin library management system.

Loan Class
---------

.. autoclass:: Loan
   :members:
   :undoc-members:
   :show-inheritance:

   The ``Loan`` class represents a book loan to a user.

   **Fields**:

   * ``id``: UUID primary key, automatically generated
   * ``user_id``: UUID of the user who borrowed the book
   * ``book_id``: UUID of the borrowed book
   * ``loan_date``: Date when the book was borrowed
   * ``due_date``: Date when the book is due to be returned
   * ``return_date``: Date when the book was returned (null if not yet returned)
   * ``renewal_count``: Number of times the loan has been renewed
   * ``created_at``: Timestamp when the loan record was created
   * ``updated_at``: Timestamp when the loan record was last updated
   * ``user``: Relationship to the user who borrowed the book
   * ``book``: Relationship to the borrowed book

   **Properties**:

   * ``status``: Status of the loan (active, returned, overdue)
   * ``is_overdue``: Boolean indicating if the loan is overdue
   * ``days_overdue``: Number of days the loan is overdue (0 if not overdue)

   **Methods**:

   * ``renew(days=30)``: Renew the loan for a specified number of days
   * ``return_book()``: Mark the book as returned
   * ``to_dict()``: Convert the loan to a dictionary representation
   * ``from_dict()``: Create a loan instance from a dictionary
   * ``to_schema()``: Convert the loan to a Pydantic schema
   * ``from_schema()``: Create a loan instance from a Pydantic schema

   **Example Usage**:

   .. code-block:: python

      # Create a new loan
      loan = Loan(
          user_id=user.id,
          book_id=book.id,
          loan_date=datetime.utcnow(),
          due_date=datetime.utcnow() + timedelta(days=30)
      )
      
      # Check if the loan is overdue
      if loan.is_overdue:
          # Handle overdue loan
          print(f"Loan is overdue by {loan.days_overdue} days")
      
      # Renew the loan
      loan.renew(days=14)
      
      # Return the book
      loan.return_book()

LoanStatus Enum
-------------

.. autoclass:: LoanStatus
   :members:
   :undoc-members:
   :show-inheritance:

   The ``LoanStatus`` enum defines the possible statuses for a loan.

   **Values**:

   * ``ACTIVE``: The loan is active and the book is currently borrowed
   * ``RETURNED``: The book has been returned
   * ``OVERDUE``: The loan is active but past the due date

   **Example Usage**:

   .. code-block:: python

      # Check the status of a loan
      if loan.status == LoanStatus.ACTIVE:
          # Loan is active
          pass
      elif loan.status == LoanStatus.RETURNED:
          # Book has been returned
          pass
      elif loan.status == LoanStatus.OVERDUE:
          # Loan is overdue
          pass

Loan Management
-------------

The Loan model provides methods for managing the loan lifecycle:

Renewal
~~~~~~

The ``renew()`` method extends the due date of a loan:

.. code-block:: python

   # Renew a loan for 14 days
   loan.renew(days=14)
   
   # The due_date will be extended by 14 days from the current date
   # The renewal_count will be incremented by 1

Renewal rules:

* A loan can only be renewed if it is active (not returned)
* A loan cannot be renewed if it is already overdue
* There may be a maximum number of renewals allowed per loan

Return
~~~~~

The ``return_book()`` method marks a book as returned:

.. code-block:: python

   # Return a book
   loan.return_book()
   
   # The return_date will be set to the current date
   # The status will change to RETURNED
   # The book's available_copies count will be incremented

Return rules:

* A book can only be returned if it is currently on loan (not already returned)
* When a book is returned, the book's availability is updated automatically

Overdue Management
----------------

The Loan model includes functionality for managing overdue loans:

* ``is_overdue``: Boolean property that checks if the current date is past the due date
* ``days_overdue``: Property that calculates the number of days the loan is overdue
* ``status``: Returns ``LoanStatus.OVERDUE`` if the loan is overdue

Example of overdue management:

.. code-block:: python

   # Get all overdue loans
   overdue_loans = db.query(Loan).filter(
       Loan.return_date.is_(None),
       Loan.due_date < datetime.utcnow()
   ).all()
   
   # Process overdue loans
   for loan in overdue_loans:
       # Calculate overdue days
       days_overdue = loan.days_overdue
       
       # Send notification if significantly overdue
       if days_overdue > 7:
           send_overdue_notification(loan.user, loan.book, days_overdue) 