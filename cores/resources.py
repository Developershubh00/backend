from import_export import resources
from .models import (
    CollegeCutoff,
    MedicalCollege,
    INICETAllotment,
    UGSeatMatrix,
    PGFeeDetails,
    ClosingRank,
    PrivateCollege,
    NIRFUniversityRanking,
    RankPredictionCollege,
    CollegeDatabase
)

class CollegeCutoffResource(resources.ModelResource):
    class Meta:
        model = CollegeCutoff

class MedicalCollegeResource(resources.ModelResource):
    class Meta:
        model = MedicalCollege

class INICETAllotmentResource(resources.ModelResource):
    class Meta:
        model = INICETAllotment

class UGSeatMatrixResource(resources.ModelResource):
    class Meta:
        model = UGSeatMatrix

class PGFeeDetailsResource(resources.ModelResource):
    class Meta:
        model = PGFeeDetails

class ClosingRankResource(resources.ModelResource):
    class Meta:
        model = ClosingRank

class PrivateCollegeResource(resources.ModelResource):
    class Meta:
        model = PrivateCollege

class NIRFUniversityRankingResource(resources.ModelResource):
    class Meta:
        model = NIRFUniversityRanking

class RankPredictionCollegeResource(resources.ModelResource):
    class Meta:
        model = RankPredictionCollege

class CollegeDatabaseResource(resources.ModelResource):
    class Meta:
        model = CollegeDatabase
