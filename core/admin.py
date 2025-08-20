from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from io import TextIOWrapper
import csv
from django.contrib.auth.models import AbstractUser

from .models import (
    CustomUser,
    CollegeCutoff,
    MedicalCollege,
    INICETAllotment,
    UGSeatMatrix,
    PGFeeDetails,
    ClosingRank,
    PrivateCollege,
    NIRFUniversityRanking,
    FAQ,
    FAQCategory,
    RankPredictionCollege,
    CollegeDatabase
)

from .resources import (
    CollegeCutoffResource,
    MedicalCollegeResource,
    INICETAllotmentResource,
    UGSeatMatrixResource,
    PGFeeDetailsResource,
    ClosingRankResource,
    PrivateCollegeResource,
    NIRFUniversityRankingResource,
    RankPredictionCollegeResource,
    CollegeDatabaseResource
)

# ------------------------- Custom User -------------------------

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'username', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar', 'phone', 'state', 'category', 'neet_rank')}),
    )

# ------------------------- Admin Panels -------------------------

@admin.register(CollegeCutoff)
class CollegeCutoffAdmin(ImportExportModelAdmin):
    list_display = ('round', 'ai_rank', 'state', 'institute', 'course', 'quota', 'category')
    search_fields = ('state', 'institute', 'course', 'quota', 'category')
    list_filter = ('round', 'state', 'quota', 'category')
    resource_class = CollegeCutoffResource


@admin.register(MedicalCollege)
class MedicalCollegeAdmin(ImportExportModelAdmin):
    resource_class = MedicalCollegeResource


@admin.register(INICETAllotment)
class INICETAllotmentAdmin(ImportExportModelAdmin):
    list_display = ('round', 'ai_rank', 'state', 'institute', 'course', 'quota', 'category')
    search_fields = ('state', 'institute', 'course', 'quota', 'category')
    list_filter = ('round', 'state', 'quota', 'category')
    resource_class = INICETAllotmentResource


# @admin.register(UGSeatMatrix)
# class UGSeatMatrixAdmin(ImportExportModelAdmin):
#     list_display = ('state', 'institute', 'course', 'total_seats', 'category')
#     search_fields = ('state', 'institute', 'course', 'category')
#     list_filter = ('state', 'category')
#     resource_class = UGSeatMatrixResource


@admin.register(PGFeeDetails)
class PGFeeDetailsAdmin(ImportExportModelAdmin):
    list_display = ('institute', 'course', 'annual_fee', 'stipend')
    search_fields = ('institute', 'course')
    list_filter = ('institute', 'course')
    resource_class = PGFeeDetailsResource


# @admin.register(ClosingRank)
# class ClosingRankAdmin(ImportExportModelAdmin):
#     list_display = ('round', 'institute', 'course', 'category', 'closing_rank')
#     search_fields = ('round', 'institute', 'course', 'category')
#     list_filter = ('round', 'category')
#     resource_class = ClosingRankResource


@admin.register(PrivateCollege)
class PrivateCollegeAdmin(ImportExportModelAdmin):
    list_display = ('name', 'state', 'ownership', 'course_offered')
    search_fields = ('name', 'state', 'ownership', 'course_offered')
    list_filter = ('state', 'ownership')
    resource_class = PrivateCollegeResource


@admin.register(NIRFUniversityRanking)
class NIRFUniversityRankingAdmin(ImportExportModelAdmin):
    list_display = ('university_name', 'city', 'rank', 'score')
    search_fields = ('university_name', 'city')
    list_filter = ('city',)
    resource_class = NIRFUniversityRankingResource


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    search_fields = ('question', 'answer')
    list_filter = ('category',)


@admin.register(RankPredictionCollege)
class RankPredictionCollegeAdmin(ImportExportModelAdmin):
    list_display = ('college_name', 'course', 'closing_rank', 'ownership', 'is_aiims')
    search_fields = ('college_name', 'city', 'state', 'course')
    list_filter = ('ownership', 'is_aiims', 'intake_year', 'seat_type')
    resource_class = RankPredictionCollegeResource


@admin.register(CollegeDatabase)
class CollegeDatabaseAdmin(ImportExportModelAdmin):
    list_display = ('college_name', 'course', 'state', 'ownership', 'college_type', 'closing_rank')
    list_filter = ('state', 'ownership', 'college_type', 'is_aiims')
    search_fields = ('college_name', 'state', 'city', 'course')
    change_list_template = "admin/core/collegedatabase/change_list.html"
    # resource_class = CollegeDatabaseResource

    def changelist_view(self, request, extra_context=None):
        if 'csv_file' in request.FILES:
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            count = 0
            for row in reader:
                CollegeDatabase.objects.create(
                    college_name=row['College Name'],
                    state=row['State'],
                    city=row['City'],
                    ownership=row['Ownership'],
                    is_aiims=row['Is AIIMS'].strip().lower() in ['yes', 'true', '1'],
                    college_type=row['Type'].upper(),
                    course=row['Course'],
                    seat_type=row.get('Seat Type', ''),
                    closing_rank=int(row['Closing Rank']) if row['Closing Rank'].isdigit() else None,
                    total_seats=int(row['Seats']) if row['Seats'].isdigit() else 0
                )
                count += 1
            self.message_user(request, f"✅ Successfully imported {count} colleges from CSV", level=messages.SUCCESS)
        return super().changelist_view(request, extra_context)

# ------------------------- Signals -------------------------

@receiver(post_save, sender=CustomUser)
def generate_avatar_initials(sender, instance, created, **kwargs):
    if created and not instance.avatar:
        initials = ''.join([part[0].upper() for part in instance.first_name.strip().split()[:2]])
        instance.avatar = initials
        instance.save()

# ------------------------- Other Models Admin -------------------------
from core.models import Allotment, ClosingRank, SeatMatrix, FeeStipendBond

@admin.register(Allotment)
class AllotmentAdmin(ImportExportModelAdmin):
    list_display = ("institute", "course", "state", "category", "quota", "ai_rank")
    search_fields = ("institute", "course", "state", "category")
    list_filter = ("category", "state", "quota")
    
    # def changelist_view(self, request, extra_context=None):
    #     if 'csv_file' in request.FILES:
    #         csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
    #         reader = csv.DictReader(csv_file)
    #         count = 0
    #         for row in reader:
    #             Allotment.objects.create(
    #                 college_name=row['College Name'],
    #                 state=row['State'],
    #                 city=row['City'],
    #                 ownership=row['Ownership'],
    #                 is_aiims=row['Is AIIMS'].strip().lower() in ['yes', 'true', '1'],
    #                 college_type=row['Type'].upper(),
    #                 course=row['Course'],
    #                 seat_type=row.get('Seat Type', ''),
    #                 closing_rank=int(row['Closing Rank']) if row['Closing Rank'].isdigit() else None,
    #                 total_seats=int(row['Seats']) if row['Seats'].isdigit() else 0
    #             )
    #             count += 1
    #         self.message_user(request, f"✅ Successfully imported {count} colleges from CSV", level=messages.SUCCESS)
    #     return super().changelist_view(request, extra_context)



@admin.register(ClosingRank)
class ClosingRankAdmin(ImportExportModelAdmin):
    list_display = ("institute", "course", "state", "category")
    search_fields = ("institute", "course", "state", "category")
    list_filter = ("category", "state", "quota")


@admin.register(SeatMatrix)
class SeatMatrixAdmin(ImportExportModelAdmin):
    list_display = ("institute", "program", "category", "total_seats")
    search_fields = ("institute", "program", "category")
    list_filter = ("category",)


@admin.register(FeeStipendBond)
class FeeStipendBondAdmin(ImportExportModelAdmin):
    list_display = ("institute", "course", "state", "category", "fee")
    search_fields = ("institute", "course", "state", "category")
    list_filter = ("category", "state")
