from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('hsta', views.index, name='index'),
    path('hsta/login', views.log_in, name='login'),
    path('hsta/logout', views.log_out, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
