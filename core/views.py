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
from .models import Allotment, ClosingRank, SeatMatrix, FeeStipendBond
from .serializers import (
    UGSeatMatrixSerializer, PGFeeDetailsSerializer, OldClosingRankSerializer,
    PrivateCollegeSerializer, NIRFUniversityRankingSerializer, LoginSerializer,
    AllotmentSerializer, ClosingRankSerializer, SeatMatrixSerializer, FeeStipendBondSerializer
)

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


User = get_user_model()

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

# class LoginAPIView(APIView):
#     @swagger_auto_schema(
#         request_body=LoginSerializer,
#         responses={
#             200: openapi.Response(
#                 description="Successful login",
#                 examples={
#                     "application/json": {
#                         "access": "your_jwt_token",
#                         "refresh": "your_refresh_token",
#                         "user_id": 1,
#                         "username": "shubh",
#                         "email": "shubh@example.com"
#                     }
#                 }
#             ),
#             401: "Invalid credentials",
#         }
#     )
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    "application/json": {
                        "access": "your_jwt_token",
                        "refresh": "your_refresh_token",
                    }
                }
            ),
            401: "Invalid credentials",
        }
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'detail': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Find user by email
            user = User.objects.get(email=email)
            
            # Authenticate using username (since Django auth uses username)
            authenticated_user = authenticate(
                request, 
                username=user.username, 
                password=password
            )
            
            if authenticated_user:
                # Generate tokens
                refresh = RefreshToken.for_user(authenticated_user)
                
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'detail': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except User.DoesNotExist:
            return Response({
                'detail': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'detail': 'Login failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Removed duplicate SignupView and ProfileView definitions to avoid conflicts.

class CollegeCutoffViewSet(viewsets.ModelViewSet):
    queryset = CollegeCutoff.objects.all()
    serializer_class = CollegeCutoffSerializer

class MedicalCollegeList(generics.ListAPIView):
    queryset = MedicalCollege.objects.all()
    serializer_class = MedicalCollegeSerializer

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
            return Response(UserProfileSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)


# class ProfileView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data)

#     def put(self, request):
#         user = request.user
#         # Update all fields that are provided
#         if 'email' in request.data:
#             user.email = request.data['email']
#         if 'name' in request.data:
#             user.first_name = request.data['name']
#         if 'phone' in request.data:
#             user.phone = request.data['phone']
#         if 'neet_rank' in request.data:
#             user.neet_rank = request.data['neet_rank']
#         if 'category' in request.data:
#             user.category = request.data['category']
#         if 'state' in request.data:
#             user.state = request.data['state']
        
#         user.save()
#         serializer = UserProfileSerializer(user)
#         return Response(serializer.data)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # Map backend field names to frontend expected names
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.first_name,
            'phone': user.phone,
            'neetRank': user.neet_rank,  # Map neet_rank to neetRank
            'category': user.category,
            'state': user.state,
        }
        return Response(user_data)

    def put(self, request):
        user = request.user
        # Update all fields that are provided
        if 'email' in request.data:
            user.email = request.data['email']
        if 'name' in request.data:
            user.first_name = request.data['name']
        if 'phone' in request.data:
            user.phone = request.data['phone']
        if 'neetRank' in request.data:  # Handle neetRank from frontend
            user.neet_rank = request.data['neetRank']
        if 'category' in request.data:
            user.category = request.data['category']
        if 'state' in request.data:
            user.state = request.data['state']
        
        user.save()
        
        # Return mapped field names
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.first_name,
            'phone': user.phone,
            'neetRank': user.neet_rank,
            'category': user.category,
            'state': user.state,
        }
        return Response(user_data)
    
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
