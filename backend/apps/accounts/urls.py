from django.urls import path

from .views import MeView, RegisterView, ChangePasswordView, MeStatsView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
    path('me/stats/', MeStatsView.as_view(), name="me-stats"),
]
