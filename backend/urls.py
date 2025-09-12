from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from core import views
from django.http import JsonResponse

from core.views import (
    CollegeCutoffViewSet, UGSeatMatrixViewSet, PGFeeDetailsViewSet,
    ClosingRankViewSet, PrivateCollegeViewSet, NIRFUniversityRankingViewSet,
    INICETAllotmentViewSet, FAQCategoryViewSet, FAQViewSet,
    CollegeChoiceViewSet, MedicalCollegeList, SignupView,
    ProfileView, RankPredictorView, CollegeDatabaseList,
    verify_email_otp, LogoutView, HealthCheckView,
    CategoryBasedAllotmentView, CategoryBasedClosingRankView,
    CategoryBasedSeatMatrixView, CategoryBasedFeeStipendBondView,
    CategoryListView, CategorySummaryView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="BD Counselling API",
      default_version='v1',
      description="API docs for BD Counselling Platform",
      contact=openapi.Contact(email="shubham.saxena@believersdestination.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


# def home(request):
#     return JsonResponse({"message": "BD Counselling Backend API", "status": "OK"})

def home(request):
    return JsonResponse({"status": "ok", "message": "Backend live 🎉"})

# Routers for ViewSets
router = DefaultRouter()
router.register(r'cutoffs', CollegeCutoffViewSet)
router.register(r'ug-seat-matrix', UGSeatMatrixViewSet)
router.register(r'pg-fee-details', PGFeeDetailsViewSet)
router.register(r'closing-ranks', ClosingRankViewSet)
router.register(r'private-colleges', PrivateCollegeViewSet)
router.register(r'nirf-rankings', NIRFUniversityRankingViewSet)
router.register(r'allotments', INICETAllotmentViewSet)
router.register(r'faq-categories', FAQCategoryViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'choice-list', CollegeChoiceViewSet, basename='choice-list')
router.register(r'college-choices', CollegeChoiceViewSet, basename='collegechoice')

# Single urlpatterns definition
urlpatterns = [
    path('', home),  # Root endpoint
    path('health/', HealthCheckView.as_view(), name='health-check'),  # Health check endpoint
    path('admin/', admin.site.urls),

    # API Router URLs
    path('api/', include(router.urls)),

    # Auth & User
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path("auth/logout/", LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path("auth/verify-email/", verify_email_otp, name='verify-email'),
    # path("auth/logout/", LogoutView.as_view()),  # Uncomment when ready

    # Other APIs
    path('medical-colleges/', MedicalCollegeList.as_view(), name='medical-college-list'),
    path('rank-predictor/', RankPredictorView.as_view(), name='rank-predictor'),
    path('college-database/', CollegeDatabaseList.as_view(), name='college-database'),

    # Token auth and DRF login
    path('auth/login/', views.LoginAPIView.as_view(), name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls')),
    # Swagger and Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    
    path("api/allotments/", views.AllotmentListView.as_view(), name="allotment-list"),
    path("api/allotments/<str:category>/", views.AllotmentListView.as_view(), name="allotment-list-category"),

    path("api/closing-ranks/", views.ClosingRankListView.as_view(), name="closingrank-list"),
    path("api/closing-ranks/<str:category>/", views.ClosingRankListView.as_view(), name="closingrank-list-category"),

    path("api/seat-matrix/", views.SeatMatrixListView.as_view(), name="seatmatrix-list"),
    path("api/seat-matrix/<str:category>/", views.SeatMatrixListView.as_view(), name="seatmatrix-list-category"),

    path("api/fees/", views.FeeListView.as_view(), name="fee-list"),
    path("api/fees/<str:category>/", views.FeeListView.as_view(), name="fee-list-category"),

    # CSV upload:
    path("api/upload/<str:type>/", views.CSVUploadView.as_view(), name="csv-upload"),

    # Category-based API endpoints
    path("api/categories/", CategoryListView.as_view(), name="category-list"),
    path("api/category/summary/<str:category>/", CategorySummaryView.as_view(), name="category-summary"),
    path("api/category/allotments/<str:category>/", CategoryBasedAllotmentView.as_view(), name="category-allotments"),
    path("api/category/closing-ranks/<str:category>/", CategoryBasedClosingRankView.as_view(), name="category-closing-ranks"),
    path("api/category/seat-matrix/<str:category>/", CategoryBasedSeatMatrixView.as_view(), name="category-seat-matrix"),
    path("api/category/fee-stipend-bond/<str:category>/", CategoryBasedFeeStipendBondView.as_view(), name="category-fee-stipend-bond"),

]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
