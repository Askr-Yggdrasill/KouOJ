from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.problems.models import Problem
from .models import Solution
from .serializers import SolutionSerializer
from .permissions import IsAuthorOrAdminOrReadOnly

class ProblemSolutionsListCreateView(generics.ListCreateAPIView):
  '''题解列表和创建接口'''
  serializer_class = SolutionSerializer
  permission_classes = [IsAuthorOrAdminOrReadOnly]
  

  def get_queryset(self):
    problem_id = self.kwargs["problem_id"]
    return Solution.objects.select_related("author", "problem").filter(
      problem_id=problem_id,
      is_public=True,
    )

  def perform_create(self, serializer):
    problem_id = self.kwargs["problem_id"]
    problem = Problem.objects.get(id=problem_id)
    serializer.save(author=self.request.user, problem=problem)

class SolutionDetailView(generics.RetrieveUpdateDestroyAPIView):
  '''支持GET PATCH DELETE'''
  serializer_class = SolutionSerializer
  permission_classes = [IsAuthorOrAdminOrReadOnly]

  def get_queryset(self):
    return Solution.objects.select_related("author", "problem").filter(is_public=True,)