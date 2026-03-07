
ROLE_PERMISSIONS = {
    "ADMIN": [
        "create_assignment",
        "view_all_results",
        "input_result",
        "manage_users",
    ],
    "TEACHER": [
        "create_assignment",
        "input_result",
        "view_subjects",
    ],
    "STUDENT": [
        "view_assignments",
        "view_own_results",
    ],
    "ACCOUNTANT": [
        "manage_fees",
    ],
}
