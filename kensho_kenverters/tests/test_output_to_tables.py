import json
import os
from typing import Any, ClassVar
from unittest import TestCase

from ..extract_output_models import AnnotationDataModel, AnnotationModel, LocationModel
from ..output_to_tables import (
    build_table_grids,
    extract_pd_dfs_from_output,
    extract_pd_dfs_with_locs_and_table_structure_from_output,
)

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
            {
                "index": (0, 0),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.22128,
                        "x": 0.16008,
                        "y": 0.40464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (0, 1),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.02241,
                        "x": 0.46007,
                        "y": 0.40464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (0, 2),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.02241,
                        "x": 0.56008,
                        "y": 0.40464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (0, 3),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.02241,
                        "x": 0.66008,
                        "y": 0.40464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (0, 4),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.02241,
                        "x": 0.76008,
                        "y": 0.40464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (1, 0),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.03736,
                        "x": 0.16008,
                        "y": 0.42464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (1, 1),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.46007,
                        "y": 0.42464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (1, 2),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.56008,
                        "y": 0.42464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (1, 3),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.66008,
                        "y": 0.42464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (1, 4),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.76008,
                        "y": 0.42464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (2, 0),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.03736,
                        "x": 0.16008,
                        "y": 0.44464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (2, 1),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.46007,
                        "y": 0.44464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (2, 2),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.56008,
                        "y": 0.44464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (2, 3),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.66008,
                        "y": 0.44464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (2, 4),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.76008,
                        "y": 0.44464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (3, 0),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.03736,
                        "x": 0.16008,
                        "y": 0.46465,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (3, 1),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.46007,
                        "y": 0.46465,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (3, 2),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.56008,
                        "y": 0.46465,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (3, 3),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.66008,
                        "y": 0.46465,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (3, 4),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.76008,
                        "y": 0.46465,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (4, 0),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.03736,
                        "x": 0.16008,
                        "y": 0.48464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (4, 1),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.46007,
                        "y": 0.48464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (4, 2),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.56008,
                        "y": 0.48464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (4, 3),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.66008,
                        "y": 0.48464,
                        "page_number": 0,
                    }
                ],
            },
            {
                "index": (4, 4),
                "span": (1, 1),
                "is_column_header": None,
                "is_projected_row_header": None,
                "locations": [
                    {
                        "height": 0.01188,
                        "width": 0.06071,
                        "x": 0.76008,
                        "y": 0.48464,
                        "page_number": 0,
                    }
                ],
            },
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

        expected_tables = {
            "11": (
                "TABLE",
                [
                    ["Kensho Revenue in millions $", "Q1", "Q2", "Q3", "Q4"],
                    ["2025", "500,000", "505,000", "510,000", "520,000"],
                    ["2026", "600,000", "605,000", "610,000", "620,000"],
                    ["2027", "700,000", "705,000", "710,000", "720,000"],
                    ["2028", "800,000", "805,000", "810,000", "820,000"],
                ],
            )
        }

        expected_cell_annotations = {
            "11": [
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
                AnnotationModel(
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
            ]
        }

        tables, table_cell_annotations = build_table_grids(
            {"content_tree": content, "annotations": annotations}, True
        )
        self.assertEqual(expected_tables, tables)
        self.assertEqual(expected_cell_annotations, table_cell_annotations)

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

        expected_tables = {
            "6": (
                "FIGURE_EXTRACTED_TABLE",
                [
                    ["SDFII", "YIUIO", "789"],
                    ["234", "123", "123"],
                    ["12", "789", "123"],
                    ["789", "123", "789"],
                    ["789", "456", "123"],
                    ["123", "123", "234"],
                    ["345", "456", "789"],
                ],
            ),
            "35": (
                "FIGURE_EXTRACTED_TABLE",
                [
                    ["EFG", "ELP", "345"],
                    ["12", "123", "345"],
                    ["321", "123", "123"],
                    ["345", "234", "123"],
                    ["12", "789", "12"],
                    ["123", "789", "910"],
                    ["12", "456", "321"],
                    ["910", "345", "234"],
                ],
            ),
        }

        expected_table_id_to_cell_annotations = {
            "6": [
                AnnotationModel(
                    content_uids=["7"],
                    data=AnnotationDataModel(
                        index=(0, 0),
                        span=(1, 1),
                        value="SDFII",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["8"],
                    data=AnnotationDataModel(
                        index=(0, 1),
                        span=(1, 1),
                        value="YIUIO",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["9"],
                    data=AnnotationDataModel(
                        index=(0, 2),
                        span=(1, 1),
                        value="789",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["10"],
                    data=AnnotationDataModel(
                        index=(1, 0),
                        span=(1, 1),
                        value="234",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["11"],
                    data=AnnotationDataModel(
                        index=(1, 1),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["12"],
                    data=AnnotationDataModel(
                        index=(1, 2),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["13"],
                    data=AnnotationDataModel(
                        index=(2, 0),
                        span=(1, 1),
                        value="12",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["14"],
                    data=AnnotationDataModel(
                        index=(2, 1),
                        span=(1, 1),
                        value="789",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["15"],
                    data=AnnotationDataModel(
                        index=(2, 2),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["16"],
                    data=AnnotationDataModel(
                        index=(3, 0),
                        span=(1, 1),
                        value="789",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["17"],
                    data=AnnotationDataModel(
                        index=(3, 1),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["18"],
                    data=AnnotationDataModel(
                        index=(3, 2),
                        span=(1, 1),
                        value="789",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["19"],
                    data=AnnotationDataModel(
                        index=(4, 0),
                        span=(1, 1),
                        value="789",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["20"],
                    data=AnnotationDataModel(
                        index=(4, 1),
                        span=(1, 1),
                        value="456",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["21"],
                    data=AnnotationDataModel(
                        index=(4, 2),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["22"],
                    data=AnnotationDataModel(
                        index=(5, 0),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["23"],
                    data=AnnotationDataModel(
                        index=(5, 1),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["24"],
                    data=AnnotationDataModel(
                        index=(5, 2),
                        span=(1, 1),
                        value="234",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["25"],
                    data=AnnotationDataModel(
                        index=(6, 0),
                        span=(1, 1),
                        value="345",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["26"],
                    data=AnnotationDataModel(
                        index=(6, 1),
                        span=(1, 1),
                        value="456",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["27"],
                    data=AnnotationDataModel(
                        index=(6, 2),
                        span=(1, 1),
                        value="789",
                        is_column_header=None,
                        is_projected_row_header=None,
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
            "35": [
                AnnotationModel(
                    content_uids=["36"],
                    data=AnnotationDataModel(
                        index=(0, 0),
                        span=(1, 1),
                        value="EFG",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["37"],
                    data=AnnotationDataModel(
                        index=(0, 1),
                        span=(1, 1),
                        value="ELP",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["38"],
                    data=AnnotationDataModel(
                        index=(0, 2),
                        span=(1, 1),
                        value="345",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["39"],
                    data=AnnotationDataModel(
                        index=(1, 0),
                        span=(1, 1),
                        value="12",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["40"],
                    data=AnnotationDataModel(
                        index=(1, 1),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["41"],
                    data=AnnotationDataModel(
                        index=(1, 2),
                        span=(1, 1),
                        value="345",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["42"],
                    data=AnnotationDataModel(
                        index=(2, 0),
                        span=(1, 1),
                        value="321",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["43"],
                    data=AnnotationDataModel(
                        index=(2, 1),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["44"],
                    data=AnnotationDataModel(
                        index=(2, 2),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["45"],
                    data=AnnotationDataModel(
                        index=(3, 0),
                        span=(1, 1),
                        value="345",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["46"],
                    data=AnnotationDataModel(
                        index=(3, 1),
                        span=(1, 1),
                        value="234",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["47"],
                    data=AnnotationDataModel(
                        index=(3, 2),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["48"],
                    data=AnnotationDataModel(
                        index=(4, 0),
                        span=(1, 1),
                        value="12",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["49"],
                    data=AnnotationDataModel(
                        index=(4, 1),
                        span=(1, 1),
                        value="789",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["50"],
                    data=AnnotationDataModel(
                        index=(4, 2),
                        span=(1, 1),
                        value="12",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["51"],
                    data=AnnotationDataModel(
                        index=(5, 0),
                        span=(1, 1),
                        value="123",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["52"],
                    data=AnnotationDataModel(
                        index=(5, 1),
                        span=(1, 1),
                        value="789",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["53"],
                    data=AnnotationDataModel(
                        index=(5, 2),
                        span=(1, 1),
                        value="910",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["54"],
                    data=AnnotationDataModel(
                        index=(6, 0),
                        span=(1, 1),
                        value="12",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["55"],
                    data=AnnotationDataModel(
                        index=(6, 1),
                        span=(1, 1),
                        value="456",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["56"],
                    data=AnnotationDataModel(
                        index=(6, 2),
                        span=(1, 1),
                        value="321",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["57"],
                    data=AnnotationDataModel(
                        index=(7, 0),
                        span=(1, 1),
                        value="910",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["58"],
                    data=AnnotationDataModel(
                        index=(7, 1),
                        span=(1, 1),
                        value="345",
                        is_column_header=None,
                        is_projected_row_header=None,
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
                AnnotationModel(
                    content_uids=["59"],
                    data=AnnotationDataModel(
                        index=(7, 2),
                        span=(1, 1),
                        value="234",
                        is_column_header=None,
                        is_projected_row_header=None,
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
        }
        tables, table_id_to_cell_annotations = build_table_grids(
            {"content_tree": content, "annotations": annotations}, True
        )
        self.assertEqual(expected_tables, tables)
        self.assertEqual(
            expected_table_id_to_cell_annotations, table_id_to_cell_annotations
        )
