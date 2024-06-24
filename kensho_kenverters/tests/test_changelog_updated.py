"""A template used to add a changelog updated test."""

import os
import re
import unittest
from importlib import metadata

_version_pattern = re.compile(r"## v(\d+\.\d+\.\d+)")
package_name = "kensho_kenverters"


class ChangelogTests(unittest.TestCase):
    def test_changelog_updated_after_version_bump(self) -> None:
        changelog_start_found = False
        inside_changelog = False

        changelog_lines = []

        changelog_file_path = os.path.join(package_name, "CHANGELOG.md")
        with open(changelog_file_path, "r") as f:
            changelog = f.readlines()

        for line in changelog:
            stripped_line = line.strip()
            if stripped_line == "# Changelog":
                # Found the start of the changelog.
                changelog_start_found = True
                inside_changelog = True
            elif stripped_line.startswith("# "):
                # Found the start of another top-level section.
                inside_changelog = False
            elif inside_changelog:
                # Found a line that is inside the changelog.
                changelog_lines.append(stripped_line)

        # Checks to ensure the changelog is adequately parsed.
        self.assertTrue(changelog_start_found)
        self.assertGreater(len(changelog_lines), 0)

        versions_in_changelog: set[str] = set()
        versions_in_changelog_in_order = []  # For readability on error printout
        for changelog_line in changelog_lines:
            match = _version_pattern.fullmatch(changelog_line)
            if match is not None:
                found_version = match.group(1)

                # Ensure there are no duplicate versions in the changelog.
                self.assertNotIn(found_version, versions_in_changelog)
                versions_in_changelog.add(found_version)
                versions_in_changelog_in_order.append(found_version)

        # Ensure that the latest version in the changelog is the current package version
        latest_changelog_version = versions_in_changelog_in_order[0]
        current_package_version = metadata.version(package_name)
        self.assertEqual(
            current_package_version,
            latest_changelog_version,
            msg=(
                f"The latest CHANGELOG entry is not for version {current_package_version}, "
                "the current version of the package in pyproject.toml. "
                "Please remember to update the latest entry in the CHANGELOG to include a "
                "description of your changes. "
                f"Latest version found: {latest_changelog_version}. "
                f"All versions mentioned in CHANGELOG: {versions_in_changelog_in_order}."
            ),
        )
