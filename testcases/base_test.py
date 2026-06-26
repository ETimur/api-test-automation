"""Base test class with shared assertions."""
import allure
from utils.schema_validator import validate_response_schema


class BaseTest:
    """Base test class providing common assertion methods."""

    def _assert_standard_json_response(self, response, schema: str = None,
                                        expected_status: int = 200):
        """Assert standard JSON response: status code, content-type, optional schema."""
        with allure.step(f"Assert status code is {expected_status}"):
            assert response.status_code == expected_status, \
                f"Expected {expected_status}, got {response.status_code}: {response.text}"

        with allure.step("Assert Content-Type is application/json"):
            content_type = response.headers.get("Content-Type", "")
            assert "application/json" in content_type, \
                f"Expected JSON content-type, got: {content_type}"

        if schema:
            with allure.step(f"Validate response against schema: {schema}"):
                is_valid, error = validate_response_schema(response.json(), schema)
                assert is_valid, f"Schema validation failed: {error}"

    def validate_response_json(self, response, expected_fields: dict):
        """Validate specific fields in response JSON."""
        data = response.json()
        for key, expected_value in expected_fields.items():
            with allure.step(f"Validate field '{key}' == '{expected_value}'"):
                actual_value = data.get(key)
                assert actual_value == expected_value, \
                    f"Field '{key}': expected '{expected_value}', got '{actual_value}'"
