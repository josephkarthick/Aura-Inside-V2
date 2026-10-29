from CDR.models import VoipRecord


class EmployeeService:

    @staticmethod
    def find(number):

        record = (
            VoipRecord.objects
            .select_related("empid")
            .filter(cdr_id=str(number))
            .first()
        )

        # No VoIP record exists
        if not record:
            return {
                "employee": "Not Mapped",
                "employee_id": "NOT_FOUND",
                "department": "",
            }

        # VoIP record exists but no employee assigned
        if record.empid is None:
            return {
                "employee": "Free Extension",
                "employee_id": "UNASSIGNED",
                "department": "",
            }

        return {
            "employee": record.empid.get_full_name(),
            "employee_id": record.empid.employee_id,
            "department": record.empid.department.name if record.empid.department else "",
        }