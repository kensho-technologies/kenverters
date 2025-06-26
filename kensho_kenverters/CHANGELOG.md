# Changelog

## v1.2.9

* Fixed bug for creating figure extraction segments in convert_output_to_items_list 

## v1.2.8

* Fixing edge case where we want to build a table with only figure extracted table annotations or only table annotations
* Making build_content_grid_from_figure_extracted_table_cell_annotations public

## v1.2.7

* Fixing PyPI version mismatch - no code changes

## v1.2.6

* Another addition to enable FIGURE types

## v1.2.5

* Add handling for FIGURE types in Extract output

## v1.2.4

* Add conversion from a given table annotation to grid, finding the first and last associated text object
* Fix markdown table bug by adding an extra newline before and after the table text

## v1.2.3

* Remove table validation for rows and columns to not fail downstream of Extract model failures
* Added support of figure extracted table.

## v1.2.2

* Use underscores instead of hyphens for setuptools 78

## v1.2.1

* Bug fix for spanning cells at the outer edge of a table

## v1.2.0

* Add support for heirarchical_v2 model output

## v1.1.0

* Add support for structured_output_with_character_offsets output format from Extract

## v1.0.1

* Fix tables to markdown bug where tables were not converting to markdown properly

## v1.0.0

* Synchronizing the version number with the pypi release number

## v0.0.2

* Allowing for empty tables found in the output

## v0.0.1

* Initializing first open sourced version of Kenverters
