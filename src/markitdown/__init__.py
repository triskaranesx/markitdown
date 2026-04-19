"""MarkItDown - Convert various file formats to Markdown."""

# Personal fork of microsoft/markitdown
# Main reason for forking: experimenting with custom converters

from markitdown._markitdown import MarkItDown, DocumentConverter, ConversionResult

__version__ = "0.1.0"
__author__ = "personal fork of microsoft/markitdown"
__all__ = ["MarkItDown", "DocumentConverter", "ConversionResult"]
