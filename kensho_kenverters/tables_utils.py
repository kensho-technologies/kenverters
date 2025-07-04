# Copyright 2024-present Kensho Technologies, LLC.
"""Helper functions for formatting tables."""

from typing import Sequence

import pandas as pd

from .constants import AnnotationType
from .extract_output_models import AnnotationDataModel, AnnotationModel


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
