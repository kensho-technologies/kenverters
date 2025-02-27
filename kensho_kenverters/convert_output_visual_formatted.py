# Copyright 2024-present Kensho Technologies, LLC.
"""Functions for converting the JSON output into a text representation with visual formatting.

The resulting visual formatting will resemble the original document's layout.
"""

import math
from logging import getLogger
from typing import Any, TypeAlias

from kensho_kenverters.constants import (
    LOCATIONS_KEY,
    TABLE_CONTENT_CATEGORIES,
    TEXT_KEY,
    AnnotationType,
    ContentCategory,
)
from kensho_kenverters.extract_output_models import ContentModel, LocationModel
from kensho_kenverters.utils import load_output_to_pydantic

logger = getLogger(__name__)

LocationListType: TypeAlias = list[LocationModel] | None
MAX_RETRIES = 10
HEIGHT_INC_AMOUNT = 50


class PageTooShortException(Exception):
    """Too many lines for the specified page size."""


def _get_segments_from_table_cells(
    table_cells: list[ContentModel],
    uid_to_location: dict[str, LocationListType],
) -> list[dict[str, Any]]:
    """Use the table content and table cell annotations together to create a dictionary segment."""
    segments = []
    for cell in table_cells:
        location = uid_to_location[cell.uid]
        if not isinstance(cell.content, str):
            raise ValueError(
                "Cell content is not a string. Cannot construct a table of strings"
            )
        segment = {
            TEXT_KEY: cell.content.strip(),
            LOCATIONS_KEY: location,
        }
        segments.append(segment)
    return segments


def _convert_output_to_texts_with_locs(
    serialized_document: dict[str, Any]
) -> list[dict[str, Any]]:
    """Convert Extract output into a list of items.

    These items include document titles, texts, and table cells with text and location.
    """
    parsed_serialized_document = load_output_to_pydantic(serialized_document)
    annotations = parsed_serialized_document.annotations

    # Read table cell structure
    uid_to_location: dict[str, LocationListType] = {}

    for annotation in annotations:
        if annotation.type == AnnotationType.TABLE_STRUCTURE.value:
            content_uids = annotation.content_uids  # a list
            for uid in content_uids:
                uid_to_location[uid] = annotation.locations
        else:
            raise TypeError(f"{annotation.type} is not a supported annotation type")

    # Parse content into segments
    content_tree = parsed_serialized_document.content_tree
    segments: list[dict[str, Any]] = []
    for content in content_tree.children:
        # For tables, use table cell structures read above
        if content.type in TABLE_CONTENT_CATEGORIES:
            # Construct the table from cells
            table_cells = content.children
            # Drop tables with no cells
            if len(table_cells) == 0:
                continue
            table_cell_segments = _get_segments_from_table_cells(
                table_cells, uid_to_location
            )
            segments += table_cell_segments
        elif content.type in [e.value for e in ContentCategory]:
            segment: dict[str, Any] = {
                TEXT_KEY: content.content,
                LOCATIONS_KEY: content.locations,
            }
            segments.append(segment)
        else:
            raise TypeError(
                f"Content category must be in {[e.value for e in ContentCategory]}. "
                f"Found {content.type}"
            )

    return segments


def _convert_segments_to_dict(
    document_items: list[dict[str, Any]],
    page_width: int,
    page_height: int,
    resize: bool,
) -> dict[str, list[list[str]]]:
    """Convert extracted document segments into a dictionary of page -> 2D text representation."""
    page_text_arrs: dict[str, list[list[str]]] = {}
    for item in document_items:
        for location in item[LOCATIONS_KEY]:
            page_number = location.page_number
            # If this is the first time we see a box with this page number, create the page array
            if page_number not in page_text_arrs:
                page_text_arrs[page_number] = [
                    [" " for _ in range(page_width)] for _ in range(page_height)
                ]

            # Get segment coordinates
            x_0 = math.floor(location.x * page_width)
            y_0 = math.floor(location.y * page_height)
            x_1 = x_0 + math.ceil(location.width * page_width)
            y_1 = y_0 + math.ceil(location.height * page_height)
            words = item["text"].split()

            # Create segment array to later put into page array
            segment_width = max(x_1 - x_0, 1)
            segment_height = max(y_1 - y_0, 1)
            segment_arr = [
                [" " for _ in range(segment_width)] for _ in range(segment_height)
            ]
            current_col = 0
            current_row = 0

            for word in words:
                # Check if word fits in line
                if current_col + len(word) >= segment_width:
                    current_row += 1  # Move to the next line if it doesn't fit
                    current_col = 0  # Reset to the start of the box

                # Check if word exceeds the box vertically or horizontally
                if (
                    current_row >= segment_height
                    or current_col + len(word) > segment_width
                ):
                    if resize:
                        raise PageTooShortException
                    else:
                        logger.info(
                            "Not enough space to finish the segment, skipping remaining words "
                            "in this segment."
                        )
                        break  # Skip remaining words if no space
                for i, char in enumerate(word):
                    segment_arr[current_row][current_col + i] = char
                current_col += len(word) + 1

            # Spread out the lines more if we don't take up the entire box
            if current_row != y_1 - 1:
                num_rows_used = min(current_row + 1, segment_height)
                num_rows_between_lines = int(segment_height / num_rows_used)
                new_segment_arr = [
                    [" " for _ in range(segment_width)] for _ in range(segment_height)
                ]
                for line_index in range(0, num_rows_used):
                    new_line_index = min(
                        line_index * num_rows_between_lines, segment_height - 1
                    )
                    new_segment_arr[new_line_index] = segment_arr[line_index]
            else:
                new_segment_arr = segment_arr

            for i in range(segment_height):
                for j in range(segment_width):
                    page_text_arrs[page_number][y_0 + i][x_0 + j] = new_segment_arr[i][
                        j
                    ]

    return page_text_arrs


def _non_blank_line(text_line_str: str) -> bool:
    """Check if line is not blank."""
    return any(line.strip() for line in text_line_str)


def _num_left_white_spaces(text_line_list: list[str]) -> int:
    """Check how many spaces are on the lefthand side of the text for later cleaning purposes."""
    last_left_space_index = 0
    for char in text_line_list:
        if char == " ":
            last_left_space_index += 1
        # Word has started
        else:
            break
    return last_left_space_index


def _clean_page_text_arr(text_arr: list[list[str]]) -> str:
    """Take in a 2D array of a page, with char text lines, and convert it to one page string."""
    # Remove as much left white space as possible without changing relative positions
    num_left_spaces = min(_num_left_white_spaces(text_line) for text_line in text_arr)

    page_line_texts_list = []
    previous_is_blank = False
    for text_line in text_arr:
        # Put all chars in that line together
        line_text = "".join(text_line[num_left_spaces:]).rstrip()
        # Remove multiple consecutive blank lines and keep only one
        line_not_blank = _non_blank_line(line_text)
        if line_not_blank or not previous_is_blank:
            page_line_texts_list.append(line_text)

        # Update previous line is blank
        if line_not_blank:
            previous_is_blank = False
        else:
            previous_is_blank = True

    # Combine all lines with a new line character
    page_lines_str = "\n".join(page_line_texts_list).rstrip()

    # End of page
    page_lines_str += (
        "\n"
        + "======================================================================================="
    )
    return page_lines_str


def convert_output_to_str_formatted(
    serialized_document: dict[str, Any],
    page_width: int = 300,
    page_height: int = 100,
    resize: bool = True,
) -> list[str]:
    """Convert entire Extract output into a string per page that visually looks like the original.

    The output will contain spaces and newlines to make the printed output resemble the page
    layout.

    Args:
        serialized_document: a serialized document
        page_width: the max number of characters in a printed line
        page_height: the max lines in a printed document representation
        resize: if the given page_width and page_height would cut off any segment,
            allow for overriding those values (resizing the output). Setting this to False will
            enforce the width and height of the output and will truncate any words that spill over.

    Returns:
        full text string for each page

    Example Output:

                                                                Valerie
                                                          123 The Street
                                                           Somewhere, XX

        Dear Reader,

        I am writing to you from somewhere! Here's an important table:

                        Item        Favorite

                        Animal      Duck
                        Color       Red
                        Reader      You


        Thanks for reading!

        Lots of love,

            Valerie
    """
    document_items = _convert_output_to_texts_with_locs(serialized_document)
    page_text_arrays = {}

    for _ in range(MAX_RETRIES):
        try:
            page_text_arrays = _convert_segments_to_dict(
                document_items, page_width, page_height, resize
            )
        except PageTooShortException:
            logger.info(
                "Could not fit all words on line with width {%s} and height {%s}. "
                "Trying width {%s} and height {%s}",
                page_width,
                page_height,
                page_width + HEIGHT_INC_AMOUNT,
                page_height + HEIGHT_INC_AMOUNT,
            )
            page_height += HEIGHT_INC_AMOUNT
            page_width += HEIGHT_INC_AMOUNT
        else:
            break
    else:
        logger.info(
            "Could not fit all words on line with width {%s} and height {%s}. "
            "Retry with new page_height or page_width or set resize=False.",
            page_width,
            page_height,
        )

    converted_pages = []
    for _, text_arr in sorted(page_text_arrays.items()):
        page_lines_str = _clean_page_text_arr(text_arr)
        converted_pages.append(page_lines_str)

    return converted_pages
