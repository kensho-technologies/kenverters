# Copyright 2024-present Kensho Technologies, LLC.
"""Functions to organize the output into conceptually related sections."""

from typing import Any

from kensho_kenverters.constants import CATEGORY_KEY, ContentCategory
from kensho_kenverters.convert_output import convert_output_to_items_list


def extract_organized_sections(
    serialized_document: dict[str, Any]
) -> list[list[dict[str, Any]]]:
    r"""Return a version of the output organized into sections split on titles.

    Args:
        serialized_document: a serialized document
    Returns:
        a list of sections, each of which is a list of items within that section in dictionary
            form describing their category and text value

    Example Output:
        [[
            {
                'category': 'title',
                'text': 'ESTIMATE for Kensho'
            },
            {
                'category': 'table',
                'table': [
                    ['Kensho Revenue in millions $', 'Q1', 'Q2', 'Q3', 'Q4'],
                    ['2020', '100,000', '200,000', '300,000', '400,000']
                ],
                'text': '| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| 2020 | '
                        '100,000 | 200,000 | 300,000 | 400,000 |'
            },
            {
                'category': 'text',
                'text': 'Machine learning (ML)'
            }
        ]]
    """
    markdown_items = convert_output_to_items_list(serialized_document)
    paragraphs: list[list[dict[str, Any]]] = []
    current_paragraph: list[dict[str, Any]] = []
    for item in markdown_items:
        # If this item is a title, split the section
        if (
            item[CATEGORY_KEY]
            in (ContentCategory.TITLE.value.lower(), ContentCategory.H1.value.lower())
            and current_paragraph
        ):
            paragraphs.append(current_paragraph)
            current_paragraph = []
        current_paragraph.append(item)
    if current_paragraph:
        paragraphs.append(current_paragraph)
    return paragraphs
