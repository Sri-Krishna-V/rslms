Loans API
=========

.. module:: revsin.api.routes.loans

The Loans API provides endpoints for managing book loans in the library.

List Loans
---------

.. http:get:: /api/loans/

   Get a list of loans (librarian or admin only).

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Query Parameters**:

   * ``skip`` (int, optional): Number of loans to skip (default: 0)
   * ``limit`` (int, optional): Maximum number of loans to return (default: 100)
   * ``user_id`` (uuid, optional): Filter loans by user ID
   * ``book_id`` (uuid, optional): Filter loans by book ID
   * ``status`` (str, optional): Filter loans by status (active, returned, overdue)
   * ``due_before`` (datetime, optional): Filter loans due before a specific date
   * ``due_after`` (datetime, optional): Filter loans due after a specific date

   **Response**:

   .. code-block:: json

      {
        "total": 75,
        "items": [
          {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "user_id": "550e8400-e29b-41d4-a716-446655440001",
            "book_id": "550e8400-e29b-41d4-a716-446655440002",
            "loan_date": "2023-11-15T10:30:00Z",
            "due_date": "2023-12-15T10:30:00Z",
            "return_date": null,
            "status": "active",
            "renewal_count": 0,
            "user": {
              "id": "550e8400-e29b-41d4-a716-446655440001",
              "username": "johndoe",
              "email": "john@example.com"
            },
            "book": {
              "id": "550e8400-e29b-41d4-a716-446655440002",
              "title": "The Great Gatsby",
              "author": "F. Scott Fitzgerald"
            }
          },
          {
            "id": "550e8400-e29b-41d4-a716-446655440003",
            "user_id": "550e8400-e29b-41d4-a716-446655440004",
            "book_id": "550e8400-e29b-41d4-a716-446655440005",
            "loan_date": "2023-11-10T14:20:00Z",
            "due_date": "2023-12-10T14:20:00Z",
            "return_date": null,
            "status": "active",
            "renewal_count": 1,
            "user": {
              "id": "550e8400-e29b-41d4-a716-446655440004",
              "username": "janedoe",
              "email": "jane@example.com"
            },
            "book": {
              "id": "550e8400-e29b-41d4-a716-446655440005",
              "title": "To Kill a Mockingbird",
              "author": "Harper Lee"
            }
          }
        ]
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions

Get Loan
-------

.. http:get:: /api/loans/(uuid:loan_id)

   Get a specific loan by ID.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "user_id": "550e8400-e29b-41d4-a716-446655440001",
        "book_id": "550e8400-e29b-41d4-a716-446655440002",
        "loan_date": "2023-11-15T10:30:00Z",
        "due_date": "2023-12-15T10:30:00Z",
        "return_date": null,
        "status": "active",
        "renewal_count": 0,
        "created_at": "2023-11-15T10:30:00Z",
        "updated_at": "2023-11-15T10:30:00Z",
        "user": {
          "id": "550e8400-e29b-41d4-a716-446655440001",
          "username": "johndoe",
          "email": "john@example.com",
          "full_name": "John Doe"
        },
        "book": {
          "id": "550e8400-e29b-41d4-a716-446655440002",
          "title": "The Great Gatsby",
          "author": "F. Scott Fitzgerald",
          "isbn": "9780743273565"
        }
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 404: Loan not found

Create Loan
---------

.. http:post:: /api/loans/

   Create a new loan (librarian or admin only).

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Request Body**:

   .. code-block:: json

      {
        "user_id": "550e8400-e29b-41d4-a716-446655440001",
        "book_id": "550e8400-e29b-41d4-a716-446655440002",
        "due_date": "2023-12-15T10:30:00Z"
      }

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "user_id": "550e8400-e29b-41d4-a716-446655440001",
        "book_id": "550e8400-e29b-41d4-a716-446655440002",
        "loan_date": "2023-11-15T10:30:00Z",
        "due_date": "2023-12-15T10:30:00Z",
        "return_date": null,
        "status": "active",
        "renewal_count": 0,
        "created_at": "2023-11-15T10:30:00Z"
      }

   :statuscode 201: Loan created successfully
   :statuscode 400: Book not available or user has reached loan limit
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 404: User or book not found
   :statuscode 422: Validation error

Return Book
---------

.. http:post:: /api/loans/(uuid:loan_id)/return

   Return a book (librarian or admin only).

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "user_id": "550e8400-e29b-41d4-a716-446655440001",
        "book_id": "550e8400-e29b-41d4-a716-446655440002",
        "loan_date": "2023-11-15T10:30:00Z",
        "due_date": "2023-12-15T10:30:00Z",
        "return_date": "2023-11-25T14:20:00Z",
        "status": "returned",
        "renewal_count": 0,
        "updated_at": "2023-11-25T14:20:00Z"
      }

   :statuscode 200: Book returned successfully
   :statuscode 400: Book already returned
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 404: Loan not found

Renew Loan
---------

.. http:post:: /api/loans/(uuid:loan_id)/renew

   Renew a loan.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "user_id": "550e8400-e29b-41d4-a716-446655440001",
        "book_id": "550e8400-e29b-41d4-a716-446655440002",
        "loan_date": "2023-11-15T10:30:00Z",
        "due_date": "2024-01-15T10:30:00Z",
        "return_date": null,
        "status": "active",
        "renewal_count": 1,
        "updated_at": "2023-11-25T14:20:00Z"
      }

   :statuscode 200: Loan renewed successfully
   :statuscode 400: Loan cannot be renewed (already returned, maximum renewals reached, or overdue)
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 404: Loan not found

Get User Loans
------------

.. http:get:: /api/loans/user/me

   Get loans for the current authenticated user.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Query Parameters**:

   * ``status`` (str, optional): Filter loans by status (active, returned, overdue)
   * ``skip`` (int, optional): Number of loans to skip (default: 0)
   * ``limit`` (int, optional): Maximum number of loans to return (default: 100)

   **Response**:

   .. code-block:: json

      {
        "total": 3,
        "items": [
          {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "book_id": "550e8400-e29b-41d4-a716-446655440002",
            "loan_date": "2023-11-15T10:30:00Z",
            "due_date": "2023-12-15T10:30:00Z",
            "return_date": null,
            "status": "active",
            "renewal_count": 0,
            "book": {
              "id": "550e8400-e29b-41d4-a716-446655440002",
              "title": "The Great Gatsby",
              "author": "F. Scott Fitzgerald",
              "isbn": "9780743273565"
            }
          }
        ]
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized

Get Overdue Loans
---------------

.. http:get:: /api/loans/overdue

   Get a list of overdue loans (librarian or admin only).

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Query Parameters**:

   * ``days_overdue`` (int, optional): Filter loans overdue by at least this many days
   * ``skip`` (int, optional): Number of loans to skip (default: 0)
   * ``limit`` (int, optional): Maximum number of loans to return (default: 100)

   **Response**:

   .. code-block:: json

      {
        "total": 15,
        "items": [
          {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "user_id": "550e8400-e29b-41d4-a716-446655440001",
            "book_id": "550e8400-e29b-41d4-a716-446655440002",
            "loan_date": "2023-10-15T10:30:00Z",
            "due_date": "2023-11-15T10:30:00Z",
            "return_date": null,
            "status": "overdue",
            "renewal_count": 0,
            "days_overdue": 10,
            "user": {
              "id": "550e8400-e29b-41d4-a716-446655440001",
              "username": "johndoe",
              "email": "john@example.com"
            },
            "book": {
              "id": "550e8400-e29b-41d4-a716-446655440002",
              "title": "The Great Gatsby",
              "author": "F. Scott Fitzgerald"
            }
          }
        ]
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions 