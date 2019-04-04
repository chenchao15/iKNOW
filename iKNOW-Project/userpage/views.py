import os
import time
import smtplib
from django.http import Http404
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from backend.models import *
from userpage.serializers import *
from competition.serializers import *
from tutorial.serializers import *
from userpage.permissions import *
from iKNOW.settings import MY_STATIC_URL

# Create your views here.

class SignUp(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid() and request.data.get("usertype") != None:
            serializer.save()
            user = User.objects.get(username=request.data.get("username"))
            if request.data.get("usertype") == '0':
                user.first_name = "contestant"
                contestant = ContestantUser()
                contestant.user = user
                contestant.save()
            elif request.data.get("usertype") == '1':
                user.first_name = "organizer"
                organizer = OrganizerUser()
                organizer.user = user
                organizer.save()
            else:
                user.delete()
                return Response({'signup': 1}, status=status.HTTP_400_BAD_REQUEST)
            user.last_name = '0'
            user.save()
            encode_username = make_password(user.username, 'a', 'pbkdf2_sha256')
            email_token = EmailToken()
            email_token.username = user.username
            email_token.username_token = encode_username
            email_token.save()
            try:
                send_content = user.username + ' 您好\n欢迎注册iKNOW，请点击下方链接来验证您的Email\n' + MY_STATIC_URL + '/#/validate_email/' + encode_username
                send_mail(u'请验证您的Email', send_content, 'iknow_cpcs@163.com', [user.email], fail_silently=False)
            except smtplib.SMTPException:
                user.delete()
                email_token.delete()
                return Response({'signup': 2}, status=status.HTTP_400_BAD_REQUEST)
            response = serializer.data
            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'signup': 1}, status=status.HTTP_400_BAD_REQUEST)


class Username(APIView):

    def get(self, request):
        users = User.objects.filter(username=request.query_params.dict().get("username"))
        if users:
            return Response({'used':1}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'used':0}, status=status.HTTP_200_OK)


class Email(APIView):

    def get(self, request):
        users = User.objects.filter(email=request.query_params.dict().get("email"))
        if users:
            return Response({'email_used':1}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'email_used':0}, status=status.HTTP_200_OK)


class Login(APIView):

    def get(self, request):
        user = request.user
        if user.is_authenticated():
            if user.first_name == "contestant":
                usertype = 0
                the_user = user.contestant_user
            elif user.first_name == "organizer":
                usertype = 1
                the_user = user.organizer_user
            else:
                return Response({'login': 0}, status=status.HTTP_401_UNAUTHORIZED)
            userid = the_user.id
            avatar_url = the_user.avatar_url
            return Response({'login':1, 'usertype':usertype, 'userid':userid, 'avatar_url': avatar_url}, status=status.HTTP_200_OK)
        else:
            return Response({'login':0}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            #if user.last_name == '0':
            #   return Response({'login':2}, status=status.HTTP_401_UNAUTHORIZED)
            auth.login(request, user)
            if user.first_name == "contestant":
                usertype = 0
                the_user = user.contestant_user
            elif user.first_name == "organizer":
                usertype = 1
                the_user = user.organizer_user
            else:
                auth.logout(request)
                return Response({'login': 1}, status=status.HTTP_401_UNAUTHORIZED)
            userid = the_user.id
            avatar_url = the_user.avatar_url
            return Response({'login':0, 'usertype':usertype, 'userid':userid, 'avatar_url': avatar_url}, status=status.HTTP_200_OK)
        else:
            return Response({'login':1}, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):

    def get(self, request):

        if request.user.is_authenticated():
            auth.logout(request)
            return Response({'logout':1}, status=status.HTTP_200_OK)
        else:
            return Response({'logout':0}, status=status.HTTP_401_UNAUTHORIZED)


class ForgetPassword(APIView):

    def post(self, request):
        email = request.data.get('email')
        users = User.objects.filter(email=email)
        if users:
            user = users[0]
            encode_username = make_password(user.username, 'b', 'pbkdf2_sha256')
            email_token = PasswordToken()
            email_token.username = user.username
            email_token.username_token = encode_username
            email_token.save()
            send_content = user.username + ' 您好\n您正在试图使用验证邮箱来修改您的iKNOW账户密码\n如确实是您本人操作，请点击以下链接进行密码修改\n' + MY_STATIC_URL + '/#/change_password/' + encode_username
            send_mail(u'请验证您的Email', send_content, 'iknow_cpcs@163.com', [email], fail_silently=False)
            return Response({'encode_string': encode_username}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):

    def post(self, request):
        encode_string = request.data.get('encode_id')
        if encode_string is None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        email_tokens = PasswordToken.objects.filter(username_token=encode_string)
        if not email_tokens:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        username = email_tokens[0].username
        user = User.objects.get(username=username)
        if user is not None:
            user.set_password(request.data['password'])
            user.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ValidateEmail(APIView):

    def post(self, request):
        encode_string = request.data.get('encode_id')
        if encode_string is None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        email_tokens = EmailToken.objects.filter(username_token=encode_string)
        if not email_tokens:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        username = email_tokens[0].username
        user = User.objects.get(username=username)
        if user is not None:
            if user.last_name == '1':
                return Response({'validate': 2}, status=status.HTTP_200_OK)
            user.last_name = '1'
            user.save()
            return Response({'validate': 1}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ConDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = ContestantUser.objects.all()
    serializer_class = ContestantUserSerializer
    permission_classes = (IsConOwnerOrReadOnly,)
    #@csrf_exempt

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class OrgDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = OrganizerUser.objects.all()
    serializer_class = OrganizerUserSerializer
    permission_classes = (IsOrgOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AvatarUpload(APIView):

    def post(self, request):
        user = request.user
        if request.user.is_authenticated():
            if user.first_name == 'contestant':
                the_user = user.contestant_user
            elif user.first_name == 'organizer':
                the_user = user.organizer_user
            else:
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)
            if the_user.avatar_url != 'static/static/avatar/default_avatar.jpg':
                os.remove('frontend/dist/' + the_user.avatar_url)
            image = request.data.get('file')
            present_time = str(int(time.time()))
            present_time.replace('.', '_')
            image_name = user.username + '_' + present_time + '.' + image.name.split('.')[-1]
            ava_file = open(os.path.join('frontend/dist/static/static/avatar', image_name), "wb")
            for chunk in image.chunks():
                ava_file.write(chunk)
            ava_file.close()
            the_user.avatar_url = 'static/static/avatar/' + image_name
            the_user.save()
            return Response({'avatar_url':the_user.avatar_url}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class MyCompetition(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        #if not user.is_authenticated():
        #    return Response({'return_code':0}, status=status.HTTP_401_UNAUTHORIZED)
        params = request.query_params.dict()
        competition_status = params.get('status')
        if user.first_name == "contestant":
            contestant_user = user.contestant_user
            if competition_status == '0':
                serializer = CompetitionSerializer(contestant_user.follow_competition.all(), many=True)
            else:
                serializer = CompetitionSerializer(contestant_user.join_competition.all(), many=True)
            competition = {'competitions': serializer.data}
            return Response(competition, status=status.HTTP_200_OK)
        elif user.first_name == "organizer":
            organizer_user = user.organizer_user
            serializer = CompetitionSerializer(organizer_user.competition.filter(status__exact=competition_status), many=True)
            competition = {'competitions': serializer.data}
            return Response(competition, status=status.HTTP_200_OK)
        return Response({'return_code':0}, status=status.HTTP_400_BAD_REQUEST)


class CollectCompetition(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        #user.is_authenticated() and
        if user.first_name == "contestant":
            contestant = user.contestant_user
            focus_status = request.data.get('status')
            competitions = Competition.objects.filter(id=request.data.get('competition_id'))
            if not competitions:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            competition = competitions[0]
            if focus_status == '1':
                contestant.follow_competition.add(competition)
            else:
                contestant.follow_competition.remove(competition)
            contestant.save()
            queryset = CompetitionAndContestant.objects.filter(competition=competition, contestant=contestant)
            if queryset:
                queryset[0].is_focus = focus_status
                queryset[0].save()
            else:
                competition_and_contestant = CompetitionAndContestant()
                competition_and_contestant.contestant = contestant
                competition_and_contestant.competition = competition
                competition_and_contestant.is_focus = focus_status
                competition_and_contestant.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class CollectTutorial(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        if user.first_name == "contestant":
            contestant = user.contestant_user
            collect_status = request.data.get('status')
            tutorials = Tutorial.objects.filter(id=request.data.get('tutorial_id'))
            if not tutorials:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            tutorial = tutorials[0]
            if collect_status == '1':
                contestant.collect_tutorial.add(tutorial)
            else:
                contestant.collect_tutorial.remove(tutorial)
            contestant.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class IsTutorial(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        params = request.query_params.dict()
        tutorials = Tutorial.objects.filter(id=params.get('tutorial_id'))
        if not tutorials:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        tutorial = tutorials[0]
        if request.user.first_name == 'contestant':
            tutorial_status = 0
            contestant = request.user.contestant_user
            if tutorial in contestant.collect_tutorial.all():
                tutorial_status = 1
            return Response({'tutorial_status': tutorial_status}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class MyPersonalLetter(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        user = request.user
        if user.is_authenticated():
            contacts = []
            for letter in user.receive_letter.all():
                contacts.append(letter.sender)
            for letter in user.send_letter.all():
                contacts.append(letter.receiver)
            mcontacts = list(set(contacts))
            mcontacts.sort(key=contacts.index)
            receivers = []
            for contact in mcontacts:
                letter = user.receive_letter.filter(sender__exact=contact) | user.send_letter.filter(receiver__exact=contact)
                letter = letter.order_by('-post_time')
                if contact.first_name == "contestant":
                    con_receiver_user = contact.contestant_user
                elif contact.first_name == "organizer":
                    con_receiver_user = contact.organizer_user
                else:
                    continue
                first_letter = letter[0]
                if first_letter.receiver == user:
                    is_other = 1
                else:
                    is_other = 0
                is_read = len(user.receive_letter.filter(sender__exact=contact).filter(is_read__exact=0))
                content = {'isread': is_read, 'isother': is_other, 'content': first_letter.content}
                author = UserShortSerializer(contact)
                receiver = {'author' : author.data, 'picurl': con_receiver_user.avatar_url, 'content': content}
                receivers.append(receiver)
            return Response({'receivers': receivers}, status=status.HTTP_200_OK)
        return Response({'return_code': 0}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):

        sender_user = request.user
        receiver_user = User.objects.get(id=request.data.get('id'))
        if not sender_user.is_authenticated():
            return Response({'return_code': 0}, status=status.HTTP_401_UNAUTHORIZED)
        personal_letter = PersonalLetter()
        personal_letter.sender = sender_user
        personal_letter.receiver = receiver_user
        personal_letter.content = request.data.get('content')
        personal_letter.is_read = 0
        personal_letter.save()
        return Response({'return_code': 1}, status=status.HTTP_201_CREATED)


class LetterDetail(APIView):

    def get(self, request):

        sender_user = request.user
        receiver_user = User.objects.get(id=request.query_params.dict().get('id'))

        if not sender_user.is_authenticated():
            return Response({'return_code': 0}, status=status.HTTP_401_UNAUTHORIZED)
        letters = sender_user.receive_letter.filter(sender__exact=receiver_user) | sender_user.send_letter.filter(receiver__exact=receiver_user)
        letters = letters.order_by('post_time')
        our_letters = []
        for letter in letters:
            if letter.receiver == sender_user:
                isother = 1
                letter.is_read = 1
                letter.save()
            else:
                isother = 0
            our_letters.append({'isother': isother, 'content': letter.content})
        response = {'our_letters':our_letters}
        return Response(response, status=status.HTTP_200_OK)


class OtherContestantCompetition(APIView):

    def get(self, request):

        contestants = ContestantUser.objects.filter(id=self.request.query_params.dict().get("id"))
        if not contestants:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        contestant = contestants[0]
        queryset = contestant.follow_competition
        serializer = CompetitionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OtherOrganizerCompetition(APIView):

    def get(self, request):

        organizers = OrganizerUser.objects.filter(id=self.request.query_params.dict().get("id"))
        if not organizers:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        organizer = organizers[0]
        queryset = organizer.competition
        serializer = CompetitionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OtherContestantTutorial(APIView):

    def get(self, request):

        contestants = ContestantUser.objects.filter(id=self.request.query_params.dict().get("id"))
        if not contestants:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        contestant = contestants[0].user
        queryset = contestant.tutorial
        serializer = TutorialSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OtherOrganizerTutorial(APIView):

    def get(self, request):

        organizers = OrganizerUser.objects.filter(id=self.request.query_params.dict().get("id"))
        if not organizers:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        organizer = organizers[0].user
        queryset = organizer.tutorial
        serializer = TutorialSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManagerLogin(APIView):

    def post(self, request):

        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.first_name == 'manager':
            auth.login(request, user)
            return Response({'login':0}, status=status.HTTP_200_OK)
        else:
            return Response({'login':1}, status=status.HTTP_401_UNAUTHORIZED)


class GetAudit(APIView):

    #permission_classes = (IsAuthenticated)

    def post(self, request):

        serializer = PostEventSerializer(data=request.data)
        if serializer.is_valid():
            phase = Phase.objects.all()[0]
            #phase = Phase.objects.get(id=request.data.get('phase_id'))
            if request.data.get('event_type') == '7':
                contestant = ContestantUser.objects.get(id=request.data.get('contestant_id'))
            else:
                contestant = request.user.contestant_user
            serializer.save(phase=phase, contestant=contestant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):

        params = request.query_params.dict()
        if request.user.first_name == 'manager':
            audit_query_set = AuditEvent.objects.all()
            audit_status = params.get('status')
            statuses = [1, 2, 3]
            if audit_status in statuses:
                audit_query_set = audit_query_set.filter(status__exact=audit_status)
            if len(audit_query_set) <= 0:
                return Response({}, status=status.HTTP_200_OK)
            current_page = int(params.get('current_page'))
            event_num = int(params.get('event_num'))
            min_num = event_num * (current_page - 1)
            max_num = event_num * current_page - 1
            if min_num >= 0 and max_num < len(audit_query_set):
                audit_query_set = audit_query_set[min_num:max_num + 1]
                serializer = AuditSerializer(audit_query_set, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif min_num >= 0 and max_num > len(audit_query_set) and min_num < len(audit_query_set):
                audit_query_set = audit_query_set[min_num:len(audit_query_set)]
                serializer = AuditSerializer(event_query_set, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class AuditNumber(APIView):

    def get(self, request):

        params = request.query_params.dict()
        if request.user.first_name == 'manager':
            audit_query_set = AuditEvent.objects.all()
            audit_status = params.get('status')
            statuses = [1, 2, 3]
            if audit_status in statuses:
                audit_query_set = audit_query_set.filter(status__exact=audit_status)
            return Response({'event_number': len(audit_query_set)}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class HandleAudit(APIView):

    #permission_classes = (IsAuthenticated)

    def post(self, request):

        audit = AuditEvent.objects.get(id=request.data.get('id'))
        if request.user.first_name == 'manager':
            audit.status = request.data.get('status')
            audit.reason = request.data.get('reason')
            audit.save()
            return Response({'status':audit.status, 'reason':audit.reason}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
