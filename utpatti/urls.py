
from utpatti.settings import MEDIA_ROOT
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name = "home"),
    path('account/',include('account.urls')),
    path('crop/',include('crop.urls')),
    path('bidding/', include('bidding.urls')),
    
] + static(settings.MEDIA_URL , document_root = MEDIA_ROOT)
