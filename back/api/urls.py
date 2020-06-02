from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from api import views

schema_view = get_schema_view(
    openapi.Info(title="API", default_version="v1"), public=True
)

urlpatterns = [
    path(
        "", schema_view.with_ui("swagger", cache_timeout=None), name="schema-swagger-ui"
    ),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path(
        "playing-user-ready/",
        views.PlayingUserReadyUpdateView.as_view(),
        name="playing-user-ready",
    ),
    path("playing-users/", views.PlayingUserListView.as_view(), name="playing-users"),
    path("dice-roll/", views.DiceRollView.as_view(), name="dice-roll"),
    path("board/", views.BoardView.as_view(), name="board"),
    path("field/<int:pk>/", views.FieldView.as_view(), name="board"),
    path("lobby", views.LobbyView.as_view(), name='lobby'),
    path("field/buy", views.BuyFieldView.as_view(), name='buy-field'),
    path("field/sell/<int:pk>/", views.SellFieldView.as_view(), name='sell-field'),
    path("field/pledge/", views.PledgeFieldView.as_view(), name='pledge-field'),
    path("field/pledge-reverse/", views.UnPledgeFieldView.as_view(), name='pledge-field-revere'),
    path("field/buy-estate/", views.BuyEstateFieldView.as_view(), name='buy-estate'),
    path("field/sell-estate/", views.SellEstateFieldView.as_view(), name='sell-estate'),
    path("transaction/", views.TransactionsView.as_view(), name='transactions'),
    path("transaction/<int:pk>/", views.TransactionUpdateView.as_view(), name='transaction-update'),
    path("auth-user/", views.AuthUserView.as_view(), name='auth-user')
]
