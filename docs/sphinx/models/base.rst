Base Model
==========

.. module:: revsin.models.base

The Base model provides common functionality for all models in the RevSin system.

Base Class
---------

.. autoclass:: Base
   :members:
   :undoc-members:
   :show-inheritance:

   The ``Base`` class is the foundation for all models in the RevSin system. It provides common fields and methods that are used by all models.

   **Common Fields**:

   * ``id``: UUID primary key, automatically generated
   * ``created_at``: Timestamp when the record was created
   * ``updated_at``: Timestamp when the record was last updated

   **Common Methods**:

   * ``to_dict()``: Convert the model to a dictionary representation
   * ``from_dict()``: Create a model instance from a dictionary
   * ``to_schema()``: Convert the model to a Pydantic schema
   * ``from_schema()``: Create a model instance from a Pydantic schema

   **Example Usage**:

   .. code-block:: python

      # Create a new model instance
      user = User(username="johndoe", email="john@example.com")
      
      # Convert to dictionary
      user_dict = user.to_dict()
      
      # Convert to schema
      user_schema = user.to_schema()
      
      # Create from dictionary
      user = User.from_dict(user_dict)
      
      # Create from schema
      user = User.from_schema(user_schema)

TimestampMixin
-------------

.. autoclass:: TimestampMixin
   :members:
   :undoc-members:
   :show-inheritance:

   The ``TimestampMixin`` adds created_at and updated_at timestamps to models.

   **Fields**:

   * ``created_at``: Timestamp when the record was created
   * ``updated_at``: Timestamp when the record was last updated

   **Example Usage**:

   .. code-block:: python

      class MyModel(Base, TimestampMixin):
          __tablename__ = "my_models"
          name = Column(String, nullable=False)
          
      # The created_at and updated_at fields will be automatically set
      model = MyModel(name="Test")
      db.add(model)
      db.commit()

UUIDMixin
--------

.. autoclass:: UUIDMixin
   :members:
   :undoc-members:
   :show-inheritance:

   The ``UUIDMixin`` adds a UUID primary key to models.

   **Fields**:

   * ``id``: UUID primary key, automatically generated

   **Example Usage**:

   .. code-block:: python

      class MyModel(Base, UUIDMixin):
          __tablename__ = "my_models"
          name = Column(String, nullable=False)
          
      # The id field will be automatically set to a UUID
      model = MyModel(name="Test")
      db.add(model)
      db.commit()

SerializationMixin
----------------

.. autoclass:: SerializationMixin
   :members:
   :undoc-members:
   :show-inheritance:

   The ``SerializationMixin`` adds methods for serializing and deserializing models.

   **Methods**:

   * ``to_dict()``: Convert the model to a dictionary representation
   * ``from_dict()``: Create a model instance from a dictionary
   * ``to_schema()``: Convert the model to a Pydantic schema
   * ``from_schema()``: Create a model instance from a Pydantic schema

   **Example Usage**:

   .. code-block:: python

      class MyModel(Base, SerializationMixin):
          __tablename__ = "my_models"
          id = Column(UUID, primary_key=True, default=uuid.uuid4)
          name = Column(String, nullable=False)
          
      # Convert to dictionary
      model = MyModel(name="Test")
      model_dict = model.to_dict()
      
      # Create from dictionary
      model = MyModel.from_dict({"name": "Test"}) 