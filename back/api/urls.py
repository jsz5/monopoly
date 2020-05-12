from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from api import views

schema_view = get_schema_view(
    openapi.Info(title="API", default_version="v1"), public=True)

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=None), name="schema-swagger-ui"),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("test/", views.Test.as_view(), name="test")
]
