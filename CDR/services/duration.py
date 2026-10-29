class DurationService:

    @staticmethod
    def calculate(value):

        if value is None or value == "":
            seconds = 0

        elif isinstance(value, str) and ":" in value:

            try:

                h, m, s = value.split(":")

                seconds = (
                    int(h) * 3600 +
                    int(m) * 60 +
                    int(float(s))
                )

            except:

                seconds = 0

        else:

            try:

                seconds = int(float(value))

            except:

                seconds = 0

        # HH:MM:SS
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        duration = f"{hours:02}:{minutes:02}:{secs:02}"

        # Category
        if seconds < 60:

            category = "Less Than 1 Min"

            less_1 = True
            between_1_3 = False
            greater_3 = False
            hold = False

        elif seconds < 180:

            category = "1-3 Mins"

            less_1 = False
            between_1_3 = True
            greater_3 = False
            hold = False

        elif seconds < 3600:

            category = "3 Mins - 1 Hour"

            less_1 = False
            between_1_3 = False
            greater_3 = True
            hold = False

        else:

            category = "Greater Than 1 Hour"

            less_1 = False
            between_1_3 = False
            greater_3 = False
            hold = True

        return {

            "seconds": seconds,

            "duration": duration,

            "category": category,

            "less_1": less_1,

            "between_1_3": between_1_3,

            "greater_3": greater_3,

            "hold": hold,

        }