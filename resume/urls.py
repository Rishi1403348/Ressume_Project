from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home_view, resume_view, sample_view
from django.urls import path
from .views import home_view, resume_view, sample_view

urlpatterns = [
    path('', home_view, name='home'),
    path('resume/', resume_view, name='resume'),
    path('sample/', sample_view, name='sample'),
    path('', home_view, name='home'),
    path('resume/', resume_view, name='resume'),
    path('sample/', sample_view, name='sample'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
