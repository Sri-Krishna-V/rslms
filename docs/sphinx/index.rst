Welcome to RevSin's Documentation! 🚀
=========================================

RevSin is a **comprehensive, modern Library Management System** built with FastAPI, PostgreSQL, and Redis. Designed for libraries of all sizes, it offers exceptional performance, beautiful interfaces, and delightful user experiences.

.. raw:: html

   <div style="text-align: center; margin: 20px 0;">
     <img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python" alt="Python 3.12+">
     <img src="https://img.shields.io/badge/FastAPI-Latest-green?style=for-the-badge&logo=fastapi" alt="FastAPI">
     <img src="https://img.shields.io/badge/PostgreSQL-14+-blue?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
     <img src="https://img.shields.io/badge/Redis-6+-red?style=for-the-badge&logo=redis" alt="Redis">
   </div>

🎯 **Quick Start**: Jump to :doc:`installation` → Create your first user → Start managing your library!

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   introduction
   installation

.. toctree::
   :maxdepth: 2
   :caption: User Guides:

   user_guide/index
   cli/index

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/index
   models/index
   crud/index
   auth/index

.. toctree::
   :maxdepth: 2
   :caption: Development:

   development/index
   deployment/index

🌟 Key Features
===============

**👥 User Management**
   Complete user lifecycle with role-based access control

**📚 Book Management** 
   Advanced book catalog with search, categories, and availability tracking

**📖 Loan Management**
   Streamlined borrowing with automated due dates and fine calculation

**🎨 Beautiful CLI**
   Interactive, colorful command-line interface with Rich formatting

**⚡ High Performance**
   Redis caching, optimized queries, and async processing

**🔐 Security First**
   JWT authentication, password hashing, and role-based authorization

**🚀 Production Ready**
   Docker support, comprehensive monitoring, and cloud deployment guides

🚀 Quick Tour
=============

**Install & Setup** (2 minutes)

.. code-block:: bash

   # Quick install with UV
   curl -LsSf https://astral.sh/uv/install.sh | sh
   git clone https://github.com/yourusername/revsin.git
   cd revsin && uv sync
   
   # Configure environment
   cp env.example .env  # Edit with your settings
   
   # Initialize system
   revsin system init-db
   revsin users create  # Create your admin user

**Start Using RevSin**

.. code-block:: bash

   # Beautiful CLI interface
   revsin system status     # Check health
   revsin books add        # Add books interactively
   revsin users list       # Manage users
   revsin loans stats      # View statistics
   
   # Start API server
   uvicorn src.revsin.main:app --reload
   # Visit http://localhost:8000/docs

🎨 CLI Showcase
===============

RevSin's CLI provides a **delightful terminal experience**:

.. code-block:: text

   $ revsin loans stats
   
   ┌─ 📊 Loan Statistics ─────────────────────┐
   │ Total Active Loans    │ 1,234           │
   │ Overdue Loans        │ 56 (4.5%)       │ 
   │ Due This Week        │ 89              │
   │ Popular Categories   │ Fiction, Tech    │
   │ Average Loan Period  │ 14.2 days       │
   └──────────────────────────────────────────┘
   
   $ revsin system init-db
   🚀 Initializing database...
   
   ⚡ Creating tables    ████████████████████ 100%
   📊 Seeding data      ████████████████████ 100% 
   🔧 Setting up cache  ████████████████████ 100%
   
   🎉 Database initialized successfully!

**CLI Features:**
* 🌈 Rich color coding and emojis
* 📊 Interactive tables and progress bars
* 🤖 Smart prompts with validation
* ✅ Confirmation dialogs for safety
* 🎉 Success animations and celebrations

🏗 Architecture Overview
========================

.. code-block:: text

   ┌─────────────────────────────────────────────────────┐
   │                    Client Layer                     │
   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
   │  │   Web App   │  │     CLI     │  │  Mobile App │ │
   │  └─────────────┘  └─────────────┘  └─────────────┘ │
   └─────────────────┬───────────────────────────────────┘
                     │
   ┌─────────────────▼───────────────────────────────────┐
   │                 FastAPI Server                      │
   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
   │  │ Auth Module │  │ API Routes  │  │ Middleware  │ │
   │  └─────────────┘  └─────────────┘  └─────────────┘ │
   └─────────────────┬───────────────────────────────────┘
                     │
   ┌─────────────────▼───────────────────────────────────┐
   │               Business Logic                        │
   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
   │  │    CRUD     │  │   Models    │  │   Schemas   │ │
   │  └─────────────┘  └─────────────┘  └─────────────┘ │
   └─────────────────┬───────────────────────────────────┘
                     │
   ┌─────────────────▼───────────────────────────────────┐
   │                Data Layer                           │
   │  ┌─────────────┐              ┌─────────────┐      │
   │  │ PostgreSQL  │              │    Redis    │      │
   │  │ (NeonDB)    │              │  (Upstash)  │      │
   │  └─────────────┘              └─────────────┘      │
   └─────────────────────────────────────────────────────┘

📚 Documentation Sections
==========================

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🚀 Getting Started
      :link: installation
      :link-type: doc

      Quick installation and setup guide to get RevSin running in minutes.

   .. grid-item-card:: 🎨 CLI Guide  
      :link: cli/index
      :link-type: doc

      Master the beautiful, interactive command-line interface.

   .. grid-item-card:: 🔌 API Reference
      :link: api/index
      :link-type: doc

      Complete REST API documentation with examples.

   .. grid-item-card:: 👥 User Guide
      :link: user_guide/index
      :link-type: doc

      Learn how to use all features effectively.

   .. grid-item-card:: 🏗 Development
      :link: development/index
      :link-type: doc

      Contributing, testing, and development setup.

   .. grid-item-card:: 🚀 Deployment
      :link: deployment/index
      :link-type: doc

      Production deployment and scaling guides.

🎯 User Roles & Capabilities
=============================

.. list-table::
   :header-rows: 1
   :widths: 20 25 25 30

   * - Role
     - Permissions
     - CLI Access
     - Typical Use Cases
   * - **👑 Admin**
     - Full system access
     - All commands
     - System management, user administration
   * - **📋 Librarian** 
     - Book & loan management
     - Books, loans, user assistance
     - Daily operations, inventory management
   * - **📖 Member**
     - Personal account only
     - Profile, loan history
     - Browse catalog, manage loans

💡 Common Workflows
===================

**📚 Daily Library Operations**

.. code-block:: bash

   # Morning routine
   revsin system status --detailed    # Health check
   revsin loans list --due-today      # Check due returns
   revsin books add                   # Add new acquisitions
   
   # Patron assistance
   revsin users search "john"         # Find user
   revsin books search "python"       # Find books
   revsin loans create                # Process borrowing

**🔧 System Administration**

.. code-block:: bash

   # System maintenance
   revsin system health               # Check all systems
   revsin system cache-stats          # Monitor cache
   revsin system backup-db            # Create backup
   
   # User management
   revsin users list --inactive       # Review inactive users
   revsin users bulk-import users.csv # Import from CSV

📊 Performance & Monitoring
============================

RevSin includes built-in monitoring and performance optimization:

* **📈 Real-time Metrics**: System health, response times, cache hit rates
* **⚡ Redis Caching**: Automatic caching with smart invalidation
* **🔍 Query Optimization**: Efficient database queries with proper indexing
* **📝 Comprehensive Logging**: Structured logging for debugging and monitoring

🤝 Community & Support
=======================

* **📖 Documentation**: Comprehensive guides and API references
* **🐛 Issue Tracking**: GitHub Issues for bugs and feature requests  
* **💬 Discussions**: GitHub Discussions for questions and ideas
* **🚀 Contributions**: Welcome! See our development guide

**Need Help?**

1. Check this documentation
2. Try ``revsin system doctor`` for diagnostics
3. Search GitHub Issues
4. Open a new issue with details

Indices and Tables
==================

* :ref:`genindex` - General Index
* :ref:`modindex` - Module Index  
* :ref:`search` - Search Documentation

---

.. raw:: html

   <div style="text-align: center; margin: 40px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;">
     <h3>🎉 Ready to Transform Your Library Management?</h3>
     <p><strong>Start with our <a href="installation.html">Installation Guide</a> and be up and running in minutes!</strong></p>
   </div> 