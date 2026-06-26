"""Patient CRUD test suite."""
import allure
import pytest
from testcases.base_test import BaseTest
from pages.EHR.patient_page import PatientApiPage
from utils.helper import random_suffix


@allure.feature("Patient")
@allure.story("Patient CRUD")
class TestPatientCRUD(BaseTest):
    """Patient create, read, search, update tests."""

    patient_id = None

    @pytest.fixture(autouse=True)
    def setup(self, base_url, auth_headers):
        self.patient_page = PatientApiPage(base_url)
        self.headers = auth_headers

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.sanity
    @pytest.mark.order(1)
    def test_create_patient(self):
        """Create a new patient."""
        suffix = random_suffix()
        resp, payload = self.patient_page.create_patient(
            self.headers,
            first_name=f"QA",
            last_name=f"AutoTest_{suffix}",
            email=f"qa.auto.{suffix}@example.com",
        )

        self._assert_standard_json_response(
            resp, schema="Patient/create_patient.json"
        )

        data = resp.json()
        assert data["first_name"] == "QA"
        TestPatientCRUD.patient_id = data["id"]

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.sanity
    @pytest.mark.order(2)
    def test_get_patient_by_id(self):
        """Retrieve patient by ID."""
        assert self.patient_id, "No patient_id from previous test"

        resp = self.patient_page.get_patient(self.headers, self.patient_id)
        self._assert_standard_json_response(resp)
        assert resp.json()["id"] == self.patient_id

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.order(3)
    def test_search_patient(self):
        """Search for patient by name."""
        assert self.patient_id, "No patient_id from previous test"

        resp = self.patient_page.search_patients(self.headers, "QA AutoTest")
        self._assert_standard_json_response(resp)
        results = resp.json()
        assert len(results) > 0, "Search returned no results"

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.order(4)
    def test_update_patient_phone(self):
        """Update patient phone number."""
        assert self.patient_id, "No patient_id from previous test"

        resp = self.patient_page.update_patient(
            self.headers, self.patient_id, phone="555-9999"
        )
        self._assert_standard_json_response(resp)
        assert resp.json()["phone"] == "555-9999"
