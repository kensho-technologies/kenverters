import itertools
from dataclasses import dataclass
from typing import Generic, Mapping, TypeVar

from kensho_kenverters.constants import AnnotationType

from .extract_output_models import AnnotationDataModel, AnnotationModel, ContentModel
from .output_to_tables import (
    build_uids_grid_from_table_cell_annotations,
    convert_uid_grid_to_content_grid,
)

T = TypeVar("T")


@dataclass(frozen=True)
class GridAndTextObject(Generic[T]):
    uid_grid: list[list[str | None]]
    text_data: list[list[str | None]]
    merges: list[tuple[int, int]]
    first_text_node: T
    last_text_node: T


def _calculate_merge_group_for_cell(
    table_cell: AnnotationDataModel,
) -> list[tuple[int, int]]:
    """Get the merge group for a table cell from its span.

    When a cell has a span greater than 1, i.e. a spanning cell, it should have a merge group
    that includes all the cells it spans over.
    """
    merges_group = []
    for row_delta, column_delta in itertools.product(
        range(table_cell.span[0]), range(table_cell.span[1])
    ):
        row_index = table_cell.index[0] + row_delta
        column_index = table_cell.index[1] + column_delta
        merges_group.append((row_index, column_index))
    return merges_group


def get_grid_and_merges_from_structured_output_table_annotation(
    annotation_content_uid_to_text_contents: Mapping[str, list[T]],
    annotations_related_to_table: list[AnnotationModel],
    table_content: ContentModel,
) -> GridAndTextObject[T]:
    """Get the table grid, structure, and first/last text objects from a table annotation.

    Args:
        annotation_content_uid_to_text_contents: Mapping from content UID to text objects.
        annotations_related_to_table: List of annotations related to the table.
        table_content: Table content from the structured output.

    Returns:
        Tuple of uid grid, text data, merges, first text object, and last text object.
    """

    merges: list[list[tuple[int, int]]] = []

    # Separate out table cell annotations
    table_cell_annotations = [
        cell
        for cell in annotations_related_to_table
        if cell.type == AnnotationType.TABLE_STRUCTURE.value
    ]
    # Build grid from table cell annotations
    uid_grid = build_uids_grid_from_table_cell_annotations(
        table_cell_annotations, duplicate_content_flag=False
    )
    cell_contents = table_content.children  # Safe to do in the current setup
    text_data: list[list[str | None]] = convert_uid_grid_to_content_grid(
        uid_grid, cell_contents
    )  # type: ignore
    # Convert "" to None
    for row_index, row in enumerate(text_data):
        for col in range(len(text_data[row_index])):
            if row[col] == "":
                text_data[row_index][col] = None

    # Get first and last text objects based on the ordering of the table
    first_text_node: T | None = None
    last_text_node: T | None = None

    for table_cell_annotation in table_cell_annotations:
        for uid in table_cell_annotation.content_uids:
            text_contents = annotation_content_uid_to_text_contents[uid]

            for text_content in text_contents:
                # Calculate merge group
                if (
                    table_cell_annotation.data.span[0] > 1
                    or table_cell_annotation.data.span[1] > 1
                ):
                    merges.append(
                        _calculate_merge_group_for_cell(table_cell_annotation.data)
                    )

                if first_text_node is None:
                    first_text_node = text_content

                last_text_node = text_content

    if first_text_node is None or last_text_node is None:
        raise AssertionError(
            f"Expected Extract Structured Output table {table_content} to have at least "
            "one text object associated with it."
        )

    return GridAndTextObject(
        uid_grid, text_data, merges, first_text_node, last_text_node  # type: ignore
    )
