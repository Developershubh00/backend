from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    neet_rank = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  

    def __str__(self):
        return self.email or self.username
    
class CollegeChoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='choices')
    college_name = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    rank = models.PositiveIntegerField(null=True, blank=True)  # optional field

    def __str__(self):
        return f"{self.user.username} - {self.college_name} ({self.course_name})"


class CollegeCutoff(models.Model):
    round = models.CharField(max_length=20)
    ai_rank = models.IntegerField()
    state = models.CharField(max_length=100)
    institute = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    quota = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.institute} - {self.course} - {self.round}"

class MedicalCollege(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # Govt, Private, Deemed
    ownership = models.CharField(max_length=50, blank=True)
    courses_offered = models.CharField(max_length=255, blank=True)
    total_seats = models.IntegerField(null=True, blank=True)
    ranking = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class INICETAllotment(models.Model):
    round = models.CharField(max_length=20)
    ai_rank = models.PositiveIntegerField()
    state = models.CharField(max_length=100)
    institute = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    quota = models.CharField(max_length=100)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"Round {self.round} - Rank {self.ai_rank} - {self.institute}"

class UGSeatMatrix(models.Model):
    state = models.CharField(max_length=100)
    institute = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    total_seats = models.PositiveIntegerField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.institute} - {self.course}"

class PGFeeDetails(models.Model):
    institute = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2)
    stipend = models.DecimalField(max_digits=10, decimal_places=2)
    bond_years = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.institute} - {self.course}"



class PrivateCollege(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    ownership = models.CharField(max_length=50)
    course_offered = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class NIRFUniversityRanking(models.Model):
    rank = models.PositiveIntegerField()
    university_name = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.rank} - {self.university_name}"
    


class FAQCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')

    def __str__(self):
        return self.question
    
class RankPredictionCollege(models.Model):
    college_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    course = models.CharField(max_length=255)
    ownership = models.CharField(max_length=50)  # Govt / Private
    is_aiims = models.BooleanField(default=False)
    seat_type = models.CharField(max_length=100, blank=True)  # e.g., All India, State Quota
    closing_rank = models.PositiveIntegerField()  # This is the key to predict
    total_seats = models.PositiveIntegerField()
    intake_year = models.PositiveIntegerField(default=2025)  # Just in case

    def __str__(self):
            return f"{self.college_name} - {self.course}"
    
class CollegeDatabase(models.Model):
        COLLEGE_TYPE_CHOICES = [
            ("UG", "Undergraduate"),
            ("PG", "Postgraduate"),
        ]
    
        college_name = models.CharField(max_length=255)
        state = models.CharField(max_length=100)
        city = models.CharField(max_length=100)
        ownership = models.CharField(max_length=50)  # Government / Private
        is_aiims = models.BooleanField(default=False)
        college_type = models.CharField(max_length=2, choices=COLLEGE_TYPE_CHOICES)
        course = models.CharField(max_length=255)
        seat_type = models.CharField(max_length=100, blank=True)  # All India, State Quota, etc.
        closing_rank = models.PositiveIntegerField(null=True, blank=True)
        total_seats = models.PositiveIntegerField(default=0)
    
        def __str__(self):
            return f"{self.college_name} ({self.course})"
        
email_verified = models.BooleanField(default=False)
email_otp = models.CharField(max_length=6, blank=True, null=True)

from django.db import models

# Put the long list of categories here
CATEGORIES = [
    "All India Counseling - PG Medical",
    "Armed Forces Medical Services - AFMS (through MCC) - PG Medical",
    "Open States (Private Institute seats available for all candidates)",
    "Andhra Pradesh Government Quota - PG Medical",
    "Andhra Pradesh Management Quota - PG Medical",
    "Assam - PG Medical",
    "Bihar - PG Medical",
    "Chandigarh - PG Medical",
    "Chhattisgarh - PG Medical",
    "Delhi - PG Medical",
    "DNB Sponsored - PG Medical (Govt or PSU Inservice Candidates)",
    "Goa - PG Medical",
    "Gujarat - PG Medical",
    "Haryana - PG Medical",
    "Himachal Pradesh - PG Medical",
    "Jammu and Kashmir - PG Medical",
    "Jharkhand - PG Medical",
    "Karnataka - PG Medical",
    "Kerala - PG Medical",
    "Madhya Pradesh - PG Medical",
    "Maharashtra - PG Medical",
    "Manipur-JNIMS - PG Medical",
    "Manipur-RIMS - PG Medical",
    "NEIGRIHMS - PG Medical",
    "Odisha - PG Medical",
    "Pondicherry - PG Medical",
    "Punjab - PG Medical",
    "Rajasthan - PG Medical",
    "Sikkim - PG Medical",
    "Tamil Nadu Government Quota - PG Medical",
    "Tamil Nadu Management Quota - PG Medical",
    "Telangana Government Quota - PG Medical",
    "Telangana Management Quota - PG Medical",
    "Tripura - PG Medical",
    "Uttarakhand - PG Medical",
    "Uttar Pradesh - PG Medical",
    "West Bengal - PG Medical",
]

CATEGORY_CHOICES = tuple((c, c) for c in CATEGORIES)


class BaseTimestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Allotment(BaseTimestamp):
    # CSV columns: Round, AI Rank, State, Institute, Course, Quota, Category, Fee, Stipend Year 1, Bond Years, Bond Penalty, Beds
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    round = models.CharField(max_length=100, blank=True, null=True)
    ai_rank = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    institute = models.CharField(max_length=300, blank=True, null=True)
    course = models.CharField(max_length=300, blank=True, null=True)
    quota = models.CharField(max_length=200, blank=True, null=True)
    quota_category = models.CharField(max_length=200, blank=True, null=True)  # column named Category in CSV
    fee = models.CharField(max_length=200, blank=True, null=True)
    stipend_year1 = models.CharField(max_length=200, blank=True, null=True)
    bond_years = models.CharField(max_length=50, blank=True, null=True)
    bond_penalty = models.CharField(max_length=200, blank=True, null=True)
    beds = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.institute} | {self.course} | {self.category}"


class ClosingRank(BaseTimestamp):
    # CSV columns: Quota, Category, State, Institute, Course, Fee, Stipend Year 1, Bond Years, Bond Penalty, Beds, CR 2023 1..5, CR 2024 1..5
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    quota = models.CharField(max_length=200, blank=True, null=True)
    quota_category = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    institute = models.CharField(max_length=300, blank=True, null=True)
    course = models.CharField(max_length=300, blank=True, null=True)
    fee = models.CharField(max_length=200, blank=True, null=True)
    stipend_year1 = models.CharField(max_length=200, blank=True, null=True)
    bond_years = models.CharField(max_length=50, blank=True, null=True)
    bond_penalty = models.CharField(max_length=200, blank=True, null=True)
    beds = models.CharField(max_length=50, blank=True, null=True)

    # Closing Rank fields
    cr_2023_1 = models.CharField(max_length=100, blank=True, null=True)
    cr_2023_2 = models.CharField(max_length=100, blank=True, null=True)
    cr_2023_3 = models.CharField(max_length=100, blank=True, null=True)
    cr_2023_4 = models.CharField(max_length=100, blank=True, null=True)
    cr_2023_5 = models.CharField(max_length=100, blank=True, null=True)

    cr_2024_1 = models.CharField(max_length=100, blank=True, null=True)
    cr_2024_2 = models.CharField(max_length=100, blank=True, null=True)
    cr_2024_3 = models.CharField(max_length=100, blank=True, null=True)
    cr_2024_4 = models.CharField(max_length=100, blank=True, null=True)
    cr_2024_5 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.institute} | {self.course} | {self.category}"


class SeatMatrix(BaseTimestamp):
    # CSV columns: Institute Program Quota Open Open PwD General-EWS General-EWS PwD OBC OBC PwD SC SC PwD ST ST PwD TotalSeats
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    institute = models.CharField(max_length=300, blank=True, null=True)
    program = models.CharField(max_length=300, blank=True, null=True)
    quota = models.CharField(max_length=200, blank=True, null=True)

    open_seats = models.IntegerField(blank=True, null=True)
    open_pwd = models.IntegerField(blank=True, null=True)

    gen_ews = models.IntegerField(blank=True, null=True)
    gen_ews_pwd = models.IntegerField(blank=True, null=True)

    obc = models.IntegerField(blank=True, null=True)
    obc_pwd = models.IntegerField(blank=True, null=True)

    sc = models.IntegerField(blank=True, null=True)
    sc_pwd = models.IntegerField(blank=True, null=True)

    st = models.IntegerField(blank=True, null=True)
    st_pwd = models.IntegerField(blank=True, null=True)

    total_seats = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.institute} | {self.program} | {self.category}"


class FeeStipendBond(BaseTimestamp):
    # CSV columns: State Institute Course Quota Fee Stipend Year 1 Bond Years Bond Penalty Beds
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    state = models.CharField(max_length=200, blank=True, null=True)
    institute = models.CharField(max_length=300, blank=True, null=True)
    course = models.CharField(max_length=300, blank=True, null=True)
    quota = models.CharField(max_length=200, blank=True, null=True)
    fee = models.CharField(max_length=200, blank=True, null=True)
    stipend_year1 = models.CharField(max_length=200, blank=True, null=True)
    bond_years = models.CharField(max_length=50, blank=True, null=True)
    bond_penalty = models.CharField(max_length=200, blank=True, null=True)
    beds = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.institute} | {self.course} | {self.category}"

        