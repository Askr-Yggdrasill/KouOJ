from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.announcements.models import Announcement
from apps.problems.models import Problem
from apps.submissions.models import Submission
from .serializers import HomeAnnouncementSerializer, HomeProblemSerializer

class HomeView(APIView):
  '''首页接口，返回每日一题、未完成的题目和公告'''
  permission_classes = [AllowAny]
  def get(self, request):
    '''获取每日一题，未完成题目与公告'''
    daily_problem = Problem.objects.filter(is_public=True).order_by("?").first()
    unfinished_problems = Problem.objects.filter(is_public=True)
    if request.user.is_authenticated:
      solved_problem_ids = Submission.objects.filter(
        user = request.user,
        status = Submission.Status.ACCEPTED
      ).values_list("problem_id", flat=True)

      unfinished_problems = unfinished_problems.exclude(id__in=solved_problem_ids)
    unfinished_problems = unfinished_problems.order_by("id")[:5]

    announcements = Announcement.objects.filter(is_active=True)[:5]

    # 返回相应的json数据
    return Response(
      {
        "daily_problem": HomeProblemSerializer(daily_problem).data
        if daily_problem else None,
        "unfinished_problems": HomeProblemSerializer(
          unfinished_problems, 
          many=True,
        ).data,
        "announcements": HomeAnnouncementSerializer(
          announcements,
          many=True,
        ).data,
      }
    )
