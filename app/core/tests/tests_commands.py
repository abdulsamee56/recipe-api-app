from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# Mock the 'check' method in the wait_for_db command
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available immediately."""
        patched_check.return_value = True  # Simulate DB is ready

        call_command('wait_for_db')

        # Check if the command checks the 'databases' parameter correctly
        patched_check.assert_called_once_with(databases=['default'])  # Fixed 'databases'

    @patch('time.sleep')  # Patch sleep to speed up the test
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting operational error."""
        # Simulate the database being unavailable multiple times, then available
        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # Ensure check() was called 6 times in total
        self.assertEqual(patched_check.call_count, 6)

        # Verify the final call to 'check' uses the correct 'databases' parameter
        patched_check.assert_called_with(databases=['default'])  # Fixed 'databases'
