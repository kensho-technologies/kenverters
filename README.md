# Kenverters: Kensho Extract Translators

Welcome to Kenverters! This project is a set of conversion tools for the output from Kensho Extract. It'll help you take the output JSON from Extract and convert it to different formats for your downstream use cases. Think text for RAGs, pandas tables for extracting tabular data, markdown for rendering, and more.

For documentation on how to use the Extract API to parse your documents, visit https://docs.kensho.com/extract. If you plan to use locations in your output - for example, to organize output by page - uncomment `params["output_format"] = "structured_document_with_locations"` when using the API. Once you receive the JSON output, you can pass it as the `serialized_document` arg for any of the conversion functions to get your converted output. Note: If your output JSON has keys `['error', 'metadata', 'output', 'status']`, pass the value for the `'output'` key as `serialized_document`. Otherwise, if the output directly has the keys `['annotations', 'content_tree']`, just pass in the output as-is.

We welcome contributions from the community. Additionally, if you have a suggestion for a new adapter for a particular use case, feel free to reach out, but please note that our decision to devote development time is at our sole discretion.

Any questions or suggestions can be sent to kenverters-maintainer@kensho.com. Happy document processing!

# Setup

## Option 1: PyPI (Recommended)

You can install kenverters on [PyPI](https://pypi.org/project/kensho-kenverters/) via 

`pip install kensho-kenverters`

## Option 2: From Repo

For setup from the repo itself, we recommend using [Poetry](https://python-poetry.org/). Within the cloned repo, simply run in the terminal:

```poetry install```

You can now activate the environment within the terminal with

```poetry shell```

It will also print out the path where Poetry installed the virtual environment.

# Usage

## Conversion to Items

To convert the output to a list of paragraphs, titles, and tables represented as dictionaries, use `convert_output_to_items_list` in `convert_output.py`. It will return a list of dictionaries representing a text, title, or table. It converts tables to markdown using `table_to_markdown` under the hood.

To use: 
```python
from kensho_kenverters.convert_output import convert_output_to_items_list
```

Function definition:

```python
def convert_output_to_items_list(
    serialized_document: dict[str, Any], return_locations: bool = False
) -> list[dict[str, Any]]:
    """Convert Extract output into a list of items representing the different document entitites.

    Args:
        serialized_document: a serialized document
        return_locations: whether to return segment locations in the result

    Returns:
            a list of dictionaries representing a "segment".
                If an item is a text or title entity, it will contain keys:
                    1) "category" equal to "text" or "title"
                    2) "text" containing the text
                    If return_locations:
                        3) "locations" containing the locations as a list of location dictionaries

                If an item is a table, it will contain keys:
                    1) "category" equal to "table"
                    2) "text" containing the markdown version of the table cell texts
                    3) "table" containing the 2D grid of table texts
                    If return_locations:
                        4) "locations" containing the locations as a list of location dictionaries
    """
```


## Full Text Extraction

To get all the text output as a single string, use `convert_output_to_str` in `convert_output.py`. It will return each separate item (paragraph, title, or table) with \n as a delimiter, and all the text within tables will be represented in a markdown-style format.

To get the text output as a string per page, use `convert_output_to_str_by_page` in `convert_output.py`. This will give you a list of full-page outputs as strings.

To use: 
```python
from kensho_kenverters.convert_output import convert_output_to_str_by_page
```

Function definition:

```python
def convert_output_to_str(serialized_document: dict[str, Any]) -> str:
    """Convert entire Extract output into a single string.

    Args:
        serialized_document: a serialized document

    Returns:
        full text string of the document with markdown-style tables using | as a delimiter
    """
```

```python
def convert_output_to_str_by_page(serialized_document: dict[str, Any]) -> list[str]:
    """Convert entire Extract output into a single string by page.

    Args:
        serialized_document: a serialized document

    Returns:
        a list of full text strings of the document by page with markdown-style tables 
            using | as a delimiter.
    
    Example Output:
        [
            'Random Title for the First Page\nThis page is about things.', 
            'Page 2: Another Title.\nThis page is not about things.', 
            'Supplementary materials found here\n|T|L|'
        ]
    """
```


## Markdown Conversion

To convert all text from a document into markdown, use `convert_output_to_markdown` in `convert_output.py`. It will return a string output with # before each title and a markdown representation of each table, using the | delimiter between cells.
To convert all text from each page into markdown, use `convert_output_to_markdown_by_page` in `convert_output.py`. It will return a list of string outputs representing each page.
To convert a specific table to markdown format, use `table_to_markdown` in `convert_output.py`.

To use: 
```python
from kensho_kenverters.convert_output import convert_output_to_markdown, convert_output_to_markdown_by_page, table_to_markdown
```

Function definition:

```python
def convert_output_to_markdown(serialized_document: dict[str, Any]) -> str:
    """Convert entire Extract output into a single markdown string.

        Args:
            serialized_document: a serialized document

        Returns:
            full text string of the document with markdown-style tables using | as a delimiter 
            and titles prefaced with #
    """
```

```python
def convert_output_to_markdown_by_page(serialized_document: dict[str, Any]) -> list[str]:
    """Convert entire Extract output into a markdown string per page.

    Args:
        serialized_document: a serialized document

    Returns:
        list of full text strings of the document by page with markdown-style tables using | 
        as a delimiter and titles prefaced with #
    
    Example Output:
        [
            '# Random Title for the First Page\nThis page is about things.', 
            '# Page 2: Another Title.\nThis page is not about things.', 
            'Supplementary materials found here\n|T|L|'
        ]
    """
```

```python
def table_to_markdown(table: list[list[str]]) -> str:
    """Convert 2D grid table to a single string with | as a delimiter."""
```


## Table Extraction

To extract all tables from the output, you have the following options in `output_to_tables.py`: 

- `build_table_grids` will return a dictionary mapping a table ID to a list of lists containing the cell contents (2D grid of strings).
- `extract_pd_dfs_from_output` will return a list of pandas DataFrame representations of each table. It uses `build_table_grids` under the hood and converts the values to pandas DataFrames. The order of the tables is preserved.
- `extract_pd_dfs_with_locs_from_output` will return a list of NamedTuples consisting of a pandas DataFrame representation of the table and the location(s) of the table on the page. The `df` attribute will give you the table and the `locations` attribute will you give a list of dictionaries consisting of the x0, y0, height, and width relative to the page size as well as the page number. The order of the tables is preserved.

To use: 
```python
from kensho_kenverters.output_to_tables import build_table_grids, extract_pd_dfs_from_output, extract_pd_dfs_with_locs_from_output
```

Function definition:

```python
def build_table_grids(
    serialized_document: dict[str, Any], duplicate_merged_cells_content_flag: bool = True
) -> dict[str, list[list[str]]]:
    """Convert serialized tables to a 2D grid of strings.

    Args:
        serialized_document: a serialized document
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells. 
            If False, only fill the first cell (top left) of the merged area, other cells are empty.

    Returns:
        a mapping of table UIDs to table grid structures

    Example Output:
        {
            '1': [['header1', 'header2'], ['row1_val', 'row2_val']], 
            '2': [['another_header1'], ['another_row1_val']]
        }
    """
```

```python
def extract_pd_dfs_from_output(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
    use_first_row_as_header: bool = True,
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
```

```python
def extract_pd_dfs_with_locs_from_output(
    serialized_document: dict[str, Any],
    duplicate_merged_cells_content_flag: bool = True,
    use_first_row_as_header: bool = True,
) -> list[Table]:
    """Extract Extract output's tables and convert them to a list of pandas DataFrames and table 
    locations.

    Args:
        serialized_document: a serialized document
        duplicate_merged_cells_content_flag: if True, duplicate cell content for merged cells. 
            If False, only fill the first cell (top left) of the merged area, other cells are 
            empty.
        use_first_row_as_header: if True, use the first row of the extracted table as the columns. 
            Set to False if you know there is no header row in your tables.

    Returns:
        a list of Table NamedTuples with a pandas DataFrame and locations

    Example Output:
        [Table(
            df=Kensho Revenue in millions $       Q1       Q2       Q3       Q4
                0                         2020  100,000  200,000  300,000  400,000
                1                         2021  101,001  201,001  301,001  401,001
                2                         2022  102,004  202,004  302,004  402,004
                3                         2023  103,009  203,009  303,009  403,009,
            locations=[
                {'height': 0.09188, 'width': 0.66072, 'x': 0.16008, 'y': 0.40464, 'page_number': 0}
            ]
        )]
    """
```

## Organized Sections

If you would like to get a list of sections in a document, you can use `extract_organized_sections` in `output_to_sections.py`. It will return a list of lists containing document segments (title, table, or text). Sections are divided by titles, and everything is returned in the predicted reading order. `convert_output_to_items_list` is used under the hood to get the list of document segments before splitting into sections.

To use: 
```python
from kensho_kenverters.output_to_sections import extract_organized_sections
```

Function definition:

```python
def extract_organized_sections(serialized_document: dict[str, Any]) -> list[list[dict[str, Any]]]:
    r"""Return a version of the output organized into sections split on titles.

    Args:
        serialized_document: a serialized document
    Returns:
        a list of sections, each of which is a list of items within that section in dictionary 
            form describing their category and text value

    Example Output:
        [[
            {
                'category': 'title', 
                'text': 'ESTIMATE for Kensho'
            },
            {
                'category': 'table',
                'table': [
                    ['Kensho Revenue in millions $', 'Q1', 'Q2', 'Q3', 'Q4'], 
                    ['2020', '100,000', '200,000', '300,000', '400,000']
                ],
                'text': '\n| Kensho Revenue in millions $ | Q1 | Q2 | Q3 | Q4 |\n| 2020 | '
                        '100,000 | 200,000 | 300,000 | 400,000 |\n'
            },
            {
                'category': 'text', 
                'text': 'Machine learning (ML)'
            }
        ]]
    """
```

## Visually Formatted Text

If you would like to get visually-formatted text for each page, you can use `convert_output_to_str_formatted` in `convert_output_visual_formatted.py`. It will return a list of strings, each one containing the text in the page with spaces and line breaks simulating the original white space between the different segments. 

How this will look will depend on your downstream use case or file viewer. Adjusting `page_width` and `page_height` to match the canvas size will improve results. `resize` will allow for attempting to override your given overall width and height if it would cut off any words. In the case where you require a specific size regardless of if all words fit, set `resize` to False. Otherwise, allowing the function to find a suitable size will retain all words and segments.

To use: 
```python
from kensho_kenverters.convert_output_visual_formatted import convert_output_to_str_formatted
```

Function definition:

```python
def convert_output_to_str_formatted(
    serialized_document: dict[str, Any],
    page_width: int = 500,
    page_height: int = 100,
    resize: bool = True,
) -> list[str]:
    """Convert entire Extract output into a string per page with spaces and newlines to make the 
    printed output resemble the page layout.

    Args:
        serialized_document: a serialized document
        page_width: the max number of characters in a printed line
        page_height: the max lines in a printed document representation
        resize: if the given page_width and page_height would cut off any segment, 
            allow for overriding those values (resizing the output). Setting this to False will 
            enforce the width and height of the output and will truncate any words that spill over.

    Returns:
        full text string for each page
    
    Example Output:

                                                                Valerie
                                                          123 The Street
                                                           Somewhere, XX
        
        Dear Reader,

        I am writing to you from somewhere! Here's an important table:

                        Item        Favorite

                        Animal      Duck
                        Color       Red
                        Reader      You

        
        Thanks for reading!

        Lots of love,


            Valerie
    """
```

# License

Licensed under the Apache 2.0 License. Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Copyright 2024-present Kensho Technologies, LLC. The present date is determined by the timestamp of the most recent commit in the repository.

