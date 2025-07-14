Developer Guide
==============

This section provides a comprehensive guide for developers working with the RevSin codebase.

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide:

   architecture
   contributing
   testing
   code_style
   extending

Architecture Overview
------------------

RevSin follows a clean, modular architecture:

* **API Layer**: FastAPI-based REST API endpoints
* **Business Logic Layer**: CRUD operations and service functions
* **Data Access Layer**: SQLAlchemy ORM models and database connections
* **Authentication**: JWT-based authentication system
* **CLI**: Command-line interface for administrative tasks
* **Caching**: Redis-based caching for improved performance

For a detailed architecture overview, see the :doc:`architecture` guide.

Project Structure
---------------

The RevSin project is structured as follows:

.. code-block:: text

   revsin/
   ├── src/
   │   └── revsin/
   │       ├── api/                # API endpoints
   │       │   └── routes/         # API route definitions
   │       ├── auth/               # Authentication system
   │       ├── cli/                # Command-line interface
   │       │   └── commands/       # CLI command definitions
   │       ├── crud/               # CRUD operations
   │       ├── database/           # Database connections
   │       ├── models/             # SQLAlchemy models
   │       └── schemas/            # Pydantic schemas
   ├── tests/                      # Test suite
   ├── docs/                       # Documentation
   ├── alembic/                    # Database migrations
   └── scripts/                    # Utility scripts

Development Setup
--------------

To set up a development environment for RevSin:

1. Clone the repository
2. Create and activate a virtual environment
3. Install the package in development mode:

   .. code-block:: bash

      pip install -e ".[dev,docs]"

4. Set up environment variables:

   .. code-block:: bash

      cp env.example .env

5. Run database migrations:

   .. code-block:: bash

      alembic upgrade head

6. Start the development server:

   .. code-block:: bash

      uvicorn revsin.main:app --reload

For more detailed setup instructions, see the :doc:`../installation` guide.

Contributing
----------

We welcome contributions to RevSin! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

For detailed contribution guidelines, see the :doc:`contributing` guide.

Testing
------

RevSin uses pytest for testing. To run the tests:

.. code-block:: bash

   pytest

For more information on testing, see the :doc:`testing` guide.

Code Style
--------

RevSin follows the Black code style and uses various linting tools:

* Black for code formatting
* isort for import sorting
* flake8 for linting
* mypy for type checking

To check code style:

.. code-block:: bash

   black --check src tests
   isort --check src tests
   flake8 src tests
   mypy src

For more information on code style, see the :doc:`code_style` guide.

Extending RevSin
--------------

RevSin is designed to be extensible. You can:

* Add new API endpoints
* Create new CLI commands
* Add new models and schemas
* Implement new features

For guidance on extending RevSin, see the :doc:`extending` guide. 