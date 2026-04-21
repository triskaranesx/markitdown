"""MarkItDown - Convert various file formats to Markdown."""

# Personal fork of microsoft/markitdown
# Main reason for forking: experimenting with custom converters
# Fork notes:
#   - Added StreamConverter to public API for easier stream-based conversion
#   - Tracking upstream: https://github.com/microsoft/markitdown

from markitdown._markitdown import MarkItDown, DocumentConverter, ConversionResult, StreamConverter

__version__ = "0.1.0-personal"
__author__ = "personal fork of microsoft/markitdown"
__all__ = ["MarkItDown", "DocumentConverter", "ConversionResult", "StreamConverter"]
