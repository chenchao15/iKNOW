from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from backend.views import *


urlpatterns = [
   url(r'^search$', Search.as_view()),
]
