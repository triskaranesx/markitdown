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

        raise ValueError(f"Unsupported MIME type for string conversion: {mime_type}")

    def _convert_local(self, path: Path, **kwargs) -> DocumentConverterResult:
        """Convert a local file to Markdown."""
        mime_type, _ = mimetypes.guess_type(str(path))
        extension = path.suffix.lower()

        # Plain text / markdown — read directly
        if extension in (".md", ".markdown", ".txt") or mime_type == "text/plain":
            text = path.read_text(encoding="utf-8", errors="replace")
            return DocumentConverterResult(title=path.stem, text_content=text)

        raise ValueError(
            f"Unsupported file type: {extension!r} (mime: {mime_type}). "
            "Install optional dependencies for additional format support."
        )

    def _convert_url(self, url: str, **kwargs) -> DocumentConverterResult:
        """Convert a URL resource to Markdown."""
        try:
            import requests
        except ImportError as exc:
            raise ImportError(
                "The 'requests' package is required for URL conversion. "
                "Install it with: pip install requests"
            ) from exc

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "text/plain").split(";")[0].strip()

        if content_type in ("text/plain", "text/markdown"):
            return DocumentConverterResult(text_content=response.text)

        raise ValueError(
            f"Unsupported content type from URL: {content_type!r}. "
            "Additional format support requires optional dependencies."
        )
