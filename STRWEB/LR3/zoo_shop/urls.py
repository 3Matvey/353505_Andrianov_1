# zoo_shop/urls.py
from django.contrib import admin
from django.urls import path, include
from store.views import signup
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # аутентификация
    path('accounts/signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),  # login/, logout/, password_change/ и т.п.

    # все остальные урлы – ваше приложение store
    path('', include('store.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#handler403 = 'store.views.permission_denied'
