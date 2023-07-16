import aiohttp
import unittest
import asyncio
from unittest.mock import patch, call


class TestLogs(unittest.TestCase):
    def setUp(self):
        # Mock the aiohttp.ClientSession context manager
        self.mock_session = patch("aiohttp.ClientSession").start()
        self.mock_resp = (
            self.mock_session.return_value.get.return_value.__aenter__.return_value
        )
        self.mock_resp.content.__aiter__.return_value = [
            b"line 1\n",
            b"line 2\n",
            b"line 3\n",
        ]

    def tearDown(self):
        # Stop the mock
        patch.stopall()

    async def test_logs(self):
        # Import the logs function here
        from ..main import logs

        # Set up the test parameters
        cont = "container_id"
        name = "container_name"

        # Run the logs function
        await logs(cont, name)

        # Assert that the aiohttp.ClientSession was created
        self.mock_session.assert_called_once_with(
            connector=patch("aiohttp.UnixConnector").return_value
        )

        # Assert that the session.get method was called with the correct URL
        self.mock_session.return_value.get.assert_called_once_with(
            f"http://xx/containers/{cont}/logs?follow=1&stdout=1"
        )

        # Assert that the print function was called with the expected output
        expected_output = [
            f"{name} line 1\n",
            f"{name} line 2\n",
            f"{name} line 3\n",
        ]
        calls = [call(name, line) for line in expected_output]
        self.assertEqual(self.mock_print.call_args_list, calls)


if __name__ == "__main__":
    unittest.main()
