import os
import time
import datetime
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
from competition.permissions import *

# Create your views here.

class Create(APIView):

    def post(self, request):

        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=self.request.user.organizer_user)
            return Response({'returnCode':0, 'id':serializer.data.get('id')}, status=status.HTTP_201_CREATED) #serializer.data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class List(generics.ListCreateAPIView):

    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user.organizer_user)


class HomeCompetition(APIView):

    def get(self, request):

        query_set = Competition.objects.filter(status__exact=1)
        if len(query_set) >= 6:
            query_set = query_set[0:6]
        serializer = HomeCompetitionSerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Detail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    #permission_classes = (IsOwnerOrReadOnly,)


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DetailWithPhase(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = Competition.objects.all()
    serializer_class = CompetitionDetialSerializer
    #permission_classes = (IsOwnerOrReadOnly,)


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CoverUpload(APIView):

    def post(self, request):
        user = request.user
        if user.is_authenticated() and user.first_name == 'organizer':

            image = request.data.get('file')
            present_time = str(int(time.time()))
            present_time.replace('.', '_')
            pre_name = image.name.split('.')
            image_name = user.username + '_' + pre_name[0] + '_' + present_time + '.' + pre_name[-1]
            cover_file = open(os.path.join('frontend/dist/static/static/cover', image_name), "wb")
            for chunk in image.chunks():
                cover_file.write(chunk)
            cover_file.close()
            pic_url = 'static/static/cover/' + image_name
            return Response({'pic_url': pic_url}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class AttachmentUpload(APIView):

    def post(self, request):
        user = request.user
        if user.is_authenticated() and user.first_name == 'organizer':

            attachment_file = request.data.get('file')
            present_time = str(int(time.time()))
            present_time.replace('.', '_')
            pre_name = attachment_file.name.split('.')
            file_name = user.username + '_' + pre_name[0] + '_' + present_time + '.' + pre_name[-1]
            attach_file = open(os.path.join('frontend/dist/static/static/attachment', file_name), "wb")
            for chunk in attachment_file.chunks():
                attach_file.write(chunk)
            attach_file.close()
            attachment_url = 'static/static/attachment/' + file_name
            return Response({'attachment_url': attachment_url}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class SubmitUpload(APIView):

    def post(self, request):
        user = request.user
        if user.is_authenticated() and user.first_name == 'contestant':
            submit_file = request.data.get('file')
            present_time = str(int(time.time()))
            present_time.replace('.', '_')
            pre_name = submit_file.name.split('.')
            file_name = user.username + '_' + pre_name[0] + '_' + present_time + '.' + pre_name[-1]
            sub_file = open(os.path.join('frontend/dist/static/static/submit', file_name), "wb")
            for chunk in submit_file.chunks():
                sub_file.write(chunk)
            sub_file.close()
            submit_url = 'static/static/submit/' + file_name
            return Response({'submit_url': submit_url}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class GetNotice(APIView):

    def post(self, request):

        competition = Competition.objects.get(id=request.data.get('competition_id'))
        if request.user.organizer_user != competition.organizer:
            return Response({'reason': 1}, status=status.HTTP_400_BAD_REQUEST)
        notice = Notice()
        notice.competition = competition
        notice.title = request.data.get('title')
        notice.content = request.data.get('content')
        notice.status = request.data.get('status')
        notice.save()
        return Response({}, status=status.HTTP_200_OK)

    def get(self, request):
        competition = Competition.objects.get(id=request.query_params.dict().get('competition_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == competition.organizer:
            saving_notices = []
            published_notices = []
            deleted_notices = []
            for notice in competition.notice.filter(status__exact=0):
                saving_notices.append({'id':notice.id, 'title':notice.title, 'content':notice.content})
            for notice in competition.notice.filter(status__exact=1):
                published_notices.append({'id':notice.id, 'title':notice.title, 'content':notice.content})
            for notice in competition.notice.filter(status__exact=2):
                deleted_notices.append({'id':notice.id, 'title':notice.title, 'content':notice.content})
            return Response({'saving_notices':saving_notices, 'published_notices':published_notices,\
             'deleted_notices':deleted_notices}, status=status.HTTP_200_OK)

        else:
            serializer = NoticeSerializer(competition.notice.filter(status__exact=1), many=True)
            for notice in serializer.data:
                notice['post_time'] = notice['post_time'].split('.')[0].replace('T', ' ')
        return Response({'posted_notices':serializer.data}, status=status.HTTP_200_OK)


class NoticeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = (IsNoticeOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class NoticeStatus(APIView):

    def post(self, request):
        notice = Notice.objects.get(id=request.data.get('notice_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == notice.competition.organizer:
            statuses = ['0', '1', '2']
            if request.data.get('new_status') in statuses:
                notice.status = request.data.get('new_status')
                notice.save()
                return Response({}, status=status.HTTP_200_OK)
            elif request.data.get('new_status') == '3':
                notice.delete()
                return Response({}, status=status.HTTP_200_OK)
            return Response({'reason': 2}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'reason': 1}, status=status.HTTP_400_BAD_REQUEST)


class GetEvent(APIView):

    #permission_classes = (IsAuthenticated)

    def post(self, request):

        serializer = PostEventSerializer(data=request.data)
        if serializer.is_valid():
            phase = Phase.objects.get(id=request.data.get('phase_id'))
            if request.data.get('event_type') == '7':
                contestant = ContestantUser.objects.get(id=request.data.get('contestant_id'))
                personal_letter = PersonalLetter()
                personal_letter.receiver = contestant.user
                personal_letter.sender = phase.competition.organizer.user
                personal_letter.is_read = 0
                personal_letter.content = contestant.name + '同学您好，您在比赛 ' + phase.competition.name + ' 中受到警告，警告理由如下： ' + request.data.get('content')
                personal_letter.save()
            else:
                contestant = request.user.contestant_user
            serializer.save(phase=phase, contestant=contestant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):

        params = request.query_params.dict()
        phase = Phase.objects.get(id=params.get('phase_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == phase.competition.organizer:
            event_query_set = phase.event.all()
            event_query_set = event_query_set.exclude(event_type__exact=7)
            event_type = int(params.get('event_type'))
            event_types = [1, 2, 3, 4, 5, 6, 8]
            if event_type in event_types:
                event_query_set = event_query_set.filter(event_type__exact=event_type)
            event_status = int(params.get('status'))
            statuses = [1, 2, 3]
            if event_status in statuses:
                event_query_set = event_query_set.filter(status__exact=event_status)
            if len(event_query_set) <= 0:
                return Response({}, status=status.HTTP_200_OK)
            current_page = int(params.get('current_page'))
            event_num = int(params.get('event_num'))
            min_num = event_num * (current_page - 1)
            max_num = event_num * current_page - 1
            if min_num >= 0 and max_num < len(event_query_set):
                event_query_set = event_query_set[min_num:max_num + 1]
                serializer = EventSerializer(event_query_set, many=True)
            elif min_num >= 0 and max_num > len(event_query_set) and min_num < len(event_query_set):
                event_query_set = event_query_set[min_num:len(event_query_set)]
                serializer = EventSerializer(event_query_set, many=True)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            for event in serializer.data:
                event['time'] = event['time'].split('.')[0].replace('T', ' ')
                event['handle_time'] = event['handle_time'].split('.')[0].replace('T', ' ')
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.first_name == 'contestant':
            contestant = request.user.contestant_user
            event_query_set = contestant.event.filter(phase__exact=phase)
            serializer = EventSerializer(event_query_set, many=True)
            for event in serializer.data:
                event['time'] = event['time'].split('.')[0].replace('T', ' ')
                event['handle_time'] = event['handle_time'].split('.')[0].replace('T', ' ')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class EventNumber(APIView):

    def get(self, request):

        params = request.query_params.dict()
        phase = Phase.objects.get(id=params.get('phase_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == phase.competition.organizer:
            event_query_set = phase.event.filter(event_type__lt=7)
            event_type = params.get('event_type')
            event_types = [1, 2, 3, 4, 5, 6, 8]
            if event_type in event_types:
                event_query_set = event_query_set.filter(event_type__exact=event_type)
            event_status = params.get('status')
            statuses = [1, 2, 3]
            if event_status in statuses:
                event_query_set = event_query_set.filter(status__exact=event_status)
            return Response({'event_number': len(event_query_set)}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class HandleEvent(APIView):

    #permission_classes = (IsAuthenticated)

    def post(self, request):

        event = Event.objects.get(id=request.data.get('id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == event.phase.competition.organizer:
            event.status = request.data.get('status')
            event.reason = request.data.get('reason')
            event.save()
            if event.event_type == 1 or event.event_type == 8:
                is_joining = 0
                if event.status == '2':
                    is_joining = 2
                elif event.status == '3':
                    is_joining = 0
                queryset = CompetitionAndContestant.objects.filter(competition=event.phase.competition, contestant=event.contestant)
                if queryset:
                    queryset[0].is_joining = is_joining
                    queryset[0].current_phase = event.phase
                    queryset[0].save()
                else:
                    competition_and_contestant = CompetitionAndContestant()
                    competition_and_contestant.contestant = event.contestant
                    competition_and_contestant.competition = event.phase.competition
                    competition_and_contestant.current_phase = event.phase
                    competition_and_contestant.is_joining = is_joining
                    competition_and_contestant.save()
                if (is_joining == 0):
                    return Response({'status':event.status, 'reason':event.reason}, status=status.HTTP_200_OK)
                event.phase.joiner.add(event.contestant)
                event.contestant.join_competition.add(event.phase.competition)
                event.contestant.save()
                if event.is_team >= 1:
                    if event.event_type == 1:
                        event_content = json.loads(event.content)
                        team = Team()
                        team.team_leader = event.contestant
                        team.phase = event.phase
                        team.name = event_content[0][0]
                        team.introduction = event_content[1][0]
                        team.save()
                    if event.event_type == 8:
                        team = Team.objects.filter(id=event.is_team)
                        print(event.is_team)
                        if team:
                            team[0].team_member.add(event.contestant)
                            team[0].save()
            if event.status == '2':
                if event.event_type == 2:
                    event.phase.joiner.remove(event.contestant)
                    event.phase.save()
                    event.contestant.join_competition.remove(event.phase.competition)
                    event.contestant.save()
                    queryset = CompetitionAndContestant.objects.filter(competition=event.phase.competition, contestant=event.contestant)
                    if queryset:
                        queryset[0].is_joining = 0
                        queryset[0].save()
                    team = event.contestant.leader_team.filter(phase__exact=event.phase)
                    if team:
                        team[0].delete()
                    team = event.contestant.member_team.filter(phase__exact=event.phase)
                    if team:
                        team[0].team_member.remove(event.contestant)
                elif event.event_type == 4:
                    team = event.contestant.leader_team.filter(phase__exact=event.phase)
                    if team:
                        contestant = ContestantUser.objects.get(id=event.is_team)
                        team[0].team_member.add(team[0].team_leader)
                        team[0].team_leader = contestant
                        team[0].team_member.remove(contestant)
                        team[0].save()
                elif event.event_type == 5:
                    team = event.contestant.member_team.filter(phase__exact=event.phase)
                    if team:
                        team[0].team_member.add(team[0].team_leader)
                        team[0].team_leader = event.contestant
                        team[0].team_member.remove(event.contestant)
                        team[0].save()
                elif event.event_type == 6:
                    enrolment = Enrolment.objects.filter(contestant=event.contestant, phase=event.phase)
                    if enrolment:
                        enrolment[0].enrolment_info = event.content
                        enrolment[0].save()

            return Response({'status':event.status, 'reason':event.reason}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class GetGrade(APIView):

    #permission_classes = (IsAuthenticated)

    def post(self, request):

        phase = Phase.objects.get(id=request.data.get('phase_id'))
        contestant = request.user.contestant_user
        if contestant in phase.joiner.all():
            serializer = PostGradeSerializer(data=request.data)
            if serializer.is_valid():
                grade_contestant = contestant
                if(phase.max_group != 1 or phase.min_group != 1):
                    team = contestant.leader_team.filter(phase__exact=phase)
                    if len(team) <= 0:
                        team = contestant.member_team.filter(phase__exact=phase)
                        if len(team) <= 0:
                            return Response({}, status=status.HTTP_400_BAD_REQUEST)
                        grade_contestant = team[0].team_leader
                serializer.save(phase=phase, contestant=grade_contestant)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        params = request.query_params.dict()
        phase = Phase.objects.get(id=params.get('phase_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == phase.competition.organizer:
            grade_type = params.get('grade_type')
            if grade_type == '1':
                grade_query_set = phase.grade.all()
                if len(grade_query_set) <= 0:
                    return Response([], status=status.HTTP_200_OK)
                current_page = int(params.get('current_page'))
                grade_num = int(params.get('grade_num'))
                min_num = grade_num * (current_page - 1)
                max_num = grade_num * current_page - 1
                if min_num >= 0 and max_num < len(grade_query_set):
                    grade_query_set = grade_query_set[min_num:max_num + 1]
                elif min_num >= 0 and max_num > len(grade_query_set) and min_num < len(grade_query_set):
                    grade_query_set = grade_query_set[min_num:len(grade_query_set)]
                else:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
                serializer = GradeSerializer(grade_query_set, many=True)
                for grade in serializer.data:
                    if(phase.min_group != 1 or phase.max_group != 1):
                        team_leader = ContestantUser.objects.get(id=grade['contestant']['id'])
                        grade['contestant']['name'] = team_leader.leader_team.get(phase=phase).name
                    grade['time'] = grade['time'].split('.')[0].replace('T', ' ')
                    grade['handle_time'] = grade['handle_time'].split('.')[0].replace('T', ' ')
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                if phase.max_group == 1 and phase.min_group == 1:
                    joiner_query_set = phase.joiner.all()
                else:
                    joiner_query_set = phase.team.all()
                if len(joiner_query_set) <= 0:
                    return Response({'joiners': []}, status=status.HTTP_200_OK)
                current_page = int(params.get('current_page'))
                grade_num = int(params.get('grade_num'))
                min_num = grade_num * (current_page - 1)
                max_num = grade_num * current_page - 1
                if min_num >= 0 and max_num < len(joiner_query_set):
                    joiner_query_set = joiner_query_set[min_num:max_num + 1]
                elif min_num >= 0 and max_num > len(joiner_query_set) and min_num < len(joiner_query_set):
                    joiner_query_set = joiner_query_set[min_num:len(joiner_query_set)]
                else:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
                joiners = []
                for joiner in joiner_query_set:
                    if phase.max_group == 1 and phase.min_group == 1:
                        grade_query_set = joiner.grade.filter(phase__exact=phase)
                    else:
                        grade_query_set = joiner.team_leader.grade.filter(phase__exact=phase)
                    serializer = GradeSerializer(grade_query_set, many=True)
                    for grade in serializer.data:
                        grade['time'] = grade['time'].split('.')[0].replace('T', ' ')
                        grade['handle_time'] = grade['handle_time'].split('.')[0].replace('T', ' ')
                    joiners.append({'id': joiner.id, 'name': joiner.name, 'grades': serializer.data})
                return Response({'joiners': joiners}, status=status.HTTP_200_OK)


class GradeNumber(APIView):

    def get(self, request):

        params = request.query_params.dict()
        phase = Phase.objects.get(id=params.get('phase_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == phase.competition.organizer:
            grade_type = params.get('grade_type')
            if grade_type == '1':
                grade_query_set = phase.grade.all()
                return Response({'grade_number': len(grade_query_set)}, status=status.HTTP_200_OK)
            else:
                joiner_query_set = phase.joiner.all()
                return Response({'joiner_number': len(joiner_query_set)}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class HandleGrade(APIView):

    #permission_classes = (IsAuthenticated)

    def post(self, request):

        grade = Grade.objects.get(id=request.data.get('grade_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == grade.phase.competition.organizer:
            #grade.handle_content = request.data.get('handle_content')
            grade.is_handled = 1
            grade.submit_grade = request.data.get('submit_grade')
            grade.save()
            return Response({'submit_grade':grade.submit_grade}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class LeaderBoard(APIView):

    def get(self, request):

        params = request.query_params.dict()
        phase = Phase.objects.get(id=params.get('phase_id'))
        grade_query_set = phase.grade.all().order_by('-submit_grade')
        serializer = GradeSerializer(grade_query_set, many=True)
        for grade in serializer.data:
            if phase.min_group != 1 or phase.max_group != 1:
                team_leader = ContestantUser.objects.get(id=grade['contestant']['id'])
                grade['contestant']['name'] = team_leader.leader_team.get(phase=phase).name
            grade['time'] = grade['time'].split('.')[0].replace('T', ' ')
            grade['handle_time'] = grade['handle_time'].split('.')[0].replace('T', ' ')
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmitHistory(APIView):

    def get(self, request):

        params = request.query_params.dict()
        phase = Phase.objects.get(id=params.get('phase_id'))
        if request.user.first_name == 'contestant':
            contestant = request.user.contestant_user
            grade_query_set = contestant.grade.filter(phase__exact=phase)
            serializer = GetGradeSerializer(grade_query_set, many=True)
            for grade in serializer.data:
                if phase.min_group != 1 or phase.max_group != 1:
                    team_leader = ContestantUser.objects.get(id=grade['contestant']['id'])
                    grade['contestant']['name'] = team_leader.leader_team.get(phase=phase).name
                grade['time'] = grade['time'].split('.')[0].replace('T', ' ')
                grade['handle_time'] = grade['handle_time'].split('.')[0].replace('T', ' ')
            return Response(serializer.data, status=status.HTTP_200_OK)


class SendGroupMessage(APIView):

    def post(self, request):

        serializer = GroupMessageSerializer(data=request.data)
        if serializer.is_valid():
            competition = Competition.objects.get(id=request.data.get('competition_id'))
            group_message = serializer.save(competition=competition)
            contestant_ids = json.loads(request.data.get('contestant_id'))
            for contestant_id in contestant_ids:
                contestant = ContestantUser.objects.get(id=contestant_id)
                group_message.receiver.add(contestant)
            group_message.save()
            if group_message.status == 1:
                for contestant in group_message.receiver.all():
                    personal_letter = PersonalLetter()
                    personal_letter.receiver = contestant.user
                    personal_letter.sender = competition.organizer.user
                    personal_letter.is_read = 0
                    personal_letter.content = group_message.title + ' 这是比赛 ' + competition.name + ' 的通知\n    ' + group_message.content
                    personal_letter.save()
            return Response({}, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        competition = Competition.objects.get(id=request.query_params.dict().get('competition_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == competition.organizer:
            saving_group_messages = []
            published_group_messages = []
            for group_message in competition.group_message.filter(status__exact=0):
                saving_group_messages.append({'id':group_message.id, 'title':group_message.title, 'content':group_message.content})
            for group_message in competition.group_message.filter(status__exact=1):
                published_group_messages.append({'id':group_message.id, 'title':group_message.title, 'content':group_message.content})
            return Response({'saving_group_messages':saving_group_messages, 'published_group_messages':published_group_messages},\
             status=status.HTTP_200_OK)
        return Response({'reason': 1}, status=status.HTTP_400_BAD_REQUEST)


class ReceiveGroupMessage(APIView):

    permission_classes = (IsAuthenticated)

    def get(self, request):

        if request.user.first_name == 'organizer':
            group_messages = request.user.contestant_user.group_message.filter(status__exact=1)
            response = []
            for group_message in group_messages:
                competition = group_message.competition
                competition_dic = {'id': competition.id, 'name': competition.name}
                organizer = competition.organizer
                organizer_dic = {'id': organizer.id, 'name': organizer.name}
                group_message_dic = {'id': group_message.id, 'title':group_message.title, 'content':group_message.content}
                response.append({'organizer':organizer_dic, 'competition':competition_dic, 'group_message':group_message_dic})
            return Response(response, status=status.HTTP_200_OK)
        return Response({'reason': 1}, status=status.HTTP_400_BAD_REQUEST)


class GroupMessageDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    #permission_classes = (IsNoticeOwnerOrReadOnly,)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class ListPhase(APIView):

    def get(self, request):
        queryset = Competition.objects.get(id=self.request.query_params.dict().get("id")).phase.all()
        serializer = PhaseSerializer(queryset, many=True)
        res = serializer.data
        for i in res:
            i['start_time'] = i['start_time'].split('+')[0].replace('T', ' ')
            i['sign_start_time'] = i['sign_start_time'].split('+')[0].replace('T', ' ')
            i['end_time'] = i['end_time'].split('+')[0].replace('T', ' ')
            i['sign_end_time'] = i['sign_end_time'].split('+')[0].replace('T', ' ')
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListPhaseSimple(APIView):

    def get(self, request):
        queryset = Competition.objects.get(id=self.request.query_params.dict().get("id")).phase.all()
        serializer = SimplePhaseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePhase(generics.ListCreateAPIView):

    queryset = Competition.objects.all()
    serializer_class = PhaseDetialSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        comp = Competition.objects.get(id=self.request.data.get('id'))
        serializer.save(competition=comp, start_time=datetime.datetime.fromtimestamp(int(self.request.data.get('starttime')) / 1000),\
        end_time=datetime.datetime.fromtimestamp(int(self.request.data.get('endtime')) / 1000),\
        sign_start_time=datetime.datetime.fromtimestamp(int(self.request.data.get('signstarttime')) / 1000),\
        sign_end_time=datetime.datetime.fromtimestamp(int(self.request.data.get('signendtime')) / 1000))


class DetailPhase(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer
    #permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.data.get('starttime') is not None:
            obj.start_time = datetime.datetime.fromtimestamp(int(self.request.data.get('starttime')) / 1000)
            obj.end_time = datetime.datetime.fromtimestamp(int(self.request.data.get('endtime')) / 1000)
            obj.sign_start_time = datetime.datetime.fromtimestamp(int(self.request.data.get('signstarttime')) / 1000)
            obj.sign_end_time = datetime.datetime.fromtimestamp(int(self.request.data.get('signendtime')) / 1000)
            obj.save()
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CreateEnrolment(generics.ListCreateAPIView):

    queryset = Enrolment.objects.all()
    serializer_class = EnrolmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        cont = self.request.user.contestant_user
        pha = Phase.objects.get(id=self.request.data.get('id'))
        serializer.save(phase=pha, contestant=cont)


class GroupMessageStatus(APIView):

    #permission_classes = (IsAuthenticated)

    def post(self, request):

        group_message = GroupMessage.objects.get(id=request.data.get('group_message_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == group_message.competition.organizer:
            new_status = request.data.get('new_status')
            if new_status == '1':
                group_message.status = 1
                group_message.save()
                for contestant in group_message.receiver.all():
                    personal_letter = PersonalLetter()
                    personal_letter.receiver = contestant.user
                    personal_letter.sender = competition.organizer.user
                    personal_letter.is_read = 0
                    personal_letter.content = group_message.title + '  ' + competition.name + '\n    ' + group_message.content
                    personal_letter.save()
                return Response({}, status=status.HTTP_200_OK)
            elif new_status == '2':
                group_message.delete()
                return Response({}, status=status.HTTP_200_OK)
            return Response({'reason': 2}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'reason': 1}, status=status.HTTP_400_BAD_REQUEST)


class GetTeam(APIView):

    def post(self, request):

        if request.user.is_authenticated():
            contestant = request.user.contestant
            phase = Phase.objects.get(id=request.data.get('phase_id'))
            for team in contestant.leader_team:
                if team.phase == phase:
                    return Response({'reason': 1}, status=status.HTTP_400_BAD_REQUEST)
            for team in contestant.member_team:
                if team.phase == phase:
                    return Response({'reason': 1}, status=status.HTTP_400_BAD_REQUEST)
            team = Team()
            team.name = request.data.get('name')
            team.introduction = request.data.get('introduction')
            team.team_leader = contestant
            team.phase = phase
            team.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response({'reason': 0}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):

        if request.user.is_authenticated():
            params = request.query_params.dict()
            phase = Phase.objects.get(id=params.get('phase_id'))
            if request.user.first_name == 'organizer':
                organizer = request.user.organizer_user
                if organizer == phase.competition.organizer:
                    team_list = []
                    for team in phase.team.all():
                        team_list.append({'team_name': team.name})
                    return Response({'team_list': team_list}, status=status.HTTP_200_OK)
                return Response({'reason': 1}, status=status.HTTP_400_BAD_REQUEST)
            elif request.user.first_name == 'contestant':
                team_datas = []
                for team in phase.team.all():
                    leader = team.team_leader
                    team_leader = {'uid': leader.user.id, 'id': leader.id, 'name': leader.name}
                    team_number = 1 + len(team.team_member.all())
                    team_datas.append({'team_id': team.id, 'team_name': team.name, 'team_leader': team_leader, 'team_number': team_number,\
                     'create_time': team.create_time.strftime("%Y-%m-%d %H:%M:%S")})
                return Response({'team_datas': team_datas}, status=status.HTTP_200_OK)
        return Response({'reason': 0}, status=status.HTTP_401_UNAUTHORIZED)


class TeamDetail(APIView):

    def get(self, request):

        if request.user.is_authenticated():
            if request.user.first_name == 'contestant':
                contestant = request.user.contestant_user
                params = request.query_params.dict()
                phase = Phase.objects.get(id=params.get('phase_id'))
                teams = contestant.leader_team.filter(phase__exact=phase)
                if teams:
                    team = teams[0]
                    team_player = {'uid': contestant.user.id, 'id': contestant.id, 'name': contestant.name, 'identity': '队长'}
                    team_datas = []
                    team_datas.append(team_player)
                    for team_member in team.team_member.all():
                        team_datas.append({'uid': team_member.user.id, 'id': team_member.id, 'name':team_member.name, 'identity': '队员'})
                    return Response({'team_id': team.id, 'team_player': team_player, 'team_datas': team_datas}, status=status.HTTP_200_OK)
                teams = contestant.member_team.filter(phase__exact=phase)
                if teams:
                    team = teams[0]
                    team_player = {'name': contestant.name, 'identity': '队员'}
                    team_datas = []
                    team_datas.append({'uid': team.team_leader.user.id, 'id': team.team_leader.id, 'name':team.team_leader.name, 'identity': '队长'})
                    for team_member in team.team_member.all():
                        team_datas.append({'uid': team_member.user.id, 'id': team_member.id, 'name':team_member.name, 'identity': '队员'})
                    return Response({'team_id': team.id, 'team_player': team_player, 'team_datas': team_datas}, status=status.HTTP_200_OK)
                return Response({'reason': 1}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'reason': 0}, status=status.HTTP_401_UNAUTHORIZED)


class InvitationCode(APIView):

    def get(self, request):

        if request.user.is_authenticated() and request.user.first_name == 'contestant':
            contestant = request.user.contestant_user
            params = request.query_params.dict()
            team = Team.objects.get(id=params.get('team_id'))
            if team.team_leader != contestant:
                return Response({'reason': 1}, status=status.HTTP_400_BAD_REQUEST)
            if team.invitation_code == '':
                invitation_codes = []
            else:
                invitation_codes = json.loads(team.invitation_code)
            member_number = len(team.team_member.all()) + 1 + len(invitation_codes)
            if member_number > 3:
                return Response({'reason': 2}, status=status.HTTP_400_BAD_REQUEST)
            invitation_code = make_password(team.name, None, 'pbkdf2_sha256')
            invitation_codes.append(invitation_code)
            team.invitation_code = json.dumps(invitation_codes)
            team.save()
            return Response({'invitation_code':invitation_code}, status=status.HTTP_200_OK)
        return Response({'reason': 0}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):

        if request.user.is_authenticated() and request.user.first_name == 'contestant':
            contestant = request.user.contestant_user
            team = Team.objects.get(id=request.data.get('team_id'))
            invitation_code = request.data.get('invitation_code')
            if team.invitation_code == '':
                invitation_codes = []
            else:
                invitation_codes = json.loads(team.invitation_code)
            if invitation_code in invitation_codes:
                invitation_codes.remove(invitation_code)
                team.invitation_code = json.dumps(invitation_codes)
                team.save()
                return Response({'is_join': 1}, status=status.HTTP_200_OK)
            return Response({'is_join': 0}, status=status.HTTP_200_OK)
        return Response({'reason': 0}, status=status.HTTP_401_UNAUTHORIZED)

class CreateAttachment(generics.ListCreateAPIView):

    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        comp = Competition.objects.get(id=self.request.data.get('cmp_id'))
        serializer.save(competition=comp)


class ListAttachment(APIView):

    def get(self, request):
        queryset = Competition.objects.get(id=self.request.query_params.dict().get("id")).attachment
        serializer = AttachmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteAttachment(APIView):

    def post(self, request):
        atta = Attachment.objects.get(id=self.request.data.get("id"))
        if request.user.is_authenticated() and request.user == atta.competition.organizer.user:
            os.remove('frontend/dist/' + atta.attachment_url)
            atta.delete()
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class JoinerNumber(APIView):

    def get(self, request):

        params = request.query_params.dict()
        phase = Phase.objects.get(id=params.get('phase_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == phase.competition.organizer:
            if phase.max_group == phase.min_group and phase.max_group == 1:
                joiner_number = len(phase.joiner.all())
            else:
                joiner_number = len(phase.team.all())
            return Response({'joiner_number': joiner_number}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class Joiner(APIView):

    def get(self, request):

        params = request.query_params.dict()
        phase = Phase.objects.get(id=params.get('phase_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == phase.competition.organizer:
            current_page = int(params.get('current_page'))
            joiner_num = int(params.get('joiner_num'))
            min_num = joiner_num * (current_page - 1)
            max_num = joiner_num * current_page - 1
            if(phase.max_group == phase.min_group and phase.max_group == 1):
                joiner_query_set = phase.joiner.all()
                if len(joiner_query_set) <= 0:
                    return Response({'joiners': []}, status=status.HTTP_200_OK)
                if min_num >= 0 and max_num < len(joiner_query_set):
                    max_num = max_num + 1
                elif min_num >= 0 and max_num >= len(joiner_query_set) and min_num < len(joiner_query_set):
                    max_num = len(joiner_query_set)
                else:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
                joiner_query_set = joiner_query_set[min_num:max_num]
                joiners = []
                for joiner in joiner_query_set:
                    joiners.append({'joiner': {'id': joiner.id, 'name': joiner.name}, 'grade': '123'})
            else:
                joiner_query_set = phase.team.all()
                if len(joiner_query_set) <= 0:
                    return Response({'joiners': []}, status=status.HTTP_200_OK)
                if min_num >= 0 and max_num < len(joiner_query_set):
                    max_num = max_num + 1
                elif min_num >= 0 and max_num >= len(joiner_query_set) and min_num < len(joiner_query_set):
                    max_num = len(joiner_query_set)
                else:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
                joiner_query_set = joiner_query_set[min_num:max_num]
                joiners = []
                for joiner in joiner_query_set:
                    team = {'id': joiner.id, 'name': joiner.name}
                    leader = {'id': joiner.team_leader.id, 'name': joiner.team_leader.name, 'identity': '队长'}
                    members = []
                    members.append(leader)
                    for member in joiner.team_member.all():
                        members.append({'id': member.id, 'name': member.name, 'identity': '队员'})
                    team_number = len(joiner.team_member.all()) + 1
                    joiners.append({'stage_id': params.get('phase_id'), 'team': team, 'team_number': team_number,\
                     'create_date': joiner.create_time, 'leader': leader, 'team_member': members})
            return Response({'joiners': joiners}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class JoinerType(APIView):

    def get(self, request):

        params = request.query_params.dict()
        phase = Phase.objects.get(id=params.get('phase_id'))
        if phase:
            joiner_type = 1
            if phase.max_group == 1 and phase.min_group == 1:
                joiner_type = 0
                joiner_number = len(phase.joiner.all())
            else:
                joiner_number = len(phase.team.all())
            return Response({'joiner_type': joiner_type, 'joiner_number': joiner_number}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class AddJoiner(APIView):

    def post(self, request):
        phase = Phase.objects.get(id=request.data.get('phase_id'))
        if request.user.first_name == 'organizer' and request.user.organizer_user == phase.competition.organizer:
            contestant_ids = json.loads(request.data.get('contestant_id'))
            for contestant_id in contestant_ids:
                contestant = ContestantUser.objects.get(id=contestant_id)
                phase.joiner.add(contestant)
                phase.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class AndContestant(APIView):

    def get(self, request):
        comp = Competition.objects.get(id=self.request.query_params.dict().get("id"))
        user = request.user
        try:
            queryset = CompetitionAndContestant.objects.get(competition=comp, contestant=user.contestant_user)
            serializer = CompetitionAndContestantSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response({'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        comp = Competition.objects.get(id=self.request.data.get('id'))
        user = request.user
        if user.is_authenticated():
            queryset = CompetitionAndContestant.objects.filter(competition=comp, contestant=user.contestant_user)
            if queryset:
                queryset[0].is_focus = self.request.data.get('is_focus')
                queryset[0].is_joining = self.request.data.get('is_joining')
                queryset[0].is_remind = self.request.data.get('is_remind')
                queryset[0].save()
            else:
                serializer = CompetitionAndContestantSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'returnCode': 0}, status=status.HTTP_401_UNAUTHORIZED)


class Enroll(APIView):

    def post(self, request):

        user = self.request.user
        if user.first_name != 'contestant':
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        contestant = self.request.user.contestant_user
        serializer = EnrolmentSerializer(data=request.data)
        phase = Phase.objects.get(id=request.data.get('phase_id'))
        if serializer.is_valid():
            serializer.save(contestant=contestant, phase=phase)
            event = Event()
            event.phase = phase
            event.contestant = contestant
            if event.phase.max_group == 1:
                event.is_team = 0
            else:
                event.is_team = 1
            event.event_type = 1
            if request.data.get('join_status') == '1':
                event.event_type = 8
                event.is_team = request.data.get('team_id')
            event.content = request.data.get('enrolment_info')
            event.save()
            queryset = CompetitionAndContestant.objects.filter(competition=event.phase.competition, contestant=contestant)
            if queryset:
                queryset[0].is_joining = 1
                queryset[0].current_phase = event.phase
                queryset[0].save()
            else:
                competition_and_contestant = CompetitionAndContestant()
                competition_and_contestant.contestant = event.contestant
                competition_and_contestant.competition = event.phase.competition
                competition_and_contestant.current_phase = event.phase
                competition_and_contestant.is_joining = 1
                competition_and_contestant.save()
            return Response({'returnCode':0, 'id':serializer.data.get('id')}, status=status.HTTP_201_CREATED) #serializer.data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StateUpdate(APIView):

    def get(self, request):

        comp = Competition.objects.get(id=self.request.query_params.dict().get("id"))
        now_time = datetime.timedelta(hours=-8) + datetime.datetime.now()
        for i in comp.phase.all():
            if i.start_time.replace(tzinfo=None) < now_time and i.end_time.replace(tzinfo=None) > now_time:
                i.competition_ongoing = i.competition
            else:
                i.competition_ongoing = None
            if i.sign_start_time.replace(tzinfo=None) < now_time and i.sign_end_time.replace(tzinfo=None) > now_time and i.able_to_sign:
                i.competition_enrolling = i.competition
            else:
                i.competition_enrolling = None
            i.save()
        if not comp.phase_ongoing.all():
            comp.category = 0
            recent_end_phase = Phase()
            recent_end_time = datetime.datetime.fromtimestamp(0)
            for i in comp.phase.all():
                if i.end_time.replace(tzinfo=None) < now_time and i.end_time.replace(tzinfo=None) > recent_end_time:
                    recent_end_time = i.end_time
                    recent_end_phase = i
            if recent_end_time.replace(tzinfo=None) > datetime.datetime.fromtimestamp(0):
                recent_end_phase.competition_ongoing = recent_end_phase.competition
        else:
            comp.category = 1
        comp.save()
        ser = CompetitionDetialSerializer(comp)
        data = ser.data
        data['organizer']['uid'] = comp.organizer.user.id
        if comp.phase_ongoing.all():
            data['team_number'] = comp.phase_ongoing.all()[0].joiner.all().count()
            data['focus_number'] = comp.followers.all().count()
        else:
            data['team_number'] = 0
            data['focus_number'] = 0
        for i in data['phase_enrolling']:
            i['start_time'] = i['start_time'].split('+')[0].replace('T', ' ')
            i['sign_start_time'] = i['sign_start_time'].split('+')[0].replace('T', ' ')
            i['end_time'] = i['end_time'].split('+')[0].replace('T', ' ')
            i['sign_end_time'] = i['sign_end_time'].split('+')[0].replace('T', ' ')
        for i in data['phase_ongoing']:
            i['start_time'] = i['start_time'].split('+')[0].replace('T', ' ')
            i['sign_start_time'] = i['sign_start_time'].split('+')[0].replace('T', ' ')
            i['end_time'] = i['end_time'].split('+')[0].replace('T', ' ')
            i['sign_end_time'] = i['sign_end_time'].split('+')[0].replace('T', ' ')
        return Response(data, status=status.HTTP_200_OK)


class EnrolmentInfo(APIView):

    def get(self, request):

        if request.user.is_authenticated():
            contestant = request.user.contestant_user
            phase = Phase.objects.filter(id=request.query_params.dict().get("id"))
            if phase:
                enrolment = Enrolment.objects.filter(phase=phase[0], contestant=contestant)
                if enrolment:
                    serializer = EnrolmentSerializer(enrolment[0])
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        return Response({'returnCode':0}, status=status.HTTP_401_UNAUTHORIZED)


class ListContestant(APIView):

    def get(self, request):

        comp_id = request.query_params.dict().get("comp_id")
        phase_id = request.query_params.dict().get("phase_id")
        if phase_id == '-1':
            competition = Competition.objects.get(id=comp_id)
            queryset = competition.joiners.all()
        else:
            phase = Phase.objects.get(id=phase_id)
            queryset = phase.joiner.all()
        serializer = SimpleContestantUserSerializer(queryset, many=True)
        for i_serializer in serializer.data:
            i = ContestantUser.objects.get(id=i_serializer['id'])
            grade_max = None
            grade_latest = None
            if phase_id != '-1':
                for j in i.grade.all().filter(phase=phase).exclude(is_handled=0):
                    if grade_max == None or grade_max.submit_grade < j.submit_grade:
                        grade_max = j
                    if grade_latest == None or grade_latest.time < grade_latest.time:
                        grade_latest = j
            i_serializer['grade_max'] = SimpleGradeSerializer(grade_max).data
            i_serializer['grade_latest'] = SimpleGradeSerializer(grade_latest).data
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateComment(APIView):

    def post(self, request):

        serializer = SimpleCompetitionCommentSerializer(data=request.data)
        if serializer.is_valid():
            competition = Competition.objects.get(id=request.data.get('competition_id'))
            floor = len(competition.comment.all()) + 1
            comment_id = request.data.get('comment_id')
            if comment_id:
                link_comment = CompetitionComment.objects.get(id=comment_id)
                serializer.save(author=self.request.user, competition=competition, floor=floor, link_comment=link_comment)
            else:
                serializer.save(author=self.request.user, competition=competition, floor=floor)
            return Response({'id':serializer.data.get('id')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        params = request.query_params.dict()
        competition = Competition.objects.get(id=params.get('competition_id'))
        query_set = competition.comment.all()
        current_page = int(params.get('current_page'))
        comment_num = int(params.get('comment_num'))
        min_num = comment_num * (current_page - 1)
        max_num = comment_num * current_page - 1
        if len(query_set) <= 0:
            return Response({}, status=status.HTTP_200_OK)
        if min_num >= 0 and max_num < len(query_set):
            max_num = max_num + 1
        elif min_num >= 0 and max_num >= len(query_set) and min_num < len(query_set):
            max_num = len(query_set)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        query_set = query_set[min_num:max_num]
        serializer = CompetitionCommentSerializer(query_set, many=True)
        for comment in serializer.data:
            comment['post_time'] = comment['post_time'].split('.')[0].replace('T', ' ')
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentNumber(APIView):

    def get(self, request):
        params = request.query_params.dict()
        competition = Competition.objects.get(id=params.get('competition_id'))
        query_set = competition.comment.all()
        return Response({'comment_number': len(query_set)}, status=status.HTTP_200_OK)


class CommentDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = CompetitionComment.objects.all()
    serializer_class = SimpleCompetitionCommentSerializer
    #permission_classes = (IsOwnerOrReadOnly,)


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
