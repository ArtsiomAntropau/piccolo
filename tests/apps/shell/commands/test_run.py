from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from piccolo.apps.shell.commands.run import run


class TestRun(TestCase):
    @patch("piccolo.apps.shell.commands.run.start_ipython_shell")
    @patch("piccolo.apps.shell.commands.run.print")
    def test_run(self, print_: MagicMock, start_ipython_shell: MagicMock):
        """
        A simple test to make sure it executes without raising any exceptions.
        """
        run()

        self.assertEqual(
            print_.mock_calls,
            [
                call("-------"),
                call("Importing example_app tables:"),
                call("- Band"),
                call("- Concert"),
                call("- Manager"),
                call("- Poster"),
                call("- Ticket"),
                call("- Venue"),
                call("-------"),
            ],
        )

        self.assertTrue(start_ipython_shell.called)
