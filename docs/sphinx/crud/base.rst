Base CRUD
=========

.. module:: revsin.crud.base

The Base CRUD module provides common CRUD operations that are inherited by all entity-specific CRUD modules.

CRUDBase Class
------------

.. autoclass:: CRUDBase
   :members:
   :undoc-members:
   :show-inheritance:

   The ``CRUDBase`` class is a generic class that provides common CRUD operations for all entities.

   **Type Parameters**:

   * ``ModelType``: The SQLAlchemy model type
   * ``CreateSchemaType``: The Pydantic schema type for create operations
   * ``UpdateSchemaType``: The Pydantic schema type for update operations

   **Methods**:

   * ``get(id)``: Get a single entity by ID
   * ``get_multi(skip, limit, **filters)``: Get multiple entities with pagination and filtering
   * ``create(obj_in)``: Create a new entity
   * ``update(id, obj_in)``: Update an existing entity
   * ``delete(id)``: Delete an entity
   * ``count(**filters)``: Count entities with filtering

   **Example Usage**:

   .. code-block:: python

      from revsin.crud.base import CRUDBase
      from revsin.models.user import User
      from revsin.schemas.user import UserCreate, UserUpdate
      
      class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
          # Custom user-specific CRUD operations can be added here
          pass
      
      user_crud = CRUDUser(User)

Get Operation
-----------

The ``get`` method retrieves a single entity by its ID:

.. code-block:: python

   async def get(self, id: Any) -> Optional[ModelType]:
       """
       Get a single entity by ID.
       
       Args:
           id: The ID of the entity to retrieve
           
       Returns:
           The entity if found, None otherwise
       """
       query = select(self.model).where(self.model.id == id)
       result = await self.db.execute(query)
       return result.scalars().first()

Example usage:

.. code-block:: python

   # Get a user by ID
   user = await user_crud.get(user_id)
   
   if user:
       # User found
       print(f"Found user: {user.username}")
   else:
       # User not found
       print("User not found")

Get Multiple Operation
-------------------

The ``get_multi`` method retrieves multiple entities with pagination and filtering:

.. code-block:: python

   async def get_multi(
       self, 
       skip: int = 0, 
       limit: int = 100, 
       **filters
   ) -> List[ModelType]:
       """
       Get multiple entities with pagination and filtering.
       
       Args:
           skip: Number of entities to skip
           limit: Maximum number of entities to return
           **filters: Filter parameters
           
       Returns:
           List of entities
       """
       query = select(self.model)
       
       # Apply filters
       for field, value in filters.items():
           if hasattr(self.model, field):
               query = query.where(getattr(self.model, field) == value)
       
       # Apply pagination
       query = query.offset(skip).limit(limit)
       
       result = await self.db.execute(query)
       return result.scalars().all()

Example usage:

.. code-block:: python

   # Get active members with pagination
   users = await user_crud.get_multi(
       skip=0,
       limit=10,
       role="member",
       is_active=True
   )
   
   # Process the users
   for user in users:
       print(f"User: {user.username}, Email: {user.email}")

Create Operation
-------------

The ``create`` method creates a new entity:

.. code-block:: python

   async def create(self, obj_in: CreateSchemaType) -> ModelType:
       """
       Create a new entity.
       
       Args:
           obj_in: The data to create the entity with
           
       Returns:
           The created entity
       """
       # Convert Pydantic model to dict
       obj_in_data = obj_in.model_dump()
       
       # Create SQLAlchemy model instance
       db_obj = self.model(**obj_in_data)
       
       # Add to database and commit
       self.db.add(db_obj)
       await self.db.commit()
       await self.db.refresh(db_obj)
       
       return db_obj

Example usage:

.. code-block:: python

   # Create a new user
   user_create = UserCreate(
       username="johndoe",
       email="john@example.com",
       password="securepassword",
       full_name="John Doe",
       role="member"
   )
   user = await user_crud.create(user_create)
   
   print(f"Created user with ID: {user.id}")

Update Operation
-------------

The ``update`` method updates an existing entity:

.. code-block:: python

   async def update(
       self, 
       id: Any, 
       obj_in: Union[UpdateSchemaType, Dict[str, Any]]
   ) -> Optional[ModelType]:
       """
       Update an entity.
       
       Args:
           id: The ID of the entity to update
           obj_in: The data to update the entity with
           
       Returns:
           The updated entity if found, None otherwise
       """
       # Get the entity
       db_obj = await self.get(id)
       if not db_obj:
           return None
       
       # Convert input to dict if it's a Pydantic model
       update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
       
       # Update the entity
       for field, value in update_data.items():
           if hasattr(db_obj, field):
               setattr(db_obj, field, value)
       
       # Commit changes
       self.db.add(db_obj)
       await self.db.commit()
       await self.db.refresh(db_obj)
       
       return db_obj

Example usage:

.. code-block:: python

   # Update a user
   user_update = UserUpdate(
       email="newemail@example.com",
       full_name="John Smith"
   )
   updated_user = await user_crud.update(user_id, user_update)
   
   if updated_user:
       print(f"Updated user: {updated_user.username}")
   else:
       print("User not found")

Delete Operation
-------------

The ``delete`` method deletes an entity:

.. code-block:: python

   async def delete(self, id: Any) -> bool:
       """
       Delete an entity.
       
       Args:
           id: The ID of the entity to delete
           
       Returns:
           True if the entity was deleted, False otherwise
       """
       # Get the entity
       db_obj = await self.get(id)
       if not db_obj:
           return False
       
       # Delete the entity
       await self.db.delete(db_obj)
       await self.db.commit()
       
       return True

Example usage:

.. code-block:: python

   # Delete a user
   deleted = await user_crud.delete(user_id)
   
   if deleted:
       print("User deleted successfully")
   else:
       print("User not found") 