from django.urls import path
from django.conf.urls import url, include

from .views import RankView, UpdateView, ProblemListingView, CompareView, CompareResult, ResetRank, ResetRelationship

urlpatterns = [
    path(r'', RankView.as_view(), name='ranking'),
    path(r'update_all_user', UpdateView.as_view(), name = 'updating'),
    path(r'list', ProblemListingView.as_view(), name = 'listing'),
    path(r'compare', CompareView.as_view(), name = 'compare'),
    path(r'compare_result', CompareResult.as_view(), name = "compare_result"),
    path(r'reset_rank_12321', ResetRank.as_view(), name="reset rank"),
    path(r'reset_relationship_12321', ResetRelationship.as_view(), name="reset relationship")
]