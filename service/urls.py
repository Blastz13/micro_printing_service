from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ServicePage

urlpatterns = [
    path('', ServicePage.as_view(), name="ServicePage")
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
