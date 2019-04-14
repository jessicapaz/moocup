from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from .users.views import UserViewSet, UserCreateListView
from .users.custom_auth_token.views import CustomAuthToken
from .management.views import UseManagementViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)

router.register(r'use', UseManagementViewSet, base_name='use')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
    path('users/', UserCreateListView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
