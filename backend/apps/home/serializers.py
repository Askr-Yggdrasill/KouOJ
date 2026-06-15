from rest_framework import serializers

from apps.announcements.models import Announcement
from apps.problems.models import Problem, Tag

class HomeTagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ["id","name"]

class HomeProblemSerializer(serializers.ModelSerializer):
  '''每日一题转换json，轻量级展示题目信息'''
  tags = HomeTagSerializer(many=True, read_only=True)
  
  class Meta:
    model = Problem
    fields = [
      "id",
      "title",
      "difficulty",
      "time_limit",
      "memory_limit",
      "tags",
    ]

class HomeAnnouncementSerializer(serializers.ModelSerializer):
  '''公告内容转换json'''
  class Meta:
    model = Announcement
    fields = [
      "id",
      "title",
      "content",
      "is_pinned",
      "created_at",
    ]
