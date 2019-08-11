from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static 
urlpatterns = [
    path('', views.home, name='home'),
    path('image_upload/', views.upload_image, name = 'image_upload'),
    path('login', views.login, name='login'),
    path('select', views.select, name='select'),
    path('ocr', views.ocr, name='ocr'),
    path('profile', views.profile, name='profile'),
    path('demo', views.demo, name='demo'),
]

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 

