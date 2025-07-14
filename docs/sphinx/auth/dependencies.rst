Authentication Dependencies
======================

.. module:: revsin.auth.dependencies

The Authentication Dependencies module provides FastAPI dependencies for authentication and authorization.

Get Current User
--------------

.. autofunction:: get_current_user

   Extracts and validates the current user from the JWT token in the request.

   **Parameters**:

   * ``token``: The JWT token from the Authorization header

   **Returns**:

   * The current user if the token is valid

   **Raises**:

   * ``HTTPException 401``: If the token is missing, invalid, or expired
   * ``HTTPException 404``: If the user is not found in the database

   **Example Usage**:

   .. code-block:: python

      from fastapi import Depends
      from revsin.auth.dependencies import get_current_user
      from revsin.models.user import User
      
      @router.get("/api/protected")
      async def protected_route(
          current_user: User = Depends(get_current_user)
      ):
          return {"message": f"Hello, {current_user.username}!"}

Get Current Active User
---------------------

.. autofunction:: get_current_active_user

   Ensures the current user is active.

   **Parameters**:

   * ``current_user``: The current user from ``get_current_user``

   **Returns**:

   * The current user if active

   **Raises**:

   * ``HTTPException 400``: If the user is inactive

   **Example Usage**:

   .. code-block:: python

      from fastapi import Depends
      from revsin.auth.dependencies import get_current_active_user
      from revsin.models.user import User
      
      @router.get("/api/users/me")
      async def get_my_info(
          current_user: User = Depends(get_current_active_user)
      ):
          return current_user

Get Current Admin User
--------------------

.. autofunction:: get_current_admin_user

   Ensures the current user is an admin.

   **Parameters**:

   * ``current_user``: The current user from ``get_current_active_user``

   **Returns**:

   * The current user if admin

   **Raises**:

   * ``HTTPException 403``: If the user is not an admin

   **Example Usage**:

   .. code-block:: python

      from fastapi import Depends
      from revsin.auth.dependencies import get_current_admin_user
      from revsin.models.user import User
      
      @router.post("/api/admin/settings")
      async def update_settings(
          settings: dict,
          current_user: User = Depends(get_current_admin_user)
      ):
          # Only admins can access this endpoint
          return {"message": "Settings updated"}

Get Current Librarian User
------------------------

.. autofunction:: get_current_librarian_user

   Ensures the current user is a librarian or admin.

   **Parameters**:

   * ``current_user``: The current user from ``get_current_active_user``

   **Returns**:

   * The current user if librarian or admin

   **Raises**:

   * ``HTTPException 403``: If the user is not a librarian or admin

   **Example Usage**:

   .. code-block:: python

      from fastapi import Depends
      from revsin.auth.dependencies import get_current_librarian_user
      from revsin.models.user import User
      
      @router.post("/api/books/")
      async def create_book(
          book_data: dict,
          current_user: User = Depends(get_current_librarian_user)
      ):
          # Only librarians and admins can create books
          return {"message": "Book created"}

OAuth2 Scheme
-----------

.. autodata:: oauth2_scheme

   The OAuth2 password bearer scheme used to extract the JWT token from the Authorization header.

   **Example Usage**:

   .. code-block:: python

      from fastapi import Depends
      from revsin.auth.dependencies import oauth2_scheme
      
      @router.get("/api/token-info")
      async def get_token_info(
          token: str = Depends(oauth2_scheme)
      ):
          return {"token": token}

Dependency Chain
--------------

The authentication dependencies form a chain of validation:

1. ``oauth2_scheme``: Extracts the token from the Authorization header
2. ``get_current_user``: Validates the token and retrieves the user
3. ``get_current_active_user``: Ensures the user is active
4. ``get_current_admin_user`` or ``get_current_librarian_user``: Ensures the user has the required role

This chain allows for progressive validation of user authentication and authorization. 