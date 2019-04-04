from rest_framework import serializers
from django.contrib.auth.models import User
from backend.models import *

class PersonalLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalLetter
        fields = ('id', 'content', 'post_time', 'is_read')


class ContestantUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContestantUser
        fields = ('id', 'name', 'nickname', 'gender', 'introduction', 'school', 'major', 'student_number', 'phone_number', 'avatar_url')


class SimpleContestantUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContestantUser
        fields = ('id', 'name')


class OrganizerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizerUser
        fields = ('id', 'name', 'shortname', 'introduction', 'address', 'field', 'contact', 'contact_number', 'contact_email', 'avatar_url')


class SimpleOrganizerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizerUser
        fields = ('id', 'name', 'avatar_url')

class SimpleOrganizerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizerUser
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):

    contestant_user = ContestantUserSerializer(read_only=True)
    organizer_user = OrganizerUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'contestant_user', 'organizer_user')

    def create(self, validated_data):
        name = validated_data['username']
        ipass = validated_data['password']
        email = validated_data['email']
        user = User.objects.create_user(username=name, password=ipass, email=email)
        return user


class UserShortSerializer(serializers.ModelSerializer):

    contestant_user = SimpleContestantUserSerializer(read_only=True)
    organizer_user = SimpleOrganizerUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'contestant_user', 'organizer_user')


class AuditSerializer(serializers.ModelSerializer):

    organizer = SimpleOrganizerUserSerializer(read_only=True)
    class Meta:

        model = AuditEvent
        fields = ('id', 'organizer', 'time', 'content', 'status', 'reason')


class SpecialContestantUserSerializer(serializers.ModelSerializer):

    user = UserShortSerializer(read_only=True)

    class Meta:
        model = ContestantUser
        fields = ('user', 'avatar_url')


class SpecialOrganizerUserSerializer(serializers.ModelSerializer):

    user = UserShortSerializer(read_only=True)

    class Meta:
        model = OrganizerUser
        fields = ('user', 'avatar_url')


class SpecialDetailOrganizerUserSerializer(serializers.ModelSerializer):

    user = UserShortSerializer(read_only=True)

    class Meta:
        model = OrganizerUser
        fields = ('user', 'shortname', 'introduction', 'address', 'field', 'contact', 'contact_number', 'contact_email', 'avatar_url')
