import json
import os
from collections import defaultdict
from typing import Any, ClassVar
from unittest import TestCase

from ..constants import ContentCategory
from ..extract_output_models import (
    AnnotationDataModel,
    Cell,
    ContentModel,
    LocationModel,
    TableCellHierarchyTreeModel,
    TableGridAndStructure,
    TableGridHierarchyModel,
    TableStructureAnnotationModel,
)
from ..output_to_tables import (
    _build_table_cell_hierarchy_tree_node,
    _convert_table_cell_hierarchy_tree_to_table_grid_hierarchy_tree,
    _expand_annotations_to_row_groups,
    _get_column_header_grid,
    _get_table_uid_to_table_cell_hierarchy_tree,
    _get_table_uid_to_table_grid_hierarchy_tree,
    build_table_grids,
    extract_pd_dfs_from_output,
    extract_pd_dfs_with_locs_and_table_structure_from_output,
    get_table_uid_to_cells_mapping,
)
from ..utils import load_output_to_pydantic

OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "extract_output.json"
)


class TestTableExtraction(TestCase):
    extract_output: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        with open(OUTPUT_FILE_PATH, "r") as f:
            cls.extract_output = json.load(f)

    def test_extract_pd_dfs(self) -> None:
        # Test with locations
        tables = extract_pd_dfs_with_locs_and_table_structure_from_output(
            self.extract_output
        )
        self.assertEqual(len(tables), 1)
        table = tables[0]
        expected_table_csv = (
            ',Kensho Revenue in millions $,Q1,Q2,Q3,Q4\n0,2020,"100,000","200,000","300,000","'
            '400,000"\n1,2021,"101,001","201,001","301,001","401,001"\n2,2022,"102,004","202,00'
            '4","302,004","402,004"\n3,2023,"103,009","203,009","303,009","403,009"\n'
        )
        self.assertEqual(table.df.to_csv(), expected_table_csv)
        expected_table_locations = [
            {
                "height": 0.09188,
                "width": 0.66072,
                "x": 0.16008,
                "y": 0.40464,
                "page_number": 0,
            }
        ]

        self.assertEqual(table.locations, expected_table_locations)

        expected_table_structure = [
            Cell(
                index=(0, 0),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.22128,
                        "x": 0.16008,
                        "y": 0.40464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(0, 1),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.02241,
                        "x": 0.46007,
                        "y": 0.40464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(0, 2),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.02241,
                        "x": 0.56008,
                        "y": 0.40464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(0, 3),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.02241,
                        "x": 0.66008,
                        "y": 0.40464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(0, 4),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.02241,
                        "x": 0.76008,
                        "y": 0.40464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(1, 0),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.03736,
                        "x": 0.16008,
                        "y": 0.42464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(1, 1),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.46007,
                        "y": 0.42464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(1, 2),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.56008,
                        "y": 0.42464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(1, 3),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.66008,
                        "y": 0.42464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(1, 4),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.76008,
                        "y": 0.42464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(2, 0),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.03736,
                        "x": 0.16008,
                        "y": 0.44464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(2, 1),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.46007,
                        "y": 0.44464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(2, 2),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.56008,
                        "y": 0.44464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(2, 3),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.66008,
                        "y": 0.44464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(2, 4),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.76008,
                        "y": 0.44464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(3, 0),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.03736,
                        "x": 0.16008,
                        "y": 0.46465,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(3, 1),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.46007,
                        "y": 0.46465,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(3, 2),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.56008,
                        "y": 0.46465,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(3, 3),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.66008,
                        "y": 0.46465,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(3, 4),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.76008,
                        "y": 0.46465,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(4, 0),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.03736,
                        "x": 0.16008,
                        "y": 0.48464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(4, 1),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.46007,
                        "y": 0.48464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(4, 2),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.56008,
                        "y": 0.48464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(4, 3),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.66008,
                        "y": 0.48464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
            Cell(
                index=(4, 4),
                span=(1, 1),
                locations=[
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.76008,
                        "y": 0.48464,
                        "page_number": 0,
                    }
                ],
                is_column_header=False,
                is_projected_row_header=False,
            ),
        ]
        self.assertEqual(table.cells, expected_table_structure)

        # Test without locations
        tables_no_locs = extract_pd_dfs_from_output(self.extract_output)
        self.assertEqual(len(tables_no_locs), 1)
        table_no_locs = tables_no_locs[0]
        # Assert the tables are equal (logic for the tables is the same in the two fns)
        self.assertEqual(table_no_locs.to_csv(), table.df.to_csv())

    def test_empty_tables(self) -> None:
        # Test that tables with no cells don't crash the code
        output_with_empty_table = {
            "annotations": [],
            "content_tree": {
                "content": None,
                "type": "DOCUMENT",
                "uid": "0",
                "children": [
                    {"content": None, "children": [], "uid": "1", "type": "TABLE"}
                ],
            },
        }
        extract_pd_dfs_from_output(output_with_empty_table)

    def test_build_table_grids_table_structure(self) -> None:
        # Test with a spanning cell: Make sure it's duplicated
        content = {
            "children": [
                {
                    "children": [
                        {
                            "children": [],
                            "content": "kensho is great.",
                            "locations": [
                                {
                                    "height": 0.06898,
                                    "page_number": 0,
                                    "width": 0.75446,
                                    "x": 0.11765,
                                    "y": 0.14167,
                                }
                            ],
                            "type": "PARAGRAPH",
                            "uid": "2",
                        }
                    ],
                    "content": "Kensho: A Rising Innovator Poised for a Strong Future",
                    "locations": [
                        {
                            "height": 0.01389,
                            "page_number": 0,
                            "width": 0.47301,
                            "x": 0.11765,
                            "y": 0.10814,
                        }
                    ],
                    "type": "H1",
                    "uid": "1",
                },
                {
                    "children": [
                        {
                            "children": [],
                            "content": "Kensho shape the future.",
                            "locations": [
                                {
                                    "height": 0.08736,
                                    "page_number": 0,
                                    "width": 0.76042,
                                    "x": 0.11765,
                                    "y": 0.26966,
                                }
                            ],
                            "type": "PARAGRAPH",
                            "uid": "4",
                        }
                    ],
                    "content": "A Promising Start",
                    "locations": [
                        {
                            "height": 0.01641,
                            "page_number": 0,
                            "width": 0.18525,
                            "x": 0.11765,
                            "y": 0.23318,
                        }
                    ],
                    "type": "H1",
                    "uid": "3",
                },
                {
                    "children": [
                        {
                            "children": [],
                            "content": "Kensho have cutting-edge research.",
                            "locations": [
                                {
                                    "height": 0.06899,
                                    "page_number": 0,
                                    "width": 0.70489,
                                    "x": 0.11765,
                                    "y": 0.41602,
                                }
                            ],
                            "type": "PARAGRAPH",
                            "uid": "6",
                        },
                        {
                            "children": [],
                            "content": "Kensho represent the futrue of AI.",
                            "locations": [
                                {
                                    "height": 0.03225,
                                    "page_number": 0,
                                    "width": 0.76047,
                                    "x": 0.11765,
                                    "y": 0.50465,
                                }
                            ],
                            "type": "PARAGRAPH",
                            "uid": "7",
                        },
                    ],
                    "content": "Innovation at the Core",
                    "locations": [
                        {
                            "height": 0.01641,
                            "page_number": 0,
                            "width": 0.23007,
                            "x": 0.11765,
                            "y": 0.37955,
                        }
                    ],
                    "type": "H1",
                    "uid": "5",
                },
                {
                    "children": [
                        {
                            "children": [],
                            "content": "Kensho leading the future of AI.",
                            "locations": [
                                {
                                    "height": 0.05062,
                                    "page_number": 0,
                                    "width": 0.76938,
                                    "x": 0.11765,
                                    "y": 0.59591,
                                }
                            ],
                            "type": "PARAGRAPH",
                            "uid": "9",
                        },
                        {
                            "children": [],
                            "content": "Kensho’s commitment to long-term growth.",
                            "locations": [
                                {
                                    "height": 0.06899,
                                    "page_number": 0,
                                    "width": 0.76134,
                                    "x": 0.11765,
                                    "y": 0.66616,
                                }
                            ],
                            "type": "PARAGRAPH",
                            "uid": "10",
                        },
                        {
                            "children": [
                                {
                                    "children": [],
                                    "content": "Kensho Revenue in millions $",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.23598,
                                            "x": 0.13183,
                                            "y": 0.77674,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "12",
                                },
                                {
                                    "children": [],
                                    "content": "2025",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.23598,
                                            "x": 0.13183,
                                            "y": 0.80008,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "13",
                                },
                                {
                                    "children": [],
                                    "content": "2026",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.23598,
                                            "x": 0.13183,
                                            "y": 0.8234,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "14",
                                },
                                {
                                    "children": [],
                                    "content": "2027",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.23598,
                                            "x": 0.13183,
                                            "y": 0.84672,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "15",
                                },
                                {
                                    "children": [],
                                    "content": "2028",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.23598,
                                            "x": 0.13183,
                                            "y": 0.87005,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "16",
                                },
                                {
                                    "children": [],
                                    "content": "Q1",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.4092,
                                            "y": 0.77674,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "17",
                                },
                                {
                                    "children": [],
                                    "content": "500,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.4092,
                                            "y": 0.80008,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "18",
                                },
                                {
                                    "children": [],
                                    "content": "600,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.4092,
                                            "y": 0.8234,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "19",
                                },
                                {
                                    "children": [],
                                    "content": "700,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.4092,
                                            "y": 0.84672,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "20",
                                },
                                {
                                    "children": [],
                                    "content": "800,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.4092,
                                            "y": 0.87005,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "21",
                                },
                                {
                                    "children": [],
                                    "content": "Q2",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.53175,
                                            "y": 0.77674,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "22",
                                },
                                {
                                    "children": [],
                                    "content": "505,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.53175,
                                            "y": 0.80008,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "23",
                                },
                                {
                                    "children": [],
                                    "content": "605,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.53175,
                                            "y": 0.8234,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "24",
                                },
                                {
                                    "children": [],
                                    "content": "705,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.53175,
                                            "y": 0.84672,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "25",
                                },
                                {
                                    "children": [],
                                    "content": "805,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.53175,
                                            "y": 0.87005,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "26",
                                },
                                {
                                    "children": [],
                                    "content": "Q3",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.6543,
                                            "y": 0.77674,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "27",
                                },
                                {
                                    "children": [],
                                    "content": "510,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.6543,
                                            "y": 0.80008,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "28",
                                },
                                {
                                    "children": [],
                                    "content": "610,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.6543,
                                            "y": 0.8234,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "29",
                                },
                                {
                                    "children": [],
                                    "content": "710,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.6543,
                                            "y": 0.84672,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "30",
                                },
                                {
                                    "children": [],
                                    "content": "810,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.6543,
                                            "y": 0.87005,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "31",
                                },
                                {
                                    "children": [],
                                    "content": "Q4",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.77685,
                                            "y": 0.77674,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "32",
                                },
                                {
                                    "children": [],
                                    "content": "520,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.77685,
                                            "y": 0.80008,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "33",
                                },
                                {
                                    "children": [],
                                    "content": "620,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.77685,
                                            "y": 0.8234,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "34",
                                },
                                {
                                    "children": [],
                                    "content": "720,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.77685,
                                            "y": 0.84672,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "35",
                                },
                                {
                                    "children": [],
                                    "content": "820,000",
                                    "locations": [
                                        {
                                            "height": 0.01263,
                                            "page_number": 0,
                                            "width": 0.06359,
                                            "x": 0.77685,
                                            "y": 0.87005,
                                        }
                                    ],
                                    "type": "TABLE_CELL",
                                    "uid": "36",
                                },
                            ],
                            "content": None,
                            "locations": [
                                {
                                    "height": 0.10593,
                                    "page_number": 0,
                                    "width": 0.70861,
                                    "x": 0.13183,
                                    "y": 0.77674,
                                }
                            ],
                            "type": "TABLE",
                            "uid": "11",
                        },
                    ],
                    "content": "A Vision for the Future",
                    "locations": [
                        {
                            "height": 0.01641,
                            "page_number": 0,
                            "width": 0.2344,
                            "x": 0.11765,
                            "y": 0.55943,
                        }
                    ],
                    "type": "H1",
                    "uid": "8",
                },
            ],
            "content": None,
            "locations": None,
            "type": "DOCUMENT",
            "uid": "0",
        }

        annotations = [
            {
                "content_uids": ["12"],
                "data": {
                    "index": [0, 0],
                    "is_column_header": True,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.23598,
                        "x": 0.13183,
                        "y": 0.77674,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["13"],
                "data": {
                    "index": [1, 0],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.23598,
                        "x": 0.13183,
                        "y": 0.80008,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["14"],
                "data": {
                    "index": [2, 0],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.23598,
                        "x": 0.13183,
                        "y": 0.8234,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["15"],
                "data": {
                    "index": [3, 0],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.23598,
                        "x": 0.13183,
                        "y": 0.84672,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["16"],
                "data": {
                    "index": [4, 0],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.23598,
                        "x": 0.13183,
                        "y": 0.87005,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["17"],
                "data": {
                    "index": [0, 1],
                    "is_column_header": True,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.4092,
                        "y": 0.77674,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["18"],
                "data": {
                    "index": [1, 1],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.4092,
                        "y": 0.80008,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["19"],
                "data": {
                    "index": [2, 1],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.4092,
                        "y": 0.8234,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["20"],
                "data": {
                    "index": [3, 1],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.4092,
                        "y": 0.84672,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["21"],
                "data": {
                    "index": [4, 1],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.4092,
                        "y": 0.87005,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["22"],
                "data": {
                    "index": [0, 2],
                    "is_column_header": True,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.53175,
                        "y": 0.77674,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["23"],
                "data": {
                    "index": [1, 2],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.53175,
                        "y": 0.80008,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["24"],
                "data": {
                    "index": [2, 2],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.53175,
                        "y": 0.8234,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["25"],
                "data": {
                    "index": [3, 2],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.53175,
                        "y": 0.84672,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["26"],
                "data": {
                    "index": [4, 2],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.53175,
                        "y": 0.87005,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["27"],
                "data": {
                    "index": [0, 3],
                    "is_column_header": True,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.6543,
                        "y": 0.77674,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["28"],
                "data": {
                    "index": [1, 3],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.6543,
                        "y": 0.80008,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["29"],
                "data": {
                    "index": [2, 3],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.6543,
                        "y": 0.8234,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["30"],
                "data": {
                    "index": [3, 3],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.6543,
                        "y": 0.84672,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["31"],
                "data": {
                    "index": [4, 3],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.6543,
                        "y": 0.87005,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["32"],
                "data": {
                    "index": [0, 4],
                    "is_column_header": True,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.77685,
                        "y": 0.77674,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["33"],
                "data": {
                    "index": [1, 4],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.77685,
                        "y": 0.80008,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["34"],
                "data": {
                    "index": [2, 4],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.77685,
                        "y": 0.8234,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["35"],
                "data": {
                    "index": [3, 4],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.77685,
                        "y": 0.84672,
                    }
                ],
                "type": "table_structure",
            },
            {
                "content_uids": ["36"],
                "data": {
                    "index": [4, 4],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                    "span": [1, 1],
                },
                "locations": [
                    {
                        "height": 0.01263,
                        "page_number": 0,
                        "width": 0.06359,
                        "x": 0.77685,
                        "y": 0.87005,
                    }
                ],
                "type": "table_structure",
            },
        ]

        expected_tables_grid_and_structure = {
            "11": TableGridAndStructure(
                table_category_type="TABLE",
                table_string_grid=[
                    ["Kensho Revenue in millions $", "Q1", "Q2", "Q3", "Q4"],
                    ["2025", "500,000", "505,000", "510,000", "520,000"],
                    ["2026", "600,000", "605,000", "610,000", "620,000"],
                    ["2027", "700,000", "705,000", "710,000", "720,000"],
                    ["2028", "800,000", "805,000", "810,000", "820,000"],
                ],
                table_structure_annotations=[
                    TableStructureAnnotationModel(
                        content_uids=["12"],
                        data=AnnotationDataModel(
                            index=(0, 0),
                            span=(1, 1),
                            value=None,
                            is_column_header=True,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.23598,
                                x=0.13183,
                                y=0.77674,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["13"],
                        data=AnnotationDataModel(
                            index=(1, 0),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.23598,
                                x=0.13183,
                                y=0.80008,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["14"],
                        data=AnnotationDataModel(
                            index=(2, 0),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.23598,
                                x=0.13183,
                                y=0.8234,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["15"],
                        data=AnnotationDataModel(
                            index=(3, 0),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.23598,
                                x=0.13183,
                                y=0.84672,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["16"],
                        data=AnnotationDataModel(
                            index=(4, 0),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.23598,
                                x=0.13183,
                                y=0.87005,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["17"],
                        data=AnnotationDataModel(
                            index=(0, 1),
                            span=(1, 1),
                            value=None,
                            is_column_header=True,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.4092,
                                y=0.77674,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["18"],
                        data=AnnotationDataModel(
                            index=(1, 1),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.4092,
                                y=0.80008,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["19"],
                        data=AnnotationDataModel(
                            index=(2, 1),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.4092,
                                y=0.8234,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["20"],
                        data=AnnotationDataModel(
                            index=(3, 1),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.4092,
                                y=0.84672,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["21"],
                        data=AnnotationDataModel(
                            index=(4, 1),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.4092,
                                y=0.87005,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["22"],
                        data=AnnotationDataModel(
                            index=(0, 2),
                            span=(1, 1),
                            value=None,
                            is_column_header=True,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.53175,
                                y=0.77674,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["23"],
                        data=AnnotationDataModel(
                            index=(1, 2),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.53175,
                                y=0.80008,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["24"],
                        data=AnnotationDataModel(
                            index=(2, 2),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.53175,
                                y=0.8234,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["25"],
                        data=AnnotationDataModel(
                            index=(3, 2),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.53175,
                                y=0.84672,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["26"],
                        data=AnnotationDataModel(
                            index=(4, 2),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.53175,
                                y=0.87005,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["27"],
                        data=AnnotationDataModel(
                            index=(0, 3),
                            span=(1, 1),
                            value=None,
                            is_column_header=True,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.6543,
                                y=0.77674,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["28"],
                        data=AnnotationDataModel(
                            index=(1, 3),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.6543,
                                y=0.80008,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["29"],
                        data=AnnotationDataModel(
                            index=(2, 3),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.6543,
                                y=0.8234,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["30"],
                        data=AnnotationDataModel(
                            index=(3, 3),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.6543,
                                y=0.84672,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["31"],
                        data=AnnotationDataModel(
                            index=(4, 3),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.6543,
                                y=0.87005,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["32"],
                        data=AnnotationDataModel(
                            index=(0, 4),
                            span=(1, 1),
                            value=None,
                            is_column_header=True,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.77685,
                                y=0.77674,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["33"],
                        data=AnnotationDataModel(
                            index=(1, 4),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.77685,
                                y=0.80008,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["34"],
                        data=AnnotationDataModel(
                            index=(2, 4),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.77685,
                                y=0.8234,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["35"],
                        data=AnnotationDataModel(
                            index=(3, 4),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.77685,
                                y=0.84672,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["36"],
                        data=AnnotationDataModel(
                            index=(4, 4),
                            span=(1, 1),
                            value=None,
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="table_structure",
                        locations=[
                            LocationModel(
                                height=0.01263,
                                width=0.06359,
                                x=0.77685,
                                y=0.87005,
                                page_number=0,
                            )
                        ],
                    ),
                ],
            )
        }

        tables_grid_and_structure = build_table_grids(
            {"content_tree": content, "annotations": annotations}, True
        )
        self.assertEqual(expected_tables_grid_and_structure, tables_grid_and_structure)

    def test_build_table_grids_figure_extracted_table_structure(self) -> None:
        # Test with a spanning cell: Make sure it's duplicated
        content = {
            "children": [
                {
                    "children": [
                        {
                            "children": [],
                            "content": "12",
                            "locations": [
                                {
                                    "height": 0.01069,
                                    "page_number": 0,
                                    "width": 0.20342,
                                    "x": 0.09526,
                                    "y": 0.15867,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "2",
                        },
                        {
                            "children": [],
                            "content": "12",
                            "locations": [
                                {
                                    "height": 0.01069,
                                    "page_number": 0,
                                    "width": 0.19072,
                                    "x": 0.19001,
                                    "y": 0.17463,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "3",
                        },
                        {
                            "children": [],
                            "content": "123",
                            "locations": [
                                {
                                    "height": 0.00621,
                                    "page_number": 0,
                                    "width": 0.01772,
                                    "x": 0.19305,
                                    "y": 0.30414,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "4",
                        },
                        {
                            "children": [],
                            "content": "HIJ",
                            "locations": [
                                {
                                    "height": 0.01069,
                                    "page_number": 0,
                                    "width": 0.18484,
                                    "x": 0.19294,
                                    "y": 0.32121,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "5",
                        },
                        {
                            "children": [
                                {
                                    "children": [],
                                    "content": "SDFII",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "7",
                                },
                                {
                                    "children": [],
                                    "content": "YIUIO",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "8",
                                },
                                {
                                    "children": [],
                                    "content": "789",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "9",
                                },
                                {
                                    "children": [],
                                    "content": "234",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "10",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "11",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "12",
                                },
                                {
                                    "children": [],
                                    "content": "12",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "13",
                                },
                                {
                                    "children": [],
                                    "content": "789",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "14",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "15",
                                },
                                {
                                    "children": [],
                                    "content": "789",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "16",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "17",
                                },
                                {
                                    "children": [],
                                    "content": "789",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "18",
                                },
                                {
                                    "children": [],
                                    "content": "789",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "19",
                                },
                                {
                                    "children": [],
                                    "content": "456",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "20",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "21",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "22",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "23",
                                },
                                {
                                    "children": [],
                                    "content": "234",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "24",
                                },
                                {
                                    "children": [],
                                    "content": "345",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "25",
                                },
                                {
                                    "children": [],
                                    "content": "456",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "26",
                                },
                                {
                                    "children": [],
                                    "content": "789",
                                    "locations": [
                                        {
                                            "height": 0.1181,
                                            "page_number": 0,
                                            "width": 0.33085,
                                            "x": 0.11975,
                                            "y": 0.34856,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "27",
                                },
                            ],
                            "content": None,
                            "locations": [
                                {
                                    "height": 0.1181,
                                    "page_number": 0,
                                    "width": 0.33085,
                                    "x": 0.11975,
                                    "y": 0.34856,
                                }
                            ],
                            "type": "FIGURE_EXTRACTED_TABLE",
                            "uid": "6",
                        },
                        {
                            "children": [],
                            "content": "123",
                            "locations": [
                                {
                                    "height": 0.1181,
                                    "page_number": 0,
                                    "width": 0.33086,
                                    "x": 0.11975,
                                    "y": 0.34856,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "28",
                        },
                        {
                            "children": [],
                            "content": "SDFB",
                            "locations": [
                                {
                                    "height": 0.01069,
                                    "page_number": 0,
                                    "width": 0.17143,
                                    "x": 0.19969,
                                    "y": 0.47834,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "29",
                        },
                        {
                            "children": [],
                            "content": "123",
                            "locations": [
                                {
                                    "height": 0.00671,
                                    "page_number": 0,
                                    "width": 0.03699,
                                    "x": 0.1381,
                                    "y": 0.50235,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "30",
                        },
                        {
                            "children": [],
                            "content": "910",
                            "locations": [
                                {
                                    "height": 0.00671,
                                    "page_number": 0,
                                    "width": 0.05705,
                                    "x": 0.37761,
                                    "y": 0.50235,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "31",
                        },
                        {
                            "children": [],
                            "content": "SDFB",
                            "locations": [
                                {
                                    "height": 0.00834,
                                    "page_number": 0,
                                    "width": 0.20781,
                                    "x": 0.09526,
                                    "y": 0.79686,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "32",
                        },
                        {
                            "children": [],
                            "content": "456",
                            "locations": [
                                {
                                    "height": 0.01069,
                                    "page_number": 0,
                                    "width": 0.14368,
                                    "x": 0.61359,
                                    "y": 0.17463,
                                }
                            ],
                            "type": "FIGURE_TITLE",
                            "uid": "33",
                        },
                        {
                            "children": [],
                            "content": "YNC",
                            "locations": [
                                {
                                    "height": 0.01069,
                                    "page_number": 0,
                                    "width": 0.18489,
                                    "x": 0.59302,
                                    "y": 0.32121,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "34",
                        },
                        {
                            "children": [
                                {
                                    "children": [],
                                    "content": "EFG",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "36",
                                },
                                {
                                    "children": [],
                                    "content": "ELP",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "37",
                                },
                                {
                                    "children": [],
                                    "content": "345",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "38",
                                },
                                {
                                    "children": [],
                                    "content": "12",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "39",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "40",
                                },
                                {
                                    "children": [],
                                    "content": "345",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "41",
                                },
                                {
                                    "children": [],
                                    "content": "321",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "42",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "43",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "44",
                                },
                                {
                                    "children": [],
                                    "content": "345",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "45",
                                },
                                {
                                    "children": [],
                                    "content": "234",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "46",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "47",
                                },
                                {
                                    "children": [],
                                    "content": "12",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "48",
                                },
                                {
                                    "children": [],
                                    "content": "789",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "49",
                                },
                                {
                                    "children": [],
                                    "content": "12",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "50",
                                },
                                {
                                    "children": [],
                                    "content": "123",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "51",
                                },
                                {
                                    "children": [],
                                    "content": "789",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "52",
                                },
                                {
                                    "children": [],
                                    "content": "910",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "53",
                                },
                                {
                                    "children": [],
                                    "content": "12",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "54",
                                },
                                {
                                    "children": [],
                                    "content": "456",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "55",
                                },
                                {
                                    "children": [],
                                    "content": "321",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "56",
                                },
                                {
                                    "children": [],
                                    "content": "910",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "57",
                                },
                                {
                                    "children": [],
                                    "content": "345",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "58",
                                },
                                {
                                    "children": [],
                                    "content": "234",
                                    "locations": [
                                        {
                                            "height": 0.12461,
                                            "page_number": 0,
                                            "width": 0.34248,
                                            "x": 0.50986,
                                            "y": 0.34171,
                                        }
                                    ],
                                    "type": "FIGURE_EXTRACTED_TABLE_CELL",
                                    "uid": "59",
                                },
                            ],
                            "content": None,
                            "locations": [
                                {
                                    "height": 0.12461,
                                    "page_number": 0,
                                    "width": 0.34248,
                                    "x": 0.50986,
                                    "y": 0.34171,
                                }
                            ],
                            "type": "FIGURE_EXTRACTED_TABLE",
                            "uid": "35",
                        },
                        {
                            "children": [],
                            "content": None,
                            "locations": [
                                {
                                    "height": 0.12461,
                                    "page_number": 0,
                                    "width": 0.34248,
                                    "x": 0.50986,
                                    "y": 0.34171,
                                }
                            ],
                            "type": "FIGURE",
                            "uid": "599",
                        },
                        {
                            "children": [],
                            "content": "789",
                            "locations": [
                                {
                                    "height": 0.12461,
                                    "page_number": 0,
                                    "width": 0.34248,
                                    "x": 0.50986,
                                    "y": 0.34171,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "60",
                        },
                        {
                            "children": [],
                            "content": "FJD",
                            "locations": [
                                {
                                    "height": 0.01069,
                                    "page_number": 0,
                                    "width": 0.12609,
                                    "x": 0.62236,
                                    "y": 0.47834,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "61",
                        },
                        {
                            "children": [],
                            "content": "234",
                            "locations": [
                                {
                                    "height": 0.00672,
                                    "page_number": 0,
                                    "width": 0.07239,
                                    "x": 0.53809,
                                    "y": 0.50228,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "62",
                        },
                        {
                            "children": [],
                            "content": "456",
                            "locations": [
                                {
                                    "height": 0.00672,
                                    "page_number": 0,
                                    "width": 0.03711,
                                    "x": 0.79764,
                                    "y": 0.50228,
                                }
                            ],
                            "type": "TEXT",
                            "uid": "63",
                        },
                        {
                            "children": [],
                            "content": "321",
                            "locations": [
                                {
                                    "height": 0.01221,
                                    "page_number": 0,
                                    "width": 0.83324,
                                    "x": 0.09526,
                                    "y": 0.96147,
                                }
                            ],
                            "type": "PAGE_FOOTER",
                            "uid": "64",
                        },
                    ],
                    "content": "SDFL",
                    "locations": [
                        {
                            "height": 0.01903,
                            "page_number": 0,
                            "width": 0.37017,
                            "x": 0.28578,
                            "y": 0.10378,
                        }
                    ],
                    "type": "H1",
                    "uid": "1",
                }
            ],
            "content": None,
            "locations": None,
            "type": "DOCUMENT",
            "uid": "0",
        }

        annotations = [
            {
                "content_uids": ["7"],
                "data": {"index": [0, 0], "span": [1, 1], "value": "SDFII"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["8"],
                "data": {"index": [0, 1], "span": [1, 1], "value": "YIUIO"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["9"],
                "data": {"index": [0, 2], "span": [1, 1], "value": "789"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["10"],
                "data": {"index": [1, 0], "span": [1, 1], "value": "234"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["11"],
                "data": {"index": [1, 1], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["12"],
                "data": {"index": [1, 2], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["13"],
                "data": {"index": [2, 0], "span": [1, 1], "value": "12"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["14"],
                "data": {"index": [2, 1], "span": [1, 1], "value": "789"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["15"],
                "data": {"index": [2, 2], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["16"],
                "data": {"index": [3, 0], "span": [1, 1], "value": "789"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["17"],
                "data": {"index": [3, 1], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["18"],
                "data": {"index": [3, 2], "span": [1, 1], "value": "789"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["19"],
                "data": {"index": [4, 0], "span": [1, 1], "value": "789"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["20"],
                "data": {"index": [4, 1], "span": [1, 1], "value": "456"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["21"],
                "data": {"index": [4, 2], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["22"],
                "data": {"index": [5, 0], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["23"],
                "data": {"index": [5, 1], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["24"],
                "data": {"index": [5, 2], "span": [1, 1], "value": "234"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["25"],
                "data": {"index": [6, 0], "span": [1, 1], "value": "345"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["26"],
                "data": {"index": [6, 1], "span": [1, 1], "value": "456"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["27"],
                "data": {"index": [6, 2], "span": [1, 1], "value": "789"},
                "locations": [
                    {
                        "height": 0.1181,
                        "page_number": 0,
                        "width": 0.33085,
                        "x": 0.11975,
                        "y": 0.34856,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["36"],
                "data": {"index": [0, 0], "span": [1, 1], "value": "EFG"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["37"],
                "data": {"index": [0, 1], "span": [1, 1], "value": "ELP"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["38"],
                "data": {"index": [0, 2], "span": [1, 1], "value": "345"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["39"],
                "data": {"index": [1, 0], "span": [1, 1], "value": "12"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["40"],
                "data": {"index": [1, 1], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["41"],
                "data": {"index": [1, 2], "span": [1, 1], "value": "345"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["42"],
                "data": {"index": [2, 0], "span": [1, 1], "value": "321"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["43"],
                "data": {"index": [2, 1], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["44"],
                "data": {"index": [2, 2], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["45"],
                "data": {"index": [3, 0], "span": [1, 1], "value": "345"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["46"],
                "data": {"index": [3, 1], "span": [1, 1], "value": "234"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["47"],
                "data": {"index": [3, 2], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["48"],
                "data": {"index": [4, 0], "span": [1, 1], "value": "12"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["49"],
                "data": {"index": [4, 1], "span": [1, 1], "value": "789"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["50"],
                "data": {"index": [4, 2], "span": [1, 1], "value": "12"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["51"],
                "data": {"index": [5, 0], "span": [1, 1], "value": "123"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["52"],
                "data": {"index": [5, 1], "span": [1, 1], "value": "789"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["53"],
                "data": {"index": [5, 2], "span": [1, 1], "value": "910"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["54"],
                "data": {"index": [6, 0], "span": [1, 1], "value": "12"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["55"],
                "data": {"index": [6, 1], "span": [1, 1], "value": "456"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["56"],
                "data": {"index": [6, 2], "span": [1, 1], "value": "321"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["57"],
                "data": {"index": [7, 0], "span": [1, 1], "value": "910"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["58"],
                "data": {"index": [7, 1], "span": [1, 1], "value": "345"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
            {
                "content_uids": ["59"],
                "data": {"index": [7, 2], "span": [1, 1], "value": "234"},
                "locations": [
                    {
                        "height": 0.12461,
                        "page_number": 0,
                        "width": 0.34248,
                        "x": 0.50986,
                        "y": 0.34171,
                    }
                ],
                "type": "figure_extracted_table_structure",
            },
        ]

        expected_tables_grid_and_structure = {
            "6": TableGridAndStructure(
                table_category_type="FIGURE_EXTRACTED_TABLE",
                table_string_grid=[
                    ["SDFII", "YIUIO", "789"],
                    ["234", "123", "123"],
                    ["12", "789", "123"],
                    ["789", "123", "789"],
                    ["789", "456", "123"],
                    ["123", "123", "234"],
                    ["345", "456", "789"],
                ],
                table_structure_annotations=[
                    TableStructureAnnotationModel(
                        content_uids=["7"],
                        data=AnnotationDataModel(
                            index=(0, 0),
                            span=(1, 1),
                            value="SDFII",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["8"],
                        data=AnnotationDataModel(
                            index=(0, 1),
                            span=(1, 1),
                            value="YIUIO",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["9"],
                        data=AnnotationDataModel(
                            index=(0, 2),
                            span=(1, 1),
                            value="789",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["10"],
                        data=AnnotationDataModel(
                            index=(1, 0),
                            span=(1, 1),
                            value="234",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["11"],
                        data=AnnotationDataModel(
                            index=(1, 1),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["12"],
                        data=AnnotationDataModel(
                            index=(1, 2),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["13"],
                        data=AnnotationDataModel(
                            index=(2, 0),
                            span=(1, 1),
                            value="12",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["14"],
                        data=AnnotationDataModel(
                            index=(2, 1),
                            span=(1, 1),
                            value="789",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["15"],
                        data=AnnotationDataModel(
                            index=(2, 2),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["16"],
                        data=AnnotationDataModel(
                            index=(3, 0),
                            span=(1, 1),
                            value="789",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["17"],
                        data=AnnotationDataModel(
                            index=(3, 1),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["18"],
                        data=AnnotationDataModel(
                            index=(3, 2),
                            span=(1, 1),
                            value="789",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["19"],
                        data=AnnotationDataModel(
                            index=(4, 0),
                            span=(1, 1),
                            value="789",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["20"],
                        data=AnnotationDataModel(
                            index=(4, 1),
                            span=(1, 1),
                            value="456",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["21"],
                        data=AnnotationDataModel(
                            index=(4, 2),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["22"],
                        data=AnnotationDataModel(
                            index=(5, 0),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["23"],
                        data=AnnotationDataModel(
                            index=(5, 1),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["24"],
                        data=AnnotationDataModel(
                            index=(5, 2),
                            span=(1, 1),
                            value="234",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["25"],
                        data=AnnotationDataModel(
                            index=(6, 0),
                            span=(1, 1),
                            value="345",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["26"],
                        data=AnnotationDataModel(
                            index=(6, 1),
                            span=(1, 1),
                            value="456",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["27"],
                        data=AnnotationDataModel(
                            index=(6, 2),
                            span=(1, 1),
                            value="789",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.1181,
                                width=0.33085,
                                x=0.11975,
                                y=0.34856,
                                page_number=0,
                            )
                        ],
                    ),
                ],
            ),
            "35": TableGridAndStructure(
                table_category_type="FIGURE_EXTRACTED_TABLE",
                table_string_grid=[
                    ["EFG", "ELP", "345"],
                    ["12", "123", "345"],
                    ["321", "123", "123"],
                    ["345", "234", "123"],
                    ["12", "789", "12"],
                    ["123", "789", "910"],
                    ["12", "456", "321"],
                    ["910", "345", "234"],
                ],
                table_structure_annotations=[
                    TableStructureAnnotationModel(
                        content_uids=["36"],
                        data=AnnotationDataModel(
                            index=(0, 0),
                            span=(1, 1),
                            value="EFG",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["37"],
                        data=AnnotationDataModel(
                            index=(0, 1),
                            span=(1, 1),
                            value="ELP",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["38"],
                        data=AnnotationDataModel(
                            index=(0, 2),
                            span=(1, 1),
                            value="345",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["39"],
                        data=AnnotationDataModel(
                            index=(1, 0),
                            span=(1, 1),
                            value="12",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["40"],
                        data=AnnotationDataModel(
                            index=(1, 1),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["41"],
                        data=AnnotationDataModel(
                            index=(1, 2),
                            span=(1, 1),
                            value="345",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["42"],
                        data=AnnotationDataModel(
                            index=(2, 0),
                            span=(1, 1),
                            value="321",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["43"],
                        data=AnnotationDataModel(
                            index=(2, 1),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["44"],
                        data=AnnotationDataModel(
                            index=(2, 2),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["45"],
                        data=AnnotationDataModel(
                            index=(3, 0),
                            span=(1, 1),
                            value="345",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["46"],
                        data=AnnotationDataModel(
                            index=(3, 1),
                            span=(1, 1),
                            value="234",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["47"],
                        data=AnnotationDataModel(
                            index=(3, 2),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["48"],
                        data=AnnotationDataModel(
                            index=(4, 0),
                            span=(1, 1),
                            value="12",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["49"],
                        data=AnnotationDataModel(
                            index=(4, 1),
                            span=(1, 1),
                            value="789",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["50"],
                        data=AnnotationDataModel(
                            index=(4, 2),
                            span=(1, 1),
                            value="12",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["51"],
                        data=AnnotationDataModel(
                            index=(5, 0),
                            span=(1, 1),
                            value="123",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["52"],
                        data=AnnotationDataModel(
                            index=(5, 1),
                            span=(1, 1),
                            value="789",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["53"],
                        data=AnnotationDataModel(
                            index=(5, 2),
                            span=(1, 1),
                            value="910",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["54"],
                        data=AnnotationDataModel(
                            index=(6, 0),
                            span=(1, 1),
                            value="12",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["55"],
                        data=AnnotationDataModel(
                            index=(6, 1),
                            span=(1, 1),
                            value="456",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["56"],
                        data=AnnotationDataModel(
                            index=(6, 2),
                            span=(1, 1),
                            value="321",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["57"],
                        data=AnnotationDataModel(
                            index=(7, 0),
                            span=(1, 1),
                            value="910",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["58"],
                        data=AnnotationDataModel(
                            index=(7, 1),
                            span=(1, 1),
                            value="345",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                    TableStructureAnnotationModel(
                        content_uids=["59"],
                        data=AnnotationDataModel(
                            index=(7, 2),
                            span=(1, 1),
                            value="234",
                            is_column_header=False,
                            is_projected_row_header=False,
                        ),
                        type="figure_extracted_table_structure",
                        locations=[
                            LocationModel(
                                height=0.12461,
                                width=0.34248,
                                x=0.50986,
                                y=0.34171,
                                page_number=0,
                            )
                        ],
                    ),
                ],
            ),
        }
        tables_grid_and_structure = build_table_grids(
            {"content_tree": content, "annotations": annotations}, True
        )
        self.assertEqual(expected_tables_grid_and_structure, tables_grid_and_structure)


def _make_table_structure_annotation(
    content_uid: str,
    row: int,
    col: int,
    row_span: int = 1,
    col_span: int = 1,
    is_column_header: bool = False,
    is_projected_row_header: bool = False,
) -> TableStructureAnnotationModel:
    """Create a TableStructureAnnotationModel for testing."""
    return TableStructureAnnotationModel(
        content_uids=[content_uid],
        data=AnnotationDataModel(
            index=(row, col),
            span=(row_span, col_span),
            is_column_header=is_column_header,
            is_projected_row_header=is_projected_row_header,
        ),
        type="table_structure",
        locations=None,
    )


def _make_content_model_dict(
    uid: str, content: str, node_type: str = "TABLE_CELL"
) -> dict[str, Any]:
    """Create a ContentModel-compatible dict for testing."""
    return {
        "uid": uid,
        "type": node_type,
        "content": content,
        "children": [],
        "locations": None,
    }


def _build_simple_table_document() -> dict[str, Any]:
    """Build a simple table document for testing hierarchy.

    Table structure:
        Row 0: Column headers ["Name", "Value"]
        Row 1: Projected row header "ASSETS" (spans 2 cols)
        Row 2: Projected row header "Current Assets" (spans 2 cols)
        Row 3: Data row ["Cash", "100"]  (child of "Current Assets")
        Row 4: Data row ["Securities", "200"]  (child of "Current Assets")
        Row 5: Data row ["Equipment", "500"]  (child of "ASSETS", not via "Current Assets")

    Hierarchy:
        TABLE
          ASSETS
            Current Assets
              Cash | 100
              Securities | 200
            Equipment | 500
    """
    return {
        "annotations": [
            # Column headers (row 0)
            {
                "content_uids": ["c1"],
                "data": {
                    "index": [0, 0],
                    "span": [1, 1],
                    "is_column_header": True,
                    "is_projected_row_header": False,
                },
                "type": "table_structure",
            },
            {
                "content_uids": ["c2"],
                "data": {
                    "index": [0, 1],
                    "span": [1, 1],
                    "is_column_header": True,
                    "is_projected_row_header": False,
                },
                "type": "table_structure",
            },
            # Projected row header "ASSETS" (row 1, spans 2 cols)
            {
                "content_uids": ["c3"],
                "data": {
                    "index": [1, 0],
                    "span": [1, 2],
                    "is_column_header": False,
                    "is_projected_row_header": True,
                },
                "type": "table_structure",
            },
            # Projected row header "Current Assets" (row 2, spans 2 cols)
            {
                "content_uids": ["c4"],
                "data": {
                    "index": [2, 0],
                    "span": [1, 2],
                    "is_column_header": False,
                    "is_projected_row_header": True,
                },
                "type": "table_structure",
            },
            # Data row "Cash" (row 3)
            {
                "content_uids": ["c5"],
                "data": {
                    "index": [3, 0],
                    "span": [1, 1],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                },
                "type": "table_structure",
            },
            {
                "content_uids": ["c6"],
                "data": {
                    "index": [3, 1],
                    "span": [1, 1],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                },
                "type": "table_structure",
            },
            # Data row "Securities" (row 4)
            {
                "content_uids": ["c7"],
                "data": {
                    "index": [4, 0],
                    "span": [1, 1],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                },
                "type": "table_structure",
            },
            {
                "content_uids": ["c8"],
                "data": {
                    "index": [4, 1],
                    "span": [1, 1],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                },
                "type": "table_structure",
            },
            # Data row "Equipment" (row 5)
            {
                "content_uids": ["c9"],
                "data": {
                    "index": [5, 0],
                    "span": [1, 1],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                },
                "type": "table_structure",
            },
            {
                "content_uids": ["c10"],
                "data": {
                    "index": [5, 1],
                    "span": [1, 1],
                    "is_column_header": False,
                    "is_projected_row_header": False,
                },
                "type": "table_structure",
            },
            # Relations
            {
                "data": {
                    "relation_type": "row_key_parent",
                    "source_content_uid": "c3",
                    "target_content_uid": "c4",
                },
                "type": "relation",
            },
            {
                "data": {
                    "relation_type": "row_key_parent",
                    "source_content_uid": "c4",
                    "target_content_uid": "c5",
                },
                "type": "relation",
            },
            {
                "data": {
                    "relation_type": "row_key_parent",
                    "source_content_uid": "c4",
                    "target_content_uid": "c7",
                },
                "type": "relation",
            },
            {
                "data": {
                    "relation_type": "row_key_parent",
                    "source_content_uid": "c3",
                    "target_content_uid": "c9",
                },
                "type": "relation",
            },
        ],
        "content_tree": {
            "uid": "0",
            "type": "DOCUMENT",
            "content": None,
            "children": [
                {
                    "uid": "t1",
                    "type": "TABLE",
                    "content": None,
                    "children": [
                        _make_content_model_dict("c1", "Name"),
                        _make_content_model_dict("c2", "Value"),
                        _make_content_model_dict("c3", "ASSETS"),
                        _make_content_model_dict("c4", "Current Assets"),
                        _make_content_model_dict("c5", "Cash"),
                        _make_content_model_dict("c6", "100"),
                        _make_content_model_dict("c7", "Securities"),
                        _make_content_model_dict("c8", "200"),
                        _make_content_model_dict("c9", "Equipment"),
                        _make_content_model_dict("c10", "500"),
                    ],
                }
            ],
        },
    }


class TestBuildTableCellHierarchyTreeNode(TestCase):
    """Tests for _build_table_cell_hierarchy_tree_node."""

    def test_leaf_node_no_children(self) -> None:
        """A projected row header with only data row children produces contents, no child nodes."""
        cell_uid_to_annotation = {
            "c4": _make_table_structure_annotation(
                "c4", 2, 0, is_projected_row_header=True
            ),
            "c5": _make_table_structure_annotation("c5", 3, 0),
            "c6": _make_table_structure_annotation("c6", 3, 1),
            "c7": _make_table_structure_annotation("c7", 4, 0),
            "c8": _make_table_structure_annotation("c8", 4, 1),
        }
        parent_to_children = {"c4": ["c5", "c7"]}
        all_projected_row_header_uids = {"c3", "c4"}
        row_index_to_annotations = defaultdict(list)
        row_index_to_annotations[3] = [
            cell_uid_to_annotation["c5"],
            cell_uid_to_annotation["c6"],
        ]
        row_index_to_annotations[4] = [
            cell_uid_to_annotation["c7"],
            cell_uid_to_annotation["c8"],
        ]

        node = _build_table_cell_hierarchy_tree_node(
            "c4",
            cell_uid_to_annotation,
            parent_to_children,
            all_projected_row_header_uids,
            row_index_to_annotations,
        )

        self.assertEqual(node.node_uid, "c4")
        self.assertEqual(node.node_type, ContentCategory.TABLE_CELL.value)
        self.assertEqual(len(node.children), 0)
        self.assertEqual(len(node.contents), 4)

    def test_node_with_projected_row_header_children(self) -> None:
        """A projected row header with sub-headers produces child nodes."""
        cell_uid_to_annotation = {
            "c3": _make_table_structure_annotation(
                "c3", 1, 0, is_projected_row_header=True
            ),
            "c4": _make_table_structure_annotation(
                "c4", 2, 0, is_projected_row_header=True
            ),
            "c9": _make_table_structure_annotation("c9", 5, 0),
            "c10": _make_table_structure_annotation("c10", 5, 1),
        }
        parent_to_children = {"c3": ["c4", "c9"]}
        all_projected_row_header_uids = {"c3", "c4"}
        row_index_to_annotations = defaultdict(list)
        row_index_to_annotations[5] = [
            cell_uid_to_annotation["c9"],
            cell_uid_to_annotation["c10"],
        ]

        node = _build_table_cell_hierarchy_tree_node(
            "c3",
            cell_uid_to_annotation,
            dict(parent_to_children),
            all_projected_row_header_uids,
            row_index_to_annotations,
        )

        self.assertEqual(node.node_uid, "c3")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].node_uid, "c4")
        self.assertEqual(len(node.contents), 2)


class TestGetTableUidToTableCellHierarchyTree(TestCase):
    """Tests for _get_table_uid_to_table_cell_hierarchy_tree."""

    def test_builds_tree_for_simple_table(self) -> None:
        """Test building hierarchy tree from annotations and relations."""
        doc = _build_simple_table_document()
        parsed = load_output_to_pydantic(doc)

        table_uid_to_cells_mapping = get_table_uid_to_cells_mapping(parsed.content_tree)
        table_cell_annotations = [
            ann
            for ann in parsed.annotations
            if isinstance(ann, TableStructureAnnotationModel)
        ]
        relation_annotations = [
            ann
            for ann in parsed.annotations
            if not isinstance(ann, TableStructureAnnotationModel)
        ]

        result = _get_table_uid_to_table_cell_hierarchy_tree(
            table_uid_to_cells_mapping,
            table_cell_annotations,
            relation_annotations,
        )

        self.assertIn("t1", result)
        tree = result["t1"]
        self.assertEqual(tree.node_uid, "t1")
        self.assertEqual(tree.node_type, ContentCategory.TABLE.value)
        self.assertEqual(len(tree.children), 1)

        assets_node = tree.children[0]
        self.assertEqual(assets_node.node_uid, "c3")
        self.assertEqual(len(assets_node.children), 1)
        self.assertEqual(len(assets_node.contents), 2)

        current_assets_node = assets_node.children[0]
        self.assertEqual(current_assets_node.node_uid, "c4")
        self.assertEqual(len(current_assets_node.children), 0)
        self.assertEqual(len(current_assets_node.contents), 4)


class TestExpandAnnotationsToRowGroups(TestCase):
    """Tests for _expand_annotations_to_row_groups."""

    def test_single_annotation_no_span(self) -> None:
        """Single annotation with span (1,1) produces one entry."""
        uid_to_text = {"c1": "Hello"}
        annotations = [_make_table_structure_annotation("c1", 0, 0)]
        result = _expand_annotations_to_row_groups(annotations, uid_to_text)
        self.assertEqual(dict(result), {0: [(0, "Hello")]})

    def test_col_span_with_duplicate(self) -> None:
        """Column span duplicates text across columns when flag is True."""
        uid_to_text = {"c1": "Wide"}
        annotations = [_make_table_structure_annotation("c1", 0, 0, col_span=3)]
        result = _expand_annotations_to_row_groups(
            annotations, uid_to_text, duplicate_merged_cells_content_flag=True
        )
        self.assertEqual(dict(result), {0: [(0, "Wide"), (1, "Wide"), (2, "Wide")]})

    def test_col_span_without_duplicate(self) -> None:
        """Column span fills empty strings for non-first cells when flag is False."""
        uid_to_text = {"c1": "Wide"}
        annotations = [_make_table_structure_annotation("c1", 0, 0, col_span=3)]
        result = _expand_annotations_to_row_groups(
            annotations, uid_to_text, duplicate_merged_cells_content_flag=False
        )
        self.assertEqual(dict(result), {0: [(0, "Wide"), (1, ""), (2, "")]})

    def test_row_span_with_duplicate(self) -> None:
        """Row span duplicates text across rows when flag is True."""
        uid_to_text = {"c1": "Tall"}
        annotations = [_make_table_structure_annotation("c1", 1, 0, row_span=2)]
        result = _expand_annotations_to_row_groups(
            annotations, uid_to_text, duplicate_merged_cells_content_flag=True
        )
        self.assertEqual(dict(result), {1: [(0, "Tall")], 2: [(0, "Tall")]})

    def test_row_span_without_duplicate(self) -> None:
        """Row span fills empty string for non-first cells when flag is False."""
        uid_to_text = {"c1": "Tall"}
        annotations = [_make_table_structure_annotation("c1", 1, 0, row_span=2)]
        result = _expand_annotations_to_row_groups(
            annotations, uid_to_text, duplicate_merged_cells_content_flag=False
        )
        self.assertEqual(dict(result), {1: [(0, "Tall")], 2: [(0, "")]})

    def test_missing_content_uid_uses_empty_string(self) -> None:
        """Annotation whose content_uid is not in uid_to_text uses empty string."""
        uid_to_text = {"c1": "Hello"}
        annotations = [_make_table_structure_annotation("c_missing", 0, 0)]
        result = _expand_annotations_to_row_groups(annotations, uid_to_text)
        self.assertEqual(dict(result), {0: [(0, "")]})

    def test_multiple_annotations_same_row(self) -> None:
        """Multiple annotations in the same row are grouped together."""
        uid_to_text = {"c1": "A", "c2": "B"}
        annotations = [
            _make_table_structure_annotation("c1", 0, 0),
            _make_table_structure_annotation("c2", 0, 1),
        ]
        result = _expand_annotations_to_row_groups(annotations, uid_to_text)
        self.assertEqual(dict(result), {0: [(0, "A"), (1, "B")]})


class TestGetColumnHeaderGrid(TestCase):
    """Tests for _get_column_header_grid."""

    def test_extracts_consecutive_headers(self) -> None:
        """Column header rows starting from row 0 are extracted."""
        cells = [
            ContentModel(**_make_content_model_dict("c1", "Name")),
            ContentModel(**_make_content_model_dict("c2", "Value")),
            ContentModel(**_make_content_model_dict("c3", "Data")),
        ]
        annotations = [
            _make_table_structure_annotation("c1", 0, 0, is_column_header=True),
            _make_table_structure_annotation("c2", 0, 1, is_column_header=True),
            _make_table_structure_annotation("c3", 1, 0, is_column_header=False),
        ]
        grid = _get_column_header_grid(cells, annotations)
        self.assertEqual(grid, [["Name", "Value"]])

    def test_no_headers_returns_empty(self) -> None:
        """Table with no column headers returns empty grid."""
        cells = [ContentModel(**_make_content_model_dict("c1", "Data"))]
        annotations = [
            _make_table_structure_annotation("c1", 0, 0, is_column_header=False)
        ]
        grid = _get_column_header_grid(cells, annotations)
        self.assertEqual(grid, [])

    def test_spanning_header_with_duplicate(self) -> None:
        """Spanning column headers are duplicated when flag is True."""
        cells = [
            ContentModel(**_make_content_model_dict("c1", "Header")),
            ContentModel(**_make_content_model_dict("c2", "Other")),
        ]
        annotations = [
            _make_table_structure_annotation(
                "c1", 0, 0, col_span=2, is_column_header=True
            ),
            _make_table_structure_annotation("c2", 0, 2, is_column_header=True),
        ]
        grid = _get_column_header_grid(
            cells, annotations, duplicate_merged_cells_content_flag=True
        )
        self.assertEqual(grid, [["Header", "Header", "Other"]])

    def test_spanning_header_without_duplicate(self) -> None:
        """Spanning column headers leave empty cells when flag is False."""
        cells = [
            ContentModel(**_make_content_model_dict("c1", "Header")),
            ContentModel(**_make_content_model_dict("c2", "Other")),
        ]
        annotations = [
            _make_table_structure_annotation(
                "c1", 0, 0, col_span=2, is_column_header=True
            ),
            _make_table_structure_annotation("c2", 0, 2, is_column_header=True),
        ]
        grid = _get_column_header_grid(
            cells, annotations, duplicate_merged_cells_content_flag=False
        )
        self.assertEqual(grid, [["Header", "", "Other"]])


class TestConvertCellHierarchyTreeToGridHierarchyTree(TestCase):
    """Tests for _convert_table_cell_hierarchy_tree_to_table_grid_hierarchy_tree."""

    def test_converts_to_text_grid(self) -> None:
        """Converts annotation-based contents to string grid with text."""
        cell_contents = [
            ContentModel(**_make_content_model_dict("c3", "ASSETS")),
            ContentModel(**_make_content_model_dict("c5", "Cash")),
            ContentModel(**_make_content_model_dict("c6", "100")),
        ]
        cell_tree = TableCellHierarchyTreeModel(
            node_uid="c3",
            node_type=ContentCategory.TABLE_CELL.value,
            children=[],
            contents=[
                _make_table_structure_annotation("c5", 3, 0),
                _make_table_structure_annotation("c6", 3, 1),
            ],
        )
        grid_tree = _convert_table_cell_hierarchy_tree_to_table_grid_hierarchy_tree(
            cell_tree, cell_contents
        )
        self.assertEqual(grid_tree.node_text, "ASSETS")
        self.assertEqual(grid_tree.contents, [["Cash", "100"]])

    def test_prepends_column_headers(self) -> None:
        """Column header grid is prepended to contents."""
        cell_contents = [
            ContentModel(**_make_content_model_dict("c3", "ASSETS")),
            ContentModel(**_make_content_model_dict("c5", "Cash")),
            ContentModel(**_make_content_model_dict("c6", "100")),
        ]
        cell_tree = TableCellHierarchyTreeModel(
            node_uid="c3",
            node_type=ContentCategory.TABLE_CELL.value,
            children=[],
            contents=[
                _make_table_structure_annotation("c5", 3, 0),
                _make_table_structure_annotation("c6", 3, 1),
            ],
        )
        grid_tree = _convert_table_cell_hierarchy_tree_to_table_grid_hierarchy_tree(
            cell_tree, cell_contents, column_header_grid=[["Name", "Value"]]
        )
        self.assertEqual(grid_tree.contents, [["Name", "Value"], ["Cash", "100"]])

    def test_empty_contents_no_header_prepend(self) -> None:
        """Column headers are NOT prepended if there are no content rows."""
        cell_contents = [ContentModel(**_make_content_model_dict("c3", "ASSETS"))]
        cell_tree = TableCellHierarchyTreeModel(
            node_uid="c3",
            node_type=ContentCategory.TABLE_CELL.value,
            children=[],
            contents=[],
        )
        grid_tree = _convert_table_cell_hierarchy_tree_to_table_grid_hierarchy_tree(
            cell_tree, cell_contents, column_header_grid=[["Name", "Value"]]
        )
        self.assertEqual(grid_tree.contents, [])


class TestGetTableUidToTableGridHierarchyTree(TestCase):
    """Tests for _get_table_uid_to_table_grid_hierarchy_tree (end-to-end)."""

    def test_end_to_end_hierarchy(self) -> None:
        """Full pipeline: build grid hierarchy tree from a serialized document."""
        doc = _build_simple_table_document()
        parsed = load_output_to_pydantic(doc)
        result = _get_table_uid_to_table_grid_hierarchy_tree(parsed)

        self.assertIn("t1", result)
        tree = result["t1"]
        self.assertIsNone(tree.node_text)
        self.assertEqual(tree.node_type, ContentCategory.TABLE.value)

        self.assertEqual(len(tree.children), 1)
        assets = tree.children[0]
        self.assertEqual(assets.node_text, "ASSETS")
        self.assertEqual(len(assets.children), 1)
        self.assertEqual(assets.contents, [["Name", "Value"], ["Equipment", "500"]])

        current_assets = assets.children[0]
        self.assertEqual(current_assets.node_text, "Current Assets")
        self.assertEqual(
            current_assets.contents,
            [["Name", "Value"], ["Cash", "100"], ["Securities", "200"]],
        )

    def test_end_to_end_no_hierarchy(self) -> None:
        """Table with no projected row headers has all rows in table contents."""
        doc = {
            "annotations": [
                {
                    "content_uids": ["c1"],
                    "data": {
                        "index": [0, 0],
                        "span": [1, 1],
                        "is_column_header": False,
                        "is_projected_row_header": False,
                    },
                    "type": "table_structure",
                },
            ],
            "content_tree": {
                "uid": "0",
                "type": "DOCUMENT",
                "content": None,
                "children": [
                    {
                        "uid": "t1",
                        "type": "TABLE",
                        "content": None,
                        "children": [_make_content_model_dict("c1", "Data")],
                    }
                ],
            },
        }
        parsed = load_output_to_pydantic(doc)
        result = _get_table_uid_to_table_grid_hierarchy_tree(parsed)
        tree = result["t1"]
        self.assertEqual(len(tree.children), 0)
        self.assertEqual(tree.contents, [["Data"]])
