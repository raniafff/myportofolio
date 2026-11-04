from django.urls import path
from main.api_views import (
    api_project_list,
    api_project_detail,
    api_project_toggle_star,
    api_education_list,
    api_education_detail,
    api_education_toggle_star,
)

app_name = "api_v1"

urlpatterns = [
    # Projects Endpoints
    path("projects/", api_project_list, name="api_project_list"),
    path("projects/<uuid:id>/", api_project_detail, name="api_project_detail"),
    path("projects/<uuid:id>/star/", api_project_toggle_star, name="api_project_toggle_star"),

    # Education Endpoints
    path("education/", api_education_list, name="api_education_list"),
    path("education/<int:id>/", api_education_detail, name="api_education_detail"),
    path("education/<int:id>/star/", api_education_toggle_star, name="api_education_toggle_star"),
]

