from django.urls import path
from .views import AnnouncementListView

# 公告相关的URL配置
urlpatterns = [
  path("", AnnouncementListView.as_view(), name="announcement-list"),
]