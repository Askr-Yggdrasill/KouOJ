from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Announcement
from .serializers import AnnouncementSerializer

class AnnouncementListView(generics.ListAPIView):
  '''公告列表视图，返回所有活跃的公告，置顶公告优先显示'''
  serializer_class = AnnouncementSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    return Announcement.objects.filter(is_active =True)

