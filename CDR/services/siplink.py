import requests

from CDR.models import Vendor

import pandas as pd


def parse_siplink(df):

    records = []

    for _, row in df.iterrows():

        record = {

            "call_id": row.get("Call ID"),

            "call_direction": row.get("Call Direction"),

            "caller": str(row.get("Caller")).strip(),

            "caller_name": row.get("Caller Name"),

            "callee": str(row.get("Callee")).strip(),

            "callee_name": row.get("Callee Name"),

            "start_time": row.get("Start Time"),

            "end_time": row.get("End Time"),

            "duration_seconds": row.get("Call Second"),

            "call_status": row.get("Call Status"),

            "hangup_reason": row.get("Hangup Reason"),

            "unique_token": row.get("Unique Token"),

        }

        records.append(record)

    return records
    
class SiplinkAPI:

    def __init__(self):
        self.vendor = Vendor.objects.get(
            name__iexact="SIPLINK",
            is_active=True
        )

        self.token = self.vendor.api_token.strip()

        self.base_url = (
            "https://hostedpbx.siplink.in/"
            "hodupbx_api/v1.4/api/info"
        )

    def get_call_logs(self, from_date, to_date):

        url = (
            f"{self.base_url}/"
            f"{from_date}/"
            f"{to_date}/"
            f"TENANT/callLog"
        )

        payload = {
            "token_id": self.token,
            "timezone_id": "140",    
            "required_media_state": "YES",
            "required_transaction_state": "YES",
        }

        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60,
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        return response.json()
        
   