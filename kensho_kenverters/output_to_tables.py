# Copyright 2024-present Kensho Technologies, LLC.
"""Functions to extract the tables in the output and turn them into pandas DataFrames."""

import typing
from collections import defaultdict
from typing import Any, Sequence

import pandas as pd

from .constants import (
    EMPTY_STRING,
    TABLE_CONTENT_CATEGORIES,
    AnnotationType,
    ContentCategory,
    TableType,
)
from .extract_output_models import (
    AnnotationModel,
    Cell,
    ContentModel,
    LocationModel,
    LocationType,
    Table,
    TableCategoryType,
    TableGridAndStructure,
)
from .tables_utils import (
    convert_table_to_pd_df,
    duplicate_spanning_annotations,
    get_table_shape,
)
from .utils import load_output_to_pydantic


def get_table_uid_to_cells_mapping(
    content: ContentModel,
) -> dict[str, list[ContentModel]]:
    """Recursively get table uids to cells mapping from nested structured document."""
    current_mapping: dict[str, list[ContentModel]] = {}
    if content.type in TABLE_CONTENT_CATEGORIES:
        # Termination condition 1
        cells = [
            child
            for child in content.children
            if child.type
            in (
                ContentCategory.TABLE_CELL.value,
                ContentCategory.FIGURE_EXTRACTED_TABLE_CELL.value,
            )
        ]
        current_mapping[content.uid] = cells
    elif len(content.children) > 0:
        for child in content.children:
            # Recursive call to children
            nested_mapping = get_table_uid_to_cells_mapping(child)
            current_mapping.update(nested_mapping)
    return current_mapping


def _get_table_uid_to_types_mapping(
    content: ContentModel,
) -> dict[str, TableCategoryType]:
    """Recursively get table uids to table types mapping."""
    table_uid_to_types: dict[str, TableCategoryType] = {}
    if content.type in TABLE_CONTENT_CATEGORIES:
        # Termination condition 1
        table_uid_to_types[content.uid] = typing.cast(TableCategoryType, content.type)
    elif len(content.children) > 0:
        for child in content.children:
            # Recursive call to children
            nested_mapping = _get_table_uid_to_types_mapping(child)
            table_uid_to_types.update(nested_mapping)
    return table_uid_to_types


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


def get_table_uid_to_annotations_mapping(
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
        # It's possible that we're only passing in table structure annotations or only
        # figure table structure annotations. In that case, we only want to keep the
        # annotations that match the cell uids.
        table_to_annotations[table_uid] = [
            uid_to_annotation[uid] for uid in cell_uids if uid in uid_to_annotation
        ]
    return table_to_annotations


def _convert_table_annotations_to_cells(
    table_annotations: list[AnnotationModel],
) -> list[Cell]:
    """Convert list of table annotations to list of cells.

    Args:
        table_annotations: a list of table structure annotations.

    Example Input:
        table_annotations = [AnnotationModel(content_uids=['2'],data=AnnotationDataModel(index=(0, 0),
        span=(1, 1), value=None, is_column_header=True, is_projected_row_header=False),type='table_structure',
        locations=[LocationModel(height=0.015,width=0.17, x=0.22, y=0.09, page_number=0)] ,
         AnnotationModel(content_uids=['3'],data=AnnotationDataModel(index=(0, 1), span=(1, 1),
        value=None, is_column_header=False,is_projected_row_header=False), type='table_structure',
        locations=[LocationModel(height=0.015, width=0.04, x=0.72, y=0.19, page_number=0),
        ...]
    """  # noqa: E501

    cells: list[Cell] = []
    for annotation in table_annotations:
        cell_index = annotation.data.index
        cell_span = annotation.data.span
        cell_is_column_header = annotation.data.is_column_header
        cell_is_projected_row_header = annotation.data.is_projected_row_header
        if annotation.locations is not None:
            cell_locations: list[LocationType] | None = [
                LocationModel.model_dump(loc) for loc in annotation.locations
            ]
        else:
            cell_locations = None
        cell = Cell(
            index=cell_index,
            span=cell_span,
            locations=cell_locations,
            is_column_header=cell_is_column_header,
            is_projected_row_header=cell_is_projected_row_header,
        )
        cells.append(cell)
    return cells


def build_uids_grid_from_table_cell_annotations(
    annotations: Sequence[AnnotationModel],
    duplicate_content_flag: bool = False,
) -> list[list[list[str]]]:
    """Build grid where each location has a list of content uids."""
    if any(
        annotation.type != AnnotationType.TABLE_STRUCTURE.value
        for annotation in annotations
    ):
        raise ValueError(
            "Content uids grid can only be built from table structure annotations."
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


def build_content_grid_from_figure_extracted_table_cell_annotations(
    annotations: Sequence[AnnotationModel],
) -> TableType:
    """Build content grid where each location has a string of content."""
    if any(
        annotation.type != AnnotationType.FIGURE_EXTRACTED_TABLE_STRUCTURE.value
        for annotation in annotations
    ):
        raise ValueError(
            "Content grid can only be built from figure extracted table structure annotations."
        )

    if any(annotation.data.value is None for annotation in annotations):
        raise ValueError(
            "Data value of figure extracted table structure "
            "annotations cannot be None."
        )
    # If annotations are figure extracted table structure, we fill the grids
    # with extracted values.
    n_rows, n_cols = get_table_shape(annotations)
    index_to_annotation_value_mapping = {}
    for annotation in annotations:
        if annotation.data.value is not None:
            index_to_annotation_value_mapping[annotation.data.index] = (
                annotation.data.value
            )
        else:
            index_to_annotation_value_mapping[annotation.data.index] = ""
    rows: list[list[str]] = []
    for row_index in range(n_rows):
        current_content_row = []
        for col_index in range(n_cols):
            current_content_row.append(
                index_to_annotation_value_mapping[(row_index, col_index)]
            )
        rows.append(current_content_row)
    return rows


def convert_uid_grid_to_content_grid(
    uid_grid: list[list[list[str]]], cell_contents: Sequence[ContentModel]
) -> list[list[str]]:
    """Convert a UID grid to content grid."""
    uids_to_content = {cell.uid: cell.content or EMPTY_STRING for cell in cell_contents}

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


# --------- Main API ---------


def build_table_grids(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
) -> dict[str, TableGridAndStructure]:
    """Convert serialized tables to objects consisting of table category type, string grid and structure annotations.

    Args:
        serialized_document: a serialized document
        duplicate_merged_cells_content_flag: If True, duplicate cell content for merged cells
        in 2D grid of strings. If False, only fill the first cell (top left) of the merged area,
        other cells are empty in 2D grid of strings.

    Returns:
        a mapping of table UIDs to the objects consisting of the table category type, the string
        grid and the structure annotations.
    Example Output:
        {
            '1': TableGridAndStructure(table_category_type = "TABLE", table_string_grid =
            [['header1', 'header2'], ['row1_val', 'row2_val']], tables_structure_annotations =
            [AnnotationModel(content_uids=['2'],data=AnnotationDataModel(index=(0, 0), span=(1, 1),
            value=None, is_column_header=True, is_projected_row_header=False),type='table_structure',
            locations=[LocationModel(height=0.015,width=0.17, x=0.22, y=0.09, page_number=0)]), ...]),
            '2': TableGridAndStructure(table_category_type = "FIGURE_EXTRACTED_TABLE",table_string_grid =
             [['another_header1'], ['another_row1_val']], tables_structure_annotations =
             [AnnotationModel(content_uids=['26'],data=AnnotationDataModel(index=(4, 4), span=(1, 1),
            value=None, is_column_header=False,is_projected_row_header=False), type='table_structure',
            locations=[LocationModel(height=0.015, width=0.04, x=0.72, y=0.19, page_number=0), ...])
        }
    """  # noqa: E501
    parsed_serialized_document = load_output_to_pydantic(serialized_document)
    annotations = parsed_serialized_document.annotations
    content = parsed_serialized_document.content_tree

    table_uid_to_cells_mapping = get_table_uid_to_cells_mapping(content)
    table_uid_to_type_mapping = _get_table_uid_to_types_mapping(content)

    table_cell_annotations = [
        annotation
        for annotation in annotations
        if annotation.type
        in (
            AnnotationType.TABLE_STRUCTURE.value,
            AnnotationType.FIGURE_EXTRACTED_TABLE_STRUCTURE.value,
        )
    ]
    table_uid_to_cell_annotations = get_table_uid_to_annotations_mapping(
        table_uid_to_cells_mapping, table_cell_annotations
    )

    tables_grid_and_structure = {}
    for table_uid, cell_annotations in table_uid_to_cell_annotations.items():
        if table_uid_to_type_mapping[table_uid] in (
            ContentCategory.TABLE.value,
            ContentCategory.TABLE_OF_CONTENTS.value,
        ):
            uids_grid = build_uids_grid_from_table_cell_annotations(
                cell_annotations,
                duplicate_content_flag=duplicate_merged_cells_content_flag,
            )
            cell_contents = table_uid_to_cells_mapping[table_uid]
            content_grid = convert_uid_grid_to_content_grid(uids_grid, cell_contents)
        else:
            content_grid = (
                build_content_grid_from_figure_extracted_table_cell_annotations(
                    cell_annotations
                )
            )
        tables_grid_and_structure[table_uid] = TableGridAndStructure(
            table_category_type=table_uid_to_type_mapping[table_uid],
            table_string_grid=content_grid,
            table_structure_annotations=table_uid_to_cell_annotations[table_uid],
        )

    return tables_grid_and_structure


def extract_pd_dfs_from_output(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
    use_first_row_as_header: bool = True,
    include_figure_extracted_table: bool = False,
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
    table_id_to_grid_and_structure = build_table_grids(
        serialized_document, duplicate_merged_cells_content_flag
    )
    table_dfs = []
    for table_grid_structure in table_id_to_grid_and_structure.values():
        if table_grid_structure.table_category_type in (
            ContentCategory.TABLE.value,
            ContentCategory.TABLE_OF_CONTENTS.value,
        ) or (
            include_figure_extracted_table
            and table_grid_structure.table_category_type
            == ContentCategory.FIGURE_EXTRACTED_TABLE.value
        ):
            table_df = convert_table_to_pd_df(
                table_grid_structure.table_string_grid,
                use_first_row_as_header=use_first_row_as_header,
            )
            table_dfs.append(table_df)

    return table_dfs


def extract_pd_dfs_with_locs_and_table_structure_from_output(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
    use_first_row_as_header: bool = True,
    include_figure_extracted_table: bool = False,
) -> list[Table]:
    """Extract tables and convert them to a list of pd DataFrames, table locations and structures.

    Args:
        serialized_document: a serialized document
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area, other cells are
            empty.
        use_first_row_as_header: if True, use the first row of the extracted table as the columns.
            Set to False if you know there is no header row in your tables.

    Returns:
        a list of Table NamedTuples with a pandas DataFrame, locations and structures.

    Example Output:
        [Table(
            df=Kensho Revenue in millions $       Q1       Q2       Q3       Q4
                0                         2020  100,000  200,000  300,000  400,000
                1                         2021  101,001  201,001  301,001  401,001
                2                         2022  102,004  202,004  302,004  402,004
                3                         2023  103,009  203,009  303,009  403,009,
            locations=[
                {'height': 0.09188, 'width': 0.66072, 'x': 0.16008, 'y': 0.40464, 'page_number': 0}
            ],
            cells=[Cell(index=(0, 0), span=(1, 1), locations=[{'height': 0.01188,
            'width': 0.22128, 'x': 0.16008, 'y': 0.40464, 'page_number': 0}],
            is_column_header=True, is_projected_row_header=False), ...]
        )]
    """
    # Get dfs
    table_id_to_grid_and_structure = build_table_grids(
        serialized_document, duplicate_merged_cells_content_flag
    )

    # Get locations
    parsed_serialized_document = load_output_to_pydantic(serialized_document)
    table_uid_to_locs_mapping = _get_table_uid_to_locations_mapping(
        parsed_serialized_document.content_tree
    )

    # Match dfs and locations
    tables: list[Table] = []
    for table_uid, table_grid_and_structure in table_id_to_grid_and_structure.items():
        if table_grid_and_structure.table_category_type in (
            ContentCategory.TABLE.value,
            ContentCategory.TABLE_OF_CONTENTS.value,
        ) or (
            include_figure_extracted_table
            and table_grid_and_structure.table_category_type
            == ContentCategory.FIGURE_EXTRACTED_TABLE.value
        ):
            table_df = convert_table_to_pd_df(
                table_grid_and_structure.table_string_grid,
                use_first_row_as_header=use_first_row_as_header,
            )
            table_cells = _convert_table_annotations_to_cells(
                table_grid_and_structure.table_structure_annotations
            )
            tables.append(
                Table(
                    df=table_df,
                    table_type=table_grid_and_structure.table_category_type,
                    locations=table_uid_to_locs_mapping[table_uid],
                    cells=table_cells,
                )
            )
    return tables
