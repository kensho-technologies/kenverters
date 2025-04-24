import json
import os
from typing import Any, ClassVar
from unittest import TestCase

from kensho_kenverters.output_to_sections import extract_organized_sections

OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "extract_output.json"
)


class TestMarkdownConversion(TestCase):
    extract_output: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        with open(OUTPUT_FILE_PATH, "r") as f:
            cls.extract_output = json.load(f)
        cls.maxDiff = None

    def test_extract_organized_sections(self) -> None:
        # Example not starting with a title
        expected_sections = [
            [
                {"category": "text", "text": "2019"},
                {"category": "text", "text": "test noise string at top"},
            ],
            [
                {"category": "title", "text": "Generated Toy File Title"},
                {
                    "category": "text",
                    "text": (
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
                },
            ],
            [
                {"category": "title", "text": "ESTIMATE for Kensho"},
                {
                    "category": "table",
                    "table": [
                        ["Kensho Revenue in millions $", "Q1", "Q2", "Q3", "Q4"],
                        ["2020", "100,000", "200,000", "300,000", "400,000"],
                        ["2021", "101,001", "201,001", "301,001", "401,001"],
                        ["2022", "102,004", "202,004", "302,004", "402,004"],
                        ["2023", "103,009", "203,009", "303,009", "403,009"],
                    ],
                    "text": (
                        "\n| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| --- | --- |"
                        " --- | --- | --- |\n| 2020 | 100,000 | "
                        "200,000 | 300,000 | 400,000 |\n| 2021 | 101,001 | 201,001 | 301,001 | "
                        "401,001 |\n"
                        "| 2022 | 102,004 | 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | "
                        "203,009 | "
                        "303,009 | 403,009 |\n"
                    ),
                },
                {
                    "category": "text",
                    "text": (
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
                },
                {"category": "figure", "text": ""},
            ],
            [
                {"category": "title", "text": "Recommendation: BUY"},
                {"category": "text", "text": "42"},
                {"category": "text", "text": "test noise string at bottom"},
                {"category": "text", "text": "999"},
            ],
        ]
        sections = extract_organized_sections(self.extract_output)
        self.assertEqual(sections, expected_sections)

        # Example starting with a title
        output = {
            "annotations": [
                {
                    "content_uids": ["7"],
                    "data": {"index": [0, 0], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.22128,
                            "x": 0.16008,
                            "y": 0.40464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["8"],
                    "data": {"index": [0, 1], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.02241,
                            "x": 0.46007,
                            "y": 0.40464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["9"],
                    "data": {"index": [0, 2], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.02241,
                            "x": 0.56008,
                            "y": 0.40464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["10"],
                    "data": {"index": [0, 3], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.02241,
                            "x": 0.66008,
                            "y": 0.40464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["11"],
                    "data": {"index": [0, 4], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.02241,
                            "x": 0.76008,
                            "y": 0.40464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["12"],
                    "data": {"index": [1, 0], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.03736,
                            "x": 0.16008,
                            "y": 0.42464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["13"],
                    "data": {"index": [1, 1], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.46007,
                            "y": 0.42464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["14"],
                    "data": {"index": [1, 2], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.56008,
                            "y": 0.42464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["15"],
                    "data": {"index": [1, 3], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.66008,
                            "y": 0.42464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["16"],
                    "data": {"index": [1, 4], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.76008,
                            "y": 0.42464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["17"],
                    "data": {"index": [2, 0], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.03736,
                            "x": 0.16008,
                            "y": 0.44464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["18"],
                    "data": {"index": [2, 1], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.46007,
                            "y": 0.44464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["19"],
                    "data": {"index": [2, 2], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.56008,
                            "y": 0.44464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["20"],
                    "data": {"index": [2, 3], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.66008,
                            "y": 0.44464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["21"],
                    "data": {"index": [2, 4], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.76008,
                            "y": 0.44464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["22"],
                    "data": {"index": [3, 0], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.03736,
                            "x": 0.16008,
                            "y": 0.46465,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["23"],
                    "data": {"index": [3, 1], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.46007,
                            "y": 0.46465,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["24"],
                    "data": {"index": [3, 2], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.56008,
                            "y": 0.46465,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["25"],
                    "data": {"index": [3, 3], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.66008,
                            "y": 0.46465,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["26"],
                    "data": {"index": [3, 4], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.76008,
                            "y": 0.46465,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["27"],
                    "data": {"index": [4, 0], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.03736,
                            "x": 0.16008,
                            "y": 0.48464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["28"],
                    "data": {"index": [4, 1], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.46007,
                            "y": 0.48464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["29"],
                    "data": {"index": [4, 2], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.56008,
                            "y": 0.48464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["30"],
                    "data": {"index": [4, 3], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.66008,
                            "y": 0.48464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["31"],
                    "data": {"index": [4, 4], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.76008,
                            "y": 0.48464,
                        }
                    ],
                    "type": "table_structure",
                },
            ],
            "content_tree": {
                "children": [
                    {
                        "children": [],
                        "content": "Generated Toy File Title",
                        "locations": [
                            {
                                "height": 0.02376,
                                "page_number": 0,
                                "width": 0.35368,
                                "x": 0.32316,
                                "y": 0.0564,
                            }
                        ],
                        "type": "TITLE",
                        "uid": "3",
                    },
                    {
                        "children": [],
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
                        "locations": [
                            {
                                "height": 0.16867,
                                "page_number": 0,
                                "width": 0.8,
                                "x": 0.1,
                                "y": 0.10141,
                            }
                        ],
                        "type": "TEXT",
                        "uid": "4",
                    },
                    {
                        "children": [],
                        "content": "ESTIMATE for Kensho",
                        "locations": [
                            {
                                "height": 0.01425,
                                "page_number": 0,
                                "width": 0.21953,
                                "x": 0.3,
                                "y": 0.36869,
                            }
                        ],
                        "type": "TITLE",
                        "uid": "5",
                    },
                    {
                        "children": [
                            {
                                "children": [],
                                "content": "Kensho Revenue in millions $",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.22128,
                                        "x": 0.16008,
                                        "y": 0.40464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "7",
                            },
                            {
                                "children": [],
                                "content": "Q1",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.02241,
                                        "x": 0.46007,
                                        "y": 0.40464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "8",
                            },
                            {
                                "children": [],
                                "content": "Q2",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.02241,
                                        "x": 0.56008,
                                        "y": 0.40464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "9",
                            },
                            {
                                "children": [],
                                "content": "Q3",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.02241,
                                        "x": 0.66008,
                                        "y": 0.40464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "10",
                            },
                            {
                                "children": [],
                                "content": "Q4",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.02241,
                                        "x": 0.76008,
                                        "y": 0.40464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "11",
                            },
                            {
                                "children": [],
                                "content": "2020",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.03736,
                                        "x": 0.16008,
                                        "y": 0.42464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "12",
                            },
                            {
                                "children": [],
                                "content": "100,000",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.46007,
                                        "y": 0.42464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "13",
                            },
                            {
                                "children": [],
                                "content": "200,000",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.56008,
                                        "y": 0.42464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "14",
                            },
                            {
                                "children": [],
                                "content": "300,000",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.66008,
                                        "y": 0.42464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "15",
                            },
                            {
                                "children": [],
                                "content": "400,000",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.76008,
                                        "y": 0.42464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "16",
                            },
                            {
                                "children": [],
                                "content": "2021",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.03736,
                                        "x": 0.16008,
                                        "y": 0.44464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "17",
                            },
                            {
                                "children": [],
                                "content": "101,001",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.46007,
                                        "y": 0.44464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "18",
                            },
                            {
                                "children": [],
                                "content": "201,001",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.56008,
                                        "y": 0.44464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "19",
                            },
                            {
                                "children": [],
                                "content": "301,001",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.66008,
                                        "y": 0.44464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "20",
                            },
                            {
                                "children": [],
                                "content": "401,001",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.76008,
                                        "y": 0.44464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "21",
                            },
                            {
                                "children": [],
                                "content": "2022",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.03736,
                                        "x": 0.16008,
                                        "y": 0.46465,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "22",
                            },
                            {
                                "children": [],
                                "content": "102,004",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.46007,
                                        "y": 0.46465,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "23",
                            },
                            {
                                "children": [],
                                "content": "202,004",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.56008,
                                        "y": 0.46465,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "24",
                            },
                            {
                                "children": [],
                                "content": "302,004",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.66008,
                                        "y": 0.46465,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "25",
                            },
                            {
                                "children": [],
                                "content": "402,004",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.76008,
                                        "y": 0.46465,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "26",
                            },
                            {
                                "children": [],
                                "content": "2023",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.03736,
                                        "x": 0.16008,
                                        "y": 0.48464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "27",
                            },
                            {
                                "children": [],
                                "content": "103,009",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.46007,
                                        "y": 0.48464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "28",
                            },
                            {
                                "children": [],
                                "content": "203,009",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.56008,
                                        "y": 0.48464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "29",
                            },
                            {
                                "children": [],
                                "content": "303,009",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.66008,
                                        "y": 0.48464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "30",
                            },
                            {
                                "children": [],
                                "content": "403,009",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.76008,
                                        "y": 0.48464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "31",
                            },
                        ],
                        "content": None,
                        "locations": [
                            {
                                "height": 0.09188,
                                "page_number": 0,
                                "width": 0.66072,
                                "x": 0.16008,
                                "y": 0.40464,
                            }
                        ],
                        "type": "TABLE",
                        "uid": "6",
                    },
                    {
                        "children": [],
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
                        "locations": [
                            {
                                "height": 0.16867,
                                "page_number": 0,
                                "width": 0.8,
                                "x": 0.1,
                                "y": 0.58142,
                            }
                        ],
                        "type": "TEXT",
                        "uid": "32",
                    },
                    {
                        "children": [],
                        "content": None,
                        "locations": [
                            {
                                "height": 0.01425,
                                "page_number": 0,
                                "width": 0.21622,
                                "x": 0.60002,
                                "y": 0.8388,
                            }
                        ],
                        "type": "FIGURE",
                        "uid": "33",
                    },
                    {
                        "children": [],
                        "content": "Recommendation: BUY",
                        "locations": [
                            {
                                "height": 0.01425,
                                "page_number": 0,
                                "width": 0.21622,
                                "x": 0.60001,
                                "y": 0.8387,
                            }
                        ],
                        "type": "TITLE",
                        "uid": "34",
                    },
                    {
                        "children": [],
                        "content": "42",
                        "locations": [
                            {
                                "height": 0.01425,
                                "page_number": 0,
                                "width": 0.02802,
                                "x": 0.1,
                                "y": 0.9637,
                            }
                        ],
                        "type": "TEXT",
                        "uid": "35",
                    },
                    {
                        "children": [],
                        "content": "test noise string at bottom",
                        "locations": [
                            {
                                "height": 0.01425,
                                "page_number": 0,
                                "width": 0.23641,
                                "x": 0.17286,
                                "y": 0.9637,
                            }
                        ],
                        "type": "TEXT",
                        "uid": "36",
                    },
                    {
                        "children": [],
                        "content": "999",
                        "locations": [
                            {
                                "height": 0.01425,
                                "page_number": 0,
                                "width": 0.03923,
                                "x": 0.8,
                                "y": 0.9637,
                            }
                        ],
                        "type": "TEXT",
                        "uid": "37",
                    },
                ],
                "content": None,
                "locations": None,
                "type": "DOCUMENT",
                "uid": "0",
            },
        }
        sections = extract_organized_sections(output)
        self.assertEqual(sections, expected_sections[1:])

        # Example ending with a title
        output = {
            "annotations": [
                {
                    "content_uids": ["7"],
                    "data": {"index": [0, 0], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.22128,
                            "x": 0.16008,
                            "y": 0.40464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["8"],
                    "data": {"index": [0, 1], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.02241,
                            "x": 0.46007,
                            "y": 0.40464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["9"],
                    "data": {"index": [0, 2], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.02241,
                            "x": 0.56008,
                            "y": 0.40464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["10"],
                    "data": {"index": [0, 3], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.02241,
                            "x": 0.66008,
                            "y": 0.40464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["11"],
                    "data": {"index": [0, 4], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.02241,
                            "x": 0.76008,
                            "y": 0.40464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["12"],
                    "data": {"index": [1, 0], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.03736,
                            "x": 0.16008,
                            "y": 0.42464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["13"],
                    "data": {"index": [1, 1], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.46007,
                            "y": 0.42464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["14"],
                    "data": {"index": [1, 2], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.56008,
                            "y": 0.42464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["15"],
                    "data": {"index": [1, 3], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.66008,
                            "y": 0.42464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["16"],
                    "data": {"index": [1, 4], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.76008,
                            "y": 0.42464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["17"],
                    "data": {"index": [2, 0], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.03736,
                            "x": 0.16008,
                            "y": 0.44464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["18"],
                    "data": {"index": [2, 1], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.46007,
                            "y": 0.44464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["19"],
                    "data": {"index": [2, 2], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.56008,
                            "y": 0.44464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["20"],
                    "data": {"index": [2, 3], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.66008,
                            "y": 0.44464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["21"],
                    "data": {"index": [2, 4], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.76008,
                            "y": 0.44464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["22"],
                    "data": {"index": [3, 0], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.03736,
                            "x": 0.16008,
                            "y": 0.46465,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["23"],
                    "data": {"index": [3, 1], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.46007,
                            "y": 0.46465,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["24"],
                    "data": {"index": [3, 2], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.56008,
                            "y": 0.46465,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["25"],
                    "data": {"index": [3, 3], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.66008,
                            "y": 0.46465,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["26"],
                    "data": {"index": [3, 4], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.76008,
                            "y": 0.46465,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["27"],
                    "data": {"index": [4, 0], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.03736,
                            "x": 0.16008,
                            "y": 0.48464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["28"],
                    "data": {"index": [4, 1], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.46007,
                            "y": 0.48464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["29"],
                    "data": {"index": [4, 2], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.56008,
                            "y": 0.48464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["30"],
                    "data": {"index": [4, 3], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.66008,
                            "y": 0.48464,
                        }
                    ],
                    "type": "table_structure",
                },
                {
                    "content_uids": ["31"],
                    "data": {"index": [4, 4], "span": [1, 1]},
                    "locations": [
                        {
                            "height": 0.01188,
                            "page_number": 0,
                            "width": 0.06071,
                            "x": 0.76008,
                            "y": 0.48464,
                        }
                    ],
                    "type": "table_structure",
                },
            ],
            "content_tree": {
                "children": [
                    {
                        "children": [],
                        "content": "Generated Toy File Title",
                        "locations": [
                            {
                                "height": 0.02376,
                                "page_number": 0,
                                "width": 0.35368,
                                "x": 0.32316,
                                "y": 0.0564,
                            }
                        ],
                        "type": "TITLE",
                        "uid": "3",
                    },
                    {
                        "children": [],
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
                        "locations": [
                            {
                                "height": 0.16867,
                                "page_number": 0,
                                "width": 0.8,
                                "x": 0.1,
                                "y": 0.10141,
                            }
                        ],
                        "type": "TEXT",
                        "uid": "4",
                    },
                    {
                        "children": [],
                        "content": "ESTIMATE for Kensho",
                        "locations": [
                            {
                                "height": 0.01425,
                                "page_number": 0,
                                "width": 0.21953,
                                "x": 0.3,
                                "y": 0.36869,
                            }
                        ],
                        "type": "TITLE",
                        "uid": "5",
                    },
                    {
                        "children": [
                            {
                                "children": [],
                                "content": "Kensho Revenue in millions $",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.22128,
                                        "x": 0.16008,
                                        "y": 0.40464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "7",
                            },
                            {
                                "children": [],
                                "content": "Q1",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.02241,
                                        "x": 0.46007,
                                        "y": 0.40464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "8",
                            },
                            {
                                "children": [],
                                "content": "Q2",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.02241,
                                        "x": 0.56008,
                                        "y": 0.40464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "9",
                            },
                            {
                                "children": [],
                                "content": "Q3",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.02241,
                                        "x": 0.66008,
                                        "y": 0.40464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "10",
                            },
                            {
                                "children": [],
                                "content": "Q4",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.02241,
                                        "x": 0.76008,
                                        "y": 0.40464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "11",
                            },
                            {
                                "children": [],
                                "content": "2020",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.03736,
                                        "x": 0.16008,
                                        "y": 0.42464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "12",
                            },
                            {
                                "children": [],
                                "content": "100,000",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.46007,
                                        "y": 0.42464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "13",
                            },
                            {
                                "children": [],
                                "content": "200,000",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.56008,
                                        "y": 0.42464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "14",
                            },
                            {
                                "children": [],
                                "content": "300,000",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.66008,
                                        "y": 0.42464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "15",
                            },
                            {
                                "children": [],
                                "content": "400,000",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.76008,
                                        "y": 0.42464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "16",
                            },
                            {
                                "children": [],
                                "content": "2021",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.03736,
                                        "x": 0.16008,
                                        "y": 0.44464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "17",
                            },
                            {
                                "children": [],
                                "content": "101,001",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.46007,
                                        "y": 0.44464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "18",
                            },
                            {
                                "children": [],
                                "content": "201,001",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.56008,
                                        "y": 0.44464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "19",
                            },
                            {
                                "children": [],
                                "content": "301,001",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.66008,
                                        "y": 0.44464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "20",
                            },
                            {
                                "children": [],
                                "content": "401,001",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.76008,
                                        "y": 0.44464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "21",
                            },
                            {
                                "children": [],
                                "content": "2022",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.03736,
                                        "x": 0.16008,
                                        "y": 0.46465,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "22",
                            },
                            {
                                "children": [],
                                "content": "102,004",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.46007,
                                        "y": 0.46465,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "23",
                            },
                            {
                                "children": [],
                                "content": "202,004",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.56008,
                                        "y": 0.46465,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "24",
                            },
                            {
                                "children": [],
                                "content": "302,004",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.66008,
                                        "y": 0.46465,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "25",
                            },
                            {
                                "children": [],
                                "content": "402,004",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.76008,
                                        "y": 0.46465,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "26",
                            },
                            {
                                "children": [],
                                "content": "2023",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.03736,
                                        "x": 0.16008,
                                        "y": 0.48464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "27",
                            },
                            {
                                "children": [],
                                "content": "103,009",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.46007,
                                        "y": 0.48464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "28",
                            },
                            {
                                "children": [],
                                "content": "203,009",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.56008,
                                        "y": 0.48464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "29",
                            },
                            {
                                "children": [],
                                "content": "303,009",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.66008,
                                        "y": 0.48464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "30",
                            },
                            {
                                "children": [],
                                "content": "403,009",
                                "locations": [
                                    {
                                        "height": 0.01188,
                                        "page_number": 0,
                                        "width": 0.06071,
                                        "x": 0.76008,
                                        "y": 0.48464,
                                    }
                                ],
                                "type": "TABLE_CELL",
                                "uid": "31",
                            },
                        ],
                        "content": None,
                        "locations": [
                            {
                                "height": 0.09188,
                                "page_number": 0,
                                "width": 0.66072,
                                "x": 0.16008,
                                "y": 0.40464,
                            }
                        ],
                        "type": "TABLE",
                        "uid": "6",
                    },
                    {
                        "children": [],
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
                        "locations": [
                            {
                                "height": 0.16867,
                                "page_number": 0,
                                "width": 0.8,
                                "x": 0.1,
                                "y": 0.58142,
                            }
                        ],
                        "type": "TEXT",
                        "uid": "32",
                    },
                    {
                        "children": [],
                        "content": None,
                        "locations": [
                            {
                                "height": 0.01425,
                                "page_number": 0,
                                "width": 0.21622,
                                "x": 0.60002,
                                "y": 0.8388,
                            }
                        ],
                        "type": "FIGURE",
                        "uid": "333",
                    },
                    {
                        "children": [],
                        "content": "Recommendation: BUY",
                        "locations": [
                            {
                                "height": 0.01425,
                                "page_number": 0,
                                "width": 0.21622,
                                "x": 0.60001,
                                "y": 0.8387,
                            }
                        ],
                        "type": "TITLE",
                        "uid": "33",
                    },
                ],
                "content": None,
                "locations": None,
                "type": "DOCUMENT",
                "uid": "0",
            },
        }
        sections = extract_organized_sections(output)
        expected_sections = [
            [
                {"category": "title", "text": "Generated Toy File Title"},
                {
                    "category": "text",
                    "text": (
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
                },
            ],
            [
                {"category": "title", "text": "ESTIMATE for Kensho"},
                {
                    "category": "table",
                    "table": [
                        ["Kensho Revenue in millions $", "Q1", "Q2", "Q3", "Q4"],
                        ["2020", "100,000", "200,000", "300,000", "400,000"],
                        ["2021", "101,001", "201,001", "301,001", "401,001"],
                        ["2022", "102,004", "202,004", "302,004", "402,004"],
                        ["2023", "103,009", "203,009", "303,009", "403,009"],
                    ],
                    "text": "\n| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| "
                    "--- | --- | --- | --- | --- |\n| 2020 | "
                    "100,000 | "
                    "200,000 | 300,000 | 400,000 |\n| 2021 | 101,001 | 201,001 | 301,001 | "
                    "401,001 |\n"
                    "| 2022 | 102,004 | 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | "
                    "203,009 | "
                    "303,009 | 403,009 |\n",
                },
                {
                    "category": "text",
                    "text": (
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
                },
                {"category": "figure", "text": ""},
            ],
            [{"category": "title", "text": "Recommendation: BUY"}],
        ]
        self.assertEqual(sections, expected_sections)
