from zoneinfo import ZoneInfo
import pandas as pd
import re


class DateTimeService:

    EASTERN_TZ = ZoneInfo("America/New_York")
    IST_TZ = ZoneInfo("Asia/Kolkata")

    @staticmethod
    def convert_est_to_ist(value):

        if value is None or pd.isna(value):
            return {}

        try:

            value = str(value).strip()

            # SKYFALL example:
            # 2026-09-24 18:45:41 -0400 EDT
            #
            # Remove:
            # -0400 EDT
            #
            # Keep:
            # 2026-09-24 18:45:41

            value = re.sub(
                r"\s+[+-]\d{4}(?:\s+[A-Za-z]{2,5})?\s*$",
                "",
                value
            ).strip()

            # Parse the vendor date/time
            dt = pd.to_datetime(
                value,
                errors="coerce"
            )

            if pd.isna(dt):
                return {}

            dt = dt.to_pydatetime()

            # SKYFALL time is America/New_York
            eastern_time = dt.replace(
                tzinfo=DateTimeService.EASTERN_TZ
            )

            # Convert Eastern Time → IST
            ist_time = eastern_time.astimezone(
                DateTimeService.IST_TZ
            )

            return {

                # Original SKYFALL date
                "date": eastern_time.strftime(
                    "%d-%m-%Y"
                ),

                # Original SKYFALL Eastern time
                "est_time": eastern_time.strftime(
                    "%I:%M:%S %p"
                ),

                # Converted IST time
                "ist_time": ist_time.strftime(
                    "%I:%M:%S %p"
                ),

                # Hour based on IST
                "hour": ist_time.strftime(
                    "%I %p"
                ),

                # IST datetime internally
                "datetime": ist_time,
            }

        except Exception as e:

            print(
                f"DateTime conversion error: {value} -> {e}"
            )

            return {}
            
            