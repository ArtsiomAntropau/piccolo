Running migrations
==================

.. hint:: To see all available options for these commands, use the ``--help``
    flag, for example ``piccolo migrations forwards --help``.

Forwards
--------

When the migration is run, the forwards function is executed. To do this:

.. code-block:: bash

    piccolo migrations forwards my_app

Migrations table
~~~~~~~~~~~~~~~~

When running the migrations, Piccolo will automatically create a database table
called 'migration' if it doesn't already exist. Each time a migration is
succesfully ran, a new row is added to this table.

Faking
~~~~~~

Sometimes you'll want to 'fake' run a migration. Piccolo will store a record in
the 'migration' table marking it as a successfuly ran, without actually
applying the migration.

The reason you may want to do this is if you use ``piccolo schema generate`` (see :ref:`docs <SchemaApp>`)
to create your Piccolo ``Table`` classes from an existing database.

.. code-block:: bash

    piccolo migrations forwards my_app some_migration_id --fake

-------------------------------------------------------------------------------

Reversing migrations
--------------------

To reverse the migration, run this:

.. code-block:: bash

    piccolo migrations backwards 2018-09-04T19:44:09

You can try going forwards and backwards a few times to make sure it works as
expected.

-------------------------------------------------------------------------------

Checking migrations
-------------------

You can easily check which migrations have and haven't ran using the following:

.. code-block:: bash

    piccolo migrations check
