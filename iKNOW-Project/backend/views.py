import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from backend.models import *
from competition.serializers import *
from userpage.serializers import *
from tutorial.serializers import *
from competition.permissions import *


# Create your views here.

class Search(APIView):

    def post(self, request):

        search_type = request.data.get('type')
        val = request.data.get('val')
        if search_type == '0':
            queryset = Competition.objects.all()
            queryset = queryset.filter(name__contains=val, status=1)
            serializer = CompetitionSerializer(queryset, many=True)
        elif search_type == '1':
            queryset = OrganizerUser.objects.all()
            queryset = queryset.filter(name__contains=val)
            serializer = SpecialDetailOrganizerUserSerializer(queryset, many=True)
        elif search_type == '2':
            queryset = Tutorial.objects.all()
            queryset = queryset.filter(title__contains=val)
            serializer = TutorialSerializer(queryset, many=True)
        #elif request.data.get('type') == '3':
        	#queryset = .objects.all()
        return Response(serializer.data, status=status.HTTP_200_OK)
