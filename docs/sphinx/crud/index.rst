CRUD Operations
==============

RevSin uses a set of CRUD (Create, Read, Update, Delete) operations to interact with the database. This section documents the CRUD operations for each entity in the system.

.. toctree::
   :maxdepth: 2
   :caption: CRUD Operations:

   base
   user
   book
   loan

CRUD Architecture
---------------

The CRUD operations in RevSin follow a consistent pattern:

* Each entity has its own CRUD module
* All CRUD modules inherit from a base CRUD class
* Operations are implemented as async methods
* Proper error handling and validation are included
* Database transactions are used where appropriate

Common CRUD Operations
-------------------

All CRUD modules provide the following common operations:

* ``get(id)``: Get a single entity by ID
* ``get_multi(skip, limit, **filters)``: Get multiple entities with pagination and filtering
* ``create(obj_in)``: Create a new entity
* ``update(id, obj_in)``: Update an existing entity
* ``delete(id)``: Delete an entity

These operations are implemented in the base CRUD class and can be customized in the entity-specific CRUD modules as needed.

Example Usage
-----------

Here's an example of using the CRUD operations:

.. code-block:: python

   from revsin.crud.user import user_crud
   from revsin.schemas.user import UserCreate, UserUpdate
   
   # Create a new user
   user_create = UserCreate(
       username="johndoe",
       email="john@example.com",
       password="securepassword",
       full_name="John Doe",
       role="member"
   )
   user = await user_crud.create(user_create)
   
   # Get a user by ID
   user = await user_crud.get(user_id)
   
   # Get multiple users with filtering
   users = await user_crud.get_multi(
       skip=0,
       limit=10,
       role="member",
       is_active=True
   )
   
   # Update a user
   user_update = UserUpdate(
       email="newemail@example.com",
       full_name="John Smith"
   )
   updated_user = await user_crud.update(user_id, user_update)
   
   # Delete a user
   deleted = await user_crud.delete(user_id) 