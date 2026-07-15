# Copyright 2024-present Kensho Technologies, LLC.
"""Functions to extract the tables in the output and turn them into pandas DataFrames."""

import typing
from collections import defaultdict
from typing import Any, NamedTuple, Sequence

import pandas as pd

from .constants import (
    EMPTY_STRING,
    ROW_KEY_PARENT_RELATION,
    TABLE_CONTENT_CATEGORIES,
    AnnotationType,
    ContentCategory,
    TableType,
)
from .extract_output_models import (
    Cell,
    ContentModel,
    ExtractOutputModel,
    LocationModel,
    LocationType,
    RelationAnnotationModel,
    Table,
    TableCategoryType,
    TableCellHierarchyTreeModel,
    TableDataFrameHierarchyModel,
    TableGridAndStructure,
    TableGridHierarchyModel,
    TableStructureAnnotationModel,
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
    table_cell_annotations: list[TableStructureAnnotationModel],
) -> dict[str, list[TableStructureAnnotationModel]]:
    """Get table uid to table structure annotations mapping."""
    uid_to_annotation: dict[str, TableStructureAnnotationModel] = {
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
    table_annotations: list[TableStructureAnnotationModel],
) -> list[Cell]:
    """Convert list of table annotations to list of cells.

    Args:
        table_annotations: a list of table structure annotations.

    Example Input:
        table_annotations = [TableStructureAnnotationModel(content_uids=['2'],data=AnnotationDataModel(index=(0, 0),
        span=(1, 1), value=None, is_column_header=True, is_projected_row_header=False),type='table_structure',
        locations=[LocationModel(height=0.015,width=0.17, x=0.22, y=0.09, page_number=0)] ,
         TableStructureAnnotationModel(content_uids=['3'],data=AnnotationDataModel(index=(0, 1), span=(1, 1),
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
    annotations: Sequence[TableStructureAnnotationModel],
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
    annotations: Sequence[TableStructureAnnotationModel],
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


# --------- Table Hierarchy Tree ---------


def _build_table_cell_hierarchy_tree_node(
    cell_uid: str,
    cell_uid_to_annotation: dict[str, TableStructureAnnotationModel],
    parent_to_children: dict[str, list[str]],
    all_projected_row_header_uids: set[str],
    row_index_to_annotations: dict[int, list[TableStructureAnnotationModel]],
) -> TableCellHierarchyTreeModel:
    """Recursively build a hierarchy tree node for a projected row header cell.

    Args:
        cell_uid: the uid of the projected row header cell to build a node for.
        cell_uid_to_annotation: mapping from cell uid to its table structure annotation.
        parent_to_children: mapping from parent uid to its children uids
            (from row_key_parent relations).
        all_projected_row_header_uids: set of all projected row header uids across all tables.
        row_index_to_annotations: mapping from row index to all cell annotations in that row.

    Returns:
        a TableCellHierarchyTreeModel node for the given cell uid.
    """
    children_uids = parent_to_children.get(cell_uid, [])

    # Separate children into projected row headers (tree children) and
    # data row cells (contents)
    child_nodes: list[TableCellHierarchyTreeModel] = []
    content_annotations: list[TableStructureAnnotationModel] = []
    for child_uid in children_uids:
        # If the child is a projected header, make a new child node
        if child_uid in all_projected_row_header_uids:
            child_nodes.append(
                _build_table_cell_hierarchy_tree_node(
                    child_uid,
                    cell_uid_to_annotation,
                    parent_to_children,
                    all_projected_row_header_uids,
                    row_index_to_annotations,
                )
            )
        else:
            # If the child is a regular row header, assign all annotations in the row
            # to the contents
            child_annotation = cell_uid_to_annotation.get(child_uid)
            if child_annotation:
                row_index = child_annotation.data.index[0]
                content_annotations.extend(row_index_to_annotations.get(row_index, []))

    return TableCellHierarchyTreeModel(
        node_uid=cell_uid,
        node_type=ContentCategory.TABLE_CELL.value,
        children=child_nodes,
        contents=content_annotations,
    )


def _get_table_uid_to_table_cell_hierarchy_tree(
    table_uid_to_cells_mapping: dict[str, list[ContentModel]],
    table_cell_annotations: list[TableStructureAnnotationModel],
    relation_annotations: list[RelationAnnotationModel],
) -> dict[str, TableCellHierarchyTreeModel]:
    """Build a TableCellHierarchyTreeModel for each table uid.

    The root node represents the table itself. Its children are the top-level projected row
    header cells. Each projected row header node's children are its sub-level projected row
    headers (from row_key_parent relations), and its contents are the cell annotations for the
    leftmost cells (regular row headers) that belong to that projected row header and the cell
    annotations in the same row.

    Args:
        table_uid_to_cells_mapping: mapping of table uid to cells (ContentModel) in that table.
        table_cell_annotations: list of table structure annotations.
        relation_annotations: list of relation annotations (row_key_parent relations define
            the hierarchy).

    Returns:
        a mapping of table uid to the TableCellHierarchyTreeModel representing the table hierarchy.
    """
    # Build mapping from cell uid to its table uid
    cell_uid_to_table_uid: dict[str, str] = {}
    for table_uid, cells in table_uid_to_cells_mapping.items():
        for cell in cells:
            cell_uid_to_table_uid[cell.uid] = table_uid

    # Build mapping from cell uid to its annotation
    cell_uid_to_annotation: dict[str, TableStructureAnnotationModel] = {}
    for annotation in table_cell_annotations:
        for uid in annotation.content_uids:
            cell_uid_to_annotation[uid] = annotation

    # Extract row_key_parent relations and group by table uid
    # In row_key_parent: source is parent, target is child
    parent_to_children: dict[str, list[str]] = defaultdict(list)
    child_uids: set[str] = set()
    for relation in relation_annotations:
        if relation.data.relation_type == ROW_KEY_PARENT_RELATION:
            parent_uid = relation.data.source_content_uid
            child_uid = relation.data.target_content_uid
            parent_to_children[parent_uid].append(child_uid)
            child_uids.add(child_uid)

    # Identify projected row header uids per table
    table_uid_to_projected_row_header_uids: dict[str, list[str]] = defaultdict(list)
    for table_uid, cells in table_uid_to_cells_mapping.items():
        for cell in cells:
            cell_ann = cell_uid_to_annotation.get(cell.uid)
            if cell_ann and cell_ann.data.is_projected_row_header:
                table_uid_to_projected_row_header_uids[table_uid].append(cell.uid)

    # Set of all projected row header uids for quick lookup
    all_projected_row_header_uids: set[str] = set()
    for uids in table_uid_to_projected_row_header_uids.values():
        all_projected_row_header_uids.update(uids)

    # Build the tree for each table
    result: dict[str, TableCellHierarchyTreeModel] = {}
    for table_uid in table_uid_to_cells_mapping:
        # Build row_index_to_annotations for this table
        row_index_to_annotations: dict[int, list[TableStructureAnnotationModel]] = (
            defaultdict(list)
        )
        for cell in table_uid_to_cells_mapping[table_uid]:
            cell_ann = cell_uid_to_annotation.get(cell.uid)
            if cell_ann:
                row_index_to_annotations[cell_ann.data.index[0]].append(cell_ann)

        projected_uids = table_uid_to_projected_row_header_uids.get(table_uid, [])
        # Top-level projected row headers are those that are not children of any other
        top_level_uids = [uid for uid in projected_uids if uid not in child_uids]

        # Build child nodes for top-level projected row headers
        top_level_nodes = [
            _build_table_cell_hierarchy_tree_node(
                uid,
                cell_uid_to_annotation,
                parent_to_children,
                all_projected_row_header_uids,
                row_index_to_annotations,
            )
            for uid in top_level_uids
        ]

        # Collect row indices already represented in the hierarchy tree
        # (either as children of a projected row header, or as projected row headers
        # themselves). These rows will be excluded from the table root's contents,
        # since they already appear as nodes or contents within the tree.
        excluded_row_indices: set[int] = set()
        for child_uid in child_uids:
            child_ann = cell_uid_to_annotation.get(child_uid)
            if child_ann and cell_uid_to_table_uid.get(child_uid) == table_uid:
                excluded_row_indices.add(child_ann.data.index[0])
        for uid in projected_uids:
            proj_ann = cell_uid_to_annotation.get(uid)
            if proj_ann:
                excluded_row_indices.add(proj_ann.data.index[0])

        # Remaining rows (not excluded, not column headers) belong to the table
        table_contents: list[TableStructureAnnotationModel] = []
        for row_index, annotations in row_index_to_annotations.items():
            if row_index in excluded_row_indices:
                continue
            # Skip rows that contain column headers
            if any(ann.data.is_column_header for ann in annotations):
                continue
            table_contents.extend(annotations)

        # The root node represents the table itself
        result[table_uid] = TableCellHierarchyTreeModel(
            node_uid=table_uid,
            node_type=ContentCategory.TABLE.value,
            children=top_level_nodes,
            contents=table_contents,
        )

    return result


class CellEntry(NamedTuple):
    """A single cell entry with its column index and text content."""

    col_index: int
    text: str


def _expand_annotations_to_row_groups(
    annotations: Sequence[TableStructureAnnotationModel],
    uid_to_text: dict[str, str],
    duplicate_merged_cells_content_flag: bool = True,
) -> dict[int, list[CellEntry]]:
    """Expand table structure annotations into row-grouped CellEntry pairs.

    For each annotation, resolves its text from uid_to_text and expands its row/col spans
    into individual cell entries grouped by row index.

    Args:
        annotations: the table structure annotations to expand.
        uid_to_text: mapping from content uid to text content.
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area.

    Returns:
        a dict mapping row index to a list of CellEntry named tuples.
    """
    row_groups: dict[int, list[CellEntry]] = defaultdict(list)
    for annotation in annotations:
        row_index = annotation.data.index[0]
        col_index = annotation.data.index[1]
        row_span, col_span = annotation.data.span
        if annotation.content_uids:
            cell_text = uid_to_text.get(annotation.content_uids[0], EMPTY_STRING)
        else:
            cell_text = EMPTY_STRING
        for r_offset in range(row_span):
            for c_offset in range(col_span):
                if duplicate_merged_cells_content_flag or (
                    r_offset == 0 and c_offset == 0
                ):
                    row_groups[row_index + r_offset].append(
                        CellEntry(col_index + c_offset, cell_text)
                    )
                else:
                    row_groups[row_index + r_offset].append(
                        CellEntry(col_index + c_offset, EMPTY_STRING)
                    )
    return row_groups


def _convert_table_cell_hierarchy_tree_to_table_grid_hierarchy_tree(
    cell_hierarchy_tree: TableCellHierarchyTreeModel,
    cell_contents: Sequence[ContentModel],
    column_header_grid: list[list[str]] | None = None,
    duplicate_merged_cells_content_flag: bool = True,
) -> TableGridHierarchyModel:
    """Convert a TableCellHierarchyTreeModel to a TableGridHierarchyModel.

    Resolves the node_uid to its cell's text content and populates the node_text field,
    and converts the annotation-based contents into a 2D string grid. If column_header_grid
    is provided, it is prepended to each node's contents grid.

    Args:
        cell_hierarchy_tree: the hierarchy tree with annotation-based contents.
        cell_contents: the list of ContentModel cells for looking up text by uid.
        column_header_grid: optional column header rows to prepend to each node's contents.
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area.

    Returns:
        a TableGridHierarchyModel with human-readable text and string grid contents.
    """
    uid_to_text = {cell.uid: cell.content or EMPTY_STRING for cell in cell_contents}

    # Recover node text from the content tree
    node_text = uid_to_text.get(cell_hierarchy_tree.node_uid)

    # Convert annotation contents to a 2D string grid grouped by row, expanding spans
    row_groups = _expand_annotations_to_row_groups(
        cell_hierarchy_tree.contents, uid_to_text, duplicate_merged_cells_content_flag
    )

    # Build sorted 2D grid
    contents_grid: list[list[str]] = []
    for row_index in sorted(row_groups.keys()):
        row = row_groups[row_index]
        row.sort(key=lambda entry: entry.col_index)
        contents_grid.append([entry.text for entry in row])

    # Prepend column header rows to contents if available
    if column_header_grid and contents_grid:
        contents_grid = column_header_grid + contents_grid

    # Recursively convert children
    children = [
        _convert_table_cell_hierarchy_tree_to_table_grid_hierarchy_tree(
            child,
            cell_contents,
            column_header_grid,
            duplicate_merged_cells_content_flag,
        )
        for child in cell_hierarchy_tree.children
    ]

    return TableGridHierarchyModel(
        node_uid=cell_hierarchy_tree.node_uid,
        node_text=node_text,
        node_type=cell_hierarchy_tree.node_type,
        children=children,
        contents=contents_grid,
    )


def _get_column_header_grid(
    cells: list[ContentModel],
    table_cell_annotations: list[TableStructureAnnotationModel],
    duplicate_merged_cells_content_flag: bool = True,
) -> list[list[str]]:
    """Extract consecutive column header rows starting from row 0 as a string grid.

    Args:
        cells: the list of ContentModel cells for this table.
        table_cell_annotations: list of table structure annotations.
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area.

    Returns:
        a 2D string grid of consecutive column header rows starting from row 0.
        Returns an empty list if there are no column headers starting at row 0.
    """
    uid_to_text = {cell.uid: cell.content or EMPTY_STRING for cell in cells}

    # Filter to only column header annotations for this table
    header_annotations = [
        ann
        for ann in table_cell_annotations
        if ann.content_uids
        and ann.content_uids[0] in uid_to_text
        and ann.data.is_column_header
    ]

    # Group by row index, expanding spans
    header_row_groups = _expand_annotations_to_row_groups(
        header_annotations, uid_to_text, duplicate_merged_cells_content_flag
    )

    # Build consecutive column header grid starting from row 0
    column_header_grid: list[list[str]] = []
    row_idx = 0
    while row_idx in header_row_groups:
        row = header_row_groups[row_idx]
        row.sort(key=lambda entry: entry.col_index)
        column_header_grid.append([entry.text for entry in row])
        row_idx += 1
    return column_header_grid


def _get_table_uid_to_table_grid_hierarchy_tree(
    parsed_serialized_document: ExtractOutputModel,
    duplicate_merged_cells_content_flag: bool = True,
) -> dict[str, TableGridHierarchyModel]:
    """Build a TableGridHierarchyModel for each table uid.

    Integrates building the annotation hierarchy tree and converting it to a
    human-readable grid hierarchy tree with text content and string grids.

    Args:
        parsed_serialized_document: the parsed Extract output model.
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area.

    Returns:
        a mapping of table uid to the TableGridHierarchyModel representing the hierarchy.
    """
    annotations = parsed_serialized_document.annotations
    table_uid_to_cells_mapping = get_table_uid_to_cells_mapping(
        parsed_serialized_document.content_tree
    )
    table_cell_annotations: list[TableStructureAnnotationModel] = [
        annotation
        for annotation in annotations
        if isinstance(annotation, TableStructureAnnotationModel)
        and annotation.type
        in (
            AnnotationType.TABLE_STRUCTURE.value,
            AnnotationType.FIGURE_EXTRACTED_TABLE_STRUCTURE.value,
        )
    ]
    relation_annotations: list[RelationAnnotationModel] = [
        annotation
        for annotation in annotations
        if isinstance(annotation, RelationAnnotationModel)
        and annotation.data.relation_type == ROW_KEY_PARENT_RELATION
    ]

    # Generate table cell hierarchy trees from annotations and relations
    table_uid_to_cell_hierarchy_tree = _get_table_uid_to_table_cell_hierarchy_tree(
        table_uid_to_cells_mapping,
        table_cell_annotations,
        relation_annotations,
    )

    # Extract column header grid for each table
    table_uid_to_column_header_grid: dict[str, list[list[str]]] = {}
    for table_uid, cells in table_uid_to_cells_mapping.items():
        table_uid_to_column_header_grid[table_uid] = _get_column_header_grid(
            cells, table_cell_annotations, duplicate_merged_cells_content_flag
        )

    # Convert table cell hierarchy trees to table grid hierarchy trees
    table_uid_to_grid_hierarchy_tree: dict[str, TableGridHierarchyModel] = {}
    for table_uid, cell_hierarchy_tree in table_uid_to_cell_hierarchy_tree.items():
        column_header_grid = table_uid_to_column_header_grid.get(table_uid) or None
        table_uid_to_grid_hierarchy_tree[table_uid] = (
            _convert_table_cell_hierarchy_tree_to_table_grid_hierarchy_tree(
                cell_hierarchy_tree,
                table_uid_to_cells_mapping[table_uid],
                column_header_grid,
                duplicate_merged_cells_content_flag,
            )
        )

    return table_uid_to_grid_hierarchy_tree


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
            [TableStructureAnnotationModel(content_uids=['2'],data=AnnotationDataModel(index=(0, 0), span=(1, 1),
            value=None, is_column_header=True, is_projected_row_header=False),type='table_structure',
            locations=[LocationModel(height=0.015,width=0.17, x=0.22, y=0.09, page_number=0)]), ...]),
            '2': TableGridAndStructure(table_category_type = "FIGURE_EXTRACTED_TABLE",table_string_grid =
             [['another_header1'], ['another_row1_val']], tables_structure_annotations =
             [TableStructureAnnotationModel(content_uids=['26'],data=AnnotationDataModel(index=(4, 4), span=(1, 1),
            value=None, is_column_header=False,is_projected_row_header=False), type='table_structure',
            locations=[LocationModel(height=0.015, width=0.04, x=0.72, y=0.19, page_number=0), ...])
        }
    """  # noqa: E501
    parsed_serialized_document = load_output_to_pydantic(serialized_document)
    annotations = parsed_serialized_document.annotations
    content = parsed_serialized_document.content_tree

    table_uid_to_cells_mapping = get_table_uid_to_cells_mapping(content)
    table_uid_to_type_mapping = _get_table_uid_to_types_mapping(content)

    table_cell_annotations: list[TableStructureAnnotationModel] = [
        annotation
        for annotation in annotations
        if isinstance(annotation, TableStructureAnnotationModel)
        and annotation.type
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


def _convert_table_grid_hierarchy_tree_to_table_df_hierarchy_tree(
    grid_hierarchy_tree: TableGridHierarchyModel,
) -> TableDataFrameHierarchyModel:
    """Convert a TableGridHierarchyModel to a TableDataFrameHierarchyModel.

    Converts the 2D string grid contents into a pandas DataFrame.

    Args:
        grid_hierarchy_tree: the hierarchy tree with string grid contents.

    Returns:
        a TableDataFrameHierarchyModel with DataFrame contents.
    """
    contents_df = convert_table_to_pd_df(
        grid_hierarchy_tree.contents,
        use_first_row_as_header=False,
    )

    children = [
        _convert_table_grid_hierarchy_tree_to_table_df_hierarchy_tree(child)
        for child in grid_hierarchy_tree.children
    ]

    return TableDataFrameHierarchyModel(
        node_uid=grid_hierarchy_tree.node_uid,
        node_text=grid_hierarchy_tree.node_text,
        node_type=grid_hierarchy_tree.node_type,
        children=children,
        contents=contents_df,
    )


def extract_pd_dfs_with_locs_and_table_structure_from_output(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
    use_first_row_as_header: bool = True,
    include_figure_extracted_table: bool = False,
    include_table_hierarchy_tree: bool = False,
) -> list[Table]:
    """Extract tables and convert them to a list of pd DataFrames, table locations and structures.

    Args:
        serialized_document: a serialized document
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells.
            If False, only fill the first cell (top left) of the merged area, other cells are
            empty.
        use_first_row_as_header: if True, use the first row of the extracted table as the columns.
            Set to False if you know there is no header row in your tables.
        include_figure_extracted_table: if True, include tables extracted from figures.
        include_table_hierarchy_tree: if True, also extract the table annotation hierarchy tree
            for each table showing the projected row header structure.

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

    # Build hierarchy trees if requested
    table_uid_to_table_grid_hierarchy_tree: dict[str, TableGridHierarchyModel] = {}
    if include_table_hierarchy_tree:
        table_uid_to_table_grid_hierarchy_tree = (
            _get_table_uid_to_table_grid_hierarchy_tree(
                parsed_serialized_document,
                duplicate_merged_cells_content_flag,
            )
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
            hierarchy_tree: TableDataFrameHierarchyModel | None = None
            grid_hierarchy_tree = table_uid_to_table_grid_hierarchy_tree.get(table_uid)
            if grid_hierarchy_tree is not None:
                hierarchy_tree = (
                    _convert_table_grid_hierarchy_tree_to_table_df_hierarchy_tree(
                        grid_hierarchy_tree,
                    )
                )
            tables.append(
                Table(
                    df=table_df,
                    table_type=table_grid_and_structure.table_category_type,
                    locations=table_uid_to_locs_mapping[table_uid],
                    cells=table_cells,
                    hierarchy_tree=hierarchy_tree,
                )
            )
    return tables
