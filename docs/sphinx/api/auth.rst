Authentication API
================

.. module:: revsin.api.routes.auth

The Authentication API provides endpoints for user authentication, registration, and token management.

Login
----

.. http:post:: /api/auth/login

   Authenticate a user and return a JWT token.

   **Request Body**:

   .. code-block:: json

      {
        "username": "johndoe",
        "password": "securepassword"
      }

   **Response**:

   .. code-block:: json

      {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "expires_in": 3600,
        "user": {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "username": "johndoe",
          "email": "john@example.com",
          "role": "member",
          "is_active": true
        }
      }

   :statuscode 200: Login successful
   :statuscode 401: Invalid credentials
   :statuscode 422: Validation error

Register
-------

.. http:post:: /api/auth/register

   Register a new user.

   **Request Body**:

   .. code-block:: json

      {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "securepassword",
        "full_name": "John Doe"
      }

   **Response**:

   .. code-block:: json

      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "johndoe",
        "email": "john@example.com",
        "role": "member",
        "is_active": true,
        "created_at": "2023-11-15T10:30:00Z"
      }

   :statuscode 201: User created successfully
   :statuscode 400: Username or email already exists
   :statuscode 422: Validation error

Refresh Token
-----------

.. http:post:: /api/auth/refresh

   Refresh an access token.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Response**:

   .. code-block:: json

      {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "expires_in": 3600
      }

   :statuscode 200: Token refreshed successfully
   :statuscode 401: Invalid or expired token

Verify Token
----------

.. http:post:: /api/auth/verify

   Verify a token's validity.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Response**:

   .. code-block:: json

      {
        "valid": true,
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "johndoe",
        "role": "member",
        "expires_at": "2023-11-15T11:30:00Z"
      }

   :statuscode 200: Token is valid
   :statuscode 401: Invalid or expired token

Change Password
-------------

.. http:post:: /api/auth/change-password

   Change the user's password.

   **Request Headers**:

   .. code-block:: text

      Authorization: Bearer <your_token>

   **Request Body**:

   .. code-block:: json

      {
        "current_password": "oldpassword",
        "new_password": "newpassword"
      }

   **Response**:

   .. code-block:: json

      {
        "message": "Password changed successfully"
      }

   :statuscode 200: Password changed successfully
   :statuscode 401: Invalid current password
   :statuscode 422: Validation error 