from django.db import models
from django.conf import settings

from apps.problems.models import Problem

class Solution(models.Model):
  problem = models.ForeignKey(
    Problem,
    on_delete=models.CASCADE,
    related_name="solutions",
  )

  author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="solutions",
  )
  problem = models.ForeignKey(
    Problem,
    on_delete=models.CASCADE,
    related_name="solutions",
  )

  author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="solutions",
  )

  title = models.CharField(max_length=100)
  content = models.TextField()
  language = models.CharField(max_length=20,blank=True)
  is_public = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ["-created_at"]
  
  def __str__(self):
    return f"{self.problem_id} - {self.title}"