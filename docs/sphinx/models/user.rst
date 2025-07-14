User Model
==========

.. module:: revsin.models.user

The User model represents user accounts in the RevSin system.

User Class
---------

.. autoclass:: User
   :members:
   :undoc-members:
   :show-inheritance:

   The ``User`` class represents a user account in the system.

   **Fields**:

   * ``id``: UUID primary key, automatically generated
   * ``username``: Unique username for the user
   * ``email``: Unique email address for the user
   * ``hashed_password``: Hashed password for the user (not directly accessible)
   * ``full_name``: Full name of the user
   * ``role``: Role of the user (admin, librarian, member)
   * ``is_active``: Whether the user account is active
   * ``created_at``: Timestamp when the user was created
   * ``updated_at``: Timestamp when the user was last updated
   * ``loans``: Relationship to the user's loans

   **Methods**:

   * ``verify_password(plain_password)``: Verify if the provided password matches the stored hashed password
   * ``set_password(plain_password)``: Set a new password for the user
   * ``to_dict()``: Convert the user to a dictionary representation
   * ``from_dict()``: Create a user instance from a dictionary
   * ``to_schema()``: Convert the user to a Pydantic schema
   * ``from_schema()``: Create a user instance from a Pydantic schema

   **Example Usage**:

   .. code-block:: python

      # Create a new user
      user = User(
          username="johndoe",
          email="john@example.com",
          full_name="John Doe",
          role="member"
      )
      user.set_password("securepassword")
      
      # Verify password
      is_valid = user.verify_password("securepassword")
      
      # Get user loans
      user_loans = user.loans

UserRole Enum
-----------

.. autoclass:: UserRole
   :members:
   :undoc-members:
   :show-inheritance:

   The ``UserRole`` enum defines the possible roles for users in the system.

   **Values**:

   * ``ADMIN``: Administrator role with full access to all features
   * ``LIBRARIAN``: Librarian role with access to book and loan management
   * ``MEMBER``: Member role with access to borrowing books and managing their own account

   **Example Usage**:

   .. code-block:: python

      # Create a user with admin role
      admin_user = User(
          username="admin",
          email="admin@example.com",
          role=UserRole.ADMIN
      )
      
      # Check if a user is an admin
      if user.role == UserRole.ADMIN:
          # Perform admin-only operations
          pass

Password Handling
---------------

The User model includes secure password handling using the passlib library:

* Passwords are hashed using bcrypt with appropriate work factors
* Password verification is done securely using constant-time comparison
* Plain text passwords are never stored in the database

Example of password handling:

.. code-block:: python

   # Setting a password
   user = User(username="johndoe", email="john@example.com")
   user.set_password("securepassword")
   
   # Verifying a password
   if user.verify_password("securepassword"):
       # Password is correct
       pass
   else:
       # Password is incorrect
       pass

Role-Based Access Control
-----------------------

The User model supports role-based access control through the ``role`` field:

* ``ADMIN``: Full access to all features
* ``LIBRARIAN``: Access to book and loan management
* ``MEMBER``: Access to borrowing books and managing their own account

Example of role-based access control:

.. code-block:: python

   # Check if a user has sufficient permissions
   if user.role in [UserRole.ADMIN, UserRole.LIBRARIAN]:
       # Allow access to librarian features
       pass
   elif user.role == UserRole.MEMBER:
       # Allow access to member features
       pass
   else:
       # Deny access
       pass 