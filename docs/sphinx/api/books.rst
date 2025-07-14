Books API
=========

.. module:: revsin.api.routes.books

The Books API provides endpoints for managing books in the library.

List Books
---------

.. http:get:: /api/books/

   Get a list of books.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Query Parameters**:

   * ``skip`` (int, optional): Number of books to skip (default: 0)
   * ``limit`` (int, optional): Maximum number of books to return (default: 100)
   * ``title`` (str, optional): Filter books by title (case-insensitive, partial match)
   * ``author`` (str, optional): Filter books by author (case-insensitive, partial match)
   * ``isbn`` (str, optional): Filter books by ISBN
   * ``category`` (str, optional): Filter books by category
   * ``available`` (bool, optional): Filter books by availability status

   **Response**:

   .. code-block:: json

      {
        "total": 250,
        "items": [
          {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "isbn": "9780743273565",
            "publication_year": 1925,
            "category": "Fiction",
            "available": true,
            "total_copies": 3,
            "available_copies": 2,
            "created_at": "2023-11-15T10:30:00Z"
          },
          {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "isbn": "9780061120084",
            "publication_year": 1960,
            "category": "Fiction",
            "available": true,
            "total_copies": 5,
            "available_copies": 3,
            "created_at": "2023-11-14T09:15:00Z"
          }
        ]
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized

Get Book
-------

.. http:get:: /api/books/(uuid:book_id)

   Get a specific book by ID.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565",
        "publication_year": 1925,
        "publisher": "Scribner",
        "category": "Fiction",
        "description": "The Great Gatsby is a 1925 novel by American writer F. Scott Fitzgerald...",
        "available": true,
        "total_copies": 3,
        "available_copies": 2,
        "created_at": "2023-11-15T10:30:00Z",
        "updated_at": "2023-11-15T10:30:00Z",
        "current_loans": 1
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized
   :statuscode 404: Book not found

Create Book
---------

.. http:post:: /api/books/

   Create a new book (librarian or admin only).

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Request Body**:

   .. code-block:: json

      {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "9780451524935",
        "publication_year": 1949,
        "publisher": "Signet Classics",
        "category": "Fiction",
        "description": "1984 is a dystopian novel by George Orwell...",
        "total_copies": 5
      }

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "title": "1984",
        "author": "George Orwell",
        "isbn": "9780451524935",
        "publication_year": 1949,
        "publisher": "Signet Classics",
        "category": "Fiction",
        "description": "1984 is a dystopian novel by George Orwell...",
        "available": true,
        "total_copies": 5,
        "available_copies": 5,
        "created_at": "2023-11-16T14:20:00Z"
      }

   :statuscode 201: Book created successfully
   :statuscode 400: ISBN already exists
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 422: Validation error

Update Book
---------

.. http:put:: /api/books/(uuid:book_id)

   Update a book (librarian or admin only).

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Request Body**:

   .. code-block:: json

      {
        "title": "Updated Title",
        "author": "Updated Author",
        "publisher": "Updated Publisher",
        "description": "Updated description...",
        "total_copies": 7
      }

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Updated Title",
        "author": "Updated Author",
        "isbn": "9780743273565",
        "publication_year": 1925,
        "publisher": "Updated Publisher",
        "category": "Fiction",
        "description": "Updated description...",
        "available": true,
        "total_copies": 7,
        "available_copies": 6,
        "updated_at": "2023-11-16T15:45:00Z"
      }

   :statuscode 200: Book updated successfully
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 404: Book not found
   :statuscode 422: Validation error

Delete Book
---------

.. http:delete:: /api/books/(uuid:book_id)

   Delete a book (admin only).

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Response**:

   .. code-block:: json

      {
        "message": "Book deleted successfully"
      }

   :statuscode 200: Book deleted successfully
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 404: Book not found
   :statuscode 409: Book has active loans

Search Books
----------

.. http:get:: /api/books/search

   Search for books using full-text search.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Query Parameters**:

   * ``query`` (str, required): Search query
   * ``skip`` (int, optional): Number of books to skip (default: 0)
   * ``limit`` (int, optional): Maximum number of books to return (default: 100)
   * ``category`` (str, optional): Filter by category
   * ``available`` (bool, optional): Filter by availability

   **Response**:

   .. code-block:: json

      {
        "total": 15,
        "items": [
          {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "isbn": "9780743273565",
            "publication_year": 1925,
            "category": "Fiction",
            "available": true,
            "total_copies": 3,
            "available_copies": 2,
            "created_at": "2023-11-15T10:30:00Z",
            "relevance_score": 0.89
          }
        ]
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized
   :statuscode 422: Validation error 