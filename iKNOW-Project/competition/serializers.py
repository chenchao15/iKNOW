from rest_framework import serializers
from backend.models import *
from userpage.serializers import *

class CompetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competition
        fields = ('id', 'name', 'organizer', 'sponsor', 'contractor', 'status', 'level', 'objectrange', 'objectschool', 'category', 'detail', 'pic_url')


class HomeCompetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competition
        fields = ('id', 'name', 'pic_url')

         
class SimplePhaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phase
        fields = ('id', 'name')


class NoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'status', 'post_time')


class EventSerializer(serializers.ModelSerializer):

    contestant = SpecialContestantUserSerializer(read_only=True)
    class Meta:

        model = Event
        fields = ('id', 'contestant', 'time', 'event_type', 'content', 'status', 'reason', 'handle_time')


class PostEventSerializer(serializers.ModelSerializer):

    class Meta:

        model = Event
        fields = ('id', 'is_team', 'event_type', 'content')


class GradeSerializer(serializers.ModelSerializer):

    contestant = SimpleContestantUserSerializer(read_only=True)
    class Meta:

        model = Grade
        fields = ('id', 'contestant', 'time', 'is_team', 'submit_url', 'is_handled', 'submit_grade', 'handle_content', 'handle_time')


class GetGradeSerializer(serializers.ModelSerializer):

    contestant = SimpleContestantUserSerializer(read_only=True)
    class Meta:

        model = Grade
        fields = ('id', 'contestant', 'time', 'is_team', 'is_handled', 'submit_grade', 'handle_time')


class PostGradeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Grade
        fields = ('id', 'submit_url')


class SimpleGradeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Grade
        fields = ('id', 'time', 'is_team', 'submit_grade')


class GroupMessageSerializer(serializers.ModelSerializer):

    class Meta:

        model = GroupMessage
        fields = ('id', 'title', 'content', 'status')

   
class PhaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phase
        fields = ('id', 'name', 'able_to_sign', 'start_time', 'end_time', 'sign_start_time', 'sign_end_time', 'max_group',  'min_group', 'status', 'enrolment_method', 'result_submit_method', 'test_upload_method') 


class PhaseDetialSerializer(serializers.ModelSerializer):

    competition = CompetitionSerializer(read_only=True)

    class Meta:
        model = Phase
        fields = ('id', 'name', 'able_to_sign', 'competition', 'start_time', 'end_time', 'sign_start_time', 'sign_end_time', 'max_group',  'min_group', 'status', 'enrolment_method') 


class EnrolmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrolment
        fields = ('id', 'phase', 'contestant', 'enrolment_info') 


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = ('id', 'competition', 'label', 'islook', 'name', 'attachment_url')


class CompetitionAndContestantSerializer(serializers.ModelSerializer):

    current_phase = PhaseSerializer()

    class Meta:
        model = CompetitionAndContestant
        fields = ('id', 'is_focus', 'is_joining', 'is_remind', 'current_phase', 'backup')


class CompetitionDetialSerializer(serializers.ModelSerializer):

    organizer = SpecialOrganizerUserSerializer(read_only=True)
    phase_ongoing = PhaseSerializer(many = True, read_only=True)
    phase_enrolling = PhaseSerializer(many = True, read_only=True)
    organizer = SimpleOrganizerUserSerializer(read_only=True)

    class Meta:
        model = Competition
        fields = ('id', 'name', 'organizer', 'sponsor', 'contractor', 'status', 'level', 'objectrange', 'objectschool', 'category', 'detail', 'pic_url', 'phase_ongoing', 'phase_enrolling')


class FloorCompetitionCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompetitionComment
        fields = ('id', 'floor')


class CompetitionCommentSerializer(serializers.ModelSerializer):

    author = UserShortSerializer(read_only=True)
    link_comment = FloorCompetitionCommentSerializer(read_only=True)

    class Meta:
        model = CompetitionComment
        fields = ('id', 'author', 'competition', 'content', 'post_time', 'floor', 'link_comment')


class SimpleCompetitionCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompetitionComment
        fields = ('id', 'content')
