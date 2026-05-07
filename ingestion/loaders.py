from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    WebBaseLoader,
    TextLoader,
)

from langchain_core.documents import Document

from pathlib import Path
from typing import List
import logging

from config import settings


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class DocumentLoader:
    """
    Unified document loader for:
    - PDF
    - DOCX
    - TXT
    - MD
    - URLs
    """

    def load(self, source: str) -> List[Document]:
        """
        Load a single source.
        """

        # URL Handling
        if source.startswith(("http://", "https://")):
            return self._load_url(source)

        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {source}"
            )

        # Dispatch Table
        dispatch = {
            ".pdf": self._load_pdf,
            ".docx": self._load_docx,
            ".txt": self._load_text,
            ".md": self._load_text,
        }

        loader_function = dispatch.get(
            path.suffix.lower()
        )

        if not loader_function:
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        return loader_function(source)

    def load_multiple(
        self,
        sources: List[str]
    ) -> List[Document]:
        """
        Load multiple documents safely.
        """

        all_documents = []

        for source in sources:

            try:
                docs = self.load(source)

                logger.info(
                    f"Successfully loaded: {source}"
                )

                all_documents.extend(docs)

            except Exception as e:

                logger.error(
                    f"Failed loading {source}: {str(e)}"
                )

        logger.info(
            f"Total documents loaded: {len(all_documents)}"
        )

        return all_documents

    def _add_metadata(
        self,
        docs: List[Document],
        source_type: str,
        source: str
    ) -> List[Document]:
        """
        Standardized metadata.
        """

        for doc in docs:

            doc.metadata["source_type"] = source_type
            doc.metadata["source"] = source

            if not source.startswith(
                ("http://", "https://")
            ):
                doc.metadata["file_name"] = (
                    Path(source).name
                )

                doc.metadata["file_path"] = str(
                    Path(source).absolute()
                )

        return docs

    def _load_pdf(
        self,
        path: str
    ) -> List[Document]:

        loader = PyPDFLoader(path)

        docs = loader.load()

        return self._add_metadata(
            docs,
            "pdf",
            path
        )

    def _load_docx(
        self,
        path: str
    ) -> List[Document]:

        loader = Docx2txtLoader(path)

        docs = loader.load()

        return self._add_metadata(
            docs,
            "docx",
            path
        )

    def _load_text(
        self,
        path: str
    ) -> List[Document]:

        loader = TextLoader(
            path,
            encoding="utf-8"
        )

        docs = loader.load()

        return self._add_metadata(
            docs,
            "text",
            path
        )

    def _load_url(
        self,
        url: str
    ) -> List[Document]:

        loader = WebBaseLoader(
            web_paths=[url],
            header_template={
                "User-Agent": settings.USER_AGENT
            }
        )

        docs = loader.load()

        return self._add_metadata(
            docs,
            "web",
            url
        )