class CommonParser:

    @staticmethod
    def normalize_number(value):

        if value is None:
            return ""

        # Handle pandas NaN
        try:
            if pd.isna(value):
                return ""
        except Exception:
            pass

        value = str(value).strip()

        # Excel may convert extension 35002 to 35002.0
        if value.endswith(".0"):
            value = value[:-2]

        # Remove common formatting
        value = (
            value
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        return value

    @staticmethod
    def parse(
        vendor,
        row,
        mapping,
        datetime_service,
        duration_service,
        employee_service,
    ):

        # ==========================================================
        # DATE / TIME
        # ==========================================================

        dt = datetime_service.convert_est_to_ist(
            row.get(mapping["call_datetime"])
        )

        # ==========================================================
        # DURATION
        # ==========================================================

        duration = duration_service.calculate(
            row.get(mapping["duration"])
        )

        # ==========================================================
        # RAW FROM / TO
        # ==========================================================

        number_1 = CommonParser.normalize_number(
            row.get(mapping["from_number"])
        )

        number_2 = CommonParser.normalize_number(
            row.get(mapping["to_number"])
        )

        # ==========================================================
        # EXPLICIT CALL DIRECTION
        #
        # Only use this if the vendor actually provides it.
        # ==========================================================

        direction = str(
            row.get("Call Direction", "")
        ).strip().upper()

        # ==========================================================
        # EMPLOYEE LOOKUP
        #
        # IMPORTANT:
        # Always check BOTH numbers.
        #
        # This fixes inbound calls such as:
        #
        # 18003234314 -> 35002
        #
        # where 35002 is the employee extension.
        # ==========================================================

        employee_1 = None
        employee_2 = None

        try:
            if number_1:
                employee_1 = employee_service.find(number_1)
        except Exception as e:
            print(
                f"Employee lookup error for {number_1}: {e}"
            )

        try:
            if number_2:
                employee_2 = employee_service.find(number_2)
        except Exception as e:
            print(
                f"Employee lookup error for {number_2}: {e}"
            )

        # ==========================================================
        # CHECK WHETHER EMPLOYEE WAS FOUND
        # ==========================================================

        found_1 = (
            employee_1
            and employee_1.get("employee_id")
            and employee_1.get("employee_id") != "NOT_FOUND"
        )

        found_2 = (
            employee_2
            and employee_2.get("employee_id")
            and employee_2.get("employee_id") != "NOT_FOUND"
        )

        # ==========================================================
        # CASE 1
        # EXPLICIT INBOUND
        # ==========================================================

        if direction == "INBOUND":

            # Number 1 = employee
            # Number 2 = external
            if found_1 and not found_2:

                from_number = number_2
                to_number = number_1
                employee = employee_1

            # Number 2 = employee
            # Number 1 = external
            elif found_2 and not found_1:

                from_number = number_1
                to_number = number_2
                employee = employee_2

            # If both are found, prefer TO as employee
            elif found_2:

                from_number = number_1
                to_number = number_2
                employee = employee_2

            # Last fallback
            elif found_1:

                from_number = number_2
                to_number = number_1
                employee = employee_1

            else:

                from_number = number_1
                to_number = number_2
                employee = {
                    "employee": "Not Mapped",
                    "employee_id": "NOT_FOUND",
                }

        # ==========================================================
        # CASE 2
        # EXPLICIT OUTBOUND
        # ==========================================================

        elif direction == "OUTBOUND":

            # Number 1 = employee
            # Number 2 = external
            if found_1 and not found_2:

                from_number = number_1
                to_number = number_2
                employee = employee_1

            # Number 2 = employee
            # Number 1 = external
            elif found_2 and not found_1:

                from_number = number_2
                to_number = number_1
                employee = employee_2

            # Prefer FROM as employee for outbound
            elif found_1:

                from_number = number_1
                to_number = number_2
                employee = employee_1

            elif found_2:

                from_number = number_2
                to_number = number_1
                employee = employee_2

            else:

                from_number = number_1
                to_number = number_2
                employee = {
                    "employee": "Not Mapped",
                    "employee_id": "NOT_FOUND",
                }

        # ==========================================================
        # CASE 3
        # NO DIRECTION PROVIDED
        #
        # Determine automatically using employee lookup.
        # ==========================================================

        else:

            # ------------------------------------------------------
            # Employee -> External
            # OUTBOUND
            # ------------------------------------------------------

            if found_1 and not found_2:

                direction = "OUTBOUND"

                from_number = number_1
                to_number = number_2

                employee = employee_1

            # ------------------------------------------------------
            # External -> Employee
            # INBOUND
            # ------------------------------------------------------

            elif found_2 and not found_1:

                direction = "INBOUND"

                from_number = number_1
                to_number = number_2

                employee = employee_2

            # ------------------------------------------------------
            # Both are employee/internal numbers
            # ------------------------------------------------------

            elif found_1 and found_2:

                direction = "INTERNAL"

                from_number = number_1
                to_number = number_2

                employee = employee_1

            # ------------------------------------------------------
            # Neither number mapped
            # ------------------------------------------------------

            else:

                direction = "UNKNOWN"

                from_number = number_1
                to_number = number_2

                employee = {
                    "employee": "Not Mapped",
                    "employee_id": "NOT_FOUND",
                }

        # ==========================================================
        # FINAL SAFETY
        # ==========================================================

        if not employee:

            employee = {
                "employee": "Not Mapped",
                "employee_id": "NOT_FOUND",
            }

        # ==========================================================
        # RETURN
        # ==========================================================

        return {

            "vendor": vendor,

            "employee": employee.get(
                "employee",
                "Not Mapped"
            ),

            "employee_id": employee.get(
                "employee_id",
                "NOT_FOUND"
            ),

            "from": from_number,

            "to": to_number,

            "direction": direction,

            "date": dt.get("date"),

            "est_time": dt.get("est_time"),

            "ist_time": dt.get("ist_time"),

            "duration_seconds": duration["seconds"],

            "duration": duration["duration"],

            "category": duration["category"],

            "less_1": duration["less_1"],

            "between_1_3": duration["between_1_3"],

            "greater_3": duration["greater_3"],

            "hold": duration["hold"],

            "hour": dt.get("hour"),

            "status": row.get(
                mapping["call_status"]
            ),

        }