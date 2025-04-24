import json
import os
from typing import Any, ClassVar
from unittest import TestCase

from kensho_kenverters.output_to_tables import (
    build_table_grids,
    extract_pd_dfs_from_output,
    extract_pd_dfs_with_locs_from_output,
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
        tables = extract_pd_dfs_with_locs_from_output(self.extract_output)
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
            "uid": "0",
            "type": "DOCUMENT",
            "content": None,
            "children": [
                {
                    "uid": "1",
                    "type": "TEXT",
                    "content": "2019",
                    "children": [],
                    "locations": [
                        {
                            "height": 0.01425,
                            "width": 0.05043,
                            "x": 0.20001,
                            "y": 0.0137,
                            "page_number": 0,
                        }
                    ],
                },
                {
                    "uid": "2",
                    "type": "TEXT",
                    "content": "test noise string at top",
                    "children": [],
                    "locations": [
                        {
                            "height": 0.01425,
                            "width": 0.20281,
                            "x": 0.29527,
                            "y": 0.0137,
                            "page_number": 0,
                        }
                    ],
                },
                {
                    "uid": "3",
                    "type": "TITLE",
                    "content": "Generated Toy File Title",
                    "children": [],
                    "locations": [
                        {
                            "height": 0.02376,
                            "width": 0.35368,
                            "x": 0.32316,
                            "y": 0.0564,
                            "page_number": 0,
                        }
                    ],
                },
                {
                    "uid": "4",
                    "type": "TEXT",
                    "content": (
                        "Machine learning (ML) is the scientific study of algorithms "
                        "and statistical models that computer systems use in order to"
                        " perform a specific task effectively without using explicit "
                        "instructions, relying on patterns and inference instead. It "
                        "is seen as a subset of artificial intelligence. Machine lear"
                        "ning algorithms build a mathematical model based on sample d"
                        "ata, known as training data, in order to make predictions or"
                        " decisions without being explicitly programmed to perform th"
                        "e task. Valerie is awesome. Machine learning algorithms are "
                        "used in a wide variety of applications, such as email filter"
                        "ing, and computer vision, where it is infeasible to develop "
                        "an algorithm of specific instructions for performing the tas"
                        "k. Machine learning is closely related to computational stat"
                        "istics, which focuses on making predictions using computers."
                        " The study of mathematical optimization delivers methods, th"
                        "eory and application domains to the field of machine learnin"
                        "g. Data mining is a field of study within machine learning, "
                        "and focuses on exploratory data analysis through unsupervise"
                        "d learning. In its application across business problems, mac"
                        "hine learning is also referred to as predictive analytics."
                    ),
                    "children": [],
                    "locations": [
                        {
                            "height": 0.16867,
                            "width": 0.8,
                            "x": 0.1,
                            "y": 0.10141,
                            "page_number": 0,
                        }
                    ],
                },
                {
                    "uid": "5",
                    "type": "TITLE",
                    "content": "ESTIMATE for Kensho",
                    "children": [],
                    "locations": [
                        {
                            "height": 0.01425,
                            "width": 0.21953,
                            "x": 0.3,
                            "y": 0.36869,
                            "page_number": 0,
                        }
                    ],
                },
                {
                    "uid": "6",
                    "type": "TABLE",
                    "content": None,
                    "children": [
                        {
                            "uid": "7",
                            "type": "TABLE_CELL",
                            "content": "Kensho Revenue in millions $",
                            "children": [],
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
                            "uid": "8",
                            "type": "TABLE_CELL",
                            "content": "Q1",
                            "children": [],
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
                            "uid": "9",
                            "type": "TABLE_CELL",
                            "content": "Q2",
                            "children": [],
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
                            "uid": "10",
                            "type": "TABLE_CELL",
                            "content": "Q3",
                            "children": [],
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
                            "uid": "11",
                            "type": "TABLE_CELL",
                            "content": "Q4",
                            "children": [],
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
                            "uid": "12",
                            "type": "TABLE_CELL",
                            "content": "2020",
                            "children": [],
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
                            "uid": "13",
                            "type": "TABLE_CELL",
                            "content": "100,000",
                            "children": [],
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
                            "uid": "14",
                            "type": "TABLE_CELL",
                            "content": "200,000",
                            "children": [],
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
                            "uid": "15",
                            "type": "TABLE_CELL",
                            "content": "300,000",
                            "children": [],
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
                            "uid": "16",
                            "type": "TABLE_CELL",
                            "content": "400,000",
                            "children": [],
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
                            "uid": "17",
                            "type": "TABLE_CELL",
                            "content": "2021",
                            "children": [],
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
                            "uid": "18",
                            "type": "TABLE_CELL",
                            "content": "101,001",
                            "children": [],
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
                            "uid": "19",
                            "type": "TABLE_CELL",
                            "content": "201,001",
                            "children": [],
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
                            "uid": "20",
                            "type": "TABLE_CELL",
                            "content": "301,001",
                            "children": [],
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
                            "uid": "21",
                            "type": "TABLE_CELL",
                            "content": "401,001",
                            "children": [],
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
                            "uid": "22",
                            "type": "TABLE_CELL",
                            "content": "2022",
                            "children": [],
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
                            "uid": "23",
                            "type": "TABLE_CELL",
                            "content": "102,004",
                            "children": [],
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
                            "uid": "24",
                            "type": "TABLE_CELL",
                            "content": "202,004",
                            "children": [],
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
                            "uid": "25",
                            "type": "TABLE_CELL",
                            "content": "302,004",
                            "children": [],
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
                            "uid": "26",
                            "type": "TABLE_CELL",
                            "content": "402,004",
                            "children": [],
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
                            "uid": "27",
                            "type": "TABLE_CELL",
                            "content": "2023",
                            "children": [],
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
                            "uid": "28",
                            "type": "TABLE_CELL",
                            "content": "103,009",
                            "children": [],
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
                            "uid": "29",
                            "type": "TABLE_CELL",
                            "content": "203,009",
                            "children": [],
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
                            "uid": "30",
                            "type": "TABLE_CELL",
                            "content": "303,009",
                            "children": [],
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
                    ],
                    "locations": [
                        {
                            "height": 0.09188,
                            "width": 0.66072,
                            "x": 0.16008,
                            "y": 0.40464,
                            "page_number": 0,
                        }
                    ],
                },
                {
                    "uid": "32",
                    "type": "TEXT",
                    "content": (
                        "Machine learning (ML) is the scientific study of algorithms "
                        "and statistical models that computer systems use in order to"
                        " perform a specific task effectively without using explicit "
                        "instructions, relying on patterns and inference instead. It "
                        "is seen as a subset of artificial intelligence. Machine lear"
                        "ning algorithms build a mathematical model based on sample d"
                        "ata, known as training data, in order to make predictions or"
                        " decisions without being explicitly programmed to perform th"
                        "e task. Valerie is awesome. Machine learning algorithms are "
                        "used in a wide variety of applications, such as email filter"
                        "ing, and computer vision, where it is infeasible to develop "
                        "an algorithm of specific instructions for performing the tas"
                        "k. Machine learning is closely related to computational stat"
                        "istics, which focuses on making predictions using computers."
                        " The study of mathematical optimization delivers methods, th"
                        "eory and application domains to the field of machine learnin"
                        "g. Data mining is a field of study within machine learning, "
                        "and focuses on exploratory data analysis through unsupervise"
                        "d learning. In its application across business problems, mac"
                        "hine learning is also referred to as predictive analytics."
                    ),
                    "children": [],
                    "locations": [
                        {
                            "height": 0.16867,
                            "width": 0.8,
                            "x": 0.1,
                            "y": 0.58142,
                            "page_number": 0,
                        }
                    ],
                },
                {
                    "uid": "33",
                    "type": "TITLE",
                    "content": "Recommendation: BUY",
                    "children": [],
                    "locations": [
                        {
                            "height": 0.01425,
                            "width": 0.21622,
                            "x": 0.60001,
                            "y": 0.8387,
                            "page_number": 0,
                        }
                    ],
                },
                {
                    "uid": "34",
                    "type": "TEXT",
                    "content": "42",
                    "children": [],
                    "locations": [
                        {
                            "height": 0.01425,
                            "width": 0.02802,
                            "x": 0.1,
                            "y": 0.9637,
                            "page_number": 0,
                        }
                    ],
                },
                {
                    "uid": "35",
                    "type": "TEXT",
                    "content": "test noise string at bottom",
                    "children": [],
                    "locations": [
                        {
                            "height": 0.01425,
                            "width": 0.23641,
                            "x": 0.17286,
                            "y": 0.9637,
                            "page_number": 0,
                        }
                    ],
                },
                {
                    "uid": "36",
                    "type": "TEXT",
                    "content": "999",
                    "children": [],
                    "locations": [
                        {
                            "height": 0.01425,
                            "width": 0.03923,
                            "x": 0.8,
                            "y": 0.9637,
                            "page_number": 0,
                        }
                    ],
                },
            ],
            "locations": None,
        }
        annotations = [
            {
                "content_uids": ["7"],
                "data": {"index": (0, 0), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["8"],
                "data": {"index": (0, 1), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["9"],
                "data": {"index": (0, 2), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["10"],
                "data": {"index": (0, 3), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["11"],
                "data": {"index": (0, 4), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["12"],
                "data": {"index": (1, 0), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["13"],
                "data": {"index": (1, 1), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["14"],
                "data": {"index": (1, 2), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["15"],
                "data": {"index": (1, 3), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["16"],
                "data": {"index": (1, 4), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["17"],
                "data": {"index": (2, 0), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["18"],
                "data": {"index": (2, 1), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["19"],
                "data": {"index": (2, 2), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["20"],
                "data": {"index": (2, 3), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["21"],
                "data": {"index": (2, 4), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["22"],
                "data": {"index": (3, 0), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["23"],
                "data": {"index": (3, 1), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["24"],
                "data": {"index": (3, 2), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["25"],
                "data": {"index": (3, 3), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["26"],
                "data": {"index": (3, 4), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["27"],
                "data": {"index": (4, 0), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["28"],
                "data": {"index": (4, 1), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["29"],
                "data": {"index": (4, 2), "span": (1, 1)},
                "type": "table_structure",
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
                "content_uids": ["30"],
                "data": {"index": (4, 3), "span": (1, 2)},
                "type": "table_structure",
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
        ]

        expected_tables = {
            "6": (
                "TABLE",
                [
                    ["Kensho Revenue in millions $", "Q1", "Q2", "Q3", "Q4"],
                    ["2020", "100,000", "200,000", "300,000", "400,000"],
                    ["2021", "101,001", "201,001", "301,001", "401,001"],
                    ["2022", "102,004", "202,004", "302,004", "402,004"],
                    ["2023", "103,009", "203,009", "303,009", "303,009"],
                ],
            )
        }
        tables = build_table_grids(
            {"content_tree": content, "annotations": annotations}, True
        )
        self.assertEqual(expected_tables, tables)

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

        tables = build_table_grids(
            {"content_tree": content, "annotations": annotations}, True
        )
        self.assertEqual(expected_tables, tables)
