from django.core.exceptions import PermissionDenied
from .permissions import ROLE_PERMISSIONS

ROLE_PERMISSIONS = {
    "ADMIN": [
        "create_assignment",
        "view_all_results",
        "input_result",
        "manage_users",
    ],
      "HEADMASTER": [
        "create_assignment",
        "view_all_results",
        "input_result",
        "assign_teacher",
        "manage_teachers",
    ],
    "ACADEMIC_TEACHER": [
        "create_assignment",
        "input_result",
        "view_all_results",
        
    ],
    "NORMAL_TEACHER": [
        "create_assignment",
        "input_result",
        "view_own_results",
        "view_subjects",
    ],
    "STUDENT": [
        "view_assignments",
        "view_own_results",
        "view_subjects"
    ],
    "ACCOUNTANT": [
        "manage_fees",
    ],
}


def has_permission(user, permission):
    role = getattr(user, "role", None)

    if not role:
        return False

    permissions = ROLE_PERMISSIONS.get(role.upper(), [])

    return permission in permissions