JWT Handler
===========

.. module:: revsin.auth.jwt_handler

The JWT Handler module provides functions for creating, decoding, and validating JWT tokens.

Token Creation
------------

.. autofunction:: create_access_token

   Creates a JWT access token for a user.

   **Parameters**:

   * ``data``: Dictionary containing the data to encode in the token
   * ``expires_delta``: Optional expiration time delta (defaults to 30 minutes)

   **Returns**:

   * A JWT token string

   **Example Usage**:

   .. code-block:: python

      from revsin.auth.jwt_handler import create_access_token
      from datetime import timedelta
      
      # Create token with default expiration (30 minutes)
      token_data = {"sub": user.username, "id": str(user.id), "role": user.role}
      token = create_access_token(data=token_data)
      
      # Create token with custom expiration (1 hour)
      token = create_access_token(
          data=token_data,
          expires_delta=timedelta(hours=1)
      )

Token Decoding
------------

.. autofunction:: decode_token

   Decodes and validates a JWT token.

   **Parameters**:

   * ``token``: The JWT token to decode

   **Returns**:

   * The decoded token payload

   **Raises**:

   * ``HTTPException``: If the token is invalid or expired

   **Example Usage**:

   .. code-block:: python

      from revsin.auth.jwt_handler import decode_token
      from fastapi import HTTPException
      
      try:
          # Decode and validate token
          payload = decode_token(token)
          
          # Extract user information from payload
          username = payload.get("sub")
          user_id = payload.get("id")
          user_role = payload.get("role")
      except HTTPException as e:
          # Handle invalid or expired token
          print(f"Token error: {e.detail}")

Token Configuration
----------------

JWT tokens are configured using the following settings from the application config:

* ``SECRET_KEY``: Secret key used to sign the tokens
* ``ALGORITHM``: Algorithm used for token signing (default: "HS256")
* ``ACCESS_TOKEN_EXPIRE_MINUTES``: Default token expiration time in minutes

These settings can be configured in the ``.env`` file:

.. code-block:: text

   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

Security Considerations
--------------------

When working with JWT tokens, consider the following security best practices:

1. **Secret Key Security**:
   
   * Use a strong, randomly generated secret key
   * Keep the secret key secure and never expose it in client-side code
   * Rotate the secret key periodically

2. **Token Expiration**:
   
   * Use short-lived tokens (30-60 minutes) to minimize the impact of token theft
   * Implement token refresh mechanisms for longer sessions

3. **Token Payload**:
   
   * Only include necessary information in the token payload
   * Never include sensitive information like passwords
   * Keep the payload small to minimize overhead

4. **HTTPS**:
   
   * Always transmit tokens over HTTPS to prevent interception

5. **Token Storage**:
   
   * Store tokens securely on the client side (e.g., HttpOnly cookies)
   * Implement proper token invalidation on logout 