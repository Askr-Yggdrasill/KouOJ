from django.urls import path
from .views import ProblemSolutionsListCreateView, SolutionDetailView

urlpatterns = [
  path(
    "problems/<int:problem_id>/solutions/",
    ProblemSolutionsListCreateView.as_view(),
    name="problem-solutions",
  ),
  path(
    "solutions/<int:pk>/",
    SolutionDetailView.as_view(),
    name="solution-detail",
  )
]

