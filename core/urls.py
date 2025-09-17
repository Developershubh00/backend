# from django.urls import path, include
# from django.contrib import admin
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework.authtoken.views import obtain_auth_token

# from .views import (
#     CollegeCutoffViewSet, UGSeatMatrixViewSet, PGFeeDetailsViewSet,
#     ClosingRankViewSet, PrivateCollegeViewSet, NIRFUniversityRankingViewSet,
#     INICETAllotmentViewSet, FAQCategoryViewSet, FAQViewSet,
#     CollegeChoiceViewSet, MedicalCollegeList, SignupView,
#     ProfileView, RankPredictorView, CollegeDatabaseList,
#     verify_email_otp
#     # , LogoutView  # Uncomment if you implement this later
# )

# router = DefaultRouter()
# router.register(r'cutoffs', CollegeCutoffViewSet)
# router.register(r'ug-seat-matrix', UGSeatMatrixViewSet)
# router.register(r'pg-fee-details', PGFeeDetailsViewSet)
# router.register(r'closing-ranks', ClosingRankViewSet)
# router.register(r'private-colleges', PrivateCollegeViewSet)
# router.register(r'nirf-rankings', NIRFUniversityRankingViewSet)
# router.register(r'allotments', INICETAllotmentViewSet)
# router.register(r'faq-categories', FAQCategoryViewSet)
# router.register(r'faqs', FAQViewSet)
# router.register(r'choice-list', CollegeChoiceViewSet, basename='choice-list')
# router.register(r'college-choices', CollegeChoiceViewSet, basename='collegechoice')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('medical-colleges/', MedicalCollegeList.as_view(), name='medical-college-list'),
#     path('auth/signup/', SignupView.as_view(), name='signup'),
#     path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('auth/profile/', ProfileView.as_view(), name='profile'),
#     path("auth/verify-email/", verify_email_otp, name='verify-email'),

#     path('rank-predictor/', RankPredictorView.as_view(), name='rank-predictor'),
#     path('college-database/', CollegeDatabaseList.as_view(), name='college-database'),

#     path('admin/', admin.site.urls),
#     path('api/core/', include('core.urls')),
#     # path('api/inicet/', include('inicet.urls')),
#     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
#     path('api-auth/', include('rest_framework.urls')),

#     # path("auth/logout/", LogoutView.as_view()),  # Uncomment when ready
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CollegeCutoffViewSet, INICETAllotmentViewSet, UGSeatMatrixViewSet,
    PGFeeDetailsViewSet, ClosingRankViewSet, PrivateCollegeViewSet,
    NIRFUniversityRankingViewSet, FAQViewSet, FAQCategoryViewSet,
    CollegeChoiceViewSet, RankPredictorView, CollegeDatabaseList,
    SignupView, ProfileView, MedicalCollegeList, EmailVerificationView, LoginAPIView,
    verify_email_otp,
)

router = DefaultRouter()
router.register(r'college-cutoffs', CollegeCutoffViewSet)
router.register(r'inicet-allotments', INICETAllotmentViewSet)
router.register(r'ug-seat-matrix', UGSeatMatrixViewSet)
router.register(r'pg-fees', PGFeeDetailsViewSet)
router.register(r'closing-ranks', ClosingRankViewSet)
router.register(r'private-colleges', PrivateCollegeViewSet)
router.register(r'nirf-rankings', NIRFUniversityRankingViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'faq-categories', FAQCategoryViewSet)
router.register(r'college-choices', CollegeChoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('medical-colleges/', MedicalCollegeList.as_view(), name='medical-colleges'),
    path('rank-predictor/', RankPredictorView.as_view(), name='rank-predictor'),
    path('college-database/', CollegeDatabaseList.as_view(), name='college-database'),
    path('email-verification/', EmailVerificationView.as_view(), name='email-verification'),
    path('verify-email-otp/', verify_email_otp, name='verify-email-otp'),
]
