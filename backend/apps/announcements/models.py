from django.db import models

class Announcement(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField(max_length=200)
  is_active = models.BooleanField(default=True)
  is_pinned = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  # 置顶序优先，然后按照创建时间逆序
  class Meta:
    ordering = ["-is_pinned","-created_at"]

  def __str__(self):
    return self.title
