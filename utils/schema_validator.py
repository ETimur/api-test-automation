"""JSON Schema validation utilities."""
import json
import os
from jsonschema import validate, ValidationError
from typing import Tuple


SCHEMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schemas")


def validate_response_schema(response_json: dict, schema_path: str) -> Tuple[bool, str]:
    """Validate response JSON against a schema file.
    
    Args:
        response_json: The response body as dict
        schema_path: Relative path to schema file (e.g., "Calendar/create_appointment.json")
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    full_path = os.path.join(SCHEMA_DIR, schema_path)

    if not os.path.exists(full_path):
        return False, f"Schema file not found: {full_path}"

    with open(full_path, "r") as f:
        schema = json.load(f)

    try:
        validate(instance=response_json, schema=schema)
        return True, ""
    except ValidationError as e:
        return False, f"Schema validation failed: {e.message}"
