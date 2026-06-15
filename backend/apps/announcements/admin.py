from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
  '''注册admin界面'''
  list_display = ("id", "title", "is_active", "is_pinned", "created_at")
  list_filter = ("is_active", "is_pinned")
  search_fields = ("title", "content")