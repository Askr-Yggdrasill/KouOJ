from rest_framework import serializers
from .models import Solution

class SolutionSerializer(serializers.ModelSerializer):
  '''题解转换json'''
  author_username = serializers.CharField(source="author.username", read_only=True)

  class Meta:
    model = Solution
    fields = [
      "id",
      "problem",
      "author",
      "author_username",
      "title",
      "content",
      "language",
      "is_public",
      "created_at",
      "updated_at",
    ]
    read_only_fields = [
      "id",
      "problem",
      "author",
      "author_username",
      "created_at",
      "updated_at",
    ]