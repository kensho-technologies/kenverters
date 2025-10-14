# Copyright 2024-present Kensho Technologies, LLC.
"""Helper functions for formatting tables."""

from typing import Sequence

import pandas as pd

from .constants import AnnotationType, EMPTY_STRING
from .extract_output_models import AnnotationDataModel, AnnotationModel, ContentModel, TableCategoryType, LocationType
from .extract_output_models import Table

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


def get_projected_row_header_row_indexes(
        table_structure_annotations: Sequence[AnnotationModel]) -> list[int]:
    """Get the row indexes of projected row headers."""
    # Get the number of column of the table
    _, n_cols = get_table_shape(table_structure_annotations)

    # Get the projected row header row indexes
    projected_row_header_row_indexes: list[int] = []

    for annotation in table_structure_annotations:
        data = annotation.data
        row_span, col_span = data.span
        # If the cell is spread in all the columns, it should be projected row header.
        if row_span == 1 and col_span == n_cols:
            row_index, col_index = data.index
            if row_index not in projected_row_header_row_indexes:
                projected_row_header_row_indexes.append(row_index)

    projected_row_header_row_indexes.sort()
    return projected_row_header_row_indexes


def _verify_all_contents_empty_or_contain_alphabet(content_string_list: list[str]) -> bool:
    """Verify whether the current row is a row with all contents either empty or contain alphabet."""
    for content_string in content_string_list:
        if content_string != EMPTY_STRING and any(char.isalpha() for char in content_string) is False:
            return False
    return True


def get_column_header_row_max_index(table_structure_annotations: Sequence[AnnotationModel],
                                  cell_contents: Sequence[ContentModel],
                                  projected_row_header_row_indexes:list[int]) -> int:
    """Get the maximum index of the rows of column headers."""
    # Get number of rows of the table
    n_rows, _ = get_table_shape(table_structure_annotations)

    # Get the mapping from uids to contents
    uids_to_content = {cell.uid: cell.content or EMPTY_STRING for cell in cell_contents}

    # Get the mapping from row indexes to list of contents
    row_indexes_to_contents : dict[str, list[str]] = {row_index:[] for row_index in range(n_rows)}
    for annotation in table_structure_annotations:
        data = annotation.data
        row_span, col_span = data.span
        row_index, _ = data.index
        annotation_content_string = " ".join([uids_to_content[content_uid] for content_uid in annotation.content_uids])
        for row_span_index in range(row_span):
            row_indexes_to_contents[row_index + row_span_index].append(annotation_content_string)

    # Get the row index of column headers
    column_header_row_max_index_candidates : list[int] = []
    for row_index in range(n_rows):
        # Verify whether all contents of the row either empty or containing alphabet
        if _verify_all_contents_empty_or_contain_alphabet(row_indexes_to_contents[row_index]) == True:
            # If pass the verification and either the first row or non-projected-header-row, add it in the list of max index candidates.
            if row_index == 0 or row_index not in projected_row_header_row_indexes:
                column_header_row_max_index_candidates.append(row_index)
        # If fail the verification, break the loop
        else:
            break

    if len(column_header_row_max_index_candidates) > 0:
        return max(column_header_row_max_index_candidates)
    else:
        return None


def split_table_dataframe_by_projected_row_headers(table_df: pd.DataFrame,
                                                   table_type: TableCategoryType,
                                                   projected_row_header_row_indexes:list[int] | None,
                                                   column_header_row_max_index:int|None,
                                                   locations: list[LocationType] | None = None) -> list[Table]:
    """Split table dataframe by projected row headers."""
    if projected_row_header_row_indexes is None or len(projected_row_header_row_indexes) == 0 or column_header_row_max_index is None:
        return [Table(df=table_df,
                      table_type=table_type,
                      locations=locations,
                    )]

    splitting_tables: list[Table] = []
    n_rows = len(table_df)
    column_header_rows_df = table_df[:column_header_row_max_index]

    extracted_data_row_indexes: list[int] = []
    captions_list: list[str] = []
    for row_index in range(column_header_row_max_index, n_rows):
        if row_index in projected_row_header_row_indexes or row_index == n_rows - 1:
            # If the last row and the last row is not projected row header, add the index into extracted data row indexes.
            if row_index not in projected_row_header_row_indexes:
                extracted_data_row_indexes.append(row_index)

            if len(extracted_data_row_indexes) > 0:
                extract_data_df = table_df.iloc[extracted_data_row_indexes]
                extract_table_df = pd.concat([column_header_rows_df, extract_data_df], ignore_index = True)
                splitting_tables.append(Table(df=extract_table_df,
                      table_type=table_type,
                      locations=locations,
                      captions = captions_list,
                      from_splitting = True,
                    ))
                # reset the list of indexes of extracted data rows and caption list
                extracted_data_row_indexes = []
                captions_list = []
            captions_list.append(table_df.iloc[row_index, 0])
        else:
            extracted_data_row_indexes.append(row_index)
    return splitting_tables

















