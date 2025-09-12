from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CollegeCutoff
from .models import MedicalCollege
from .models import INICETAllotment
from .models import UGSeatMatrix, PGFeeDetails, PrivateCollege, NIRFUniversityRanking
from .models import RankPredictionCollege
from .models import CollegeChoice
from .models import CollegeDatabase
from .models import Allotment, ClosingRank, SeatMatrix, FeeStipendBond
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import FAQ, FAQCategory
import uuid
User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist.")

            user = authenticate(username=user.username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is deactivated.")
                refresh = RefreshToken.for_user(user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            else:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Email and password required.")

import uuid

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name', 'phone', 'neet_rank', 'category', 'state']

    def create(self, validated_data):
        name = validated_data.pop('name')
        password = validated_data.pop('password')

        # Auto-generate username from name or fallback to uuid
        username = name.lower().replace(" ", "")[:12] + str(uuid.uuid4())[:4]
        user = User(username=username, first_name=name, **validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')  # expose 'first_name' as 'name'

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'neet_rank', 'category', 'state']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class CollegeCutoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeCutoff
        fields = '__all__'

class MedicalCollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCollege
        fields = '__all__'




class INICETAllotmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = INICETAllotment
        fields = '__all__'

       

class UGSeatMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = UGSeatMatrix
        fields = '__all__'

class PGFeeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGFeeDetails
        fields = '__all__'

class OldClosingRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosingRank
        fields = '__all__'

class PrivateCollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateCollege
        fields = '__all__'

class NIRFUniversityRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NIRFUniversityRanking
        fields = '__all__'

class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    category = FAQCategorySerializer()

    class Meta:
        model = FAQ
        fields = '__all__'

class CollegeChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeChoice
        fields = ['id', 'college_name', 'course_name', 'state', 'rank']

        


class RankPredictionCollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankPredictionCollege
        fields = '__all__'

class CollegeDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeDatabase
        fields = '__all__'

# New Category-based Serializers
class AllotmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allotment
        fields = "__all__"


class ClosingRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosingRank
        fields = "__all__"


class SeatMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatMatrix
        fields = "__all__"


class FeeStipendBondSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStipendBond
        fields = "__all__"
