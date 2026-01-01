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
    TableStringGridType,
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
    table_string_grid: TableStringGridType,
) -> tuple[list[Cell], list[str]]:
    """Convert list of table annotations to list of cells and return the project row header of the table.

    Args:
        table_annotations: a list of table structure annotations.
        table_string_grid: a list of table string grids.

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
    project_row_headers: list[str] = []
    for annotation in table_annotations:
        if annotation.data.is_projected_row_header:
            project_row_headers.append(
                table_string_grid[annotation.data.index[0]][annotation.data.index[1]]
            )

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
    return cells, project_row_headers


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


def _get_max_col_header_row_and_project_header_rows(
    annotations: list[AnnotationModel], n_row: int
) -> tuple[int | None, list[int]]:
    """Get the max column header row and project header row from the annotations list."""
    # Extract the row ids of column headers and project row headers
    column_header_rows = []
    project_row_headers_rows = []
    for annotation in annotations:
        if annotation.data.is_column_header or annotation.data.is_projected_row_header:
            for column_header_row_idx in range(
                annotation.data.index[0],
                annotation.data.index[0] + annotation.data.span[0],
            ):
                if (
                    annotation.data.is_column_header
                    and column_header_row_idx not in column_header_rows
                ):
                    column_header_rows.append(column_header_row_idx)
                elif (
                    annotation.data.is_projected_row_header
                    and column_header_row_idx not in project_row_headers_rows
                ):
                    project_row_headers_rows.append(column_header_row_idx)

    max_column_header_row_id = None
    for row_idx in range(n_row):
        if row_idx in column_header_rows:
            max_column_header_row_id = row_idx
        else:
            break
    project_row_headers_rows.sort()
    return max_column_header_row_id, project_row_headers_rows


def _split_row_ids(
    max_column_header_row_id: int | None,
    n_row: int,
    project_row_headers_rows: list[int],
) -> list[list[int]]:
    """Split row ids into several sub-list of row ids based on the project row headers rows."""
    if max_column_header_row_id is not None:
        initial_row_id = max_column_header_row_id + 1
    else:
        initial_row_id = 0
    subtables_row_id_list = []
    row_id_cursor = initial_row_id
    non_project_row_header_row_id_list: list[int] = []
    for row_idx in range(initial_row_id, n_row):
        if row_idx == n_row - 1:
            subtables_row_id_list.append(list(range(row_id_cursor, row_idx + 1)))
        elif row_idx in project_row_headers_rows:
            if len(non_project_row_header_row_id_list) > 0:
                subtables_row_id_list.append(list(range(row_id_cursor, row_idx)))
                row_id_cursor = row_idx
                non_project_row_header_row_id_list = []
        elif row_idx not in project_row_headers_rows:
            non_project_row_header_row_id_list.append(row_idx)
    return subtables_row_id_list


def _split_table_grids_and_annotations(
    max_column_header_row_id: int | None,
    subtables_row_ids_list: list[list[int]],
    table_grid_and_structure: TableGridAndStructure,
) -> tuple[list[TableStringGridType], list[list[AnnotationModel]]]:
    """Split the table grids and structure annotations into several sub-list of table grid and structure annotations based on the project row headers."""  # noqa: E501
    if max_column_header_row_id is not None:
        intial_row_id = max_column_header_row_id + 1
    else:
        intial_row_id = 0

    subtable_string_grids_list: list[TableStringGridType] = []
    subtable_structure_annotations_list: list[list[AnnotationModel]] = []
    for subtable_id in range(len(subtables_row_ids_list)):
        subtable_string_grids_list.append([])
        subtable_structure_annotations_list.append([])

    for row_id, row_grid in enumerate(table_grid_and_structure.table_string_grid):
        for subtable_id, subtable_row_ids in enumerate(subtables_row_ids_list):
            if row_id in subtable_row_ids:
                subtable_string_grids_list[subtable_id].append(row_grid)

    for annotation in table_grid_and_structure.table_structure_annotations:
        for subtable_id, subtable_row_ids in enumerate(subtables_row_ids_list):
            if annotation.data.index[0] in subtable_row_ids:
                adjusted_index = (
                    intial_row_id + annotation.data.index[0] - min(subtable_row_ids),
                    annotation.data.index[1],
                )
                annotation.data.index = adjusted_index
                subtable_structure_annotations_list[subtable_id].append(annotation)

    return subtable_string_grids_list, subtable_structure_annotations_list


def _split_long_tables(
    table_grid_and_structure: TableGridAndStructure,
) -> tuple[list[TableStringGridType], list[list[AnnotationModel]]]:
    """Split the grids and structure annotations of long tables into small tables based on project row header."""  # noqa: E501

    n_row = len(table_grid_and_structure.table_string_grid)
    max_column_header_row_id, project_row_headers_rows = (
        _get_max_col_header_row_and_project_header_rows(
            table_grid_and_structure.table_structure_annotations, n_row
        )
    )
    if max_column_header_row_id is None or len(project_row_headers_rows) == 0:
        return [table_grid_and_structure.table_string_grid], [
            table_grid_and_structure.table_structure_annotations
        ]
    else:
        subtables_row_id_list = _split_row_ids(
            max_column_header_row_id, n_row, project_row_headers_rows
        )
        subtable_string_grids_list, subtable_structure_annotations_list = (
            _split_table_grids_and_annotations(
                max_column_header_row_id,
                subtables_row_id_list,
                table_grid_and_structure,
            )
        )

        # Extract column header grids and annotations
        column_header_grid = table_grid_and_structure.table_string_grid[
            : max_column_header_row_id + 1
        ]
        column_header_annotations = []
        for annotation in table_grid_and_structure.table_structure_annotations:
            if annotation.data.index[0] <= max_column_header_row_id:
                column_header_annotations.append(annotation)

        return [
            column_header_grid + subtable_string_grid
            for subtable_string_grid in subtable_string_grids_list
        ], [
            column_header_annotations + subtable_structure_annotations
            for subtable_structure_annotations in subtable_structure_annotations_list
        ]


def extract_pd_dfs_from_output(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
    use_first_row_as_header: bool = True,
    include_figure_extracted_table: bool = False,
    split_long_tables: bool = False,
) -> list[pd.DataFrame]:
    """Extract output's tables and convert them to a list of pandas DataFrames.

    Args:
        serialized_document: a serialized document
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area, other cells are
            empty.
        use_first_row_as_header: if True, use the first row of the extracted table as the columns.
            Set to False if you know there is no header row in your tables.
        split_long_tables: if True, split long tables based on the projected row headers.

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
    for table_grid_and_structure in table_id_to_grid_and_structure.values():
        if table_grid_and_structure.table_category_type in (
            ContentCategory.TABLE.value,
            ContentCategory.TABLE_OF_CONTENTS.value,
        ) or (
            include_figure_extracted_table
            and table_grid_and_structure.table_category_type
            == ContentCategory.FIGURE_EXTRACTED_TABLE.value
        ):
            if split_long_tables:
                subtable_string_grid_list, _ = _split_long_tables(
                    table_grid_and_structure
                )
                for subtable_string_grid in subtable_string_grid_list:
                    table_dfs.append(
                        convert_table_to_pd_df(
                            subtable_string_grid,
                            use_first_row_as_header=use_first_row_as_header,
                        )
                    )
            else:
                table_dfs.append(
                    convert_table_to_pd_df(
                        table_grid_and_structure.table_string_grid,
                        use_first_row_as_header=use_first_row_as_header,
                    )
                )
    return table_dfs


def extract_pd_dfs_with_locs_and_table_structure_from_output(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
    use_first_row_as_header: bool = True,
    include_figure_extracted_table: bool = False,
    split_long_tables: bool = False,
) -> list[Table]:
    """Extract tables and convert them to a list of pd DataFrames, table locations and structures.

    Args:
        serialized_document: a serialized document
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area, other cells are
            empty.
        use_first_row_as_header: if True, use the first row of the extracted table as the columns.
            Set to False if you know there is no header row in your tables.
        split_long_tables: if True, split long tables based on the projected row headers.

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
        )],
        table_type='TABLE',
        project_row_headers=[],
        table_uid='3',
        subtable_id=None),
        ]
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
            table_category_type = table_grid_and_structure.table_category_type
            if split_long_tables:
                subtable_string_grid_list, subtable_structure_annotation_list = (
                    _split_long_tables(table_grid_and_structure)
                )
                for subtable_id, (
                    subtable_string_grid,
                    subtable_structure_annotation,
                ) in enumerate(
                    zip(subtable_string_grid_list, subtable_structure_annotation_list)
                ):
                    subtable_df = convert_table_to_pd_df(
                        subtable_string_grid,
                        use_first_row_as_header=use_first_row_as_header,
                    )
                    subtable_cells, project_row_headers = (
                        _convert_table_annotations_to_cells(
                            subtable_structure_annotation,
                            subtable_string_grid,
                        )
                    )
                    tables.append(
                        Table(
                            df=subtable_df,
                            table_type=table_category_type,
                            locations=table_uid_to_locs_mapping[table_uid],
                            cells=subtable_cells,
                            project_row_headers=project_row_headers,
                            table_uid=table_uid,
                            subtable_id=subtable_id,
                        )
                    )
            else:
                table_df = convert_table_to_pd_df(
                    table_grid_and_structure.table_string_grid,
                    use_first_row_as_header=use_first_row_as_header,
                )
                table_cells, project_row_headers = _convert_table_annotations_to_cells(
                    table_grid_and_structure.table_structure_annotations,
                    table_grid_and_structure.table_string_grid,
                )
                tables.append(
                    Table(
                        df=table_df,
                        table_type=table_category_type,
                        locations=table_uid_to_locs_mapping[table_uid],
                        cells=table_cells,
                        project_row_headers=project_row_headers,
                        table_uid=table_uid,
                    )
                )
    return tables
