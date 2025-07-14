Installation
============

RevSin can be installed in multiple ways depending on your environment and use case. This guide covers all installation methods from development to production deployment.

Prerequisites
------------

**System Requirements:**

* **Python**: 3.12 or higher (recommended: 3.12+)
* **Database**: PostgreSQL 14+ (or NeonDB account)
* **Cache**: Redis 6+ (or Upstash Redis account)
* **Package Manager**: UV (recommended) or pip
* **Git**: For cloning the repository

**Optional but Recommended:**

* **Docker**: For containerized deployment
* **Node.js**: For frontend development (if building a web interface)

Installation Methods
-------------------

Method 1: Quick Install with UV (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UV is a fast Python package manager. Install it first:

.. code-block:: bash

   # Install UV
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # or
   pip install uv

Then install RevSin:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/yourusername/revsin.git
   cd revsin
   
   # Install with all dependencies
   uv sync
   
   # Activate the virtual environment
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows

Method 2: Standard pip Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/yourusername/revsin.git
   cd revsin
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate    # Linux/macOS
   # or
   venv\Scripts\activate       # Windows
   
   # Install dependencies
   pip install -e ".[dev,docs]"

Method 3: Docker Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/yourusername/revsin.git
   cd revsin
   
   # Build and run with Docker Compose
   docker-compose up -d
   
   # Access the application at http://localhost:8000

Configuration Setup
-----------------

1. **Environment Configuration**

   Copy the example environment file:

   .. code-block:: bash

      cp env.example .env

   Edit the `.env` file with your specific configuration:

   .. code-block:: bash

      # Database Configuration
      DATABASE_URL=postgresql://username:password@localhost:5432/revsin
      
      # Redis Configuration  
      REDIS_URL=redis://localhost:6379
      
      # Application Configuration
      SECRET_KEY=your-super-secret-key-change-this-in-production
      ENVIRONMENT=development

2. **Database Setup**

   Initialize the database:

   .. code-block:: bash

      # Create database tables
      revsin system init-db
      
      # Verify database connection
      revsin system status

3. **Create Admin User**

   .. code-block:: bash

      # Interactive user creation
      revsin users create
      
      # Follow prompts to create an admin user

Development Installation
-----------------------

For contributors and developers:

.. code-block:: bash

   # Clone with development tools
   git clone https://github.com/yourusername/revsin.git
   cd revsin
   
   # Install with development dependencies
   uv sync -G dev -G docs -G test
   
   # Install pre-commit hooks
   pre-commit install
   
   # Run tests to verify installation
   pytest
   
   # Start development server
   uvicorn src.revsin.main:app --reload

**Development Dependencies Include:**

* **Testing**: pytest, pytest-asyncio, httpx
* **Code Quality**: black, isort, flake8, mypy
* **Documentation**: sphinx, sphinx-rtd-theme
* **Pre-commit**: Automated code formatting and linting

Cloud Deployment Setup
---------------------

**NeonDB (Recommended for PostgreSQL):**

1. Create account at `neon.tech <https://neon.tech>`_
2. Create a new database
3. Copy connection string to `DATABASE_URL` in `.env`

**Upstash Redis (Recommended for Redis):**

1. Create account at `upstash.com <https://upstash.com>`_
2. Create a new Redis database
3. Copy connection string to `REDIS_URL` in `.env`

**Environment Variables for Production:**

.. code-block:: bash

   # Production settings
   ENVIRONMENT=production
   DEBUG=false
   HTTPS_ONLY=true
   
   # Security
   SECRET_KEY=<strong-random-key>
   
   # Logging
   LOG_LEVEL=INFO

Verification
-----------

Verify your installation:

.. code-block:: bash

   # Check CLI availability
   revsin --version
   
   # Test system health
   revsin system health
   
   # Start the API server
   uvicorn src.revsin.main:app --host 0.0.0.0 --port 8000
   
   # Test API (in another terminal)
   curl http://localhost:8000/health

You should see:

* ✅ CLI commands working
* ✅ Database connection successful  
* ✅ Redis connection successful
* ✅ API server running on port 8000

Common Installation Issues
------------------------

**Database Connection Issues:**

.. code-block:: bash

   # Check database URL format
   DATABASE_URL=postgresql://user:password@host:port/database
   
   # Test connection
   revsin system doctor

**Redis Connection Issues:**

.. code-block:: bash

   # Check Redis URL format
   REDIS_URL=redis://user:password@host:port
   
   # Test Redis connection
   revsin system status --detailed

**Permission Issues:**

.. code-block:: bash

   # Ensure proper file permissions
   chmod +x cli.py
   
   # Recreate virtual environment if needed
   rm -rf venv
   python -m venv venv

**Python Version Issues:**

.. code-block:: bash

   # Check Python version
   python --version  # Should be 3.12+
   
   # Use specific Python version
   python3.12 -m venv venv

Production Installation
---------------------

For production deployment:

.. code-block:: bash

   # Install production dependencies only
   uv sync --no-dev
   
   # Set production environment variables
   export ENVIRONMENT=production
   export DEBUG=false
   
   # Run with Gunicorn
   gunicorn src.revsin.main:app -w 4 -k uvicorn.workers.UvicornWorker

**Production Checklist:**

* ✅ Use strong SECRET_KEY
* ✅ Set ENVIRONMENT=production
* ✅ Configure HTTPS_ONLY=true
* ✅ Set up proper logging
* ✅ Configure CORS origins
* ✅ Set up monitoring
* ✅ Regular database backups

Next Steps
---------

After installation:

1. **Explore the CLI**: :doc:`cli/index`
2. **Read the User Guide**: :doc:`user_guide/index`
3. **API Documentation**: :doc:`api/index`
4. **Deploy to Production**: :doc:`deployment/index`

**Quick Start Commands:**

.. code-block:: bash

   # Create your first user
   revsin users create
   
   # Add some books
   revsin books add
   
   # Check system status
   revsin system status
   
   # Start the API server
   uvicorn src.revsin.main:app --reload

Need help? Check our :doc:`development/index` guide or open an issue on GitHub! 