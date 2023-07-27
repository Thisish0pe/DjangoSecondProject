from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

User = get_user_model()

class IsQuestionerOnly(BasePermission):
    # 작성자만 접근
    pass