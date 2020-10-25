from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from rest_framework import routers
from shrinker import views
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter()
router.register('urls', views.UrlRedirectViewSet, basename='urls')

handler404 = views.handler404
handler500 = views.handler500

urlpatterns = []
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('<slug:url_new>', views.RedirectToOriginalUrlView.as_view(), name='redirect-url'),
    path('', views.MainPageView.as_view())
]
