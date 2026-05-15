# Copyright 2024-present Kensho Technologies, LLC.
"""Pydantic models for the output JSON."""

from dataclasses import dataclass
from typing import Annotated, Any, Literal, NamedTuple, TypeAlias, Union

import pandas as pd
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

# Location types are either dictionaries of bbox coordinates and page numbers
# or None if locations are not returned in the Extract output.
LocationType: TypeAlias = dict[str, float | int] | None


class Cell(BaseModel):
    index: tuple[int, int]
    span: tuple[int, int]
    locations: list[LocationType] | None
    is_column_header: bool
    is_projected_row_header: bool


TableCategoryType: TypeAlias = Literal[
    "TABLE",
    "TABLE_OF_CONTENTS",
    "FIGURE_EXTRACTED_TABLE",
]


class Table(NamedTuple):
    """Converted table types consisting of the table as a pandas DataFrame and its location(s)."""

    df: pd.DataFrame
    table_type: TableCategoryType
    locations: list[LocationType] | None = None
    cells: list[Cell] | None = None


class LocationModel(BaseModel):
    """Pydantic object for the location dictionary."""

    height: float
    width: float
    x: float
    y: float
    page_number: int


class AnnotationDataModel(BaseModel):
    """Pydantic object for an annotation table cell's index and span."""

    index: tuple[int, int]
    span: tuple[int, int]
    value: str | None = None
    is_column_header: bool = False
    is_projected_row_header: bool = False


class TableStructureAnnotationModel(BaseModel):
    """Pydantic object for the Extract table structure annotations."""

    content_uids: list[str]
    data: AnnotationDataModel
    type: Literal["table_structure", "figure_extracted_table_structure"]
    locations: list[LocationModel] | None = None


class RelationAnnotationDataModel(BaseModel):
    """Pydantic object for a relation annotation's data."""

    relation_type: str
    source_content_uid: str
    target_content_uid: str


class RelationAnnotationModel(BaseModel):
    """Pydantic object for relation annotations."""

    data: RelationAnnotationDataModel
    type: Literal["relation"]


class TextNodeDataModel(BaseModel):
    """Pydantic object for the structured output character offsets and their text boxes."""

    texts: list[str] | None
    text_locations: list[LocationModel | None] | None
    character_offsets: list[list[float] | None] | None


class ContentModel(BaseModel):
    """Pydantic object for the Extract contents."""

    uid: str
    type: str
    content: str | None
    children: list["ContentModel"]
    locations: list[LocationModel] | None = None
    text_node_data: TextNodeDataModel | None = None


class PDFPageModel(BaseModel):
    """Pydantic object for the PDF page information."""

    height: float
    width: float
    required_ccw_rotation: int


AnnotationModel = Annotated[
    Union[TableStructureAnnotationModel, RelationAnnotationModel],
    Field(discriminator="type"),
]


class ExtractOutputModel(BaseModel):
    """Pydantic object for the Extract contents and annotations."""

    annotations: list[AnnotationModel]
    content_tree: ContentModel
    pdf_pages: list[PDFPageModel] | None = None


@dataclass
class ConvertOutputResult:
    """Result of convert_output_to_items_list_and_relations."""

    item_list: list[dict[str, Any]]
    relations: list[dict[str, str]] | None


class TableGridAndStructure(NamedTuple):
    """Objects consisting of table category type, string grid and structure annotations."""

    table_category_type: TableCategoryType
    table_string_grid: list[list[str]]
    table_structure_annotations: list[TableStructureAnnotationModel]


class ContentSegmentModel(BaseModel):
    """A content segment within a header tree node."""

    category: str
    text: str
    locations: list[LocationModel]
    table: list[list[str]] | None = None


class HeaderTreeNodeModel(BaseModel):
    """A node in the header content tree produced by convert_output_to_header_tree."""

    type: str
    text: str
    children: list["HeaderTreeNodeModel"]
    locations: list[LocationModel]
    contents: list[ContentSegmentModel] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the tree to a plain dictionary."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HeaderTreeNodeModel":
        """Deserialize a plain dictionary into a HeaderTreeNodeModel."""
        return cls.model_validate(data)
