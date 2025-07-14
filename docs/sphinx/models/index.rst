Models Reference
==============

RevSin uses SQLAlchemy ORM models to represent the core entities in the system. This section documents all the models, their fields, relationships, and methods.

.. toctree::
   :maxdepth: 2
   :caption: Models:

   base
   user
   book
   loan

Model Architecture
----------------

All models in RevSin inherit from a common ``Base`` class, which provides common functionality such as:

* UUID primary key generation
* Created/updated timestamps
* Common serialization methods
* Audit logging

The models follow a clean architecture pattern, with:

* Clear separation of concerns
* Well-defined relationships
* Proper validation and constraints
* Optimized queries

Database Schema
-------------

The database schema consists of the following tables:

* ``users``: User accounts with authentication and role information
* ``books``: Book inventory with metadata and availability tracking
* ``loans``: Book loans with due dates, status, and relationships to users and books

Common Model Methods
-----------------

All models provide the following common methods:

* ``to_dict()``: Convert the model to a dictionary representation
* ``from_dict()``: Create a model instance from a dictionary
* ``to_schema()``: Convert the model to a Pydantic schema
* ``from_schema()``: Create a model instance from a Pydantic schema 