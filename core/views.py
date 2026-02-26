from django.shortcuts import render
from .models import MedicalCollege
from .serializers import MedicalCollegeSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer, UserProfileSerializer
# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import viewsets, filters
from .models import FAQ, FAQCategory
from .serializers import FAQSerializer, FAQCategorySerializer
from rest_framework import viewsets
from .models import CollegeCutoff
from .serializers import CollegeCutoffSerializer
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer, UserProfileSerializer
from rest_framework import viewsets, filters
from .models import INICETAllotment
from .serializers import INICETAllotmentSerializer
from .models import CollegeChoice
from .serializers import CollegeChoiceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import RankPredictionCollege
from .serializers import RankPredictionCollegeSerializer
from .models import UGSeatMatrix, PGFeeDetails, PrivateCollege, NIRFUniversityRanking
from .models import Allotment, ClosingRank, SeatMatrix, FeeStipendBond, AllotmentData, SeatMatrixData, FeeStipendBondData, ClosingRanksData
from .serializers import (
    UGSeatMatrixSerializer, PGFeeDetailsSerializer, OldClosingRankSerializer,
    PrivateCollegeSerializer, NIRFUniversityRankingSerializer, LoginSerializer,
    AllotmentSerializer, ClosingRankSerializer, SeatMatrixSerializer, FeeStipendBondSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import UserSerializer
from rest_framework import viewsets, filters
from .models import CollegeDatabase
from .serializers import CollegeDatabaseSerializer  
from django.core.mail import send_mail
import random
from rest_framework.decorators import api_view  
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.utils import timezone
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
# Add these imports at the top of your views.py
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()

def get_client_ip(request) -> str:
    """Extracts real client IP, handles proxies and load balancers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            "status": "healthy",
            "message": "BD Counselling Backend API is running",
            "version": "1.0.0"
        })

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    "application/json": {
                        "access": "your_jwt_token",
                        "refresh": "your_refresh_token",
                        "user_id": 1,
                        "username": "shubh",
                        "email": "shubh@example.com"
                    }
                }
            ),
            401: "Invalid credentials",
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



# Removed duplicate SignupView and ProfileView definitions to avoid conflicts.

class CollegeCutoffViewSet(viewsets.ModelViewSet):
    queryset = CollegeCutoff.objects.all()
    serializer_class = CollegeCutoffSerializer

class MedicalCollegeList(generics.ListAPIView):
    queryset = MedicalCollege.objects.all()
    serializer_class = MedicalCollegeSerializer

# class SignupView(generics.CreateAPIView):
#     serializer_class = SignupSerializer
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         print(request.data)
#         request.data['username'] = request.data['name']
#         print(request.data)
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(UserProfileSerializer(user).data, status=201)
#         return Response(serializer.errors, status=400)

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        request.data['username'] = request.data['name']
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            ip = get_client_ip(request)          # ← ADD THIS
            if ip:                               # ← ADD THIS
                user.__class__.objects.filter(pk=user.pk).update(signup_ip=ip)  # ← ADD THIS
            return Response(UserProfileSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)
    

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        # Update all fields that are provided
        if 'email' in request.data:
            user.email = request.data['email']
        if 'name' in request.data:
            user.first_name = request.data['name']
        if 'phone' in request.data:
            user.phone = request.data['phone']
        if 'neet_rank' in request.data:
            user.neet_rank = request.data['neet_rank']
        if 'category' in request.data:
            user.category = request.data['category']
        if 'state' in request.data:
            user.state = request.data['state']
        
        user.save()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

class INICETAllotmentViewSet(viewsets.ModelViewSet):
    queryset = INICETAllotment.objects.all().order_by('ai_rank')
    serializer_class = INICETAllotmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['state', 'institute', 'course', 'quota', 'category']
    ordering_fields = ['ai_rank', 'round']
    ordering = ['ai_rank']  
    
class UGSeatMatrixViewSet(viewsets.ModelViewSet):
    queryset = UGSeatMatrix.objects.all()
    serializer_class = UGSeatMatrixSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['state', 'institute', 'course', 'category']
    ordering_fields = ['total_seats']

class PGFeeDetailsViewSet(viewsets.ModelViewSet):
    queryset = PGFeeDetails.objects.all()
    serializer_class = PGFeeDetailsSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['institute', 'course']
    ordering_fields = ['annual_fee', 'stipend']

class ClosingRankViewSet(viewsets.ModelViewSet):
    queryset = ClosingRank.objects.all()
    serializer_class = ClosingRankSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['round', 'institute', 'course', 'category']
    ordering_fields = ['closing_rank']

class PrivateCollegeViewSet(viewsets.ModelViewSet):
    queryset = PrivateCollege.objects.all()
    serializer_class = PrivateCollegeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'state', 'ownership', 'course_offered']
    ordering_fields = ['name']

class NIRFUniversityRankingViewSet(viewsets.ModelViewSet):
    queryset = NIRFUniversityRanking.objects.all()
    serializer_class = NIRFUniversityRankingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['university_name', 'city']
    ordering_fields = ['rank', 'score']


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['question', 'answer']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        return queryset

class FAQCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer


class CollegeChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = CollegeChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CollegeChoice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RankPredictorView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_rank = request.query_params.get('rank')
        if not user_rank or not user_rank.isdigit():
            return Response({"error": "Please provide a valid rank (e.g. ?rank=2534)"}, status=400)

        user_rank = int(user_rank)
        colleges = RankPredictionCollege.objects.filter(closing_rank__gte=user_rank).order_by('closing_rank')[:100]
        serializer = RankPredictionCollegeSerializer(colleges, many=True)
        return Response(serializer.data)
    
class CollegeDatabaseList(APIView):
    def get(self, request):
        colleges = CollegeDatabase.objects.all().order_by('closing_rank')
        serializer = CollegeDatabaseSerializer(colleges, many=True)
        return Response(serializer.data)
    
def generate_otp():
    return f"{random.randint(100000, 999999)}"

def send_verification_email(user):
    otp = generate_otp()
    user.email_otp = otp
    user.save()
    send_mail(
        subject="Verify your email for BD Counselling",
        message=f"Hi {user.name},\nYour verification OTP is: {otp}",
        from_email="noreply@bdcounselling.com",
        recipient_list=[user.email],
    )

    return Response({"message": "Verification OTP sent to your email."})
class EmailVerificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.email_verified:
            send_verification_email(user)
            return Response({"message": "Verification email sent."}, status=status.HTTP_200_OK)
        return Response({"message": "Email already verified."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        otp = request.data.get('otp')
        if user.email_otp == otp:
            user.email_verified = True
            user.email_otp = ''
            user.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_email_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")

    try:
        user = User.objects.get(email=email)
        if user.email_otp == otp:
            user.email_verified = True
            user.email_otp = None
            user.save()
            return Response({"detail": "Email verified successfully"})
        return Response({"error": "Invalid OTP"}, status=400)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
 # core/views.py
import csv
import io
from django.db import transaction
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Allotment, ClosingRank, SeatMatrix, FeeStipendBond, CATEGORIES
from .serializers import (
    AllotmentSerializer, ClosingRankSerializer,
    SeatMatrixSerializer, FeeStipendBondSerializer
)

def _normalize_key(k):
    if k is None:
        return ""
    return k.strip().lower().replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", "_")

def _get(row, *keys):
    for k in keys:
        val = row.get(k)
        if val is not None and val != "":
            return val.strip()
    return None

def _to_int(val):
    if val is None or val == "":
        return None
    try:
        return int(float(str(val).replace(",", "").strip()))
    except Exception:
        return None

# List APIs (public)
class AllotmentListView(generics.ListAPIView):
    serializer_class = AllotmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cat = self.kwargs.get("category")
        qs = Allotment.objects.all()
        if cat:
            qs = qs.filter(category=cat)
        state = self.request.query_params.get("state")
        if state:
            qs = qs.filter(state__icontains=state)
        institute = self.request.query_params.get("institute")
        if institute:
            qs = qs.filter(institute__icontains=institute)
        return qs.order_by("institute", "course")

class ClosingRankListView(generics.ListAPIView):
    serializer_class = ClosingRankSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cat = self.kwargs.get("category")
        qs = ClosingRank.objects.all()
        if cat:
            qs = qs.filter(category=cat)
        state = self.request.query_params.get("state")
        if state:
            qs = qs.filter(state__icontains=state)
        return qs.order_by("institute", "course")

class SeatMatrixListView(generics.ListAPIView):
    serializer_class = SeatMatrixSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cat = self.kwargs.get("category")
        qs = SeatMatrix.objects.all()
        if cat:
            qs = qs.filter(category=cat)
        institute = self.request.query_params.get("institute")
        if institute:
            qs = qs.filter(institute__icontains=institute)
        return qs.order_by("institute", "program")

class FeeListView(generics.ListAPIView):
    serializer_class = FeeStipendBondSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cat = self.kwargs.get("category")
        qs = FeeStipendBond.objects.all()
        if cat:
            qs = qs.filter(category=cat)
        institute = self.request.query_params.get("institute")
        if institute:
            qs = qs.filter(institute__icontains=institute)
        return qs.order_by("institute", "course")

# CSV upload (admin only)
class CSVUploadView(APIView):
    """
    POST /api/upload/{type}/
    form-data: file (csv), category (exact string from CATEGORIES), replace (optional 'true'/'false')
    type: allotment | closingrank | seatmatrix | fee
    """
    permission_classes = [IsAdminUser]

    def post(self, request, type):
        csv_file = request.FILES.get("file")
        category = request.data.get("category")
        replace_flag = str(request.data.get("replace", "true")).lower() != "false"

        if not csv_file:
            return Response({"detail": "CSV file is required as 'file'."}, status=status.HTTP_400_BAD_REQUEST)
        if category not in CATEGORIES:
            return Response({"detail": "Invalid or missing category. Must be one of the predefined categories."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded = csv_file.read().decode("utf-8-sig")
        except Exception:
            return Response({"detail": "Could not decode file — please upload UTF-8 CSV."}, status=400)

        reader = csv.DictReader(io.StringIO(decoded))
        rows = list(reader)
        if not rows:
            return Response({"detail": "CSV appears empty or headers missing."}, status=400)

        try:
            with transaction.atomic():
                if type == "allotment":
                    if replace_flag:
                        Allotment.objects.filter(category=category).delete()
                    objs = []
                    for r in rows:
                        data = {
                            "category": category,
                            "round": _get(r, "Round", "round"),
                            "ai_rank": _get(r, "AI Rank", "Ai Rank", "ai_rank", "ai_rank"),
                            "state": _get(r, "State", "state"),
                            "institute": _get(r, "Institute", "institute"),
                            "course": _get(r, "Course", "course"),
                            "quota": _get(r, "Quota", "quota"),
                            "quota_category": _get(r, "Category", "category"),
                            "fee": _get(r, "Fee", "fee"),
                            "stipend_year1": _get(r, "Stipend Year 1", "Stipend_Year_1", "stipend_year1"),
                            "bond_years": _get(r, "Bond Years", "bond_years"),
                            "bond_penalty": _get(r, "Bond Penalty", "bond_penalty"),
                            "beds": _get(r, "Beds", "beds"),
                        }
                        objs.append(Allotment(**data))
                    Allotment.objects.bulk_create(objs, batch_size=500)

                elif type == "closingrank":
                    if replace_flag:
                        ClosingRank.objects.filter(category=category).delete()
                    objs = []
                    for r in rows:
                        data = {
                            "category": category,
                            "quota": _get(r, "Quota"),
                            "quota_category": _get(r, "Category"),
                            "state": _get(r, "State"),
                            "institute": _get(r, "Institute"),
                            "course": _get(r, "Course"),
                            "fee": _get(r, "Fee"),
                            "stipend_year1": _get(r, "Stipend Year 1"),
                            "bond_years": _get(r, "Bond Years"),
                            "bond_penalty": _get(r, "Bond Penalty"),
                            "beds": _get(r, "Beds"),
                            "cr_2023_1": _get(r, "CR 2023 1", "CR_2023_1"),
                            "cr_2023_2": _get(r, "CR 2023 2"),
                            "cr_2023_3": _get(r, "CR 2023 3"),
                            "cr_2023_4": _get(r, "CR 2023 4"),
                            "cr_2023_5": _get(r, "CR 2023 5"),
                            "cr_2024_1": _get(r, "CR 2024 1"),
                            "cr_2024_2": _get(r, "CR 2024 2"),
                            "cr_2024_3": _get(r, "CR 2024 3"),
                            "cr_2024_4": _get(r, "CR 2024 4"),
                            "cr_2024_5": _get(r, "CR 2024 5"),
                        }
                        objs.append(ClosingRank(**data))
                    ClosingRank.objects.bulk_create(objs, batch_size=500)

                elif type == "seatmatrix":
                    if replace_flag:
                        SeatMatrix.objects.filter(category=category).delete()
                    objs = []
                    for r in rows:
                        data = {
                            "category": category,
                            "institute": _get(r, "Institute", "institute"),
                            "program": _get(r, "Program", "program"),
                            "quota": _get(r, "Quota"),
                            "open_seats": _to_int(_get(r, "Open", "Open Seats", "open")),
                            "open_pwd": _to_int(_get(r, "Open PwD", "Open_PwD", "open_pwd")),
                            "gen_ews": _to_int(_get(r, "General-EWS", "General_EWS", "General EWS", "gen_ews")),
                            "gen_ews_pwd": _to_int(_get(r, "General-EWS PwD", "General_EWS_PwD", "gen_ews_pwd")),
                            "obc": _to_int(_get(r, "OBC")),
                            "obc_pwd": _to_int(_get(r, "OBC PwD", "obc_pwd")),
                            "sc": _to_int(_get(r, "SC")),
                            "sc_pwd": _to_int(_get(r, "SC PwD", "sc_pwd")),
                            "st": _to_int(_get(r, "ST")),
                            "st_pwd": _to_int(_get(r, "ST PwD", "st_pwd")),
                            "total_seats": _to_int(_get(r, "TotalSeats", "Total Seats", "total_seats")),
                        }
                        objs.append(SeatMatrix(**data))
                    SeatMatrix.objects.bulk_create(objs, batch_size=500)

                elif type == "fee":
                    if replace_flag:
                        FeeStipendBond.objects.filter(category=category).delete()
                    objs = []
                    for r in rows:
                        data = {
                            "category": category,
                            "state": _get(r, "State"),
                            "institute": _get(r, "Institute"),
                            "course": _get(r, "Course"),
                            "quota": _get(r, "Quota"),
                            "fee": _get(r, "Fee"),
                            "stipend_year1": _get(r, "Stipend Year 1"),
                            "bond_years": _get(r, "Bond Years"),
                            "bond_penalty": _get(r, "Bond Penalty"),
                            "beds": _get(r, "Beds"),
                        }
                        objs.append(FeeStipendBond(**data))
                    FeeStipendBond.objects.bulk_create(objs, batch_size=500)

                else:
                    return Response({"detail": "Invalid type param"}, status=400)

        except Exception as e:
            return Response({"detail": f"Import failed: {str(e)}"}, status=500)

        return Response({"detail": f"{len(rows)} rows imported into {type} / {category}"}, status=201)


# Category-based API Views
class CategoryBasedAllotmentView(APIView):
    """
    GET /api/category/allotments/{category}/
    Returns allotment data for a specific category
    """
    permission_classes = [AllowAny]
    
    def get(self, request, category):
        try:
            allotments = Allotment.objects.filter(category=category)
            serializer = AllotmentSerializer(allotments, many=True)
            return Response({
                "category": category,
                "count": allotments.count(),
                "data": serializer.data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class CategoryBasedClosingRankView(APIView):
    """
    GET /api/category/closing-ranks/{category}/
    Returns closing rank data for a specific category
    """
    permission_classes = [AllowAny]
    
    def get(self, request, category):
        try:
            closing_ranks = ClosingRank.objects.filter(category=category)
            serializer = ClosingRankSerializer(closing_ranks, many=True)
            return Response({
                "category": category,
                "count": closing_ranks.count(),
                "data": serializer.data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class CategoryBasedSeatMatrixView(APIView):
    """
    GET /api/category/seat-matrix/{category}/
    Returns seat matrix data for a specific category
    """
    permission_classes = [AllowAny]
    
    def get(self, request, category):
        try:
            seat_matrix = SeatMatrix.objects.filter(category=category)
            serializer = SeatMatrixSerializer(seat_matrix, many=True)
            return Response({
                "category": category,
                "count": seat_matrix.count(),
                "data": serializer.data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class CategoryBasedFeeStipendBondView(APIView):
    """
    GET /api/category/fee-stipend-bond/{category}/
    Returns fee, stipend, and bond data for a specific category
    """
    permission_classes = [AllowAny]
    
    def get(self, request, category):
        try:
            fee_data = FeeStipendBond.objects.filter(category=category)
            serializer = FeeStipendBondSerializer(fee_data, many=True)
            return Response({
                "category": category,
                "count": fee_data.count(),
                "data": serializer.data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class CategoryListView(APIView):
    """
    GET /api/categories/
    Returns list of all available categories
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        from .models import CATEGORIES
        return Response({
            "categories": CATEGORIES,
            "count": len(CATEGORIES)
        })


class CategorySummaryView(APIView):
    """
    GET /api/category/summary/{category}/
    Returns summary of all data types available for a category
    """
    permission_classes = [AllowAny]
    
    def get(self, request, category):
        try:
            allotment_count = Allotment.objects.filter(category=category).count()
            closing_rank_count = ClosingRank.objects.filter(category=category).count()
            seat_matrix_count = SeatMatrix.objects.filter(category=category).count()
            fee_count = FeeStipendBond.objects.filter(category=category).count()
            
            return Response({
                "category": category,
                "summary": {
                    "allotments": allotment_count,
                    "closing_ranks": closing_rank_count,
                    "seat_matrix": seat_matrix_count,
                    "fee_stipend_bond": fee_count
                },
                "total_records": allotment_count + closing_rank_count + seat_matrix_count + fee_count
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# app/views.py
import os
import pandas as pd
from django.conf import settings
from django.http import JsonResponse


# 1. Allotment Data (Round_1 → Round_5)
def upload_allotment_data(request):
    csv_path = os.path.join(settings.BASE_DIR, "static", "data", "allotments")
    csv_files = [f for f in os.listdir(csv_path) if f.endswith(".csv")]

    objs = []
    for file in csv_files:
        df = pd.read_csv(os.path.join(csv_path, file))
        for _, row in df.iterrows():
            print(row)
            objs.append(AllotmentData(
                round=row["Round"],
                ai_rank=row["AI Rank"],
                state=row["State"],
                institute=row["Institute"],
                course=row["Course"],
                quota=row["Quota"],
                category=row["Category"],
                fee=row["Fee"],
                stipend_year1=row["Stipend Year 1"],
                bond_years=row["Bond Years"] if not pd.isna(row["Bond Years"]) else None,
                bond_penalty=row["Bond Penalty"],
                beds=row["Beds"]
            ))
    # print(objs)
    AllotmentData.objects.bulk_create(objs)
    return JsonResponse({"status": "success", "inserted": len(objs)})


# 2. Seat Matrix Data
def upload_seatmatrix_data(request):
    file_path = os.path.join(settings.BASE_DIR, "static", "data", "Seat_matrix.csv")
    df = pd.read_csv(file_path)

    objs = []
    for _, row in df.iterrows():
        # print(row["category"])
        objs.append(SeatMatrixData(
            round=row["Round"],
            quota=row["Quota"],
            category=row["Category"],
            state=row["State"],
            institute=row["Institute"],
            course=row["Course"],
            seats=row["Seats"],
            fee=row["Fee"],
            stipend_year1=row["Stipend Year 1"],
            bond_years=row["Bond Years"] if not pd.isna(row["Bond Years"]) else None,
            bond_penalty=row["Bond Penalty"],
            beds=row["Beds"],
            cr_2023_1=row.get("CR 2023 1", None),
            cr_2023_2=row.get("CR 2023 2", None),
            cr_2023_3=row.get("CR 2023 3", None),
            cr_2023_4=row.get("CR 2023 4", None),
            cr_2023_5=row.get("CR 2023 5", None),
            cr_2024_1=row.get("CR 2024 1", None),
            cr_2024_2=row.get("CR 2024 2", None),
            cr_2024_3=row.get("CR 2024 3", None),
            cr_2024_4=row.get("CR 2024 4", None),
            cr_2024_5=row.get("CR 2024 5", None),
        ))
        print(row)
    print(objs)
    SeatMatrixData.objects.bulk_create(objs)
    return JsonResponse({"status": "success", "inserted": len(objs)})


# 3. Fee / Stipend / Bond Data (38 files)
def upload_fees_bond_data(request):
    folder_path = os.path.join(settings.BASE_DIR, "static", "data", "feestipend&bonds")
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    objs = []
    for file in csv_files:
        category_name = os.path.splitext(file)[0]  # filename as category
        df = pd.read_csv(os.path.join(folder_path, file))
        for _, row in df.iterrows():
            objs.append(FeeStipendBondData(
                category_type=category_name,
                state=row["State"],
                institute=row["Institute"],
                course=row["Course"],
                quota=row["Quota"],
                fee=row["Fee"],
                stipend_year1=row["Stipend Year 1"],
                bond_years=row["Bond Years"] if not pd.isna(row["Bond Years"]) else None,
                bond_penalty=row["Bond Penalty"],
                beds=row["Beds"]
            ))
            print(row)
    print(objs)
    FeeStipendBondData.objects.bulk_create(objs)
    return JsonResponse({"status": "success", "inserted": len(objs)})


# 4. Closing Ranks Data (38 files)
# def upload_closingranks_data(request):
#     folder_path = os.path.join(settings.BASE_DIR, "static", "data", "Closing_Ranks")
#     csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

#     objs = []
#     for file in csv_files:
#         category_name = os.path.splitext(file)[0]  # filename as category
#         df = pd.read_csv(os.path.join(folder_path, file))
#         for _, row in df.iterrows():
#             objs.append(ClosingRanksData(
#                 category_type=category_name,
#                 quota=row["Quota"],
#                 category=row["Category"],
#                 state=row["State"],
#                 institute=row["Institute"],
#                 course=row["Course"],
#                 fee=row["Fee"],
#                 stipend_year1=row["Stipend Year 1"],
#                 bond_years=row["Bond Years"] if not pd.isna(row["Bond Years"]) else None,
#                 bond_penalty=row["Bond Penalty"],
#                 beds=row["Beds"],
#                 cr_2023_1=row.get("CR 2023 1", None),
#                 cr_2023_2=row.get("CR 2023 2", None),
#                 cr_2023_3=row.get("CR 2023 3", None),
#                 cr_2023_4=row.get("CR 2023 4", None),
#                 cr_2023_5=row.get("CR 2023 5", None),
#                 cr_2024_1=row.get("CR 2024 1", None),
#                 cr_2024_2=row.get("CR 2024 2", None),
#                 cr_2024_3=row.get("CR 2024 3", None),
#                 cr_2024_4=row.get("CR 2024 4", None),
#                 cr_2024_5=row.get("CR 2024 5", None),
#             ))
#             print(row)
#     print(objs)
#     ClosingRanksData.objects.bulk_create(objs)
#     return JsonResponse({"status": "success", "inserted": len(objs)})

import pandas as pd
import os
from django.conf import settings
from django.http import JsonResponse
from .models import ClosingRanksData

def upload_closingranks_data(request):
    folder_path = os.path.join(settings.BASE_DIR, "static", "data", "Closing_Ranks")
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    objs = []
    for file in csv_files:
        category_name = os.path.splitext(file)[0]  # filename as category
        df = pd.read_csv(os.path.join(folder_path, file))
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        for _, row in df.iterrows():
            # Clean and convert data
            fee = str(row.get("Fee", "")).strip()
            stipend = str(row.get("Stipend Year 1", "")).strip()
            bond_penalty = str(row.get("Bond Penalty", "")).strip()
            
            # Convert bond years safely
            bond_years = None
            try:
                if not pd.isna(row.get("Bond Years")):
                    bond_years = float(row["Bond Years"])
            except (ValueError, TypeError):
                bond_years = None
            
            # Convert beds safely
            beds = 0
            try:
                if not pd.isna(row.get("Beds")):
                    beds = int(row["Beds"])
            except (ValueError, TypeError):
                beds = 0
                
            # Helper function to safely convert to int
            def safe_int_convert(value):
                try:
                    if pd.isna(value) or value == '' or value is None:
                        return 0
                    return int(float(value))
                except (ValueError, TypeError):
                    return 0
            
            objs.append(ClosingRanksData(
                category_type=category_name,
                quota=str(row.get("Quota", "")).strip(),
                category=str(row.get("Category", "")).strip(),
                state=str(row.get("State", "")).strip(),
                institute=str(row.get("Institute", "")).strip(),
                course=str(row.get("Course", "")).strip(),
                fee=fee,
                stipend_year1=stipend,
                bond_years=bond_years,
                bond_penalty=bond_penalty,
                beds=beds,
                cr_2023_1=safe_int_convert(row.get("CR 2023 1")),
                cr_2023_2=safe_int_convert(row.get("CR 2023 2")),
                cr_2023_3=safe_int_convert(row.get("CR 2023 3")),
                cr_2023_4=safe_int_convert(row.get("CR 2023 4")),
                cr_2023_5=safe_int_convert(row.get("CR 2023 5")),
                cr_2024_1=safe_int_convert(row.get("CR 2024 1")),
                cr_2024_2=safe_int_convert(row.get("CR 2024 2")),
                cr_2024_3=safe_int_convert(row.get("CR 2024 3")),
                cr_2024_4=safe_int_convert(row.get("CR 2024 4")),
                cr_2024_5=safe_int_convert(row.get("CR 2024 5")),
            ))
    
    # Clear existing data before bulk create
    ClosingRanksData.objects.all().delete()
    ClosingRanksData.objects.bulk_create(objs, batch_size=1000)
    
    return JsonResponse({"status": "success", "inserted": len(objs)})


# app/views.py
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from .models import AllotmentData, SeatMatrixData, FeeStipendBondData, ClosingRanksData
from .serializers import (
    AllotmentDataSerializer, 
    SeatMatrixDataSerializer, 
    FeeStipendBondDataSerializer, 
    ClosingRanksDataSerializer
)
from core.pagination import StandardResultsSetPagination

# GET All Allotment Data
class AllotmentDataList(generics.ListAPIView):
    queryset = AllotmentData.objects.all()
    serializer_class = AllotmentDataSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['round', 'category', 'quota', 'state', 'institute', 'course']
    renderer_classes = [JSONRenderer]

# GET Seat Matrix Data
class SeatMatrixDataList(generics.ListAPIView):
    queryset = SeatMatrixData.objects.all()
    serializer_class = SeatMatrixDataSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['round', 'category', 'quota', 'state', 'institute', 'course']
    renderer_classes = [JSONRenderer]

# GET Fee/Stipend/Bond Data
class FeeStipendBondDataList(generics.ListAPIView):
    queryset = FeeStipendBondData.objects.all()
    serializer_class = FeeStipendBondDataSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_type', 'state', 'institute', 'course', 'quota', 'fee', 'stipend_year1', 'bond_years', 'bond_penalty', 'beds']
    renderer_classes = [JSONRenderer]

# GET Closing Ranks Data
# class ClosingRanksDataList(generics.ListAPIView):
#     queryset = ClosingRanksData.objects.all()
#     serializer_class = ClosingRanksDataSerializer
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = [ 'category', 'quota', 'state', 'institute', 'course']
#     renderer_classes = [JSONRenderer]

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from rest_framework.renderers import JSONRenderer
from .models import ClosingRanksData
from .serializers import ClosingRanksDataSerializer
from .pagination import StandardResultsSetPagination
class ClosingRanksDataFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(lookup_expr='icontains')
    quota = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.CharFilter(lookup_expr='icontains')
    institute = django_filters.CharFilter(lookup_expr='icontains')
    course = django_filters.CharFilter(lookup_expr='icontains')
    category_type = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = ClosingRanksData
        fields = ['category', 'quota', 'state', 'institute', 'course', 'category_type']

class ClosingRanksDataList(generics.ListAPIView):
    queryset = ClosingRanksData.objects.all()
    serializer_class = ClosingRanksDataSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ClosingRanksDataFilter
    search_fields = ['institute', 'course', 'state']
    ordering_fields = ['cr_2024_1', 'cr_2024_2', 'cr_2024_3', 'fee']
    ordering = ['cr_2024_1']  # Default ordering
    renderer_classes = [JSONRenderer]



class ResetPasswordAPIView(APIView):
    """Reset password with token"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        from .serializers import ResetPasswordSerializer
        
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        token = serializer.validated_data['token']
        uid = serializer.validated_data['uid']
        password = serializer.validated_data['password']
        
        # Decode uid and get user
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except:
            return Response({
                'success': False,
                'error': 'Invalid reset link. Please request a new password reset.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify token
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({
                'success': False,
                'error': 'Invalid or expired reset link. Please request a new password reset.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Reset password
        user.set_password(password)
        user.save()
        
        return Response({
            'success': True,
            'message': 'Password reset successfully. You can now log in with your new password.'
        }, status=status.HTTP_200_OK)

# ========================================
# UPDATED ForgotPasswordAPIView
# Replace your existing ForgotPasswordAPIView with this
# ========================================

import uuid

# ========================================
# UPDATED ForgotPasswordAPIView with Company Logo
# Replace your existing ForgotPasswordAPIView with this
# ========================================

class ForgotPasswordAPIView(APIView):
    """
    Send password reset email with company logo
    If email doesn't exist, silently auto-create account
    Both scenarios get identical "Password Reset" email
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        from .serializers import ForgotPasswordSerializer
        
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        try:
            # Try to get existing user
            user = User.objects.get(email=email)
            is_new_user = False
        except User.DoesNotExist:
            # ✅ USER DOESN'T EXIST - SILENTLY AUTO-CREATE NEW ACCOUNT
            # Generate username from email
            username = email.split('@')[0] + str(uuid.uuid4())[:6]
            
            # Create new user with unusable password
            user = User.objects.create(
                username=username,
                email=email,
                first_name=email.split('@')[0].capitalize(),
            )
            user.set_unusable_password()  # They'll set password via reset link
            user.save()
            
            is_new_user = True
            print(f"✅ Silently auto-created account for: {email}")
        
        # Generate token (same for both existing and new users)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset link
        frontend_url = getattr(settings, 'FRONTEND_URL')
        reset_link = f"{frontend_url}/reset-password?token={token}&uid={uid}"
        
        # Get user name
        user_name = user.first_name if user.first_name else (user.username if user.username else "User")
        
        # ✅ IDENTICAL EMAIL FOR BOTH - USER CAN'T TELL THE DIFFERENCE
        subject = 'Password Reset Request - Believers Consultancy'
        
        message = f"""Hello {user_name},

You requested to reset your password for Believers Consultancy.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

If you didn't request this, please ignore this email and your password will remain unchanged.

Best regards,
Believers Consultancy Team"""
        
        html_message = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            color: #333; 
            background: #f4f7fa; 
            margin: 0; 
            padding: 20px; 
            line-height: 1.6;
        }}
        .container {{ 
            max-width: 600px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 10px; 
            overflow: hidden; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 40px 30px; 
            text-align: center; 
        }}
        .logo-container {{
            margin-bottom: 20px;
        }}
        .logo {{
            max-width: 180px;
            height: auto;
            display: inline-block;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .header h1 {{ 
            margin: 15px 0 0 0; 
            font-size: 28px; 
            font-weight: 600; 
        }}
        .content {{ 
            padding: 40px 30px; 
        }}
        .greeting {{ 
            font-size: 18px; 
            color: #333; 
            margin-bottom: 20px; 
        }}
        .message {{ 
            font-size: 16px; 
            color: #555; 
            line-height: 1.8; 
            margin-bottom: 25px; 
        }}
        .message p {{
            margin: 0 0 15px 0;
        }}
        .button-container {{ 
            text-align: center; 
            margin: 35px 0; 
        }}
        .button {{ 
            display: inline-block; 
            padding: 16px 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white !important; 
            text-decoration: none; 
            border-radius: 8px; 
            font-weight: 600; 
            font-size: 16px; 
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); 
            transition: transform 0.2s; 
        }}
        .button:hover {{ 
            transform: translateY(-2px); 
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5); 
        }}
        .warning {{ 
            background: #fff3cd; 
            border-left: 4px solid #ffc107; 
            padding: 15px 20px; 
            margin: 25px 0; 
            border-radius: 4px; 
        }}
        .warning p {{ 
            margin: 0; 
            color: #856404; 
            font-size: 14px; 
            font-weight: 600;
        }}
        .security-tips {{ 
            background: #e7f3ff; 
            border-left: 4px solid #2196F3; 
            padding: 20px; 
            margin: 25px 0; 
            border-radius: 4px; 
        }}
        .security-tips h3 {{ 
            margin-top: 0; 
            margin-bottom: 10px; 
            color: #1976D2; 
            font-size: 16px; 
            font-weight: 600; 
        }}
        .security-tips ul {{ 
            margin: 10px 0; 
            padding-left: 20px; 
        }}
        .security-tips li {{ 
            margin: 8px 0; 
            font-size: 14px; 
            color: #555; 
        }}
        .footer {{ 
            background: #f8f9fa; 
            padding: 30px; 
            text-align: center; 
            border-top: 1px solid #e9ecef; 
        }}
        .footer p {{ 
            margin: 5px 0; 
            font-size: 13px; 
            color: #6c757d; 
        }}
        .footer .company {{ 
            font-weight: 600; 
            color: #495057; 
            font-size: 15px;
        }}
        .link-fallback {{ 
            margin-top: 30px; 
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
            font-size: 13px; 
            color: #6c757d; 
        }}
        .link-fallback p {{
            margin: 5px 0;
        }}
        .link-fallback a {{ 
            word-break: break-all; 
            color: #667eea;
            text-decoration: none;
        }}
        .divider {{
            height: 1px;
            background: linear-gradient(to right, transparent, #ddd, transparent);
            margin: 25px 0;
        }}
        @media only screen and (max-width: 600px) {{
            body {{
                padding: 10px;
            }}
            .header {{ 
                padding: 30px 20px; 
            }}
            .content {{ 
                padding: 30px 20px; 
            }}
            .header h1 {{ 
                font-size: 24px; 
            }}
            .logo {{
                max-width: 150px;
                padding: 12px;
            }}
            .button {{ 
                padding: 14px 30px; 
                font-size: 15px; 
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header with Logo -->
        <div class="header">
            <div class="logo-container">
                <img src="https://cdn.dribbble.com/userupload/45553315/file/7f757d2c0ca31bc348006d84b4ab5752.jpeg" 
                     alt="Believers Consultancy Logo" 
                     class="logo">
            </div>
            <h1>Password Reset Request</h1>
        </div>
        
        <!-- Content -->
        <div class="content">
            <div class="greeting">
                Hello <strong>{user_name}</strong>,
            </div>
            
            <div class="message">
                <p>We received a request to reset your password for your Believers Consultancy account.</p>
                <p>Click the button below to reset your password:</p>
            </div>
            
            <div class="button-container">
                <a href="{reset_link}" class="button">Reset My Password</a>
            </div>
            
            <div class="warning">
                <p>⏱️ This link will expire in 1 hour.</p>
            </div>
            
            <div class="message">
                <p>If you didn't request this password reset, please ignore this email and your password will remain unchanged. Your account is safe.</p>
            </div>
            
            <div class="divider"></div>
            
            <div class="security-tips">
                <h3>🔒 Security Tips</h3>
                <ul>
                    <li>Use a strong, unique password with a mix of letters, numbers, and symbols</li>
                    <li>Never share your password with anyone</li>
                    <li>Change your password regularly</li>
                    <li>Enable two-factor authentication when available</li>
                </ul>
            </div>
            
        
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p class="company">Believers Consultancy</p>
            <p>Empowering Your Medical Career Journey</p>
            <p style="margin-top: 15px; font-size: 12px;">This is an automated email. Please do not reply to this message.</p>
            <p style="margin-top: 5px;">© 2025 Believers Consultancy. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
        
        # Send email (same for both existing and new users)
        try:
            send_mail(
                subject=subject,
                message=message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            # ✅ Same success message regardless of whether account existed
            return Response({
                'success': True,
                'message': 'Password reset email sent successfully. Please check your inbox.'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Email error: {str(e)}")
            
            # If email fails and we auto-created user, delete them (cleanup)
            if is_new_user:
                user.delete()
                print(f"🗑️ Deleted auto-created user due to email failure")
            
            return Response({
                'success': False,
                'error': 'Failed to send email. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# ========================================
# ALTERNATIVE ForgotPasswordAPIView with Different Emails for New vs Existing Users 

class ForgotPasswordAPIView(APIView):
    """
    Send password reset email
    If email doesn't exist, auto-create account and send "set password" email
    This solves the database crash scenario!
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        from .serializers import ForgotPasswordSerializer
        
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        try:
            # Try to get existing user
            user = User.objects.get(email=email)
            is_new_user = False
        except User.DoesNotExist:
            # ✅ USER DOESN'T EXIST - AUTO-CREATE NEW ACCOUNT
            # Generate username from email
            username = email.split('@')[0] + str(uuid.uuid4())[:6]
            
            # Create new user with unusable password (they'll set it via reset link)
            user = User.objects.create(
                username=username,
                email=email,
                first_name=email.split('@')[0].capitalize(),  # Use email prefix as name
            )
            user.set_unusable_password()  # No password yet - they'll set via reset link
            user.save()
            
            is_new_user = True
            print(f"✅ Auto-created new account for: {email}")
        
        # Generate token (works for both existing and new users)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset link
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
        reset_link = f"{frontend_url}/reset-password?token={token}&uid={uid}"
        
        # Get user name
        user_name = user.first_name if user.first_name else (user.username if user.username else "User")
        
        # ✅ DIFFERENT EMAIL CONTENT FOR NEW VS EXISTING USERS
        if is_new_user:
            # Email for NEW user (account auto-created)
            subject = 'Welcome Back! Set Your New Password - Believers Consultancy'
            message = f"""Hello {user_name},

We noticed you don't have an active account, so we've created a new one for you!

Click the link below to set your password and access your account:
{reset_link}

This link will expire in 1 hour.

Once you set your password, you can log in and access all your data.

Best regards,
Believers Consultancy Team"""
            
            html_message = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; color: #333; background: #f4f7fa; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 40px 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .content {{ padding: 40px 30px; }}
        .button {{ display: inline-block; padding: 16px 40px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white !important; text-decoration: none; border-radius: 8px; font-weight: 600; }}
        .info-box {{ background: #d1fae5; border-left: 4px solid #10b981; padding: 15px; margin: 20px 0; border-radius: 4px; }}
        .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px; }}
        .footer {{ background: #f8f9fa; padding: 30px; text-align: center; color: #6c757d; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div style="font-size: 48px; margin-bottom: 10px;">🎉</div>
            <h1>Welcome Back!</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{user_name}</strong>,</p>
            <div class="info-box">
                <p style="margin: 0;"><strong>✨ Good News!</strong> We've created a fresh account for you.</p>
            </div>
            <p>Click the button below to set your password and access your account:</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" class="button">Set My Password</a>
            </p>
            <div class="warning">
                <p style="margin: 0;"><strong>⏱️ This link will expire in 1 hour.</strong></p>
            </div>
            <p>Once you set your password, you can log in and continue where you left off!</p>
        </div>
        <div class="footer">
            <p><strong>Believers Destination</strong></p>
            <p>© 2025 Believers Consultancy. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
        
        else:
            # Email for EXISTING user (normal password reset)
            subject = 'Password Reset Request - Believers Consultancy'
            message = f"""Hello {user_name},

You requested to reset your password for Believers Consultancy.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
Believers Consultancy Team"""
            
            html_message = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; color: #333; background: #f4f7fa; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .content {{ padding: 40px 30px; }}
        .button {{ display: inline-block; padding: 16px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white !important; text-decoration: none; border-radius: 8px; font-weight: 600; }}
        .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px; }}
        .footer {{ background: #f8f9fa; padding: 30px; text-align: center; color: #6c757d; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div style="font-size: 48px; margin-bottom: 10px;">🕊️</div>
            <h1>Password Reset Request</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{user_name}</strong>,</p>
            <p>We received a request to reset your password for your Believers Consultancy account.</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" class="button">Reset My Password</a>
            </p>
            <div class="warning">
                <p style="margin: 0;"><strong>⏱️ This link will expire in 1 hour.</strong></p>
            </div>
            <p>If you didn't request this password reset, please ignore this email. Your account is safe.</p>
        </div>
        <div class="footer">
            <p><strong>Believers Destination</strong></p>
            <p>© 2025 Believers Consultancy. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
        
        # Send email (same process for both)
        try:
            send_mail(
                subject=subject,
                message=message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            return Response({
                'success': True,
                'message': 'Password reset email sent successfully. Please check your inbox.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"❌ Email error: {str(e)}")
            
            # If email fails, delete the auto-created user (cleanup)
            if is_new_user:
                user.delete()
                print(f"🗑️ Deleted auto-created user due to email failure")
            
            return Response({
                'success': False,
                'error': 'Failed to send email. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




import threading
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()


def send_reset_email_async(email, user_name, reset_link):
    """Send email in background thread (non-blocking)"""
    subject = 'Password Reset Request - Believers Consultancy'
    
    message = f"""Hello {user_name},

You requested to reset your password for Believers Consultancy.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

Best regards,
Believers Consultancy Team"""
    
    html_message = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f7fa; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .logo {{ max-width: 180px; background: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; }}
        .content {{ padding: 40px 30px; }}
        .button {{ display: inline-block; padding: 16px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white !important; text-decoration: none; border-radius: 8px; font-weight: 600; }}
        .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://cdn.dribbble.com/userupload/45553315/file/7f757d2c0ca31bc348006d84b4ab5752.jpeg" alt="Logo" class="logo">
            <h1 style="margin: 15px 0 0 0;">Password Reset Request</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{user_name}</strong>,</p>
            <p>We received a request to reset your password.</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" class="button">Reset My Password</a>
            </p>
            <div class="warning">
                <p style="margin: 0;"><strong>⏱️ This link expires in 1 hour.</strong></p>
            </div>
            <p>If you didn't request this, ignore this email.</p>
        </div>
    </div>
</body>
</html>"""
    
    try:
        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,  # Don't crash in background thread
        )
        print(f"✅ Email sent to {email}")
    except Exception as e:
        print(f"❌ Email error: {str(e)}")


class ForgotPasswordAPIView(APIView):
    """
    Fast password reset - returns immediately, sends email in background
    Auto-creates account if email doesn't exist
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        from .serializers import ForgotPasswordSerializer
        
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Auto-create account
            username = email.split('@')[0] + str(uuid.uuid4())[:6]
            user = User.objects.create(
                username=username,
                email=email,
                first_name=email.split('@')[0].capitalize(),
            )
            user.set_unusable_password()
            user.save()
            print(f"✅ Auto-created: {email}")
        
        # Generate token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset link
        frontend_url = getattr(settings, 'FRONTEND_URL' )
        reset_link = f"{frontend_url}/reset-password?token={token}&uid={uid}"
        
        user_name = user.first_name if user.first_name else user.username
        
        # ✅ Send email in BACKGROUND THREAD (non-blocking)
        email_thread = threading.Thread(
            target=send_reset_email_async,
            args=(email, user_name, reset_link),
            daemon=True
        )
        email_thread.start()
        
        # ✅ Return IMMEDIATELY (don't wait for email)
        return Response({
            'success': True,
            'message': 'Password reset email sent successfully. Please check your inbox.'
        }, status=status.HTTP_200_OK)