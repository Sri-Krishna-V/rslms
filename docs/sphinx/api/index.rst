API Reference
============

RevSin provides a comprehensive REST API for interacting with the library management system. This section documents all available API endpoints, their parameters, and responses.

.. toctree::
   :maxdepth: 2
   :caption: API Routes:

   auth
   users
   books
   loans

Authentication
-------------

Most API endpoints require authentication using JWT tokens. To authenticate:

1. Obtain a token by calling the ``/api/auth/login`` endpoint with valid credentials
2. Include the token in the ``Authorization`` header of subsequent requests:

   .. code-block:: text

      Authorization: Bearer <your_token>

Rate Limiting
-----------

API endpoints are rate-limited to prevent abuse. The current limits are:

* Authentication endpoints: 5 requests per minute
* User endpoints: 60 requests per minute
* Book endpoints: 120 requests per minute
* Loan endpoints: 60 requests per minute

Exceeding these limits will result in a 429 Too Many Requests response.

Error Handling
------------

API errors are returned as JSON responses with the following structure:

.. code-block:: json

   {
     "detail": {
       "message": "Error message",
       "code": "ERROR_CODE"
     }
   }

Common error codes include:

* ``AUTHENTICATION_ERROR``: Invalid or expired token
* ``PERMISSION_DENIED``: Insufficient permissions
* ``RESOURCE_NOT_FOUND``: Requested resource not found
* ``VALIDATION_ERROR``: Invalid request parameters
* ``RATE_LIMIT_EXCEEDED``: Too many requests 