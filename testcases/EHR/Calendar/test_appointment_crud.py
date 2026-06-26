"""Appointment CRUD test suite."""
import os
import allure
import pytest
from testcases.base_test import BaseTest
from pages.EHR.calendar_page import CalendarApiPage
from utils.helper import iso_z, future_datetime


@allure.feature("Calendar")
@allure.story("Appointment CRUD")
class TestAppointmentCRUD(BaseTest):
    """E2E appointment lifecycle: create → view → cancel."""

    appointment_id = None

    @pytest.fixture(autouse=True)
    def setup(self, base_url, auth_headers, facility_id, provider_id):
        self.calendar = CalendarApiPage(base_url)
        self.headers = auth_headers
        self.facility_id = facility_id
        self.provider_id = provider_id

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.sanity
    @pytest.mark.order(1)
    def test_create_appointment(self):
        """Create appointment and validate response schema."""
        future = future_datetime(hours=24)
        resp, payload = self.calendar.create_appointment(
            self.headers,
            patient_id="test-patient-001",
            facility_id=self.facility_id,
            provider_id=self.provider_id,
            start_datetime=iso_z(future),
        )

        self._assert_standard_json_response(
            resp, schema="Calendar/create_appointment.json"
        )

        self.validate_response_json(resp, expected_fields={
            "appointment_status": "SCHEDULED",
        })

        TestAppointmentCRUD.appointment_id = resp.json()["id"]

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.sanity
    @pytest.mark.order(2)
    def test_view_appointment_in_calendar(self):
        """Verify created appointment appears in filtered view."""
        assert self.appointment_id, "No appointment_id from previous test"

        future = future_datetime(hours=24)
        resp = self.calendar.get_appointments(
            self.headers,
            provider_id=self.provider_id,
            facility_id=self.facility_id,
            start_datetime=iso_z(future),
            end_datetime=iso_z(future),
        )

        self._assert_standard_json_response(
            resp, schema="Calendar/filter_appointments.json"
        )

        appointments = resp.json()["appointments"]
        matched = next(
            (a for a in appointments if a["id"] == self.appointment_id), None
        )
        assert matched is not None, f"Appointment {self.appointment_id} not found"
        assert matched["appointment_status"] == "SCHEDULED"

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.sanity
    @pytest.mark.order(3)
    def test_cancel_appointment(self):
        """Cancel appointment (cleanup — never hard-delete)."""
        assert self.appointment_id, "No appointment_id from previous test"

        resp = self.calendar.cancel_appointment(self.headers, self.appointment_id)

        with allure.step("Verify cancellation"):
            assert resp.status_code == 200
            assert resp.json()["appointment_status"] == "CANCELLED"
