from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from post import urls as post_urls
from userauths import urls as auth_urls
from direct import urls as direct_urls
from comment import urls as comment_urls
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(post_urls)),
    path('',include(auth_urls)),
    path('comment/',include(comment_urls)),
    path('message/',include(direct_urls)),
]

# This is used for
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)