"""Dynamic payload builder from JSON templates."""
import json
import os
import copy
from typing import Any, Dict
from utils.helper import random_suffix, iso_z, future_datetime


TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data")


class ApiRequestDataHandler:
    """Load and modify request payloads from templates."""

    def __init__(self, template_file: str):
        path = os.path.join(TEST_DATA_DIR, template_file)
        with open(path, "r") as f:
            self._templates = json.load(f)

    def get_payload(self, key: str) -> Dict[str, Any]:
        """Get a fresh copy of a payload template."""
        if key not in self._templates:
            raise KeyError(f"Template '{key}' not found in data file")
        return copy.deepcopy(self._templates[key])

    def get_modified_payload(self, key: str, **overrides) -> Dict[str, Any]:
        """Get payload with field overrides applied."""
        payload = self.get_payload(key)
        for field, value in overrides.items():
            if "." in field:
                # Support nested fields: "patient.name" -> payload["patient"]["name"]
                parts = field.split(".")
                obj = payload
                for part in parts[:-1]:
                    obj = obj.setdefault(part, {})
                obj[parts[-1]] = value
            else:
                payload[field] = value
        return payload
