# Copyright 2024-present Kensho Technologies, LLC.
"""Helper functions useful across modules."""

from logging import getLogger
from typing import Any

# pylint: disable=no-name-in-module
from pydantic_core._pydantic_core import ValidationError as PydanticValidationError

from kensho_kenverters.extract_output_models import ExtractOutputModel

logger = getLogger(__name__)


def load_output_to_pydantic(serialized_document: dict[str, Any]) -> ExtractOutputModel:
    """Convert output JSON format to pydantic model."""
    try:
        return ExtractOutputModel(**serialized_document)
    except PydanticValidationError as e:
        logger.error("Error parsing output due to its format. Please check the format.")
        raise e
