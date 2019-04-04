from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ContestantUser)
admin.site.register(OrganizerUser)
admin.site.register(Competition)
admin.site.register(Tutorial)
admin.site.register(TutorialComment)
admin.site.register(PersonalLetter)
admin.site.register(EmailToken)
admin.site.register(PasswordToken)
admin.site.register(Phase)
admin.site.register(Notice)
admin.site.register(GroupMessage)
admin.site.register(Grade)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(Enrolment)
admin.site.register(Attachment)
admin.site.register(CompetitionAndContestant)
admin.site.register(CompetitionComment)
