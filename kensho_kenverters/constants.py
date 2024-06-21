# Copyright 2024-present Kensho Technologies, LLC.
"""Constants, enums, and type aliases for use across modules."""

from enum import Enum
from typing import TypeAlias

CATEGORY_KEY = "category"
TEXT_KEY = "text"
TABLE_KEY = "table"
LOCATIONS_KEY = "locations"
DOCUMENT_CATEGORY_KEY = "DOCUMENT"

TableType: TypeAlias = list[list[str]]


class AnnotationType(Enum):
    """Enum for the annotation type from the Extract output."""

    TABLE_STRUCTURE = "table_structure"


class ContentCategory(Enum):
    """Enum for the content type from the Extract output."""

    TABLE = "TABLE"
    TITLE = "TITLE"
    TEXT = "TEXT"
    TABLE_CELL = "TABLE_CELL"
    # Types only in broker research model
    TABLE_TITLE = "TABLE_TITLE"
    FIGURE_TITLE = "FIGURE_TITLE"
    PARAGRAPH = "PARAGRAPH"
    H1 = "H1"
    H2 = "H2"


TITLE_CONTENT_CATEGORIES = {
    ContentCategory.TITLE.value,
    ContentCategory.H1.value,
    ContentCategory.H2.value,
    ContentCategory.FIGURE_TITLE.value,
    ContentCategory.TABLE_TITLE.value,
}
TEXT_CONTENT_CATEGORIES = {ContentCategory.TEXT.value, ContentCategory.PARAGRAPH.value}
