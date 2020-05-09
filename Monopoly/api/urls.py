from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from api import views

schema_view = get_schema_view(
    openapi.Info(title="API", default_version="v1"), public=True)

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=None), name="schema-swagger-ui"),
    path("test/", views.Test.as_view(), name="test")
]
