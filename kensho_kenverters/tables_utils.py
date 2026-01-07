# Copyright 2024-present Kensho Technologies, LLC.
"""Helper functions for formatting tables."""

import copy
from typing import Sequence

import pandas as pd

from .constants import AnnotationType
from .extract_output_models import (
    AnnotationDataModel,
    AnnotationModel,
    TableGridAndStructure,
    TableStringGridType,
)


def _create_empty_annotation(row: int, col: int) -> AnnotationModel:
    """Create an empty annotation."""
    return AnnotationModel(
        type=AnnotationType.TABLE_STRUCTURE.value,
        content_uids=[],
        data=AnnotationDataModel(
            span=(1, 1),
            index=(row, col),
        ),
        locations=None,
    )


def _validate_annotations(
    duplicated_annotations: list[AnnotationModel], max_row: int, max_col: int
) -> list[AnnotationModel]:
    """Validate duplicated annotations.

    Fill with empty annotations if rows or columns are missing.
    """

    # Check all spans are 1 (annotations are duplicated)
    all_spans = [annotation.data.span for annotation in duplicated_annotations]
    if any(span != (1, 1) for span in all_spans):
        raise ValueError("Un-duplicated merged cells in table.")

    # Check no overlap
    all_indices = [annotation.data.index for annotation in duplicated_annotations]
    if len(set(all_indices)) != len(all_indices):
        raise ValueError("Overlapping indices in table.")

    # Add any missing cells
    for row in range(max_row + 1):
        for col in range(max_col + 1):
            if (row, col) not in all_indices:
                duplicated_annotations.append(_create_empty_annotation(row, col))

    return duplicated_annotations


def duplicate_spanning_annotations(
    annotations: Sequence[AnnotationModel], duplicate_content_flag: bool = True
) -> list[AnnotationModel]:
    """Get duplicated annotations.

    Returns a list of annotations with span (1, 1). Input annotations that span more than one
    row and/or column are duplicated.

    Args:
        annotations: annotations to duplicate
        duplicate_content_flag: if True, duplicate text box content into all spanned table cells.
            If False, only fill the top left cell. Other spanned cells will be empty.

    Returns:
        duplicated annotations. Duplicated annotations must all have span (1, 1).
    """
    duplicated_annotations = []
    max_row = 0
    max_col = 0
    for annotation in annotations:
        data = annotation.data
        row_span, col_span = data.span
        row_index, col_index = data.index
        for row_span_index in range(row_span):
            for col_span_index in range(col_span):
                if duplicate_content_flag or (
                    row_span_index == 0 and col_span_index == 0
                ):
                    content_uids = annotation.content_uids
                else:
                    content_uids = []
                new_annotation = AnnotationModel(
                    type=annotation.type,
                    content_uids=content_uids,
                    data=AnnotationDataModel(
                        span=(1, 1),
                        index=(row_index + row_span_index, col_index + col_span_index),
                    ),
                    # Purposely not splitting locations as they're not necessary for
                    # formatting purposes
                    locations=annotation.locations,
                )
                duplicated_annotations.append(new_annotation)
                max_row = max(max_row, row_index + row_span_index)
                max_col = max(max_col, col_index + col_span_index)

    return _validate_annotations(duplicated_annotations, max_row, max_col)


def get_table_shape(
    table_structure_annotations: Sequence[AnnotationModel],
) -> tuple[int, int]:
    """Get table shape from table structure annotations."""
    if any(
        annotation.type
        not in (
            AnnotationType.TABLE_STRUCTURE.value,
            AnnotationType.FIGURE_EXTRACTED_TABLE_STRUCTURE.value,
        )
        for annotation in table_structure_annotations
    ):
        raise ValueError(
            "Table shape can only be calculated from table structure "
            "or figure extracted table annotations."
        )
    n_rows = (
        max(
            annotation.data.index[0] + annotation.data.span[0]
            for annotation in table_structure_annotations
        )
        if table_structure_annotations
        else 0
    )
    n_cols = (
        max(
            annotation.data.index[1] + annotation.data.span[1]
            for annotation in table_structure_annotations
        )
        if table_structure_annotations
        else 0
    )
    return n_rows, n_cols


def convert_table_to_pd_df(
    table_grid: list[list[str]], use_first_row_as_header: bool = True
) -> pd.DataFrame:
    """Convert a 2D list of strings to a pandas DataFrame.

    Use the first row as a header if use_first_row_as_header set to True.

    Args:
        table_grid: 2D list of strings making up the table
        use_first_row_as_header: if True, will take the first row of the table and make it the
            header of the pandas DataFrame

    Returns:
        pandas DataFrame representing the table
    """
    # Make first row the header
    if use_first_row_as_header and len(table_grid) > 1:
        table_df = pd.DataFrame(table_grid[1:], columns=table_grid[0])
    else:
        table_df = pd.DataFrame(table_grid)
    return table_df


# --------- Table splitting utils ---------


def get_column_headers_and_project_row_headers_row_ids(
    annotations: list[AnnotationModel],
) -> tuple[set[int], set[int]]:
    """Get the row ids of column_headers and project_row_headers."""

    # Extract the row ids of column headers and project row headers.
    column_header_row_ids = set()
    project_row_headers_row_ids = set()
    for annotation in annotations:
        if annotation.data.is_column_header or annotation.data.is_projected_row_header:
            for column_row_id in range(
                annotation.data.index[0],
                annotation.data.index[0] + annotation.data.span[0],
            ):
                if (
                    annotation.data.is_column_header
                    and column_row_id not in column_header_row_ids
                ):
                    column_header_row_ids.add(column_row_id)
                elif (
                    annotation.data.is_projected_row_header
                    and column_row_id not in project_row_headers_row_ids
                ):
                    project_row_headers_row_ids.add(column_row_id)

    return column_header_row_ids, project_row_headers_row_ids


def table_can_be_split(
    column_header_row_ids: set[int], project_row_headers_row_ids: set[int]
) -> bool:
    """To verify if a table can be split.

    A table can be split only if there are column headers and project row headers and the
    column header row ids are consecutive starting from the initial.
    """
    # To verify whether there are column headers
    if len(column_header_row_ids) > 0:

        # To verify whether there are project_row_headers and whether the
        # column header row ids are consecutive starting from the initial.
        col_header_row_ids_consecutive_from_initial = (
            max(column_header_row_ids) == len(column_header_row_ids) - 1
        )

        if (
            len(project_row_headers_row_ids) > 0
            and col_header_row_ids_consecutive_from_initial
        ):
            return True

    return False


def _split_row_ids_after_column_headers(
    max_column_header_row_id: int,
    n_row: int,
    project_row_header_row_ids: set[int],
) -> list[list[int]]:
    """To split row ids (after column headers) of long table into sub-lists of row ids based on the project row headers.

    We split the row ids (after the column headers) of long table based on the position of project row headers. The output
    of this function will be a list of sub-lists of row ids for subtables.
    """  # noqa: E501

    initial_row_id = max_column_header_row_id + 1

    # Initial the empty list of subtable row ids.
    subtable_row_ids_list = []

    # Split the row ids (after column headers) into a list of sublist of row ids of subtables.
    row_id_cursor = initial_row_id
    non_project_row_header_row_id_list: list[int] = []
    for row_idx in range(initial_row_id, n_row):
        if row_idx == n_row - 1:
            subtable_row_ids_list.append(list(range(row_id_cursor, row_idx + 1)))
        elif row_idx in project_row_header_row_ids:
            if len(non_project_row_header_row_id_list) > 0:
                subtable_row_ids_list.append(list(range(row_id_cursor, row_idx)))
                row_id_cursor = row_idx
                non_project_row_header_row_id_list = []
        else:
            non_project_row_header_row_id_list.append(row_idx)
    return subtable_row_ids_list


def _extract_string_grids_by_row_ids(
    table_string_grid: TableStringGridType, target_row_ids: list[int]
) -> TableStringGridType:
    """Extract the table string grid based on row ids.

    We extract specific rows of table string grid and return it as a new table string grid.
    """
    # Initialize the empty list of table grid.
    extract_string_grid = []
    # Extrac the table string grid based on row ids
    for row_id, row_grid in enumerate(table_string_grid):
        if row_id in target_row_ids:
            extract_string_grid.append(row_grid)
    return extract_string_grid


def _extract_structure_annotations_by_row_ids(
    table_structure_annotations: list[AnnotationModel], target_row_ids: list[int]
) -> list[AnnotationModel]:
    """Extract the table structure annotations based on row ids.

    We extract table structure annotations of specific rows and return them as a new list of table structure annotations.
    """  # noqa: E501
    # Initialize the empty list of table structure annotations.
    extract_structure_annotations = []
    # Extrac the table structure annotations grid based on row ids
    for annotation in table_structure_annotations:
        if annotation.data.index[0] in target_row_ids:
            extract_structure_annotations.append(annotation)
    return extract_structure_annotations


def _adjust_row_indexes_of_structure_annotations(
    row_offset: int, table_structure_annotations: list[AnnotationModel]
) -> list[AnnotationModel]:
    """Adjust the row indexes of the structure annotations."""

    adjusted_structure_annotations = []
    for annotation in table_structure_annotations:
        adjusted_index = (
            annotation.data.index[0] + row_offset,
            annotation.data.index[1],
        )
        annotation_temp = copy.deepcopy(annotation)
        annotation_temp.data.index = adjusted_index
        adjusted_structure_annotations.append(annotation_temp)
    return adjusted_structure_annotations


def split_table_into_subtables(
    table_grid_and_structure: TableGridAndStructure,
    column_header_row_ids: set[int],
    project_row_header_row_ids: set[int],
) -> tuple[list[TableStringGridType], list[list[AnnotationModel]]]:
    """To split long table into small subtables based on project row headers.

    We split the string grid and structure annotations of long table based on project row headers and return
    a list of string grid of subtables and a list of sublist of structure annotations for subtables.
    We also concatenate the string grid and structure annotations from column headers to each subtable.
    """  # noqa: E501

    max_column_header_row_id = max(column_header_row_ids)
    n_rows = len(table_grid_and_structure.table_string_grid)

    # Split the row ids (after the column header) based on the
    # project row headers
    subtable_row_ids_list = _split_row_ids_after_column_headers(
        max_column_header_row_id, n_rows, project_row_header_row_ids
    )

    # Extract the string grid for subtables
    subtable_string_grid_list = []
    for subtable_row_ids in subtable_row_ids_list:
        subtable_string_grid = _extract_string_grids_by_row_ids(
            table_grid_and_structure.table_string_grid, subtable_row_ids
        )
        subtable_string_grid_list.append(subtable_string_grid)

    # Extract the structure annotations for subtables
    subtable_structure_annotations_list = []
    for subtable_row_ids in subtable_row_ids_list:
        subtable_structure_annotations = _extract_structure_annotations_by_row_ids(
            table_grid_and_structure.table_structure_annotations, subtable_row_ids
        )
        # Adjust the row index of annotations such that it is compatible to
        # the concatenating column header rows.
        adjusted_subtable_structure_annotations = (
            _adjust_row_indexes_of_structure_annotations(
                max_column_header_row_id - min(subtable_row_ids) + 1,
                subtable_structure_annotations,
            )
        )
        subtable_structure_annotations_list.append(
            adjusted_subtable_structure_annotations
        )

    # Extract string grid and structure annotations of column headers
    column_header_grid = table_grid_and_structure.table_string_grid[
        : max_column_header_row_id + 1
    ]
    column_header_annotations = []
    for annotation in table_grid_and_structure.table_structure_annotations:
        if annotation.data.index[0] <= max_column_header_row_id:
            column_header_annotations.append(annotation)

    # Concatenate the column header string grid and structure annotations to each subtable and
    # return the string grid and structure annotations of subtables.
    return [
        column_header_grid + subtable_string_grid
        for subtable_string_grid in subtable_string_grid_list
    ], [
        column_header_annotations + subtable_structure_annotations
        for subtable_structure_annotations in subtable_structure_annotations_list
    ]


def extract_project_row_headers(
    table_structure_annotations: list[AnnotationModel],
    table_string_grid: TableStringGridType,
) -> list[str]:
    """Extract project row headers."""
    project_row_headers: list[str] = []
    for annotation in table_structure_annotations:
        if annotation.data.is_projected_row_header:
            project_row_headers.append(
                table_string_grid[annotation.data.index[0]][annotation.data.index[1]]
            )
    return project_row_headers
