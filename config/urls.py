from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/api/', include('v1.post.urls'), name='blog'),
    path('accounts/api/', include('v1.accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)