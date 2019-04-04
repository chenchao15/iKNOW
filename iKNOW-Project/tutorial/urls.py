from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from tutorial.views import *


urlpatterns = [
   url(r'^offical_tutorial$', OfficalTutorial.as_view()),
   url(r'^student_share$', StudentShare.as_view()),
   url(r'^post_tutorial$', PostTutorial.as_view()),
   url(r'^tutorial$', MyTutorial.as_view()),
   url(r'^tutorial_status$', TutorialStatus.as_view()),
   url(r'^tutorial_info/(?P<pk>[0-9]+)$', TutorialInfo.as_view()),
   url(r'^image_upload$', ImageUpload.as_view())
]

