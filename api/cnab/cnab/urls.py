"""cnab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from cnab import settings
from core import views

router = routers.DefaultRouter()
router.register("cnab-documentation", views.CNABDocumentationViewSet)
router.register("store", views.StoreViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/file/", views.FileAPIView.as_view()),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        # swagger patterns
        path("api/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
        # Optional UI:
        path(
            "api/docs/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/docs/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
        ),
        
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
