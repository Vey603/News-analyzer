"""Tests for cli."""

import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from platzi_news.io.cli import main


class TestCLI(unittest.TestCase):
    """Test CLI functions."""

    @patch("platzi_news.io.cli.NewsService")
    @patch("sys.exit")
    def test_main_search_command(self, mock_exit, mock_service_class):
        """Test main function with search command."""
        mock_service = AsyncMock()
        mock_service_class.return_value = mock_service
        mock_service.asearch_articles.return_value = []

        with patch(
            "sys.argv", ["platzi-news", "search", "test", "--source", "guardian"]
        ):
            asyncio.run(main())
        mock_service.asearch_articles.assert_called_once_with("guardian", "test")
        mock_exit.assert_called_once_with(0)

    @patch("platzi_news.io.cli.NewsService")
    @patch("sys.exit")
    def test_main_ask_command(self, mock_exit, mock_service_class):
        """Test main function with ask command."""
        mock_service = AsyncMock()
        mock_service_class.return_value = mock_service
        mock_service.asearch_articles.return_value = []
        mock_service.analyze_articles.return_value = "Answer"

        with patch(
            "sys.argv",
            ["platzi-news", "ask", "test", "question", "--source", "guardian"],
        ):
            asyncio.run(main())
        mock_service.asearch_articles.assert_called_once_with("guardian", "test")
        mock_service.analyze_articles.assert_called_once_with([], "question")
        mock_exit.assert_called_once_with(0)

    @patch("sys.exit")
    def test_main_no_command(self, mock_exit):
        """Test main with no command."""
        mock_exit.side_effect = SystemExit
        with patch("sys.argv", ["platzi-news"]), self.assertRaises(SystemExit):
            asyncio.run(main())
        mock_exit.assert_called_once_with(1)

    @patch("platzi_news.io.cli.NewsService")
    @patch("sys.exit")
    def test_main_exception_handling(self, mock_exit, mock_service_class):
        """Test main handles exceptions."""
        mock_service_class.side_effect = Exception("Test error")
        mock_exit.side_effect = SystemExit

        with (
            patch(
                "sys.argv", ["platzi-news", "search", "test", "--source", "guardian"]
            ),
            self.assertRaises(SystemExit),
        ):
            asyncio.run(main())
        mock_exit.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
