"""Tests for merge_pdfs module."""

import sys
import unittest
from unittest.mock import patch, MagicMock, call
from pathlib import Path

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.merge_pdfs import merge_pdfs


class TestMergePdfs(unittest.TestCase):
    """Test cases for merge_pdfs function."""

    @patch('pdftools.merge_pdfs.PdfMerger')
    def test_merge_pdfs_basic(self, mock_merger_class):
        """Test basic PDF merging."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger

        input_files = ["file1.pdf", "file2.pdf"]
        output_file = "merged.pdf"

        merge_pdfs(input_files, output_file)

        # Verify PdfMerger was instantiated
        mock_merger_class.assert_called_once()

        # Verify append was called for each input file
        self.assertEqual(mock_merger.append.call_count, 2)
        mock_merger.append.assert_any_call("file1.pdf")
        mock_merger.append.assert_any_call("file2.pdf")

        # Verify write was called with output file
        mock_merger.write.assert_called_once_with(output_file)

        # Verify close was called
        mock_merger.close.assert_called_once()

    @patch('pdftools.merge_pdfs.PdfMerger')
    def test_merge_pdfs_single_file(self, mock_merger_class):
        """Test merging with single input file."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger

        input_files = ["single.pdf"]
        output_file = "output.pdf"

        merge_pdfs(input_files, output_file)

        mock_merger.append.assert_called_once_with("single.pdf")
        mock_merger.write.assert_called_once_with(output_file)

    @patch('pdftools.merge_pdfs.PdfMerger')
    def test_merge_pdfs_multiple_files(self, mock_merger_class):
        """Test merging with multiple input files."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger

        input_files = ["file1.pdf", "file2.pdf", "file3.pdf", "file4.pdf"]
        output_file = "merged_all.pdf"

        merge_pdfs(input_files, output_file)

        self.assertEqual(mock_merger.append.call_count, 4)
        mock_merger.write.assert_called_once_with(output_file)
        mock_merger.close.assert_called_once()

    @patch('pdftools.merge_pdfs.PdfMerger')
    def test_merge_pdfs_exception_handling(self, mock_merger_class):
        """Test that close is called even if merge fails."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger
        mock_merger.write.side_effect = Exception("Merge failed")

        input_files = ["file1.pdf", "file2.pdf"]
        output_file = "output.pdf"

        with self.assertRaises(Exception):
            merge_pdfs(input_files, output_file)

        # close() should still be called due to finally block
        mock_merger.close.assert_called_once()

    @patch('pdftools.merge_pdfs.PdfMerger')
    def test_merge_pdfs_output_path(self, mock_merger_class):
        """Test that output path is correctly passed."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger

        output_path = "/path/to/merged_output.pdf"
        merge_pdfs(["file1.pdf"], output_path)

        mock_merger.write.assert_called_once_with(output_path)

    @patch('pdftools.merge_pdfs.PdfMerger')
    def test_merge_pdfs_preserves_order(self, mock_merger_class):
        """Test that input files are merged in order."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger

        input_files = ["first.pdf", "second.pdf", "third.pdf"]
        merge_pdfs(input_files, "output.pdf")

        # Verify append calls were made in order
        expected_calls = [call("first.pdf"), call("second.pdf"), call("third.pdf")]
        mock_merger.append.assert_has_calls(expected_calls, any_order=False)

    @patch('pdftools.merge_pdfs.PdfMerger')
    def test_merge_pdfs_with_special_paths(self, mock_merger_class):
        """Test merging with special characters in paths."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger

        input_files = ["/path/with spaces/file 1.pdf", "/path-with-dashes/file-2.pdf"]
        output_file = "/output path/merged file.pdf"

        merge_pdfs(input_files, output_file)

        mock_merger.write.assert_called_once_with(output_file)
        self.assertEqual(mock_merger.append.call_count, 2)

    @patch('pdftools.merge_pdfs.PdfMerger')
    def test_merge_pdfs_empty_list_behavior(self, mock_merger_class):
        """Test behavior with empty input list."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger

        input_files = []
        output_file = "output.pdf"

        merge_pdfs(input_files, output_file)

        # append should not be called
        mock_merger.append.assert_not_called()
        # But write and close should still be called
        mock_merger.write.assert_called_once()
        mock_merger.close.assert_called_once()

    @patch('pdftools.merge_pdfs.PdfMerger')
    def test_merge_pdfs_file_paths_as_strings(self, mock_merger_class):
        """Test that file paths are handled as strings."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger

        input_files = ["file1.pdf", "file2.pdf"]
        output_file = "merged.pdf"

        merge_pdfs(input_files, output_file)

        # Verify string paths are passed correctly
        calls = mock_merger.append.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0][0], "file1.pdf")
        self.assertEqual(calls[1][0][0], "file2.pdf")


if __name__ == "__main__":
    unittest.main()
