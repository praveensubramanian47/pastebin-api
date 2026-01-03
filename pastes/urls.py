from django.urls import path
from .views import HealthCheckView, CreatePasteView, FetchPasteView

urlpatterns = [
    path('api/healthz', HealthCheckView.as_view(), name='healthz'),
    path('api/pastes', CreatePasteView.as_view(), name='create_paste'),
    path('api/pastes/<str:id>', FetchPasteView.as_view(), name='fetch_paste'),
    # path('p/<str:id>', view_paste_html, name='view_paste')
]
