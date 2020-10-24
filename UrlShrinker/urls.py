from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from shrinker import views


router = routers.DefaultRouter()
router.register('urls', views.UrlRedirectViewSet, basename='urls')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('<slug:url_new>', views.RedirectToOriginalUrlView.as_view(), name='redirect-url'),
    path('', views.MainPageView.as_view())
]
