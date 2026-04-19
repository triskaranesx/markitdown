"""Core MarkItDown conversion engine."""

from __future__ import annotations

import mimetypes
import os
import re
from pathlib import Path
from typing import Optional, Union


class DocumentConverterResult:
    """Result of a document conversion."""

    def __init__(self, title: Optional[str] = None, text_content: str = ""):
        self.title = title
        self.text_content = text_content

    def __str__(self) -> str:
        return self.text_content


class MarkItDown:
    """Main class for converting documents to Markdown.

    Supports conversion of various file formats including:
    - Plain text and Markdown files
    - HTML files
    - PDF documents
    - Microsoft Office documents (docx, xlsx, pptx)
    - Images (with optional LLM description)
    """

    def __init__(
        self,
        llm_client=None,
        llm_model: Optional[str] = None,
    ):
        """Initialize MarkItDown.

        Args:
            llm_client: Optional LLM client for image descriptions and enrichment.
            llm_model: Optional model name to use with the LLM client.
        """
        self._llm_client = llm_client
        self._llm_model = llm_model

    def convert(
        self,
        source: Union[str, Path],
        **kwargs,
    ) -> DocumentConverterResult:
        """Convert a file or URL to Markdown.

        Args:
            source: Path to a local file or a URL string.
            **kwargs: Additional keyword arguments passed to the converter.

        Returns:
            DocumentConverterResult containing the converted Markdown text.

        Raises:
            FileNotFoundError: If a local file path does not exist.
            ValueError: If the source type is unsupported.
        """
        source = str(source)

        # Handle URLs
        if re.match(r"^https?://", source, re.IGNORECASE):
            return self._convert_url(source, **kwargs)

        # Handle local files
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {source}")

        return self._convert_local(path, **kwargs)

    def convert_string(
        self,
        content: str,
        mime_type: str = "text/plain",
        **kwargs,
    ) -> DocumentConverterResult:
        """Convert a string of content to Markdown.

        Args:
            content: The string content to convert.
            mime_type: MIME type hint for the content.
            **kwargs: Additional keyword arguments.

        Returns:
            DocumentConverterResult with the converted text.
        """
        # For plain text and markdown, return as-is
        if mime_type in ("text/plain", "text/markdown"):
            return DocumentConverterResult(text_content=content)

        # Also treat HTML as plain text fallback for quick personal use
        if mime_type == "text/html":
            # Strip tags naively for a quick plain-text approximation
            stripped = re.sub(r"<[^>]+>", "", content)
            return DocumentConverterResult(text_content=stripped)

        raise ValueError(f"Unsupported MIME type for string conversion: {mime_type}")

    def _convert_local(self, path: Path, **kwargs) -> DocumentConverterResult:
        """Convert a local file to Markdown."""
        mime_type, _ = mimetypes.guess
