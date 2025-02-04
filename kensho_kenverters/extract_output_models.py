# Copyright 2024-present Kensho Technologies, LLC.
"""Pydantic models for the output JSON."""

from typing import NamedTuple, TypeAlias

import pandas as pd
from pydantic import BaseModel  # pylint: disable=no-name-in-module

# Location types are either dictionaries of bbox coordinates and page numbers
# or None if locations are not returned in the Extract output.
LocationType: TypeAlias = dict[str, float | int] | None


class Table(NamedTuple):
    """Converted table types consisting of the table as a pandas DataFrame and its location(s)."""

    df: pd.DataFrame
    locations: list[LocationType] | None = None


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


class AnnotationModel(BaseModel):
    """Pydantic object for the Extract annotations."""

    content_uids: list[str]
    data: AnnotationDataModel
    type: str
    locations: list[LocationModel] | None = None


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


class ExtractOutputModel(BaseModel):
    """Pydantic object for the Extract contents and annotations."""

    annotations: list[AnnotationModel]
    content_tree: ContentModel
    pdf_pages: list[PDFPageModel] | None = None
