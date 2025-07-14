Command-Line Interface
====================

RevSin provides a comprehensive, **colorful, and interactive** command-line interface (CLI) for administrative tasks and batch operations. Built with Click and Rich, the CLI offers a delightful user experience with beautiful formatting, progress indicators, and smart interactions.

.. toctree::
   :maxdepth: 2
   :caption: CLI Commands:

   system
   users
   books
   loans

🎨 CLI Features
--------------

**Visual Excellence**
* 🌈 **Rich Color Coding**: Success (green ✓), errors (red ✗), warnings (yellow ⚠), info (blue ℹ)
* 🎭 **ASCII Art**: Beautiful banners and celebration animations
* 📊 **Formatted Tables**: Bordered tables with proper alignment and sorting
* 🎨 **Styled Panels**: Information displayed in attractive bordered panels

**Interactive Experience**
* 🤖 **Smart Prompts**: Interactive prompts for missing parameters with validation
* 🔒 **Secure Input**: Password masking for sensitive information
* ✅ **Confirmation Dialogs**: Safety confirmations for destructive operations
* 📋 **Choice Menus**: Interactive selection menus for roles, statuses, and options

**Progress & Feedback**
* ⚡ **Progress Spinners**: Context-aware spinners for operations
* 📈 **Progress Bars**: Visual progress indicators with time estimates
* 🎉 **Success Animations**: Celebration displays for completed operations
* 📊 **Statistics Panels**: Beautiful data summaries with metrics

**User Experience**
* 💡 **Context-Aware Help**: Detailed help with real examples
* 🔍 **Input Validation**: Real-time validation with helpful error messages
* 🎯 **Auto-completion**: Tab completion for commands and options
* 📝 **Command History**: Access to previous commands and patterns

CLI Architecture
--------------

The RevSin CLI follows a modular, extensible architecture:

**Command Groups**
* ``system`` - System administration and maintenance
* ``users`` - User management operations  
* ``books`` - Book inventory management
* ``loans`` - Loan tracking and management

**Shared Components**
* **Rich Console**: Centralized formatting and styling
* **Error Handling**: Consistent error reporting with context
* **Database Sessions**: Automatic session management
* **Configuration**: Environment-aware settings

**Utility Functions**
* Progress indicators and spinners
* Interactive prompts and confirmations
* Table formatting and data display
* ASCII art and celebrations

Installation
----------

The CLI is automatically installed when you install RevSin:

.. code-block:: bash

   # Install with UV (recommended)
   uv install -e .
   
   # Or with pip
   pip install -e .

This makes the ``revsin`` command available globally in your terminal.

Basic Usage
-----------

The CLI follows an intuitive command structure:

.. code-block:: bash

   revsin [GROUP] [COMMAND] [OPTIONS] [ARGUMENTS]

**Examples:**

.. code-block:: bash

   # System operations
   revsin system status              # Check system health
   revsin system init-db            # Initialize database
   revsin system reset-cache        # Clear Redis cache
   
   # User management
   revsin users create              # Create new user (interactive)
   revsin users list --role admin  # List admin users
   revsin users activate <user-id> # Activate user account
   
   # Book operations  
   revsin books add                 # Add book (interactive)
   revsin books search "python"    # Search books
   revsin books update <book-id>    # Update book details
   
   # Loan management
   revsin loans list --overdue      # Show overdue loans
   revsin loans return <loan-id>    # Process book return
   revsin loans stats               # Display loan statistics

Interactive Features
-------------------

**Smart Prompts**

When required information is missing, the CLI will prompt you interactively:

.. code-block:: bash

   $ revsin users create
   📝 Creating a new user...
   
   👤 Enter user details:
   Email: john@example.com
   Password: ••••••••
   First Name: John
   Last Name: Doe
   Role [member/librarian/admin]: member
   
   ✅ User created successfully!

**Progress Indicators**

Long-running operations show beautiful progress indicators:

.. code-block:: bash

   $ revsin system init-db
   🚀 Initializing database...
   
   ⚡ Creating tables    ████████████████████ 100%
   📊 Seeding data      ████████████████████ 100%
   🔧 Setting up cache  ████████████████████ 100%
   
   🎉 Database initialized successfully!

**Confirmation Dialogs**

Destructive operations require confirmation:

.. code-block:: bash

   $ revsin system reset-cache
   ⚠️  This will clear all cached data.
   
   Are you sure you want to continue? [y/N]: y
   
   🗑️  Cache cleared successfully!

**Statistics Displays**

Data is presented in beautiful, easy-to-read formats:

.. code-block:: bash

   $ revsin loans stats
   
   ┌─ 📊 Loan Statistics ─────────────────────┐
   │ Total Active Loans    │ 1,234           │
   │ Overdue Loans        │ 56 (4.5%)       │
   │ Due This Week        │ 89              │
   │ Popular Categories   │ Fiction, Tech    │
   │ Average Loan Period  │ 14.2 days       │
   └──────────────────────────────────────────┘

Getting Help
-----------

**Command Help**

Every command includes comprehensive help:

.. code-block:: bash

   revsin --help                    # Global help
   revsin users --help             # Group help  
   revsin users create --help      # Command help

**Examples in Help**

Help text includes real-world examples:

.. code-block:: bash

   $ revsin books search --help
   
   Usage: revsin books search [OPTIONS] QUERY
   
   🔍 Search for books in the library catalog.
   
   Examples:
     revsin books search "machine learning"
     revsin books search --category fiction "mystery"
     revsin books search --available-only "python"
   
   Options:
     --category TEXT     Filter by category
     --available-only    Show only available books
     --limit INTEGER     Maximum results to show
     --help             Show this message and exit.

Advanced Features
---------------

**Batch Operations**

Process multiple items efficiently:

.. code-block:: bash

   # Import users from CSV
   revsin users import users.csv
   
   # Export loan data
   revsin loans export --format csv --output loans.csv
   
   # Bulk operations
   revsin books bulk-update updates.csv

**System Administration**

Comprehensive system management:

.. code-block:: bash

   # Health monitoring
   revsin system health --detailed
   
   # Database maintenance  
   revsin system backup-db
   revsin system optimize-db
   
   # Cache management
   revsin system cache-stats
   revsin system warm-cache

**Environment Management**

Multi-environment support:

.. code-block:: bash

   # Development environment
   revsin --env development system status
   
   # Production environment  
   revsin --env production system health

Error Handling
-------------

The CLI provides clear, actionable error messages:

.. code-block:: bash

   ❌ Error: Database connection failed
   
   🔧 Troubleshooting:
   • Check your DATABASE_URL in .env
   • Ensure PostgreSQL is running
   • Verify network connectivity
   
   💡 Need help? Run: revsin system doctor

Configuration
------------

The CLI respects your environment configuration:

.. code-block:: bash

   # Set environment variables
   export DATABASE_URL="postgresql://..."
   export REDIS_URL="redis://..."
   
   # Or use .env file
   cp env.example .env
   # Edit .env with your settings

**CLI-Specific Settings**

.. code-block:: bash

   # Disable colors (for CI/CD)
   export NO_COLOR=1
   
   # Quiet mode
   revsin --quiet system status
   
   # Verbose output
   revsin --verbose system health

Next Steps
---------

* Explore the :doc:`system` commands for administration
* Learn about :doc:`users` management  
* Discover :doc:`books` operations
* Master :doc:`loans` tracking

For API integration, see the :doc:`../api/index` documentation. 