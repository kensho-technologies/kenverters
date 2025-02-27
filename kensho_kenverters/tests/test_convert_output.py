import json
import os
from typing import Any, ClassVar
from unittest import TestCase

from kensho_kenverters.convert_output import (
    _construct_table_from_cells,
    convert_output_to_items_list,
    convert_output_to_markdown,
    convert_output_to_markdown_by_page,
    convert_output_to_str,
    convert_output_to_str_by_page,
    table_to_markdown,
)
from kensho_kenverters.extract_output_models import ContentModel, LocationModel

OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "extract_output.json"
)
HIERARCHICAL_OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "extract_output_hierarchical.json"
)
HIERARCHICAL_v2_OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "extract_output_hierarchical_v2.json"
)
MULTI_PAGE_OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "output_multi_page_locs.json"
)
OUTPUT_NO_LOCS_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "extract_output_no_locs.json"
)
OUTPUT_CHAR_OFFSETS_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "extract_output_char_offsets.json"
)


class TestMarkdownConversion(TestCase):
    extract_output: ClassVar[dict[str, Any]]
    extract_output_hierarchical: ClassVar[dict[str, Any]]
    extract_output_multi_page: ClassVar[dict[str, Any]]
    extract_output_no_locs: ClassVar[dict[str, Any]]
    extract_output_char_offsets: ClassVar[dict[str, Any]]
    extract_output_hierarchical_v2: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        with open(OUTPUT_FILE_PATH, "r") as f:
            cls.extract_output = json.load(f)
        with open(HIERARCHICAL_OUTPUT_FILE_PATH, "r") as f:
            cls.extract_output_hierarchical = json.load(f)
        with open(HIERARCHICAL_v2_OUTPUT_FILE_PATH, "r") as f:
            cls.extract_output_hierarchical_v2 = json.load(f)
        with open(MULTI_PAGE_OUTPUT_FILE_PATH, "r") as f:
            cls.extract_output_multi_page = json.load(f)
        with open(OUTPUT_NO_LOCS_FILE_PATH, "r") as f:
            cls.extract_output_no_locs = json.load(f)
        with open(OUTPUT_CHAR_OFFSETS_FILE_PATH, "r") as f:
            cls.extract_output_char_offsets = json.load(f)

    def test_convert_output_to_items(self) -> None:
        expected_list = [
            {"category": "text", "text": "2019"},
            {"category": "text", "text": "test noise string at top"},
            {"category": "title", "text": "Generated Toy File Title"},
            {
                "category": "text",
                "text": "Machine learning (ML) is the scientific study of algorithms and "
                "statistical models that computer systems use in order to perform a specific "
                "task effectively without using explicit instructions, relying on patterns and "
                "inference instead. It is seen as a subset of artificial intelligence. Machine "
                "learning algorithms build a mathematical model based on sample data, known as "
                "training data, in order to make predictions or decisions without being explicitly"
                " programmed to perform the task. Valerie is awesome. Machine learning algorithms "
                "are used in a wide variety of applications, such as email filtering, and computer"
                " vision, where it is infeasible to develop an algorithm of specific instructions "
                "for performing the task. Machine learning is closely related to computational "
                "statistics, which focuses on making predictions using computers. The study of "
                "mathematical optimization delivers methods, theory and application domains to "
                "the field of machine learning. Data mining is a field of study within machine "
                "learning, and focuses on exploratory data analysis through unsupervised learning."
                " In its application across business problems, machine learning is also referred "
                "to as predictive analytics.",
            },
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
                "text": "| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| --- | --- | --- |"
                " --- | --- |\n| 2020 | 100,000 | "
                "200,000 | 300,000 | 400,000 |\n| 2021 | 101,001 | 201,001 | 301,001 | 401,001 |\n"
                "| 2022 | 102,004 | 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | 203,009 | "
                "303,009 | 403,009 |\n",
            },
            {
                "category": "text",
                "text": "Machine learning (ML) is the scientific study of algorithms and "
                "statistical models that computer systems use in order to perform a specific "
                "task effectively without using explicit instructions, relying on patterns and "
                "inference instead. It is seen as a subset of artificial intelligence. Machine "
                "learning algorithms build a mathematical model based on sample data, known as "
                "training data, in order to make predictions or decisions without being explicitly"
                " programmed to perform the task. Valerie is awesome. Machine learning algorithms "
                "are used in a wide variety of applications, such as email filtering, and computer"
                " vision, where it is infeasible to develop an algorithm of specific instructions "
                "for performing the task. Machine learning is closely related to computational "
                "statistics, which focuses on making predictions using computers. The study of "
                "mathematical optimization delivers methods, theory and application domains to "
                "the field of machine learning. Data mining is a field of study within machine "
                "learning, and focuses on exploratory data analysis through unsupervised learning."
                " In its application across business problems, machine learning is also referred "
                "to as predictive analytics.",
            },
            {"category": "title", "text": "Recommendation: BUY"},
            {"category": "text", "text": "42"},
            {"category": "text", "text": "test noise string at bottom"},
            {"category": "text", "text": "999"},
        ]
        output_list = convert_output_to_items_list(self.extract_output)
        self.assertEqual(expected_list, output_list)

        # With locations
        expected_list_with_locs = [
            {
                "category": "text",
                "text": "2019",
                "locations": [
                    LocationModel(
                        height=0.01425,
                        width=0.05043,
                        x=0.20001,
                        y=0.0137,
                        page_number=0,
                    )
                ],
            },
            {
                "category": "text",
                "text": "test noise string at top",
                "locations": [
                    LocationModel(
                        height=0.01425,
                        width=0.20281,
                        x=0.29527,
                        y=0.0137,
                        page_number=0,
                    )
                ],
            },
            {
                "category": "title",
                "text": "Generated Toy File Title",
                "locations": [
                    LocationModel(
                        height=0.02376,
                        width=0.35368,
                        x=0.32316,
                        y=0.0564,
                        page_number=0,
                    )
                ],
            },
            {
                "category": "text",
                "text": "Machine learning (ML) is the scientific study of algorithms and "
                "statistical models that computer systems use in order to perform a specific "
                "task effectively without using explicit instructions, relying on patterns and "
                "inference instead. It is seen as a subset of artificial intelligence. Machine "
                "learning algorithms build a mathematical model based on sample data, known as "
                "training data, in order to make predictions or decisions without being explicitly"
                " programmed to perform the task. Valerie is awesome. Machine learning algorithms "
                "are used in a wide variety of applications, such as email filtering, and computer"
                " vision, where it is infeasible to develop an algorithm of specific instructions "
                "for performing the task. Machine learning is closely related to computational "
                "statistics, which focuses on making predictions using computers. The study of "
                "mathematical optimization delivers methods, theory and application domains to "
                "the field of machine learning. Data mining is a field of study within machine "
                "learning, and focuses on exploratory data analysis through unsupervised learning."
                " In its application across business problems, machine learning is also referred "
                "to as predictive analytics.",
                "locations": [
                    LocationModel(
                        height=0.16867, width=0.8, x=0.1, y=0.10141, page_number=0
                    )
                ],
            },
            {
                "category": "title",
                "text": "ESTIMATE for Kensho",
                "locations": [
                    LocationModel(
                        height=0.01425, width=0.21953, x=0.3, y=0.36869, page_number=0
                    )
                ],
            },
            {
                "category": "table",
                "table": [
                    ["Kensho Revenue in millions $", "Q1", "Q2", "Q3", "Q4"],
                    ["2020", "100,000", "200,000", "300,000", "400,000"],
                    ["2021", "101,001", "201,001", "301,001", "401,001"],
                    ["2022", "102,004", "202,004", "302,004", "402,004"],
                    ["2023", "103,009", "203,009", "303,009", "403,009"],
                ],
                "text": "| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| --- | --- | --- |"
                " --- | --- |\n| 2020 | 100,000 | "
                "200,000 | 300,000 | 400,000 |\n| 2021 | 101,001 | 201,001 | 301,001 | 401,001 |\n"
                "| 2022 | 102,004 | 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | 203,009 | "
                "303,009 | 403,009 |\n",
                "locations": [
                    LocationModel(
                        height=0.09188,
                        width=0.66072,
                        x=0.16008,
                        y=0.40464,
                        page_number=0,
                    )
                ],
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
                "locations": [
                    LocationModel(
                        height=0.16867, width=0.8, x=0.1, y=0.58142, page_number=0
                    )
                ],
            },
            {
                "category": "title",
                "text": "Recommendation: BUY",
                "locations": [
                    LocationModel(
                        height=0.01425,
                        width=0.21622,
                        x=0.60001,
                        y=0.8387,
                        page_number=0,
                    )
                ],
            },
            {
                "category": "text",
                "text": "42",
                "locations": [
                    LocationModel(
                        height=0.01425, width=0.02802, x=0.1, y=0.9637, page_number=0
                    )
                ],
            },
            {
                "category": "text",
                "text": "test noise string at bottom",
                "locations": [
                    LocationModel(
                        height=0.01425,
                        width=0.23641,
                        x=0.17286,
                        y=0.9637,
                        page_number=0,
                    )
                ],
            },
            {
                "category": "text",
                "text": "999",
                "locations": [
                    LocationModel(
                        height=0.01425, width=0.03923, x=0.8, y=0.9637, page_number=0
                    )
                ],
            },
        ]
        output_list_with_locs = convert_output_to_items_list(
            self.extract_output, return_locations=True
        )
        self.assertEqual(expected_list_with_locs, output_list_with_locs)

    def test_convert_output_to_items_hierarchical(self) -> None:
        output_list = convert_output_to_items_list(self.extract_output_hierarchical)
        expected_list = [
            {"category": "text", "text": "July 1, 2000"},
            {"category": "h1", "text": "Research Update: A Company"},
            {"category": "h1", "text": "Bank"},
            {"category": "text", "text": "Credit Analyst:"},
            {"category": "text", "text": "A Guy"},
            {"category": "text", "text": "Table Of Contents"},
            {"category": "text", "text": "Ratings List"},
            {"category": "text", "text": "E-Mail Addresses"},
            {"category": "h1", "text": "Research Update: The Company"},
            {"category": "table_title", "text": "Credit Rating"},
            {"category": "table_title", "text": "Rationale"},
            {"category": "paragraph", "text": "S&P assigned it a AAAAAAA"},
            {"category": "h1", "text": "Outlook"},
            {"category": "paragraph", "text": "The unstable outlook,"},
            {
                "category": "paragraph",
                "text": "the discontinued support of the parent company.",
            },
            {"category": "table_title", "text": "Ratings List"},
            {
                "category": "table",
                "table": [
                    [
                        "ABC",
                        "ABC",
                        "ABC",
                        "ABC",
                        "Bank",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ],
                    [
                        "",
                        "Counterparty",
                        "Counterparty",
                        "credit",
                        "credit",
                        "rating",
                        "rating",
                        "",
                        "AAAAAAAAAAAAAA",
                        "AAAAAAAAAAAAAA",
                        "",
                        "",
                        "",
                    ],
                    [
                        "",
                        "Certificate",
                        "Certificate",
                        "of",
                        "deposit",
                        "",
                        "",
                        "",
                        "AAAAAAAAAAAAAA",
                        "",
                        "",
                        "",
                        "",
                    ],
                    [
                        "A",
                        "complete",
                        "complete",
                        "list",
                        "of",
                        "rating",
                        "actions",
                        "is",
                        "available",
                        "to",
                        "people",
                        "of",
                        "",
                    ],
                    [
                        "the world,",
                        "the world,",
                        "the world,",
                        "Standard",
                        "Standard",
                        "&",
                        "Poor's",
                        "??",
                        "??",
                        "credit",
                        "analysis",
                        "system,",
                        "at",
                    ],
                    [
                        "web.",
                        "web.",
                        "web.",
                        "web.",
                        "web.",
                        "They",
                        "are",
                        "also",
                        "available",
                        "on",
                        "Standard &",
                        "Poor's",
                        "public",
                    ],
                    [
                        "Web",
                        "site",
                        "at",
                        "website;",
                        "website;",
                        "website;",
                        "website;",
                        "website;",
                        "under",
                        "Rating",
                        "Actions,",
                        "select",
                        "Newly",
                    ],
                    [
                        "Released",
                        "Released",
                        "Ratings",
                        "Ratings",
                        "Listings.",
                        "Listings.",
                        "Alternatively,",
                        "Alternatively,",
                        "call",
                        "the",
                        "Standard &",
                        "Poor's",
                        "",
                    ],
                    [
                        "Ratings",
                        "Ratings",
                        "Desk",
                        "in",
                        "NYC",
                        "at",
                        "(44)",
                        "number.",
                        "number.",
                        "",
                        "",
                        "",
                        "",
                    ],
                ],
                "text": "| ABC | ABC | ABC | ABC | Bank |  |  |  |  |  |  |  |  |\n| --- | --- | "
                "--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n|  | "
                "Counterparty | Counterparty | credit | credit | rating | rating |  | "
                "AAAAAAAAAAAAAA | AAAAAAAAAAAAAA |  |  |  |\n|  | Certificate | Certificate | of "
                "| deposit |  |  |  | AAAAAAAAAAAAAA |  |  |  |  |\n| A | complete | complete | "
                "list | of | rating | actions | is | available | to | people | of |  |\n| the "
                "world, | the world, | the world, | Standard | Standard | & | Poor's | ?? | ?? | "
                "credit | analysis | system, | at |\n| web. | web. | web. | web. | web. | They | "
                "are | also | available | on | Standard & | Poor's | public |\n| Web | site | at | "
                "website; | website; | website; | website; | website; | under | Rating | Actions, |"
                " select | Newly |\n| Released | Released | Ratings | Ratings | Listings. | "
                "Listings. | Alternatively, | Alternatively, | call | the | Standard & | Poor's |  "
                "|\n| Ratings | Ratings | Desk | in | NYC | at | (44) | number. | number. |  |  |  "
                "|  |\n",
            },
            {"category": "h2", "text": "Analytical E-Mail Addresses"},
            {"category": "h2", "text": "email"},
            {"category": "paragraph", "text": "email"},
            {"category": "text", "text": "email"},
        ]
        self.assertEqual(expected_list, output_list)

    def test_convert_output_to_items_hierarchical_v2(self) -> None:
        output_list = convert_output_to_items_list(self.extract_output_hierarchical_v2)
        expected_list = [
            {"category": "page_header", "text": "2019  test noise string at top"},
            {"category": "h1", "text": "Generated Toy File Title"},
            {
                "category": "paragraph",
                "text": "Machine learning (ML) is the scientific study of algorithms and "
                "statistical models that computer systems use in order to perform a specific "
                "task effectively without using explicit instructions, relying on patterns "
                "and inference instead. It is seen as a subset of artificial intelligence. "
                "Machine learning algorithms build a mathematical model based on sample data, "
                "known as training data, in order to make predictions or decisions without "
                "being explicitly programmed to perform the task. Valerie is awesome. "
                "Machine learning algorithms are used in a wide variety of applications, "
                "such as email filtering, and computer vision, where it is infeasible to "
                "develop an algorithm of specific instructions for performing the task. "
                "Machine learning is closely related to computational statistics, which "
                "focuses on making predictions using computers. The study of mathematical "
                "optimization delivers methods, theory and application domains to the field of "
                "machine learning. Data mining is a field of study within machine learning, and "
                "focuses on exploratory data analysis through unsupervised learning. In its "
                "application across business problems, machine learning is also referred to "
                "as predictive analytics.",
            },
            {"category": "text", "text": "ESTIMATE for Kensho"},
            {
                "category": "table",
                "table": [
                    ["Kensho Revenue in millions $", "Q1", "Q2", "Q3", "Q4"],
                    ["2020", "100,000", "200,000", "300,000", "400,000"],
                    ["2021", "101,001", "201,001", "301,001", "401,001"],
                    ["2022", "102,004", "202,004", "302,004", "402,004"],
                    ["2023", "103,009", "203,009", "303,009", "403,009"],
                ],
                "text": "| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| --- | --- "
                "| --- | --- | --- |\n| 2020 | 100,000 | 200,000 | 300,000 | 400,000 |\n| 2021 "
                "| 101,001 | 201,001 | 301,001 | 401,001 |\n| 2022 | 102,004 | 202,004 | 302,004 "
                "| 402,004 |\n| 2023 | 103,009 | 203,009 | 303,009 | 403,009 |\n",
            },
            {
                "category": "paragraph",
                "text": "Machine learning (ML) is the scientific study of algorithms and "
                "statistical models that computer systems use in order to perform a specific "
                "task effectively without using explicit instructions, relying on patterns "
                "and inference instead. It is seen as a subset of artificial intelligence. "
                "Machine learning algorithms build a mathematical model based on sample data, "
                "known as training data, in order to make predictions or decisions without "
                "being explicitly programmed to perform the task. Valerie is awesome. "
                "Machine learning algorithms are used in a wide variety of applications, "
                "such as email filtering, and computer vision, where it is infeasible to "
                "develop an algorithm of specific instructions for performing the task. "
                "Machine learning is closely related to computational statistics, which "
                "focuses on making predictions using computers. The study of mathematical "
                "optimization delivers methods, theory and application domains to the field of "
                "machine learning. Data mining is a field of study within machine learning, and "
                "focuses on exploratory data analysis through unsupervised learning. In its "
                "application across business problems, machine learning is also referred to "
                "as predictive analytics.",
            },
            {"category": "text", "text": "Recommendation: BUY"},
            {"category": "page_footer", "text": "42  test noise string at bottom  999"},
        ]
        self.assertEqual(expected_list, output_list)

    def test_convert_output_to_items_char_offsets(self) -> None:
        output_list = convert_output_to_items_list(self.extract_output_char_offsets)
        expected_output_list = [
            {"category": "text", "text": "2019"},
            {"category": "text", "text": "test noise string at top"},
            {"category": "title", "text": "Generated Toy File Title"},
            {
                "category": "text",
                "text": "Machine learning (ML) is the scientific study of algorithms and "
                "statistical models that computer sys"
                "tems use in order to perform a specific task effectively without "
                "using explicit instructions, relyin"
                "g on patterns and inference instead. It is seen as a subset of artificial "
                "intelligence. Machine lear"
                "ning algorithms build a mathematical model based on sample data, known as "
                "training data, in order to"
                " make predictions or decisions without being explicitly programmed to "
                "perform the task. Valerie is"
                " awesome. Machine learning algorithms are used in a wide variety of "
                "applications, such as email filtering, and computer vision, where it is "
                "infeasible to develop an algorithm of specific instructions "
                "for performing the task. Machine learning is closely related to "
                "computational statistics, which focuses on making predictions using computers"
                ". The study of mathematical optimization delivers methods, "
                "theory and application domains to the field of machine learning. Data "
                "mining is a field of study within machine learning, and focuses on "
                "exploratory data analysis through unsupervised learning. In its"
                " application across business problems, machine learning is also "
                "referred to as predictive analytics.",
            },
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
                "text": "| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| --- | --- "
                "| --- | --- | --- |\n| 2020 | 100,000 | 200,000 | 300,000 | 400,000 |\n| "
                "2021 | 101,001 | 201,001 | 301,001 | 401,001 |\n| 2022 | 102,004 "
                "| 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | 203,009 | 303,009 | 403,009 "
                "|\n",
            },
            {
                "category": "text",
                "text": "Machine learning (ML) is the scientific study of algorithms and statis"
                "tical models that computer systems use in order to perform a specific "
                "task effectively without using explicit instructions, relying on patte"
                "rns and inference instead. It is seen as a subset of artificial intell"
                "igence. Machine learning algorithms build a mathematical model based o"
                "n sample data, known as training data, in order to make predictions or"
                " decisions without being explicitly programmed to perform the task. To"
                "ny Tong is awesome. Machine learning algorithms are used in a wide var"
                "iety of applications, such as email filtering, and computer vision, wh"
                "ere it is infeasible to develop an algorithm of specific instructions "
                "for performing the task. Machine learning is closely related to comput"
                "ational statistics, which focuses on making predictions using computer"
                "s. The study of mathematical optimization delivers methods, theory and"
                " application domains to the field of machine learning. Data mining is "
                "a field of study within machine learning, and focuses on exploratory d"
                "ata analysis through unsupervised learning. In its application across "
                "business problems, machine learning is also referred to as predictive "
                "analytics.",
            },
            {"category": "title", "text": "Recommendation: BUY"},
            {"category": "text", "text": "42"},
            {"category": "text", "text": "test noise string at bottom"},
            {"category": "text", "text": "999"},
        ]
        self.assertListEqual(expected_output_list, output_list)

    def test_convert_output_to_str(self) -> None:
        expected_str = (
            "2019\ntest noise string at top\nGenerated Toy File Title\nMachi"
            "ne learning (ML) is the scientific study of algorithms and s"
            "tatistical models that computer systems use in order to perf"
            "orm a specific task effectively without using explicit instr"
            "uctions, relying on patterns and inference instead. It is se"
            "en as a subset of artificial intelligence. Machine learning "
            "algorithms build a mathematical model based on sample data, "
            "known as training data, in order to make predictions or deci"
            "sions without being explicitly programmed to perform the tas"
            "k. Valerie is awesome. Machine learning algorithms are used "
            "in a wide variety of applications, such as email filtering, "
            "and computer vision, where it is infeasible to develop an al"
            "gorithm of specific instructions for performing the task. Ma"
            "chine learning is closely related to computational statistic"
            "s, which focuses on making predictions using computers. The "
            "study of mathematical optimization delivers methods, theory "
            "and application domains to the field of machine learning. Da"
            "ta mining is a field of study within machine learning, and f"
            "ocuses on exploratory data analysis through unsupervised lea"
            "rning. In its application across business problems, machine "
            "learning is also referred to as predictive analytics.\nESTIMA"
            "TE for Kensho\n| Kensho Revenue in millions $ | Q1 | Q2 | Q3 "
            "| Q4 |\n| --- | --- | --- | --- | --- |\n| 2020 | 100,000 | "
            "200,000 | 300,000 | 400,000 |\n| 20"
            "21 | 101,001 | 201,001 | 301,001 | 401,001 |\n| 2022 | 102,00"
            "4 | 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | 203,009"
            " | 303,009 | 403,009 |\n\nMachine learning (ML) is the scientif"
            "ic study of algorithms and statistical models that computer "
            "systems use in order to perform a specific task effectively "
            "without using explicit instructions, relying on patterns and"
            " inference instead. It is seen as a subset of artificial int"
            "elligence. Machine learning algorithms build a mathematical "
            "model based on sample data, known as training data, in order"
            " to make predictions or decisions without being explicitly p"
            "rogrammed to perform the task. Valerie is awesome. Machine l"
            "earning algorithms are used in a wide variety of application"
            "s, such as email filtering, and computer vision, where it is"
            " infeasible to develop an algorithm of specific instructions"
            " for performing the task. Machine learning is closely relate"
            "d to computational statistics, which focuses on making predi"
            "ctions using computers. The study of mathematical optimizati"
            "on delivers methods, theory and application domains to the f"
            "ield of machine learning. Data mining is a field of study wi"
            "thin machine learning, and focuses on exploratory data analy"
            "sis through unsupervised learning. In its application across"
            " business problems, machine learning is also referred to as "
            "predictive analytics.\nRecommendation: BUY\n42\ntest noise stri"
            "ng at bottom\n999"
        )
        output_str = convert_output_to_str(self.extract_output)
        self.assertEqual(expected_str, output_str)

    def test_convert_output_to_str_hierarchical(self) -> None:
        expected_str = (
            "July 1, 2000\nResearch Update: A Company\nBank\nCredit Analyst:\nA Guy\n"
            "Table Of Contents\nRatings List\nE-Mail Addresses\nResearch Update: The Company\n"
            "Credit "
            "Rating\nRationale\nS&P assigned it a AAAAAAA\nOutlook\nThe unstable outlook,\nthe "
            "discontinued support of the parent company.\nRatings List\n| ABC | ABC | ABC | ABC | "
            "Bank"
            " |  |  |  |  |  |  |  |  |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | "
            "--- | --- | --- | --- |\n|  | Counterparty | Counterparty | credit | credit | "
            "rating |"
            " rating |  | AAAAAAAAAAAAAA | AAAAAAAAAAAAAA |  |  |  |\n|  | Certificate | "
            "Certificate |"
            " of | deposit |  |  |  | AAAAAAAAAAAAAA |  |  |  |  |\n| A | complete | complete | "
            "list |"
            " of | rating | actions | is | available | to | people | of |  |\n| the world, | the "
            "world"
            ", | the world, | Standard | Standard | & | Poor's | ?? | ?? | credit | analysis | "
            "system,"
            " | at |\n| web. | web. | web. | web. | web. | They | are | also | available | on | "
            "Standard & | Poor's | public |\n| Web | site | at | website; | website; | website; | "
            "website; | website; | under | Rating | Actions, | select | Newly |\n| Released | "
            "Released"
            " | Ratings | Ratings | Listings. | Listings. | Alternatively, | Alternatively, | "
            "call | "
            "the | Standard & | Poor's |  |\n| Ratings | Ratings | Desk | in | NYC | at | (44) | "
            "number. | number. |  |  |  |  |\n\nAnalytical E-Mail Addresses\nemail\nemail\nemail"
        )
        output_str = convert_output_to_str(self.extract_output_hierarchical)
        self.assertEqual(expected_str, output_str)

    def test_convert_output_to_str_char_offsets(self) -> None:
        output_str = convert_output_to_str(self.extract_output_char_offsets)
        expected_output_str = (
            "2019\ntest noise string at top\nGenerated Toy File Title\nMachine learnin"
            "g (ML) is the scientific study of algorithms and statistical models th"
            "at computer systems use in order to perform a specific task effectivel"
            "y without using explicit instructions, relying on patterns and inferen"
            "ce instead. It is seen as a subset of artificial intelligence. Machine"
            " learning algorithms build a mathematical model based on sample data, "
            "known as training data, in order to make predictions or decisions with"
            "out being explicitly programmed to perform the task. Valerie is awes"
            "ome. Machine learning algorithms are used in a wide variety of applica"
            "tions, such as email filtering, and computer vision, where it is infea"
            "sible to develop an algorithm of specific instructions for performing "
            "the task. Machine learning is closely related to computational statist"
            "ics, which focuses on making predictions using computers. The study of"
            " mathematical optimization delivers methods, theory and application do"
            "mains to the field of machine learning. Data mining is a field of stud"
            "y within machine learning, and focuses on exploratory data analysis th"
            "rough unsupervised learning. In its application across business proble"
            "ms, machine learning is also referred to as predictive analytics.\nESTI"
            "MATE for Kensho\n| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n|"
            " --- | --- | --- | --- | --- |\n| 2020 | 100,000 | 200,000 | 300,000 | "
            "400,000 |\n| 2021 | 101,001 | 201,001 | 301,001 | 401,001 |\n| 2022 | 10"
            "2,004 | 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | 203,009 | 303"
            ",009 | 403,009 |\n\nMachine learning (ML) is the scientific study of alg"
            "orithms and statistical models that computer systems use in order to p"
            "erform a specific task effectively without using explicit instructions"
            ", relying on patterns and inference instead. It is seen as a subset of"
            " artificial intelligence. Machine learning algorithms build a mathemat"
            "ical model based on sample data, known as training data, in order to m"
            "ake predictions or decisions without being explicitly programmed to pe"
            "rform the task. Valerie is awesome. Machine learning algorithms are "
            "used in a wide variety of applications, such as email filtering, and c"
            "omputer vision, where it is infeasible to develop an algorithm of spec"
            "ific instructions for performing the task. Machine learning is closely"
            " related to computational statistics, which focuses on making predicti"
            "ons using computers. The study of mathematical optimization delivers m"
            "ethods, theory and application domains to the field of machine learnin"
            "g. Data mining is a field of study within machine learning, and focuse"
            "s on exploratory data analysis through unsupervised learning. In its a"
            "pplication across business problems, machine learning is also referred"
            " to as predictive analytics.\nRecommendation: BUY\n42\ntest noise string "
            "at bottom\n999"
        )
        self.assertEqual(expected_output_str, output_str)

    def test_convert_output_to_markdown(self) -> None:
        expected_str = (
            "2019\ntest noise string at top\n# Generated Toy File Title\nMac"
            "hine learning (ML) is the scientific study of algorithms and"
            " statistical models that computer systems use in order to pe"
            "rform a specific task effectively without using explicit ins"
            "tructions, relying on patterns and inference instead. It is "
            "seen as a subset of artificial intelligence. Machine learnin"
            "g algorithms build a mathematical model based on sample data"
            ", known as training data, in order to make predictions or de"
            "cisions without being explicitly programmed to perform the t"
            "ask. Valerie is awesome. Machine learning algorithms are use"
            "d in a wide variety of applications, such as email filtering"
            ", and computer vision, where it is infeasible to develop an "
            "algorithm of specific instructions for performing the task. "
            "Machine learning is closely related to computational statist"
            "ics, which focuses on making predictions using computers. Th"
            "e study of mathematical optimization delivers methods, theor"
            "y and application domains to the field of machine learning. "
            "Data mining is a field of study within machine learning, and"
            " focuses on exploratory data analysis through unsupervised l"
            "earning. In its application across business problems, machin"
            "e learning is also referred to as predictive analytics.\n# ES"
            "TIMATE for Kensho\n| Kensho Revenue in millions $ | Q1 | Q2 |"
            " Q3 | Q4 |\n| --- | --- | --- | --- | --- |\n| 2020 | 100,000"
            " | 200,000 | 300,000 | 400,000 |\n"
            "| 2021 | 101,001 | 201,001 | 301,001 | 401,001 |\n| 2022 | 10"
            "2,004 | 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | 203"
            ",009 | 303,009 | 403,009 |\n\nMachine learning (ML) is the scie"
            "ntific study of algorithms and statistical models that compu"
            "ter systems use in order to perform a specific task effectiv"
            "ely without using explicit instructions, relying on patterns"
            " and inference instead. It is seen as a subset of artificial"
            " intelligence. Machine learning algorithms build a mathemati"
            "cal model based on sample data, known as training data, in o"
            "rder to make predictions or decisions without being explicit"
            "ly programmed to perform the task. Valerie is awesome. Machi"
            "ne learning algorithms are used in a wide variety of applica"
            "tions, such as email filtering, and computer vision, where i"
            "t is infeasible to develop an algorithm of specific instruct"
            "ions for performing the task. Machine learning is closely re"
            "lated to computational statistics, which focuses on making p"
            "redictions using computers. The study of mathematical optimi"
            "zation delivers methods, theory and application domains to t"
            "he field of machine learning. Data mining is a field of stud"
            "y within machine learning, and focuses on exploratory data a"
            "nalysis through unsupervised learning. In its application ac"
            "ross business problems, machine learning is also referred to"
            " as predictive analytics.\n# Recommendation: BUY\n42\ntest nois"
            "e string at bottom\n999"
        )
        output_str = convert_output_to_markdown(self.extract_output)
        self.assertEqual(expected_str, output_str)

    def test_convert_output_to_markdown_hierarchical(self) -> None:
        expected_str = (
            "July 1, 2000\n# Research Update: A Company\n# Bank\nCredit Analyst:\nA Guy\n"
            "Table Of Contents\nRatings List\nE-Mail Addresses\n# Research Update: The Company\n"
            "### Credit Rating\n### Rationale\nS&P assigned it a AAAAAAA\n# Outlook\nThe unstable "
            "outlook,\nthe discontinued support of the parent company.\n### Ratings List\n| ABC | "
            "ABC | ABC | ABC | Bank |  |  |  |  |  |  |  |  |\n| --- | --- | --- | --- | --- "
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n|  | Counterparty | Counterparty |"
            " credit | credit | rating | rating |  | AAAAAAAAAAAAAA | AAAAAAAAAAAAAA |  |  |  |\n|"
            "  | Certificate | Certificate | of | deposit |  |  |  | AAAAAAAAAAAAAA |  |  |  |  "
            "|\n| A | complete | complete | list | of | rating | actions | is | available | to | "
            "people | of |  |\n| the world, | the world, | the world, | Standard | Standard | & |"
            " Poor's | ?? | ?? | credit | analysis | system, | at |\n| web. | web. | web. | web. "
            "| web. | They | are | also | available | on | Standard & | Poor's | public |\n| Web |"
            " site | at | website; | website; | website; | website; | website; | under | Rating | "
            "Actions, | select | Newly |\n| Released | Released | Ratings | Ratings | Listings. | "
            "Listings. | Alternatively, | Alternatively, | call | the | Standard & | Poor's |  "
            "|\n| Ratings | Ratings | Desk | in | NYC | at | (44) | number. | number. |  |  |  |  "
            "|\n\n## Analytical E-Mail Addresses\n## email\nemail\nemail"
        )
        output_str = convert_output_to_markdown(self.extract_output_hierarchical)
        self.assertEqual(expected_str, output_str)

    def test_convert_output_to_markdown_hierarchical_v2(self) -> None:
        expected_str = (
            "2019  test noise string at top\n# Generated Toy File Title\nMachine learning (ML) "
            "is the scientific study of algorithms and statistical models that computer systems "
            "use in order to perform a specific task effectively without using explicit "
            "instructions, relying on patterns and inference instead. It is seen as a subset"
            " of artificial intelligence. Machine learning algorithms build a mathematical"
            " model based on sample data, known as training data, in order to make predictions"
            " or decisions without being explicitly programmed to perform the task. Valerie "
            "is awesome. Machine learning algorithms are used in a wide variety of applications,"
            " such as email filtering, and computer vision, where it is infeasible to develop"
            " an algorithm of specific instructions for performing the task. Machine learning"
            " is closely related to computational statistics, which focuses on making "
            "predictions using computers. The study of mathematical optimization delivers methods"
            ", theory and application domains to the field of machine learning. Data mining is a "
            "field of study within machine learning, and focuses on exploratory data analysis "
            "through unsupervised learning. In its application across business problems, "
            "machine learning is also referred to as predictive analytics.\nESTIMATE for "
            "Kensho\n| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| --- | --- | --- "
            "| --- | --- |\n| 2020 | 100,000 | 200,000 | 300,000 | 400,000 |\n| 2021 | 101,001 "
            "| 201,001 | 301,001 | 401,001 |\n| 2022 | 102,004 | 202,004 | 302,004 | 402,004 |\n"
            "| 2023 | 103,009 | 203,009 | 303,009 | 403,009 |\n\nMachine learning (ML) is the "
            "scientific study of algorithms and statistical models that computer systems use in "
            "order to perform a specific task effectively without using explicit instructions, "
            "relying on patterns and inference instead. It is seen as a subset of artificial "
            "intelligence. Machine learning algorithms build a mathematical model based on "
            "sample data, known as training data, in order to make predictions or decisions "
            "without being explicitly programmed to perform the task. Valerie is awesome. "
            "Machine learning algorithms are used in a wide variety of applications, such as "
            "email filtering, and computer vision, where it is infeasible to develop an "
            "algorithm of specific instructions for performing the task. Machine learning "
            "is closely related to computational statistics, which focuses on making "
            "predictions using computers. The study of mathematical optimization "
            "delivers methods, theory and application domains to the field of machine learning. "
            "Data mining is a field of study within machine learning, and focuses on "
            "exploratory data analysis through unsupervised learning. In its application "
            "across business problems, machine learning is also referred to as predictive "
            "analytics.\nRecommendation: BUY\n42  test noise string at bottom  999"
        )
        output_str = convert_output_to_markdown(self.extract_output_hierarchical_v2)
        self.assertEqual(expected_str, output_str)

    def test_convert_table_to_markdown(self) -> None:
        table_cells = [
            ContentModel(
                uid="7",
                type="TABLE_CELL",
                content="Kensho Revenue in millions $",
                children=[],
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
            ContentModel(
                uid="8",
                type="TABLE_CELL",
                content="Q1",
                children=[],
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
            ContentModel(
                uid="9",
                type="TABLE_CELL",
                content="Q2",
                children=[],
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
            ContentModel(
                uid="10",
                type="TABLE_CELL",
                content="Q3",
                children=[],
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
            ContentModel(
                uid="11",
                type="TABLE_CELL",
                content="Q4",
                children=[],
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
            ContentModel(
                uid="12",
                type="TABLE_CELL",
                content="2020",
                children=[],
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
            ContentModel(
                uid="13",
                type="TABLE_CELL",
                content="100,000",
                children=[],
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
            ContentModel(
                uid="14",
                type="TABLE_CELL",
                content="200,000",
                children=[],
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
            ContentModel(
                uid="15",
                type="TABLE_CELL",
                content="300,000",
                children=[],
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
            ContentModel(
                uid="16",
                type="TABLE_CELL",
                content="400,000",
                children=[],
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
            ContentModel(
                uid="17",
                type="TABLE_CELL",
                content="2021",
                children=[],
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
            ContentModel(
                uid="18",
                type="TABLE_CELL",
                content="101,001",
                children=[],
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
            ContentModel(
                uid="19",
                type="TABLE_CELL",
                content="201,001",
                children=[],
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
            ContentModel(
                uid="20",
                type="TABLE_CELL",
                content="301,001",
                children=[],
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
            ContentModel(
                uid="21",
                type="TABLE_CELL",
                content="401,001",
                children=[],
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
            ContentModel(
                uid="22",
                type="TABLE_CELL",
                content="2022",
                children=[],
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
            ContentModel(
                uid="23",
                type="TABLE_CELL",
                content="102,004",
                children=[],
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
            ContentModel(
                uid="24",
                type="TABLE_CELL",
                content="202,004",
                children=[],
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
            ContentModel(
                uid="25",
                type="TABLE_CELL",
                content="302,004",
                children=[],
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
            ContentModel(
                uid="26",
                type="TABLE_CELL",
                content="402,004",
                children=[],
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
            ContentModel(
                uid="27",
                type="TABLE_CELL",
                content="2023",
                children=[],
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
            ContentModel(
                uid="28",
                type="TABLE_CELL",
                content="103,009",
                children=[],
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
            ContentModel(
                uid="29",
                type="TABLE_CELL",
                content="203,009",
                children=[],
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
            ContentModel(
                uid="30",
                type="TABLE_CELL",
                content="303,009",
                children=[],
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
            ContentModel(
                uid="31",
                type="TABLE_CELL",
                content="403,009",
                children=[],
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
        uid_to_index = {
            "7": (0, 0),
            "8": (0, 1),
            "9": (0, 2),
            "10": (0, 3),
            "11": (0, 4),
            "12": (1, 0),
            "13": (1, 1),
            "14": (1, 2),
            "15": (1, 3),
            "16": (1, 4),
            "17": (2, 0),
            "18": (2, 1),
            "19": (2, 2),
            "20": (2, 3),
            "21": (2, 4),
            "22": (3, 0),
            "23": (3, 1),
            "24": (3, 2),
            "25": (3, 3),
            "26": (3, 4),
            "27": (4, 0),
            "28": (4, 1),
            "29": (4, 2),
            "30": (4, 3),
            "31": (4, 4),
        }

        uid_to_span = {
            "7": (1, 1),
            "8": (1, 1),
            "9": (1, 1),
            "10": (1, 1),
            "11": (1, 1),
            "12": (1, 1),
            "13": (1, 1),
            "14": (1, 1),
            "15": (1, 1),
            "16": (1, 1),
            "17": (1, 1),
            "18": (1, 1),
            "19": (1, 1),
            "20": (1, 1),
            "21": (1, 1),
            "22": (1, 1),
            "23": (1, 1),
            "24": (1, 1),
            "25": (1, 1),
            "26": (1, 1),
            "27": (1, 1),
            "28": (1, 1),
            "29": (1, 1),
            "30": (1, 1),
            "31": (1, 1),
        }

        # Test table construction from cells
        table = _construct_table_from_cells(table_cells, uid_to_index, uid_to_span)
        expected_table = [
            ["Kensho Revenue in millions $", "Q1", "Q2", "Q3", "Q4"],
            ["2020", "100,000", "200,000", "300,000", "400,000"],
            ["2021", "101,001", "201,001", "301,001", "401,001"],
            ["2022", "102,004", "202,004", "302,004", "402,004"],
            ["2023", "103,009", "203,009", "303,009", "403,009"],
        ]
        self.assertEqual(table, expected_table)

        # Test markdown conversion
        markdown_table = table_to_markdown(table)
        expected_markdown = (
            "| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| --- | --- | --- |"
            " --- | --- |\n| 2020 | 100,000 | 200"
            ",000 | 300,000 | 400,000 |\n| 2021 | 101,001 | 201,001 | 301,001 | 401,001 |"
            "\n| 2022 | 102,004 | 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | 203,00"
            "9 | 303,009 | 403,009 |\n"
        )
        self.assertEqual(markdown_table, expected_markdown)

    def test_convert_output_to_markdown_by_page(self) -> None:
        expected_output = [
            (
                "# Torch-Struct:\n# Deep Structured Prediction Library\nAlexander M. Rush Corn"
                "ell University Department of Computer Science\nAbstract The literature on st"
                "ructured prediction for NLP describes a rich collection of distributions an"
                "d algorithms over sequences, segmentations, alignments, and trees; however,"
                " these algo- rithms are difﬁcult to utilize in deep learning frameworks. We"
                " introduce Torch-Struct, a li- braryforstructuredpredictiondesignedtotake a"
                "dvantage of and integrate with vectorized, auto-differentiation based frame"
                "works. Torch- Struct includes a broad collection of proba- bilistic structu"
                "res accessed through a simple and ﬂexible distribution-based API that con- "
                "nects to any deep learning model. The li- brary utilizes batched, vectorize"
                "d operations and exploits auto-differentiation to produce readable, fast, a"
                "nd testable code. Internally, we also include a number of general-purpose o"
                "ptimizations to provide cross-algorithm ef- ﬁciency. Experiments show signi"
                "ﬁcant per- formance gains over fast baselines and case- studies demonstrate"
                " the beneﬁts of the library. Torch-Struct is available at https://github. c"
                "om/harvardnlp/pytorch-struct. 1 Introduction Structuredpredictionisanareaof"
                "machinelearning focusing on representations of spaces with combi- natorial "
                "structure, and algorithms for inference and parameter estimation over these"
                " structures. Core methods include both tractable exact approaches like dyna"
                "mic programming and spanning tree algo- rithms as well as heuristic techniq"
                "ues such linear programming relaxations and greedy search. Structured predi"
                "ction has played a key role in the history of natural language processing. "
                "Ex- ample methods include techniques for sequence labeling and segmentation"
                " (Lafferty et al., 2001; Sarawagi and Cohen, 2005), discriminative depen- d"
                "ency and constituency parsing (Finkel et al., 2008; McDonald et al., 2005),"
                " unsupervised learning for a r X i v : 2 0 0 2 . 0 0 8 7 6 v 1 [ c s . C L "
                "] 3 F e b 2 0 2 0\nFigure 1: Distribution of binary trees over an 1000- toke"
                "n sequence. Coloring shows the marginal proba- bilities of every span. Torc"
                "h-Struct is an optimized col- lection of common CRF distributions used in N"
                "LP de- signed to integrate with deep learning frameworks.\nlabeling and alig"
                "nment (Vogel et al., 1996; Gold- water and Grifﬁths, 2007), approximate tra"
                "nslation decoding with beam search (Tillmann and Ney, 2003), among many oth"
                "ers.\nIn recent years, research into deep structured pre- diction has studie"
                "d how these approaches can be in- tegrated with neural networks and pretrai"
                "ned mod- els. One line of work has utilized structured predic- tion as the "
                "ﬁnal ﬁnal layer for deep models (Col- lobert et al., 2011; Durrett and Klei"
                "n, 2015). An- other has incorporated structured prediction within deep lear"
                "ning models, exploring novel models for latent-structure learning, unsuperv"
                "ised learning, or model control (Johnson et al., 2016; Yogatama et al., 201"
                "6; Wiseman et al., 2018). We aspire to make both of these use-cases as easy"
                " to use as standard neural networks.\nThe practical challenge of employing s"
                "tructured"
            ),
            (
                "| Name | Structure ( ) | Parts ( |  | ) |  | Algorithm (A(`)) | LoC | T/S |"
                " Sample Reference | Sample Reference |  |\n| --- | --- | --- | --- | --- | "
                "--- | --- | --- | --- | --- | --- | --- |\n|  | Z |  | P | P |  |  |  |  |  "
                "|  |  |\n| Linear-Chain | Labeled Chain | Edges (TC^2 | Edges (TC^2 | Edges "
                "(TC^2 | ) | Forward-Backward, | 20 | 390k | (Lafferty et al., 2001) | (Laff"
                "erty et al., 2001) |  |\n|  |  |  |  |  |  | Viterbi |  |  |  |  |  |\n| Fact"
                "orial-HMM | Labeled Chains | Trans. | (LC^2 | (LC^2 | ) | Factorial F-B | 2"
                "0 | 25k | (Ghahramani | and | Jordan, |\n|  |  | Obs. | (TC^L | ) |  |  |  |"
                "  | 1996) |  |  |\n| Alignment | Alignment | Match (NM) | Match (NM) | Match"
                " (NM) | Match (NM) | DTW, CTC, | 50 | 13k | (Needleman | and Wunsch, | and "
                "Wunsch, |\n|  |  | Skips (2NM) | Skips (2NM) | Skips (2NM) | Skips (2NM) | N"
                "eedleman-Wunsch |  |  | 1970) |  |  |\n| Semi-Markov | Seg. Labels | Edges |"
                "  |  |  | Segmental F-B | 30 | 87k | (Baum and Petrie, 1966) | (Baum and Pe"
                "trie, 1966) | (Baum and Petrie, 1966) |\n|  |  | (NKC^2 | (NKC^2 | ) |  |  |"
                "  |  | (Sarawagi and Cohen, 2005) | (Sarawagi and Cohen, 2005) | (Sarawagi "
                "and Cohen, 2005) |\n| Context-Free | Labeled Tree | CF Rules (G) | CF Rules "
                "(G) | CF Rules (G) | CF Rules (G) | Inside-Outside CKY | 70 | 37k | (Kasami"
                ", 1966) |  |  |\n|  |  | Term. | (CN) | (CN) |  |  |  |  |  |  |  |\n| Simple"
                " CKY | Labeled Tree | Splits (CN^2 | Splits (CN^2 | Splits (CN^2 | ) | 0-th"
                " order CKY | 30 | 118k | (Kasami, 1966) |  |  |\n| Dependency | Proj. Tree |"
                " Arcs (N^2 | Arcs (N^2 | ) |  | Eisner Algorithm | 40 | 28k | (Eisner, 2000"
                ") |  |  |\n| Dependency (NP) | Non-Proj. Tree | Arcs (N^2 | Arcs (N^2 | ) | "
                " | Matrix-Tree | 40 | 1.1m | (Koo et al., 2007) | (Koo et al., 2007) |  |\n|"
                "  |  |  |  |  |  | Chiu-Liu (MAP) |  |  | (McDonald et al., 2005) | (McDona"
                "ld et al., 2005) | (McDonald et al., 2005) |\n| Auto-Regressive | Sequence |"
                " Preﬁx (C^N | Preﬁx (C^N | ) |  | Greedy Search, | 60 | - | (Tillmann and N"
                "ey, 2003) | (Tillmann and Ney, 2003) | (Tillmann and Ney, 2003) |\n|  |  |  "
                "|  |  |  | Beam Search |  |  |  |  |  |\n\nTable 1: Models and algorithms impl"
                "emented in Torch-Struct. Notation is developed in Section 5. Parts are desc"
                "ribed in terms of sequence lengths N,M, label size C, segment length K, and"
                " layers / grammar size L,G. Lines of code (LoC) is from the log-partition ("
                "A(`)) implementation. T/S is the tokens per second of a batched computation"
                ", computed with batch 32, N = 25,C = 20,K = 5,L = 3 (K80 GPU run on Google "
                "Colab).\nprediction is that many required algorithms are dif- ﬁcult to imple"
                "ment efﬁciently and correctly. Most projects reimplement custom versions of"
                " standard algorithms or focus particularly on a single well- deﬁned model c"
                "lass. This research style makes it difﬁcult to combine and try out new appr"
                "oaches, a problem that has compounded with the complexity of research in de"
                "ep structured prediction. With this challenge in mind, we introduce Torch- "
                "Struct with three speciﬁc contributions: •mains. Most ambitiously, Modulari"
                "ty: models are represented as distri- butions with a standard ﬂexible API i"
                "ntegrated into a deep learning framework. • Completeness: a broad array of "
                "classical algo- rithms are implemented and new models can easily be added i"
                "n Python. •motivating this approach with a case study. Efﬁciency: implement"
                "ations target computa- tional/memory efﬁciency for GPUs and the backend inc"
                "ludes extensions for optimization. 2007) or CRF++ (Kudo, 2005), implement i"
                "n- ference for a ﬁxed set of popular models, such as linear-chain CRFs. Gen"
                "eral-purpose inference libraries, such as PyStruct (M¨uller and Behnke, 201"
                "4) or TurboParser (Martins et al., 2010), uti- lize external solvers for (p"
                "rimarily MAP) inference such as integer linear programming solvers and ADMM"
                ". Probabilistic programming languages, for example languages that integrate"
                " with deep learn- ing such as Pyro (Bingham et al., 2019), allow for speciﬁ"
                "cation and inference over some discrete do- inference libraries such as Dyn"
                "a (Eisner et al., 2004) allow for declarative speciﬁcations of dynamic prog"
                "ramming algorithms to support inference for generic algorithms. Torch- Stru"
                "ct takes a different approach and integrates a library of optimized structu"
                "red distributions into a vectorized deep learning system. We begin by 3 Mot"
                "ivating Case Study\nIn this system description, we ﬁrst motivate the ap- pro"
                "ach taken by the library, then present a technical description of the metho"
                "ds used, and ﬁnally present several example use cases. 2 Related Work Sever"
                "al software libraries target structured pre- diction. Optimization tools, s"
                "uch as SVM- struct (Joachims, 2008), focus on parameter estima- tion. Model"
                " libraries, such as CRFSuite (Okazaki, While structured prediction is tradi"
                "tionally pre- sented at the output layer, recent applications have deployed"
                " structured models broadly within neural networks (Johnson et al., 2016; Ki"
                "m et al., 2017; Yogatama et al., 2016, inter alia). Torch-Struct aims to en"
                "courage this general use case. To illustrate, we consider a latent tree mod"
                "el. ListOps (Nangia and Bowman, 2018) is a dataset of mathematical function"
                "s. Each data point consists"
            ),
            (
                "of a preﬁx expression x and its result y, e.g.\nx = [ MAX 2 9 [ MIN 4 7 ] 0 ] "
                "y = 9\nModels such as a ﬂat RNN will fail to capture the hierarchical structure "
                "of this task. However, if a model can induce an explicit latent z, the parse tree "
                "of the expression, then the task is easy to learn by a tree-RNN model p(y | x,z) "
                "(Yogatama et al., 2016; Havrylov et al., 2019).\nA popular approach is a "
                "latent-tree"
                " RL model which we brieﬂy summarize. The objective is to maximize the probability"
                " of the correct predic- tion under the expectation of a prior tree model, p(z | x"
                ";\x00),\n| Figure | 2: | Latent | Tree | CRF | example. | (a) | Log- |\n| --- |"
                " --- | --- | --- | --- | --- | --- | --- |\n| "
                "potentials"
                " | ` | for | each | part/span. | (b) Marginals | (b) Marginals | for |\n| CRF(`) "
                "| "
                "computed by backpropagation. | computed by backpropagation. | computed by "
                "backpropagation. | computed by backpropagation. | (c) Mode | (c) Mode | tree "
                "|\n| "
                "argmaxz CRF(z;`). | argmaxz CRF(z;`). | argmaxz CRF(z;`). | (d) Sampled tree z | "
                "(d) Sampled tree z | ⇠ | CRF(`). | CRF(`). |\n\n# 4 Library Design\nO = Ez^⇠ p(z |"
                " x;\x00)[logp(y | z,x)] Computing the expectation is intractable so pol- icy "
                "gradient is used. First a tree is sampled ˜z ⇠ p(z | x;\x00), then the gradient "
                "with respect to \x00 is approximated as, @ @\x00 O ⇡ (logp(y | ˜z,x) \x00 b)( @ @"
                "\x00 p(z | x;\x00)) where b is a variance reduction baseline. A com- mon choice "
                "is "
                "the self-critical baseline (Rennie et al., 2017), b = logp(y | z⇤,x) with z⇤ = "
                "argmax z p(z | x;\x00) Finally an entropy regularization term is added to the "
                "objective "
                "encourage exploration of different trees, O + \x00H(p(z | x;\x00)). Even in this "
                "brief overview, we can see how complex a latent structured learning problem can"
                " be."
                " To compute these terms, we need 5 different properties of the tree model p(z | "
                "x;\x00): Sampling Policy gradient, ˜z ⇠ p(z | x;\x00) Density Score policy "
                "samples"
                ", p(z | x;\x00) Gradient Backpropagation,^@\x00 @ p(z | x;\x00) Argmax "
                "Self-critical, argmaxz p(z | x;\x00) Entropy Objective regularizer, H(p(z | "
                "x;\x00)) For structured models, each of these terms is non- trivial to compute. "
                "A goal of Torch-Struct is to make it seamless to deploy structured models for "
                "these complex settings. To demonstrate this, Torch- Struct includes an "
                "implementation of this latent- tree approach. With a minimal amount of user code, "
                "the implementation achieves near perfect accuracy on the ListOps dataset. The "
                "library design of Torch-Struct follows the dis- tributions API used by both "
                "TensorFlow and Py- Torch (Dillon et al., 2017). For each structured model in the "
                "library, we deﬁne a conditional ran- dom ﬁeld (CRF) distribution object. From a "
                "user’s standpoint, this object provides all necessary distri- butional "
                "properties. "
                "Given log-potentials (scores) output from a deep network `, the user can request "
                "samples z ⇠ CRF(`), probabilities CRF(z;`), modes argmaxz CRF(`), or other "
                "distributional properties such as H(CRF(`)). The library is ag- nostic to how "
                "these are utilized, and when possible, they allow for backpropagation to update "
                "the in- put network. The same distributional object can be used for standard"
                " output"
                " prediction as for more complex operations like attention or reinforcement "
                "learning"
                ". Figure 2 demonstrates this API for a binary tree CRF over an ordered sequence, "
                "such as p(z | y;\x00) from the previous section. The distribution takes in "
                "log-potentials ` which score each possible span in the input. The distribution "
                "converts these to proba- bilities of a speciﬁc tree. This distribution can be "
                "queried for predicting over the set of trees, sam- pling a tree for model "
                "structure, or even computing entropy over all trees. Table 1 shows all of the "
                "structures and distribu- tions implemented in Torch-Struct. While each is "
                "internally implemented using different specialized algorithms and optimizations, "
                "from the user’s per- spective they all utilize the same external distribu- tional"
                " API, and pass a generic set of distributional tests.^1 This approach hides the "
                "internal complexity 1 The test suite for each distribution enumerates over all "
                "structures to ensure that properties hold. While this is in- tractable for "
                "large spaces, it can be done for small sets and"
            ),
        ]
        output = convert_output_to_markdown_by_page(self.extract_output_multi_page)
        self.assertEqual(output, expected_output)

    def test_convert_output_to_markdown_by_page_no_locs(self) -> None:
        expected_output = (
            "2019\ntest noise string at top\n# Generated Toy File Title\nMachine learning ("
            "ML) is the scientific study of algorithms and statistical models that compu"
            "ter systems use in order to perform a specific task effectively without usi"
            "ng explicit instructions, relying on patterns and inference instead. It is "
            "seen as a subset of artificial intelligence. Machine learning algorithms bu"
            "ild a mathematical model based on sample data, known as training data, in o"
            "rder to make predictions or decisions without being explicitly programmed t"
            "o perform the task. Valerie is awesome. Machine learning algorithms are use"
            "d in a wide variety of applications, such as email filtering, and computer "
            "vision, where it is infeasible to develop an algorithm of specific instruct"
            "ions for performing the task. Machine learning is closely related to comput"
            "ational statistics, which focuses on making predictions using computers. Th"
            "e study of mathematical optimization delivers methods, theory and applicati"
            "on domains to the field of machine learning. Data mining is a field of stud"
            "y within machine learning, and focuses on exploratory data analysis through"
            " unsupervised learning. In its application across business problems, machin"
            "e learning is also referred to as predictive analytics.\n# ESTIMATE for Kens"
            "ho\n| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| --- | --- | --- "
            "| --- | --- |\n| 2020 | 100,000 | "
            "200,000 | 300,000 | 400,000 |\n| 2021 | 101,001 | 201,001 | 301,001 | 401,00"
            "1 |\n| 2022 | 102,004 | 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | 203"
            ",009 | 303,009 | 403,009 |\n\nMachine learning (ML) is the scientific study of"
            " algorithms and statistical models that computer systems use in order to pe"
            "rform a specific task effectively without using explicit instructions, rely"
            "ing on patterns and inference instead. It is seen as a subset of artificial"
            " intelligence. Machine learning algorithms build a mathematical model based"
            " on sample data, known as training data, in order to make predictions or de"
            "cisions without being explicitly programmed to perform the task. Valerie is"
            " awesome. Machine learning algorithms are used in a wide variety of applica"
            "tions, such as email filtering, and computer vision, where it is infeasible"
            " to develop an algorithm of specific instructions for performing the task. "
            "Machine learning is closely related to computational statistics, which focu"
            "ses on making predictions using computers. The study of mathematical optimi"
            "zation delivers methods, theory and application domains to the field of mac"
            "hine learning. Data mining is a field of study within machine learning, and"
            " focuses on exploratory data analysis through unsupervised learning. In its"
            " application across business problems, machine learning is also referred to"
            " as predictive analytics.\n# Recommendation: BUY\n42\ntest noise string at bot"
            "tom\n999"
        )
        output = convert_output_to_markdown_by_page(self.extract_output_no_locs)
        self.assertEqual(output, [expected_output])

    def test_convert_output_to_str_by_page_no_locs(self) -> None:
        expected_output = (
            "2019\ntest noise string at top\nGenerated Toy File Title\nMachine learning (ML"
            ") is the scientific study of algorithms and statistical models that compute"
            "r systems use in order to perform a specific task effectively without using"
            " explicit instructions, relying on patterns and inference instead. It is se"
            "en as a subset of artificial intelligence. Machine learning algorithms buil"
            "d a mathematical model based on sample data, known as training data, in ord"
            "er to make predictions or decisions without being explicitly programmed to "
            "perform the task. Valerie is awesome. Machine learning algorithms are used "
            "in a wide variety of applications, such as email filtering, and computer vi"
            "sion, where it is infeasible to develop an algorithm of specific instructio"
            "ns for performing the task. Machine learning is closely related to computat"
            "ional statistics, which focuses on making predictions using computers. The "
            "study of mathematical optimization delivers methods, theory and application"
            " domains to the field of machine learning. Data mining is a field of study "
            "within machine learning, and focuses on exploratory data analysis through u"
            "nsupervised learning. In its application across business problems, machine "
            "learning is also referred to as predictive analytics.\nESTIMATE for Kensho\n|"
            " Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| --- | --- | --- | --- "
            "| --- |\n| 2020 | 100,000 | 200,"
            "000 | 300,000 | 400,000 |\n| 2021 | 101,001 | 201,001 | 301,001 | 401,001 |\n"
            "| 2022 | 102,004 | 202,004 | 302,004 | 402,004 |\n| 2023 | 103,009 | 203,009"
            " | 303,009 | 403,009 |\n\nMachine learning (ML) is the scientific study of alg"
            "orithms and statistical models that computer systems use in order to perfor"
            "m a specific task effectively without using explicit instructions, relying "
            "on patterns and inference instead. It is seen as a subset of artificial int"
            "elligence. Machine learning algorithms build a mathematical model based on "
            "sample data, known as training data, in order to make predictions or decisi"
            "ons without being explicitly programmed to perform the task. Valerie is awe"
            "some. Machine learning algorithms are used in a wide variety of application"
            "s, such as email filtering, and computer vision, where it is infeasible to "
            "develop an algorithm of specific instructions for performing the task. Mach"
            "ine learning is closely related to computational statistics, which focuses "
            "on making predictions using computers. The study of mathematical optimizati"
            "on delivers methods, theory and application domains to the field of machine"
            " learning. Data mining is a field of study within machine learning, and foc"
            "uses on exploratory data analysis through unsupervised learning. In its app"
            "lication across business problems, machine learning is also referred to as "
            "predictive analytics.\nRecommendation: BUY\n42\ntest noise string at bottom\n99"
            "9"
        )
        output = convert_output_to_str_by_page(self.extract_output_no_locs)
        self.assertEqual(output, [expected_output])

    def test_convert_output_to_str_by_page(self) -> None:
        expected_output = [
            (
                "Torch-Struct:\nDeep Structured Prediction Library\nAlexander M. Rush Corn"
                "ell University Department of Computer Science\nAbstract The literature on st"
                "ructured prediction for NLP describes a rich collection of distributions an"
                "d algorithms over sequences, segmentations, alignments, and trees; however,"
                " these algo- rithms are difﬁcult to utilize in deep learning frameworks. We"
                " introduce Torch-Struct, a li- braryforstructuredpredictiondesignedtotake a"
                "dvantage of and integrate with vectorized, auto-differentiation based frame"
                "works. Torch- Struct includes a broad collection of proba- bilistic structu"
                "res accessed through a simple and ﬂexible distribution-based API that con- "
                "nects to any deep learning model. The li- brary utilizes batched, vectorize"
                "d operations and exploits auto-differentiation to produce readable, fast, a"
                "nd testable code. Internally, we also include a number of general-purpose o"
                "ptimizations to provide cross-algorithm ef- ﬁciency. Experiments show signi"
                "ﬁcant per- formance gains over fast baselines and case- studies demonstrate"
                " the beneﬁts of the library. Torch-Struct is available at https://github. c"
                "om/harvardnlp/pytorch-struct. 1 Introduction Structuredpredictionisanareaof"
                "machinelearning focusing on representations of spaces with combi- natorial "
                "structure, and algorithms for inference and parameter estimation over these"
                " structures. Core methods include both tractable exact approaches like dyna"
                "mic programming and spanning tree algo- rithms as well as heuristic techniq"
                "ues such linear programming relaxations and greedy search. Structured predi"
                "ction has played a key role in the history of natural language processing. "
                "Ex- ample methods include techniques for sequence labeling and segmentation"
                " (Lafferty et al., 2001; Sarawagi and Cohen, 2005), discriminative depen- d"
                "ency and constituency parsing (Finkel et al., 2008; McDonald et al., 2005),"
                " unsupervised learning for a r X i v : 2 0 0 2 . 0 0 8 7 6 v 1 [ c s . C L "
                "] 3 F e b 2 0 2 0\nFigure 1: Distribution of binary trees over an 1000- toke"
                "n sequence. Coloring shows the marginal proba- bilities of every span. Torc"
                "h-Struct is an optimized col- lection of common CRF distributions used in N"
                "LP de- signed to integrate with deep learning frameworks.\nlabeling and alig"
                "nment (Vogel et al., 1996; Gold- water and Grifﬁths, 2007), approximate tra"
                "nslation decoding with beam search (Tillmann and Ney, 2003), among many oth"
                "ers.\nIn recent years, research into deep structured pre- diction has studie"
                "d how these approaches can be in- tegrated with neural networks and pretrai"
                "ned mod- els. One line of work has utilized structured predic- tion as the "
                "ﬁnal ﬁnal layer for deep models (Col- lobert et al., 2011; Durrett and Klei"
                "n, 2015). An- other has incorporated structured prediction within deep lear"
                "ning models, exploring novel models for latent-structure learning, unsuperv"
                "ised learning, or model control (Johnson et al., 2016; Yogatama et al., 201"
                "6; Wiseman et al., 2018). We aspire to make both of these use-cases as easy"
                " to use as standard neural networks.\nThe practical challenge of employing s"
                "tructured"
            ),
            (
                "| Name | Structure ( ) | Parts ( |  | ) |  | Algorithm (A(`)) | LoC | T/S |"
                " Sample Reference | Sample Reference |  |\n| --- | --- | --- | --- | --- | "
                "--- | --- | --- | --- | --- | --- | --- |\n|  | Z |  | P | P |  |  |  |  |  "
                "|  |  |\n| Linear-Chain | Labeled Chain | Edges (TC^2 | Edges (TC^2 | Edges "
                "(TC^2 | ) | Forward-Backward, | 20 | 390k | (Lafferty et al., 2001) | (Laff"
                "erty et al., 2001) |  |\n|  |  |  |  |  |  | Viterbi |  |  |  |  |  |\n| Fact"
                "orial-HMM | Labeled Chains | Trans. | (LC^2 | (LC^2 | ) | Factorial F-B | 2"
                "0 | 25k | (Ghahramani | and | Jordan, |\n|  |  | Obs. | (TC^L | ) |  |  |  |"
                "  | 1996) |  |  |\n| Alignment | Alignment | Match (NM) | Match (NM) | Match"
                " (NM) | Match (NM) | DTW, CTC, | 50 | 13k | (Needleman | and Wunsch, | and "
                "Wunsch, |\n|  |  | Skips (2NM) | Skips (2NM) | Skips (2NM) | Skips (2NM) | N"
                "eedleman-Wunsch |  |  | 1970) |  |  |\n| Semi-Markov | Seg. Labels | Edges |"
                "  |  |  | Segmental F-B | 30 | 87k | (Baum and Petrie, 1966) | (Baum and Pe"
                "trie, 1966) | (Baum and Petrie, 1966) |\n|  |  | (NKC^2 | (NKC^2 | ) |  |  |"
                "  |  | (Sarawagi and Cohen, 2005) | (Sarawagi and Cohen, 2005) | (Sarawagi "
                "and Cohen, 2005) |\n| Context-Free | Labeled Tree | CF Rules (G) | CF Rules "
                "(G) | CF Rules (G) | CF Rules (G) | Inside-Outside CKY | 70 | 37k | (Kasami"
                ", 1966) |  |  |\n|  |  | Term. | (CN) | (CN) |  |  |  |  |  |  |  |\n| Simple"
                " CKY | Labeled Tree | Splits (CN^2 | Splits (CN^2 | Splits (CN^2 | ) | 0-th"
                " order CKY | 30 | 118k | (Kasami, 1966) |  |  |\n| Dependency | Proj. Tree |"
                " Arcs (N^2 | Arcs (N^2 | ) |  | Eisner Algorithm | 40 | 28k | (Eisner, 2000"
                ") |  |  |\n| Dependency (NP) | Non-Proj. Tree | Arcs (N^2 | Arcs (N^2 | ) | "
                " | Matrix-Tree | 40 | 1.1m | (Koo et al., 2007) | (Koo et al., 2007) |  |\n|"
                "  |  |  |  |  |  | Chiu-Liu (MAP) |  |  | (McDonald et al., 2005) | (McDona"
                "ld et al., 2005) | (McDonald et al., 2005) |\n| Auto-Regressive | Sequence |"
                " Preﬁx (C^N | Preﬁx (C^N | ) |  | Greedy Search, | 60 | - | (Tillmann and N"
                "ey, 2003) | (Tillmann and Ney, 2003) | (Tillmann and Ney, 2003) |\n|  |  |  "
                "|  |  |  | Beam Search |  |  |  |  |  |\n\nTable 1: Models and algorithms impl"
                "emented in Torch-Struct. Notation is developed in Section 5. Parts are desc"
                "ribed in terms of sequence lengths N,M, label size C, segment length K, and"
                " layers / grammar size L,G. Lines of code (LoC) is from the log-partition ("
                "A(`)) implementation. T/S is the tokens per second of a batched computation"
                ", computed with batch 32, N = 25,C = 20,K = 5,L = 3 (K80 GPU run on Google "
                "Colab).\nprediction is that many required algorithms are dif- ﬁcult to imple"
                "ment efﬁciently and correctly. Most projects reimplement custom versions of"
                " standard algorithms or focus particularly on a single well- deﬁned model c"
                "lass. This research style makes it difﬁcult to combine and try out new appr"
                "oaches, a problem that has compounded with the complexity of research in de"
                "ep structured prediction. With this challenge in mind, we introduce Torch- "
                "Struct with three speciﬁc contributions: •mains. Most ambitiously, Modulari"
                "ty: models are represented as distri- butions with a standard ﬂexible API i"
                "ntegrated into a deep learning framework. • Completeness: a broad array of "
                "classical algo- rithms are implemented and new models can easily be added i"
                "n Python. •motivating this approach with a case study. Efﬁciency: implement"
                "ations target computa- tional/memory efﬁciency for GPUs and the backend inc"
                "ludes extensions for optimization. 2007) or CRF++ (Kudo, 2005), implement i"
                "n- ference for a ﬁxed set of popular models, such as linear-chain CRFs. Gen"
                "eral-purpose inference libraries, such as PyStruct (M¨uller and Behnke, 201"
                "4) or TurboParser (Martins et al., 2010), uti- lize external solvers for (p"
                "rimarily MAP) inference such as integer linear programming solvers and ADMM"
                ". Probabilistic programming languages, for example languages that integrate"
                " with deep learn- ing such as Pyro (Bingham et al., 2019), allow for speciﬁ"
                "cation and inference over some discrete do- inference libraries such as Dyn"
                "a (Eisner et al., 2004) allow for declarative speciﬁcations of dynamic prog"
                "ramming algorithms to support inference for generic algorithms. Torch- Stru"
                "ct takes a different approach and integrates a library of optimized structu"
                "red distributions into a vectorized deep learning system. We begin by 3 Mot"
                "ivating Case Study\nIn this system description, we ﬁrst motivate the ap- pro"
                "ach taken by the library, then present a technical description of the metho"
                "ds used, and ﬁnally present several example use cases. 2 Related Work Sever"
                "al software libraries target structured pre- diction. Optimization tools, s"
                "uch as SVM- struct (Joachims, 2008), focus on parameter estima- tion. Model"
                " libraries, such as CRFSuite (Okazaki, While structured prediction is tradi"
                "tionally pre- sented at the output layer, recent applications have deployed"
                " structured models broadly within neural networks (Johnson et al., 2016; Ki"
                "m et al., 2017; Yogatama et al., 2016, inter alia). Torch-Struct aims to en"
                "courage this general use case. To illustrate, we consider a latent tree mod"
                "el. ListOps (Nangia and Bowman, 2018) is a dataset of mathematical function"
                "s. Each data point consists"
            ),
            (
                "of a preﬁx expression x and its result y, e.g.\nx = [ MAX 2 9 [ MIN 4 7 ] 0 ] "
                "y = 9\nModels such as a ﬂat RNN will fail to capture the hierarchical structure "
                "of this task. However, if a model can induce an explicit latent z, the parse tree"
                " of the expression, then the task is easy to learn by a tree-RNN model p(y | x,z)"
                " (Yogatama et al., 2016; Havrylov et al., 2019).\nA popular approach is a "
                "latent-tree"
                " RL model which we brieﬂy summarize. The objective is to maximize the probability "
                "of the correct predic- tion under the expectation of a prior tree model, p(z | x;"
                "\x00),\n| Figure | 2: | Latent | Tree | CRF | example. | (a) | Log- |\n| --- | "
                "--- | --- | --- | --- | --- | --- | --- |\n| "
                "potentials"
                " | ` | for | each | part/span. | (b) Marginals | (b) Marginals | for |\n| CRF(`) "
                "| computed by backpropagation. | computed by backpropagation. | computed by "
                "backpropagation. | computed by backpropagation. | (c) Mode | (c) Mode | tree |\n|"
                " argmaxz CRF(z;`). | argmaxz CRF(z;`). | argmaxz CRF(z;`). | (d) Sampled tree z |"
                " (d) Sampled tree z | ⇠ | CRF(`). | CRF(`). |\n\n4 Library Design\nO = Ez^⇠ p(z |"
                " x;\x00)[logp(y | z,x)] Computing the expectation is intractable so pol- icy "
                "gradient is used. First a tree is sampled ˜z ⇠ p(z | x;\x00), then the gradient "
                "with respect to \x00 is approximated as, @ @\x00 O ⇡ (logp(y | ˜z,x) \x00 b)( @ @"
                "\x00 p(z | x;\x00)) where b is a variance reduction baseline. A com- mon "
                "choice is "
                "the self-critical baseline (Rennie et al., 2017), b = logp(y | z⇤,x) with z⇤ = "
                "argmax z p(z | x;\x00) Finally an entropy regularization term is added to the "
                "objective "
                "encourage exploration of different trees, O + \x00H(p(z | x;\x00)). Even in this "
                "brief overview, we can see how complex a latent structured learning problem can "
                "be."
                " To compute these terms, we need 5 different properties of the tree model p(z | "
                "x;\x00): Sampling Policy gradient, ˜z ⇠ p(z | x;\x00) Density Score policy "
                "samples, p(z | x;\x00) Gradient Backpropagation,^@\x00 @ p(z | x;\x00) Argmax "
                "Self-critical, argmaxz p(z | x;\x00) Entropy Objective regularizer, H(p(z | "
                "x;\x00)) For structured models, each of these terms is non- trivial to compute. "
                "A goal of Torch-Struct is to make it seamless to deploy structured models for "
                "these complex settings. To demonstrate this, Torch- Struct includes an "
                "implementation of this latent- tree approach. With a minimal amount of user "
                "code, "
                "the implementation achieves near perfect accuracy on the ListOps dataset. The "
                "library design of Torch-Struct follows the dis- tributions API used by both "
                "TensorFlow and Py- Torch (Dillon et al., 2017). For each structured model in the "
                "library, we deﬁne a conditional ran- dom ﬁeld (CRF) distribution object. From a "
                "user’s standpoint, this object provides all necessary distri- butional "
                "properties. "
                "Given log-potentials (scores) output from a deep network `, the user can request "
                "samples z ⇠ CRF(`), probabilities CRF(z;`), modes argmaxz CRF(`), or other "
                "distributional properties such as H(CRF(`)). The library is ag- nostic to how "
                "these are utilized, and when possible, they allow for backpropagation to update "
                "the in- put network. The same distributional object can be used for standard "
                "output"
                " prediction as for more complex operations like attention or reinforcement "
                "learning"
                ". Figure 2 demonstrates this API for a binary tree CRF over an ordered sequence, "
                "such as p(z | y;\x00) from the previous section. The distribution takes in "
                "log-potentials ` which score each possible span in the input. The distribution "
                "converts these to proba- bilities of a speciﬁc tree. This distribution can be "
                "queried for predicting over the set of trees, sam- pling a tree for model "
                "structure, or even computing entropy over all trees. Table 1 shows all of the "
                "structures and distribu- tions implemented in Torch-Struct. While each is "
                "internally implemented using different specialized algorithms and optimizations, "
                "from the user’s per- spective they all utilize the same external distribu- tional"
                " API, and pass a generic set of distributional tests.^1 This approach hides the "
                "internal complexity 1 The test suite for each distribution enumerates over all "
                "structures to ensure that properties hold. While this is in- tractable for "
                "large spaces, it can be done for small sets and"
            ),
        ]
        output = convert_output_to_str_by_page(self.extract_output_multi_page)
        self.assertEqual(output, expected_output)

    def test__construct_table_from_cells(self) -> None:
        # Test spanning cell
        table_cells = [
            ContentModel(
                uid="7",
                type="TABLE_CELL",
                content="Kensho Revenue in millions $",
                children=[],
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
            ContentModel(
                uid="9",
                type="TABLE_CELL",
                content="Q2",
                children=[],
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
            ContentModel(
                uid="10",
                type="TABLE_CELL",
                content="Q3",
                children=[],
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
            ContentModel(
                uid="11",
                type="TABLE_CELL",
                content="Q4",
                children=[],
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
            ContentModel(
                uid="12",
                type="TABLE_CELL",
                content="2020",
                children=[],
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
            ContentModel(
                uid="13",
                type="TABLE_CELL",
                content="100,000",
                children=[],
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
            ContentModel(
                uid="14",
                type="TABLE_CELL",
                content="200,000",
                children=[],
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
            ContentModel(
                uid="15",
                type="TABLE_CELL",
                content="300,000",
                children=[],
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
            ContentModel(
                uid="16",
                type="TABLE_CELL",
                content="400,000",
                children=[],
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
            ContentModel(
                uid="17",
                type="TABLE_CELL",
                content="2021",
                children=[],
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
            ContentModel(
                uid="18",
                type="TABLE_CELL",
                content="101,001",
                children=[],
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
            ContentModel(
                uid="19",
                type="TABLE_CELL",
                content="201,001",
                children=[],
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
            ContentModel(
                uid="20",
                type="TABLE_CELL",
                content="301,001",
                children=[],
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
            ContentModel(
                uid="21",
                type="TABLE_CELL",
                content="401,001",
                children=[],
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
            ContentModel(
                uid="22",
                type="TABLE_CELL",
                content="2022",
                children=[],
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
            ContentModel(
                uid="23",
                type="TABLE_CELL",
                content="102,004",
                children=[],
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
            ContentModel(
                uid="24",
                type="TABLE_CELL",
                content="202,004",
                children=[],
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
            ContentModel(
                uid="25",
                type="TABLE_CELL",
                content="302,004",
                children=[],
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
            ContentModel(
                uid="26",
                type="TABLE_CELL",
                content="402,004",
                children=[],
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
            ContentModel(
                uid="27",
                type="TABLE_CELL",
                content="2023",
                children=[],
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
            ContentModel(
                uid="28",
                type="TABLE_CELL",
                content="103,009",
                children=[],
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
            ContentModel(
                uid="29",
                type="TABLE_CELL",
                content="203,009",
                children=[],
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
            ContentModel(
                uid="30",
                type="TABLE_CELL",
                content="303,009",
                children=[],
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
            ContentModel(
                uid="31",
                type="TABLE_CELL",
                content="403,009",
                children=[],
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
        uid_to_index = {
            "7": (0, 0),
            "9": (0, 2),
            "10": (0, 3),
            "11": (0, 4),
            "12": (1, 0),
            "13": (1, 1),
            "14": (1, 2),
            "15": (1, 3),
            "16": (1, 4),
            "17": (2, 0),
            "18": (2, 1),
            "19": (2, 2),
            "20": (2, 3),
            "21": (2, 4),
            "22": (3, 0),
            "23": (3, 1),
            "24": (3, 2),
            "25": (3, 3),
            "26": (3, 4),
            "27": (4, 0),
            "28": (4, 1),
            "29": (4, 2),
            "30": (4, 3),
            "31": (4, 4),
        }
        uid_to_span = {
            "7": (1, 2),
            "9": (1, 1),
            "10": (1, 1),
            "11": (1, 1),
            "12": (1, 1),
            "13": (1, 1),
            "14": (1, 1),
            "15": (1, 1),
            "16": (1, 1),
            "17": (1, 1),
            "18": (1, 1),
            "19": (1, 1),
            "20": (1, 1),
            "21": (1, 1),
            "22": (1, 1),
            "23": (1, 1),
            "24": (1, 1),
            "25": (1, 1),
            "26": (1, 1),
            "27": (1, 1),
            "28": (1, 1),
            "29": (1, 1),
            "30": (1, 1),
            "31": (1, 1),
        }
        table = _construct_table_from_cells(table_cells, uid_to_index, uid_to_span)
        expected_table = [
            [
                "Kensho Revenue in millions $",
                "Kensho Revenue in millions $",
                "Q2",
                "Q3",
                "Q4",
            ],
            ["2020", "100,000", "200,000", "300,000", "400,000"],
            ["2021", "101,001", "201,001", "301,001", "401,001"],
            ["2022", "102,004", "202,004", "302,004", "402,004"],
            ["2023", "103,009", "203,009", "303,009", "403,009"],
        ]
        self.assertEqual(table, expected_table)
