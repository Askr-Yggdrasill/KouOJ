from rest_framework import permissions

class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
  '''创建权限，该权限只允许本人或者管理员，用于题解的修改和删除'''
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.author==request.user or request.user.is_staff