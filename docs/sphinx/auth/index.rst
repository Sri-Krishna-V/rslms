Authentication System
===================

RevSin uses a JWT-based authentication system to secure API endpoints. This section documents the authentication system components.

.. toctree::
   :maxdepth: 2
   :caption: Authentication:

   jwt_handler
   dependencies

Authentication Flow
-----------------

The authentication flow in RevSin works as follows:

1. A user logs in with their username and password via the ``/api/auth/login`` endpoint
2. If the credentials are valid, the system generates a JWT token
3. The client includes this token in the ``Authorization`` header of subsequent requests
4. The system validates the token and extracts the user information
5. Access is granted or denied based on the user's role and permissions

JWT Tokens
---------

JWT (JSON Web Token) is used for secure authentication:

* Tokens contain encoded user information (user ID, username, role)
* Tokens are signed with a secret key to prevent tampering
* Tokens have an expiration time for security
* Tokens can be refreshed using the ``/api/auth/refresh`` endpoint

Role-Based Access Control
-----------------------

RevSin implements role-based access control (RBAC) to restrict access to certain endpoints:

* ``ADMIN``: Full access to all endpoints
* ``LIBRARIAN``: Access to book and loan management endpoints
* ``MEMBER``: Access to borrowing books and managing their own account

Dependencies
----------

FastAPI dependencies are used to implement authentication and authorization:

* ``get_current_user``: Extracts and validates the user from the JWT token
* ``get_current_active_user``: Ensures the user is active
* ``get_current_admin_user``: Ensures the user is an admin
* ``get_current_librarian_user``: Ensures the user is a librarian or admin

Example Usage
-----------

Here's an example of using the authentication system in an API endpoint:

.. code-block:: python

   from fastapi import Depends
   from revsin.auth.dependencies import get_current_active_user
   from revsin.models.user import User
   
   @router.get("/api/users/me")
   async def get_current_user_info(
       current_user: User = Depends(get_current_active_user)
   ):
       """
       Get information about the current authenticated user.
       """
       return current_user 