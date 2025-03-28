import json
import os
from typing import ClassVar
from unittest import TestCase

import pandas as pd

from kensho_kenverters.extract_output_models import (
    AnnotationDataModel,
    AnnotationModel,
    ExtractOutputModel,
    LocationModel,
)
from kensho_kenverters.tables_utils import (
    convert_table_to_pd_df,
    duplicate_spanning_annotations,
    get_table_shape,
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
