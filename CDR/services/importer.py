import pandas as pd


class FileImporter:

    @staticmethod
    def clean(value):

        if pd.isna(value):
            return ""

        value = str(value).strip()

        # Remove Excel-generated .0
        # only when the entire value is numeric.
        if value.endswith(".0"):

            number_part = value[:-2]

            if number_part.replace(".", "", 1).isdigit():
                value = number_part

        return value

    @staticmethod
    def read(file_path):

        # ==========================================================
        # CSV
        # ==========================================================

        if file_path.lower().endswith(".csv"):

            bad_lines = []

            def handle_bad_line(bad_line):

                bad_lines.append(bad_line)

                print(
                    "=========================================="
                )

                print(
                    "BAD CSV ROW DETECTED"
                )

                print(
                    f"Field count: {len(bad_line)}"
                )

                print(
                    bad_line
                )

                print(
                    "=========================================="
                )

                # Do not import malformed record
                return None

            df = pd.read_csv(

                file_path,

                dtype=str,

                keep_default_na=False,

                engine="python",

                on_bad_lines=handle_bad_line,

            )

            # Store information for debugging
            df.attrs["bad_lines"] = bad_lines

            if bad_lines:

                print(
                    f"WARNING: {len(bad_lines)} malformed "
                    f"CSV row(s) skipped."
                )

        # ==========================================================
        # EXCEL
        # ==========================================================

        else:

            df = pd.read_excel(

                file_path,

                dtype=str,

                keep_default_na=False,

            )

        # ==========================================================
        # CLEAN EVERY CELL
        # ==========================================================

        df = df.map(
            FileImporter.clean
        )

        return df