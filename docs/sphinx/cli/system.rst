System Commands
==============

.. module:: revsin.cli.commands.system

The System command group provides commands for system administration and maintenance.

Status
------

.. code-block:: bash

   revsin system status

Displays the current status of the RevSin system, including:

* Database connection status
* Redis connection status
* API server status
* System version
* Environment (development, production)
* Database statistics (users, books, loans)

Example output:

.. code-block:: text

   RevSin System Status
   ====================
   
   Version: 0.1.0
   Environment: development
   
   Connections:
   - Database: Connected (PostgreSQL 14.5)
   - Redis: Connected (Redis 7.0.5)
   - API Server: Running (http://localhost:8000)
   
   Statistics:
   - Users: 25 (3 admins, 5 librarians, 17 members)
   - Books: 150 (120 available)
   - Loans: 45 (40 active, 5 overdue)

Create Admin
-----------

.. code-block:: bash

   revsin system create-admin --username USERNAME --email EMAIL [--password PASSWORD] [--full-name FULL_NAME]

Creates a new admin user in the system.

**Options**:

* ``--username``: Username for the admin user (required)
* ``--email``: Email address for the admin user (required)
* ``--password``: Password for the admin user (if not provided, will prompt securely)
* ``--full-name``: Full name for the admin user

Example:

.. code-block:: bash

   revsin system create-admin --username admin --email admin@example.com --full-name "System Administrator"

If you don't provide a password, you'll be prompted to enter it securely:

.. code-block:: text

   Password: ********
   Confirm password: ********
   
   Admin user 'admin' created successfully.

Backup
------

.. code-block:: bash

   revsin system backup [--output-dir OUTPUT_DIR] [--include-media]

Creates a backup of the system database.

**Options**:

* ``--output-dir``: Directory to store the backup (default: current directory)
* ``--include-media``: Include media files in the backup

Example:

.. code-block:: bash

   revsin system backup --output-dir /path/to/backups --include-media
   
   Backup created successfully: /path/to/backups/revsin_backup_2023-11-15_10-30-00.zip

Restore
-------

.. code-block:: bash

   revsin system restore BACKUP_FILE [--force]

Restores the system from a backup file.

**Arguments**:

* ``BACKUP_FILE``: Path to the backup file to restore from

**Options**:

* ``--force``: Force restore without confirmation

Example:

.. code-block:: bash

   revsin system restore /path/to/backups/revsin_backup_2023-11-15_10-30-00.zip
   
   Warning: This will overwrite the current database. Continue? [y/N]: y
   
   Restoring backup...
   Backup restored successfully.

Init
----

.. code-block:: bash

   revsin system init [--sample-data]

Initializes the system, creating necessary database tables and initial data.

**Options**:

* ``--sample-data``: Load sample data for testing

Example:

.. code-block:: bash

   revsin system init --sample-data
   
   Initializing system...
   Creating database tables...
   Loading sample data...
   System initialized successfully.

Migrate
-------

.. code-block:: bash

   revsin system migrate [--revision REVISION]

Runs database migrations to update the schema.

**Options**:

* ``--revision``: Specific migration revision to migrate to

Example:

.. code-block:: bash

   revsin system migrate
   
   Running database migrations...
   Database migrated successfully to revision a1b2c3d4e5f6.

Clear Cache
----------

.. code-block:: bash

   revsin system clear-cache [--all]

Clears the Redis cache.

**Options**:

* ``--all``: Clear all caches (including session data)

Example:

.. code-block:: bash

   revsin system clear-cache
   
   Cache cleared successfully. 