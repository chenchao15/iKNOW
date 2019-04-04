from rest_framework import serializers
from django.contrib.auth.models import User
from backend.models import *
from userpage.serializers import *


class TutorialCommentSerializer(serializers.ModelSerializer):

    author = UserShortSerializer(read_only=True)

    class Meta:
        model = TutorialComment
        fields = ('id', 'author', 'tutorial', 'content', 'post_time')


class TutorialSerializer(serializers.ModelSerializer):

    author = UserShortSerializer(read_only=True)

    class Meta:
        model = Tutorial
        fields = ('id', 'status', 'author', 'title', 'brief', 'post_time')


class TutorialPostSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Tutorial
        fields = ('id', 'status', 'author', 'title', 'brief', 'content', 'post_time')


class TutorialDetailSerializer(serializers.ModelSerializer):

    author = UserShortSerializer(read_only=True)
    #tutorial_comment = TutorialCommentSerializer()

    class Meta:
        model = Tutorial
        fields = ('id', 'status', 'author', 'title', 'brief', 'content', 'post_time') #, 'tutorial_comment'

