# Copyright 2024-present Kensho Technologies, LLC.
"""Functions for converting the JSON output into markdown, text, and lists of extracted segments."""

from collections import defaultdict
from logging import getLogger
from typing import Any

from kensho_kenverters.constants import (
    CATEGORY_KEY,
    DOCUMENT_CATEGORY_KEY,
    ELEMENT_TITLE_CONTENT_CATEGORIES,
    LOCATIONS_KEY,
    TABLE_CONTENT_CATEGORIES,
    TABLE_KEY,
    TEXT_KEY,
    AnnotationType,
    ContentCategory,
    TableType,
)
from kensho_kenverters.extract_output_models import ContentModel, LocationModel
from kensho_kenverters.utils import load_output_to_pydantic

logger = getLogger(__name__)


def table_to_markdown(table: TableType) -> str:
    """Convert 2D grid table to a single string with | as a delimiter."""
    lines = []
    for row_index, row in enumerate(table):
        row = [str(x) for x in row]
        line = "| " + " | ".join(row) + " |"
        lines.append(line)
        # Markdown tables only render correctly if there's a header row
        # and an extra line at the end to mark the end of the table
        if row_index == 0:
            lines.append("| " + " | ".join(["---" for _ in row]) + " |")
    table_text = "\n".join(lines) + "\n"
    return table_text


def _construct_table_from_cells(
    table_cells: list[ContentModel],
    uid_to_index: dict[str, tuple[int, int]],
    uid_to_span: dict[str, tuple[int, int]],
) -> TableType:
    """Return the 2D list of content strings from a list of ContentModels."""
    cell_uids = [
        cell.uid
        for cell in table_cells
        if cell.type == ContentCategory.TABLE_CELL.value
    ]
    indexes = [uid_to_index[uid] for uid in cell_uids]
    rows, cols = zip(*indexes)

    # Calculate the necessary number of rows and columns based on the spans
    n_row = max(rows) + 1
    n_col = max(cols) + 1
    for cell in table_cells:
        row, col = uid_to_index[cell.uid]
        row_span, col_span = uid_to_span[cell.uid]
        # Update the table dimensions if a cell spans beyond the current limits
        n_row = max(n_row, row + row_span)
        n_col = max(n_col, col + col_span)

    # Construct the table
    table = [["" for _ in range(n_col)] for _ in range(n_row)]
    for cell in table_cells:
        row, col = uid_to_index[cell.uid]
        row_span, col_span = uid_to_span[cell.uid]
        if not isinstance(cell.content, str):
            raise ValueError(
                "Cell content is not a string. Cannot construct a table of strings"
            )
        for row_span_index in range(row_span):
            for col_span_index in range(col_span):
                table[row + row_span_index][col + col_span_index] = cell.content.strip()
    return table


def _get_markdown_text(item: dict[str, Any]) -> str:
    """Convert an item to markdown text based on its category."""
    # Add # to titles for full markdown
    if item[CATEGORY_KEY] in (
        ContentCategory.TITLE.value.lower(),
        ContentCategory.H1.value.lower(),
    ):
        return "# " + item[TEXT_KEY]  # type: ignore[no-any-return]
    # Add ## to section headers
    elif item[CATEGORY_KEY] == ContentCategory.H2.value.lower():
        return "## " + item[TEXT_KEY]  # type: ignore[no-any-return]
    # Add ### to figure titles and table titles
    elif (
        item[CATEGORY_KEY]
        in [content_type.lower() for content_type in ELEMENT_TITLE_CONTENT_CATEGORIES]
        or item[CATEGORY_KEY] == ContentCategory.H3.value.lower()
    ):
        return "### " + item[TEXT_KEY]  # type: ignore[no-any-return]
    # Add #### to H4
    elif item[CATEGORY_KEY] == ContentCategory.H4.value.lower():
        return "#### " + item[TEXT_KEY]  # type: ignore[no-any-return]
    # Add ##### to H5
    elif item[CATEGORY_KEY] == ContentCategory.H5.value.lower():
        return "##### " + item[TEXT_KEY]  # type: ignore[no-any-return]
    return item[TEXT_KEY]  # type: ignore[no-any-return]


def _create_segment(
    content: ContentModel,
    uid_to_index: dict[str, tuple[int, int]],
    uid_to_span: dict[str, tuple[int, int]],
) -> dict[str, Any]:
    """Create segment dictionary from the content, and if applicable its matching table cells."""
    segment: dict[str, Any] = {}
    # DOCUMENT is just a head node
    if content.type == DOCUMENT_CATEGORY_KEY:
        return {}
    # For tables, use table cell structures read above
    elif content.type in TABLE_CONTENT_CATEGORIES:
        # Construct the table from cells
        table_cells = content.children
        # Drop tables with no cells
        if len(table_cells) == 0:
            return {}
        table = _construct_table_from_cells(table_cells, uid_to_index, uid_to_span)
        # Drop tables with length 0
        if len(table) == 0:
            return {}
        segment = {
            CATEGORY_KEY: content.type.lower(),
            TABLE_KEY: table,
            TEXT_KEY: table_to_markdown(table),
        }
    elif content.type == ContentCategory.TABLE_CELL.value:
        # Skip - already accounted for in tables
        return {}
    # For texts and titles, add the text content and the category
    elif content.type in [e.value for e in ContentCategory]:
        segment = {
            CATEGORY_KEY: content.type.lower(),
            TEXT_KEY: content.content,
        }
    else:
        raise TypeError(
            f"Content category must be in {[e.value for e in ContentCategory]}. "
            f"Found {content.type}"
        )
    return segment


def _get_segments_from_all_children(
    content: ContentModel,
    uid_to_index: dict[str, tuple[int, int]],
    uid_to_span: dict[str, tuple[int, int]],
    return_locations: bool,
    segments: list[dict[str, Any]],
    visited: list[str],
) -> None:
    """Recursively get all text from the content node and its children."""
    if content.uid in visited:
        return

    # Get current segment from content and add to list
    segment = _create_segment(content, uid_to_index, uid_to_span)
    visited.append(content.uid)
    if segment:
        if return_locations:
            segment[LOCATIONS_KEY] = content.locations
        segments.append(segment)

    # Get all children segments
    for child in content.children:
        _get_segments_from_all_children(
            child, uid_to_index, uid_to_span, return_locations, segments, visited
        )


def convert_output_to_items_list(
    serialized_document: dict[str, Any], return_locations: bool = False
) -> list[dict[str, Any]]:
    """Convert Extract output into a list of items representing the different document entitites.

    Args:
        serialized_document: a serialized document
        return_locations: whether to return segment locations in the result

    Returns:
            a list of dictionaries representing a "segment".
                If an item is a text or title entity, it will contain keys:
                    1) "category" equal to "text" or "title"
                    2) "text" containing the text
                    If return_locations:
                        3) "locations" containing the locations as a list of location dictionaries

                If an item is a table, it will contain keys:
                    1) "category" equal to "table"
                    2) "text" containing the markdown version of the table cell texts
                    3) "table" containing the 2D grid of table texts
                    If return_locations:
                        4) "locations" containing the locations as a list of location dictionaries
    """
    parsed_serialized_document = load_output_to_pydantic(serialized_document)
    annotations = parsed_serialized_document.annotations

    # Read table cell structure
    uid_to_index: dict[str, tuple[int, int]] = {}
    uid_to_span: dict[str, tuple[int, int]] = {}
    for annotation in annotations:
        if annotation.type == AnnotationType.TABLE_STRUCTURE.value:
            content_uids = annotation.content_uids  # a list
            row, col = annotation.data.index  # 2D index of table cell
            for uid in content_uids:
                uid_to_index[uid] = (row, col)
                uid_to_span[uid] = annotation.data.span
        else:
            raise TypeError(f"{annotation.type} is not a supported annotation type")

    # Parse content into segments
    content_tree = parsed_serialized_document.content_tree
    segments: list[dict[str, Any]] = []
    visited: list[str] = []
    _get_segments_from_all_children(
        content_tree, uid_to_index, uid_to_span, return_locations, segments, visited
    )
    return segments


def convert_output_to_str(serialized_document: dict[str, Any]) -> str:
    """Convert entire Extract output into a single string.

    Args:
        serialized_document: a serialized document

    Returns:
        full text string of the document with markdown-style tables using | as a delimiter
    """
    document_items = convert_output_to_items_list(serialized_document)
    return "\n".join(item[TEXT_KEY] for item in document_items)


def convert_output_to_str_by_page(serialized_document: dict[str, Any]) -> list[str]:
    r"""Convert entire Extract output into a single string by page.

    Args:
        serialized_document: a serialized document

    Returns:
        a list of full text strings of the document by page with markdown-style tables
            using | as a delimiter.

    Example Output:
        [
            'Random Title for the First Page\nThis page is about things.',
            'Page 2: Another Title.\nThis page is not about things.',
            'Supplementary materials found here\n|T|L|'
        ]
    """
    document_items = convert_output_to_items_list(
        serialized_document, return_locations=True
    )
    page_texts = defaultdict(list)
    for item in document_items:
        locations = item[LOCATIONS_KEY]
        if locations is None:
            logger.info(
                "Unable to get location information from the output file. "
                "Putting all text on one page."
            )
            locations = [LocationModel(page_number=0, height=1, width=1, x=0, y=0)]
        for location in locations:
            page_texts[location.page_number].append(item[TEXT_KEY])
    return ["\n".join(text) for _, text in sorted(page_texts.items())]


def convert_output_to_markdown(serialized_document: dict[str, Any]) -> str:
    """Convert entire Extract output into a single markdown string.

    Args:
        serialized_document: a serialized document

    Returns:
        full text string of the document with markdown-style tables using | as a delimiter
        and titles prefaced with #
    """
    document_items = convert_output_to_items_list(serialized_document)
    item_texts = []
    for item in document_items:
        item_text = _get_markdown_text(item)
        item_texts.append(item_text)
    return "\n".join(item_texts)


def convert_output_to_markdown_by_page(
    serialized_document: dict[str, Any]
) -> list[str]:
    r"""Convert entire Extract output into a markdown string per page.

    Args:
        serialized_document: a serialized document

    Returns:
        list of full text strings of the document by page with markdown-style tables using |
            as a delimiter and titles prefaced with #

    Example Output:
        [
            '# Random Title for the First Page\nThis page is about things.',
            '# Page 2: Another Title.\nThis page is not about things.',
            'Supplementary materials found here\n|T|L|'
        ]
    """
    document_items = convert_output_to_items_list(
        serialized_document, return_locations=True
    )
    page_texts = defaultdict(list)

    for item in document_items:
        item_text = _get_markdown_text(item)
        locations = item[LOCATIONS_KEY]
        if locations is None:
            logger.info(
                "Unable to get location information from the output file. "
                "Putting all text on one page."
            )
            locations = [LocationModel(page_number=0, height=1, width=1, x=0, y=0)]
        for location in locations:
            page_texts[location.page_number].append(item_text)

    return ["\n".join(text) for _, text in sorted(page_texts.items())]
