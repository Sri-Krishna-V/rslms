Users API
=========

.. module:: revsin.api.routes.users

The Users API provides endpoints for managing users in the system.

List Users
---------

.. http:get:: /api/users/

   Get a list of users.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Query Parameters**:

   * ``skip`` (int, optional): Number of users to skip (default: 0)
   * ``limit`` (int, optional): Maximum number of users to return (default: 100)
   * ``role`` (str, optional): Filter users by role (admin, librarian, member)
   * ``active`` (bool, optional): Filter users by active status

   **Response**:

   .. code-block:: json

      {
        "total": 120,
        "items": [
          {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "username": "johndoe",
            "email": "john@example.com",
            "role": "member",
            "is_active": true,
            "created_at": "2023-11-15T10:30:00Z"
          },
          {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "username": "janedoe",
            "email": "jane@example.com",
            "role": "librarian",
            "is_active": true,
            "created_at": "2023-11-14T09:15:00Z"
          }
        ]
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions

Get User
-------

.. http:get:: /api/users/(uuid:user_id)

   Get a specific user by ID.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "role": "member",
        "is_active": true,
        "created_at": "2023-11-15T10:30:00Z",
        "updated_at": "2023-11-15T10:30:00Z",
        "loans_count": 3
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 404: User not found

Create User
---------

.. http:post:: /api/users/

   Create a new user (admin only).

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Request Body**:

   .. code-block:: json

      {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword",
        "full_name": "New User",
        "role": "librarian",
        "is_active": true
      }

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "username": "newuser",
        "email": "newuser@example.com",
        "role": "librarian",
        "is_active": true,
        "created_at": "2023-11-16T14:20:00Z"
      }

   :statuscode 201: User created successfully
   :statuscode 400: Username or email already exists
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 422: Validation error

Update User
---------

.. http:put:: /api/users/(uuid:user_id)

   Update a user (admin only).

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Request Body**:

   .. code-block:: json

      {
        "email": "updated@example.com",
        "full_name": "Updated Name",
        "role": "librarian",
        "is_active": true
      }

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "johndoe",
        "email": "updated@example.com",
        "role": "librarian",
        "is_active": true,
        "updated_at": "2023-11-16T15:45:00Z"
      }

   :statuscode 200: User updated successfully
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 404: User not found
   :statuscode 422: Validation error

Delete User
---------

.. http:delete:: /api/users/(uuid:user_id)

   Delete a user (admin only).

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Response**:

   .. code-block:: json

      {
        "message": "User deleted successfully"
      }

   :statuscode 200: User deleted successfully
   :statuscode 401: Unauthorized
   :statuscode 403: Insufficient permissions
   :statuscode 404: User not found

Get Current User
--------------

.. http:get:: /api/users/me

   Get the current authenticated user.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "role": "member",
        "is_active": true,
        "created_at": "2023-11-15T10:30:00Z",
        "updated_at": "2023-11-15T10:30:00Z",
        "loans_count": 3
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized 