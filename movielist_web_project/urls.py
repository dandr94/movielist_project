from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('movielist_web_project.web.urls')),
                  path('', include('movielist_web_project.accounts.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'movielist_web_project.web.errors.handle_404_not_found'
handler403 = 'movielist_web_project.web.errors.handle_403_forbidden'
