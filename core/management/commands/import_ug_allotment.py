# import os
# import pandas as pd

# from django.conf import settings
# from django.core.management.base import BaseCommand

# from core.models import UGAllotmentData


# class Command(BaseCommand):
#     help = "Import UG Allotment CSV"

#     def handle(self, *args, **kwargs):

#         file_path = os.path.join(
#             settings.BASE_DIR,
#             "static",
#             "data",
#             "allotment2025UG.csv",
#         )

#         if not os.path.exists(file_path):
#             self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
#             return

#         df = pd.read_csv(file_path)

#         df.columns = df.columns.str.strip()

#         objects = []

#         for _, row in df.iterrows():

#             objects.append(
#                 UGAllotmentData(
#                     round=int(row["Round"]),
#                     ai_rank=int(row["AI Rank"]),
#                     state=str(row["State"]).strip(),
#                     institute=str(row["Institute"]).strip(),
#                     course=str(row["Course"]).strip(),
#                     quota=str(row["Quota"]).strip(),
#                     category=str(row["Category"]).strip(),
#                     fee=int(row["Fee"]) if pd.notna(row["Fee"]) else None,
#                     beds=int(row["Beds"]) if pd.notna(row["Beds"]) else None,
#                     bond_years=(
#                         int(row["Bond Years"]) if pd.notna(row["Bond Years"]) else None
#                     ),
#                     bond_penalty=(
#                         int(row["Bond Penalty"])
#                         if pd.notna(row["Bond Penalty"])
#                         else None
#                     ),
#                     stipend_year1=(
#                         int(row["Stipend Year 1"])
#                         if pd.notna(row["Stipend Year 1"])
#                         else None
#                     ),
#                 )
#             )

#         UGAllotmentData.objects.bulk_create(
#             objects,
#             batch_size=1000,
#         )

#         self.stdout.write(
#             self.style.SUCCESS(f"Successfully imported {len(objects)} rows")
#         )


import os
import pandas as pd

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import UGAllotmentData


class Command(BaseCommand):
    help = "Import UG Allotment CSV"

    def safe_int(self, value):
        """
        Safely convert values to integer.
        Handles:
        - NaN
        - Empty strings
        - Info not available
        - N/A
        - -
        - Decimal numbers
        """

        try:
            if pd.isna(value):
                return None

            value = str(value).strip()

            if value == "":
                return None

            if value.lower() in [
                "info not available",
                "not available",
                "n/a",
                "na",
                "-",
            ]:
                return None

            return int(float(value))

        except Exception:
            return None

    def safe_string(self, value):
        if pd.isna(value):
            return ""
        return str(value).strip()

    def handle(self, *args, **kwargs):

        file_path = os.path.join(
            settings.BASE_DIR,
            "static",
            "data",
            "allotment2025UG.csv",
        )

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        self.stdout.write(self.style.WARNING("Reading CSV..."))

        df = pd.read_csv(file_path, low_memory=False)

        df.columns = df.columns.str.strip()

        self.stdout.write(
            self.style.SUCCESS(f"CSV Loaded Successfully. Rows Found: {len(df)}")
        )

        objects = []

        for index, row in df.iterrows():

            try:

                objects.append(
                    UGAllotmentData(
                        round=self.safe_int(row.get("Round")),
                        ai_rank=self.safe_int(row.get("AI Rank")),
                        state=self.safe_string(row.get("State")),
                        institute=self.safe_string(row.get("Institute")),
                        course=self.safe_string(row.get("Course")),
                        quota=self.safe_string(row.get("Quota")),
                        category=self.safe_string(row.get("Category")),
                        fee=self.safe_int(row.get("Fee")),
                        beds=self.safe_int(row.get("Beds")),
                        bond_years=self.safe_int(row.get("Bond Years")),
                        bond_penalty=self.safe_int(row.get("Bond Penalty")),
                        stipend_year1=self.safe_int(row.get("Stipend Year 1")),
                    )
                )

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error on row {index + 1}: {e}"))

        self.stdout.write(
            self.style.WARNING("Deleting existing UG Allotment records...")
        )

        UGAllotmentData.objects.all().delete()

        self.stdout.write(self.style.WARNING(f"Inserting {len(objects)} records..."))

        UGAllotmentData.objects.bulk_create(
            objects,
            batch_size=1000,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {len(objects)} rows")
        )
