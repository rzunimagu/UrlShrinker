from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from rest_framework import routers
from shrinker import views


router = routers.DefaultRouter()
router.register('urls', views.UrlRedirectViewSet, basename='urls')

handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('<slug:url_new>', views.RedirectToOriginalUrlView.as_view(), name='redirect-url'),
    path('', views.MainPageView.as_view())
]
