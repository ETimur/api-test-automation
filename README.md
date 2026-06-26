# 🔌 API Test Automation Framework

Production-grade API testing framework for RESTful healthcare APIs using Python + pytest + Allure.

## 🏗️ Architecture

```
├── testcases/                      # Test suites organized by domain
│   ├── EHR/
│   │   ├── Calendar/               # Appointment scheduling APIs
│   │   ├── Patient/                # Patient CRUD APIs
│   │   └── Billing/                # Billing & insurance APIs
│   ├── Auth/                       # Authentication & authorization
│   └── base_test.py               # Base test class with shared assertions
├── pages/                          # API Page Objects (request builders)
│   ├── base_page.py               # Base with HTTP methods & auth
│   ├── login_api_page.py          # Authentication endpoint
│   ├── EHR/
│   │   ├── calendar_page.py       # Calendar API endpoints
│   │   └── patient_page.py        # Patient API endpoints
├── schemas/                        # JSON Schema validation files
│   ├── Calendar/
│   │   ├── create_appointment.json
│   │   └── filter_appointments.json
│   └── Patient/
│       └── create_patient.json
├── test_data/                      # Request payload templates
│   ├── calendar.json
│   └── patient.json
├── utils/
│   ├── api_request_data_handler.py # Dynamic payload builder
│   ├── helper.py                   # Common utilities (iso_z, random_suffix)
│   ├── schema_validator.py         # JSON Schema validation
│   └── request_handler.py         # HTTP request wrapper with logging
├── configs/
│   ├── staging.ini                # Staging environment
│   └── production.ini            # Production environment
├── conftest.py                    # Fixtures & test configuration
├── pytest.ini
└── requirements.txt
```

## ✨ Key Features

- **API Page Object Pattern** — Clean separation of endpoint logic from assertions
- **JSON Schema Validation** — Every response validated against defined schemas
- **Dynamic Payload Builder** — Template-based request data with runtime overrides
- **Data Safety Rules** — Never delete shared resources; cancel/archive only
- **Allure Integration** — Rich reports with request/response bodies
- **Retry Logic** — Slot-retry for appointment booking (handles scheduling conflicts)
- **Cross-Environment** — Run against staging/production with config switch
- **CI-Ready** — Parallel execution with proper test isolation

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest testcases/ -v --alluredir=reports/allure-results

# Run specific domain
pytest testcases/EHR/Calendar/ -v

# Run sanity only
pytest testcases/ -m sanity

# Generate report
allure serve reports/allure-results
```

## 🔧 Sample API Page Object

```python
from pages.base_page import BasePage
from utils.request_handler import RequestHandler

class CalendarApiPage(BasePage):
    """API page object for Calendar/Appointment endpoints."""

    def create_appointment(self, request_data, headers, **overrides):
        """Create an appointment with slot-retry logic.
        
        Returns (response, payload) tuple.
        Performs NO assertions — caller validates.
        """
        payload = request_data.get_modified_payload(
            "post_create_appointment_v3", **overrides
        )

        for attempt in range(32):  # Retry with next available slot
            resp = RequestHandler.post(
                request_path="/v1/ehr/appointments/v3/create",
                headers=headers,
                json_data=payload,
            )
            if resp.status_code == 200:
                return resp, payload
            if resp.status_code == 400 and "already exists" in resp.text:
                payload = self._next_slot(payload)
                continue
            return resp, payload

        return resp, payload

    def get_appointments(self, headers, provider_id, facility_id, 
                         start_datetime, end_datetime):
        """GET filtered appointments from calendar."""
        params = {
            "provider_id": provider_id,
            "facility_id": facility_id,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        }
        return RequestHandler.get(
            request_path="/v1/ehr/appointments/v3",
            headers=headers,
            params=params,
        )
```

## 📄 Sample Test

```python
import allure
import pytest
from testcases.base_test import BaseTest

class TestAppointmentE2E(BaseTest):
    """E2E appointment lifecycle: create → view → check-in → cancel."""

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.sanity
    @pytest.mark.order(1)
    def test_create_appointment(self):
        """Create appointment and validate response schema."""
        resp, payload = self.calendar_page.create_appointment(
            self.request_data,
            self.headers,
            patient_id=self.patient_id,
            facility_id=self.facility_id,
            provider_id=self.provider_id,
        )

        with allure.step("Validate 200 + JSON headers + schema"):
            self._assert_standard_json_response(
                resp, schema="Calendar/create_appointment.json"
            )

        with allure.step("Validate response fields"):
            self.validate_response_json(resp, expected_fields={
                "patient_id": self.patient_id,
                "appointment_status": "SCHEDULED",
            })

        self.__class__.appointment_id = resp.json()["id"]

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.sanity
    @pytest.mark.order(2)
    def test_view_appointment_in_calendar(self):
        """Verify created appointment appears in filtered calendar view."""
        resp = self.calendar_page.get_appointments(
            self.headers,
            provider_id=self.provider_id,
            facility_id=self.facility_id,
            start_datetime=self.start_date,
            end_datetime=self.end_date,
        )

        with allure.step("Validate response"):
            self._assert_standard_json_response(resp, schema="Calendar/filter.json")

        with allure.step("Verify appointment in list"):
            appointments = resp.json()["appointments"]
            matched = next(
                (a for a in appointments if a["id"] == self.appointment_id), None
            )
            assert matched is not None, f"Appointment {self.appointment_id} not found"
            assert matched["appointment_status"] == "SCHEDULED"
```

## 📊 Test Coverage

| Domain | Endpoints | Tests | Pass Rate |
|--------|-----------|-------|-----------|
| Calendar | 8 | 24 | 98% |
| Patient | 6 | 18 | 100% |
| Auth | 4 | 12 | 100% |
| Billing | 5 | 15 | 95% |
| **Total** | **23** | **69** | **98.2%** |

## 🛠️ Tech Stack

- **Python 3.10+** — Test language
- **pytest** — Framework with ordering & markers
- **requests** — HTTP client
- **jsonschema** — Response validation
- **Allure** — Reporting
- **GitHub Actions** — CI/CD

## 📋 Data Safety Rules

1. NEVER delete patients — they are inert
2. Appointments are CANCELLED, not deleted
3. Only cancel resources created in the current test run
4. Teardown failures log and continue, never raise
5. Staging is shared — never bulk-delete by prefix

## 📝 Product Context

Built for **HealthNote - AI**, an AI-powered healthcare platform with EHR integration, appointment scheduling, billing, and clinical documentation modules.

## 👤 Author

**Md Enamul Karim** — Senior QA Automation Engineer
- API test architecture for healthcare platforms
- E2E validation across EHR, scheduling, and billing domains
- Schema-driven testing with production safety guarantees
