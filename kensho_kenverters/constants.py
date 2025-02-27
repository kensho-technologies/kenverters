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
    # Types only in hierarchical models
    TABLE_TITLE = "TABLE_TITLE"
    FIGURE_TITLE = "FIGURE_TITLE"
    PARAGRAPH = "PARAGRAPH"
    H1 = "H1"
    H2 = "H2"
    # Types only in hierarchical_v2 model
    H3 = "H3"
    H4 = "H4"
    H5 = "H5"
    IMAGE_TITLE = "IMAGE_TITLE"
    TABLE_CAPTION = "TABLE_CAPTION"
    FIGURE_CAPTION = "FIGURE_CAPTION"
    IMAGE_CAPTION = "IMAGE_CAPTION"
    TABLE_LABEL = "TABLE_LABEL"
    FIGURE_LABEL = "FIGURE_LABEL"
    IMAGE_LABEL = "IMAGE_LABEL"
    TABLE_FOOTER = "TABLE_FOOTER"
    FIGURE_FOOTER = "FIGURE_FOOTER"
    IMAGE_FOOTER = "IMAGE_FOOTER"
    PAGE_HEADER = "PAGE_HEADER"
    PAGE_FOOTER = "PAGE_FOOTER"
    PAGE_FOOTNOTE = "PAGE_FOOTNOTE"
    TABLE_OF_CONTENTS = "TABLE_OF_CONTENTS"
    TABLE_OF_CONTENTS_TITLE = "TABLE_OF_CONTENTS_TITLE"


ELEMENT_TITLE_CONTENT_CATEGORIES = {
    ContentCategory.TABLE_TITLE.value,
    ContentCategory.FIGURE_TITLE.value,
    ContentCategory.IMAGE_TITLE.value,
    ContentCategory.TABLE_OF_CONTENTS_TITLE.value,
}

TITLE_CONTENT_CATEGORIES = {
    ContentCategory.TITLE.value,
    ContentCategory.H1.value,
    ContentCategory.H2.value,
    ContentCategory.H3.value,
    ContentCategory.H4.value,
    ContentCategory.H5.value,
} | ELEMENT_TITLE_CONTENT_CATEGORIES


TABLE_CONTENT_CATEGORIES = {
    ContentCategory.TABLE.value,
    ContentCategory.TABLE_OF_CONTENTS.value,
}
