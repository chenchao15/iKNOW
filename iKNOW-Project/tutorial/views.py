import os
import time
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from backend.models import *
from tutorial.serializers import *
from tutorial.permissions import IsOwnerOrReadOnly

# Create your views here.

class OfficalTutorial(generics.ListCreateAPIView):

    queryset = Tutorial.objects.exclude(author__organizer_user__isnull=True).filter(status=1)
    serializer_class = TutorialSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        list_type = request.query_params.dict().get("type")
        if list_type == '1':
            queryset = queryset.order_by('-post_time')
        elif list_type == '2':
            queryset = queryset.order_by('collectors')
        serializer = TutorialSerializer(queryset, many=True)
        data = serializer.data
        for i in data:
            i['post_time'] = i['post_time'].split('.')[0].replace('T', ' ')
        return Response(serializer.data)


class StudentShare(generics.ListCreateAPIView):

    queryset = Tutorial.objects.exclude(author__contestant_user__isnull=True).filter(status=1)
    serializer_class = TutorialSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        list_type = request.query_params.dict().get("type")
        if list_type == '1':
            queryset = queryset.order_by('-post_time')
        elif list_type == '2':
            queryset = queryset.order_by('collectors')
        serializer = TutorialSerializer(queryset, many=True)
        data = serializer.data
        for i in data:
            i['post_time'] = i['post_time'].split('.')[0].replace('T', ' ')
        return Response(serializer.data)


class PostTutorial(generics.ListCreateAPIView):

    queryset = Tutorial.objects.all()
    serializer_class = TutorialPostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MyTutorial(APIView):

    def get(self, request):
        user = request.user
        if not user.is_authenticated():
            return Response({'return_code':0}, status=status.HTTP_401_UNAUTHORIZED)
        params = request.query_params.dict()
        tutorial_status = params.get('status')
        if user.first_name == "contestant":
            contestant_user = user.contestant_user
            if tutorial_status == '2':
                serializer = TutorialSerializer(contestant_user.collect_tutorial.all(), many=True)
            else:
                serializer = TutorialSerializer(user.tutorial.filter(status__exact=tutorial_status), many=True)
            for tutorial in serializer.data:
                tutorial['post_time'] = tutorial['post_time'].split('.')[0].replace('T', ' ')
            tutorial = {'tutorials': serializer.data}
            return Response(tutorial, status=status.HTTP_200_OK)
        elif user.first_name == "organizer":
            serializer = TutorialSerializer(user.tutorial.filter(status__exact=tutorial_status), many=True)
            for tutorial in serializer.data:
                tutorial['post_time'] = tutorial['post_time'].split('.')[0].replace('T', ' ')
            tutorial = {'tutorials': serializer.data}
            return Response(tutorial, status=status.HTTP_200_OK)
        return Response({'return_code':0}, status=status.HTTP_400_BAD_REQUEST)


class TutorialStatus(APIView):

    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return Response({'return_code':0}, status=status.HTTP_401_UNAUTHORIZED)
        tutorial_status = request.data.get('status')
        tutorial = Tutorial.objects.get(id=request.data.get('tutorial_id'))
        if tutorial is not None and user == tutorial.author:
            if tutorial_status == 3:
                tutorial.delete()
            else:
                tutorial.status = tutorial_status
                tutorial.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class TutorialInfo(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        data = serializer.data
        data['collect_number'] = obj.collectors.all().count()
        data['is_collect'] = 0
        data['post_time'] = data['post_time'].split('.')[0].replace('T', ' ')
        if request.user.is_authenticated() and obj.collectors.all().filter(user=request.user):
            data['is_collect'] = 1
        return Response(data)


class ImageUpload(APIView):

    def post(self, request):
        user = request.user
        if user.is_authenticated():
            image_file = request.data.get('file')
            present_time = str(int(time.time()))
            present_time.replace('.', '_')
            pre_name = image_file.name.split('.')
            file_name = user.username + '_' + pre_name[0] + '_' + present_time + '.' + pre_name[-1]
            img_file = open(os.path.join('frontend/dist/static/static/tutorial', file_name), "wb")
            for chunk in image_file.chunks():
                img_file.write(chunk)
            img_file.close()
            image_url = 'static/static/tutorial/' + file_name
            return Response({'image_url': image_url}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)