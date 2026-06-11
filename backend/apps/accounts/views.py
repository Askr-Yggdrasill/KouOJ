from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDate
from collections import defaultdict
from django.utils import timezone

from apps.submissions.models import Submission
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer

# 注册用
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# 登录用
class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# 修改密码用
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"detail":"修改成功"})
    
# 获取个人信息用
class MeStatsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        submissions = Submission.objects.filter(user=user)
        accepted_submissions = submissions.filter(status=Submission.Status.ACCEPTED)
        solved_problems_ids = accepted_submissions.values_list("problem_id", flat=True).distinct()
        solved_count = solved_problems_ids.count()

        difficulty_stats = {
            "easy": accepted_submissions.filter(problem__difficulty="easy").distinct().count(),
            "medium": accepted_submissions.filter(problem__difficulty="medium").distinct().count(),
            "hard": accepted_submissions.filter(problem__difficulty="hard").distinct().count(),
        }

        heatmap_counts = defaultdict(int)
        for created_at in accepted_submissions.exclude(created_at__isnull=True).values_list("created_at", flat=True):
            date_text = timezone.localtime(created_at).date().isoformat()
            heatmap_counts[date_text]+=1

        return Response(
            {
                "submit_count": submissions.count(),
                "accepted_count": accepted_submissions.count(),
                "solved_count": solved_count,
                "difficulty": difficulty_stats,
                "heatmap": [
                    {"date":date, "count":count}
                    for date, count in sorted(heatmap_counts.items())
                ],
            }
        )