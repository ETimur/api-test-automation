"""Patient API page object."""
from pages.base_page import BasePage
from utils.request_handler import RequestHandler
from utils.api_request_data_handler import ApiRequestDataHandler


class PatientApiPage(BasePage):
    """API page object for Patient CRUD endpoints."""

    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.request_data = ApiRequestDataHandler("patient.json")

    def create_patient(self, headers: dict, **overrides):
        """Create a new patient."""
        payload = self.request_data.get_modified_payload(
            "post_create_patient", **overrides
        )
        resp = self.request.post(
            request_path=self._url("/v1/ehr/patients"),
            headers=headers,
            json_data=payload,
        )
        return resp, payload

    def get_patient(self, headers: dict, patient_id: str):
        """Get patient by ID."""
        return self.request.get(
            request_path=self._url(f"/v1/ehr/patients/{patient_id}"),
            headers=headers,
        )

    def search_patients(self, headers: dict, query: str):
        """Search patients by name or MRN."""
        return self.request.get(
            request_path=self._url("/v1/ehr/patients/search"),
            headers=headers,
            params={"q": query},
        )

    def update_patient(self, headers: dict, patient_id: str, **fields):
        """Update patient fields."""
        return self.request.patch(
            request_path=self._url(f"/v1/ehr/patients/{patient_id}"),
            headers=headers,
            json_data=fields,
        )
