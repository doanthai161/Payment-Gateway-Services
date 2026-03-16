from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("transactions.urls")),
    path("", include("django_prometheus.urls")),
]
