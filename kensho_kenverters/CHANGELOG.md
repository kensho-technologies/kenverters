# Changelog

## v3.1.0

### Added

* Add `convert_output_to_header_tree` function to `convert_output` to build a header content tree from the Extract output. Each heading (TITLE, H1-H5) becomes a tree node with `children` (sub-headings) and `contents` (non-heading segments such as paragraphs and tables).

## v3.0.0

### Changed

* Change the convert_output_to_items_list to convert_output_to_items_list_and_relations
* Change the output from convert_output_to_items_list_and_relations to be data class. 

### Added

* Add content_id to the items from convert_output_to_items_list_and_relations.
* Add relations between items to the output from convert_output_to_items_list_and_relations.  

## v2.1.0

### Added

* Add support of image type.  

## v2.0.0

* Add parsing of table structure.  

## v1.3.0

* Add support of new figure types. 

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
