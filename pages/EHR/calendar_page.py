"""Calendar/Appointment API page object."""
from pages.base_page import BasePage
from utils.request_handler import RequestHandler
from utils.api_request_data_handler import ApiRequestDataHandler


class CalendarApiPage(BasePage):
    """API page object for Calendar/Appointment endpoints."""

    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.request_data = ApiRequestDataHandler("calendar.json")

    def create_appointment(self, headers: dict, **overrides):
        """Create an appointment with slot-retry logic.
        
        Returns (response, payload) tuple.
        """
        payload = self.request_data.get_modified_payload(
            "post_create_appointment", **overrides
        )

        for attempt in range(32):
            resp = self.request.post(
                request_path=self._url("/v1/ehr/appointments/create"),
                headers=headers,
                json_data=payload,
            )
            if resp.status_code == 200:
                return resp, payload
            if resp.status_code == 400 and "already exists" in resp.text:
                # Shift to next available time slot
                payload = self._next_slot(payload)
                continue
            return resp, payload

        return resp, payload

    def get_appointments(self, headers: dict, provider_id: str, facility_id: str,
                         start_datetime: str, end_datetime: str):
        """GET filtered appointments."""
        params = {
            "provider_id": provider_id,
            "facility_id": facility_id,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        }
        return self.request.get(
            request_path=self._url("/v1/ehr/appointments"),
            headers=headers,
            params=params,
        )

    def cancel_appointment(self, headers: dict, appointment_id: str):
        """Cancel an appointment (never delete)."""
        return self.request.patch(
            request_path=self._url(f"/v1/ehr/appointments/{appointment_id}/cancel"),
            headers=headers,
            json_data={"reason": "QA test cleanup"},
        )

    def _next_slot(self, payload: dict) -> dict:
        """Shift appointment time to next 15-min slot."""
        from datetime import datetime, timedelta
        start = datetime.fromisoformat(payload["start_datetime"].replace("Z", "+00:00"))
        start += timedelta(minutes=15)
        payload["start_datetime"] = start.strftime("%Y-%m-%dT%H:%M:%SZ")
        end = start + timedelta(minutes=30)
        payload["end_datetime"] = end.strftime("%Y-%m-%dT%H:%M:%SZ")
        return payload
