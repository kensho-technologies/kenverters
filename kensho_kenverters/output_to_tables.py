# Copyright 2024-present Kensho Technologies, LLC.
"""Functions to extract the tables in the output and turn them into pandas DataFrames."""

from collections import defaultdict
from typing import Any, Sequence

import pandas as pd

from kensho_kenverters.constants import (
    TABLE_CONTENT_CATEGORIES,
    AnnotationType,
    ContentCategory,
)
from kensho_kenverters.extract_output_models import (
    AnnotationModel,
    ContentModel,
    LocationModel,
    LocationType,
    Table,
)
from kensho_kenverters.tables_utils import (
    convert_table_to_pd_df,
    duplicate_spanning_annotations,
    get_table_shape,
)
from kensho_kenverters.utils import load_output_to_pydantic


def _get_table_uid_to_cells_mapping(
    content: ContentModel,
) -> dict[str, list[ContentModel]]:
    """Recursively get table uids to cells mapping from nested structured document."""
    current_mapping: dict[str, list[ContentModel]] = {}
    if content.type in TABLE_CONTENT_CATEGORIES:
        # Termination condition 1
        cells = [
            child
            for child in content.children
            if child.type == ContentCategory.TABLE_CELL.value
        ]
        current_mapping[content.uid] = cells
    elif len(content.children) > 0:
        for child in content.children:
            # Recursive call to children
            nested_mapping = _get_table_uid_to_cells_mapping(child)
            current_mapping.update(nested_mapping)
    return current_mapping


def _get_table_uid_to_locations_mapping(
    content: ContentModel,
) -> dict[str, list[LocationType]]:
    """Recursively get table uids to locations mapping from nested structured document."""
    current_mapping: dict[str, list[LocationType]] = {}
    if content.type in TABLE_CONTENT_CATEGORIES:
        # Termination condition 1
        if content.locations is not None:
            current_mapping[content.uid] = [
                LocationModel.model_dump(loc) for loc in content.locations
            ]
        else:
            current_mapping[content.uid] = [None]
    elif len(content.children) > 0:
        for child in content.children:
            # Recursive call to children
            nested_mapping = _get_table_uid_to_locations_mapping(child)
            current_mapping.update(nested_mapping)
    return current_mapping


def _get_table_uid_to_annotations_mapping(
    table_uid_to_cells: dict[str, list[ContentModel]],
    table_cell_annotations: list[AnnotationModel],
) -> dict[str, list[AnnotationModel]]:
    """Get table uid to table structure annotations mapping."""
    uid_to_annotation: dict[str, AnnotationModel] = {
        annotation.content_uids[0]: annotation for annotation in table_cell_annotations
    }
    table_to_annotations = {}
    for table_uid, cells in table_uid_to_cells.items():
        cell_uids = [cell.uid for cell in cells]
        table_to_annotations[table_uid] = [uid_to_annotation[uid] for uid in cell_uids]
    return table_to_annotations


def _build_grid_from_table_cell_annotations(
    annotations: Sequence[AnnotationModel], duplicate_content_flag: bool = False
) -> list[list[list[str]]]:
    """Build grid where each location has a list of content uids."""
    if any(
        annotation.type != AnnotationType.TABLE_STRUCTURE.value
        for annotation in annotations
    ):
        raise ValueError(
            "Table grid can only be built from table structure annotations."
        )

    duplicated_annotations = duplicate_spanning_annotations(
        annotations, duplicate_content_flag
    )
    index_to_uids_mapping = defaultdict(
        list,
        {
            annotation.data.index: annotation.content_uids
            for annotation in duplicated_annotations
        },
    )

    n_rows, n_cols = get_table_shape(duplicated_annotations)

    rows: list[list[list[str]]] = []
    for row_index in range(n_rows):
        current_row = []
        for col_index in range(n_cols):
            current_row.append(index_to_uids_mapping[(row_index, col_index)])
        rows.append(current_row)
    return rows


def _convert_uid_grid_to_content_grid(
    uid_grid: list[list[list[str]]], cell_contents: Sequence[ContentModel]
) -> list[list[str]]:
    """Convert a UID grid to content grid."""
    uids_to_content = {cell.uid: cell.content for cell in cell_contents}
    content_grid = []
    for uid_row in uid_grid:
        content_row = []
        for content_uids in uid_row:
            if len(content_uids) > 0:
                first_content_uid = content_uids[0]
                text = uids_to_content[first_content_uid]
                # content will always exist except for a DOCUMENT type, which has long been
                # filtered out. Check anyway
                if text is None:
                    raise ValueError(
                        "Found content=None for a table cell. Table cells must have str content."
                    )
            else:
                text = ""
            content_row.append(text)
        content_grid.append(content_row)
    return content_grid


def build_table_grids(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
) -> dict[str, list[list[str]]]:
    """Convert serialized tables to a 2D grid of strings.

    Args:
        serialized_document: a serialized document
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area, other cells are
            empty.

    Returns:
        a mapping of table UIDs to table grid structures

    Example Output:
        {
            '1': [['header1', 'header2'], ['row1_val', 'row2_val']],
            '2': [['another_header1'], ['another_row1_val']]
        }
    """
    parsed_serialized_document = load_output_to_pydantic(serialized_document)
    annotations = parsed_serialized_document.annotations
    content = parsed_serialized_document.content_tree

    table_uid_to_cells_mapping = _get_table_uid_to_cells_mapping(content)

    table_cell_annotations = [
        annotation
        for annotation in annotations
        if annotation.type == AnnotationType.TABLE_STRUCTURE.value
    ]
    table_uid_to_cell_annotations = _get_table_uid_to_annotations_mapping(
        table_uid_to_cells_mapping, table_cell_annotations
    )

    tables = {}
    for table_uid, cell_annotations in table_uid_to_cell_annotations.items():
        grid = _build_grid_from_table_cell_annotations(
            cell_annotations, duplicate_content_flag=duplicate_merged_cells_content_flag
        )
        cell_contents = table_uid_to_cells_mapping[table_uid]
        content_grid = _convert_uid_grid_to_content_grid(grid, cell_contents)
        tables[table_uid] = content_grid
    return tables


def extract_pd_dfs_from_output(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
    use_first_row_as_header: bool = True,
) -> list[pd.DataFrame]:
    """Extract Extract output's tables and convert them to a list of pandas DataFrames.

    Args:
        serialized_document: a serialized document
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area, other cells are
            empty.
        use_first_row_as_header: if True, use the first row of the extracted table as the columns.
            Set to False if you know there is no header row in your tables.

    Returns:
            a list of pandas DataFrames, each containing a table

    Example Output:
        [  Kensho Revenue in millions $       Q1       Q2       Q3       Q4
        0                         2020  100,000  200,000  300,000  400,000
        1                         2021  101,001  201,001  301,001  401,001
        2                         2022  102,004  202,004  302,004  402,004
        3                         2023  103,009  203,009  303,009  403,009]
    """
    table_grids = build_table_grids(
        serialized_document, duplicate_merged_cells_content_flag
    )
    table_dfs = []
    for table_grid in table_grids.values():
        table_df = convert_table_to_pd_df(
            table_grid, use_first_row_as_header=use_first_row_as_header
        )
        table_dfs.append(table_df)

    return table_dfs


def extract_pd_dfs_with_locs_from_output(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
    use_first_row_as_header: bool = True,
) -> list[Table]:
    """Extract tables from output and convert them to a list of pd DataFrames and table locations.

    Args:
        serialized_document: a serialized document
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area, other cells are
            empty.
        use_first_row_as_header: if True, use the first row of the extracted table as the columns.
            Set to False if you know there is no header row in your tables.

    Returns:
        a list of Table NamedTuples with a pandas DataFrame and locations

    Example Output:
        [Table(
            df=Kensho Revenue in millions $       Q1       Q2       Q3       Q4
                0                         2020  100,000  200,000  300,000  400,000
                1                         2021  101,001  201,001  301,001  401,001
                2                         2022  102,004  202,004  302,004  402,004
                3                         2023  103,009  203,009  303,009  403,009,
            locations=[
                {'height': 0.09188, 'width': 0.66072, 'x': 0.16008, 'y': 0.40464, 'page_number': 0}
            ]
        )]
    """
    # Get dfs
    table_grids = build_table_grids(
        serialized_document, duplicate_merged_cells_content_flag
    )

    # Get locations
    parsed_serialized_document = load_output_to_pydantic(serialized_document)
    table_uid_to_locs_mapping = _get_table_uid_to_locations_mapping(
        parsed_serialized_document.content_tree
    )

    # Match dfs and locations
    tables: list[Table] = []
    for table_uid, table_grid in table_grids.items():
        table_df = convert_table_to_pd_df(
            table_grid, use_first_row_as_header=use_first_row_as_header
        )
        tables.append(
            Table(df=table_df, locations=table_uid_to_locs_mapping[table_uid])
        )
    return tables
