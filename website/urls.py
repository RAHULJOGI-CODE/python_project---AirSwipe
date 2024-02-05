from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("present/<int:file_id>", views.present, name="present"),
    path("myaccount/", views.myaccount, name="myaccount"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout, name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
