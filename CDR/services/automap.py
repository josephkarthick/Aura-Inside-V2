class AutoMapper:

    MAPPING = {

        # ======================================================
        # FROM NUMBER
        # ======================================================

        "from_number": [
            "Caller",
            "Caller ID Number",
            "Source",
            "MemberExtensionNumber",
            "Extension",
            
        ],

        # ======================================================
        # TO NUMBER
        # ======================================================

        "to_number": [
            "Callee",
            "CustomerPhoneNumber",
            "Destination",
            "Phone Number",
            "To",
        ],

        # ======================================================
        # DATE + TIME
        # ======================================================

        "call_datetime": [
            "Start Time",
            "CallDateTime",
            "DateTime",
            "Connect time",
            "Date",
            "Call Date",
            "Date & Time",
            "Started Time",
        ],

        # ======================================================
        # DURATION
        # ======================================================

        "duration": [
            "Connected (sec)",
            "Call Second",
            "CallDuration",
            "Duration",
            "Charged time, hour:min:sec",
            "Bill Second",
            "Talk Duration",
        ],

        # ======================================================
        # CALL STATUS
        # ======================================================

        "call_status": [
            "Hangup Cause",
            "Call Status",
            "CallDisposition",
            "Status",
            "Description",
            "End Reason",
        ],

        # ======================================================
        # CALL DIRECTION
        # ======================================================

        "direction": [
            "Call Direction",
            "CallDirection",
            "Direction",
            "Call Type",
            "Direction",

        ],
    }

    @classmethod
    def detect(cls, columns):

        mapping = {}

        normalized_columns = {
            str(col).strip().lower(): col
            for col in columns
        }

        for common_field, possible_headers in cls.MAPPING.items():

            mapping[common_field] = ""

            for header in possible_headers:

                key = header.strip().lower()

                if key in normalized_columns:

                    mapping[common_field] = (
                        normalized_columns[key]
                    )

                    break

        return mapping