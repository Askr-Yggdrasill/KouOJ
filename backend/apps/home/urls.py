from django.urls import path

from .views import HomeView

# 主页相关的URL配置
urlpatterns = [
  path("", HomeView.as_view(), name="home"),
]