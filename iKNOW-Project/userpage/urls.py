from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from userpage.views import *

urlpatterns = [
    url(r'^signup$', SignUp.as_view()),
    url(r'^login$', Login.as_view()),
    url(r'^con_detail/(?P<pk>[0-9]+)$', ConDetail.as_view()),
    url(r'^org_detail/(?P<pk>[0-9]+)$', OrgDetail.as_view()),
    url(r'^avatar_upload$', AvatarUpload.as_view()),
    url(r'^competition$', MyCompetition.as_view()),
    url(r'^collect_tutorial$', CollectTutorial.as_view()),
    url(r'^is_tutorial$', IsTutorial.as_view()),
    url(r'^personal_letter$', MyPersonalLetter.as_view()),
    url(r'^collect_competition$', CollectCompetition.as_view()),
    url(r'^letter_detail$', LetterDetail.as_view()),
    url(r'^logout$', Logout.as_view()),
    url(r'^username$', Username.as_view()),
    url(r'^email$', Email.as_view()),
    url(r'^forget_password$', ForgetPassword.as_view()),
    url(r'^change_password$', ChangePassword.as_view()),
    url(r'^validate_email$', ValidateEmail.as_view()),
    url(r'^other_contestant_competition$', OtherContestantCompetition.as_view()),
    url(r'^other_organizer_competition$', OtherOrganizerCompetition.as_view()),
    url(r'^other_contestant_tutorial$', OtherContestantTutorial.as_view()),
    url(r'^other_organizer_tutorial$', OtherOrganizerTutorial.as_view()),
    url(r'^manager_login$', ManagerLogin.as_view())
]

