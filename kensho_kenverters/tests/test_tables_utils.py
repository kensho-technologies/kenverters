import json
import os
from typing import ClassVar
from unittest import TestCase

import pandas as pd

from ..constants import ContentCategory
from ..extract_output_models import (
    AnnotationDataModel,
    AnnotationModel,
    ExtractOutputModel,
    LocationModel,
    TableGridAndStructure,
)
from ..tables_utils import (
    _adjust_row_indexes_of_structure_annotations,
    _extract_string_grids_by_row_ids,
    _extract_structure_annotations_by_row_ids,
    _split_row_ids_after_column_headers,
    convert_table_to_pd_df,
    duplicate_spanning_annotations,
    extract_project_row_headers,
    get_column_headers_and_project_row_headers_row_ids,
    get_table_shape,
    split_table_into_subtables,
    table_can_be_split,
)

OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "extract_output.json"
)


class TestTablesUtils(TestCase):
    parsed_serialized_document: ClassVar[ExtractOutputModel]

    @classmethod
    def setUpClass(cls) -> None:
        with open(OUTPUT_FILE_PATH, "r") as f:
            extract_output = json.load(f)
        cls.parsed_serialized_document = ExtractOutputModel(**extract_output)

    def test_get_table_shape(self) -> None:
        expected_shape = (5, 5)
        self.assertEqual(
            get_table_shape(self.parsed_serialized_document.annotations), expected_shape
        )

    def test_convert_tpdle_to_pd_df(self) -> None:
        # 1-row table: no headers
        expected_df = pd.DataFrame([["this", "that"]])
        converted_df = convert_table_to_pd_df([["this", "that"]])
        self.assertEqual(expected_df.to_csv(), converted_df.to_csv())

        # 2-row table: first row is a header
        expected_df = pd.DataFrame([["this", "that"]], columns=["header1", "header2"])
        converted_df = convert_table_to_pd_df(
            [["header1", "header2"], ["this", "that"]]
        )
        self.assertEqual(expected_df.to_csv(), converted_df.to_csv())

        # 2-row table: first row is not a header
        expected_df = pd.DataFrame([["header1", "header2"], ["this", "that"]])
        converted_df = convert_table_to_pd_df(
            [["header1", "header2"], ["this", "that"]], use_first_row_as_header=False
        )
        self.assertEqual(expected_df.to_csv(), converted_df.to_csv())

    def test_duplicate_spanning_annotations_1_spans(self) -> None:
        # Test no duplication when all spans are 1
        duplicated = duplicate_spanning_annotations(
            self.parsed_serialized_document.annotations
        )
        expected_duplicated = [
            AnnotationModel(
                content_uids=["7"],
                data=AnnotationDataModel(index=(0, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.22128,
                        x=0.16008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["8"],
                data=AnnotationDataModel(index=(0, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.02241,
                        x=0.46007,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["9"],
                data=AnnotationDataModel(index=(0, 2), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.02241,
                        x=0.56008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["10"],
                data=AnnotationDataModel(index=(0, 3), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.02241,
                        x=0.66008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["11"],
                data=AnnotationDataModel(index=(0, 4), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.02241,
                        x=0.76008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["12"],
                data=AnnotationDataModel(index=(1, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.03736,
                        x=0.16008,
                        y=0.42464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["13"],
                data=AnnotationDataModel(index=(1, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.46007,
                        y=0.42464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["14"],
                data=AnnotationDataModel(index=(1, 2), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.56008,
                        y=0.42464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["15"],
                data=AnnotationDataModel(index=(1, 3), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.66008,
                        y=0.42464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["16"],
                data=AnnotationDataModel(index=(1, 4), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.76008,
                        y=0.42464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["17"],
                data=AnnotationDataModel(index=(2, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.03736,
                        x=0.16008,
                        y=0.44464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["18"],
                data=AnnotationDataModel(index=(2, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.46007,
                        y=0.44464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["19"],
                data=AnnotationDataModel(index=(2, 2), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.56008,
                        y=0.44464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["20"],
                data=AnnotationDataModel(index=(2, 3), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.66008,
                        y=0.44464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["21"],
                data=AnnotationDataModel(index=(2, 4), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.76008,
                        y=0.44464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["22"],
                data=AnnotationDataModel(index=(3, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.03736,
                        x=0.16008,
                        y=0.46465,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["23"],
                data=AnnotationDataModel(index=(3, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.46007,
                        y=0.46465,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["24"],
                data=AnnotationDataModel(index=(3, 2), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.56008,
                        y=0.46465,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["25"],
                data=AnnotationDataModel(index=(3, 3), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.66008,
                        y=0.46465,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["26"],
                data=AnnotationDataModel(index=(3, 4), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.76008,
                        y=0.46465,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["27"],
                data=AnnotationDataModel(index=(4, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.03736,
                        x=0.16008,
                        y=0.48464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["28"],
                data=AnnotationDataModel(index=(4, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.46007,
                        y=0.48464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["29"],
                data=AnnotationDataModel(index=(4, 2), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.56008,
                        y=0.48464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["30"],
                data=AnnotationDataModel(index=(4, 3), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.66008,
                        y=0.48464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["31"],
                data=AnnotationDataModel(index=(4, 4), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.76008,
                        y=0.48464,
                        page_number=0,
                    )
                ],
            ),
        ]

        self.assertEqual(duplicated, expected_duplicated)

    def test_duplicate_spanning_annotations_greater_1_spans(self) -> None:
        # Test properly duplicated when cells have a span > 1
        annotations = self.parsed_serialized_document.annotations
        annotations.pop(-1)
        annotations[-1].data.span = (1, 2)
        expected_duplicated = [
            AnnotationModel(
                content_uids=["7"],
                data=AnnotationDataModel(index=(0, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.22128,
                        x=0.16008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["8"],
                data=AnnotationDataModel(index=(0, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.02241,
                        x=0.46007,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["9"],
                data=AnnotationDataModel(index=(0, 2), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.02241,
                        x=0.56008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["10"],
                data=AnnotationDataModel(index=(0, 3), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.02241,
                        x=0.66008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["11"],
                data=AnnotationDataModel(index=(0, 4), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.02241,
                        x=0.76008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["12"],
                data=AnnotationDataModel(index=(1, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.03736,
                        x=0.16008,
                        y=0.42464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["13"],
                data=AnnotationDataModel(index=(1, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.46007,
                        y=0.42464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["14"],
                data=AnnotationDataModel(index=(1, 2), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.56008,
                        y=0.42464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["15"],
                data=AnnotationDataModel(index=(1, 3), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.66008,
                        y=0.42464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["16"],
                data=AnnotationDataModel(index=(1, 4), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.76008,
                        y=0.42464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["17"],
                data=AnnotationDataModel(index=(2, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.03736,
                        x=0.16008,
                        y=0.44464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["18"],
                data=AnnotationDataModel(index=(2, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.46007,
                        y=0.44464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["19"],
                data=AnnotationDataModel(index=(2, 2), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.56008,
                        y=0.44464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["20"],
                data=AnnotationDataModel(index=(2, 3), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.66008,
                        y=0.44464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["21"],
                data=AnnotationDataModel(index=(2, 4), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.76008,
                        y=0.44464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["22"],
                data=AnnotationDataModel(index=(3, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.03736,
                        x=0.16008,
                        y=0.46465,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["23"],
                data=AnnotationDataModel(index=(3, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.46007,
                        y=0.46465,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["24"],
                data=AnnotationDataModel(index=(3, 2), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.56008,
                        y=0.46465,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["25"],
                data=AnnotationDataModel(index=(3, 3), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.66008,
                        y=0.46465,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["26"],
                data=AnnotationDataModel(index=(3, 4), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.76008,
                        y=0.46465,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["27"],
                data=AnnotationDataModel(index=(4, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.03736,
                        x=0.16008,
                        y=0.48464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["28"],
                data=AnnotationDataModel(index=(4, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.46007,
                        y=0.48464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["29"],
                data=AnnotationDataModel(index=(4, 2), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.56008,
                        y=0.48464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["30"],
                data=AnnotationDataModel(index=(4, 3), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.66008,
                        y=0.48464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["30"],
                data=AnnotationDataModel(index=(4, 4), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.66008,
                        y=0.48464,
                        page_number=0,
                    )
                ],
            ),
        ]
        duplicated = duplicate_spanning_annotations(annotations)
        self.assertEqual(expected_duplicated, duplicated)

    def test_duplicate_spanning_annotations_missing_cells(self) -> None:
        # Test missing cells
        annotations = [
            AnnotationModel(
                content_uids=["7"],
                data=AnnotationDataModel(index=(0, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.22128,
                        x=0.16008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["8"],
                data=AnnotationDataModel(index=(0, 1), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.22128,
                        x=0.16008,
                        y=0.80464,
                        page_number=0,
                    )
                ],
            ),
            AnnotationModel(
                content_uids=["9"],
                data=AnnotationDataModel(index=(3, 0), span=(1, 1)),
                type="table_structure",
                locations=[
                    LocationModel(
                        height=0.01188,
                        width=0.22128,
                        x=0.7008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
            ),
        ]

        duplicated = duplicate_spanning_annotations(annotations)
        self.assertEqual(len(duplicated), 8)


class TestSplitLongTables(TestCase):
    """Test cases for table splitting functions."""

    def setUp(self) -> None:
        self.table_string_grid = [
            ["Category", "Q1 2022", "Q2 2022", "Q3 2022", "Q4 2022"],
            ["Revenue", "Revenue", "Revenue", "Revenue", "Revenue"],
            ["", "101", "111", "121", "131"],
            ["", "102", "112", "122", "132"],
            ["Expenses", "Expenses", "Expenses", "Expenses", "Expenses"],
            ["", "201", "211", "221", "231"],
            ["", "202", "212", "222", "232"],
            ["Total", "300", "310", "320", "330"],
        ]

        # Create annotation models for each cell in the table
        self.table_structure_annotations = []
        # Add annotations for each cell
        for row_idx, _ in enumerate(self.table_string_grid):
            # "Revenue" and "Expenses" are projected row headers
            if row_idx in [1, 4]:
                is_column_header = False
                is_projected_row_header = True
                # Create a mock location
                locations = [
                    LocationModel(
                        height=0.01188,
                        width=0.06071,
                        x=0.10 + len(self.table_string_grid[row_idx]) * 0.1,
                        y=0.10 + row_idx * 0.05,
                        page_number=0,
                    )
                ]
                # Create the cell annotation
                annotation = AnnotationModel(
                    content_uids=[],
                    data=AnnotationDataModel(
                        index=(row_idx, 0),
                        span=(1, len(self.table_string_grid[row_idx])),
                        value=None,
                        is_column_header=is_column_header,
                        is_projected_row_header=is_projected_row_header,
                    ),
                    type="table_structure",
                    locations=locations,
                )
                self.table_structure_annotations.append(annotation)
            else:
                for col_idx in range(len(self.table_string_grid[row_idx])):
                    is_column_header = row_idx <= 0  # First row is column header
                    is_projected_row_header = False
                    # Create a mock location
                    locations = [
                        LocationModel(
                            height=0.01188,
                            width=0.06071,
                            x=0.10 + col_idx * 0.1,
                            y=0.10 + row_idx * 0.05,
                            page_number=0,
                        )
                    ]

                    # Create the cell annotation
                    annotation = AnnotationModel(
                        content_uids=[f"cell_{row_idx}_{col_idx}"],
                        data=AnnotationDataModel(
                            index=(row_idx, col_idx),
                            span=(1, 1),
                            value=None,
                            is_column_header=is_column_header,
                            is_projected_row_header=is_projected_row_header,
                        ),
                        type="table_structure",
                        locations=locations,
                    )
                    self.table_structure_annotations.append(annotation)

            # Create the TableGridAndStructure object
            self.table_grid_and_structure = TableGridAndStructure(
                table_category_type=ContentCategory.TABLE.value,
                table_string_grid=self.table_string_grid,
                table_structure_annotations=self.table_structure_annotations,
            )

    def test_get_column_headers_and_project_row_headers_row_ids(self) -> None:
        """Test the get_column_headers_and_project_row_headers_row_ids function."""
        # Call the function with our test fixture
        column_header_row_ids, project_row_header_row_ids = (
            get_column_headers_and_project_row_headers_row_ids(
                self.table_structure_annotations
            )
        )

        # Verify the results
        self.assertEqual(column_header_row_ids, {0})  # We have column headers in rows 0
        self.assertEqual(
            project_row_header_row_ids, {1, 4}
        )  # We have project row headers in rows 1 and 4

        # Test with a table that has no column headers
        annotations_no_headers = []
        for annotation in self.table_structure_annotations:
            # Create a copy of the annotation with is_column_header set to False
            new_data = AnnotationDataModel(
                index=annotation.data.index,
                span=annotation.data.span,
                value=annotation.data.value,
                is_column_header=False,  # Set all to False
                is_projected_row_header=annotation.data.is_projected_row_header,
            )
            new_annotation = AnnotationModel(
                content_uids=annotation.content_uids,
                data=new_data,
                type=annotation.type,
                locations=annotation.locations,
            )
            annotations_no_headers.append(new_annotation)

        # Call the function with no column headers
        column_header_row_ids, project_row_header_row_ids = (
            get_column_headers_and_project_row_headers_row_ids(annotations_no_headers)
        )

        # Verify the results
        self.assertEqual(column_header_row_ids, set())  # No column headers
        self.assertEqual(
            project_row_header_row_ids, {1, 4}
        )  # Project row headers should be the same

        # Test with no project row headers
        annotations_no_project_headers = []
        for annotation in self.table_structure_annotations:
            # Create a copy of the annotation with is_projected_row_header set to False
            new_data = AnnotationDataModel(
                index=annotation.data.index,
                span=annotation.data.span,
                value=annotation.data.value,
                is_column_header=annotation.data.is_column_header,
                is_projected_row_header=False,  # Set all to False
            )
            new_annotation = AnnotationModel(
                content_uids=annotation.content_uids,
                data=new_data,
                type=annotation.type,
                locations=annotation.locations,
            )
            annotations_no_project_headers.append(new_annotation)

        # Call the function with no project row headers
        column_header_row_ids, project_row_header_row_ids = (
            get_column_headers_and_project_row_headers_row_ids(
                annotations_no_project_headers
            )
        )

        # Verify the results
        self.assertEqual(
            column_header_row_ids, {0}
        )  # Column headers should be the same
        self.assertEqual(project_row_header_row_ids, set())  # No project row headers

    def test_table_can_be_split(self) -> None:
        """Test the table_can_be_split function."""
        # The column header row ids is empty.
        column_header_row_ids: set[int] = set()
        project_row_header_row_ids: set[int] = {1, 4}

        table_can_be_split_or_not = table_can_be_split(
            column_header_row_ids, project_row_header_row_ids
        )
        # The table can not be split.
        self.assertEqual(table_can_be_split_or_not, False)

        # The project row header row ids is empty.
        column_header_row_ids = {0}
        project_row_header_row_ids = set()

        table_can_be_split_or_not = table_can_be_split(
            column_header_row_ids, project_row_header_row_ids
        )
        # The table can not be split.
        self.assertEqual(table_can_be_split_or_not, False)

        # The column header row ids are not consecutive starting from the initial.
        column_header_row_ids = {1, 3}
        project_row_header_row_ids = {5, 8}

        table_can_be_split_or_not = table_can_be_split(
            column_header_row_ids, project_row_header_row_ids
        )
        # The table can not be split.
        self.assertEqual(table_can_be_split_or_not, False)

        # The table with column header row ids and project row header row ids is empty.
        # and the column header row ids are consecutive starting from the initial
        column_header_row_ids = {0, 1, 2}
        project_row_header_row_ids = {5, 8}

        table_can_be_split_or_not = table_can_be_split(
            column_header_row_ids, project_row_header_row_ids
        )

        # The table can be split.
        self.assertEqual(table_can_be_split_or_not, True)

    def test_split_row_ids_after_column_headers(self) -> None:
        """Test the table_can_be_split function."""
        # First get the max column header row and project header rows
        column_header_row_ids, project_row_header_row_ids = (
            get_column_headers_and_project_row_headers_row_ids(
                self.table_structure_annotations
            )
        )
        max_col_header_row_id = max(column_header_row_ids)
        # Call the function with our test data
        subtables_row_id_list = _split_row_ids_after_column_headers(
            max_col_header_row_id,
            len(self.table_string_grid),
            project_row_header_row_ids,
        )

        # Expected result:
        # - Row 1-3 should be in the first subtable (Revenue section)
        # - Row 4-7 should be in the second subtable (Expenses and Total section)
        expected_subtables = [[1, 2, 3], [4, 5, 6, 7]]

        self.assertEqual(len(subtables_row_id_list), 2)
        self.assertEqual(subtables_row_id_list, expected_subtables)

    def test_extract_string_grids_by_row_ids(self) -> None:
        """Test the _extract_string_grids_by_row_ids function."""

        # Testing case one
        target_row_ids = [1, 2, 3]
        extract_grid = _extract_string_grids_by_row_ids(
            self.table_string_grid, target_row_ids
        )
        expected_subtables = [
            ["Revenue", "Revenue", "Revenue", "Revenue", "Revenue"],
            ["", "101", "111", "121", "131"],
            ["", "102", "112", "122", "132"],
        ]
        self.assertEqual(extract_grid, expected_subtables)

        # Testing case two
        target_row_ids = [4, 5, 6, 7]
        extract_grid = _extract_string_grids_by_row_ids(
            self.table_string_grid, target_row_ids
        )
        expected_subtables = [
            ["Expenses", "Expenses", "Expenses", "Expenses", "Expenses"],
            ["", "201", "211", "221", "231"],
            ["", "202", "212", "222", "232"],
            ["Total", "300", "310", "320", "330"],
        ]
        self.assertEqual(extract_grid, expected_subtables)

    def test_extract_structure_annotations_by_row_ids(self) -> None:
        """Test the _extract_structure_annotations_by_row_ids function."""

        # Test case 1: Extract annotations from rows 1-3 (Revenue section)
        target_row_ids = [1, 2, 3]
        extracted_annotations = _extract_structure_annotations_by_row_ids(
            self.table_structure_annotations, target_row_ids
        )

        # Check if we extracted the correct number of annotations
        # Should include 1 project row header (row 1) + 2 rows (2-3)
        # with 5 columns each = 11 annotations
        expected_count = 11
        self.assertEqual(len(extracted_annotations), expected_count)

        # Verify that all extracted annotations have row indices in our target range
        for annotation in extracted_annotations:
            self.assertIn(annotation.data.index[0], target_row_ids)

        # Verify that the Revenue project row header is included
        revenue_annotation = next(
            (a for a in extracted_annotations if a.data.is_projected_row_header)
        )
        self.assertIsNotNone(revenue_annotation)
        self.assertEqual(revenue_annotation.data.index[0], 1)

        # Test case 2: Extract annotations from rows 4-7 (Expenses and Total section)
        target_row_ids = [4, 5, 6, 7]
        extracted_annotations = _extract_structure_annotations_by_row_ids(
            self.table_structure_annotations, target_row_ids
        )

        # Check if we extracted the correct number of annotations
        # Should include 1 project row header (row 4) + 3 rows (5-7)
        # with 5 columns each = 16 annotations
        expected_count = 16
        self.assertEqual(len(extracted_annotations), expected_count)

        # Verify that all extracted annotations have row indices in our target range
        for annotation in extracted_annotations:
            self.assertIn(annotation.data.index[0], target_row_ids)

        # Verify that the Expenses project row header is included
        expenses_annotation = next(
            (a for a in extracted_annotations if a.data.is_projected_row_header)
        )
        self.assertIsNotNone(expenses_annotation)
        self.assertEqual(expenses_annotation.data.index[0], 4)

    def test_adjust_row_indexes_of_structure_annotations(self) -> None:
        # Create a simple list of annotations to test with
        test_annotations = [
            AnnotationModel(
                content_uids=["test1"],
                data=AnnotationDataModel(
                    index=(1, 0),
                    span=(1, 1),
                ),
                type="table_structure",
                locations=None,
            ),
            AnnotationModel(
                content_uids=["test2"],
                data=AnnotationDataModel(
                    index=(2, 3),
                    span=(1, 1),
                ),
                type="table_structure",
                locations=None,
            ),
        ]

        # Apply a positive row offset (moving rows down)
        row_offset = 3
        adjusted_annotations = _adjust_row_indexes_of_structure_annotations(
            row_offset, test_annotations
        )

        # Check that the annotations were correctly adjusted
        self.assertEqual(adjusted_annotations[0].data.index, (4, 0))  # 1 + 3 = 4
        self.assertEqual(adjusted_annotations[1].data.index, (5, 3))  # 2 + 3 = 5

        # Check that column indices remain unchanged
        self.assertEqual(adjusted_annotations[0].data.index[1], 0)
        self.assertEqual(adjusted_annotations[1].data.index[1], 3)

        # Test with a negative offset (moving rows up)
        row_offset = -1
        adjusted_annotations = _adjust_row_indexes_of_structure_annotations(
            row_offset, test_annotations
        )

        # Check that the annotations were correctly adjusted
        self.assertEqual(adjusted_annotations[0].data.index, (0, 0))  # 1 - 1 = 0
        self.assertEqual(adjusted_annotations[1].data.index, (1, 3))  # 2 - 1 = 1

    def test_split_table_into_subtables(self) -> None:
        """Test the split_table_into_subtables function."""

        # Get the row ids  column headers and project row headers
        column_header_row_ids, project_row_header_row_ids = (
            get_column_headers_and_project_row_headers_row_ids(
                self.table_structure_annotations
            )
        )

        # Call the function with our test fixture
        subtable_string_grid_list, subtable_structure_annotations_list = (
            split_table_into_subtables(
                self.table_grid_and_structure,
                column_header_row_ids,
                project_row_header_row_ids,
            )
        )

        # Verify we got the expected number of subtables
        self.assertEqual(len(subtable_string_grid_list), 2)
        self.assertEqual(len(subtable_structure_annotations_list), 2)

        # Each subtable should include the header rows (0 and 1) and the relevant data rows

        # Check the content of the first subtable
        # It should have the header rows (0, 1) + rows 2, 3, 4 from the original table
        expected_first_subtable = [
            ["Category", "Q1 2022", "Q2 2022", "Q3 2022", "Q4 2022"],  # Header row 0
            [
                "Revenue",
                "Revenue",
                "Revenue",
                "Revenue",
                "Revenue",
            ],  # Data row with project header
            ["", "101", "111", "121", "131"],  # Regular data row
            ["", "102", "112", "122", "132"],  # Regular data row
        ]
        self.assertEqual(subtable_string_grid_list[0], expected_first_subtable)

        # Check the content of the second subtable
        # It should have the header rows (0, 1) + rows 5, 6, 7, 8 from the original table
        expected_second_subtable = [
            ["Category", "Q1 2022", "Q2 2022", "Q3 2022", "Q4 2022"],  # Header row 0
            [
                "Expenses",
                "Expenses",
                "Expenses",
                "Expenses",
                "Expenses",
            ],  # Data row with project header
            ["", "201", "211", "221", "231"],  # Regular data row
            ["", "202", "212", "222", "232"],  # Regular data row
            ["Total", "300", "310", "320", "330"],  # Data row
        ]
        self.assertEqual(subtable_string_grid_list[1], expected_second_subtable)

        # Check annotations for the first subtable
        first_annotations = subtable_structure_annotations_list[0]

        # There should be 1 header rows × 5 columns + 1 project row header
        # + 2 data rows × 5 columns = 16 annotations
        self.assertEqual(len(first_annotations), 16)

        # Check annotations for the second subtable
        second_annotations = subtable_structure_annotations_list[1]

        # There should be 1 header rows × 5 columns + 1 project row header
        # + 3 data rows × 5 columns = 30 annotations
        self.assertEqual(len(second_annotations), 21)

    def test_extract_project_row_headers(self) -> None:
        """Test the extract_project_row_headers function."""
        # Test with the existing table setup that has project row headers
        project_headers = extract_project_row_headers(
            self.table_structure_annotations, self.table_string_grid
        )

        # We expect to get "Revenue" and "Expenses", which are the values
        # at row indices 1 and 4, column 0
        expected_headers = ["Revenue", "Expenses"]
        self.assertEqual(project_headers, expected_headers)

        # Test with a table that has no project row headers
        # Create a copy with is_projected_row_header set to False for all annotations
        annotations_no_project_headers = []
        for annotation in self.table_structure_annotations:
            new_data = AnnotationDataModel(
                index=annotation.data.index,
                span=annotation.data.span,
                value=annotation.data.value,
                is_column_header=annotation.data.is_column_header,
                is_projected_row_header=False,  # Set all to False
            )
            new_annotation = AnnotationModel(
                content_uids=annotation.content_uids,
                data=new_data,
                type=annotation.type,
                locations=annotation.locations,
            )
            annotations_no_project_headers.append(new_annotation)

        project_headers = extract_project_row_headers(
            annotations_no_project_headers, self.table_string_grid
        )

        # With no project row headers, we expect an empty list
        self.assertEqual(project_headers, [])
