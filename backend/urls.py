# backend/urls.py
from django.contrib import admin
from django.urls import path, include  # Add include
from django.conf import settings         # Add this
from django.conf.urls.static import static # Add this

urlpatterns = [
    path('admin/', admin.site.urls),
    # We will add our app's URLs here later
    path('api/', include('summarizer.urls')), # Add this line

]

# Add this line to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)